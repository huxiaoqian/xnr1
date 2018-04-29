# -*-coding:utf-8-*-
import math
import time
import json
import os
import sys
from elasticsearch.helpers import scan
sys.path.append('../../')
from xnr.wx_xnr.global_config import WX_GROUP_MESSAGE_START_DATE_ASSESSMENT
from xnr.wx_xnr.time_utils import ts2datetime, datetime2ts, get_wx_groupmessage_index_list
from xnr.wx_xnr.parameter import DAY, MAX_VALUE, MAX_SEARCH_SIZE
from xnr.wx_xnr.wx.control_bot import load_wxxnr_redis_data
from xnr.wx_xnr.global_utils import wx_xnr_history_count_index_name, wx_xnr_history_count_index_type, es_xnr,\
                wx_group_message_index_name_pre, wx_group_message_index_type, wx_xnr_index_name,\
                wx_xnr_index_type, wx_xnr_history_be_at_index_type, wx_xnr_history_sensitive_index_type
from xnr.wx_xnr.wx_xnr_manage_mappings import wx_xnr_history_count_mappings

def wx_history_count(xnr_user_no, xnr_puid, current_time):
    current_date = ts2datetime(current_time)
    last_date = ts2datetime(current_time-DAY)
    #获取今日发言总数
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'speaker_id': xnr_puid}},
                    {'term':{'xnr_id':xnr_puid}}
                ]
            }
        }
    }
    today_index_name = wx_group_message_index_name_pre + current_date
    today_count_result = es_xnr.count(index=today_index_name,doc_type=wx_group_message_index_type,body=query_body)
    if today_count_result['_shards']['successful'] != 0:
        today_count = today_count_result['count']
    else:
        print 'es index rank error'
        today_count = 0
    #获取历史发言总数
    total_query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_user_no': xnr_user_no}},
                    {'term':{'puid':xnr_puid}},
                    {'term':{'date_time':last_date}}
                ]
            }
        }
    }
    total_index_name = wx_xnr_history_count_index_name
    try:
        total_count_result = es_xnr.search(index=total_index_name,doc_type=wx_xnr_history_count_index_type,body=total_query_body)
        if total_count_result['_shards']['successful'] != 0:
            total_count = total_count_result['hits']['hits'][0]['_source']['total_post_num']
    except Exception,e:
        print e
        total_count = 0
    #包括今天在内的发言总数
    total_count_totay = total_count + today_count
    #发言次数最大值
    query_body_total_day = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_id':xnr_puid}
                }
            }
        },
        'aggs':{
            'all_speakers':{
                'terms':{'field':'speaker_id',"order" : { "_count" : "desc" }}
            }
        }
    }
    try:
        results_total_day = es_xnr.search(index=wx_group_message_index_name,doc_type=wx_group_message_index_type,\
                    body=query_body_total_day)['aggregations']['all_speakers']['buckets']
        speaker_max = results_total_day[0]['doc_count']
    except:
        speaker_max = today_count
    #整合
    item_dict = dict()
    item_dict['total_post_num'] = total_count_totay
    item_dict['daily_post_num'] = today_count
    safe_active = (float(math.log(today_count+1))/(math.log(speaker_max+1)+1))*100
    safe_active = round(safe_active,2)  # 保留两位小数
    item_dict['mark'] = safe_active
    return item_dict

