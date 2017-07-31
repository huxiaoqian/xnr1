# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import sys
from xnr.global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type,\
                             group_message_index_name_pre, group_message_index_type
from xnr.parameter import MAX_VALUE
from xnr.time_utils import get_groupmessage_index_list

def search_by_xnr_number(xnr_qq_number, date):
    # 需求：能够按虚拟人qq号查找其所有监控群的历史信息
    # 问题：暂无
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}}
                            # {"term":{"sensitive":}}
                        ]
                    }
                }
            }
            },
            "size": MAX_VALUE,
            "sort":{"timestamp":{"order":"desc"}}
        }
    index_name = group_message_index_name_pre + date
    result = es_xnr.search(index=index_name,doc_type=group_message_index_type,body=query_body)
    return result