# -*- coding: utf-8 -*-
import redis
from elasticsearch import Elasticsearch
from multiprocessing import Pool, Manager
import os, time, random
import math
import getopt
import sys
from googletrans import Translator
sys.path.append('../cron/trans')
sys.path.append('../')
from global_utils import es_xnr_2 as es, r_37 as r
from facebook_mappings import facebook_flow_text_mappings,facebook_count_mappings,facebook_user_mappings
from twitter_mappings import twitter_flow_text_mappings,twitter_count_mappings,twitter_user_mappings
from global_utils import twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
                    twitter_count_index_name_pre,twitter_count_index_type,\
                    twitter_user_index_name,twitter_user_index_type,\
                    facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
                    facebook_count_index_name_pre,facebook_count_index_type,\
                    facebook_user_index_name,facebook_user_index_type,\
                    twitter_flow_text_trans_task_name,facebook_flow_text_trans_task_name,\
                    twitter_user_trans_task_name,facebook_user_trans_task_name

batch = 3
redis_task = 'test'

def init_data(redis_task, length):
    for i in range(length):
        r.lpush(redis_task, [i,i+1])

def load_batch_data(redis_task):
    redis_task_temp = redis_task + '_temp'
    length = r.llen(redis_task)
    temp = r.lrange(redis_task, length-batch, length-1)
    if temp:
        for t in temp:
            r.rpush(redis_task_temp, eval(t))
        return redis_task_temp
    return False

def remove_batch_data(redis_task, length):
    redis_task_temp = redis_task + '_temp'
    for i in range(length):
        r.rpop(redis_task)
    r.delete(redis_task_temp)

def f(redis_task):
    redis_task_temp = load_batch_data(redis_task)
    print 'redis_task_temp: ', redis_task_temp, r.llen(redis_task_temp)
    if redis_task_temp:
        length = r.llen(redis_task_temp)
        while r.llen(redis_task_temp):
            l = r.rpop(redis_task_temp)
            print l
        remove_batch_data(redis_task, length)

init_data(redis_task, 9)
f(redis_task)



