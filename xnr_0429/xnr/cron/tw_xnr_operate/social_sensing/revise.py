# -*-coding:utf-8-*-
import time
import re
import json
import math
import numpy as np
from duplicate import duplicate
import operator
from text_classify.test_topic import topic_classfiy
from clustering import freq_word, tfidf, kmeans, text_classify, cluster_evaluation
from elasticsearch.helpers import scan
from elasticsearch import Elasticsearch
import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_flow_text as es_text
#from global_utils import es_user_portrait
es_user_portrait = Elasticsearch("10.128.55.83:9206")
from global_utils import R_SOCIAL_SENSING as r
from time_utils import ts2datetime, datetime2ts, ts2date
from parameter import topic_en2ch_dict

time_interval = 3600
time_range = 24*3600
monitor_index_name = "text_0602"
monitor_index_type = "text"
result_filename = "revise_0602.txt"


#给定微博mid，聚合微博数量
def aggregation_root_weibo_retweet(mid_list,ts):
    size = len(mid_list)
    if size == 0:
        size = 10
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":
                                {"timestamp":{
                                    "gte":ts-time_interval,
                                    "lt":ts
                                }}
                            },
                            {"terms":{"root_mid":mid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_count":{
                "terms":{"field":"root_mid", "size":size},
                "aggs":{
                    "message_type":{
                        "terms":{
                            "field":"message_type"
                        }
                    }
                }
            }
        }
    }

    datetime = ts2datetime(ts-time_interval)
    index_name = "flow_text_"+datetime

    results = es_text.search(index=index_name, doc_type="text", body=query_body)['aggregations']['all_count']['buckets']
    return_results = dict()
    if results:
        for item in results:
            temp_dict = dict()
            temp_dict[item['key']] = item['doc_count']
            detail = item['message_type']['buckets']
            detail_dict = dict()
            for iter_item in detail:
                detail_dict[iter_item['key']] = iter_item['doc_count']
            temp_dict['retweeted'] = detail_dict.get(3, 0)
            temp_dict['comment'] = detail_dict.get(2, 0)
            return_results[item['key']] = temp_dict['retweeted']
    be_retweetd_list = return_results.keys()
    no_retweeted = set(mid_list) - set(be_retweetd_list)
    for mid in no_retweeted:
        return_results[mid] = 0
    return return_results


#给定用户uid，查找感知微博
def search_sensored_weibo(uid_list, ts):
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must":[
                            {"range": {
                                "timestamp": {
                                    "gte": ts-time_interval,
                                    "lt":ts
                                }
                            }},
                            {"terms":{"uid": uid_list}}
                        ]
                    }
                }
            }
        },
        "size":200000
    }
    mid_set = set()
    index_name = "flow_text_" + ts2datetime(ts-time_interval)
    results = es_text.search(index=index_name, doc_type="text", body=query_body)["hits"]["hits"]
    for item in results:
        if item["_source"]["message_type"] == 1:
            mid_set.add(item['_source']["mid"])
        else:
            try:
                mid_set.add(item['_source']["root_mid"])
            except Exception, r:
                print Exception, r
    print len(mid_set)

    # 获得原创微博和转发微博信息存入es中，应当在近两天里
    index_list = []
    index_list.append(index_name)
    index_list.append("flow_text_"+ts2datetime(ts-3600*24))
    mid_list = list(mid_set)
    bulk_action = []
    non_exist_list = [] #尚未监控的微博
    exist_results = es_user_portrait.mget(index=monitor_index_name, doc_type=monitor_index_type, body={"ids":mid_list})["docs"]
    for item in exist_results:
        if not item["found"]:
            non_exist_list.append(item["_id"])
    
    #将尚未监控的微博纳入监控的范围内
    if non_exist_list:
        count = 0
        classify_text_dict = dict() # 分类文本
        classify_uid_list = []
        #f = open("text.txt", "a")
        lenth = len(non_exist_list)
        dividion = lenth/1000
        weibo_results = []
        for i in range(0,dividion+1):
            tmp_mid_list = non_exist_list[i*1000:(i+1)*1000]
            tmp_weibo_results = es_text.search(index=index_list, doc_type="text", body={"query":{"bool":{"must":[{"terms":{"mid":tmp_mid_list}}]}}, "size":100000})["hits"]["hits"]
            weibo_results.extend(tmp_weibo_results)
        for item in weibo_results:
            iter_uid = item['_source']['uid']
            iter_mid = item['_source']['mid']
            iter_text = item['_source']['text'].encode('utf-8', 'ignore')
            #f.write(str(iter_text)+"\n")
            keywords_dict = json.loads(item['_source']['keywords_dict'])
            personal_keywords_dict = dict()
            for k, v in keywords_dict.iteritems():
                k = k.encode('utf-8', 'ignore')
                personal_keywords_dict[k] = v
            classify_text_dict[iter_mid] = personal_keywords_dict
            classify_uid_list.append(iter_uid)
        #f.close()

        if classify_text_dict:
            classify_results = topic_classfiy(classify_uid_list, classify_text_dict)
            mid_value = dict()
            #print "classify_results: ", classify_results
            for k,v in classify_results.iteritems(): # mid:category
                mid_value[k] = v[0] 


        for item in weibo_results:
            action = {"index":{"_id":item['_id']}}
            item['_source']['category'] = mid_value[item['_id']]
            bulk_action.extend([action, item["_source"]])
            count += 1
            if count % 1000 == 0:
                es_user_portrait.bulk(bulk_action, index=monitor_index_name, doc_type=monitor_index_type, timeout=600)
                bulk_action = []
        if bulk_action:
            es_user_portrait.bulk(bulk_action, index=monitor_index_name, doc_type=monitor_index_type, timeout=600)
        

    return 1


