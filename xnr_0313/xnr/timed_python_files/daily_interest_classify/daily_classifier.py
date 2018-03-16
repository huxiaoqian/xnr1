# -*- coding: utf-8 -*-

import re
import opencc
import os
import time
import csv
import json
from collections import Counter
from sklearn import metrics
#from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
import numpy as np
from gensim import corpora
from utils import load_scws, cut, CLASSIFICATION_COUNT, LABEL_DICT, FASHION_DICT, SOUL_DICT, \
                 MOVIE_DICT, FITNESS_DICT, HEALTH_DICT,FINAL_DICT

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classify_dict')

##dictionary_3 = corpora.Dictionary.load(os.path.join(AB_PATH, 'daily_classify.dict'))
##word_list = [word[1].encode('utf-8') for word in dictionary_3.items()]

def load_word_list():

    reader = csv.reader(file('./classify_dict/word_list.csv', 'rb'))
    word_list = []
    count = 0
    for line in reader:
        if count == 0:
            word = line[0].strip('\xef\xbb\xbf')
        else:
            word = line[0]
        count = count + 1
        word_list.append(word)

    return word_list

def normalized_list(p_list):#归一化数据

    if len(p_list) == 0:
        return []
    n = len(p_list[0])
    max_list = [0.0]*n
    min_list = [999999.0]*n
    for i in range(0,len(p_list)):
        for k in range(0,n):
            data = p_list[i][k]
            if data >= max_list[k]:
                max_list[k] = data
            if data <= min_list[k]:
                min_list[k] = data

    x_list  = []
    for i in range(0,len(p_list)):
        row = []
        for k in range(0,n):
            data = p_list[i][k]
            dis = max_list[k] - min_list[k]
            if dis != 0:
                row.append(float(data - min_list[k])/float(dis))
            else:
                row.append(0.0)
        x_list.append(row)

    return x_list

def get_label(test_x):

    row = []
    for i in range(0,len(key_list)):
        for j in range(i+1,len(key_list)):
            key1 = key_list[i]
            key2 = key_list[j]
            if key1 == key2:
                continue
            try:
                model = joblib.load(os.path.join(AB_PATH, 'model_svc_%s_%s.pkl' % (key1,key2)))
            except:
                model = joblib.load(os.path.join(AB_PATH, 'model_svc_%s_%s.pkl' % (key2,key1)))
            predicted = model.predict(test_x)
            row.append(predicted)
    p_dict = dict(Counter(label_list[i]))
    result = 'other'
    max_v = 0
    for k,v in p_dict.iteritems():
        if v > max_v:
            max_v = v
            result = k
    if max_v > 11:
        label = result
    else:
        label = 'other'

def load_word_dict():

    word_dict = dict()
    new_label = LABEL_DICT.values()
    for k in new_label:
        reader = csv.reader(file('./word_dict/word_list_%s.csv' % k, 'rb'))
        count = 0
        word_list = []
        for line in reader:
            if count == 0:
                word = line[0].strip('\xef\xbb\xbf')
            else:
                word = line[0]
            weight = float(line[1])
            count = count + 1
            word_list.append([word,weight])
        word_dict[k] = word_list

    return word_dict

def triple_classifier_new(text_list):

    result = []
    word_dict = load_word_dict()
    for text in text_list:
        max_k = 'other'
        max_p = 0
        for k,v in word_dict.iteritems():
            sum_weight = 0
            for w in v:
                if w[0] in text:
                    sum_weight = sum_weight + w[1]
            if sum_weight > max_p:
                max_p = sum_weight
                max_k = k

        if max_p > 1:
            p = max_k
        else:
            p = 'other'
        if p in FASHION_DICT:
            result.append('fashion')
        elif p in SOUL_DICT:
            result.append('soul')
        elif p in MOVIE_DICT:
            result.append('movie')
        elif p in FITNESS_DICT:
            result.append('fitness')
        elif p in HEALTH_DICT:
            result.append('health')
        else:
            result.append(p)

    return result

