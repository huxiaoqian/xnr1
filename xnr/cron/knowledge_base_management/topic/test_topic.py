#-*- coding: UTF-8 -*-

import os
import sys
import time
import csv
import heapq
import random
from decimal import *
from config import abs_path,DOMAIN_DICT,DOMAIN_COUNT,LEN_DICT,TOTAL,name_list,TOPIC_DICT
#from test_data import input_data #测试输入

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

def com_p(word_list,domain_dict,domain_count,len_dict,total):

    p = 0
    test_word = set(word_list.keys())
    train_word = set(domain_dict.keys())
    c_set = test_word & train_word
    p = sum([float(domain_dict[k]*word_list[k])/float(domain_count) for k in c_set])

    return p

def load_weibo(uid_weibo):

    result_data = dict()
    p_data = dict()
    for k,v in uid_weibo.iteritems():
        domain_p = TOPIC_DICT
        for d_k in domain_p.keys():
            domain_p[d_k] = com_p(v,DOMAIN_DICT[d_k],DOMAIN_COUNT[d_k],LEN_DICT[d_k],TOTAL)#计算文档属于每一个类的概率
            end_time = time.time()
        result_data[k] = domain_p
        p_data[k] = rank_result(domain_p)

    return result_data,p_data

def rank_dict(has_word):

    n = len(has_word)
    keyword = TopkHeap(n)
    count = 0
    for k,v in has_word.iteritems():
        keyword.Push((v,k))
        count = count + v

    keyword_data = keyword.TopK()
    return keyword_data,count    

def rank_result(domain_p):
    
    data_v,count = rank_dict(domain_p)
    if count == 0:
        uid_topic = ['life']
    else:
        uid_topic = [data_v[0][1],data_v[1][1],data_v[2][1]]

    return uid_topic

def topic_classfiy(uid_list,uid_weibo):#话题分类主函数
    '''
    用户话题分类主函数
    输入数据示例：
    uidlist:uid列表（[uid1,uid2,uid3,...]）
    uid_weibo:分词之后的词频字典（{uid1:{'key1':f1,'key2':f2...}...}）

    输出数据示例：字典
    用户18个话题的分布：
    {uid1:{'art':0.1,'social':0.2...}...}
    用户关注较多的话题（最多有3个）：
    {uid1:['art','social','media']...}
    '''
    if not len(uid_weibo) and len(uid_list):
        result_data = dict()
        uid_topic = dict()
        for uid in uid_list:
            result_data[uid] = TOPIC_DICT
            uid_topic[uid] = ['life']
        return result_data,uid_topic
    elif len(uid_weibo) and not len(uid_list):
        uid_list = uid_weibo.keys()
    elif not len(uid_weibo) and not len(uid_list):
        result_data = dict()
        uid_topic = dict()
        return result_data,uid_topic
    else:
        pass        
        
    result_data,uid_topic = load_weibo(uid_weibo)#话题分类主函数

    for uid in uid_list:
        if not result_data.has_key(uid):
            result_data[uid] = TOPIC_DICT
            uid_topic[uid] = ['life']
    
    return result_data,uid_topic


if __name__ == '__main__':

    uid_list,uid_weibo = input_data()
    uid_weibo = dict()
    result_data,uid_topic = topic_classfiy(uid_list,uid_weibo)
    print result_data
    print uid_topic







        
