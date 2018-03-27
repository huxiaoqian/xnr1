# -*- coding: UTF-8 -*-
import re
import sys
import csv
import json
import time
import redis

sys.path.append('../../')

from global_config import R_BEGIN_TIME
from global_utils import R_retweet, fb_retweet_dict, tw_retweet_dict

r_begin_ts = datetime2ts(R_BEGIN_TIME)

# two weeks retweet relation write to one db
# need add delete module
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = (((date_ts - r_begin_ts) / Day) / 7) % 2 + 1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number

#use to save retweet and be_retweet
#write in version: 15-12-08
#input: uid, root_uid, timestamp
#output: {'retweet_'+date_ts:{uid:{root_uid:count, ...}}}   {'be_retweet_'+date_ts:{root_uid:{uid:count, ...}}}
def save_retweet(uid, root_uid, timestamp):
    db_number = get_db_num(timestamp)
    r = retweet_redis_dict[str(db_number)]
    #r.hincrby('retweet_'+str(uid), str(root_uid), 1)
    r.hincrby('be_retweet_'+str(root_uid), str(uid), 1)
    # R_SPARK.hincrby('retweet_'+str(uid), str(root_uid), 1)
    # R_SPARK.hincrby('be_retweet_'+str(root_uid), str(uid), 1)

