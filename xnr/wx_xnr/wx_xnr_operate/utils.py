# -*- coding: utf-8 -*-
import time
import datetime
from xnr.wx_xnr.global_utils import es_xnr,wx_xnr_index_name,wx_xnr_index_type,\
                             wx_group_message_index_name_pre, wx_group_message_index_type
from xnr.wx_xnr.parameter import MAX_VALUE, DAY, group_message_windowsize
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

#查看监听到的一个指定群组的群消息，可指定起始、终止时间
def utils_search_by_group_puid(wxbot_id, group_puid, startdate='', enddate=''):
    #end date
    if enddate == '':
        end = ts2datetime(time.time())
    else:
        end = enddate
    #start date 
    if startdate == '': 
        start = ts2datetime(datetime2ts(end) - group_message_windowsize*DAY)
    else:
        start = startdate
    index_names = get_wx_groupmessage_index_list(start, end)
    index_names.reverse()
    xnr_puid = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid'])['puid']
    query_body = {
    "query": {
        "filtered":{
            "filter":{
                "bool":{
                    "must":[
                        {"term":{"xnr_id":xnr_puid}},
                        {'term':{'group_id':group_puid}}

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