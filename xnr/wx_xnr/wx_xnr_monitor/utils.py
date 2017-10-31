# -*- coding: utf-8 -*-
import time
import datetime
from xnr.wx_xnr.global_utils import es_xnr,wx_xnr_index_name,wx_xnr_index_type,\
                             wx_group_message_index_name_pre, wx_group_message_index_type
from xnr.wx_xnr.parameter import MAX_VALUE, DAY, group_message_windowsize
from xnr.wx_xnr.time_utils import get_wx_groupmessage_index_list, ts2datetime, datetime2ts
from xnr.wx_xnr.wx.control_bot import load_wxxnr_redis_data

#查看虚拟人监听到的所有群组的群消息，可指定起始、终止时间
def utils_search(wxbot_id, startdate='', enddate=''):
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
                            {"term":{"xnr_id": xnr_puid}},
                            {"term":{"sensitive_flag": 1}}                      ]
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