# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import heapq
import Levenshtein

sys.path.append('/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/intelligent_writing/text_greneration/')
from config_text_cron import re_cut,cut_des,TopkHeap

def get_s(text,weibo):#计算相似度，剔除重复文本

        max_r = 0

        for i in range(0,len(text)):
                r = Levenshtein.ratio(str(text[i]), str(weibo))
                if max_r < r:
                    max_r = r

        return max_r

def rank_text_list(text_list,keywords):#根据关键词匹配的长度，对text文本排序

    total_n = len(text_list)
    n = int(total_n*0.3)
    if n < 1:
        n = 1
    result_list = TopkHeap(n)

##  w_n = int(0.5*len(keywords))
##  if w_n < 1:
##      w_n = 1
        
    for i in range(0,len(text_list)):
        text = text_list[i]
        row = []
        word_sum = 0
        for key in keywords:
            if key in text:
                word_sum = word_sum + text.count(key)
                row.append(key)
        if len(row) >= 1:
                        result_list.Push(((len(row)*word_sum),text))
            #result_list.Push((float(word_sum)/float(len(row)),text))

    result = result_list.TopK()
        
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
    summary_list = [rank_text[0][1]]
    count = 0
    while count < 2:#将三个文本拼成一段话
        max_weight = 0
        max_index = 0
        len_sw = len(summary_word)
        w_n = int(0.3*len_sw)
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
                r = get_s(summary_list,text)
                if r >= 0.7:
                        continue
                else:
                        max_index = i
                        max_weight = weight

        if max_weight == 0:#没有可以拼接的文本
            break
        else:
            summary = summary + '。' +  rank_text[max_index][1]
            summary_word = summary_word | word_dict[max_index]
            flag_dict[max_index] = 1
            summary_list.append(rank_text[max_index][1])

        count = count + 1

    return summary


def text_generation_main(text_list,keyword_list):#文本生成主函数
    '''
    输入数据：
    text_list:文本列表
    keyword_list:关键词列表（观点关键词）

    输出数据：
    summary:生成的发帖文本
    '''

    sen_list = []
    for text in text_list:
        text_re = re_cut(text)
        ts = text_re.split('。')
        sen_list.extend(ts)

    rank_text = rank_text_list(sen_list,keyword_list)
    if len(rank_text) == 0:#加入错误判定
            summary = ''
    else:
            summary = combine_rank_text(rank_text)

    return summary