# -*- coding: utf-8 -*-

#  gathering snmp data
from __future__ import division
import os
import sys
import datetime
import random
import time
import re
import scws
import csv
from collections import Counter
from sklearn import metrics
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
from imblearn.over_sampling import SMOTE
import numpy as np
from gensim import corpora, models, similarities
import math
import string
from utils import single_word_whitelist,black_word,load_scws,cx_dict,LABEL_DICT

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classify_dict_new')
sw = load_scws()

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

def get_train_test(text_dict,flag):

    train_text = []
    train_y = []
    for k,v in text_dict.iteritems():
        if flag == k:
            item = ['1']*len(v)
            train_y.extend(item)
        else:
            item = ['0']*len(v)
            train_y.extend(item)
        train_text.extend(v)

    return train_text,train_y

def process_word(text_dict):

    union_set = set()
    for k,v in text_dict.iteritems():
        dictionary_3 = corpora.Dictionary.load(os.path.join(AB_PATH, 'daily_classify_%s.dict' % k))
        word_list = [word[1].encode('utf-8') for word in dictionary_3.items()]
        union_set = union_set | set(word_list)

    word_list = list(union_set)
    with open(AB_PATH+'/word_dict.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(word_list)):
            writer.writerow((i,word_list[i]))
    f.close()

def main_training(text_dict):

##    dictionary_p = corpora.Dictionary([])
    train_text = []
    train_y = []
    for k,v in text_dict.iteritems():
        print k,len(v)
##        for p in v:
##            kw_pos = sw.participle(p)
##            entries = []
##            for kw in kw_pos:
##                if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
##                    entries.append(kw[0])
##            dictionary_p.add_documents([entries])
        train_text.extend(v)
        train_y.extend([k]*len(v))
##    dictionary_p.filter_extremes(10,0.7,1000000)
##    dictionary_p.compactify()
##    dictionary_p.save('./classify_dict_new/daily_classify.dict')

    dictionary_3 = corpora.Dictionary.load(os.path.join(AB_PATH, 'daily_classify.dict'))
    word_list = [word[1].encode('utf-8') for word in dictionary_3.items()]
                    
    
    model = OneVsRestClassifier(SVC())

    train_x = []
    for text in train_text:
        row = [text.count(w) for w in word_list]
        train_x.append(row)

##        sm = SMOTE(kind='borderline2')
##        #print len(train_x),len(train_y)
##        x_resampled, y_resampled = sm.fit_sample(train_x,train_y)
##        t_x = np.array(x_resampled)
##        t_y = np.array(y_resampled)
    model.fit(train_x, train_y)
    joblib.dump(model,os.path.join(AB_PATH, 'model.pkl'))

##    X_train, X_test, y_train, y_test = cross_validation.train_test_split(train_x, train_y, test_size=0.2,random_state=0)
##    model.fit(X_train, y_train)
##    predicted = model.predict(X_test)
##
##    labels = predicted.tolist()
##    p_dict = dict()
##    for i in range(0,len(labels)):
##        if labels[i] == y_test[i]:
##            try:
##                p_dict[labels[i]] = p_dict[labels[i]] + 1
##            except KeyError:
##                p_dict[labels[i]] = 1
##
##    true_dict = dict(Counter(y_test))
##    false_dict = dict(Counter(labels))
##
##    with open('./result/result_cross.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k in LABEL_DICT.values():
##            try:
##                p = p_dict[k]
##            except KeyError:
##                p = 0
##            try:
##                tp = true_dict[k]
##            except KeyError:
##                tp = 0
##            try:
##                tr = false_dict[k]
##            except KeyError:
##                tr = 0
##            writer.writerow((k,p,tp,tr))
##    f.close()
    
if __name__ == '__main__':

    text_dict = read_csv('./data/')
    #process_word(text_dict)
    main_training(text_dict)
##    for i in range(0,10):
##        print i
##        text_dict = read_load2('./result/',str(i))
##        main_training(text_dict,str(i))
        
