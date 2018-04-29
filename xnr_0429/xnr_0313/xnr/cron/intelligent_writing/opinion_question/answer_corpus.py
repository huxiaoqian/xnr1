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
from global_config import cut_filter

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
time_list = ['2016-11-15','2016-11-16',\
             '2016-11-17','2016-11-18','2016-11-19','2016-11-20','2016-11-21','2016-11-22','2016-11-23','2016-11-24','2016-11-25','2016-11-26',\
             '2016-11-27']

def cut_flow_text(text):#对流文本切分评论

    text_result = dict()
    text = cut_filter(text)
    if '//@' in text:
        texts = text.split('//@')
    elif '/@' in text:#表示有评论
        texts = text.split('/@')
    else:
        return 0,0

    text_list = []
    for i in range(0,len(texts)):
        text_str = texts[i].strip()
        if not len(text_str):#空文本
            continue
        if i == 0:
            text_list.append(text_str)
        else:
            if ':' in text_str:
                s_list = text_str.split(':')
                s_content = s_list[-1]
                if len(s_content):
                    text_list.append(s_content)
            else:
                text_list.append(text_str)
    try:
        key = text_list[-1]
    except IndexError:
        return 0,0
    if len(key) < 2:
        return 0,0
    
    return key,text_list[0:len(text_list)-1]

def get_weibo_text_bymessagetype(key_list,name):#根据敏感词获取微博文本

    if len(key_list) == 0:
        return -1

    keywords_list = []
    for key in key_list:
        keywords_list.append({'term':{'message_type':key}})
    keywords_list.append({'range':{'sensitive':{'from':1}}})

    query_body = {'query':{'bool':{'should':keywords_list}}}
    
    for t_name in time_list:
        print t_name
        index_list = flow_text_index_name_pre+t_name
        s_re = scan(es_text,index=index_list,doc_type=flow_text_index_type,query=query_body)#{'query':{'match_all':{}}})
        text_result = dict()
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
                if m_type != 2 and m_type != 3:
                    continue
                key,value = cut_flow_text(text)
                if key == 0:
                    continue
                try:#有该问题
                    item = text_result[key]
                    item.extend(value)
                    text_result[key] = item
                except KeyError:
                    text_result[key] = value
            
            except:
                print "all done"
                break

        with open('./text_data/answer/text_%s_%s.csv' % (name,t_name), 'wb') as f:
            writer = csv.writer(f)
            for k,v in text_result.iteritems():
                for item in v:
                    writer.writerow((k,item))

        f.close()

    return 0

if __name__ == '__main__':

    get_weibo_text_bymessagetype(['2','3'],'lawyer')
