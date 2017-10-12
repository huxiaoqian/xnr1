# -*-coding:utf-8-*-
import time
import json
import os
import sys
sys.path.append('../')
from global_utils import qq_xnr_history_count_index_name,qq_xnr_history_count_index_type,es_xnr as es,\
                group_message_index_name_pre,group_message_index_type,qq_xnr_index_name,\
                qq_xnr_index_type,qq_xnr_history_be_at_index_type,qq_xnr_history_sensitive_index_type

from time_utils import ts2datetime,datetime2ts
from parameter import DAY,MAX_VALUE

def qq_history_count(xnr_user_no,qq_number,current_time):

    current_date = ts2datetime(current_time)
    #timestamp = datetime2ts(current_date)
    last_date = ts2datetime(current_time-DAY)
    print 'current_date:::',current_date

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

    count_result = es.count(index=group_message_index_name,doc_type=group_message_index_type,body=query_body)

    if count_result['_shards']['successful'] != 0:
        today_count = count_result['count']
    else:
        print 'es index rank error'
        today_count = 0

    _id_last = xnr_user_no +'_'+ last_date
    print '_id_last::',_id_last

    try:
        get_result = es.get(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                            id=_id_last)['_source']
        total_count_history = get_result['total_post_num']
    except:
        total_count_history = 0

    total_count_totay = total_count_history + today_count

    _id_today = xnr_user_no + '_' + current_date

    item_dict = dict()
    #item_dict['date_time'] = current_date
    #item_dict['xnr_user_no'] = xnr_user_no
    item_dict['total_post_num'] = total_count_totay
    item_dict['daily_post_num'] = today_count
    #item_dict['qq_number'] = qq_number
    #item_dict['timestamp'] = current_time

    query_body_total_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_qq_number':qq_number}},
                    {'wildcard':{'text':'*'+'@'+'*'}}
                ]
            }
        },
        'aggs':{
                'uid_list':{
                    'terms':{'field':'uid','size':MAX_VALUE,'order':{'avg_sort':'desc'} },
                    'aggs':{'avg_sort':{'avg':{'field':sort_item}}}

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
    
    item_dict['mark'] = influence

    # es.index(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
    #             id=_id_today,body=item_dict)

    return item_dict

# 活跃性  统计 指标
# def main_qq_count():
#     query_body = {
#         'query':{
#             'match_all':{}
#         },
#         'size':MAX_VALUE
#     }
#     results = es.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,body=query_body)['hits']['hits']

#     for item in results:
#         item = item['_source']
#         xnr_user_no = item['xnr_user_no']
#         qq_number = item['qq_number']
#         current_time = time.time() - DAY
        # qq_history_count(xnr_user_no,qq_number,current_time)

# 影响力 指标 统计
def get_influence_at_num(xnr_user_no):
    
    item_dict = {}
    # item_dict['daily_be_at_num'] = {}
    # item_dict['daily_be_at_num'] = {}

    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']
    nickname = get_result['nickname']
        
    # if S_TYPE == 'test':
    #     current_time = datetime2ts(QQ_S_DATE_ASSESSMENT)
    # else:
    #     current_time = int(time.time())
    current_timestamp = int(time.time()-DAY)
    current_date = ts2datetime(current_timestamp)
    current_time = datetime2ts(current_date)

    group_message_index_list = get_groupmessage_index_list(QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT,ts2datetime(current_time))

    # for i in range(WEEK-1,-1,-1):
    #     current_time_new = current_time - i*DAY
    #     current_date = ts2datetime(current_time_new)
        
    #     #start_ts = current_time_new - i*DAY  # DAY=3600*24
    #     end_ts = current_time_new + DAY 

    group_message_index_name = group_message_index_name_pre + current_date
    #group_message_index_list = get_groupmessage_index_list(QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT,current_date)
    
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
                    {'wildcard':{'text':'*'+'@ME'+'*'}},
                    {'range':{'timestamp':{'lte':end_ts}}}
                ]
            }
        }
    }


    results_total = es_xnr.count(index=group_message_index_list,doc_type=group_message_index_type,\
                body=query_body_total)

    if results_total['_shards']['successful'] != 0:
        at_num_total = results_total['count']
    else:
        print 'es index rank error'
        at_num_total = 0

    item_dict['daily_be_at_num'] = at_num_xnr
    item_dict['total_be_at_num'] = at_num_total
    #item_dict['timestamp'] = current_time
    #item_dict['date_time'] = current_date
    #item_dict['xnr_user_no'] = xnr_user_no
    #item_dict['qq_number'] = qq_number

    
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
def get_penetration_num(xnr_user_no):
    
    follow_group_sensitive = {}
    follow_group_sensitive['sensitive_info'] = {}

    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
    qq_number = get_result['qq_number']
    nickname = get_result['nickname']
    
    group_list = get_result['qq_groups']
        
    current_timestamp = int(time.time()-DAY)
    current_date = ts2datetime(current_timestamp)
    current_time = datetime2ts(current_date)

    # #for i in range(WEEK):
    # current_time_new = current_time - i*DAY
    # current_date = ts2datetime(current_time_new)
    
    # start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
    # end_ts = current_time_new - i*DAY 
    
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
        follow_group_sensitive['sensitive_info'] = sensitive_value
    except:
        follow_group_sensitive['sensitive_info'] = 0

    #if i == (WEEK-1):
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


def qq_assessment_save_to_es():

    penetration = get_penetration_num(xnr_user_no)
    influence = get_influence_at_num(xnr_user_no)
    safe = 

    #  一起存三个分值

def cron_compute_mark_qq():

    current_time = int(time.time()-DAY)
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    xnr_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,\
                body={'query':{'match_all':{}},'_source':['xnr_user_no'],'size':MAX_SEARCH_SIZE})['hits']['hits']
    
    if S_TYPE == 'test':
        xnr_results = [{'_source':{'xnr_user_no':'WXNR0004','qq_number':'1965056593'}}]

    for result in xnr_results:
        xnr_user_no = result['_source']['xnr_user_no']
        qq_number = result['_source']['qq_number']
        #xnr_user_no = 'WXNR0004'
        influence = get_influence_at_num(xnr_user_no)
        penetration = get_penetration_num(xnr_user_no)
        safe = qq_history_count(xnr_user_no,qq_number,current_time)

        _id = xnr_user_no + '_' + current_date

        #xnr_user_detail = create_xnr_history_info_count(xnr_user_no,current_date)

        #item = {}
        #xnr_user_detail['xnr_user_no'] = xnr_user_no
        xnr_user_detail['influence'] = influence
        xnr_user_detail['penetration'] = penetration
        xnr_user_detail['safe'] = safe
        #xnr_user_detail['date'] = current_date
        xnr_user_detail['timestamp'] = current_time_new

        # es.index(index=weibo_xnr_assessment_index_name,doc_type=weibo_xnr_assessment_index_type,\
        #     id=_id,body=item)

        try:

            es.index(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
                id=_id,body=xnr_user_detail)
            
            mark = True

        except:
            mark = False

        return mark


if __name__ == '__main__':

    # xnr_user_no = 'QXNR0001'
    # qq_number = '1965056593'
    # current_time = time.time()
    # qq_history_count(xnr_user_no,qq_number,current_time)

    #main_qq_count()
    cron_compute_mark_qq()








