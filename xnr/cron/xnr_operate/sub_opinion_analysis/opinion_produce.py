# -*- coding: utf-8 -*-

import os
import scws
import csv
import time
import re
import datetime
from datetime import datetime
from datetime import date
import heapq
import math
import sys
from config import *
from word_cut import word_net
from text_classify import text_net

def opinion_main(weibo_data,k_cluster):
    '''
        观点挖掘主函数：
        输入数据：
        weibo_data：微博列表，[weibo1,weibo2,...]
        k_cluster：子话题个数

        输出数据：
        opinion_name：子话题名称字典，{topic1:name1,topic2:name2,...}
        word_result：子话题关键词对，{topic1:[w1,w2,...],topic2:[w1,w2,...],...}
        text_list：子话题对应的文本，{topic1:[text1,text2,...],topic2:[text1,text2,..],..}
    '''
    
    weibo_new = []
    for i in range(0,len(weibo_data)):
        text = weibo_data[i]
        n = str(text).count('@')
        if n >= 5:
            continue
        value = cut_filter(text)
        if len(value) > 0:
            if text != '转发微博':
                weibo_new.append(value)
    
    word_result,word_weight = word_net(weibo_new,k_cluster)#提取关键词对
    
    text_list,opinion_name = text_net(word_result,word_weight,weibo_new)#提取代表文本

    return opinion_name,word_result,text_list

if __name__ == '__main__':
    main('0521',5)#生成训练集
