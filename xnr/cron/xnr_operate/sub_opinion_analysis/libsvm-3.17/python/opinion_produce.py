# -*- coding: utf-8 -*-

import os
import scws
import csv
import time
import re
from svmutil import *
import datetime
from datetime import datetime
from datetime import date
import heapq
import math
from config import *
from word_cut import word_net
from text_classify import text_net

def test_data(weibo,flag):
    word_dict = dict()
    reader = csv.reader(file('./svm/new_feature.csv', 'rb'))
    for w,c in reader:
        word_dict[str(w)] = c 

    sw = load_scws()
    items = []
    for i in range(0,len(weibo)):
        words = sw.participle(weibo[i])
        row = dict()
        for word in words:
            if row.has_key(str(word[0])):
                row[str(word[0])] = row[str(word[0])] + 1
            else:
                row[str(word[0])] = 1
        items.append(row)


    f_items = []
    for i in range(0,len(items)):
        row = items[i]
        f_row = ''
        f_row = f_row + str(1)
        for k,v in word_dict.iteritems():
            if row.has_key(k):
                item = str(word_dict[k])+':'+str(row[k])
                f_row = f_row + ' ' + str(item) 
        f_items.append(f_row)

    with open('./svm_test/test%s.txt' % flag, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(f_items)):
            row = []
            row.append(f_items[i])
            writer.writerow((row))
    f.close()
    
def choose_ad(flag):
##    y, x = svm_read_problem('./svm/new_train.txt')
##    m = svm_train(y, x, '-c 4')
##    svm_save_model('./svm/train.model',m)
    m = svm_load_model('./svm/train.model')
    y, x = svm_read_problem('./svm_test/test%s.txt' % flag)
    p_label, p_acc, p_val  = svm_predict(y, x, m)

    return p_label

def wash_weibo(weibo,label):

    new_list = []
    for i in range(0,len(weibo)):
        if label[i] == 0:
            new_list.append(weibo[i])

    return new_list

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
    flag = str(time.time()) + '_' + str(k_cluster)
    weibo = []
    for i in range(0,len(weibo_data)):
        text = weibo_data[i]
        n = str(text).count('@')
        if n >= 5:
            continue
        value = cut_filter(text)
        if len(value) > 0:
            if text != '转发微博':
                weibo.append(value)

    test_data(weibo,flag)#生成测试数据
    
    label = choose_ad(flag)#广告过滤

    weibo_new = wash_weibo(weibo,label)#清洗广告微博
    
    word_result,word_weight = word_net(weibo_new,k_cluster)#提取关键词对
    
    text_list,opinion_name = text_net(word_result,word_weight,weibo_new)#提取代表文本

    return opinion_name,word_result,text_list

if __name__ == '__main__':
    main('0521',5)#生成训练集
