# -*- coding:utf-8 -*-
# version 3


import sys
import time
import json
import math
import numpy as np
from elasticsearch import Elasticsearch
from  mappings_social_sensing import mappings_sensing_task
from text_classify.test_topic import topic_classfiy
from duplicate import duplicate
from extract_feature_update import organize_feature, trendline_list
import pickle
reload(sys)
sys.path.append("../../../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_portrait as es_profile
from global_utils import R_SOCIAL_SENSING as r
from global_utils import es_xnr
from time_utils import ts2datetime, datetime2ts, ts2date

from parameter import topic_value_dict
AVERAGE_COUNT = 4000
MEAN_COUNT = 100


time_interval = 3600
forward_time_range = 12*3600
DAY = 24*3600
index_sensing_task = "social_sensing_task"
type_sensing_task = "social_sensing"
index_manage_social_task = "manage_sensing_task"
task_doc_type = "task"
forward_n = 24
initial_count = 12
flow_text_index_name_pre = "flow_text_"
flow_text_index_type = "text"
profile_index_name = "weibo_user"
profile_index_type = "user"


def get_weibo(item):
    keys = ["text","sensitive_words_string","sensitive", "uid", "user_fansnum", "mid", "keywords_string", "geo", "ip", "timestamp", "message_type"]
    results = dict()
    for key in keys:
        results[key] = item[key]
    return results


"""
def get_weibo(mid_list, ts):
    llen = len(mid_list)
    l_1000 = llen/1000
    index_list = []
    for i in range(3):
        index_list.append("flow_text_"+ts2datetime(ts-i*24*3600))
    results = dict()

    keys = ["text","sensitive_words_string","sensitive", "uid", "user_fansnum", "mid", "keywords_string", "geo", "ip", "timestamp", "message_type"]
    for i in range(l_1000+1):
        if mid_list[i*1000: (i+1)*1000]:
            query_body = {
                "query":{
                    "terms":{"mid":mid_list[i*1000: (i+1)*1000]}
                },
                "size":10000
            }

            es_results = es_text.search(index=index_list, doc_type="text", body=query_body)["hits"]["hits"]
            for item in es_results:
                item = item["_source"]
                tmp = dict()
                for key in keys:
                    tmp[key] = item[key]
                results[item["mid"]] = tmp

    return results
"""

# 获得前12个小时内 各个时间段内社会传感器发布微博的原创微博/转发微博/评论微博，计算均值和方差

def get_forward_numerical_info(task_name, ts):
    results = []
    ts_series = []
    for i in range(1, forward_n+1):
        ts_series.append(ts-i*time_interval)

    # check if detail es of task exists
    doctype = task_name
    index_exist = es_xnr.indices.exists_type(index_sensing_task, doctype)
    if not index_exist:
        print "new create task detail index"
        mappings_sensing_task(doctype)

    if ts_series:
        search_results = es_xnr.mget(index=index_sensing_task, doc_type=doctype, body={"ids":ts_series})['docs']
        found_count = 0
        average_origin = []
        average_retweeted = []
        average_commet = []
        average_total = []
        average_negetive = []
        for item in search_results:
            if item['found']:
                temp = item['_source']
                sentiment_dict = json.loads(temp['sentiment_distribution'])
                average_total.append(int(temp['weibo_total_number']))
                average_negetive.append(int(sentiment_dict["2"])+int(sentiment_dict['3'])+int(sentiment_dict['4'])+int(sentiment_dict['5'])+int(sentiment_dict['6']))
                found_count += 1

        if found_count > initial_count:
            number_mean = np.mean(average_total)
            number_std = np.std(average_total)
            sentiment_mean = np.mean(average_negetive)
            sentiment_std = np.mean(average_negetive)
            results = [1, number_mean, number_std, sentiment_mean, sentiment_std]
        else:
            results = [0]

    return results

# 给定社会传感器，查找原创微博列表
def query_mid_list(ts, social_sensors, time_segment, message_type=1):
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must":[
                            {"range": {
                                "timestamp": {
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"uid": social_sensors}},
                            {"term":{"message_type": message_type}}
                        ]
                    }
                }
            }
        },
        "sort": {"sentiment": {"order": "desc"}},
        "size": 10000
    }

    mid_dict = dict()

    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)
    if index_list:
        search_results = es_text.search(index=index_list, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    else:
        search_results = []
    origin_mid_list = set()
    if search_results:
        for item in search_results:
            if message_type == 1:
                origin_mid_list.add(item["_id"])
            else:
                origin_mid_list.add(item['_source']['root_mid'])
                mid_dict[item['_source']['root_mid']] = item["_id"] # 源头微博和当前转发微博的mid

    if message_type != 1:
    # 保证获取的源头微博能在最近两天内找到
        filter_list = []
        filter_mid_dict = dict()
        for iter_index in index_list:
            exist_es = es_text.mget(index=iter_index, doc_type="text", body={"ids":list(origin_mid_list)})["docs"]
            for item in exist_es:
                if item["found"]:
                    filter_list.append(item["_id"])
                    filter_mid_dict[item["_id"]] = mid_dict[item["_id"]]
        origin_mid_list = filter_list
        mid_dict = filter_mid_dict
    return list(origin_mid_list), mid_dict


# 给定原创微博list，搜索之前time_segment时间段内的微博总数，即转发和评论总数
def query_related_weibo(ts, origin_mid_list, time_segment):
    query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_count":{
                "terms":{"field": "message_type"}
            }
        }
    }

    return_results = {"origin": 0, "retweeted": 0, "comment": 0}
    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)
    if index_list:
        results = es_text.search(index=index_list, doc_type=flow_text_index_type,body=query_all_body)['aggregations']['all_count']['buckets']
        if results:
            for item in results:
                if int(item['key']) == 1:
                    return_results['origin'] = item['doc_count']
                elif int(item['key']) == 3:
                    return_results['retweeted'] = item['doc_count']
                elif int(item['key']) == 2:
                    return_results['comment'] = item['doc_count']
                else:
                    pass

    return_results['total_count'] = sum(return_results.values())
    return return_results



