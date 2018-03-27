# -*- coding:utf-8 -*-
# version 2


import sys
import time
import json
import math
import numpy as np
from elasticsearch import Elasticsearch
from  mappings_social_sensing import mappings_sensing_task
from clustering import freq_word, tfidf, kmeans, text_classify, cluster_evaluation
from get_group_keywords import count_trend, detect_burst
reload(sys)
sys.path.append("../../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait·
from global_utils import R_SOCIAL_SENSING as r
from time_utils import ts2datetime, datetime2ts
from global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_social_task
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import FORWARD_N as forward_n
from parameter import INITIAL_EXIST_COUNT as initial_count
from parameter import IMPORTANT_USER_NUMBER, IMPORTANT_USER_THRESHOULD, signal_brust, signal_track,\
                       signal_count_varition, signal_sentiment_varition, signal_nothing,signal_nothing_variation, \
                       unfinish_signal, finish_signal, signal_sensitive_variation, WARNING_SENSITIVE_COUNT
AVERAGE_COUNT = 500
MEAN_COUNT = 100

# 获得前12个小时内 各个时间段内社会传感器发布微博的原创微博/转发微博/评论微博，计算均值和方差

def get_forward_numerical_info(task_name, ts, create_by):
    results = []
    ts_series = []
    for i in range(1, forward_n+1):
        ts_series.append(ts-i*time_interval)

    # check if detail es of task exists
    doctype = create_by + "-" + task_name
    index_exist = es_user_portrait.indices.exists_type(index_sensing_task, doctype)
    if not index_exist:
        print "new create task detail index"
        mappings_sensing_task(doctype)

    if ts_series:
        search_results = es_user_portrait.mget(index=index_sensing_task, doc_type=doctype, body={"ids":ts_series})['docs']
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
                average_negetive.append(int(sentiment_dict["2"])+int(sentiment_dict['3'])+int(sentiment_dict['4']+int(sentiment_dict['5']+int(sentiment_dict['6'])
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
def query_mid_list(ts, social_sensors, time_segment):
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
                            {"terms":{"message_type": 1}}
                        ]
                    }
                }
            }
        },
        "sort": {"sentiment": {"order": "desc"}},
        "size": 10000
    }

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
        search_results = es_text.search(index=index_list, doc_type=flow_text_index_type, body=query_body, _source=False)["hits"]["hits"]
    else:
        search_results = []
    origin_mid_list = set()
    if search_results:
        for item in search_results:
            origin_mid_list.add(item["_id"])

    return list(origin_mid_list)


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
    print "return_results: ", return_results
    return return_results



# 给定原创微博list，搜索之前time_segment时间段内的微博情绪
def aggregation_sentiment_related_weibo(ts, origin_mid_list, time_segment):
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
        results = es_text.search(index=index_list, doc_type=flow_text_index_type,body=query_all_body)['aggregations']['all_count']['buckets']
        if results:
            for item in results:
                key = item['key']
                count = item['doc_count']
                results[key] = count
    print "results: ", results
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
        "aggs":{
            "all_count":{
                "terms":{"field":"uid", "size":1000}
            }
        }
    }

    datetime = ts2datetime(ts - time_segment)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    results = dict()
    if origin_mid_list and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_all_body)['aggregations']['all_count']['buckets']
        if search_results:
            for item in search_results:
                results[item['key']] = item['doc_count']

    return results

