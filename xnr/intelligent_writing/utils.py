#-*- coding:utf-8 -*-
import os
import time
import json
import sys
import random
import re
import pinyin

from xnr.global_config import S_TYPE,S_DATE,S_DATE_FB
from xnr.global_utils import es_xnr as es, es_intel, R_ADMIN as r_sensitive, writing_task_index_name, writing_task_index_type,\
                        topics_river_index_name, topics_river_index_type, intel_opinion_results_index_name,\
                        intel_models_text_index_name, intel_models_text_index_type, opinion_corpus_index_name,\
                        opinion_corpus_index_type, opinion_corpus_results_index_name, opinion_corpus_results_index_type

from xnr.parameter import MAX_SEARCH_SIZE, sensitive_score_dict
from time_utils import ts2HourlyTime, ts2datetime, datetime2ts, full_datetime2ts
from DFA_filter import createWordTree, searchWord

MinInterval = 15*60 #15min
Day = 24*3600

def get_create_writing_task(task_detail):
    
    task_source = task_detail['task_source']
    task_name_pinyin = task_detail['task_name_pinyin']
    xnr_user_no = task_detail['xnr_user_no']
    task_id = task_source + '_' + xnr_user_no.lower() + '_' + task_name_pinyin

    try:
        es.get(index=writing_task_index_name,doc_type=writing_task_index_type,\
            id=task_id)['_source']

        return 'exists'

    except:
        item_dict = dict()
        item_dict['task_id'] = task_id
        item_dict['xnr_user_no'] = xnr_user_no
        item_dict['task_name'] = task_detail['task_name']
        item_dict['task_name_pinyin'] = task_detail['task_name_pinyin']
        item_dict['event_keywords'] = '&'.join(task_detail['event_keywords'].encode('utf-8').split('，'))
        item_dict['opinion_keywords'] = '&'.join(task_detail['opinion_keywords'].encode('utf-8').split('，'))
        item_dict['opinion_type'] = task_detail['opinion_type']
        item_dict['create_time'] = task_detail['create_time']
        item_dict['submitter'] = task_detail['submitter']
        item_dict['compute_status'] = task_detail['compute_status']
        item_dict['task_source'] = task_detail['task_source']
        try:
            es.index(index=writing_task_index_name,doc_type=writing_task_index_type,id=task_id,body=item_dict)
            return True

        except:
            return False

def get_show_writing_task(task_detail):

    xnr_user_no = task_detail['xnr_user_no']
    task_source = task_detail['task_source']

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_user_no':xnr_user_no}},
                    {'term':{'task_source':task_source}}
                ]
            }
        },
        'size':MAX_SEARCH_SIZE,
        'sort':{'create_time':{'order':'desc'}}
    }

    search_results = es.search(index=writing_task_index_name,doc_type=writing_task_index_type,\
        body=query_body)['hits']['hits']

    results = []
    if search_results:
        for result in search_results:
            result = result['_source']
            results.append(result)

    return results

def get_delete_writing_task(task_detail):

    task_id = task_detail['task_id']

    try:
        es.delete(index=writing_task_index_name,doc_type=writing_task_index_type,\
        id=task_id)
        mark = True
    except:
        mark = False

    return mark


# 主题河
def get_topics_river(task_source, task_id,start_ts,end_ts,unit=MinInterval):#主题河
    #topic='event'
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'name':task_id}}
                ]
            }
        }
    }
    
    news_topics = json.loads(es_intel.search(index=topics_river_index_name,doc_type=topics_river_index_type,body=query_body)['hits']['hits'][0]['_source']['features'])
    zhutihe_results = cul_key_weibo_time_count(task_source, task_id,news_topics,start_ts,end_ts,unit)
    results = {}
    for k,v in news_topics.iteritems():
        if len(v)>0:
            results[v[0]] = zhutihe_results[k]
    return results


