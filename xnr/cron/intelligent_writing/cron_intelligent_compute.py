# -*-coding:utf-8-*-

import os
import sys
import json
import time

from save_utils import save_intelligent_opinion_results,save2topic_es, save2models_text,save2opinion_corpus

sys.path.append('./public/')
from comment_module import comments_calculation_v2

sys.path.append('./fix/')
from fix_config import emotions_vk_v1

sys.path.append('/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/intelligent_writing/text_greneration/')
from text_generation import text_generation_main

sys.path.append('/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/intelligent_writing/summary_produce/')
from process_summary import summary_main

sys.path.append('/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/intelligent_writing/sub_opinion_analysis/')
from opinion_produce import opinion_main

sys.path.append('/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/intelligent_writing/opinion_question/')
from opinion_search import opinion_relevance

sys.path.append('../../')
from global_utils import R_WRITING as r_r
from global_config import S_TYPE, S_DATE, S_DATE_FB, S_DATE_TW, S_DATE_BCI
from global_utils import es_xnr, es_flow_text,es_intel, es_user_portrait, writing_task_queue_name,\
                    fb_bci_index_name_pre, fb_bci_index_type, tw_bci_index_name_pre, \
                    tw_bci_index_type, weibo_bci_index_name_pre, weibo_bci_index_type,\
                    weibo_xnr_fans_followers_index_name, weibo_xnr_fans_followers_index_type,\
                    fb_xnr_fans_followers_index_name, fb_xnr_fans_followers_index_type, \
                    tw_xnr_fans_followers_index_name, tw_xnr_fans_followers_index_name,\
                    writing_task_index_name, writing_task_index_type, topics_river_index_name,\
                    topics_river_index_type, intel_type_all, intel_type_follow, intel_type_influence,\
                    intel_type_sensitive, opinion_corpus_index_name, opinion_corpus_index_type

from flow_text_mappings import get_mappings
from timed_python_files.facebook_mappings import facebook_flow_text_mappings
from timed_python_files.twitter_mappings import twitter_flow_text_mappings
from time_utils import datetime2ts,ts2datetime,ts2datetime_full ,get_flow_text_index_list, fb_get_flow_text_index_list, tw_get_flow_text_index_list
from parameter import MAX_SEARCH_SIZE, SUB_OPINION_WEIBO_LIMIT, SENTIMENT_POS, SENTIMENT_NEG
sys.path.append('../trans/')
from trans import trans, simplified2traditional, traditional2simplified

NEWS_LIMIT = 200
default_cluster_eva_min_size = 5
default_vsm = 'v1'
LOG_FOLDER = '/home/ubuntu8/yuanhuiru/xnr/xnr1/log'

## 从redis队列中pop出任务，进行计算
def rpop_compute_intelligent_writing():

    while True:
        temp = r_r.rpop(writing_task_queue_name)

        print 'temp:::::',temp
        if not temp:
            print '当前没有智能写作推荐任务'         
            break
        task_detail = json.loads(temp)
        task_id = task_detail['task_id']
        #print 'task_detail::',task_detail

        print '把任务从队列中pop出来......'

        compute_intelligent_recommend(task_detail)

        es_xnr.update(index=writing_task_index_name,doc_type=writing_task_index_type,\
            id=task_id, body={'doc':{'compute_status':1}})


def news_content(task_source,task_id,news_limit = NEWS_LIMIT):

    if task_source == 'weibo':
        query_body ={'query':{
                        'bool':{
                            'must':[
                                {'wildcard':{'text':'*【*】*'}}
                                ]
                        }
                    },
                    'size':news_limit  
                    }
    else:
        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'wildcard':{'text':'*【*】*'}}
                        ]
                }
            },
            'sort':'share',
            'size':news_limit
        }

    news_results = es_intel.search(index=task_id,doc_type=task_source,body=query_body)['hits']['hits']#['_source']
    # print topic,weibo_index_type,start_ts,end_ts,query_body
    # print news_results
    news_list = []
    for key_weibo in news_results:
        text_weibo = key_weibo['_source']['text']
        uid = key_weibo['_source']['uid']
        timestamp = key_weibo['_source']['timestamp']
        comment = key_weibo['_source']['comment']

        if task_source == 'weibo':
            mid_weibo = key_weibo['_source']['mid']
            retweeted = key_weibo['_source']['retweeted']
        elif task_source == 'facebook':
            mid_weibo = key_weibo['_source']['fid']
            retweeted = key_weibo['_source']['share']
        else:
            mid_weibo = key_weibo['_source']['tid']
            retweeted = key_weibo['_source']['share']
        
        news_list.append({'news_id':'news','content168':text_weibo,'id':mid_weibo,'datetime':ts2datetime_full(timestamp),'comment':comment,'retweeted':retweeted})
    return news_list

