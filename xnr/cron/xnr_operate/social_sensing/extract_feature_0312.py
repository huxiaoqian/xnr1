# -*-coding:utf-8-*-

import time
import math
import sys
from create_trendline_task import get_trend
from trendline_prediction.weibo_series_prediction import *

reload(sys)
sys.path.append("../../")
import json
from time_utils import ts2datetime, datetime2ts, ts2datehour, datehour2ts

from elasticsearch import Elasticsearch
from global_utils import es_flow_text as es
from parameter import diffusion_time, diffusion_time_interval
from parameter import RUN_TYPE


topic_field_dict = {'art':1,'computer':2,'economic':3, 'education':4,'environment':5, 'medicine':6,\
                    'military':7,'politics':8,'sports':9,'traffic':10,'life':11,'anti-corruption':12,\
                     'employment':13,'fear-of-violence':14, 'house':15,'law':16,'peace':17,\
                     'religion':18,'social-security':19,'null':20}



def organize_feature(mid, topic):
    if RUN_TYPE:
        ts = time.time()
    else:
        ts = datetime2ts("2016-11-21")
    index_list = []
    for i in range(7):
        index_list.append("flow_text_"+ts2datetime(ts-i*24*3600))

    result = dict()
    for iter_index in index_list:
        if not es.indices.exists(index=iter_index):
            continue
        try:
            result = es.get(index=iter_index, doc_type="text", id=mid)["_source"]
            break
        except:
            pass
    if not result:
        return [0, 0, 0, 0, 0, 0,0]

    ts = result["timestamp"]

    query_body = {
        "query":{
            "term":{"root_mid":mid}
        }
    }
    #total_weibo
    #count = es.count(index=index_list, doc_type="text", body=query_body)["count"]

    query_body_uid = {
        "query":{
            "term":{"root_mid":mid}
        },
        "aggs":{
            "uid_count":{
                "cardinality":{"field": "uid"}
            }
        }
    }
    # total_uid
    #total_uid_count = es.search(index=index_list, doc_type="text", body=query_body_uid)['aggregations']["uid_count"]["value"]



    feature_list = []
    feature_list.append(math.log(result["user_fansnum"]+1))
    query_body_ts = {
        "query":{
            "bool":{
                "must":[
                    {"term":{"root_mid":mid}},
                    {"range":{
                        "timestamp":{
                            "lt": ts + 3600*10
                        }
                    }}
                ]
            }
        },
        "aggs":{
            "weibo_type":{
                "terms":{"field": "message_type"}
            }
        }
    }
    comment = 0
    retweet = 0
    tmp_count = es.search(index=index_list, doc_type="text", body=query_body_ts)['aggregations']["weibo_type"]["buckets"]
    if tmp_count:
        for item in tmp_count:
            if int(item["key"]) == 2:
                comment = item["doc_count"]
            elif int(item["key"]) == 3:
                retweet = item["doc_count"]
    feature_list.append(comment+retweet)
    feature_list.append(retweet)
    feature_list.append(comment)
    feature_list.append(retweet/float(comment+retweet+1))
    feature_list.append(comment/float(comment+retweet+1))
    query_body_uid = {
        "query":{
            "bool":{
                "must":[
                    {"term":{"root_mid":mid}},
                    {"range":{
                        "timestamp":{
                            "lt": ts + 3600*10
                        }
                    }}
                ]
            }
        },
        "aggs":{
            "uid_count":{
                "cardinality":{"field": "uid"}
            }
        }
    }
    uid_count = es.search(index=index_list, doc_type="text", body=query_body_uid)['aggregations']["uid_count"]["value"]
    feature_list.append(uid_count)
    #feature_list.append(topic_field_dict[topic])


    return feature_list


def trendline_list(mid, total_value):
    if RUN_TYPE:
        ts = time.time()
    else:
        ts = datetime2ts("2016-11-19")
    index_list = []
    nn = 24*3600/diffusion_time_interval ###
    for i in range(diffusion_time):
        index_list.append("flow_text_"+ts2datetime(ts-i*24*3600))

    result = dict()
    for iter_index in index_list:
        if not es.indices.exists(index=iter_index):
            continue
        try:
            result = es.get(index=iter_index, doc_type="text", id=mid)["_source"]
            break
        except:
            pass

    if not result:
        return []


    current_list = []
    rising_list = []
    falling_list = []
    exist_time_list = []
    total_time_list = []

    timestamp = result["timestamp"]
    start_ts = timestamp
    timestamp = datehour2ts(ts2datehour(timestamp))
    for i in range(diffusion_time*nn):
        total_time_list.append(timestamp+i*diffusion_time_interval)

    # diffusion more than 5 days, return time list as far
    if 1:
        while 1:
            query_body = {
                "query":{
                    "bool":{
                        "must":[
                            {"term":{"root_mid": mid}},
                            {"range":{
                                "timestamp":{
                                    "gte": timestamp,
                                    "lt": timestamp + diffusion_time_interval
                                }
                            }}
                        ]
                    }
                }
            }
            index_name = "flow_text_"+ts2datetime(timestamp)
            count = es.count(index=index_name, doc_type="text", body=query_body)["count"]
            current_list.append(count)
            exist_time_list.append(timestamp)
            timestamp += diffusion_time_interval
            if timestamp >= ts:
                break

    left_set = set(total_time_list) - set(exist_time_list)
    left_list = sorted(list(left_set), reverse=False)

    max_value = max(current_list)
    index_exist = len(current_list)
    value = current_list

    expected_value = total_value*0.8/(0.2*nn*diffusion_time)
    if expected_value <= max_value:
        top_value = (max_value +total_value)/2
    else:
        top_value = expected_value

    # weibo prediction
    k = 5
    h = 0.5
    peak = spd(value,h,k)
    flag = judge(peak,value)
    if len(flag) == 2:
        paras = getTwoBeauties(value,flag[0],flag[1])
        paras[-1] = diffusion_time*nn
        series = bassTwoPeaks(paras)
    else:
        paras = getSingleBeauty(value)
        paras[-1] = diffusion_time*nn
        series = bassOnePeak(paras)

    # 预测峰值位置
    predict_climax = series.index(max(series))



    if predict_climax > index_exist:
        predict_climax_left = predict_climax - len(current_list)
        rise_trend, fall_trend = get_trend(left_list, predict_climax_left, value[-1], top_value)
        true_climax = exist_time_list[0] + (exist_time_list[1]-exist_time_list[0])*predict_climax
    else:
        top_value = value[-1]
        rise_trend, fall_trend = get_trend(left_list, 0, value[-1], 1)
        true_climax = exist_time_list[value.index(max(value))]
        top_value = max(value)

    results = dict()
    results["climax"] = [true_climax, top_value]
    results["rise_trend"] = rise_trend
    results["fall_trend"] = fall_trend
    new_list = []
    for i in range(len(exist_time_list)):
        new_list.append([exist_time_list[i], value[i]])
    results["exist_trend"] = new_list

    return results

if __name__ == "__main__":
    print trendline_list("4042757532196878", 110)


