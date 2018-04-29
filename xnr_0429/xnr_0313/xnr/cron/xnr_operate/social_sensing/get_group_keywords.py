# -*-coding:utf-8-*-

import sys
import json
import numpy as np
import time
from config import load_scws, load_dict, cut_filter, re_cut
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait, es_user_profile, es_flow_text
from global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type, \
                         flow_text_index_name_pre, flow_text_index_type
from time_utils import ts2datetime, datetime2ts, ts2date
from parameter import DAY
from parameter import SOCIAL_SENSOR_TIME_INTERVAL as interval

#sw = load_scws()
#cx_dict = set(['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@','j'])
cx_dict = set(['Ng','n','nr','ns','nt','nz']) # 关键词词性词典, 保留名词

# 1. 获取用户最近两天的微博，抽取关键词作为监测目标
def get_group_keywords(uid_list):
    now_ts = time.time()
    now_ts = datetime2ts('2013-09-03')
    former_ts = now_ts - DAY
    flow_index_1 = flow_text_index_name_pre + ts2datetime(now_ts)
    flow_index_2 = flow_text_index_name_pre + ts2datetime(former_ts)
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "terms":{
                        "uid":uid_list
                    }
                }
            }
        },
        "size":10000
    }
    text_list = [] # 为分词前的文本
    word_dict = dict() # 分词后的word dict
    text_results = es_flow_text.search(index=[flow_index_1, flow_index_2], doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    if text_results:
        for item in text_results:
            iter_text = item['_source']['text'].encode('utf-8', "ignore")
            iter_text = re_cut(iter_text)
            text_list.append(iter_text)
    if text_list:
        for iter_text in text_list:
            cut_text = sw.participle(iter_text)
            cut_word_list = [term for term, cx in cut_text if cx in cx_dict]
            tmp_list = []
            for w in cut_word_list:
                if word_dict.has_key(w):
                    word_dict[w] += 1
                else:
                    word_dict[w] = 1

    return word_dict


# 搜索之前30天内某个关键词的走势图
def get_keyword_trend(keyword, ts, interval):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                   "gte": ts - interval,
                                   "lt": ts
                                }
                            }},
                            {"term":{"keywords_string":keyword}}
                        ]
                    }
                }
            }
        }
    }

    datetime = ts2datetime(ts - interval)
    index_name = "flow_text_" + datetime
    exist_es = es_flow_text.indices.exists(index=index_name)
    if exist_es:
        label = 1
        count = es_flow_text.count(index=index_name, doc_type="text", body=query_body)['count']
        print count
    else:
        label = 0
        count = 0
    return count, label

# 返回同一时间上的微博走势图
def count_trend(ts, keyword):
    history_list = []
    count = 0
    while 1:
        allcount, label = get_keyword_trend(keyword, ts, interval)
        if label:
            history_list.append(allcount)
            count += 1
            ts = ts - 2*3600
        else:
            break
    return history_list


# 同一时间点上的微博数走势图，检测当前与历史的区别
def detect_burst(history_list):
    current_count = history_list.pop(0)
    lenth = len(history_list)
    print lenth
    mean = np.mean(history_list)
    var = np.std(history_list)
    if current_count >= mean + 1.96*var:
        return 1
    else:
        return 0




if __name__ == "__main__":
    ts = datetime2ts("2013-09-08")
    trend_list = count_trend(ts, "车祸")
    print detect_burst(trend_list)