def cul_key_weibo_time_count(task_source, task_id,news_topics,start_ts,over_ts,during):

    if S_TYPE == 'test':
        if task_source == 'weibo':
            start_ts = datetime2ts(S_DATE) - 5*24*3600
            over_ts = datetime2ts(S_DATE)
        else:
            start_ts = datetime2ts(S_DATE_FB) - 5*24*3600
            over_ts = datetime2ts(S_DATE_FB)

    key_weibo_time_count = {}
    time_dict = {}
    during = Day
    for clusterid,keywords in news_topics.iteritems(): #{u'd2e97cf7-fc43-4982-8405-2d215b3e1fea': [u'\u77e5\u8bc6', u'\u5e7f\u5dde', u'\u9009\u624b']}
        if len(keywords)>0:
            start_ts = int(start_ts)
            over_ts = int(over_ts)

            over_ts = ts2HourlyTime(over_ts, during)
            interval = (over_ts - start_ts) / during


            for i in range(interval, 0, -1):    #时间段取每900秒的

                begin_ts = over_ts - during * i
                end_ts = begin_ts + during
                must_list=[]
                must_list.append({'range':{'timestamp':{'gte':begin_ts,'lt':end_ts}}})
                temp = []
                for word in keywords:
                    sentence =  {'wildcard':{'keywords_string':'*'+word+'*'}}
                    temp.append(sentence)
                must_list.append({'bool':{'should':temp}})

                query_body = {'query':{
                                'bool':{
                                    'must':must_list
                                }
                            }
                        }
                key_weibo = es_intel.search(index=task_id,doc_type=task_source,body=query_body)
                key_weibo_count = key_weibo['hits']['total']  #分时间段的类的数量
                time_dict[ts2datetime(end_ts)] = key_weibo_count

            key_weibo_time_count[clusterid] = sorted(time_dict.items(),key=lambda x:x[0])
    return key_weibo_time_count

# 鱼骨图
def get_symbol_weibo(task_source, task_id,start_ts,end_ts,unit=MinInterval):  #鱼骨图

    if S_TYPE == 'test':
        if task_source == 'weibo':
            start_ts = datetime2ts(S_DATE) - 5*24*3600
            over_ts = datetime2ts(S_DATE)
        else:
            start_ts = datetime2ts(S_DATE_FB) - 5*24*3600
            over_ts = datetime2ts(S_DATE_FB)


    weibos = {}
    
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'name':task_id}}
                ]
            }
        }
    }
    
    
    print query_body
    symbol = es_intel.search(index=topics_river_index_name,doc_type=topics_river_index_type,body=query_body)['hits']['hits']
    print 'symbol..',symbol
    symbol = es_intel.search(index=topics_river_index_name,doc_type=topics_river_index_type,body=query_body)['hits']['hits'][0]['_source']
    #symbol = es.search(index=topics_river_index_name,doc_type=topics_river_index_type,body=query_body)['hits']['hits']
    print 'symbol:::',symbol
    features = json.loads(symbol['features'])
    symbol_weibos = json.loads(symbol['cluster_dump_dict'])
    #print symbol_weibos
    begin_ts = end_ts - unit
    for clusterid,contents in symbol_weibos.iteritems():
        j = 0
        content = set()
        for i in contents:

            ts = full_datetime2ts(i['datetime'])
            
            title = re.findall(r'【.*】',i['content'].encode('utf8'))
            if title:
                title = title[0]

                print 'title::',title.encode('utf-8')
                if ts >= start_ts and ts <= end_ts and title not in content:  #start_ts应该改成begin_ts，现在近15分钟没数据，所以用所有的
                    try:
                        weibos[features[clusterid][0]].append(i)
                    except:
                        weibos[features[clusterid][0]] = [i]
                    content.add(title)
                    j += 1
                #print content
                if j == 3:
                    break
            else:
                continue
    #print weibos
    return weibos


def get_opinions_results(task_id,intel_type):
        
    try:
        results = es_intel.get(index=intel_opinion_results_index_name,doc_type=intel_type,id=task_id)['_source']
    except:
        results = {}

    return results


