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
import Levenshtein
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from config import cut_by_textrank,TopkHeap,K1,B,K3,global_utils_route
sys.path.append(global_utils_route)
from global_utils import qa_corpus_index_name,qa_corpus_index_type,es_xnr

def load_question_dict():#加载question语料
    
    query_body = {'query':{'match_all':{}}}
    question_dict = dict()
    s_re = scan(es_xnr, query=query_body, index=qa_corpus_index_name, doc_type=qa_corpus_index_type)
    while True:
        try:
            scan_re = s_re.next()['_source']
            try:
                text = scan_re['text'].encode('utf-8')
                answer_list = scan_re['answer_list'].encode('utf-8').split('&')
                question_dict[text] = set(answer_list)
                
            except:
                continue
        except StopIteration:
            break
    
    return question_dict


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

def rank_text_list(text_list,keywords,keyword_count,avr_n,word_set):#对text文本排序

    total_n = len(text_list)
    n = int(total_n*0.3)
    if n < 1:
        n = 1
    result_list = TopkHeap(n)
    for i in range(0,len(text_list)):
        text = text_list[i]
        word = word_set[i]
        score = get_related_score(text,keywords,keyword_count,avr_n,total_n)
        result_list.Push((score,text,word))

    result = result_list.TopK()

    return result

def get_text_by_BM(text_list,keywords):#根据BM检索对应的文本

    if len(text_list) == 0:
        return [],[]

    keyword_count = dict()
    related_text = []
    word_set = []
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
                flag = flag + 1
                row.append(key)
        word_set.append(row)
        if flag > 0:#表明没有加过长度
            related_text.append(text)            
            total_n = total_n + len(text)

    avr_n = total_n/float(len(text_list))
    if len(keyword_count) == 0:#语料库里面没有该问题相匹配的
    	return [],[]
    rank_text = rank_text_list(text_list,keywords,keyword_count,avr_n,word_set)

    result = []
    word_result = []
    for i in range(len(rank_text)):
        if rank_text[i][1] not in result:
            result.append(rank_text[i][1])
            word_result.append(rank_text[i][2])

    return result,word_result

def search_answer(text):#检索问题主函数
    '''
        输入数据：
        text:问题文本

        输出数据：
        text_question:字符串
        answer:列表，推荐的答案
    '''
    if len(text) == 0:
        return '',[]
    keywords = cut_by_textrank(text)
    
    question_dict = load_question_dict()

    key_list =  question_dict.keys()
    text_list,word_dict = get_text_by_BM(key_list,keywords)

    if len(text_list) == 0:
        return '',[]
    
    n = int(0.3*len(text_list))
    if n < 1:
        n = 1
    result_list = TopkHeap(n)

    for i in range(0,len(text_list)):        
        r = Levenshtein.ratio(text_list[i], text)
        result_list.Push((r,text_list[i]))
        

    result = result_list.TopK()
    if len(result) == 0:
        return '',[]
  
    text_question = result[0][1]
    answer = question_dict[text_question]

    return text_question,list(answer)

if __name__ == '__main__':

    text_question,answer = search_answer('美国警方宣布')

    print text_question.decode('utf-8')
    for item in answer:
        print item.decode('utf-8')

##    with open('./text_data/answer/text_answer.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for i in range(0,len(key_list)):
##            #row = [lines[i][0]]
##            writer.writerow((key_list[i][0],key_list[i][1]))
##
##    f.close()
##    with open('./text_data/answer/text_text.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for i in range(0,len(text_list)):
##            row = [text_list[i]]
##            writer.writerow(row)
##
##    f.close()

    
