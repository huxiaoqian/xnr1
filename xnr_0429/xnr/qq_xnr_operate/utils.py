# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import time
import sys
import json
from xnr.global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type,\
                             group_message_index_name_pre, group_message_index_type, r, r_qq_speak_num_pre
from xnr.parameter import MAX_VALUE, DAY, group_message_windowsize
from xnr.time_utils import get_groupmessage_index_list, ts2datetime, datetime2ts


from xnr.qq.sendQQGroupMessage import sendfromweb,sendfromweb_v2

def get_my_group(xnr_user_no,groups):

    es_get_results = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']

    qq_groups = es_get_results['qq_groups']
    my_group_list = {}
    for group_number in qq_groups:
        if group_number:
            try:
                my_group_list[group_number] = groups[group_number].strip()
            except:
                continue
    return my_group_list

def get_my_group_v2(xnr_user_no):

    try:
        es_get_results = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
        group_info = json.loads(es_get_results['group_info'])

    except:
        group_info = {}
        
    return group_info

def search_by_xnr_number(xnr_qq_number, current_date,group_qq_name):

    group_qq_name_list = group_qq_name.encode('utf-8').split('，')
    # 用于显示操作页面初始的所有群历史信息
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}},
                            {'terms':{'qq_group_nickname':group_qq_name_list}}

                        ]
                    }
                }
            }
            },
            "size": MAX_VALUE,
            "sort":{"timestamp":{"order":"desc"}}
        }

    enddate = current_date
    startdate = ts2datetime(datetime2ts(enddate)-group_message_windowsize*DAY)
    index_names = get_groupmessage_index_list(startdate,enddate)
    #print 'index_names::',index_names
    index_names.reverse()
    results = {}
    for index_name in index_names:
        # if not es_xnr.indices.exsits(index=index_name):
        #     continue
        try:
            result = es_xnr.search(index=index_name, doc_type=group_message_index_type,body=query_body)
            
            if results != {}:
                results['hits']['hits'].extend(result['hits']['hits'])
                
            else:
                results=result #.copy()
                
        except:
            pass
    # results_new = []
    # for index_name in index_names:

    #     try:
    #         es_results = es_xnr.search(index=index_name, doc_type=group_message_index_type,body=query_body)['hits']['hits']
    #         print 'es_results::',es_results
    #         for es_result in es_results:
    #             es_result = es_result['_source']
    #             results_new.append(es_result)
    #     except:
    #         continue

    return results

def search_by_period(xnr_qq_number,startdate,enddate,group_qq_name):

    group_qq_name_list = group_qq_name.encode('utf-8').split('，')

    results = {}
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}},
                            {'terms':{'qq_group_nickname':group_qq_name_list}}

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
    index_names.reverse()
    #print 'index_names::',index_names

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


def send_message(xnr_qq_number,group,content):
    
    current_date = ts2datetime(int(time.time()))
    group_list = group.split(',')           #发送多个群消息

    for g in group_list:
        # result = sendfromweb(xnr_qq_number,g,content)

        # redis计数 ： qq_speak_num_2018-05-04  - 1
        r_qq_speak_num = r_qq_speak_num_pre + current_date
        #try:
        speak_num = r.hget(r_qq_speak_num, xnr_qq_number)
	
        if speak_num == None:
            speak_num = 0
        #print 'r_qq_speak_num..',r_qq_speak_num
	#print 'xnr_qq_number...',xnr_qq_number
	#print 'speak_num...',speak_num	
        r.hset(r_qq_speak_num,xnr_qq_number,str(speak_num+1))

        result = sendfromweb_v2(xnr_qq_number,g,content)        #多端口方法

    # print result
    return result
    



# 暂时用不到的函数


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
    #print must_query_list
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