##def triple_classifier_new(text_list):
##    
##    x_text = []
##    #result = []
##    word_list = load_word_list()
##    key_list = LABEL_DICT.values()
##    for text in text_list:
##        row = [text.count(w) for w in word_list]
##        x_text.append(row)
####        p = get_label(row)
####        if p in FASHION_DICT:
####            result.append('fashion')
####        elif p in SOUL_DICT:
####            result.append('soul')
####        elif p in MOVIE_DICT:
####            result.append('movie')
####        elif p in FITNESS_DICT:
####            result.append('fitness')
####        elif p in HEALTH_DICT:
####            result.append('health')
####        else:
####            result.append(p)
##    #t_x = np.array(test_x)
##
##    test_x = normalized_list(x_text)
##    label_list = dict()
####    for i in range(0,len(key_list)):
####        for j in range(0,len(key_list)):
####            key1 = key_list[i]
####            key2 = key_list[j]
####            if key1 == key2:
####                continue
####            try:
####                model = joblib.load(os.path.join(AB_PATH, 'model_svc_%s_%s.pkl' % (key1,key2)))
####            except:
####                model = joblib.load(os.path.join(AB_PATH, 'model_svc_%s_%s.pkl' % (key2,key1)))
####            predicted = model.predict(test_x)
####            for i in range(len(predicted)):
####                p = predicted[i]
####                labels.append(p)
####                label_list[i] = labels
##    for key in key_list:
##        model = joblib.load(os.path.join(AB_PATH, 'model_svc_%s.pkl' % key))
##        predicted = model.predict(test_x)
##        for i in range(len(predicted)):
##            p = predicted[i]
##            try:
##                labels = label_list[i]
##            except KeyError:
##                labels = []
##            if str(p) == '0':#其他类
##                labels.append('other')
##            else:
##                labels.append(key)
##            label_list[i] = labels
##
##    p_list = []
##    result_p = []
####    for i in range(len(text_list)):
####        p_dict = dict(Counter(label_list[i]))
####        result_p.append(p_dict)
####        result = 'other'
####        max_v = 0
####        for k,v in p_dict.iteritems():
####            if v > max_v:
####                max_v = v
####                result = k
####
####        if max_v > 11:
####            label = result
####        else:
####            label = other
####        p_list.append(label)
##
##    for i in range(len(text_list)):
##        p_dict = dict(Counter(label_list[i]))
##        result_p.append(p_dict)
##        result = 'other'
##        flag = 0
##        for k,v in p_dict.iteritems():
##            if k == 'other':
##                continue
##            if v > 0:
##                flag = flag + 1
##                result = k
##
##        if flag > 1:
##            label = 'other'
##        else:
##            label = result
##        p_list.append(label)
##        
##    result = []
##    for p in p_list:
##        if p in FASHION_DICT:
##            result.append('fashion')
##        elif p in SOUL_DICT:
##            result.append('soul')
##        elif p in MOVIE_DICT:
##            result.append('movie')
##        elif p in FITNESS_DICT:
##            result.append('fitness')
##        elif p in HEALTH_DICT:
##            result.append('health')
##        else:
##            result.append(p)
##    return result,result_p

def read_csv(path):

    word_dict = dict() 
    files = os.listdir(path)
    for filename in files:
        title = filename.replace('.csv','')
        reader = csv.reader(file(path+filename, 'rb'))
        text_list = []
        for line in reader:
            text_list.append(line[0])
        word_dict[title] = text_list

    return word_dict

if __name__ == '__main__':

    text_dict = read_csv('./data2/')

    train_text = []
    true_list = []
    false_list = []
    p_dict = dict()
    #count = 0
    for k, v in text_dict.iteritems():
        #print len(v)
        if k in FASHION_DICT:
            labels = ['fashion']*len(v)
            true_list.extend(['fashion']*len(v))
        elif k in SOUL_DICT:
            labels = ['soul']*len(v)
            true_list.extend(['soul']*len(v))
        elif k in MOVIE_DICT:
            labels = ['movie']*len(v)
            true_list.extend(['movie']*len(v))
        elif k in FITNESS_DICT:
            labels = ['fitness']*len(v)
            true_list.extend(['fitness']*len(v))
        elif k in HEALTH_DICT:
            labels = ['health']*len(v)
            true_list.extend(['health']*len(v))
        else:
            labels = [k]*len(v)
            true_list.extend([k]*len(v))
        start_ts = time.time()
        p_label = triple_classifier_new(v)
        end_ts = time.time()
        print '%s %s' % (len(v),(end_ts-start_ts))
        false_list.extend(p_label)
        for i in range(0,len(p_label)):
            if p_label[i] == labels[i]:
                try:
                    p_dict[labels[i]] = p_dict[labels[i]] + 1
                except KeyError:
                    p_dict[labels[i]] = 1

    true_dict = dict(Counter(true_list))
    false_dict = dict(Counter(false_list))
    
    with open('./result/result0720.csv', 'wb') as f:
        writer = csv.writer(f)
        for k in FINAL_DICT:
            try:
                p = p_dict[k]
            except KeyError:
                p = 0
            try:
                tp = true_dict[k]
            except KeyError:
                tp = 0
            try:
                tr = false_dict[k]
            except KeyError:
                tr = 0
            writer.writerow((k,p,tp,tr))
    f.close()


    
