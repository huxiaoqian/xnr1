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

def load_user_info(f_name):#加载用户背景信息

    with open(path+'scout%suser.json' % f_name) as json_file:
        data = json.load(json_file)
    json_file.close()

    user_info = dict()
    for item in data:
        uid = item['id'].encode('utf-8')
        quotes = item['quotes'].encode('utf-8')
        bio = item['bio'].encode('utf-8')
        about = item['about'].encode('utf-8')
        category = item['category'].encode('utf-8')
        description = item['description'].encode('utf-8')
        user_info[uid] = {'category':category,'bio_str':'_'.join([quotes,bio,about,description])}

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
        user_data[k] = {'category':v['category'],'bio_str':v['bio_str'],'number_of_text':number}

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

##    keyword = dict()
##    for k,v in user_label.iteritems():
##        if (v == 'politician' or v == 'business') and not user_data[k]['category']:
##            bio_string = user_data[k]['bio_str']
##            bio_string_s = cc.convert(bio_string.decode('utf-8'))
##            kwdlist = cut(s, bio_string_s.encode('utf-8'))
##            for k in kwdlist:
##                try:
##                    keyword[k] = keyword[k] + 1
##                except KeyError:
##                    keyword[k] = 1
##
##    with open('./result/keywords.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in keyword.iteritems():
##            writer.writerow((k,v))
##    f.close()

    with open('./result/user_label.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in user_label.iteritems():
            writer.writerow((k,v,user_data[k]['category'],user_data[k]['bio_str'],user_data[k]['number_of_text']))
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
    test_classify('F')
    #clean_word_dict()
