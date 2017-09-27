# -*- coding: utf-8 -*-

import re
import opencc
import os
import time
import csv
import json
from collections import Counter
from sklearn import metrics
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
import numpy as np
from gensim import corpora
from utils import load_scws, cut, CLASSIFICATION_COUNT, LABEL_DICT, FASHION_DICT, SOUL_DICT, \
                 MOVIE_DICT, FITNESS_DICT, HEALTH_DICT,FINAL_DICT

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classify_dict')

dictionary_3 = corpora.Dictionary.load(os.path.join(AB_PATH, 'daily_classify.dict'))
word_list = [word[1].encode('utf-8') for word in dictionary_3.items()]

def triple_classifier_new(text_list):
       
    test_x = []
    for text in text_list:
        row = [text.count(w) for w in word_list]
        test_x.append(row)
    t_x = np.array(test_x)

    model = joblib.load(os.path.join(AB_PATH, 'model.pkl'))
    predicted = model.predict(t_x)

    p_list = predicted.tolist()

    result = []
    for p in p_list:
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


    
