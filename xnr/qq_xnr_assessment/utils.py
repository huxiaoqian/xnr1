# -*-coding:utf-8-*-
import math
import time
from xnr.global_config import S_TYPE,QQ_S_DATE_NEW,QQ_GROUP_MESSAGE_START_DATE,QQ_S_DATE_ASSESSMENT,\
                    QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT
from xnr.global_utils import es_xnr,group_message_index_name_pre,group_message_index_type,\
                    qq_xnr_index_name,qq_xnr_index_type,qq_xnr_history_count_index_name,\
                    qq_xnr_history_count_index_type
from xnr.time_utils import datetime2ts,ts2datetime,get_groupmessage_index_list
from xnr.parameter import WEEK,DAY,MAX_SEARCH_SIZE


def get_influence_at_num(xnr_user_no,start_ts,end_ts):

    at_dict = {}
    at_dict['at_day'] = {}
    at_dict['at_total'] = {}

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_SEARCH_SIZE,
        'sort':{'timestamp':{'order':'asc'}}
    }

    search_results = es_xnr.search(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                    body=query_body)['hits']['hits']
    print 'search_results:::',search_results
    for result in search_results:
        
        result = result['_source']
        timestamp = result['timestamp']

        at_dict['at_day'][timestamp] = result['daily_be_at_num']
        at_dict['at_total'][timestamp] = result['total_be_at_num']
        at_dict['mark'] = result['influence']

    return at_dict

def get_influence_at_num_today(xnr_user_no):
    at_dict = {}
    at_dict['at_day'] = {}
    at_dict['at_total'] = {}
    # if S_TYPE == 'test':
    #     qq_number = '365217204'
    #     nickname = u'无'
    # else:
    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']
    nickname = get_result['nickname']
        
    # if S_TYPE == 'test':
    #     current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)
    # else:
    #     current_time = int(time.time())
    current_timestamp = int(time.time())
    current_date = ts2datetime(current_timestamp)
    current_time = datetime2ts(current_date)
    # #message_sstart_ts = datetime2ts(QQ_GROUP_MESSAGE_START_DATE)
    # if S_TYPE == 'test':
    #     group_message_index_list = ['group_message_2017-09-28']
    # else:
    group_message_index_list = get_groupmessage_index_list(QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT,ts2datetime(current_time))

    # for i in range(WEEK):
    #     current_time_new = current_time - i*DAY
    #     current_date = ts2datetime(current_time_new)
        
    #     #start_ts = current_time_new - i*DAY  # DAY=3600*24
    #     end_ts = current_time_new + DAY 
    #     print 'current_date::',current_date
    #     print 'end_ts::',end_ts
    #     print 'end_ts_date::',ts2datetime(end_ts)
    group_message_index_name = group_message_index_name_pre + current_date
    group_message_index_list = get_groupmessage_index_list(QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT,current_date)
        
    #虚拟人被@数量
    query_body_xnr = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_qq_number':qq_number}},
                    {'wildcard':{'text':'*'+'@ME'+'*'}}
                ]
            }
        }
    }
    # query_body_xnr = {
    #     'query':{
    #         'match_all':{}
    #     }
    # }
    
    try:
        results_xnr = es_xnr.count(index=group_message_index_name,doc_type=group_message_index_type,\
                    body=query_body_xnr)

        if results_xnr['_shards']['successful'] != 0:
           at_num_xnr = results_xnr['count']

        else:
            print 'es index rank error'
            at_num_xnr = 0
    except:
        at_num_xnr = 0
        
    # 截止目前所有被@总数
    query_body_total = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_qq_number':qq_number}},
                    {'wildcard':{'text':'*'+'@ME'+'*'}}
                ]
            }
        }
    }
    # query_body_total = {
    #     'query':{
    #         'match_all':{}
    #     }
    # }
    
    results_total = es_xnr.count(index=group_message_index_list,doc_type=group_message_index_type,\
                body=query_body_total)

    if results_total['_shards']['successful'] != 0:
        at_num_total = results_total['count']
    else:
        print 'es index rank error'
        at_num_total = 0

    at_dict['at_day'][current_time] = at_num_xnr
    at_dict['at_total'][current_time] = at_num_total

    # if i == (WEEK-1):
    query_body_total_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_qq_number':qq_number}},
                    {'wildcard':{'text':'*'+'@'+'*'}}
                ]
            }
        }
    }

    try:
        results_total_day = es_xnr.count(index=group_message_index_name,doc_type=group_message_index_type,\
                    body=query_body_total_day)

        if results_total_day['_shards']['successful'] != 0:
           at_num_total_day = results_total_day['count']
        else:
            print 'es index rank error'
            at_num_total_day = 0
    except:
        at_num_total_day = 0

    influence = (float(math.log(at_num_xnr+1))/(math.log(at_num_total_day+1)+1))*100

    influence = round(influence,2)  # 保留两位小数
    
    at_dict['mark'] = influence

    return at_dict

