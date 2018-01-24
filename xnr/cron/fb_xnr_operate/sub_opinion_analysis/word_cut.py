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
import numpy as np
from config import *

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

def process_for_cluto(kEigVec,name):
    '''
    处理成cluto的输入格式，词-文本聚类
    输入数据：
        word:特征词,[(词，tfidf)]
        input_dict:每条文本中包含的词及tfidf,{"_id":{词:tfidf,词：tfidf}}
        inputs:过滤后的评论数据
    输出数据：
        cluto输入文件的位置
    '''

    #生成cluto输入文件
    #print 'kEigVec:::',kEigVec
    row = kEigVec.shape[0]#词数
    column = kEigVec.shape[1]#特征列数
    nonzero_count = 0#非0特征数

    cluto_input_folder = INPUT_FOLDER
    if not os.path.exists(cluto_input_folder):
        os.makedirs(cluto_input_folder)
    file_name = os.path.join(cluto_input_folder, '%s.txt' % name)

    with open(file_name, 'w') as fw:
        lines = []    
        #词频聚类
        count = 0
        for item in kEigVec:
            row_record = []#记录每行特征
            for i in range(len(item)):
                n = item[i]
                if n != 0:
                    nonzero_count += 1
                    row_record.append('%s %s'%(str(i+1),n))
            count = count + 1
            if count == row:
                line = ' '.join(row_record)
            else:
                line = ' '.join(row_record) + '\n'
            lines.append(line)
        fw.write('%s %s %s\n'%(row, column, nonzero_count))
        fw.writelines(lines)
    fw.close()
    return file_name

def cluto_kmeans_vcluster(k, input_file=None, vcluster=VCLUTO, \
        cluto_input_folder=INPUT_FOLDER):
    '''
    cluto kmeans聚类
    输入数据：
        k: 聚簇数
        input_file: cluto输入文件路径，如果不指定，以cluto_input_folder + pid.txt方式命名
        vcluster: cluto vcluster可执行文件路径

    输出数据：
        cluto聚类结果, list
        聚类结果评价文件位置及名称
    '''
    # 聚类结果文件, result_file
    if not input_file:
        input_file = os.path.join(cluto_input_folder, '%s.txt' % os.getpid())
        result_file = os.path.join(cluto_input_folder, '%s.txt.clustering.%s' % (os.getpid(), k))
    else:
        result_file = '%s.clustering.%s' % (input_file, k)

    command = "%s -niter=20 -zscores %s %s" % (vcluster, input_file, k)
    os.popen(command)

    results = [line.strip().split() for line in open(result_file)]

    if os.path.isfile(result_file):
        os.remove(result_file)

    if os.path.isfile(input_file):
        os.remove(input_file)
    
    return results

def kmeans(feature,k,name):

    input_file = process_for_cluto(feature,name)
    results = cluto_kmeans_vcluster(k, input_file)

    return results

def word_net(weibo,k_cluster):#词频词网
    #print 'weibo::',weibo
    #print '============================================='
    black = load_black_words()
    sw = load_scws()
    n = 0
    ts = time.time()

    f_dict = dict()#频数字典
    total = 0#词的总数
    weibo_word = []
    for i in range(0,len(weibo)):
        text = weibo[i]
        words = sw.participle(text)
        row = []
        for word in words:
            if (word[1] in cx_dict) and (3 < len(word[0]) < 30 or word[0] in single_word_whitelist) and (word[0] not in black):#选择分词结果的名词、动词、形容词，并去掉单个词
                total = total + 1
                if f_dict.has_key(str(word[0])):
                    f_dict[str(word[0])] = f_dict[str(word[0])] + 1
                else:
                    f_dict[str(word[0])] = 1
                row.append(word[0])
        weibo_word.append(row)

    keyword = TopkHeap(300)
    for k,v in f_dict.iteritems():#计算单个词的信息量
        if v >= 2 and (float(v)/float(total)) <= 0.8:#去掉频数小于3，频率高于80%的词
            p = v
            keyword.Push((p,k))#排序
    
    keyword_data = keyword.TopK()#取得前100的高频词作为顶点
    ts = time.time()
    #print 'keyword_data:::',keyword_data
    keyword = []
    k_value = dict()
    for i in range(0,len(keyword_data)):
        keyword.append(keyword_data[i][1])
        k_value[str(keyword_data[i][1])] = float(keyword_data[i][0])/float(total)

    word_net = dict()#词网字典
    for i in range(0,len(weibo_word)):
        row = weibo_word[i]
        for j in range(0,len(row)):
            if row[j] in keyword:
                if j-1 >= 0 and row[j] != row[j-1]:
                    if word_net.has_key(str(row[j]+'_'+row[j-1])):
                        word_net[str(row[j]+'_'+row[j-1])] = word_net[str(row[j]+'_'+row[j-1])] + 1
                    elif word_net.has_key(str(row[j-1]+'_'+row[j])):
                        word_net[str(row[j-1]+'_'+row[j])] = word_net[str(row[j-1]+'_'+row[j])] + 1
                    else:
                        word_net[str(row[j-1]+'_'+row[j])] = 1
                if j+1 < len(row) and row[j] != row[j+1]:
                    if word_net.has_key(str(row[j]+'_'+row[j+1])):
                        word_net[str(row[j]+'_'+row[j+1])] = word_net[str(row[j]+'_'+row[j+1])] + 1
                    elif word_net.has_key(str(row[j+1]+'_'+row[j])):
                        word_net[str(row[j+1]+'_'+row[j])] = word_net[str(row[j+1]+'_'+row[j])] + 1
                    else:
                        word_net[str(row[j]+'_'+row[j+1])] = 1

    weight = TopkHeap(500)
    for k,v in word_net.iteritems():#计算权重
        k1,k2 = k.split('_')
        if not k_value.has_key(k1):
            k_value[k1] = 0
        if not k_value.has_key(k2):
            k_value[k2] = 0
        if k_value[k1] > k_value[k2]:
            p = v*k_value[k1]
        else:
            p = v*k_value[k2]
        weight.Push((p,k))#排序

    data = weight.TopK()
    word = []
    word_weight = dict()
    for i in range(0,len(data)):
        if data[i][1] not in word:
            word.append(data[i][1])
            word_weight[data[i][1]] = data[i][0]

    #聚类
    feature = []
    for w in word:
        k1,k2 = w.split('_')
        c = []
        for i in range(0, len(weibo)):
            n1 = weibo[i].count(str(k1))
            n2 = weibo[i].count(str(k2))
            n = n1 + n2
            c.append(n)
        feature.append(c)
    #print 'feature::',feature
    features = np.array(feature)
    result = kmeans(features,k_cluster,'summary')

    word_result = dict()
    for i in range(0,len(result)):
        label = result[i][0]
        w = word[i]
        try:
            word_result[label].append(w)
        except KeyError:
            word_result[label] = [w]
        
    return word_result,word_weight

if __name__ == '__main__':
    word_net('maoming')

