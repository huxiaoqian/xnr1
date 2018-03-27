# -*- coding: utf-8 -*-

import os
import re
import sys
import opencc
import csv
import time
import json
import random
import sets
import math
from collections import Counter
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from word_cut import word_net
from text_classify import text_net,get_s
from config import TopkHeap,index_list,K1,B,K3,es_flow_text,flow_text_index_type,\
                     cut_by_textrank,MAX_SIZE,OPINION_CLUSTER,summary_text

def get_related_score(text,keywords,keyword_count,avr_n,total_n):#获取文本的分数

    len_t = len(text)
    score = 0
    for key in keywords:
        if key not in text:
            continue
        p1 = math.log(float(total_n-keyword_count[key]+0.5)/float(keyword_count[key]+0.5))
        p2 = float((K1+1)*text.count(key))/float(K1*(1-B)+B*len_t/float(avr_n)+text.count(key))
        p3 = float((K3+1)*1)/float(K3+1)
        score = score+p1*p2*p3

    return score

def rank_text_list(text_list,keywords,keyword_count,avr_n,word_dict):#对text文本排序

    total_n = len(text_list)
    n = int(total_n*0.5)
    if n < 1:
        n = 1
    result_list = TopkHeap(n)
    for i in range(0,len(text_list)):
        text = text_list[i]
        word = word_dict[i]
        score = get_related_score(text,keywords,keyword_count,avr_n,total_n)
        result_list.Push((score,text,word))

    result = result_list.TopK()

    return result

def get_text_by_id(uidlist):#根据uid列表获取对应的文本
    
    keywords_list = []
    for key in uidlist:
        keywords_list.append({'term':{'uid':key}})

    query_body = {'query':{'bool':{'should':keywords_list}},'size':MAX_SIZE}

    result = es_flow_text.search(index=index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    text_list = []
    for i in range(0,len(result)):
        source = result[i]['_source']
        text = source['text'].encode('utf-8')
        text_list.append(text)

    return text_list

def get_text_word_by_id(uidlist):#根据uid列表获取对应的文本

    keywords_list = []
    for key in uidlist:
        keywords_list.append({'term':{'uid':key}})

    query_body = {'query':{'bool':{'should':keywords_list}},'size':MAX_SIZE}
    
    result = es_flow_text.search(index=index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    text_list = []
    word_list = []
    for i in range(0,len(result)):
        source = result[i]['_source']
        text = source['text'].encode('utf-8')
        keywords_string = cut_by_textrank(text)#source['keywords_string'].encode('utf-8').split('&')
        text_list.append(text)
        word_list.append(keywords_string)

    return text_list,word_list

def get_text_by_BM(text_list,word_dict,keywords):#根据BM检索对应的文本

    if len(text_list) == 0:
        return []

    keyword_count = dict()
    related_text = []
    total_n = 0
    for text in text_list:
        flag = 0
        for key in keywords:
            if key in text:
                try:
                    keyword_count[key] = keyword_count[key] + 1
                except KeyError:
                    keyword_count[key] = 1
                flag = flag + 1
        if flag > 0:#表明没有加过长度
            related_text.append(text)
            total_n = total_n + len(text)

    avr_n = total_n/float(len(text_list))

    rank_text = rank_text_list(text_list,keywords,keyword_count,avr_n,word_dict)

    result = []
    word_result = []
    for i in range(len(rank_text)):
        if rank_text[i][1] not in result:
            result.append(rank_text[i][1])
            word_result.append(rank_text[i][2])

    return result,word_result

def search_weibo_from_word(uidlist,keywords):#第四种策略：先根据BM25检索文本，然后再根据关键词的交集筛选文本
    '''
        输入数据：
        uidlist：uid列表
        keywords：keywords列表，热点新闻切词之后的结果

        输出数据：
        text_list：筛选之后的微博文本
    '''
    text_list,word_set = get_text_word_by_id(uidlist)#根据uid列表获取对应的文本和分词之后的结果

    text_set,word_dict = get_text_by_BM(text_list,word_set,keywords)
    
    n = int(0.5*len(text_set))
    if n < 1:
        n = 1
    result_list = TopkHeap(n)

    w_n = int(0.5*len(keywords))
    if w_n < 1:
        w_n = 1

    for i in range(0,len(word_dict)):
        words = word_dict[i]
        len_n = len(set(words)&set(keywords))
        if len_n >= w_n:
            result_list.Push((len_n,text_set[i]))

    result = result_list.TopK()
    text_list = []
    for i in range(0,len(result)):
        if result[i][1] not in text_list:
            text_list.append(result[i][1])
    
    if len(text_list) >= 10:
        word_result,word_weight = word_net(text_list,OPINION_CLUSTER)
        text_list = text_net(word_result,word_weight,text_list)
        result = []
        for text in text_list:
            s = summary_text(text)
            max_r,n = get_s(result,s)
            if max_r >= 0.5:
                continue
            else:
                result.append(s)
    else:
        result = [summary_text(text_list)]

    return result

def follower_analysis(uidlist,text):#关注id讨论内容的分析
    '''
        输入数据：
        uid_list：uid列表，xnr关注的用户列表
        text：热点微博文本

        输出数据：
        summary_list：子观点列表，每个元素表示一个子观点的摘要
    '''
    if len(uidlist) == 0 or len(text) == 0:
        return []
    
    keywords = cut_by_textrank(text)

    summary_list = search_weibo_from_word(uidlist,keywords)

    return summary_list

if __name__ == '__main__':

    f_list = get_followers(['WXNR0004'])
    k_list = load_text_from_csv()
    for i in range(len(k_list)):
        k = k_list[i]
        #keywords = cut_by_textrank(k)

        start = time.time()
        print 'word starts...'
        text_list = follower_analysis(f_list,k)
        write_csv(text_list,'word_'+str(i))
        end = time.time()
        print 'word takes %s second...' % (end-start)