def get_penetration_qq(xnr_user_no,start_ts,end_ts):

    follow_group_sensitive = {}
    follow_group_sensitive['sensitive_info'] = {}

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_SEARCH_SIZE,
        'sort':{'timestamp':{'order':'asc'}}
    }

    search_results = es_xnr.search(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                    body=query_body)['hits']['hits']

    for result in search_results:
        
        result = result['_source']
        timestamp = result['timestamp']

        follow_group_sensitive['sensitive_info'][timestamp] = result['daily_sensitive_num']
        follow_group_sensitive['mark'] = result['penetration']

    return follow_group_sensitive

def get_penetration_qq_today(xnr_user_no):

    follow_group_sensitive = {}
    follow_group_sensitive['sensitive_info'] = {}

    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']
    nickname = get_result['nickname']
    
    group_list = get_result['qq_groups']

    # if S_TYPE == 'test':
    #     current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)
    # else:
    #     current_time = int(time.time())

    current_timestamp = int(time.time())
    current_date = ts2datetime(current_timestamp)
    current_time = datetime2ts(current_date)

    # for i in range(WEEK):
    #     current_time_new = current_time - i*DAY
    #     current_date = ts2datetime(current_time_new)
        
    #     start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
    #     end_ts = current_time_new - i*DAY 
        
    group_message_index_name = group_message_index_name_pre + current_date


    query_body_info = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'qq_group_number':group_list}
                }
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive_value'
                }
            }
        }
    }
    try:
        es_sensitive_result = es_xnr.search(index=group_message_index_name,doc_type=group_message_index_type,\
            body=query_body_info)['aggregations']
        sensitive_value = es_sensitive_result['avg_sensitive']['value']
        
        if sensitive_value == None:
            sensitive_value = 0.0
        follow_group_sensitive['sensitive_info'][current_time] = sensitive_value
    except:
        follow_group_sensitive['sensitive_info'][current_time] = 0

    # if i == (WEEK-1):
    query_body_max = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'qq_group_number':group_list}
                }
            }
        },
        'sort':{'sensitive_value':{'order':'desc'}}
    }
    try:
        max_results = es_xnr.search(index=group_message_index_name,doc_type=group_message_index_type,\
                        body=query_body_max)['hits']['hits']

        max_sensitive = max_results[0]['_source']['sensitive_value']
    except:
        max_sensitive = 0

    penetration = (math.log(sensitive_value+1)/(math.log(max_sensitive+1)+1))*100
    penetration = round(penetration,2)
    
    follow_group_sensitive['mark'] = penetration

    return follow_group_sensitive

def get_safe_qq(xnr_user_no,start_ts,end_ts):

    speak_dict = {}
    speak_dict['speak_day'] = {}
    speak_dict['speak_total'] = {}

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_SEARCH_SIZE,
        'sort':{'timestamp':{'order':'asc'}}
    }

    search_results = es_xnr.search(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                    body=query_body)['hits']['hits']

    for result in search_results:
        
        result = result['_source']
        timestamp = result['timestamp']

        speak_dict['speak_day'][timestamp] = result['daily_post_num']
        speak_dict['speak_total'][timestamp] = result['total_post_num']
        speak_dict['mark'] = result['safe']

    return speak_dict

