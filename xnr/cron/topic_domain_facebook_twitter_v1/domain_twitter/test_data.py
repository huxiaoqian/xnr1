# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import json
import opencc
from domain_classify import domain_main
from global_utils_do import *

path = '/home/ubuntu8/yuanshi/xnr/tweet/data/'
cc = opencc.OpenCC('t2s', opencc_path='/usr/bin/opencc')
s = load_scws()

lawyer_uid = ['55859816','882762333419741184']
university_uid = ['892431058674823169','558723995','873997240473452548','892431058674823169']
media_uid = ['427831052','116128726']
mediaworker_uid = ['49869714','99501796','2329288502','91661819','2329288502','190541883','367680547','876321004120936448',\
                '764908933446307840','578602288','2736402335']
admin_uid = ['887870714920841216','592844810','863616843889598464','886826793725960192','187428824','121328898',\
             '2450969401','69456064','863616843889598464']

def load_user_info(f_name):#加载用户背景信息

    with open(path+'scout%suser.json' % f_name) as json_file:
        data = json.load(json_file)
    json_file.close()

    user_info = dict()
    for item in data:
        uid = str(item['userid']).encode('utf-8')
        username = item['username'].encode('utf-8')
        description = item['description'].encode('utf-8')
        location = item['location'].encode('utf-8')
        user_info[uid] = {'username':username,'description':description,'location':location}        
##        quotes = item['quotes'].encode('utf-8')
##        bio = item['bio'].encode('utf-8')
##        about = item['about'].encode('utf-8')
##        category = item['category'].encode('utf-8')
##        description = item['description'].encode('utf-8')
##        user_info[uid] = {'category':category,'bio_str':'_'.join([quotes,bio,about,description])}

    return user_info

def load_user_text(f_name):#加载用户发帖信息

    with open(path+'%sID.json' % f_name) as json_file:
        data = json.load(json_file)
    json_file.close()

    user_text = dict()
    for item in data:
        uid = str(item['userid']).encode('utf-8')
        try:
            user_text[uid] = user_text[uid] + 1
        except KeyError:
            user_text[uid] = 1

    return user_text

def combine_user_info(user_info,user_text):#融合用户的信息

    user_data = dict()
    for k,v in user_info.iteritems():
        try:
            number = user_text[k]
        except KeyError:
            number = 0
        user_data[k] = {'username':v['username'],'description':v['description'],'location':v['location'],'number_of_text':number}

    return user_data

def test_classify(f_name):

    user_info = load_user_info(f_name)#加载用户背景信息
    print len(user_info)
    user_text = load_user_text(f_name)#加载用户发帖信息
    print len(user_text)
    #user_interaction = load_user_interaction()#加载用户交互信息

    user_data = combine_user_info(user_info,user_text)
    print len(user_data)
    user_label = domain_main(user_data)
    print len(user_label)