# 给定原创微博list， 聚合热门微博的转发量和评论量
def query_hot_weibo(ts, origin_mid_list, time_segment):
    query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_mid":{
                "terms":{"field": "root_mid", "size":400},
                "aggs":{
                    "message_type":{
                        "terms":{
                            "field":"message_type"
                        }
                    }
                }
            }
        }
    }

    return_results = dict()
    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)

    index_list.append(flow_text_index_name_pre+ts2datetime(ts-2*24*3600))
    if index_list:
        results = es_text.search(index=index_list, doc_type=flow_text_index_type,body=query_all_body)['aggregations']['all_mid']['buckets']
        if results:
            for item in results:
                temp_dict = dict()
                temp_dict[item['key']] = item['doc_count']
                detail = item['message_type']['buckets']
                detail_dict = dict()
                for iter_item in detail:
                    detail_dict[iter_item['key']] = iter_item['doc_count']
                temp_dict['retweeted'] = detail_dict.get(3, 0)
                temp_dict['comment'] = detail_dict.get(2, 0)
                return_results[item['key']] = temp_dict
        else:
            for item in origin_mid_list:
                temp_dict = dict()
                temp_dict[item] = 0
                temp_dict['retweeted'] = 0
                temp_dict['comment'] = 0
                return_results[item] = temp_dict

    return return_results

# 给定原创微博list，搜索之前time_segment时间段内的微博情绪
def aggregation_sentiment_related_weibo(ts, origin_mid_list, time_segment, message_type=1, uid_list=[]):
    if message_type == 1:
        query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_sentiments":{
                "terms":{ "field": "sentiment"}
            }
        }
        }
    else:
        query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}},
                            {"terms":{"directed_uid": uid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_sentiments":{
                "terms":{ "field": "sentiment"}
            }
        }
    }

    results = {"0": 0, "1": 0, "2":0, "3": 0, "4": 0, "5": 0, "6": 0}
    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)
    if index_list:
        search_results = es_text.search(index=index_list, doc_type=flow_text_index_type,body=query_all_body)['aggregations']['all_sentiments']['buckets']
        if search_results:
            for item in search_results:
                key = item['key']
                count = item['doc_count']
                results[key] = count
    #print "results: ", results, sum(results.values())
    return results