# 获得各个类别里的微博列表，更新其转发量
def update_category_retweet_number(ts):
    topic_list = topic_en2ch_dict.keys()
    for topic in topic_list:
        s_re = scan(es_user_portrait, query={"query":{"term":{"category":topic}},"size":1000}, index=monitor_index_name, doc_type=monitor_index_type)
        count = 0
        mid_list = []
        bulk_action = []
        all_scan_re = dict()
        #f = open("%s_text.txt" %topic, "a")
        while 1:
            try:
                tmp = s_re.next()
                scan_re = tmp['_source']
                #total_retweet = scan_re.get("sum_retweet", 0)
                mid = scan_re['mid']
                mid_list.append(mid)
                #f.write(scan_re['text'].encode('utf-8','ignore') +"\n")
                count +=1
                all_scan_re[mid] = scan_re
                if count % 100 == 0:
                    retweet_dict = aggregation_root_weibo_retweet(mid_list,ts)
                    for iter_mid in mid_list:
                        update_dict = {"index":{"_id":iter_mid}}
                        scan_re = all_scan_re[iter_mid]
                        total_retweet = scan_re.get("sum_retweet", 0)
                        total_retweet += retweet_dict[iter_mid]
                        scan_re["ts-"+str(ts)] = retweet_dict[iter_mid]
                        scan_re["sum_retweet"] = total_retweet
                        bulk_action.extend([update_dict, scan_re])
                    es_user_portrait.bulk(bulk_action,index=monitor_index_name, doc_type=monitor_index_type, timeout=600)
                    bulk_action = []
                    mid_list = []
                    all_scan_re = dict()
            except StopIteration:
                print topic, " iter once"
                break
        if bulk_action:
            es_user_portrait.bulk(bulk_action,index=monitor_index_name, doc_type=monitor_index_type, timeout=600)

    #f.close()
    return 1




#同一类别微博聚类
def cluster_same_topic(ts):
    # output: list [[mid, mid, mid]]
    # 1. 获取同一类别的微博
    topic_list = topic_en2ch_dict.keys()
    print topic_list
    topic_list.remove('life')
    topic_list.remove('art')
    #for topic in topic_list:
    if 1:
        s_re = scan(es_user_portrait, query={"query":{"terms":{"category":topic_list}},"size":1000}, index=monitor_index_name, doc_type=monitor_index_type)
        text_list = []
        topic_mid_list = []
        while 1:
            try:
                tmp = s_re.next()
                scan_re = tmp['_source']
                detection_type = scan_re.get("detection", 0)
                if int(detection_type) == 1:
                    continue
                mid = scan_re['mid']
                text = scan_re['text']
                temp_dict = dict()
                #temp_dict["mid"] = mid
                #temp_dict["text"] = text
                #text_list.append(temp_dict)
                temp_dict['_id'] = mid
                temp_dict['content'] = re.sub(r'http://\S+', '', text)
                temp_dict['title'] = ""
                text_list.append(temp_dict)
            except StopIteration:
                #print topic, "iter once and begin cluster"
                if len(text_list) == 1:
                    #top_word = freq_word(text_list[0])
                    #topic_list = [top_word.keys()]
                    topic_mid_list.append(text_list[0])
                elif len(text_list) == 0:
                    topic_list = []
                    #print "no relate weibo text"
                else:
                    results = duplicate(text_list)
                    dup_results = dict()
                    for item in results:
                        if item['duplicate']:
                            dup_list = dup_results[item['same_from']]
                            dup_list.append(item["_id"])
                            dup_results[item['same_from']] = dup_list
                        else:
                            dup_results[item['_id']] = [item['_id']]
                    topic_mid_list.extend(dup_results.values())

                break
    return topic_mid_list            