def find_flow_texts(task_source,task_id,event_keywords):

    # 得到nest_query_list
    nest_query_list = []

    keywords_list = event_keywords.split('&')
    keywords_list = [word.encode('utf-8') for word in keywords_list]
    query_item = 'text'
    if task_source != 'weibo':
        #文本中可能存在英文或者繁体字，所以都匹配一下
        
        en_keywords_list = trans(keywords_list, target_language='en')
        for i in range(len(keywords_list)):
            keyword = keywords_list[i].decode('utf-8')
            traditional_keyword = simplified2traditional(keyword)
            
            if len(en_keywords_list) == len(keywords_list): #确保翻译没出错
                en_keyword = en_keywords_list[i]
                nest_query_list.append({'wildcard':{query_item:'*'+en_keyword+'*'}})
            
            nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})
            nest_query_list.append({'wildcard':{query_item:'*'+traditional_keyword+'*'}})

    else:
        for keyword in keywords_list:
            nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})


    if len(nest_query_list) == 1:
        SHOULD_PERCENT = 1
    else:
        SHOULD_PERCENT = 1


    # 匹配文本
    if task_source == 'weibo':
        sort_item = 'retweeted'

        if S_TYPE == 'test':
            current_time = datetime2ts(S_DATE)
        else:
            current_time = int(time.time())

        index_name_list = get_flow_text_index_list(current_time,days=5)
        es_name = es_flow_text

    elif task_source == 'facebook':
        sort_item = 'share'
        if S_TYPE == 'test':
            current_time = datetime2ts(S_DATE_FB)
        else:
            current_time = int(time.time())

        index_name_list = fb_get_flow_text_index_list(current_time,days=5)
        es_name = es_xnr

    else:
        sort_item = 'share'
        if S_TYPE == 'test':
            current_time = datetime2ts(S_DATE_TW)
        else:
            current_time = int(time.time())
        index_name_list = tw_get_flow_text_index_list(current_time,days=5)
        es_name = es_xnr

    query_body = {
        'query':{
            'bool':{
                'should':nest_query_list,
                'minimum_should_match': SHOULD_PERCENT
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':100000
    }

    search_results = es_name.search(index=index_name_list,doc_type='text',body=query_body)['hits']['hits']

    save2topic_es(task_source,task_id,search_results)


def get_topic_tweets(task_id, task_source, event_keywords, create_time):

    task_exist = es_intel.indices.exists(index=task_id)
    #print 'task_exist..',task_exist
    if not task_exist:
        if task_source == 'weibo':
            get_mappings(task_id,index_type='weibo')
        elif task_source == 'facebook':
            print facebook_flow_text_mappings(task_id,index_type='facebook')
        else:
            twitter_flow_text_mappings(task_id,index_type='twitter')

    find_flow_texts(task_source,task_id,event_keywords)


def news_comments_list(task_source,taskid,weibo_list,cluster_num=-1,cluster_eva_min_size=default_cluster_eva_min_size,vsm=default_vsm,calculation_label=1):#weibo_list把微博读进来
    """计算饼图数据，并将饼图数据和去重后的推荐文本写到文件
    """
    
    print 'weibo_list..len...',len(weibo_list)
    params = {"taskid": taskid, "cluster_num": cluster_num, "cluster_eva_min_size": cluster_eva_min_size, \
            "vsm": vsm, "calculation_label": calculation_label}

    comments = weibo_list
    logfile = os.path.join(LOG_FOLDER, taskid + '.log')

    cal_results = comments_calculation_v2(comments, logfile=logfile, cluster_num=cluster_num, \
            cluster_eva_min_size=int(cluster_eva_min_size), version=vsm)
    #print cal_results
    features = cal_results['cluster_infos']['features']
    item_infos = cal_results['item_infos']
    cluster_ratio = dict()
    senti_ratio = dict()
    sentiment_results = dict()
    cluster_results = dict()
    rub_results = []

    # 过滤前文本数
    before_filter_count = len(item_infos)
    # 过滤后文本数
    after_filter_count = 0

    download_items = []
    for comment in item_infos:
        # print comment
        download_item = {}
        download_item["id"] = comment["id"]
        download_item["title"] = comment["title"]
        download_item["text"] = comment["text"]
        # download_item["timestamp"] = comment["timestamp"]
        download_item["datetime"] = comment["datetime"]
        download_item["clusterid"] = comment["clusterid"]
        download_item["sentiment"] = comment["sentiment"]
        download_item["ad_label"] = comment["ad_label"]
        if (comment["clusterid"][:8] != 'nonsense') and (comment["clusterid"] != 'other'):
            download_item["duplicate"] = comment["duplicate"]
            download_item["same_from"] = comment["same_from"]
        download_items.append(download_item)
        if ('clusterid' in comment) and (comment['clusterid'][:8] != 'nonsense') : 
            clusterid = comment['clusterid']

            try:
                cluster_ratio[clusterid] += 1
            except KeyError:
                cluster_ratio[clusterid] = 1
            try:
                cluster_results[clusterid].append(comment)
            except KeyError:
                cluster_results[clusterid] = [comment]

        if ('sentiment' in comment) and (comment['sentiment'] in emotions_vk_v1) and ('clusterid' in comment) \
                and (comment['clusterid'][:8] != 'nonsense'):
            sentiment = comment['sentiment']

            try:
                senti_ratio[sentiment] += 1
            except KeyError:
                senti_ratio[sentiment] = 1
            try:
                sentiment_results[sentiment].append(comment)
            except KeyError:
                sentiment_results[sentiment] = [comment]

            after_filter_count += 1

        if comment['clusterid'][:8] == 'nonsense':
            rub_results.append(comment)

    ratio_results = dict()
    ratio_total_count = sum(cluster_ratio.values())
    for clusterid, ratio in cluster_ratio.iteritems():
        if clusterid in features:
            feature = features[clusterid]
            if feature and len(feature):
                ratio_results[','.join(feature[:3])] = float(ratio) / float(ratio_total_count)

    sentiratio_results = dict()
    sentiratio_total_count = sum(senti_ratio.values())
    for sentiment, ratio in senti_ratio.iteritems():
        if sentiment in emotions_vk_v1:
            label = emotions_vk_v1[sentiment]
            if label and len(label):
                sentiratio_results[label] = float(ratio) / float(sentiratio_total_count)

    # 情感分类去重
    sentiment_dump_dict = dict()
    for sentiment, contents in sentiment_results.iteritems():
        dump_dict = dict()
        for comment in contents:
            same_from_sentiment = comment["same_from_sentiment"]
            try:
                dump_dict[same_from_sentiment].append(comment)
            except KeyError:
                dump_dict[same_from_sentiment] = [comment]
        sentiment_dump_dict[sentiment] = dump_dict

    # 子观点分类去重
    cluster_dump_dict = dict()
    for clusterid, contents in cluster_results.iteritems():
        if clusterid in features:
            feature = features[clusterid]
            if feature and len(feature):
                dump_dict = dict()
                for comment in contents:
                    same_from_cluster = comment["same_from"]
                    try:
                        dump_dict[same_from_cluster].append(comment)
                    except KeyError:
                        dump_dict[same_from_cluster] = [comment]
                    for k,v in dump_dict.iteritems():
                        sort_dump_dict = sorted(v,key=lambda x:x['weight'],reverse=True)
                    cluster_dump_dict[clusterid] = sort_dump_dict


    #task = taskid.split('_')
    index_body={'name':taskid,'features':json.dumps(features),'cluster_dump_dict':json.dumps(cluster_dump_dict)}
    es_intel.index(index=topics_river_index_name,doc_type=topics_river_index_type,id=taskid,body=index_body)

    return json.dumps({"features":features, "cluster_dump_dict":cluster_dump_dict})


def get_opinions(task_source,task_id,xnr_user_no,opinion_keywords_list,opinion_type,intel_type):

    query_item = 'text'
    nest_query_list = []
    tweets_list = []
    if task_source == 'weibo':

        if S_TYPE == 'test':
            current_time = datetime2ts(S_DATE)
                
        else:
            current_time = int(time.time())

        index_name_list = get_flow_text_index_list(current_time,days=5)
        sort_item = 'retweeted'
        for keyword in opinion_keywords_list:
            nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})
        uid_list = []
        
        if len(nest_query_list) == 1:
            SHOULD_PERCENT = 1
        else:
            SHOULD_PERCENT = 1

        if intel_type == 'all':
            query_body = {
                'query':{
                    'bool':{
                        'should':nest_query_list,
                        'minimum_should_match': SHOULD_PERCENT
                    }
                },
                'sort':{sort_item:{'order':'desc'}},
                'size':MAX_SEARCH_SIZE
            }

        elif intel_type == 'follow':

            try:
                follow_results = es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no)['_source']

                if follow_results:
                    for follow_result in follow_results:
                        uid_list = follow_result['_source']['followers']
            except:
                uid_list = []
                
            
            query_body = {
                'query':{
                    'bool':{
                        'should':nest_query_list,
                        'minimum_should_match': SHOULD_PERCENT,
                        'must':[{'terms':{'uid':uid_list}}]
                    }
                },
                'sort':{sort_item:{'order':'desc'}},
                'size':MAX_SEARCH_SIZE
            }

        elif intel_type == 'influence':
            date = ts2datetime(current_time)

            if S_TYPE == 'test':
                date = S_DATE_BCI
            
            weibo_bci_index_name = weibo_bci_index_name_pre + date[:4] + date[5:7] + date[8:10]

            query_body_bci = {
                'query':{
                    'match_all':{}
                },
                'sort':{'user_index':{'order':'desc'}},
                'size':500
            }

            weino_bci_results = es_user_portrait.search(index=weibo_bci_index_name,doc_type=weibo_bci_index_type,body=query_body_bci)['hits']['hits']
            if weino_bci_results:
                for bci_result in weino_bci_results:
                    uid = bci_result['_source']['user']
                    uid_list.append(uid)

            query_body = {
                'query':{
                    'bool':{
                        'should':nest_query_list,
                        'minimum_should_match': SHOULD_PERCENT,
                        'must':[{'terms':{'uid':uid_list}}]
                    }
                },
                'sort':{sort_item:{'order':'desc'}},
                'size':MAX_SEARCH_SIZE
            }

        else:

            query_sensitive = {
                'query':{
                    'match_all':{}
                },
                "aggs" : {
                    "uids" : {
                        "terms" : {
                          "field" : "uid",
                          "order": {
                            "avg_sensitive" : "desc" 
                          }
                        },
                        "aggs": {
                            "avg_sensitive": {
                                "avg": {"field": "sensitive"} 
                            }
                        }
                    }
                },
                'size':500
            }

            es_sensitive_result = es_flow_text.search(index=index_name_list,doc_type='text',\
                    body=query_sensitive)['aggregations']['uids']['buckets']
            for item in es_sensitive_result:
                uid = item['key']
                uid_list.append(uid)
            
            query_body = {
                'query':{
                    'bool':{
                        'should':nest_query_list,
                        'minimum_should_match': SHOULD_PERCENT,
                        'must':[{'terms':{'uid':uid_list}}]
                    }
                },
                'sort':{sort_item:{'order':'desc'}},
                'size':MAX_SEARCH_SIZE
            }


        # 得到tweets_list

        tweets_results = es_flow_text.search(index=index_name_list,doc_type='text',body=query_body)['hits']['hits']

        if tweets_results:
            for item in tweets_results:
                item = item['_source']
                weibo = item['text']
                tweets_list.append(weibo)

    else:
        if S_TYPE == 'test':
            current_time = datetime2ts(S_DATE_FB)
        else:
            current_time = int(time.time())
        uid_list = []
        sort_item = 'share'
        opinion_keywords_list = [word.encode('utf-8') for word in opinion_keywords_list]
        en_keywords_list = trans(opinion_keywords_list, target_language='en')
        for i in range(len(opinion_keywords_list)):
            keyword = opinion_keywords_list[i].decode('utf-8')
            traditional_keyword = simplified2traditional(keyword)
            
            if len(en_keywords_list) == len(opinion_keywords_list): #确保翻译没出错
                en_keyword = en_keywords_list[i]
                nest_query_list.append({'wildcard':{query_item:'*'+en_keyword+'*'}})
            
            nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})
            nest_query_list.append({'wildcard':{query_item:'*'+traditional_keyword+'*'}})

        if len(nest_query_list) == 1:
            SHOULD_PERCENT = 1
        else:
            SHOULD_PERCENT = 1

        if task_source == 'facebook':
            index_name_list = fb_get_flow_text_index_list(current_time,days=5)

            if intel_type == 'all':
                query_body = {
                    'query':{
                        'bool':{
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT
                        }
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            elif intel_type == 'follow':

                try:
                    follow_results = es_xnr.get(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
                        id=xnr_user_no)['_source']

                    if follow_results:
                        for follow_result in follow_results:
                            uid_list = follow_result['_source']['fans_list']
                except:
                    uid_list = []

                query_body = {
                    'query':{
                        'bool':{
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT,
                            'must':[{'terms':{'uid':uid_list}}]
                        }
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            elif intel_type == 'influence':
                fb_bci_index_name = fb_bci_index_name_pre + ts2datetime(current_time)
                query_body_bci = {
                    'query':{
                        'match_all':{}
                    },
                    'sort':{'influence':{'order':'desc'}},
                    'size':500
                }

                fb_bci_results = es_xnr.search(index=fb_bci_index_name,doc_type=fb_bci_index_type,body=query_body_bci)['hits']['hits']
                #print 'fb_bci_results...',len(fb_bci_results)
                if fb_bci_results:
                    for bci_result in fb_bci_results:
                        uid = bci_result['_source']['uid']
                        uid_list.append(uid)

                query_body = {
                    'query':{
                        'bool':{
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT,
                            'must':[{'terms':{'uid':uid_list}}]
                        }
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            else:

                query_sensitive = {
                    'query':{
                        'match_all':{}
                    },
                    "aggs" : {
                        "uids" : {
                            "terms" : {
                              "field" : "uid",
                              "order": {
                                "avg_sensitive" : "desc" 
                              }
                            },
                            "aggs": {
                                "avg_sensitive": {
                                    "avg": {"field": "sensitive"} 
                                }
                            }
                        }
                    },
                    'size':500
                }

                es_sensitive_result = es_xnr.search(index=index_name_list,doc_type='text',\
                        body=query_sensitive)['aggregations']['uids']['buckets']
                #print 'es_sensitive_result...',len(es_sensitive_result)
                for item in es_sensitive_result:
                    uid = item['key']
                    uid_list.append(uid)
                
                query_body = {
                    'query':{
                        'bool':{
                            
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT,
                            'must':[{'terms':{'uid':uid_list}}]
                            
                        } 
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            #print 'query_body...',query_body
            tweets_results = es_xnr.search(index=index_name_list,doc_type='text',body=query_body)['hits']['hits']

            if tweets_results:
                for item in tweets_results:
                    item = item['_source']
                    weibo = item['text']
                    tweets_list.append(weibo)

        else:
            index_name_list = tw_get_flow_text_index_list(current_time,days=5)

            if intel_type == 'all':
                query_body = {
                    'query':{
                        'bool':{
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT
                        }
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            elif intel_type == 'follow':

                try:
                    follow_results = es_xnr.get(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,\
                        id=xnr_user_no)['_source']

                    if follow_results:
                        for follow_result in follow_results:
                            uid_list = follow_result['_source']['followers_list']
                except:
                    uid_list = []

                query_body = {
                    'query':{
                        'bool':{
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT,
                            'must':[{'terms':{'uid':uid_list}}]
                        }
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            elif intel_type == 'influence':
                tw_bci_index_name = tw_bci_index_name_pre + ts2datetime(current_time)
                query_body_bci = {
                    'query':{
                        'match_all':{}
                    },
                    'sort':{'influence':{'order':'desc'}},
                    'size':500
                }

                tw_bci_results = es_xnr.search(index=tw_bci_index_name,doc_type=tw_bci_index_type,body=query_body_bci)['hits']['hits']
                if tw_bci_results:
                    for bci_result in tw_bci_results:
                        uid = bci_result['_source']['uid']
                        uid_list.append(uid)

                query_body = {
                    'query':{
                        'bool':{
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT,
                            'must':[{'terms':{'uid':uid_list}}]
                        }
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            else:

                query_sensitive = {
                    'query':{
                        'match_all':{}
                    },
                    "aggs" : {
                        "uids" : {
                            "terms" : {
                              "field" : "uid",
                              "order": {
                                "avg_sensitive" : "desc" 
                              }
                            },
                            "aggs": {
                                "avg_sensitive": {
                                    "avg": {"field": "sensitive"} 
                                }
                            }
                        }
                    },
                    'size':500
                }

                es_sensitive_result = es_xnr.search(index=index_name_list,doc_type='text',\
                        body=query_sensitive)['aggregations']['uids']['buckets']
                for item in es_sensitive_result:
                    uid = item['key']
                    uid_list.append(uid)
                
                query_body = {
                    'query':{
                        'bool':{
                            'should':nest_query_list,
                            'minimum_should_match': SHOULD_PERCENT,
                            'must':[{'terms':{'uid':uid_list}}]
                        }
                    },
                    'sort':{sort_item:{'order':'desc'}},
                    'size':MAX_SEARCH_SIZE
                }

            print 'index_name_list...',index_name_list
            print 'query_body........',query_body
            tweets_results = es_xnr.search(index=index_name_list,doc_type='text',body=query_body)['hits']['hits']

            if tweets_results:
                for item in tweets_results:
                    item = item['_source']
                    weibo = item['text']
                    tweets_list.append(weibo)

    if tweets_list:
        opinion_name,word_result,text_list = opinion_main(tweets_list,k_cluster=5)
        sub_opinion_results = dict()

        topic_keywords_list = []
        summary_text_list = []

        for topic, text in text_list.iteritems():
            
            topic_name = opinion_name[topic]
            sub_opinion_results[topic_name] = text[:SUB_OPINION_WEIBO_LIMIT]

            topic_keywords_list.extend(topic_name.split('&'))
            summary_text_list.extend(text)

        #try:
        print 'summary_text_list..',len(summary_text_list)
        print 'topic_keywords_list..',topic_keywords_list
        summary = text_generation_main(summary_text_list,topic_keywords_list)
        #summary = summary_main(summary_text_list)
        #except:
        #    summary = ''
            
    else:
        sub_opinion_results = {}
        summary = ''

    print '开始保存子观点计算结果......'
    print 'summary....',summary
    mark = save_intelligent_opinion_results(task_id,sub_opinion_results,summary,intel_type)

    return mark
    

def get_models_text(task_id,task_source,opinion_keywords_list):

    if task_source == 'weibo':
        sort_item = 'retweeted'
    else:
        sort_item = 'share'

    query_body_pos = {
        'query':{
            'terms':{'sentiment':SENTIMENT_POS}
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    query_body_neg = {
        'query':{
            'terms':{'sentiment':SENTIMENT_NEG}
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    query_body_news = {
        'query':{
            'bool':{
                'must':[
                    {'wildcard':{'text':'*【*】*'}}
                    ]
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    results_pos = es_intel.search(index=task_id,doc_type=task_source,body=query_body_pos)['hits']['hits']
    results_neg = es_intel.search(index=task_id,doc_type=task_source,body=query_body_neg)['hits']['hits']
    results_news = es_intel.search(index=task_id,doc_type=task_source,body=query_body_news)['hits']['hits']

    text_list_pos = []
    text_list_neg = []
    text_list_news = []

    for result_pos in results_pos:
        text_list_pos.append(result_pos['_source']['text'])

    for result_neg in results_neg:
        text_list_neg.append(result_neg['_source']['text'])
    
    for result_news in results_news:
        text_list_news.append(result_news['_source']['text'])

    model_text_dict = {}

    model_text_pos = text_generation_main(text_list_pos,opinion_keywords_list)
    model_text_neg = text_generation_main(text_list_neg,opinion_keywords_list)
    model_text_news = text_generation_main(text_list_news,opinion_keywords_list)

    model_text_dict['model_text_pos'] = model_text_pos
    model_text_dict['model_text_neg'] = model_text_neg
    model_text_dict['model_text_news'] = model_text_news

    print 'model_text_dict..',model_text_dict
    
    save2models_text(task_id,model_text_dict)

def opinion_relevance_main(task_source,task_id,xnr_user_no,opinion_keywords_list):

    query_body = {
        'query':{
            'match_all':{}
        },
        'size':MAX_SEARCH_SIZE
    }

    results = es_xnr.search(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,body=query_body)['hits']['hits']

    opinion_results = {}

    for result in results:

        corpus_pinyin = result['_source']['corpus_pinyin']
        corpus_name = result['_source']['corpus_name']

        item_result = opinion_relevance(opinion_keywords_list,corpus_pinyin)
        #opinion_results[corpus_pinyin] = [corpus_name,item_result[0]]
        opinion_results[corpus_name] = item_result[0]

    save2opinion_corpus(task_id,opinion_results)
    print 'opinion_results....',opinion_results
    #return opinion_results

def compute_intelligent_recommend(task_detail):

    # 修改task_list


    task_id = task_detail['task_id']
    #task_name = task_detail['task_name']
    #task_name_pinyin = task_detail['task_name_pinyin']
    task_source = task_detail['task_source']
    event_keywords = task_detail['event_keywords']
    create_time = task_detail['create_time']

    # 根据对应主题把事件相关帖子都找出来，并一个事件存为一个index,不同渠道用task_source做为index_type
    print 'find flow text...'
    get_topic_tweets(task_id, task_source, event_keywords, create_time)

    # 主题河
    print 'start compute topic river...'
    news_list = news_content(task_source,task_id,NEWS_LIMIT)   #读新闻微博
    news_classify = json.loads(news_comments_list(task_source,task_id,weibo_list=news_list))  #聚类后存到es里

    news_topics = news_classify['features']

    print 'topic river over...'
    ##按类分时间段对应的微博数 -- 直接 从es中统计
    #zhutihe_results = cul_key_weibo_time_count(task_id,news_topics,start_ts,over_ts,during)

    # 时间轴 -- 直接从es中统计

    #fish_topics = news_classify['cluster_dump_dict']

    # 代表观点\关注人群观点(从关注列表中圈人)\高影响力用户观点(从bci中圈人)\高敏感度用户观点(聚合sensitive圈人)

    xnr_user_no = task_detail['xnr_user_no']
    opinion_type = task_detail['opinion_type']
    opinion_keywords = task_detail['opinion_keywords']
    opinion_keywords_list = opinion_keywords.split('&')
    print 'start compute opinions...'
    get_opinions(task_source,task_id,xnr_user_no,opinion_keywords_list,opinion_type,intel_type_all)
    print 'compute all opinions over...'
    get_opinions(task_source,task_id,xnr_user_no,opinion_keywords_list,opinion_type,intel_type_follow)
    print 'compute follow opinions over...'
    get_opinions(task_source,task_id,xnr_user_no,opinion_keywords_list,opinion_type,intel_type_influence)
    print 'compute influence opinions over...'
    get_opinions(task_source,task_id,xnr_user_no,opinion_keywords_list,opinion_type,intel_type_sensitive)
    print 'compute sensitive opinions over...'

    # 观点语料库
    opinion_relevance_main(task_source,task_id,xnr_user_no,opinion_keywords_list)
    print 'compute opinion corpus over...'

    # 智能发帖模板文本生成 -- 正向、负向、事实陈述
    get_models_text(task_id,task_source,opinion_keywords_list)

    return []
