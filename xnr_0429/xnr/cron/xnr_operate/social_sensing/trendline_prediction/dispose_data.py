# -*-coding:utf-8-*-

import sys
import json
import redis

reload(sys)
sys.path.append('../../')
from global_utils import es_prediction
from global_config import index_manage_prediction_task, type_manage_prediction_task
from time_utils import ts2datehour, datehour2ts


def dispose_data(task_name, current_ts):
    es_result = es_prediction.get(index=index_manage_prediction_task, doc_type=type_manage_prediction_task, id=task_name)["_source"]
    macro_during = es_result['macro_during']
    start_ts = datehour2ts(ts2datehour(es_result["submit_time"]))
    task_start_ts = start_ts
    end_ts = datehour2ts(ts2datehour(es_result["stop_time"]))

    index_micro = "micro_prediction_" + task_name
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "range":{
                        "update_time":{
                            "lte": current_ts
                        }
                    }
                }
            }
        },
        "size": 10000,
        "sort":{"update_time":{"order":"asc"}}
    }
    micro_results = es_prediction.search(index=index_micro, doc_type="micro_task", body=query_body)["hits"]["hits"]
    total_list = []

    for item in micro_results:
        total_list.append(item["_source"]["total_count"])
    # 每个时间段内的微博量

    total_len = (end_ts-start_ts)/macro_during
    times = int(macro_during)/3600
    lenth = len(total_list)/times
    adjust_list = []
    time_list = []
    count = 0
    i = 0
    for item in total_list:
        count += item
        i += 1
        if i % times == 0:
            if start_ts <= current_ts:
                adjust_list.append(count)
                count = 0
                time_list.append(start_ts)
            else:
                break
        start_ts += 3600

    # 总得时间走势图
    total_time_list = []
    for i in range(total_len):
        total_time_list.append(task_start_ts+i*macro_during)

    left_time = list(set(total_time_list) - set(time_list))
    left_time = sorted(left_time)

    return adjust_list, total_len, time_list, left_time
    # 到目前为止校正的微博量 总得步长 到目前为止的时间段

