# -*- coding: utf-8 -*-
import math
import time
import datetime
from xnr.wx_xnr.global_utils import es_xnr,wx_xnr_index_name,wx_xnr_index_type,\
                             wx_group_message_index_name_pre, wx_group_message_index_type,\
                             wx_xnr_history_count_index_name, wx_xnr_history_count_index_type,\
                             wx_xnr_history_be_at_index_type, wx_xnr_history_sensitive_index_type
from xnr.wx_xnr.global_config import WX_S_DATE_NEW,WX_GROUP_MESSAGE_START_DATE,WX_S_DATE_ASSESSMENT,\
                    WX_GROUP_MESSAGE_START_DATE_ASSESSMENT                             
from xnr.wx_xnr.parameter import MAX_VALUE, WEEK, DAY, MAX_SEARCH_SIZE
from xnr.wx_xnr.time_utils import get_wx_groupmessage_index_list, ts2datetime, datetime2ts
from xnr.wx_xnr.wx.control_bot import load_wxxnr_redis_data

def dump_date(period, startdate, enddate):
    if period == '':
        period = -1 #flag
        start_ts = datetime2ts(startdate)
        end_ts = datetime2ts(enddate)
    else:
        period = int(period)
        if period == 0:
            end_ts = int(time.time())
            start_ts = datetime2ts(ts2datetime(end_ts))
        else:
            end_ts = datetime2ts(ts2datetime(int(time.time()))) - DAY
            start_ts = end_ts - (period - 1) * DAY
    return start_ts, end_ts, period

def load_timestamp_list(start_ts, end_ts):
    timestamp_list = []
    for i in range(1 + (end_ts-start_ts)/DAY):
        timestamp_list.append(start_ts + i * DAY)
    return timestamp_list

def utils_get_influence(wxbot_id, period, startdate, enddate):
    start_ts, end_ts, period = dump_date(period, startdate, enddate)
    current_timestamp = int(time.time())
    current_date = ts2datetime(current_timestamp)
    if period == 0:    #获取今天的数据
        xnr_puid = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid'])['puid']
        current_time = datetime2ts(current_date)
        query_at_num = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'xnr_id':xnr_puid}},
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
                        {'term':{'xnr_id':xnr_puid}},
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
        at_dict = {}
        at_dict['at_day'] = {}
        at_dict['at_total'] = {}
        at_dict['at_day'][current_time] = at_num_xnr
        at_dict['at_total'][current_time] = at_num_total
        influence = (float(math.log(at_num_xnr+1))/(math.log(at_num_total_day+1)+1))*100
        influence = round(influence,2)  # 保留两位小数
        at_dict['mark'] = influence
        return at_dict
    else:
        at_dict = {}
        at_dict['at_day'] = {}
        at_dict['at_total'] = {}
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'term':{'xnr_user_no':wxbot_id}},
                                {'range':{'timestamp':{'gte':start_ts,'lte':end_ts}}}
                            ]
                        }
                    }
                }
            },
            'size':MAX_SEARCH_SIZE,
            'sort':{'timestamp':{'order':'asc'}}
        }
        search_results = es_xnr.search(index=wx_xnr_history_count_index_name,doc_type=wx_xnr_history_count_index_type,\
                        body=query_body)['hits']['hits']
        #初始化
        ts_list = load_timestamp_list(start_ts, end_ts)
        for ts in ts_list:
            at_dict['at_day'][ts] = 0
            at_dict['at_total'][ts] = 0
        at_dict['mark'] = 0
        #填充数据
        for result in search_results:
            result = result['_source']
            timestamp = result['timestamp']
            at_dict['at_day'][timestamp] = result['daily_be_at_num']
            at_dict['at_total'][timestamp] = result['total_be_at_num']
            at_dict['mark'] = result['influence']
        return at_dict

