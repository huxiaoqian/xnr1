# -*- coding: utf-8 -*-
import time
import datetime
from xnr.wx_xnr.global_utils import es_xnr,wx_xnr_index_name,wx_xnr_index_type,\
                             wx_group_message_index_name_pre, wx_group_message_index_type
from xnr.wx_xnr.parameter import MAX_VALUE, DAY
from xnr.wx_xnr.time_utils import get_wx_groupmessage_index_list, ts2datetime, datetime2ts
from xnr.wx_xnr.wx.control_bot import load_wxxnr_redis_data, send_msg

def utils_send_msg(wxbot_id, puids, msg):
    return send_msg(wxbot_id, puids, msg)

def utils_load_groups(wxbot_id):
    try:
        es_get_results = es_xnr.get(index=wx_xnr_index_name,doc_type=wx_xnr_index_type,id=wxbot_id)['_source']
        wx_groups_puid = es_get_results['wx_groups_puid']
        wx_groups_nickname = es_get_results['wx_groups_nickname']
        groups = {}
        for i in range(len(wx_groups_puid)):
            groups[wx_groups_puid[i]] = wx_groups_nickname[i]
        return groups
    except Exception,e:
        print e
        return 0

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

#查看监听到的一个指定群组的群消息，可指定起始、终止时间。{'msg_type':'Text'}
def utils_search_by_group_puid(wxbot_id, group_puid, period, startdate='', enddate=''):
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
                        {"term":{"xnr_id":xnr_puid}},
                        {'term':{'group_id':group_puid}},
                        {'term':{'msg_type':'Text'.lower()}}
                    ]
                }
            }
        }
        },
        "size": MAX_VALUE,
        "sort":{"timestamp":{"order":"desc"}}
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