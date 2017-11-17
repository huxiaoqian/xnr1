# -*- coding: utf-8 -*-
import time
import datetime
from xnr.wx_xnr.global_utils import es_xnr,wx_xnr_index_name,wx_xnr_index_type,\
                             wx_group_message_index_name_pre, wx_group_message_index_type,\
                             wx_report_management_index_name, wx_report_management_index_type
from xnr.wx_xnr.parameter import MAX_VALUE, DAY
from xnr.wx_xnr.time_utils import get_wx_groupmessage_index_list, ts2datetime, datetime2ts
from xnr.wx_xnr.wx.control_bot import load_wxxnr_redis_data
from xnr.wx_xnr.wx_xnr_report_management_mappings import wx_report_management_mappings

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

#查看虚拟人监听到的所有群组的敏感群消息，可指定起始、终止时间。{'msg_type':'Text'}
def utils_search(wxbot_id, period, startdate='', enddate=''):
    start_ts, end_ts, period = dump_date(period, startdate, enddate)
    index_names = get_wx_groupmessage_index_list(ts2datetime(start_ts), ts2datetime(end_ts))
    index_names.reverse()
    xnr_puid = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid'])['puid']
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_id": xnr_puid}},
                            {"term":{"sensitive_flag": 1}},
                            {'term':{'msg_type':'Text'.lower()}}
                        ]
                    }
                }
            }
        },
        "size": MAX_VALUE,
        "sort":{"sensitive_value":{"order":"desc"}}
    }
    results = []
    for index_name in index_names:
        try:
            search_result = es_xnr.search(index=index_name, doc_type=wx_group_message_index_type,body=query_body)
            if search_result:
                results.extend(search_result['hits']['hits'])
        except Exception,e:
            pass
    return results

def utils_show_sensitive_users(wxbot_id, period, startdate='', enddate=''):
    start_ts, end_ts, period = dump_date(period, startdate, enddate)
    index_names = get_wx_groupmessage_index_list(ts2datetime(start_ts), ts2datetime(end_ts))
    index_names.reverse()
    xnr_puid = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid'])['puid']
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_id": xnr_puid}},
                            {"term":{"sensitive_flag": 1}},
                            {'term':{'msg_type':'Text'.lower()}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "sen_users":{
                "terms":{"field": "speaker_id"}
            }
        },
        "sort":{"timestamp":{"order":"desc"}}
    }
    sensitive_users = {}
    for index_name in index_names:
        try:
            search_result = es_xnr.search(index=index_name, doc_type=wx_group_message_index_type,body=query_body)
            if search_result:
                res = search_result['aggregations']['sen_users']['buckets']
                docs = search_result['hits']['hits']
                for r in res:
                    groups_list = []
                    speaker_id = r['key']
                    count = r['doc_count']
                    for doc in docs:
                        if doc['_source']['speaker_id'] == speaker_id:
                            groups_list.append(doc['_source']['group_name'])
                    if speaker_id in sensitive_users:
                        #update: groups&count。因为是倒序查询，所以last_speak_ts在最初创建的时候就是最终的值，不需要更新。
                        sensitive_users[speaker_id]['count'] += count
                        sensitive_users[speaker_id]['groups_list'].extend(groups_list)
                    else:
                        #匹配第一条即可
                        for doc in docs:
                            if doc['_source']['speaker_id'] == speaker_id:
                                nickname = doc['_source']['speaker_name']
                                last_speak_ts = doc['_source']['timestamp']
                                break
                        sensitive_users[speaker_id] = {
                            'nickname': nickname,
                            'count': count,
                            'last_speak_ts': last_speak_ts,
                            'groups_list': groups_list
                        }
        except Exception,e:
            pass
    for speaker_id,user_data in sensitive_users.items():
        temp_groups_list = user_data['groups_list']
        user_data['groups_list'] = ','.join(list(set(temp_groups_list)))
    #转换成数组嵌套字典类型的数据，方便前台使用
    res = []
    for speaker_id,user_data in sensitive_users.items():
        user_data['speaker_puid'] = speaker_id
        res.append(user_data)
    return res

def utils_report_warning_content(wxbot_id, report_type, report_time, speaker_id, wx_content_info_str):
    xnr_puid = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid'])['puid']
    report_dict = {
        'report_type': report_type,
        'report_time': report_time,
        'xnr_user_no': wxbot_id,
        'xnr_puid': xnr_puid,
        'speaker_id': speaker_id,
        'report_content': wx_content_info_str
    }
    report_id = wxbot_id + '_' + str(report_time)
    mark = 0
    try:
        wx_report_management_mappings()
        es_xnr.index(index=wx_report_management_index_name, doc_type=wx_report_management_index_type, id=report_id,body=report_dict)
        mark = 1
    except Exception,e:
        print e
    return 1