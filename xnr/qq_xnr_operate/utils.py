# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import sys
from xnr.global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type,\
                             group_message_index_name_pre, group_message_index_type
from xnr.parameter import MAX_VALUE

def show_group_info():
    # 需求：按时间顺序显示各个历史信息
    # 问题：在不知道各个表中数据量的情况下制定查表规则，以及表间切换规则

    pass

def search_by_keyword(keyword, date):
    # 需求：能够按关键词查询历史信息
    # 问题：怎么在各个表之前切换返回适当数量的结果？
    # 子问题：需要预先知道所有虚拟人的qq号
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}}

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


def search_by_speaker_number(xnr_qq_number, speaker_number, date):
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}},
                            {"term":{"speaker_qq_number":speaker_number}}


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