def get_safe_qq_today(xnr_user_no):
    # speak_dict = {}
    # speak_dict['speak_day'] = {}
    # speak_dict['speak_total'] = {}
    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']

    current_timestamp = int(time.time())
    current_date = ts2datetime(current_timestamp)
    current_time = datetime2ts(current_date)
    #group_message_index_list = get_groupmessage_index_list(QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT,ts2datetime(current_time))
    #for i in range(WEEK):
    # current_time_new = current_time-DAY
    # current_date_new = ts2datetime(current_time_new)

    #_id_last = xnr_user_no +'_'+ current_date_new
    
    group_message_index_name = group_message_index_name_pre + current_date

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'speaker_qq_number':qq_number}},
                    {'term':{'xnr_qq_number':qq_number}}
                ]
            }
        }
    }

    count_result = es_xnr.count(index=group_message_index_name,doc_type=group_message_index_type,body=query_body)

    if count_result['_shards']['successful'] != 0:
        today_count = count_result['count']
    else:
        print 'es index rank error'
        today_count = 0
    last_date = ts2datetime(current_time-DAY)
    _id_last = xnr_user_no +'_'+ last_date

    try:
        get_result = es.get(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                            id=_id_last)['_source']
        total_count_history = get_result['total_post_num']
    except:
        total_count_history = 0

    total_count_totay = total_count_history + today_count

    #_id_today = xnr_user_no + '_' + current_date

    item_dict = dict()
    #item_dict['date_time'] = current_date
    #item_dict['xnr_user_no'] = xnr_user_no
    item_dict['speak_today'] = {}
    item_dict['speak_total'] = {}
    item_dict['speak_today'][current_time] = today_count
    item_dict['speak_total'][current_time] = total_count_totay

    #if i == 0:
    #speak_num_xnr = get_results['daily_post_num']
    #group_message_index_name = group_message_index_name_pre + current_date
    query_body_total_day = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_qq_number':qq_number}
                }
            }
        },
        'aggs':{
            'all_speakers':{
                'terms':{'field':'speaker_qq_number',"order" : { "_count" : "desc" }}
            }
        }
    }

    try:

        results_total_day = es_xnr.search(index=group_message_index_name,doc_type=group_message_index_type,\
                    body=query_body_total_day)['aggregations']['all_speakers']['buckets']

        speaker_max = results_total_day[0]['doc_count']
    except:
        speaker_max = today_count

    safe_active = (float(math.log(today_count+1))/(math.log(speaker_max+1)+1))*100

    safe_active = round(safe_active,2)  # 保留两位小数
    
    item_dict['mark'] = safe_active

    return item_dict


# def get_safe_qq(xnr_user_no):

#     speak_dict = {}
#     speak_dict['speak_day'] = {}
#     speak_dict['speak_total'] = {}

#     get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
#     qq_number = get_result['qq_number']
#     # if S_TYPE == 'test':
#     #     current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)
#     # else:
#     #     current_time = int(time.time())
#     current_time = int(time.time())
#     group_message_index_list = get_groupmessage_index_list(QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT,ts2datetime(current_time))

#     for i in range(WEEK):
#         current_time_new = current_time - i*DAY
#         current_date = ts2datetime(current_time_new)

#         start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
#         end_ts = current_time_new - i*DAY 
        
#         group_message_index_name = group_message_index_name_pre + current_date
        
#         # 虚拟人发言数量
#         query_body_xnr = {
#             'query':{
#                 'filtered':{
#                     'filter':{
#                         'term':{'speaker_qq_number':qq_number}
#                     }
#                 }
#             }
#         }
#         try:
#             results_xnr = es_xnr.count(index=group_message_index_name,doc_type=group_message_index_type,\
#                         body=query_body_xnr)

#             if results_xnr['_shards']['successful'] != 0:
#                 speak_num_xnr = results_xnr['count']
#             else:
#                 print 'es index rank error'
#                 speak_num_xnr = 0
#         except:
#             speak_num_xnr = 0

#         # 截止目前所有发言总数
#         query_body_total = {
#             'query':{
#                 'bool':{
#                     'must':[
#                         {'term':{'speaker_qq_number':qq_number}},
#                         {'range':{'timestamp':{'lte':end_ts}}}
#                     ]
#                 }
#             }
#         }
#         print 'group_message_index_list:::273',group_message_index_list
#         #try:
#         results_total = es_xnr.count(index=group_message_index_list,doc_type=group_message_index_type,\
#                     body=query_body_total)

