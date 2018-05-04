# -*-coding:utf-8-*-
import math
import time
import json
import os
import sys
from elasticsearch.helpers import scan
sys.path.append('../')
from global_config import S_TYPE,QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT, QQ_S_DATE_ASSESSMENT
from global_utils import qq_xnr_history_count_index_name_pre,qq_xnr_history_count_index_type,es_xnr as es,\
                group_message_index_name_pre,group_message_index_type,qq_xnr_index_name,\
                qq_xnr_index_type,qq_xnr_history_be_at_index_type,qq_xnr_history_sensitive_index_type,\
                weibo_xnr_index_name,weibo_xnr_index_type,es_xnr, r_qq_speak_num_pre, r
from qq_xnr_manage_mappings import qq_xnr_history_count_mappings
from time_utils import ts2datetime,datetime2ts,get_groupmessage_index_list
from parameter import DAY,MAX_VALUE,MAX_SEARCH_SIZE

# 安全性
def qq_history_count(xnr_user_no,qq_number,current_time):

    if S_TYPE == 'test':
        current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)

    current_date = ts2datetime(current_time)
    last_date = ts2datetime(current_time-DAY)

    group_message_index_name = group_message_index_name_pre + current_date
    qq_xnr_history_count_index_name = qq_xnr_history_count_index_name_pre + last_date

    '''
    # 得到当天发帖数量
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

    count_result = es.count(index=group_message_index_name,doc_type=group_message_index_type,body=query_body)

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

    # 得到历史发言总数
    try:
        get_result = es.get(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                            id=xnr_user_no)['_source']

        total_count_history = get_result['total_post_num']

    except:
        total_count_history = 0

    total_count_totay = total_count_history + today_count
    

    item_dict = dict()
    item_dict['total_post_num'] = total_count_totay
    item_dict['daily_post_num'] = today_count

    # xnr所在群当天发言最多的人
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
                'terms':{'field':'speaker_nickname',"order" : { "_count" : "desc" }}
            }
        }
    }

    try:

        results_total_day = es_xnr.search(index=group_message_index_name,doc_type=group_message_index_type,\
                    body=query_body_total_day)['aggregations']['all_speakers']['buckets']

        speaker_max = results_total_day[0]['doc_count']
    except:
        speaker_max = today_count

    safe = (float(math.log(today_count+1))/(math.log(speaker_max+1)+1))*100

    safe = round(safe,2)  # 保留两位小数
    
    item_dict['mark'] = safe

    return item_dict


# 影响力 指标 统计
def get_influence_at_num(xnr_user_no, qq_number, current_time):
    
    item_dict = {}
    
    if S_TYPE == 'test':
        current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)

    current_date = ts2datetime(current_time)

    group_message_index_name = group_message_index_name_pre + current_date
        
    #虚拟人当天被@数量
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

    item_dict['daily_be_at_num'] = at_num_xnr
    item_dict['total_be_at_num'] = at_num_xnr + total_be_at_num_last

    # 被@总数
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
    
    mark = influence
    item_dict['mark'] = mark

    # es_xnr.index(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_be_at_index_type,\
    #     body=item_dict)

    return item_dict


# 渗透力 指标 统计
def get_penetration_num(xnr_user_no,qq_number,current_time):
    
    follow_group_sensitive = {}
    follow_group_sensitive['sensitive_info'] = {}
    
    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    
    #group_list = get_result['qq_groups']
    group_list = []
    group_info = json.loads(get_result['group_info'])

    for key, value_dict in group_info.iteritems():
        group_name = value_dict['group_name']
        group_list.extend(group_name)

        
    if S_TYPE == 'test':
        current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)

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
        follow_group_sensitive['sensitive_info'] = round(sensitive_value,2)
    except:
        follow_group_sensitive['sensitive_info'] = 0

    #if i == (WEEK-1):
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


def cron_compute_mark_qq(current_time):

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    xnr_results = es.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,\
                body={'query':{'match_all':{}},'_source':['xnr_user_no'],'size':MAX_SEARCH_SIZE})['hits']['hits']
    
    if S_TYPE == 'test':
        xnr_results = [{'_source':{'xnr_user_no':'QXNR0007','qq_number':'1039598173'}}]

    for result in xnr_results:
        xnr_user_no = result['_source']['xnr_user_no']
        qq_number = result['_source']['qq_number']
        #xnr_user_no = 'WXNR0004'
        influence_dict = get_influence_at_num(xnr_user_no, qq_number, current_time)
        penetration_dict = get_penetration_num(xnr_user_no, qq_number, current_time)
        safe_dict = qq_history_count(xnr_user_no,qq_number,current_time)

        #_id = xnr_user_no + '_' + current_date
        _id = xnr_user_no

        xnr_user_detail = {}
        xnr_user_detail['influence'] = influence_dict['mark']
        xnr_user_detail['penetration'] = penetration_dict['mark']
        xnr_user_detail['safe'] = safe_dict['mark']

        xnr_user_detail['daily_be_at_num'] = influence_dict['daily_be_at_num']
        xnr_user_detail['total_be_at_num'] = influence_dict['total_be_at_num']
        
        xnr_user_detail['daily_sensitive_num'] = penetration_dict['sensitive_info']
        #xnr_user_detail['daily_sensitive_num'] = penetration_dict['daily_sensitive_num']

        xnr_user_detail['total_post_num'] = safe_dict['total_post_num']
        xnr_user_detail['daily_post_num'] = safe_dict['daily_post_num']
        
        xnr_user_detail['date_time'] = current_date
        xnr_user_detail['timestamp'] = current_time_new
        xnr_user_detail['xnr_user_no'] = xnr_user_no
        xnr_user_detail['qq_number'] = qq_number

        qq_xnr_history_count_index_name = qq_xnr_history_count_index_name_pre + current_date

        try:
            #print 'xnr_user_detail...',xnr_user_detail
            print 'qq_xnr_history_count_index_name...',qq_xnr_history_count_index_name
            qq_xnr_history_count_mappings(qq_xnr_history_count_index_name)
            es.index(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                id=_id,body=xnr_user_detail)
        
            mark = True

        except:
            mark = False

        return mark

# def bulk_add():
#     s_re = scan(es, query={'query':{'match_all':{}}, 'size':20},index=qq_xnr_history_count_index_name, doc_type=qq_xnr_history_count_index_type)
#     bulk_action=[]
#     count=0
#     while  True:

#         scan_re=s_re.next()
#         _id=scan_re['_id']
#         update_dict = {'total_sensitive_num':0,'daily_sensitive_num':0,'daily_be_at_num':0,'total_be_at_num':0,\
#                         'influence':0,'penetration':0,'safe':0}
#         source={'doc':update_dict}
#         action={'update':{'_id':_id}}
#         bulk_action.extend([action,source])
#         count += 1
#         if count % 10 == 0:
#             print 'count:::',count
#             es.bulk(bulk_action,index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,timeout=100)
#             bulk_action = []
#         else:
#             pass

#     if bulk_action:
#        es.bulk(bulk_action,index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,timeout=100)

if __name__ == '__main__':



    #main_qq_count()
    # 每天凌晨统计前一天
    current_time = int(time.time()-DAY)
    cron_compute_mark_qq(current_time)
    #bulk_add()







