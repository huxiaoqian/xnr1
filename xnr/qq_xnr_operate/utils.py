# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import sys
from xnr.global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type,\
                             group_message_index_name_pre, group_message_index_type
from xnr.parameter import MAX_VALUE
from xnr.time_utils import get_groupmessage_index_list

def show_group_info():
    # 需求：按时间顺序显示各个历史信息
    # 问题：在不知道各个表中数据量的情况下制定查表规则，以及表间切换规则

    pass

def search_by_keyword(keywords, date):
# 可以传入多个关键词但关键词之间需要以逗号分隔    
    must_query_list = []
    keyword_nest_body_list = []
    keywords_list = keywords.split(',')
    for keywords_item in keywords_list:
        keyword_nest_body_list.append({"wildcard":{"text":{"wildcard": "*"+keywords_item+"*"}}})
    must_query_list.append({'bool':{'should': keyword_nest_body_list}})
    print must_query_list
    query_body = {
        "query": {
           
            "bool":{
                "must": must_query_list
                }
            },
            "size": MAX_VALUE,
            "sort":{"timestamp":{"order":"desc"}}
        }

    # query_body = {
    #     "query":{
    #         "bool": {
    #             "must": [
    #                 {"wildcard": {
    #                     "text": {
    #                         "wildcard": "*" + keywords +"*"
    #                     }
    #                 }},
                    
    #             ]
    #         }
    #     },
    #     "size": MAX_VALUE
    # }
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


def search_by_speaker_nickname(xnr_qq_number, speaker_nickname, date):
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}},
                            {"term":{"speaker_qq_nickname":speaker_nickname}}


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


def search_by_period(startdate,enddate):
    results = {}
    query_body = {
        "query":{
            "match_all": {}
        },
        "sort":{"timestamp":{"order":"desc"}},
        "size": MAX_VALUE
    }
    # es.search(index=”flow_text_2013-09-02”, doc_type=”text”, body=query_body)

    index_names = get_groupmessage_index_list(startdate,enddate)
    for index_name in index_names:
        
        try:
            result = es_xnr.search(index=index_name, doc_type=group_message_index_type,body=query_body)
            if results != {}:
                results['hits']['hits'].extend(result['hits']['hits'])
            else:
                results=result.copy()
        except:
            pass
    return results