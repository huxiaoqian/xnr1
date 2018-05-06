# -*-coding:utf-8-*-
import math
import time
import json
from xnr.global_config import S_TYPE,QQ_S_DATE_NEW,QQ_GROUP_MESSAGE_START_DATE,QQ_S_DATE_ASSESSMENT,\
                    QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT
from xnr.global_utils import es_xnr,group_message_index_name_pre,group_message_index_type,\
                    qq_xnr_index_name,qq_xnr_index_type,qq_xnr_history_count_index_name_pre,\
                    qq_xnr_history_count_index_type,r, r_qq_speak_num_pre
from xnr.time_utils import datetime2ts,ts2datetime,get_groupmessage_index_list, get_timeset_indexset_list
from xnr.parameter import WEEK,DAY,MAX_SEARCH_SIZE


def get_influence_at_num(xnr_user_no,start_ts,end_ts):

    at_dict = {}
    at_dict['at_day'] = {}
    at_dict['at_total'] = {}


    start_date = ts2datetime(start_ts)
    end_date = ts2datetime(end_ts)

    index_name_list = get_timeset_indexset_list(qq_xnr_history_count_index_name_pre,start_date,end_date)
    
    for index_name in index_name_list:

        try:
            get_result = es_xnr.get(index=index_name,doc_type=qq_xnr_history_count_index_type,\
                    id=xnr_user_no)['_source']

            timestamp = get_result['timestamp']
            at_dict['at_day'][timestamp] = get_result['daily_be_at_num']
            at_dict['at_total'][timestamp] = get_result['total_be_at_num']
            at_dict['mark'] = get_result['influence']


        except:

            date = index_name[-10:]
            timestamp = datetime2ts(date)

            at_dict['at_day'][timestamp] = 0
            at_dict['at_total'][timestamp] = 0
            at_dict['mark'] = 0.0

    return at_dict

def get_influence_at_num_today(xnr_user_no):
    at_dict = {}
    at_dict['at_day'] = {}
    at_dict['at_total'] = {}

    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']
    nickname = get_result['nickname']
        
    if S_TYPE == 'test':
        current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)
    else:
        current_time = int(time.time())

    current_date = ts2datetime(current_time)
    group_message_index_name = group_message_index_name_pre + current_date
            
    #虚拟人今天被@数量
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


    # 得到历史总数
    current_time_last = current_time - DAY
    current_date_last = ts2datetime(current_time_last)
    qq_xnr_history_count_index_name = qq_xnr_history_count_index_name_pre + current_date_last

    try:
        result_last = es_xnr.get(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_be_at_index_type,id=xnr_user_no)['_source']
        total_be_at_num_last = result_last['total_be_at_num']
    except:
        total_be_at_num_last = 0

    at_dict['at_day'][current_time] = at_num_xnr
    at_dict['at_total'][current_time]= at_num_xnr + total_be_at_num_last


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

    start_date = ts2datetime(start_ts)
    end_date = ts2datetime(end_ts)

    index_name_list = get_timeset_indexset_list(qq_xnr_history_count_index_name_pre,start_date,end_date)

    for index_name in index_name_list:

        try:
            get_result = es_xnr.get(index=index_name,doc_type=qq_xnr_history_count_index_type,\
                        id=xnr_user_no)['_source']
            
            timestamp = get_result['timestamp']

            follow_group_sensitive['sensitive_info'][timestamp] = get_result['daily_sensitive_num']
            follow_group_sensitive['mark'] = get_result['penetration']

        except:

            date = index_name[-10:]
            timestamp = datetime2ts(date)
            follow_group_sensitive['sensitive_info'][timestamp] = 0.0
            follow_group_sensitive['mark'] = 0.0

    return follow_group_sensitive

def get_penetration_qq_today(xnr_user_no):

    follow_group_sensitive = {}
    follow_group_sensitive['sensitive_info'] = {}

    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']
    nickname = get_result['nickname']
    
    #group_list = get_result['qq_groups']
    group_list = []
    group_info = json.loads(get_result['group_info'])

    for key, value_dict in group_info.iteritems():
        group_name = value_dict['group_name']
        group_list.extend(group_name)

    if S_TYPE == 'test':
        current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)
    else:
        current_time = int(time.time())
    
    current_date = ts2datetime(current_time)

    group_message_index_name = group_message_index_name_pre + current_date


    query_body_info = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'qq_group_nickname':group_list}
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
        follow_group_sensitive['sensitive_info'][current_time] = round(sensitive_value,2)
    except:
        follow_group_sensitive['sensitive_info'][current_time] = 0

    query_body_max = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'qq_group_nickname':group_list}
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

    start_date = ts2datetime(start_ts)
    end_date = ts2datetime(end_ts)

    index_name_list = get_timeset_indexset_list(qq_xnr_history_count_index_name_pre,start_date,end_date)

    for index_name in index_name_list:
        try:
            get_result = es_xnr.get(index=index_name,doc_type=qq_xnr_history_count_index_type,\
                        id=xnr_user_no)['_source']

            timestamp = get_result['timestamp']

            speak_dict['speak_day'][timestamp] = get_result['daily_post_num']
            speak_dict['speak_total'][timestamp] = get_result['total_post_num']
            speak_dict['mark'] = get_result['safe']

        except:

            date = index_name[-10:]
            timestamp = datetime2ts(date)
            speak_dict['speak_day'][timestamp] = 0
            speak_dict['speak_total'][timestamp] = 0
            speak_dict['mark'] = 0.0

    return speak_dict

def get_safe_qq_today(xnr_user_no):

    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']

    if S_TYPE == 'test':
        current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)
    else:
        current_time = int(time.time())
    
    current_date = ts2datetime(current_time)
    
    group_message_index_name = group_message_index_name_pre + current_date

    '''
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
    '''

    current_date = ts2datetime(int(time.time()))
    r_qq_speak_num = r_qq_speak_num_pre + current_date

    try:
        today_count = int(r.hget(r_qq_speak_num, qq_number))
    except:
        today_count = 0

    last_date = ts2datetime(current_time-DAY)
    qq_xnr_history_count_index_name = qq_xnr_history_count_index_name_pre + last_date

    try:
        get_result = es.get(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                            id=_id_last)['_source']
        total_count_history = get_result['total_post_num']
    except:
        total_count_history = 0

    total_count_totay = total_count_history + today_count

    item_dict = dict()
    item_dict['speak_today'] = {}
    item_dict['speak_total'] = {}
    item_dict['speak_today'][current_time] = today_count
    item_dict['speak_total'][current_time] = total_count_totay


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
