# -*-coding:utf-8-*-

import json
import time
import os

import sys
reload(sys)
sys.path.append('../')

from global_utils import flow_text_index_name_pre,flow_text_index_type,es_flow_text
from time_utils import ts2datetime
from parameter import sensitive_score_dict

def get_sensitive_info(timestamp,mid):
    index_name = flow_text_index_name_pre + ts2datetime(timestamp)
    try:
        item_result = es_flow_text.get(index=index_name,doc_type=flow_text_index_type,id=mid)['_source']
        sensitive_info = item_result['sensitive']
    except:
        sensitive_info = 0

    return sensitive_info

def get_sensitive_user(uid):
    try:
        tmp_stage = r_sensitive.hget('sensitive_words', uid)
        if tmp_stage:
            sensitive_score += v * sensitive_score_dict[str(tmp_stage)]
    except:
        sensitive_score = 0

    return sensitive_score
    
