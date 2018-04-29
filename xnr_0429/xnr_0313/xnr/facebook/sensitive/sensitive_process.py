# -*-coding:utf-8-*-

import json
import time
import os

from DFA_filter import createWordTree,searchWord 
from parameter import RUN_TYPE, RUN_TEST_TIME, DAY,sensitive_score_dict
from global_config import SENSITIVE_WORDS_PATH,S_DATE,S_TYPE
from global_utils import R_ADMIN as r_sensitive


def sensitive_process(text,timestamp):

    ## 人物敏感度
    iter_results = {} # iter_results = {uid:{}}
    now_ts = time.time()
    #run_type
    today_sensitive_results = {}
    if S_TYPE != 'test':
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = datetime2ts(S_DATE)

    for i in range(WEEK,0,-1):
        ts = now_date_ts - DAY*i
        sensitive_results = r_cluster_3.hmget('sensitive_'+str(ts), uid_list)
        count = 0
        for uid in uid_list:
            if uid not in today_sensitive_results:
                today_sensitive_results[uid] = {}

            #compute sensitive
            sensitive_item = sensitive_results[count]
            if sensitive_item:
                uid_sensitive_dict = json.loads(sensitive_item)
            else:
                uid_sensitive_dict = {}
            for sensitive_word in uid_sensitive_dict:
                try:
                    iter_results[uid]['sensitive'][sensitive_word] += uid_sensitive_dict[sensitive_word]
                except:
                    iter_results[uid]['sensitive'][sensitive_word] = uid_sensitive_dict[sensitive_word]
                if ts == now_date_ts - DAY:
                    try:
                        today_sensitive_results[uid][sensitive_word] += uid_sensitive_dict[sensitive_word]
                    except:
                        today_sensitive_results[uid][sensitive_word] = uid_sensitive_dict[sensitive_word]

        for uid in uid_list:
        results[uid] = {}

    

    ## 信息敏感度
    sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
    if sensitive_words_dict:
        item['sensitive_words_string'] = "&".join(sensitive_words_dict.keys())
        item['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
    else:
        item['sensitive_words_string'] = ""
        item['sensitive_words_dict'] = json.dumps({})
                    
    sensitive_words_dict = json.loads(item['sensitive_words_dict'])
    if sensitive_words_dict:
        score = 0
        for k,v in sensitive_words_dict.iteritems():
            tmp_stage = r_sensitive.hget("sensitive_words", k)
            if tmp_stage:
                score += v*sensitive_score_dict[str(tmp_stage)]
        index_body['sensitive'] = score