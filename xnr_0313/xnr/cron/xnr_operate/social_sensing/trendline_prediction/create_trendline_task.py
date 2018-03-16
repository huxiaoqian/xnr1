# -*-coding:utf-8-*-

import time
import json
from dispose_data import dispose_data
from weibo_series_prediction import *
import math
import numpy as np

import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_prediction, r_trendline, RUN_TYPE
from global_config import task_trendline,index_manage_prediction_task, type_manage_prediction_task,\
        index_type_prediction_task, pre_trendline, index_macro_feature_result, type_macro_feature_result
from time_utils import ts2datehour, datehour2ts

def create_task():
    ts = time.time()
    if RUN_TYPE:
        current_ts = datehour2ts(ts2datehour(ts))
    else:
        current_ts = 1482861600
    query_body = {
        "query": {
            "term":{"finish":"0"}
        },
        "size":10000
    }

    results = es_prediction.search(index=index_manage_prediction_task,\
            doc_type=type_manage_prediction_task, body=query_body)["hits"]["hits"]
    for item in results:
        print item
        task_name = item["_source"]["pinyin_task_name"]
        stop_time = item["_source"]["stop_time"]
        print stop_time, current_ts
        if stop_time < current_ts:
            es_prediction.update(index=index_manage_prediction_task,\
                    doc_type=type_manage_prediction_task, id=task_name,  body={"doc":{"macro_trendline_finish":"1", "finish": "1"}})
        else:
            r_trendline.lpush(task_trendline, task_name)


def task_list():
    create_task()
    if RUN_TYPE:
        current_ts = datehour2ts(ts2datehour(time.time()))
    else:
        current_ts = 1482861600
    while 1:
        task_detail = r_trendline.rpop(task_trendline)
        print task_detail
        if not task_detail:
            break

        task_name = task_detail
        while 1:
            micro_index = "micro_prediction_"+task_name
            es_exist = es_prediction.exists(index=micro_index, doc_type="micro_task", id=current_ts)
            if not es_exist:
                time.sleep(60)
            else:
                break


        # obtain time series
        value, total_len, time_list, left_list = dispose_data(task_name, current_ts)

        # macro prediction result
        try:
            es_macro_result = es_prediction.get(index=index_macro_feature_result,\
                doc_type=type_macro_feature_result,id=task_name)["_source"]
            prediction_total_value = es_macro_result["predict_weibo_value"]
            top_value = prediction_total_value*0.8/(0.2*total_len)
        except:
            top_value = 0

        # 已知的最大值和位置
        max_exist = max(value)
        index_exist = len(value)

        if top_value <max_exist:
            top_value = 2*max_exist


        # weibo prediction
        k = 5
        h = 0.5
        peak = spd(value,h,k)
        flag = judge(peak,value)
        if len(flag) == 2:
            print("Two peaks:")
            paras = getTwoBeauties(value,flag[0],flag[1])
            paras[-1] = total_len
            series = bassTwoPeaks(paras)
        else:
            print("Single peak:")
            paras = getSingleBeauty(value)
            paras[-1] = total_len
            series = bassOnePeak(paras)

        # 预测峰值位置
        predict_climax = series.index(max(series))



        if predict_climax > index_exist:
            predict_climax_left = predict_climax - len(value)
            # 剩余走势图 climax位置 起止点值 最大值
            rise_trend, fall_trend = get_trend(left_list, predict_climax_left, value[-1], top_value)
            true_climax = time_list[0] + (time_list[1]-time_list[0])*predict_climax
        else:
            top_value = value[-1]
            rise_trend, fall_trend = get_trend(left_list, 0, value[-1], 1)
            true_climax = time_list[value.index(max(value))]

        results = dict()
        results["climax"] = [true_climax, top_value]
        results["rise_trend"] = rise_trend
        results["fall_trend"] = fall_trend
        new_list = []
        for i in range(len(time_list)):
            new_list.append([time_list[i], value[i]])
        results["exist_trend"] = new_list
        r_trendline.set("trendline_"+task_name, json.dumps(results))
        print results


def get_trend(time_list, index, start_value, climax_value):
    rise_list = []
    fall_list = []
    if index == 1:
        rise_list.append([time_list[0], climax_value])
        # fall_list
        a = [[1,math.log(1)],[1,math.log(1+len(time_list)-index)]]
        a = np.array(a)
        b = [math.log(climax_value), math.log(start_value)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(1,len(time_list)-index+1):
            tmp_value = math.exp(np.dot([1, math.log(1+i)],x))
            fall_list.append([time_list[index+i-1], tmp_value])

    elif index == len(time_list)-1:
        a = [[1,1],[1,index]]
        a = np.array(a)
        b = [math.log(start_value), math.log(climax_value)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(index):
            tmp_value = math.exp(np.dot([1,1+i],x))
            rise_list.append([time_list[i], tmp_value])
        fall_list.append([time_list[-1], 0.5*climax_value])

    elif index == len(time_list):
        a = [[1,1],[1,index]]
        a = np.array(a)
        b = [math.log(start_value), math.log(climax_value)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(index):
            tmp_value = math.exp(np.dot([1,1+i],x))
            rise_list.append([time_list[i], tmp_value])

    elif index == 0:
        # fall_list
        a = [[1,math.log(1)],[1,math.log(1+len(time_list)-index)]]
        a = np.array(a)
        b = [math.log(start_value), math.log(1)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(1,len(time_list)-index+1):
            tmp_value = math.exp(np.dot([1, math.log(1+i)],x))
            fall_list.append([time_list[index+i-1], tmp_value])


    else:
        a = [[1,1],[1,index]]
        a = np.array(a)
        b = [math.log(start_value), math.log(climax_value)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(index):
            tmp_value = math.exp(np.dot([1,1+i], x))
            rise_list.append([time_list[i], tmp_value])

        # fall_list
        a = [[1,math.log(1)],[1,math.log(1+len(time_list)-index)]]
        a = np.array(a)
        b = [math.log(climax_value), math.log(start_value)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(1,len(time_list)-index+1):
            tmp_value = math.exp(np.dot([1, math.log(1+i)],x))
            fall_list.append([time_list[index+i-1], tmp_value])

    return rise_list, fall_list

if __name__ == "__main__":
    task_list()



