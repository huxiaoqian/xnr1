# -*- coding: UTF-8 -*-

import sys
import csv
import datetime
import time
from search import search_text_sentiment,search_text,search_profile
from global_utils_ch import WORD_DICT,TOPIC_LIST,EVENT_STA,re_cut,EVENT_DICT,abs_path
from triple_sentiment_classifier import triple_classifier
#from test_data import input_data2,input_data

def event_classify(uid_list, uid_dict):
    '''
      批判型的划分：根据用户文本进行划分
      输入数据：字典对象 {uid:[text1,text2,...]...}
      输出结果：dict对象
      1表示批判型，0表示未知
    '''

    uid_count = dict()
    for k in uid_list:
        if not uid_dict.has_key(k):
            uid_count[k] = 0
            continue

        v = set(uid_dict[k].keys())
        word_dict = uid_dict[k]
        uid = k
        com_set = v & WORD_DICT

        count = 0
        if not len(com_set):
            uid_count[uid] = 0
            continue
           
        for w in com_set:
            count = count + word_dict[w]

        if count >= EVENT_STA:
            uid_count[uid] = 1
        else:
            uid_count[uid] = 0

    return uid_count  

def topic_classify(uid_list):
    '''
      批判型的划分：根据用户话题属性进行划分
      输入数据：uid列表（list对象）
      输出结果：dict对象
      1表示批判型，0表示未知
    '''
    topic_result = search_profile(uid_list)

    topic_dict = dict()
    not_uid = []
    for uid in uid_list:
        item = topic_result[uid]
        if item:
            row = item.split('&')
            com_set = set(row) & TOPIC_LIST
        else:
            com_set = []
        if len(com_set) >= 2:
            flag = 1
        else:
            flag = 0
            not_uid.append(uid)

        topic_dict[uid] = flag

    return topic_dict,not_uid

def classify(uid_weibo,uid_list):
    '''
      有情感标签的分类主函数
      输入数据：list对象 [[uid,text,time],[uid,text,time],...]
      输出数据：字典对象 {uid1:str1,uid2:str2,...}
    '''

    t_result,not_uid = topic_classify(uid_list)

    e_result = event_classify(not_uid,uid_weibo)

    com_result = dict()
    for uid in uid_list:
        if t_result[uid] == 0:
            com_result[uid] = EVENT_DICT[e_result[uid]]
        else:
            com_result[uid] = EVENT_DICT[t_result[uid]]

    return com_result

def classify_topic(uid_list,uid_weibo):
    '''
        分类主函数：
        输入：用户id列表，用户微博分词列表
        输入样例：[uid1,uid2,uid3,...],{uid1:{'w1':f1,'w2':f2...}...}
    '''
    if not len(uid_weibo) and len(uid_list):
        com_result = dict()
        for uid in uid_list:
            com_result[uid] = EVENT_DICT[0]
        return com_result
    elif len(uid_weibo) and not len(uid_list):
        uid_list = uid_weibo.keys()
    elif not len(uid_weibo) and not len(uid_list):
        com_result = dict()
        return com_result
    else:
        pass

    com_result = classify(uid_weibo,uid_list)
        
    return com_result    

###以下函数仅供测试使用，目的是学习对应的参数
def get_event(uid_weibo,name):#学习文本有关的参数

    uid_list = []
    uid_dict = dict()
    for item in uid_weibo:
        uid = item[0]
        text = item[1]
        ts = item[2]
        if uid not in uid_list:
            uid_list.append(uid)
        if uid_dict.has_key(uid):
            item = uid_dict[uid]
            item.append(text)
            uid_dict[uid] = item
        else:
            item = []
            item.append(text)
            uid_dict[uid] = item       

    e_result = event_classify(uid_list, uid_dict)

    write_result(e_result,name) 

def write_result(result_dict,name):

    with open(abs_path + '/result0122/%s_data.csv' % name, 'wb') as f:
        writer = csv.writer(f)
        for k,v in result_dict.iteritems():
            writer.writerow((k,v))

def write_e_result(result_dict,name):

    with open(abs_path + '/result0122/%s_data.csv' % name, 'wb') as f:
        writer = csv.writer(f)
        for k,v in result_dict.iteritems():
            for k1,v1 in v.iteritems():
                writer.writerow((k,k1,v1[0],v1[1],v1[2]))   

if __name__ == '__main__':

    uid_list,uid_weibo = input_data('test_0126')
    start = time.time()
    uid_list = dict()
    result_dict = classify_topic(uid_list,uid_weibo)
    end = time.time()
    print 'it takes %s seconds...' % (end-start)
    print result_dict
##    with open('/home/ubuntu8/yuanshi/character/result0122/test_0226_content_new.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in result_dict.iteritems():
##            writer.writerow((k,v))
##    get_event(uid_weibo,'sta_in_event')
##    get_sentiment(uid_weibo,'sta_in_sentiment')
##    uid_weibo = input_data2('notin')
##    get_event(uid_weibo,'notin_event')
##    get_sentiment(uid_weibo,'notin_sentiment')
    






   
