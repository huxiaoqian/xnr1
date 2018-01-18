# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import opencc
from global_utils_do import *

sys.path.append('../../cron')
from trans.trans import trans, traditional2simplified

# cc = opencc.OpenCC('t2s', opencc_path='/usr/bin/opencc')
s = load_scws()

def classify_by_biostring(bio_string):#根据用户bio_string划分

    # bio_string_s = cc.convert(bio_string.decode('utf-8'))
    bio_string_s = traditional2simplified(bio_string.decode('utf-8'))
    

    kwdlist = bio_string_s.encode('utf-8')#cut(s, bio_string_s.encode('utf-8'))
    lawyerw_weight = sum([1 for keyword in lawyerw if keyword in kwdlist]) # 律师
    adminw_weight = sum([1 for keyword in adminw if keyword in kwdlist]) # 组织
    mediaw_weight = sum([1 for keyword in mediaw if keyword in kwdlist]) # 媒体
    businessw_weight = sum([1 for keyword in businessw if keyword in kwdlist]) # 商业人士
    govw_weight = sum([1 for keyword in govw if keyword in kwdlist]) # 政府官员
    mediaworkerw_weight = sum([1 for keyword in mediaworkerw if keyword in kwdlist]) # 媒体人士
    universityw_weight = sum([1 for keyword in universityw if keyword in kwdlist]) # 高校

    max_weight = 0
    label = 'other'
    #equal_list = []
    
    if max_weight < businessw_weight:
        max_weight = businessw_weight
        label = 'business'
##        equal_list = ['business']
##    else:
##        pass

    if max_weight < adminw_weight:
        max_weight = adminw_weight
        label = 'admin'
##        equal_list = ['admin']
##    elif max_weight == adminw_weight:#如果相等
##        equal_list.append('admin')
##    else:
##        pass

    if max_weight < mediaw_weight:
        max_weight = mediaw_weight
        label = 'media'
##        equal_list = ['media']
##    elif max_weight == mediaw_weight:#如果相等
##        equal_list.append('media')
##    else:
##        pass

    if max_weight < lawyerw_weight:
        max_weight = lawyerw_weight
        label = 'lawyer'
##        equal_list = ['lawyer']
##    elif max_weight == lawyerw_weight:#如果相等
##        equal_list.append('lawyer')
##    else:
##        pass

    if max_weight < govw_weight:
        max_weight = govw_weight
        gov = 'politician'
##        equal_list = ['politician']
##    elif max_weight == govw_weight:#如果相等
##        equal_list.append('politician')
##    else:
##        pass

    if max_weight < mediaworkerw_weight:
        max_weight = mediaworkerw_weight
        label = 'mediaworker'
##        equal_list = ['mediaworker']
##    elif max_weight == mediaworkerw_weight:#如果相等
##        equal_list.append('mediaworker')
##    else:
##        pass

    if max_weight < universityw_weight:
        max_weight = universityw_weight
        label = 'university'
##        equal_list = ['university']
##    elif max_weight == universityw_weight:#如果相等
##        equal_list.append('university')
##    else:
##        pass

##    if len(equal_list) > 2:
##        label = 'other'
##    elif len(equal_list) == 2:
##        l1 = equal_list[0]
##        l2 = equal_list[1]
##        if DICT_LENGTH[l1] > DICT_LENGTH[l2]:
##            label = l2
##        elif DICT_LENGTH[l1] < DICT_LENGTH[l2]:
##            label = l1
##        else:
##            pass
##    else:
##        pass

    return label

def classify_inner_outer(location):

    bio_string_s = traditional2simplified(location.decode('utf-8'))
    new_location = bio_string_s.encode('utf-8')
    flag = 0
    for city in inner_city:
        if city in new_location:
            flag = 1
            break

    return flag

def domain_main(user_data):#twitter用户身份分类主函数
    '''
        输入数据：
        user_data用户数据字典：{'uid':{'description':description,'username':username,'location':location,'number_of_text':number of text}...}
        description:twitter用户背景信息中的description。注意：有部分内容是英文，需要转换成中文
        username:twitter用户背景信息中的username
        location:twitter用户背景信息中的location。注意：有部分内容是英文，需要转换成中文
        number_of_text:用户最近7天发帖数量

        输出数据：
        user_label用户身份字典:{'uid':label,'uid':label...}
    '''
    if len(user_data) == 0:
        return {}

    user_label = dict()
    for k,v in user_data.iteritems():
        label = 'other'
        try:
            description = v['description']
        except KeyError:
            description = ''
        try:
            username = v['username']
        except KeyError:
            username = ''
        try:
            location = v['location']
        except KeyError:
            location = ''            
        try:
            number_of_text = v['number_of_text']
        except KeyError:
            number_of_text = 0
        
        bio_string = username + '_' + description
        #根据bio_string划分
        if len(bio_string) > 1:
            label = classify_by_biostring(bio_string)

        if label == 'admin':#组织
            if location:
                flag = classify_inner_outer(location)
                if flag == 1:#境内
                    label = 'inner_admin'
                else:
                    label = 'outer_admin'
            else:
                label = 'admin'
        elif label == 'media':#媒体
            if location:
                flag = classify_inner_outer(location)
                if flag == 1:#境内
                    label = 'inner_media'
                else:
                    label = 'outer_media'
            else:
                label = 'media'
        else:
            pass
        
        if label != 'other':
            user_label[k] = label
            continue

        #根据发帖数量判定
        if number_of_text >= ACTIVE_COUNT:
            label = 'active'
        user_label[k] = label

    return user_label
      
        
