# -*- coding:utf-8 -*-

import os
import sys
import time
import json
from sensing_v5 import social_sensing
reload(sys)
sys.path.append("../../")
from global_utils import es_xnr as es
from global_utils import R_SOCIAL_SENSING as r
#from global_utils import weibo_social_sensing_task_queue_name
from time_utils import ts2date

def social_sensing_task():
    # 1. print start info
    count = 0
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'social_sensing.py')
    now_ts = ts2date(time.time())
    print_log = "&".join([file_path, "start", now_ts])
#    print print_log #打印开始信息

    while 1:
        temp = r.rpop("task_name")
        if not temp:
            print count
            now_ts = str(int(time.time()))
            print_log = "&".join([file_path, "end", now_ts])
            break  # finish all task in task_list
        task_detail = json.loads(temp)
        count += 1
        social_sensing(task_detail)

if __name__ == "__main__":
    social_sensing_task()