# 给定所有原创微博list，搜索在time-time-interval时间内的热门微博root-uid
def get_important_user(ts, origin_mid_list, time_segment):
    query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }}],
                        "should": [
                            {"terms":{"root_mid":origin_mid_list}},
                            {"terms":{"mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "sort":{"user_fansnum":{"order":"desc"}},
        "size": 1000
    }

    datetime = ts2datetime(ts - time_segment)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    results = []
    if origin_mid_list and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_all_body,fields=["uid"], _source=False)["hits"]["hits"]
        if search_results:
            for item in search_results:
                results.append(item['fields']['uid'][0])

    return results


def filter_mid(mid_list):
    llen = len(mid_list)
    l_1000 = llen/1000

    result = []

    for i in range(l_1000+1):
        tmp = mid_list[i*1000:(i+1)*1000]
        if tmp:
            es_results = es_xnr.mget(index="social_sensing_text", doc_type="text", body={"ids":tmp}, _source=False)["docs"]
            #print 'es_results:::',es_results
            for item in es_results:
                #print 'item::',item
                if not item["found"]:
                    result.append(item["_id"])

    return result


def social_sensing(task_detail):

    '''
    with open("prediction_uid.pkl", "r") as f:
        uid_model = pickle.load(f)
    with open("prediction_weibo.pkl", "r") as f:
        weibo_model = pickle.load(f)
    '''
    # 任务名 传感器 终止时间 之前状态 创建者 时间
    
    task_name = task_detail[0]
    social_sensors = task_detail[1]
    #ts = int(task_detail[2])
    ts = float(task_detail[2])

    xnr_user_no = task_detail[3]

    print ts2date(ts)
    index_list = []
    important_words = []
    datetime_1 = ts2datetime(ts)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_es = es_text.indices.exists(index=index_name_1)
    if exist_es:
        index_list.append(index_name_1)
    datetime_2 = ts2datetime(ts-DAY)
    index_name_2 = flow_text_index_name_pre + datetime_2
    exist_es = es_text.indices.exists(index=index_name_2)
    if exist_es:
        index_list.append(index_name_2)
    if es_text.indices.exists(index=flow_text_index_name_pre+ts2datetime(ts-2*DAY)):
        index_list.append(flow_text_index_name_pre+ts2datetime(ts-2*DAY))

    # PART 1
    
    #forward_result = get_forward_numerical_info(task_name, ts, create_by)
    # 之前时间阶段内的原创微博list/retweeted
    forward_origin_weibo_list, forward_1 = query_mid_list(ts-time_interval, social_sensors, forward_time_range)
    forward_retweeted_weibo_list, forward_3 = query_mid_list(ts-time_interval, social_sensors, forward_time_range, 3)
    # 当前阶段内原创微博list
    current_mid_list, current_1 = query_mid_list(ts, social_sensors, time_interval)
    current_retweeted_mid_list, current_3 = query_mid_list(ts, social_sensors, time_interval, 3)
    all_mid_list = []
    all_mid_list.extend(current_mid_list)
    all_mid_list.extend(current_retweeted_mid_list)
    all_mid_list.extend(forward_origin_weibo_list)
    all_mid_list.extend(forward_retweeted_weibo_list)
    all_origin_list = []
    all_origin_list.extend(current_mid_list)
    all_origin_list.extend(forward_origin_weibo_list)
    all_origin_list = list(set(all_origin_list))
    all_retweeted_list = []
    all_retweeted_list.extend(current_retweeted_mid_list)
    all_retweeted_list.extend(forward_retweeted_weibo_list)#被转发微博的mid/root-mid
    all_retweeted_list = list(set(all_retweeted_list))


    all_mid_list = filter_mid(all_mid_list)
    all_origin_list = filter_mid(all_origin_list)
    all_retweeted_list = filter_mid(all_retweeted_list)

    print "all mid list: ", len(all_mid_list)
    print "all_origin_list", len(all_origin_list)
    print "all_retweeted_list", len(all_retweeted_list)


    # 查询微博在当前时间内的转发和评论数, 聚合按照message_type
    #statistics_count = query_related_weibo(ts, all_mid_list, time_interval)
    if all_origin_list:
        #origin_weibo_detail = query_hot_weibo(ts, all_origin_list, time_interval) # 原创微博详情
        origin_weibo_detail = dict()
        for mid in all_origin_list:
            retweet_count = es_text.count(index=index_list, doc_type="text", body={"query":{"bool":{"must":[{"term":{"root_mid": mid}}, {"term":{"message_type":3}}]}}})["count"]
            comment_count = es_text.count(index=index_list, doc_type="text", body={"query":{"bool":{"must":[{"term":{"root_mid": mid}}, {"term":{"message_type":2}}]}}})["count"]
            tmp = dict()
            tmp["retweeted"] = retweet_count
            tmp["comment"] = comment_count
            origin_weibo_detail[mid] = tmp
    else:
        origin_weibo_detail = {}
    print "len(origin_weibo_detail): ", len(origin_weibo_detail)
    if all_retweeted_list:
        retweeted_weibo_detail = dict()
        for mid in all_retweeted_list:
            retweet_count = es_text.count(index=index_list, doc_type="text", body={"query":{"bool":{"must":[{"term":{"root_mid": mid}}, {"term":{"message_type":3}}]}}})["count"]
            comment_count = es_text.count(index=index_list, doc_type="text", body={"query":{"bool":{"must":[{"term":{"root_mid": mid}}, {"term":{"message_type":2}}]}}})["count"]
            tmp = dict()
            tmp["retweeted"] = retweet_count
            tmp["comment"] = comment_count
            retweeted_weibo_detail[mid] = tmp
        #retweeted_weibo_detail = query_hot_weibo(ts, all_retweeted_list, time_interval) # 转发微博详情
    else:
        retweeted_weibo_detail = {}
    print "len(retweeted_weibo_detail): ", len(retweeted_weibo_detail)
    #current_total_count = statistics_count['total_count']

    # 当前阶段内所有微博总数
    #current_retweeted_count = statistics_count['retweeted']
    #current_comment_count = statistics_count['comment']

    #all_mid_list = list(set(all_origin_list[:100]) | set(all_retweeted_list[:100]))


    # 感知到的事, all_mid_list
    sensitive_text_list = []
    tmp_sensitive_warning = ""
    text_dict = dict() # 文本信息
    mid_value = dict() # 文本赋值
    duplicate_dict = dict() # 重合字典
    portrait_dict = dict() # 背景信息
    classify_text_dict = dict() # 分类文本
    classify_uid_list = []
    duplicate_text_list = []
    sensitive_words_dict = dict()
    sensitive_weibo_detail = {}
    trendline_dict = dict()
    all_text_dict = dict()

    # 有事件发生时开始
    if 1:
        print "index_list:", index_list

        if index_list and all_mid_list:
            query_body = {
                "query":{
                    "filtered":{
                        "filter":{
                            "terms":{"mid": all_mid_list}
                        }
                    }
                },
                "size": 5000
            }
            search_results = es_text.search(index=index_list, doc_type="text", body=query_body)['hits']['hits']
            print "search mid len: ", len(search_results)
            tmp_sensitive_warning = ""
            text_dict = dict() # 文本信息
            mid_value = dict() # 文本赋值
            duplicate_dict = dict() # 重合字典
            portrait_dict = dict() # 背景信息
            classify_text_dict = dict() # 分类文本
            #classify_uid_list = []
            classify_mid_list = []
            duplicate_text_list = []
            sensitive_words_dict = dict()
            mid_ts_dict = dict() # 文本发布时间
            uid_prediction_dict = dict()
            weibo_prediction_dict = dict()
            trendline_dict = dict()
            feature_prediction_list = []  # feature
            mid_prediction_list = [] # dui ying mid
            if search_results:
                for item in search_results:
                    iter_uid = item['_source']['uid']
                    iter_mid = item['_source']['mid']
                    mid_ts_dict[iter_mid] = item["_source"]["timestamp"]
                    iter_text = item['_source']['text'].encode('utf-8', 'ignore')
                    iter_sensitive = item['_source'].get('sensitive', 0)
                    tmp_text = get_weibo(item['_source'])
                    all_text_dict[iter_mid] = tmp_text

                    duplicate_text_list.append({"_id":iter_mid, "title": "", "content":iter_text.decode("utf-8",'ignore')})

                    if iter_sensitive:
                        tmp_sensitive_warning = signal_sensitive_variation #涉及到敏感词的微博
                        sensitive_words_dict[iter_mid] = iter_sensitive

                    keywords_dict = json.loads(item['_source']['keywords_dict'])
                    personal_keywords_dict = dict()
                    for k, v in keywords_dict.iteritems():
                        k = k.encode('utf-8', 'ignore')
                        personal_keywords_dict[k] = v
                    classify_text_dict[iter_mid] = personal_keywords_dict
                    #classify_uid_list.append(iter_uid)
                    classify_mid_list.append(iter_mid)

                # 去重
                print "start duplicate"
                if duplicate_text_list:
                    dup_results = duplicate(duplicate_text_list)
                    for item in dup_results:
                        if item['duplicate']:
                            duplicate_dict[item['_id']] = item['same_from']

                # 分类
                print "start classify"
                mid_value = dict()
                if classify_text_dict:
                    #classify_results = topic_classfiy(classify_uid_list, classify_text_dict)
                    classify_results = topic_classfiy(classify_mid_list, classify_text_dict)
                    
                    #print "classify_results: ", classify_results

                    for k,v in classify_results.iteritems(): # mid:value
                        #mid_value[k] = topic_value_dict[v[0]]
                        mid_value[k]=v[0]
                        #feature_list = organize_feature(k, mid_ts_dict[k])
                        #feature_prediction_list.append(feature_list) # feature list
                        #mid_prediction_list.append(k) # corresponding 
                    
                # prediction
                """
                print "start prediction"
                weibo_prediction_result = weibo_model.predict(feature_prediction_list)
                uid_prediction_result = uid_model.predict(feature_prediction_list)
                for i in range(len(mid_prediction_list)):
                    if  i % 100 == 0:
                        print i
                    uid_prediction_dict[mid_prediction_list[i]] = uid_prediction_result[i]
                    weibo_prediction_dict[mid_prediction_list[i]] = weibo_prediction_result[i]
                    tmp_trendline = trendline_list(mid_prediction_list[i], weibo_prediction_result[i], mid_ts_dict[mid_prediction_list[i]])
                    trendline_dict[mid_prediction_list[i]] = tmp_trendline
                """
    # organize data

    mid_list = all_text_dict.keys()
    print "final mid:", len(mid_list)
    print "intersection: ", len(set(mid_list)&set(all_mid_list))
    bulk_action = []
    count = 0
    for mid in mid_list:
        iter_dict = dict()
        if origin_weibo_detail.has_key(mid):
            iter_dict.update(origin_weibo_detail[mid])
            iter_dict["type"] = 1
        elif retweeted_weibo_detail.has_key(mid):
            iter_dict.update(retweeted_weibo_detail[mid])
            iter_dict["type"] = 3
        else:
            iter_dict["retweeted"] = 0
            iter_dict["comment"] = 0
            print "mid in all_mid_list: ", mid in set(all_mid_list)

        #iter_dict["trendline"] = json.dumps(trendline_dict[mid])
        if duplicate_dict.has_key(mid):
            iter_dict["duplicate"] = duplicate_dict[mid]
        else:
            iter_dict["duplicate"] = ""

        #iter_dict["uid_prediction"] = uid_prediction_dict[mid]
        #iter_dict["weibo_prediction"] = weibo_prediction_dict[mid]
        iter_dict["compute_status"] = 0  # 尚未计算
        iter_dict["topic_field"] = mid_value[mid]
        iter_dict["detect_ts"] = ts
        iter_dict["xnr_user_no"] = xnr_user_no

        iter_dict.update(all_text_dict[mid])
        count += 1
        print 'iter_dict:::',iter_dict
        _id = xnr_user_no + '_' + mid
        bulk_action.extend([{"index":{"_id": _id}}, iter_dict])
        if count % 500 == 0:
            es_xnr.bulk(bulk_action, index="social_sensing_text", doc_type="text", timeout=600)
            bulk_action = []


    if bulk_action:
        es_xnr.bulk(bulk_action, index="social_sensing_text", doc_type="text", timeout=600)


    return "1"

