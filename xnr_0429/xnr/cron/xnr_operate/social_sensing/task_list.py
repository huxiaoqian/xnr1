# -*- coding:utf-8 -*-

# 本程序定时启动，是监控任务的入口，从manag es中读取尚未完成的任务，送入redis的任务队列中，
# 由子程序从队列中pop出任务信息进行监控计算

import sys
import time
import json
import copy
import os
from social_sensing import social_sensing_task 
reload(sys)
sys.path.append("../../")
from global_utils import es_xnr as es
from global_utils import R_SOCIAL_SENSING as r
#from global_utils import weibo_social_sensing_task_index_name,weibo_social_sensing_task_index_type
from global_utils import index_sensing,type_sensing
#from global_utils import weibo_social_sensing_task_queue_name
from global_config import S_TYPE,S_DATE
from time_utils import ts2datetime, datetime2ts, ts2date, ts2datehour, datehour2ts,datetime2ts

def create_task_list():
    # 1. search from manage_sensing_task
    # 2. push to redis list-----task_work

    # print start info
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'task_list.py')
    if S_TYPE == 'test':
        now_ts = datetime2ts(S_DATE)-3600*10
    else:
        now_ts = datehour2ts(ts2datehour(time.time()-3600))
    print_log = "&".join([file_path, "start", ts2date(now_ts)])
    print print_log
    #ts = ts - 3600

    query_body = {
        "query":{
            "match_all": {}
        }
    }

    search_results = es.search(index=index_sensing, doc_type=type_sensing, body=query_body)['hits']['hits']

    count = 0
    if search_results:
        for iter_item in search_results:
            _id = iter_item['_id']
            item = iter_item['_source']
            task = []
            task.append(item['task_name']) # task_name
            try:
                task.append(json.loads(item['social_sensors'])) # social sensors
            except:
                task.append(item['social_sensors'])  # social sensors
            task.append(now_ts)
            task.append(item['xnr_user_no'])
            #task.append(given_ts)
            r.lpush("task_name", json.dumps(task))
            count += 1

    print count
    print_log = "&".join([file_path, "end", ts2date(time.time())])
    print print_log


if __name__ == "__main__":
    create_task_list()
    social_sensing_task()