#根据某个类别里的mid list判断爆发性事件
def bursty_event_detection(ts,mid_list):
    #print mid_list
    results = es_user_portrait.mget(index=monitor_index_name, doc_type=monitor_index_type, body={"ids":mid_list})["docs"]
    if len(mid_list) >=3:
        print results
        with open(result_filename, 'a') as f:
            for item in results:
                item = item['_source']
                mid = item['mid']
                f.write(str(ts2date(ts))+str(ts2date(item['timestamp']))+str(item['uid'])+item["text"].encode("utf-8", "ignore")+"\n")
                item['detection'] = 1
                es_user_portrait.index(index=monitor_index_name, doc_type=monitor_index_type,id=item['mid'], body=item)
    

    time_series = dict()
    for item in results:
        for k,v in item['_source'].iteritems():
            if "ts-" in k:
                k = k.split('-')[1]
                if int(k) in time_series:
                    time_series[int(k)] += v 
                else:
                    time_series[int(k)] = v
    sorted_result = sorted(time_series.items(), key=lambda x:x[0], reverse=False)
    if len(sorted_result) > 4 and len(mid_list) >=2:
        timestamp = sorted_result[-1][0]
        retweet_number = sorted_result[-1][1]
        average_list = [item[1] for item in sorted_result[:-1]]
        average = np.mean(average_list)
        std = np.std(average_list)
        former_three = sum(average_list[-4:-1])
        #print average_list, retweet_number
        #if retweet_number > average + 1.96*std:
        if retweet_number > former_three:
            print sorted_result
            print "detect burst event"
            print "timestamp: ", timestamp
            print "weibo list: ", mid_list
            #取按时间排序的top2
            text_list = []
            for item in results:
                text_list.append(item['_source'])
            #sorted_by_ts = sorted(text_list, key=operator.itemgetter("timestamp"), reverse=False)
            #print "最早的两个微博:", sorted_by_ts[:2]
            #sorted_by_retweet = sorted(text_list, key=operator.itemgetter("sum_retweet"), reverse=True)
            #print sorted_by_retweet[:2]
            #mining_results = []
            #mining_results.extend(sorted_by_ts[:2])
            #mining_results.extend(sorted_by_retweet[:2])
            with open(result_filename, "a") as f:
                for item in text_list:
                    mid = item['mid']
                    item['detection'] = 1
                    es_user_portrait.index(index=monitor_index_name, doc_type=monitor_index_type,id=item['mid'], body=item)
                    f.write(str(ts2date(ts))+str(ts2date(item['timestamp']))+str(item['uid'])+item["text"].encode('utf-8', 'ignore')+"\n")

        else:
            results = []

    return results

    

if __name__ == "__main__":
    uid_set = set()
    #1.读取social sensors
    with open("group.txt", "rb") as f:
        for line in f:
            uid = line.strip()
            uid_set.add(uid)
    uid_list = list(uid_set)
    #2.读取social sensors的微博列表
    for i in range(0,30):
    #if 1:
        ts = 1464710400 +i*3600
        mid_list = search_sensored_weibo(uid_list, ts)
        #print aggregation_root_weibo_retweet(mid_list, ts)
        #3. 更新微博转发量
        update_category_retweet_number(ts)
        #4. 聚类相同领域的微博，返回微博列表
        
        topic_weibo_list = cluster_same_topic(ts)
        if topic_weibo_list:
            for iter_mid_list in topic_weibo_list:
                bursty_event_detection(ts,iter_mid_list)
        