##    lawyer_keyword = dict()
##    university_keyword = dict()
##    media_keyword = dict()
##    mediaworker_keyword = dict()
##    admin_keyword = dict()
##    for k,v in user_data.iteritems():
##        bio_string = v['username'] + '_' + v['description']
##        if len(bio_string) <= 1:
##            continue
##        if k in lawyer_uid:
##            bio_string_s = cc.convert(bio_string.decode('utf-8'))
##            kwdlist = cut(s, bio_string_s.encode('utf-8'))
##            for w in kwdlist:
##                try:
##                    lawyer_keyword[w] = lawyer_keyword[w] + 1
##                except KeyError:
##                    lawyer_keyword[w] = 1
##        elif k in university_uid:
##            bio_string_s = cc.convert(bio_string.decode('utf-8'))
##            kwdlist = cut(s, bio_string_s.encode('utf-8'))
##            for w in kwdlist:
##                try:
##                    university_keyword[w] = university_keyword[w] + 1
##                except KeyError:
##                    university_keyword[w] = 1
##        elif k in media_uid:
##            bio_string_s = cc.convert(bio_string.decode('utf-8'))
##            kwdlist = cut(s, bio_string_s.encode('utf-8'))
##            for w in kwdlist:
##                try:
##                    media_keyword[w] = media_keyword[w] + 1
##                except KeyError:
##                    media_keyword[w] = 1
##        elif k in mediaworker_uid:
##            bio_string_s = cc.convert(bio_string.decode('utf-8'))
##            kwdlist = cut(s, bio_string_s.encode('utf-8'))
##            for w in kwdlist:
##                try:
##                    mediaworker_keyword[w] = mediaworker_keyword[w] + 1
##                except KeyError:
##                    mediaworker_keyword[w] = 1
##        elif k in admin_uid:
##            bio_string_s = cc.convert(bio_string.decode('utf-8'))
##            kwdlist = cut(s, bio_string_s.encode('utf-8'))
##            for w in kwdlist:
##                try:
##                    admin_keyword[w] = admin_keyword[w] + 1
##                except KeyError:
##                    admin_keyword[w] = 1
##        else:
##            continue
##
##    with open('./word_dict/admin_keywords.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in admin_keyword.iteritems():
##            writer.writerow((k,v))
##    f.close()
##
##    with open('./word_dict/mediaworker_keywords.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in mediaworker_keyword.iteritems():
##            writer.writerow((k,v))
##    f.close()
##
##    with open('./word_dict/media_keywords.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in media_keyword.iteritems():
##            writer.writerow((k,v))
##    f.close()
##
##    with open('./word_dict/university_keywords.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in university_keyword.iteritems():
##            writer.writerow((k,v))
##    f.close()
##
##    with open('./word_dict/lawyer_keywords.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in lawyer_keyword.iteritems():
##            writer.writerow((k,v))
##    f.close()

    with open('./result/user_label.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in user_label.iteritems():
            if k in lawyer_uid:
                writer.writerow((k,v,'lawyer',user_data[k]['username'],user_data[k]['description'],user_data[k]['location'],user_data[k]['number_of_text']))
            elif k in university_uid:
                writer.writerow((k,v,'university',user_data[k]['username'],user_data[k]['description'],user_data[k]['location'],user_data[k]['number_of_text']))
            elif k in media_uid:
                writer.writerow((k,v,'media',user_data[k]['username'],user_data[k]['description'],user_data[k]['location'],user_data[k]['number_of_text']))
            elif k in mediaworker_uid:
                writer.writerow((k,v,'mediaworker',user_data[k]['username'],user_data[k]['description'],user_data[k]['location'],user_data[k]['number_of_text']))
            elif k in admin_uid:
                writer.writerow((k,v,'admin',user_data[k]['username'],user_data[k]['description'],user_data[k]['location'],user_data[k]['number_of_text']))
            else:
                writer.writerow((k,v,'other',user_data[k]['username'],user_data[k]['description'],user_data[k]['location'],user_data[k]['number_of_text']))
    f.close()

def clean_word_dict():#清洗词典

    word_list = []
    reader = csv.reader(file('./result/keywords.csv', 'rb'))
    count = 0
    for line in reader:
        if count == 0:
            word = line[0].strip('\xef\xbb\xbf')
            count = 1
        else:
            word = line[0]
        word_list.append(word)

    admin_new = set(adminw) - set(word_list)
    media_new = set(mediaw) - set(word_list)
    business_new = set(businessw) - set(word_list)
    f = open('./domain_dict/adw_new.txt', 'w')
    for w in list(admin_new):
        f.write(w+'\n')
    f.close()

    f = open('./domain_dict/mediaw_new.txt', 'w')
    for w in list(media_new):
        f.write(w+'\n')
    f.close()

    f = open('./domain_dict/businessw_new.txt', 'w')
    for w in list(business_new):
        f.write(w+'\n')
    f.close()

if __name__ == '__main__':
    test_classify('T')
    #clean_word_dict()
