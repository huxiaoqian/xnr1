# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import sys
from xnr.global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type,\
                             group_message_index_name_pre, group_message_index_type
from xnr.parameter import MAX_VALUE, DAY, group_message_windowsize
from xnr.time_utils import get_groupmessage_index_list,ts2datetime,datetime2ts,ts2date,date2ts

def search_by_xnr_number(xnr_qq_number, current_date):
    # 用于显示操作页面初始的所有群历史信息
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number},
                            "term":{"sensitive_flag":1}
                            }

                        ]
                    }
                }
            }
            },
            "size": MAX_VALUE,
            "sort":{"sensitive_value":{"order":"desc"}}
        }

    enddate = current_date
    startdate = ts2datetime(datetime2ts(enddate)-group_message_windowsize*DAY)
    index_names = get_groupmessage_index_list(startdate,enddate)
    print index_names
    results = {}
    for index_name in index_names:
        # if not es_xnr.indices.exsits(index=index_name):
        #     continue
        try:
            result = es_xnr.search(index=index_name, doc_type=group_message_index_type,body=query_body)
            if results != {}:
                results['hits']['hits'].extend(result['hits']['hits'])
            else:
                results=result.copy()
        except:
            pass
    return results


def search_by_period(xnr_qq_number,startdate,enddate):
    results = {}
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number},
                            "term":{"sensitive_flag":1}
                            }

                        ]
                    }
                }
            }
            },
            "size": MAX_VALUE,
            "sort":{"timestamp":{"order":"desc"}}
    }
    # es.search(index=”flow_text_2013-09-02”, doc_type=”text”, body=query_body)

    index_names = get_groupmessage_index_list(startdate,enddate)
    for index_name in index_names:
        # if not es_xnr.indices.exsits(index_name):
        #     continue
        try:
            result = es_xnr.search(index=index_name, doc_type=group_message_index_type,body=query_body)
            if results != {}:
                results['hits']['hits'].extend(result['hits']['hits'])
            else:
                results=result.copy()
        except:
            pass
    if results == {}:
        results={'hits':{'hits':[]}}
    return results
