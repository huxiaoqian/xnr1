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
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from imblearn.over_sampling import SMOTE
import numpy as np
from gensim import corpora, models, similarities
import math
import string
from utils import single_word_whitelist,black_word,load_scws,cx_dict,LABEL_DICT

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classify_dict')
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

def compute_idf(word,label_dict,label):

    m = 1.0
    for k,v in label_dict.iteritems():
        if k == label:
            continue
        if word in v.keys():
            m = m + 1.0
    n = len(label_dict.keys()) - 1
    idf_weight = math.log(float(n)/float(m))

    return idf_weight

def get_keyword(text_dict):

    label_dict = dict()
    for k,v in text_dict.iteritems():
        print k,len(v)
        word_dict = dict()
        for p in v:
            kw_pos = sw.participle(p)
            for kw in kw_pos:
                if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                    try:
                        word_dict[kw[0]] = word_dict[kw[0]] + 1
                    except KeyError:
                        word_dict[kw[0]] = 1

        total = sum(word_dict.values())
        new_word = dict()
        for k1,v1 in word_dict.iteritems():
            new_word[k1] = float(v1)/total*1000

        label_dict[k] = new_word

    new_label = label_dict.keys()
    new_item = dict()
    for label in new_label:#计算idf
        print '%s computing...' % label
        item_dict = dict()
        word_list = label_dict[label]
        for word,weight in word_list.iteritems():
            weight_idf = compute_idf(word,label_dict,label)#计算idf函数
            item_dict[word] = weight*weight_idf
        new_item[label] = sorted(item_dict.iteritems(), key=lambda d:d[1], reverse = True)

    word_list = []
    for k,v in new_item.iteritems():
        n = int(0.5*len(v))
        row = v[0:n]
        word_list.extend(row)
##        with open('./data/20170729/des/%s/result_tfidf_%s.csv' % (name,k), 'wb') as f:
##            writer = csv.writer(f)
##            for item in row:
##                writer.writerow(item)
##        f.close()
        
    with open('./classify_dict/word_list.csv', 'wb') as f:
        writer = csv.writer(f)
        for item in word_list:
            row = [item[0]]
            writer.writerow(row)
    f.close()

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

def combine_csv():#只取每个文档前50%的词语

    new_label = LABEL_DICT.values()
    for k in new_label:
        reader = csv.reader(file('./20170930/result_tfidf_%s.csv' % k, 'rb'))
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

        n = int(0.5*len(word_list))
        new_word = word_list[0:n]
        nomalized_word = []
        max_weight = 0
        min_weight = 9999999
        for item in new_word:
            word = item[0]
            weight = item[1]
            if weight > max_weight:
                max_weight = weight
            if weight < min_weight:
                min_weight = weight

        dis = max_weight - min_weight
        for item in new_word:
            word = item[0]
            weight = item[1]            
            if dis > 0:
                new_weight = float(weight - min_weight)/float(dis)
            else:
                new_weight = 0
            nomalized_word.append([word,new_weight])

        with open('./word_dict/word_list_%s.csv' % k, 'wb') as f:
            writer = csv.writer(f)
            for item in nomalized_word:
                writer.writerow((item[0],item[1]))
        f.close()

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
    
def main_training_by_words(text_dict):#根据word计算每个类别的权重

    avr_weight = dict()
    word_dict = load_word_dict()
    for k,v in text_dict.iteritems():
        row_weight = []
        word_list = word_dict[k]
        sum_n = 0
        for text in v:
            sum_weight = 0
            for w in word_list:
                if w[0] in text:
                    sum_weight = sum_weight + w[1]
            row_weight.append(sum_weight)
            if sum_weight > 1:
                sum_n = sum_n + 1
        #avr_weight[k] = row_weight
        print k,float(sum(row_weight))/float(len(row_weight)),max(row_weight),sum_n,len(row_weight)
        with open('./weight_dict/weight_%s.csv' % k, 'wb') as f:
            writer = csv.writer(f)
            for item in row_weight:
                row = [item]
                writer.writerow(row)
        f.close()

def training_model(label,new_text):#以k为类别训练

    train_x = []
    train_y = []
    for k,v in new_text.iteritems():
        if k == label:
            train_x.extend(v)
            train_y.extend([1]*len(v))
        else:
            train_x.extend(v)
            train_y.extend([0]*len(v))

    new_x = normalized_list(train_x)

    return new_x,train_y

def training_model_new(label1,label2,new_text):#以k为类别训练

    train_x = []
    train_y = []
    
    train_x.extend(new_text[label1])
    train_y.extend([label1]*len(new_text[label1]))

    train_x.extend(new_text[label2])
    train_y.extend([label2]*len(new_text[label2]))

    return train_x,train_y    

def main_training_new(text_dict):#针对每个类别都建立分类器

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

    new_text = dict()
    for k,v in text_dict.iteritems():
        new_list = []
        for item in v:
            row = [item.count(w) for w in word_list]
            new_list.append(row)
        new_text[k] = new_list
    
    class_list = new_text.keys()
##    for i in range(0,len(class_list)):
##        for j in range(i+1,len(class_list)):
##            train_x,train_y = training_model_new(class_list[i],class_list[j],new_text)#以k为类别训练
##            sm = SMOTE(kind='borderline2')
##            x_resampled, y_resampled = sm.fit_sample(train_x,train_y)
##            lr = LinearSVC(loss='squared_hinge')
##            lr.fit(x_resampled, y_resampled)
##            joblib.dump(lr,os.path.join(AB_PATH, 'model_svc_%s_%s.pkl' % (class_list[i],class_list[j])))

    #one-vs-rest
    for k,v in new_text.iteritems():
        print k
        train_x,train_y = training_model(k,new_text)#以k为类别训练
        sm = SMOTE(kind='borderline2')
        x_resampled, y_resampled = sm.fit_sample(train_x,train_y)
        lr = LinearSVC(loss='squared_hinge')
        lr.fit(x_resampled, y_resampled)
        joblib.dump(lr,os.path.join(AB_PATH, 'model_svc_%s.pkl' % k))

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
    #get_keyword(text_dict)
    #combine_csv()
    main_training_by_words(text_dict)
    #main_training(text_dict)
##    for i in range(0,10):
##        print i
##        text_dict = read_load2('./result/',str(i))
##        main_training(text_dict,str(i))
        
