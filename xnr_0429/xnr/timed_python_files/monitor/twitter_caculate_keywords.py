# -*- coding:utf-8 -*-

'''
compute keywords
'''
import json
import time
import sys
reload(sys)
sys.path.append('../../')
from global_config import S_TYPE
from time_utils import ts2datetime,datetime2ts
from global_utils import es_xnr_2,twitter_keyword_count_index_name,twitter_keyword_count_index_type,\
                             tw_xnr_fans_followers_index_name,tw_xnr_fans_followers_index_type,\
                             twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
                             tw_xnr_index_name,tw_xnr_index_type
                             
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from parameter import DAY
test_date = '2017-10-25'


def extract_keywords(w_text):

    tr4w = TextRank4Keyword()
    tr4w.analyze(text=w_text, lower=True, window=4)
    k_dict = tr4w.get_keywords(100, word_min_len=2)

    return k_dict

#查询虚拟人的关注用户列表
def lookup_xnr_concernedusers(xnr_user_no):
    try:
        result=es_xnr_2.get(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,id=xnr_user_no)
        followers_list=result['_source']['followers_list']
    except:
        followers_list=[]
    return followers_list


#按日期计算虚拟人的关键词
def xnr_keywords_compute(xnr_user_no):
    #查询好友列表
    followers_list=lookup_xnr_concernedusers(xnr_user_no)
    lookup_condition_list=[]
    print 'xnr_user_no, followers_list:', xnr_user_no, followers_list
    lookup_condition_list.append({'filtered':{'filter':{'bool':{'must':{'terms':{'uid':followers_list}}}}}})

    #根据日期确定查询表
    if S_TYPE == 'test':
        date_time = test_date
    else:
        now_time=int(time.time())
        date_time=ts2datetime(now_time)
    flow_text_index_name=twitter_flow_text_index_name_pre+date_time

    #按日期统计
    # print lookup_condition_list
    for item_condition in lookup_condition_list:
        query_body={
            'query':item_condition,
            'aggs':{
                'keywords':{
                    'terms':{
                        'field':'keywords_string',
                        'size': 1000
                    }
                }
            }
        }
        
        flow_text_exist=es_xnr_2.search(index=flow_text_index_name,doc_type=twitter_flow_text_index_type,\
               body=query_body)['aggregations']['keywords']['buckets']

        # print 'flow_text_exist:',flow_text_exist
        word_dict = dict()

        word_dict_new = dict()

        keywords_string = ''
        for item in flow_text_exist:
            word = item['key']
            count = item['doc_count']
            word_dict[word] = count

            keywords_string += '&'
            keywords_string += item['key']

        k_dict = extract_keywords(keywords_string)

        for item_item in k_dict:
            keyword = item_item.word
            # print 'keyword::',type(keyword)
            word_dict_new[keyword] = word_dict[keyword]
        

    return word_dict_new


#查询虚拟人列表
def lookup_xnr_user_list():
    query_body={
        'query':{
            'term':{'create_status':2}
        }
    }
    try:
        es_result=es_xnr_2.search(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_list=[]
        for item in es_result:
            xnr_user_list.append(item['_id'])
    except:
        xnr_user_list=[]
    return xnr_user_list


#组织查询和存储
def compute_keywords_mark():
    xnr_user_list=lookup_xnr_user_list()
    #xnr_user_list=['TXNR0001']
    print 'xnr_user_list:', xnr_user_list
    now_time=int(time.time()) - DAY
    date_time=ts2datetime(now_time)

    mark_list=[]
    for xnr_user_no in xnr_user_list:
        keywords_task_detail=dict()
        keyword_value_string=json.dumps(xnr_keywords_compute(xnr_user_no))
        keywords_task_detail['keyword_value_string']=keyword_value_string
        keywords_task_detail['xnr_user_no']=xnr_user_no
        #keywords_task_detail['date_time']=date_time
        #keywords_task_detail['timestamp']=datetime2ts(date_time)
        if S_TYPE == 'test':
            keywords_task_id = xnr_user_no + '_' + test_date
            keywords_task_detail['timestamp']=datetime2ts(test_date)
            keywords_task_detail['date_time']=test_date
            print 'keywords_task_detail:', test_date
        else:
            keywords_task_id=xnr_user_no+'_'+date_time
            keywords_task_detail['timestamp']=datetime2ts(date_time)
            keywords_task_detail['date_time']=date_time
            print 'keywords_task_detail:', date_time
        try:
            es_xnr_2.index(index=twitter_keyword_count_index_name,doc_type=twitter_keyword_count_index_type,body=keywords_task_detail,id=keywords_task_id)
            mark=True
        except:
            mark=False
        mark_list.append(mark)
    print 'mark_list:', mark_list
    return mark_list


if __name__ == '__main__':
    compute_keywords_mark()
