#-*- coding: UTF-8 -*-

import os
import sys
import time
import csv
import heapq
import random
from decimal import *
from config import DOMAIN_DICT, DOMAIN_COUNT, LEN_DICT, TOTAL, name_list, TOPIC_DICT
from topic_input import input_data #测试输入

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


    print 'com_p'
    p = 0
    test_word = set(word_list.keys())


    test_word_encode = []
    for word in test_word :
        test_word_encode.append(word.encode('utf8'))
    test_word_encode = set(test_word_encode)

    train_word = set(domain_dict.keys())
    # print 'test_word'
    # print test_word
    # print 'train_word'
    # print train_word
    # c_set = test_word & train_word
    c_set = test_word_encode & train_word
    print 'c_set'
    print c_set
    for k in c_set:
        print 'domain_dict[k]'
        print domain_dict[k]
        print 'word_list[k]'
        print word_list[k]
    print 'domain_count'
    print domain_count
    p = sum([float(domain_dict[k])*float(word_list[k])/float(domain_count) for k in c_set])
    return p

def load_weibo(uid_weibo):
    print 'load_weibo'
    print 'uid_weibo'
    print uid_weibo
    result_data = dict()
    p_data = dict()
    for k,v in uid_weibo.iteritems():
        domain_p = TOPIC_DICT
        for d_k in domain_p.keys():
            domain_p[d_k] = com_p(v,DOMAIN_DICT[d_k],DOMAIN_COUNT[d_k],LEN_DICT[d_k],TOTAL)#计算文档属于每一个类的概率
            print 'd_k'
            print d_k
            print 'domain_p[d_k]'
            print domain_p[d_k]
            end_time = time.time()        
        
        result_data[k] = domain_p
        p_data[k] = rank_result(domain_p)
        print 'result_data[k]'
        print result_data[k]
        print 'p_data[k]'
        print p_data[k]

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
            print 'AAA'
            result_data[uid] = TOPIC_DICT
            uid_topic[uid] = ['life']
        return result_data,uid_topic
    elif len(uid_weibo) and not len(uid_list):
        print 'BBB'
        uid_list = uid_weibo.keys()
    elif not len(uid_weibo) and not len(uid_list):
        print 'CCC'
        result_data = dict()
        uid_topic = dict()
        return result_data,uid_topic
    else:
        print 'DDD'
        pass        
        
    result_data,uid_topic = load_weibo(uid_weibo)#话题分类主函数

    for uid in uid_list:
        if not result_data.has_key(uid):
            result_data[uid] = TOPIC_DICT
            uid_topic[uid] = ['life']
    
    return result_data,uid_topic


if __name__ == '__main__':

    # uid_list, uid_weibo, topic_dict = input_data('TID')
    
    # my_uid_list = uid_list[:3]
    # my_uid_weibo = {}
    # for uid in my_uid_list:
    #     my_uid_weibo[uid] = uid_weibo[uid]
    # my_topic_dict = {}
    # for uid in my_uid_list:
    #     my_topic_dict[uid] = topic_dict[uid]

    # print 'my_uid_list: ', my_uid_list
    # print 'my_uid_weibo: ', my_uid_weibo
    # print 'my_topic_dict: ', my_topic_dict
    # result_data,uid_topic = topic_classfiy(my_uid_list, my_uid_weibo)
    # print result_data
    # print uid_topic
    '''
    data = {
      u'139819436047050': {
        'life': 0.00010221216734826073,
        'law': 0.00013977955349282154,
        'computer': 5.963407179718062e-05,
        'house': 0.00011238687826906112,
        'peace': 0.0003407565081419985,
        'politics': 0.00032407369571857723,
        'fear-of-violence': 0.00019908614960790797,
        'sports': 0.0002958251099946697,
        'environment': 0.00021867854540642237,
        'religion': 0.00036401730198506755,
        'economic': 0.0003282436405055251,
        'traffic': 6.668831341206706e-05,
        'anti-corruption': 0.00016871189195860555,
        'military': 0.00011692240504074539,
        'medicine': 8.21364955405293e-05,
        'art': 0.0002306790798914899,
        'education': 0.00014142385613232555,
        'employment': 9.450582849864567e-05,
        'social-security': 8.829319602489132e-05
      },
      u'716502715155445': {
        'life': 0.00010221216734826073,
        'law': 0.00013977955349282154,
        'computer': 5.963407179718062e-05,
        'house': 0.00011238687826906112,
        'peace': 0.0003407565081419985,
        'politics': 0.00032407369571857723,
        'fear-of-violence': 0.00019908614960790797,
        'sports': 0.0002958251099946697,
        'environment': 0.00021867854540642237,
        'religion': 0.00036401730198506755,
        'economic': 0.0003282436405055251,
        'traffic': 6.668831341206706e-05,
        'anti-corruption': 0.00016871189195860555,
        'military': 0.00011692240504074539,
        'medicine': 8.21364955405293e-05,
        'art': 0.0002306790798914899,
        'education': 0.00014142385613232555,
        'employment': 9.450582849864567e-05,
        'social-security': 8.829319602489132e-05
      }
    }    
    for uid, d in data.items():
        print uid
        print rank_result(d)
    '''
    from elasticsearch import Elasticsearch
    import json
    ES_CLUSTER_HOST = ['219.224.134.213:9205', '219.224.134.214:9205',\
                       '219.224.134.215:9205']

    es_translation = Elasticsearch(ES_CLUSTER_HOST, timeout=600)
    index_name = 'fb_user_portrait'
    index_type = 'user'
    ids = ['544481513', '100010212181419']

    uid_list = []
    uid_weibo = {}
    res = es_translation.mget(index=index_name, doc_type=index_type, body={'ids': ids})['docs']
    for r in res:
        uid = r['_id']
        keywords = json.loads(r['_source']['filter_keywords'])
        uid_list.append(uid)
        uid_weibo[uid] = keywords
    print uid_weibo
    result_data,uid_topic = topic_classfiy(uid_list, uid_weibo)
    print result_data
    print uid_topic














    '''
    with open('./result/user_topic_t.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in uid_topic.iteritems():
            writer.writerow((k,'&'.join(v),'.'.join(topic_dict[k])))
    f.close()

    with open('./result/user_text_t.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in topic_dict.iteritems():
            for item in v:
                writer.writerow((k,item))
    f.close()

    uid_list,uid_weibo,topic_dict = input_data('FID')
    result_data,uid_topic = topic_classfiy(uid_list,uid_weibo)
    
    with open('./result/user_topic_f.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in uid_topic.iteritems():
            writer.writerow((k,'&'.join(v),'.'.join(topic_dict[k])))
    f.close()

    with open('./result/user_text_f.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in topic_dict.iteritems():
            for item in v:
                writer.writerow((k,item))
    f.close()
    '''






        
