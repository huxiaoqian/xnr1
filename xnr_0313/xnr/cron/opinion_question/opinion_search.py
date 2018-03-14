# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import time
import json
import heapq
import math
from config import cut_des,K1,B,K3

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

def load_text_list(file_name):#从文件读取text文本

    text_list = []
    reader = csv.reader(file('./corpus/text_%s.csv' % file_name, 'rb'))
    count = 0
    for line in reader:
        if count == 0:
            text = line[0].strip('\xef\xbb\xbf')
        else:
            text = line[0]
        count = count + 1
        if text not in text_list:
            text_list.append(text)
##        text_set = text.split('。')
##        for t in text_set:
##            if len(t) > 0 and t not in text_list:
##                text_list.append(t)
    
    return text_list        

def get_related_text(keywords,file_name):#通过keywords获取相关的文本

    text_list = load_text_list(file_name)
    keyword_count = dict()
    word_set = []
    related_text = []
    total_n = 0
    for text in text_list:
        flag = 0
        row = []
        for key in keywords:
            if key in text:
                try:
                    keyword_count[key] = keyword_count[key] + 1
                except KeyError:
                    keyword_count[key] = 1
                row.append(key)
                flag = flag + 1        
        if flag > 0:#表明没有加过长度
            word_set.append(row)
            related_text.append(text)
            total_n = total_n + len(text)

    avr_n = total_n/float(len(text_list))
    return related_text,keyword_count,avr_n,word_set

def get_related_score(text,keywords,keyword_count,avr_n,total_n):#获取文本的分数

    len_t = len(text)
    score = 0
    for key in keywords:
        if key not in text:
            continue
        p1 = math.log(float(total_n-keyword_count[key]+0.5)/float(keyword_count[key]+0.5))
        #p2 = float((k1+1)*text.count(key))/float(k1*(1-b)+text.count(key))
        p2 = float((K1+1)*text.count(key))/float(K1*(1-B)+B*len_t/float(avr_n)+text.count(key))
        p3 = float((K3+1)*1)/float(K3+1)
        score = score+p1*p2*p3

    return score

def rank_text_list(text_list,keywords,keyword_count,avr_n,word_set):#对text文本排序

    total_n = len(text_list)
    n = int(total_n*0.3)
    if n < 1:
        n = 1
    result_list = TopkHeap(n)
    for i in range(0,len(text_list)):
        text = text_list[i]
        score = get_related_score(text,keywords,keyword_count,avr_n,total_n)
        result_list.Push((score,text,word_set[i]))

    rank_text = result_list.TopK()

    return rank_text

def rank_text_list_by_word(text_list,keywords,word_set):#根据关键词匹配的长度，对text文本排序

    total_n = len(text_list)
    n = int(total_n*0.3)
    if n < 1:
        n = 1
    result_list = TopkHeap(n)

    w_n = int(0.5*len(keywords))
    if w_n < 1:
        w_n = 1

    for i in range(0,len(text_list)):
        text = text_list[i]
        words = word_set[i]
        len_n = len(set(words)&set(keywords))
        if len_n >= w_n:
            result_list.Push((len_n,text))

    result = result_list.TopK()
##    text_list = []
##    for i in range(0,len(result)):
##        if result[i][1] not in text_list:
##            text_list.append(result[i][1])

    return result

def combine_rank_text(rank_text):#将排好序的文本拼接成一篇文档

    word_dict = dict()
    flag_dict = dict()
    for i in range(0,len(rank_text)):
        text = rank_text[i][1]
        word_dict[i] = cut_des(text)
        if i == 0:
            flag_dict[i] = 1#表示已经选择过
        else:
            flag_dict[i] = 0#表示还没选择过
    
    summary = rank_text[0][1]#获取相似度最高的文本
    summary_word = word_dict[0]
    count = 0
    while count < 2:#将三个文本拼成一段话
        max_weight = 0
        max_index = 0
        len_sw = len(summary_word)
        w_n = int(0.5*len_sw)
        if w_n < 1:
            w_n = 1
        for i in range(1,len(rank_text)):
            if flag_dict[i] == 1:#已经选择过了
                continue
            text = rank_text[i][1]
            score = rank_text[i][0]
            word_set = word_dict[i]
            union_set = word_set & summary_word
            weight = len(union_set)
            if weight > max_weight and weight >= w_n:
                max_index = i
                max_weight = weight

        if max_weight == 0:#没有可以拼接的文本
            break
        else:
            summary = summary + '\n' +  rank_text[max_index][1]
            summary_word = summary_word | word_dict[max_index]
            flag_dict[max_index] = 1

        count = count + 1

    return summary        

def opinion_relevance(keywords,file_name):#观点检索主函数

    if len(keywords) == 0:
        return ''
    
    text_list,keyword_count,avr_n,word_set = get_related_text(keywords,file_name)#通过keywords获取相关的文本

    rank_text = rank_text_list_by_word(text_list,keywords,word_set)
    #rank_text = rank_text_list(text_list,keywords,keyword_count,avr_n,word_set)#对text文本排序

    if len(rank_text) == 0:
        return ''
    summary_text = combine_rank_text(rank_text)#将排好序的文本拼接成一篇文档

    return summary_text

if __name__ == '__main__':

    keywords = ['支持','维权']
    k1 = 1.5
    #result_dict = dict()
    #for k in k1:
    summary_text = opinion_relevance(keywords,'weiquan')
        #result_dict[k] = summary_text
    with open('./result/p_%s.csv' % k1, 'w') as f:
        writer = csv.writer(f)
        row = [summary_text]
        writer.writerow(row)
    f.close()
    