#         if results_total['_shards']['successful'] != 0:
#            speak_num_total = results_total['count']
#         else:
#             print 'es index rank error'
#             speak_num_total = 0
#         # except:
#         #     speak_num_total = 0
#         print 'speak_num_total:::285',speak_num_total
#         speak_dict['speak_day'][current_time_new] = speak_num_xnr
#         speak_dict['speak_total'][current_time_new] = speak_num_total

#         if i == (WEEK-1):
#             query_body_total_day = {
#                 'query':{
#                     'filtered':{
#                         'filter':{
#                             'term':{'xnr_qq_number':qq_number}
#                         }
#                     }
#                 },
#                 'aggs':{
#                     'all_speakers':{
#                         'terms':{'field':'speaker_qq_number',"order" : { "_count" : "desc" }}
#                     }
#                 }
#             }

#             try:
#                 results_total_day = es_xnr.search(index=group_message_index_name,doc_type=group_message_index_type,\
#                             body=query_body_total_day)['aggregations']['all_speakers']['buckets']

#                 speaker_max = results_total_day[0]['doc_count']
#             except:
#                 speaker_max = 0

#             safe_active = (float(math.log(speak_num_xnr+1))/(math.log(speaker_max+1)+1))*100

#             safe_active = round(safe_active,2)  # 保留两位小数
            
#             speak_dict['mark'] = safe_active

#     return speak_dict

# def get_safe_qq(xnr_user_no):

#     get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
#     qq_number = get_result['qq_number']
#     nickname = get_result['nickname']
#     group_list = get_result['qq_groups'].encode('utf-8').split('，')

#     current_time = int(time.time())

#     current_date = ts2datetime(current_time)

#     group_message_index_name = group_message_index_name_pre + current_date

#     topic_distribute_dict = {}
#     topic_distribute_dict['radar'] = {}

#     # 关注者topic分布
#     query_body_group = {
#         'query':{
#             'filtered':{
#                 'filter':{
#                     'terms':{'qq_group_number':group_list}
#                 }
#             }
#         }
#     }

#     results = es_xnr.search(index=group_message_index_name,doc_type=group_message_index_type,\
#         body=query_body_group)['hits']['hits']

#     topic_list_followers = []

#     for result in results:
#         if result['found'] == True:
#             result = result['_source']
#             topic_string_first = result['topic_string'].split('&')
#             topic_list_followers.extend(topic_string_first)

#     topic_list_followers_count = Counter(topic_list_followers)

#     #topic_distribute_dict['topic_follower'] = topic_list_followers_count
#     # 虚拟人topic分布
#     query_body_xnr = {
#         'query':{
#             'filtered':{
#                 'filter':{
#                     'term':{'speaker_qq_number':qq_number}
#                 }
#             }
#         }
#     }
    
#     results = es_xnr.search(index=group_message_index_name,doc_type=group_message_index_type,\
#         body=query_body_xnr)['hits']['hits']
#     try:
#         xnr_results = es_user_portrait.get(index=portrait_index_name,doc_type=portrait_index_type,\
#             id=uid)['_source']
#         topic_string = xnr_results['topic_string'].split('&')
#         topic_xnr_count = Counter(topic_string)
#         #topic_distribute_dict['topic_xnr'] = topic_xnr_count

#     except:
#         topic_xnr_count = {}
#         #topic_distribute_dict['topic_xnr'] = topic_xnr_count

#     # 整理雷达图数据
#     # if topic_xnr_count:
#     #     for topic, value in topic_xnr_count.iteritems():
#     #         try:
#     #             topic_value = float(value)/(topic_list_followers_count[topic])
#     #         except:
#     #             continue
#     #         topic_distribute_dict['radar'][topic] = topic_value
#     if topic_xnr_count:
#         for topic, value in topic_list_followers_count.iteritems():
#             try:
#                 topic_value = float(topic_xnr_count[topic])/value
#             except:
#                 continue
#             topic_distribute_dict['radar'][topic] = topic_value
            
#     # 整理仪表盘数据
#     mark = 0
    
#     if topic_xnr_count:
#         n_topic = len(topic_list_followers_count.keys())
#         for topic,value in topic_xnr_count.iteritems():
#             try:
#                 mark += float(value)/(topic_list_followers_count[topic]*n_topic)
#                 print topic 
#                 print mark
#             except:
#                 continue
#     topic_distribute_dict['mark'] = mark

#     return topic_distribute_dict
