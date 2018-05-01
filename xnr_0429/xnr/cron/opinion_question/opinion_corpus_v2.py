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
from config import cut_filter,global_utils_route
sys.path.append(global_utils_route)
from global_utils import all_opinion_corpus_index_name_test,all_opinion_corpus_index_name,all_opinion_corpus_index_type,es_xnr
from global_utils import es_flow_text as es_text,es_user_profile,profile_index_name,profile_index_type,portrait_index_name as portrat_index_name,\
                         portrait_index_type as portrat_index_type,flow_text_index_name_pre,flow_text_index_type
from global_config import S_TYPE
from parameter import DAY
from time_utils import ts2datetime,datetime2ts
##以下是es的配置文件
if S_TYPE == 'test':
    time_list = ['2016-11-18']
else:
    time_list = []
    start_time = int(time.time())
    for i in range(0,7):
        start_date = ts2datetime(start_time - i*DAY)
        time_list.append(start_date)



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




def save_user_results(bulk_action):
    print es_xnr.bulk(bulk_action, index=all_opinion_corpus_index_name_test, doc_type=all_opinion_corpus_index_type, timeout=600)
    return 'True'

def save_data(data,label):

    bulk_action = []
    count_dict = dict()
    for d in data:
        result = dict()
        mid = d[1]
        result['mid'] = d[1]
        result['label'] = label
        result['text'] = d[0]
        result['timestamp'] = d[2]
        try:
            count_dict[mid] = count_dict[mid] + 1            
        except KeyError:
            count_dict[mid] = 1
        flag = count_dict[mid] 
        action = {'index':{'_id': mid+'_'+str(flag)}}
        bulk_action.extend([action, result])

    status = save_user_results(bulk_action)

    return status

def rank_text(text_result,data_result,key_list):

    total_n = len(text_result)
    n = int(total_n*0.7)
    result_list = TopkHeap(n)

    for i in range(0,len(text_result)):
        c = 0
        f = 0
        text = text_result[i]
        mid = data_result[i][0]
        timestamp = data_result[i][1]
        for k in key_list:
            if k in text:
                c = c + text.count(k)
                f = f + 1
        result_list.Push((c*f,text,mid,timestamp))

    result = result_list.TopK()
    new_text = []
    for r in result:
        new_text.append([r[1],r[2],r[3]])

    return new_text

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
        data_result = []
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
                timestamp = source['timestamp']
                m_type = source["message_type"]
                if text.find('//') == 0:
                    continue
                if m_type == 3:
                    text_set,data_list = process_text(text,mid,timestamp,text_result)
                    text_result.extend(text_set)
                    data_result.extend(data_list)

            except StopIteration:
                print "all done"
                break

        result_list = rank_text(text_result,data_result,key_list)#对结果进行排序
        # with open('./text_data/opinion/text_%s_%s.csv' % (name,t_name), 'wb') as f:
        # # with open('./corpus/text_%s.csv' % name, 'wb') as f:
        #     writer = csv.writer(f)
        #     for i in range(0,len(text_result)):
        #         writer.writerow(text_result[i])

        status = save_data(result_list,name)#将数据存入es

    return status

def process_text(text,mid,timestamp,total_result):#处理文本

    text_result = []
    data_list = []
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
        if len(t_s) >= 4 and t_s not in text_result and t_s not in total_result:
            text_result.append(t_s)
            data_list.append([mid,timestamp])
        else:
            continue

    return text_result,data_list

def load_csv(name):

    text_list = []
    timestamp = time.time()
    reader = csv.reader(file('./corpus/text_%s.csv' % name, 'rb'))
    count = 0
    for line in reader:
        if count == 0:
            text = line[0].strip('\xef\xbb\xbf')
        else:
            text = line[0]
        count = count + 1
        if text not in text_list:
            text_list.append([text,'20000000000000000',timestamp])
    
    status = save_data(text_list,name)

    print name,status

if __name__ == '__main__':

    status = get_weibo_text(['民主'],'test')
    print status
    #load_csv('weiquan')