# 给定所有之前一段时间内的原创微博，聚合关键词和词频
def get_group_keywords(index_list, mid_list):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "terms":{"mid": mid_list}
                }
            }
        },
        "size":10000
    }

    text_dict = dict()#{"mid": {"word": 1}}
    word_set = set()
    tfidf_dict = dict()
    word_list = []
    search_results = es_text.search(index=index_list, doc_type=flow_text_index_type, body=query_body)['hits']['hits']
    if search_results:
        for item in search_results:
            keywords_dict = json.loads(item['_source']['keywords_dict'])
            mid = item['_id']
            freq_word = dict() #单条微博tf-idf统计
            total = sum(keywords_dict.values())
            for k,v in keywords_dict.iteritems():
                freq_word[k] = float(v)/float(total) #{"word":freq}
                word_set.add(k) #word set
            if freq_word:
                text_dict[mid] = freq_word

        item_tfidf = text_dict.values()
        total_count = len(text_dict)
        for word in word_set:
            word_tfidf = 0
            doc_count = 0
            for iter_dict in item_tfidf:
                if iter_dict.has_key(word):
                    doc_count += 1
            idf = math.log(float(total_count)/(float(doc_count+1))
            for iter_dict in item_tfidf:
                if iter_dict.has_key(word):
                    tf = iter_dict[word]
                    tfidf = tf*idf
                    try:
                        tfidf_dict[word] += tfidf
                    except:
                        tfidf_dict[k] = 1

        topk = int(len(word_set)*0.2)
        sorted_tfidf = sorted(tfidf_dict.iteritems(), key = lambda asd:asd[1],reverse = True)
        topk_list = sorted_tfidf[topk]
        for item in topk_list:
            word_list.append(item[0])

    return word_list


# 根据可能的事件关键词，搜索所有这个时间段内的原创微博文本
def get_weibo_text(ts, index_list, keywords_list):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"terms":{"keywords_string": keywords_list}},
                            {"term": {"message_type": 1}}
                        ]
                    }
                }
            }
        },
        "size": 2000
    }

    search_results = es_text.search(index=index_list, doc_type="text", body=query_body)['hits']['hits']
    text_list = []
    if search_results:
        for item in search_results:
            iter_mid = item['_source']['mid']
            iter_text = item['_source']['text']
            temp_dict = dict()
            temp_dict["mid"] = iter_mid
            temp_dict["text"] = iter_text
            text_list.append(temp_dict)

    return text_list