def get_model_text_results(task_detail):    

    text = ''

    try:
        task_id = task_detail['task_id']
        model_type = task_detail['model_type']
        #polar_type = task_detail['polar_type']
        text_type = task_detail['text_type']
        double_order = task_detail['double_order']


        results = es_intel.get(index=intel_models_text_index_name,doc_type=intel_models_text_index_type,id=task_id)['_source']

        model_text_pos = results['model_text_pos']
        model_text_neg = results['model_text_neg']
        model_text_news = results['model_text_news']

        if model_type == 'single':
            # if polar_type == 'agree' and text_type == 'positive':
            #     text = '我觉得有道理。' + model_text_pos

            # elif polar_type == 'agree' and text_type == 'negtive':
            #     text = '我觉得有道理。但是' + model_text_neg

            # elif polar_type == 'agree' and text_type == 'positive':
            #     text = '不太同意。但是' + model_text_pos

            # else:
            #     text = '不太同意。' + model_text_neg

            if text_type == 'positive':
            	text = model_text_pos
            else:
            	text = model_text_neg


        elif model_type == 'double':

            if double_order == 'although_positive':
                text = '虽然'+ model_text_pos + '。但是，' + model_text_neg
            else:
                text = '虽然'+ model_text_neg + '。但是，' + model_text_pos

        else:
            if text_type == 'positive':
                text = model_text_news + '。' + model_text_pos
            else:
                text = model_text_news + '。' + model_text_neg

    except:
        pass

    return text


def get_add_opinion_corpus(task_detail):

    mark = False

    corpus_name = task_detail['corpus_name']
    corpus_pinyin = pinyin.get(corpus_name,format='strip',delimiter='_')

    item_dict = {}
    item_dict['corpus_name'] = corpus_name
    item_dict['corpus_pinyin'] = corpus_pinyin
    item_dict['submitter'] = task_detail['submitter']

    try:
        es.get(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,id=corpus_pinyin)

        return 'exists'

    except:

        try:
            es.index(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,body=item_dict,id=corpus_pinyin)
            mark = True

        except:
            pass

    return mark


def get_delete_opinion_corpus(task_detail):

    mark = False

    corpus_name = task_detail['corpus_name']
    corpus_pinyin = pinyin.get(corpus_name,format='strip',delimiter='_')

    try:
        es.delete(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,id=corpus_pinyin)
        mark = True

    except:
        pass

    return mark


def get_show_opinion_corpus_name():

    query_body = {
        'query':{
            'match_all':{}
        },
        'size':MAX_SEARCH_SIZE
    }

    results = es.search(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,body=query_body)['hits']['hits']

    item_dict = {}

    for result in results:
        result = result['_source']
        corpus_pinyin = result['corpus_pinyin']
        corpus_name = result['corpus_name']
        item_dict[corpus_name] = corpus_pinyin

    return item_dict

def get_show_opinion_corpus_content(task_detail):

    task_id = task_detail['task_id']
    corpus_name = task_detail['corpus_name']
    get_result = es.get(index=opinion_corpus_results_index_name,doc_type=opinion_corpus_results_index_type)['result']

    opinion_results = get_result['corpus_results']

    return opinion_results[corpus_name]


def get_one_click_evaluation(task_detail):

    results = []
    text = task_detail['text'].encode('utf-8')

    node = createWordTree();
    print 'text...',text
    sensitive_words_dict = searchWord(text, node)
    print 'sensitive_words_dict..',sensitive_words_dict
    if sensitive_words_dict:
        score = 0
        sensitive_words_list = []

        for k,v in sensitive_words_dict.iteritems():
            tmp_stage = r_sensitive.hget("sensitive_words", k)
            if tmp_stage:
                score += v*sensitive_score_dict[str(tmp_stage)]
            sensitive_words_list.append(k.decode('utf-8'))
        results.append(score)
        results.append(sensitive_words_list)

    else:
        results = [0,[]]

    return results
