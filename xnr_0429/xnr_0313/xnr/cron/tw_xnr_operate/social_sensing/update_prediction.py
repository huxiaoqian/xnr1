# -*-coding:utf-8-*-

import sys
import time
import json
import math

from elasticsearch import Elasticsearch
from extract_feature_update import organize_feature, trendline_list
import pickle

reload(sys)
sys.path.append("../../")
from global_utils import es_flow_text as es_text
from global_utils import es_prediction
from time_utils import ts2datetime, datetime2ts, ts2date

def update_prediction(ts): # current ts
    query_body = {
        "query":{
            "range":{
                "timestamp":{
                    "gte": ts - 10*3600,
                    "lte": ts
                }
            }
        },
        "size":20000,
        "sort":{"timestamp":{"order":"asc"}}
    }

    es_results = es_prediction.search(index="social_sensing_text",doc_type="text",\
            body=query_body, _source=False,fields=["mid","timestamp"])["hits"]["hits"]
    print "get results lenth: ", len(es_results)
    mid_list = []
    mid_ts_list = []
    feature_list = []
    count = 0
    bulk_action = []
    with open("prediction_uid.pkl", "r") as f:
        uid_model = pickle.load(f)
    with open("prediction_weibo.pkl", "r") as f:
        weibo_model = pickle.load(f)

    print "finish loading"
    for item in es_results:
        mid = item["fields"]["mid"][0]
        mid_ts = item["fields"]["timestamp"][0]
        iter_feature = organize_feature(mid, mid_ts)
        feature_list.append(iter_feature)
        mid_list.append(mid)
        mid_ts_list.append(mid_ts)
        count += 1
        if count % 100 == 0:
            """
            weibo_prediction_result = weibo_model.predict(feature_list)
            uid_prediction_result = uid_model.predict(feature_list)
            print "finish prediction"
            for i in range(len(mid_list)):
                iter_dict = dict()
                iter_dict["mid"] = mid_list[i]
                iter_dict["uid_prediction"] = uid_prediction_result[i]
                iter_dict["weibo_prediction"] = weibo_prediction_result[i]
                tmp_trendline = trendline_list(mid_list[i], weibo_prediction_result[i],mid_ts_list[i])
                iter_dict["trendline"] = json.dumps(tmp_trendline)
                bulk_action.extend([{"update":{"_id":mid_list[i]}}, {"doc":iter_dict}])
                print uid_prediction_result[i], weibo_prediction_result[i],mid_list[i]
            print es_prediction.bulk(bulk_action,index="social_sensing_text",doc_type="text",timeout=600)
            """
            bulk_action = []
            mid_list = []
            mid_ts_list = []
            feature_list = []
            print "iter count: ",count
    if mid_list:
        weibo_prediction_result = weibo_model.predict(feature_list)
        uid_prediction_result = uid_model.predict(feature_list)
        print "finish prediction"
        for i in range(len(mid_list)):
            iter_dict = dict()
            iter_dict["mid"] = mid_list[i]
            iter_dict["uid_prediction"] = uid_prediction_result[i]
            iter_dict["weibo_prediction"] = weibo_prediction_result[i]
            tmp_trendline = trendline_list(mid_list[i], weibo_prediction_result[i],mid_ts_list[i])
            iter_dict["trendline"] = json.dumps(tmp_trendline)
            bulk_action.extend([{"update":{"_id":mid_list[i]}}, {"doc":iter_dict}])
            print uid_prediction_result[i], weibo_prediction_result[i],mid_list[i]
        es_prediction.bulk(bulk_action,index="social_sensing_text",doc_type="text",timeout=600)


if __name__ == "__main__":
    ts =  1479398400
    update_prediction(ts+10*3600)
    while 1:
        update_prediction(ts+10*3600)
        ts += 10*3600
        if ts-10*3600 > 1479484800:
            break