# 影响力 指标 统计
def get_influence_at_num(puid):
    current_timestamp = int(time.time()-DAY)
    current_date = ts2datetime(current_timestamp)
    current_time = datetime2ts(current_date)
    
    query_at_num = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_id':puid}},
                    {'term':{'at_flag':1}}
                ]
            }
        }
    }
    #虚拟人今天被@数量
    wx_group_message_index_name = wx_group_message_index_name_pre + current_date
    try:
        results_xnr = es_xnr.count(index=wx_group_message_index_name,doc_type=wx_group_message_index_type,body=query_at_num)
        if results_xnr['_shards']['successful'] != 0:
           at_num_xnr = results_xnr['count']
        else:
            print 'es index rank error'
            at_num_xnr = 0
    except:
        at_num_xnr = 0
    # 截止目前所有被@总数
    wx_group_message_index_list = get_wx_groupmessage_index_list(WX_GROUP_MESSAGE_START_DATE_ASSESSMENT,ts2datetime(current_time))
    at_num_total = 0
    for index_name in wx_group_message_index_list:
        r = es_xnr.count(index=wx_group_message_index_name,doc_type=wx_group_message_index_type,body=query_at_num)
        if r['_shards']['successful'] != 0:
            at_num_total += r['count']
    #查询所有人被@的次数
    query_body_total_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_id':puid}},
                    {'wildcard':{'text':'*'+'@'+'*'}}
                ]
            }
        }
    }
    try:
        results_total_day = es_xnr.count(index=wx_group_message_index_name,doc_type=wx_group_message_index_type,body=query_body_total_day)
        if results_total_day['_shards']['successful'] != 0:
           at_num_total_day = results_total_day['count']
        else:
            print 'es index rank error'
            at_num_total_day = 0
    except:
        at_num_total_day = 0
    #统计
    item_dict = {}
    item_dict['daily_be_at_num'] = at_num_xnr
    item_dict['total_be_at_num'] = at_num_total
    influence = (float(math.log(at_num_xnr+1))/(math.log(at_num_total_day+1)+1))*100
    influence = round(influence,2)  # 保留两位小数
    mark = influence
    item_dict['mark'] = mark
    return item_dict

# 渗透力 指标 统计
def get_penetration_num(xnr_user_no):
    current_timestamp = int(time.time()-DAY)
    current_date = ts2datetime(current_timestamp)
    current_time = datetime2ts(current_date)

    xnr_data = load_wxxnr_redis_data(wxbot_id=xnr_user_no, items=['puid','groups_list'])
    puid = xnr_data['puid']
    group_list = xnr_data['groups_list']
    
    #查询1
    wx_group_message_index_name = wx_group_message_index_name_pre + current_date
    query_body_info = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'group_id':group_list}
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
        es_sensitive_result = es_xnr.search(index=wx_group_message_index_name,doc_type=wx_group_message_index_type,body=query_body_info)['aggregations']
        sensitive_value = es_sensitive_result['avg_sensitive']['value']
        if sensitive_value == None:
            sensitive_value = 0
    except:
        sensitive_value = 0
    #查询2
    query_body_max = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'group_id':group_list}
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
    #统计
    follow_group_sensitive = {'sensitive_info': sensitive_value}
    penetration = (math.log(sensitive_value+1)/(math.log(max_sensitive+1)+1))*100
    penetration = round(penetration,2)
    follow_group_sensitive['mark'] = penetration
    return follow_group_sensitive

def cron_compute_mark_wx():
    current_time = int(time.time()-DAY)
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    #加载数据库中虚拟人信息
    xnr_query_body={'query':{'match_all':{}},'size':MAX_VALUE}
    xnr_results = es_xnr.search(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, body=xnr_query_body)['hits']['hits']
    flag = False
    for result in xnr_results:
        xnr_user_no = result['_source']['xnr_user_no']
        puid = result['_source']['puid']
        #计算
        influence_dict = get_influence_at_num(puid)
        penetration_dict = get_penetration_num(xnr_user_no)
        safe_dict = wx_history_count(xnr_user_no, puid, current_time_new)
        #整理
        _id = xnr_user_no + '_' + current_date
        xnr_user_detail = {
            'influence': influence_dict['mark'],
            'penetration': penetration_dict['mark'],
            'safe': safe_dict['mark'],
            'daily_be_at_num': influence_dict['daily_be_at_num'],
            'total_be_at_num': influence_dict['total_be_at_num'],
            'daily_sensitive_num': penetration_dict['sensitive_info'],
            'total_post_num': safe_dict['total_post_num'],
            'daily_post_num': safe_dict['daily_post_num'],
            'date_time': current_date,
            'timestamp': current_time_new,
            'xnr_user_no': xnr_user_no,
            'puid': puid
        }
        #并存储
        wx_xnr_history_count_mappings() #先确保数据库存在
        try:
            es_xnr.index(index=wx_xnr_history_count_index_name,doc_type=wx_xnr_history_count_index_type,\
                id=_id,body=xnr_user_detail)
            flag = True
        except Exception,e:
            print e
            return False
    return flag

if __name__ == '__main__':
    print cron_compute_mark_wx()