def utils_get_penetration(wxbot_id, period, startdate, enddate):
    start_ts, end_ts, period = dump_date(period, startdate, enddate)
    current_timestamp = int(time.time())
    current_date = ts2datetime(current_timestamp)
    if period == 0 :    #获取今天的数据
        current_time = datetime2ts(current_date)

        xnr_data = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid','groups_list'])
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
        follow_group_sensitive = {'sensitive_info': {current_time: sensitive_value}}
        penetration = (math.log(sensitive_value+1)/(math.log(max_sensitive+1)+1))*100
        penetration = round(penetration,2)
        follow_group_sensitive['mark'] = penetration
        return follow_group_sensitive
    else:  
        follow_group_sensitive = {}
        follow_group_sensitive['sensitive_info'] = {}
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'term':{'xnr_user_no':wxbot_id}},
                                {'range':{'timestamp':{'gte':start_ts,'lte':end_ts}}}
                            ]
                        }
                    }
                }
            },
            'size':MAX_SEARCH_SIZE,
            'sort':{'timestamp':{'order':'asc'}}
        }
        search_results = es_xnr.search(index=wx_xnr_history_count_index_name,doc_type=wx_xnr_history_count_index_type,\
                        body=query_body)['hits']['hits']
        #初始化
        ts_list = load_timestamp_list(start_ts, end_ts)
        for ts in ts_list:
            follow_group_sensitive['sensitive_info'][ts]  = 0
        follow_group_sensitive['mark'] = 0 
        #填充数据
        for result in search_results:
            result = result['_source']
            timestamp = result['timestamp']
            follow_group_sensitive['sensitive_info'][timestamp] = result['daily_sensitive_num']
            follow_group_sensitive['mark'] = result['penetration']
        return follow_group_sensitive

def utils_get_safe(wxbot_id, period, startdate, enddate):
    start_ts, end_ts, period = dump_date(period, startdate, enddate)
    current_timestamp = int(time.time())
    current_date = ts2datetime(current_timestamp)
    if period == 0:     #获取今天的数据
        current_time = datetime2ts(current_date)
        last_date = ts2datetime(current_time-DAY)

        speak_dict = {}
        speak_dict['speak_day'] = {}
        speak_dict['speak_total'] = {}
        xnr_puid = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid'])['puid']

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
                        {'term':{'xnr_user_no': wxbot_id}},
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
        speak_dict = dict()
        speak_dict['speak_today'] = {}
        speak_dict['speak_total'] = {}
        speak_dict['speak_today'][current_time] = today_count
        speak_dict['speak_total'][current_time] = total_count_totay
        safe_active = (float(math.log(today_count+1))/(math.log(speaker_max+1)+1))*100
        safe_active = round(safe_active,2)  # 保留两位小数
        speak_dict['mark'] = safe_active
        return speak_dict
    else:
        speak_dict = {}
        speak_dict['speak_day'] = {}
        speak_dict['speak_total'] = {}
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'term':{'xnr_user_no':wxbot_id}},
                                {'range':{'timestamp':{'gte':start_ts,'lte':end_ts}}}
                            ]
                        }
                    }
                }
            },
            'size':MAX_SEARCH_SIZE,
            'sort':{'timestamp':{'order':'asc'}}
        }
        search_results = es_xnr.search(index=wx_xnr_history_count_index_name,doc_type=wx_xnr_history_count_index_type,\
                        body=query_body)['hits']['hits']
        #初始化
        ts_list = load_timestamp_list(start_ts, end_ts)
        for ts in ts_list:
            speak_dict['speak_day'][ts]  = 0
            speak_dict['speak_total'][ts] = 0
        speak_dict['mark'] = 0 
        #填充数据
        for result in search_results:  
            result = result['_source']
            timestamp = result['timestamp']
            speak_dict['speak_day'][timestamp] = result['daily_post_num']
            speak_dict['speak_total'][timestamp] = result['total_post_num']
            speak_dict['mark'] = result['safe']
        return speak_dict