def social_sensing(task_detail):
    # 任务名 传感器 终止时间 之前状态 创建者 时间
    task_name = task_detail[0]
    social_sensors = task_detail[1]
    stop_time = task_detail[2]
    forward_warning_status = task_detail[3]
    create_by = task_detail[4]
    ts = int(task_detail[5])

    # PART 1
    forward_result = get_forward_numerical_info(task_name, ts, create_by)
    # 之前时间阶段内的原创微博list/retweeted
    forward_origin_weibo_list = query_mid_list(ts-time_interval, social_sensors, forward_time_range)
    # 当前阶段内原创微博list
    current_mid_list = query_mid_list(ts, social_sensors, time_interval)
    all_mid_list = []
    all_mid_list.extend(current_mid_list)
    all_mid_list.extend(forward_origin_weibo_list)
    print "all mid list: ", len(all_mid_list)

    # 查询微博在当前时间内的转发和评论数, 聚合按照message_type
    statistics_count = query_related_weibo(ts, all_mid_list, time_interval)
    current_total_count = statistics_count['total_count']

    # 当前阶段内所有微博总数
    current_origin_count = statistics_count['origin']
    current_retweeted_count = statistics_count['retweeted']
    current_comment_count = statistics_count['comment']


    # PART 2
    # 聚合当前时间内积极、中性、悲伤、愤怒情绪分布
    # sentiment_dict = {"0": "neutral", "1":"positive", "2":"sad", "3": "anger"}
    sentiment_count = {"0": 0, "1": 0, "2": 0, "3": 0}
    search_results = aggregation_sentiment_related_weibo(ts, all_mid_list, time_interval)
    sentiment_count = search_results
    print "sentiment_count: ", sentiment_count
    negetive_key = ["2", "3", "4", "5", "6"]
    negetive_count = 0
    for key in negetive_key:
        negetive_count += sentiment_count[key]


    # 聚合当前时间内重要的人
    important_uid_list = []
    datetime = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = get_important_user(ts, origin_mid_list, time_interval)
        important_uid_list = search_results.keys()
    # 根据获得uid_list，从人物库中匹配重要人物
    if important_uid_list:
        important_results = es_user_portrait.mget(index=portrait_index_name,doc_type=portrait_index_type, body={"ids": important_uid_list})['docs']
    else:
        important_results = {}
    filter_important_list = [] # uid_list
    if important_results:
        for item in important_results:
            if item['found']:
                if item['_source']['importance'] > IMPORTANT_USER_THRESHOULD:
                    filter_important_list.append(item['_id'])
    print filter_important_list


    #判断感知
    burst_reason = signal_nothing_variation
    warning_status = signal_nothing
    finish = unfinish_signal # "0"
    process_status = "1"

    if forward_result[0]:
        # 根据移动平均判断是否有时间发生
        mean_count = forward_result[1]
        std_count = forward_result[2]
        mean_sentiment = forward_result[3]
        std_sentiment = forward_result[4]
        if mean_count >= MEAN_COUNT and current_total_count > mean_count+1.96*std_count or current_total_count >= len(social_sensors)*0.2*AVERAGE_COUNT: # 异常点发生
            print "====================================================="
            if forward_warning_status == signal_brust: # 已有事件发生，改为事件追踪
                warning_status = signal_track
            else:
                warning_status = signal_brust
            burst_reason += signal_count_varition # 数量异常

        if negetive_count > mean_sentiment+1.96*std_sentiment and mean_sentiment >= MEAN_COUNT or negetive_count >= len(social_sensers)*0.2*AVERAGE_COUNT:
            warning_status = signal_brust
            burst_reason += signal_sentiment_varition # 负面情感异常, "12"表示两者均异常
            if forward_warning_status == signal_brust: # 已有事件发生，改为事件追踪
                warning_status = signal_track

    if int(stop_time) <= ts: # 检查任务是否已经完成
        finish = finish_signal
        process_status = "0"

    # 感知到的事, all_mid_list
    tmp_burst_reason = burst_reason
    topic_list = []

    # 填充微博文本
    # 有事件发生时开始
    if warning_status:
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
        if index_list and all_mid_list:
            word_list = get_group_keywords(index_list, all_mid_list)
            if word_list:
                for keyword in word_list:
                    trend_list = count_trend(ts, keyword)
                    burst_result = detect_burst(trend_list)
                    if burst_result:
                        important_words.append(keyword)

            text_list = get_weibo_text(ts, index_list, keywords_list)


    #
            if len(text_list) == 1:
                top_word = freq_word(text_list[0])
                topic_list = [top_word.keys()]
            elif len(text_list) == 0:
                topic_list = []
                tmp_burst_reason = "" #没有相关微博，归零
                print "***********************************"
            else:
                feature_words, input_word_dict = tfidf(text_list) #生成特征词和输入数据
                word_label, evaluation_results = kmeans(feature_words, text_list) #聚类
                inputs = text_classify(text_list, word_label, feature_words)
                clustering_topic = cluster_evaluation(inputs)
                print "=============================================================================="
                print "=============================================================================="
                sorted_dict = sorted(clustering_topic.items(), key=lambda x:x[1], reverse=True)
                topic_list = []
                if sorted_dict:
                    for item in sorted_dict:
                       topic_list.append(word_label[item[0]])
            print "topic_list, ", topic_list

    if not topic_list:
        warning_status = signal_nothing
        tmp_burst_reason = signal_nothing_variation

    results = dict()
    results['origin_weibo_number'] = current_origin_count
    results['retweeted_weibo_number'] = current_retweeted_count
    results['comment_weibo_number'] = current_comment_count
    results['weibo_total_number'] = current_total_count
    results['sentiment_distribution'] = json.dumps(sentiment_count)
    results['important_users'] = json.dumps(filter_important_list)
    results['unfilter_users'] = json.dumps(important_user_list)
    results['burst_reason'] = tmp_burst_reason
    results['timestamp'] = ts
    if tmp_burst_reason:
        results['clustering_topic'] = json.dumps(topic_list)
    # es存储当前时段的信息
    doctype = create_by + '-' + task_name
    es_user_portrait.index(index=index_sensing_task, doc_type=doctype, id=ts, body=results)

    # 更新manage social sensing的es信息
    temporal_result = es_user_portrait.get(index=index_manage_social_task, doc_type=task_doc_type, id=doctype)['_source']
    temporal_result['warning_status'] = warning_status
    temporal_result['burst_reason'] = tmp_burst_reason
    temporal_result['finish'] = finish
    temporal_result['create_by'] = create_by
    temporal_result['processing_status'] = process_status
    history_status = json.loads(temporal_result['history_status'])
    history_status.append([ts, task_name, warning_status])
    temporal_result['history_status'] = json.dumps(history_status)
    es_user_portrait.index(index=index_manage_social_task, doc_type=task_doc_type, id=doctype, body=temporal_result)

    return "1"

