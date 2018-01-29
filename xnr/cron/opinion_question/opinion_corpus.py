# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import time
import json
import random
import sets
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import heapq
from collections import Counter
from config import cut_filter

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

##以下是es的配置文件
user_profile_host = ["219.224.134.216:9201"]
es_user_profile = Elasticsearch(user_profile_host, timeout=600)
profile_index_name = "weibo_user"
profile_index_type = "user"
portrat_index_name = "user_portrait_1222"
portrat_index_type = "user"
flow_text_host = ["219.224.134.216:9201"]
es_text = Elasticsearch(flow_text_host, timeout=600)
flow_text_index_name_pre = 'flow_text_' # flow text: 'flow_text_2013-09-01'
flow_text_index_type = 'text'
time_list = ['2016-11-11','2016-11-12','2016-11-13','2016-11-14','2016-11-15','2016-11-16',\
             '2016-11-17','2016-11-18','2016-11-19','2016-11-20','2016-11-21','2016-11-22','2016-11-23','2016-11-24','2016-11-25','2016-11-26',\
             '2016-11-27']   

def get_weibo_text(key_list,name):

    if len(key_list) == 0:
        return -1
    keywords_list = []
    for key in key_list:
        keywords_list.append({'wildcard':{'text':'*'+key+'*'}})
    
    query_body = {'query':{'bool':{'should':keywords_list,'minimum_should_match':1}}}

    for t_name in time_list:
        print t_name
        index_list = flow_text_index_name_pre+t_name
        s_re = scan(es_text,index=index_list,doc_type=flow_text_index_type,query=query_body)#{'query':{'match_all':{}}})
        text_result = []
        count = 0
        while True:
            try:
                scan_re = s_re.next()
                source = scan_re['_source']
                count += 1
                if count % 1000 == 0:
                    print count
                mid = source['mid']
                uid = source['uid']
                text = source['text'].encode('utf-8')
                m_type = source["message_type"]
                if text.find('//') == 0:
                    continue
                if m_type == 3:
                    text_set = process_text(text)
                    text_result.extend(text_set)
            
            except StopIteration:
                print "all done"
                break

        with open('./text_data/opinion/text_%s_%s.csv' % (name,t_name), 'wb') as f:
            writer = csv.writer(f)
            for i in range(0,len(text_result)):
                writer.writerow(text_result[i])

        f.close()

    return 1

def process_text(text):#处理文本

    text_result = []
    if '//' in text:
        text_list = text.split('//@')
    elif '/' in text:
        text_list = text.split('/@')
    else:
        text_list = [text]

    for t in text_list:
        t_new = t.replace(' ', '')
        t_new = t_new.replace('\r','')
        if t_new:
            t_str = cut_filter(t_new)
            t_s = t_str.replace(' ', '')
            t_s = t_s.replace('\r', '')
        else:
            continue
        if len(t_s) >= 4 and t_s not in text_result:
            text_result.append(t_s)
        else:
            continue

    return text_result

if __name__ == '__main__':

    get_weibo_text(['民主'],'minzhu')
