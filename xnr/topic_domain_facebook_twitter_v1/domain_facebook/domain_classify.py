# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import opencc
import time
from global_utils_do import *

sys.path.append('../../cron')
from trans.trans import trans, traditional2simplified

# cc = opencc.OpenCC('t2s', opencc_path='/usr/bin/opencc')
s = load_scws()

def classify_by_category(category):#根据用户category划分

    category_lower = category.lower()
    if category_lower in UNIVERSITY_LABEL:
        label = 'university'
    elif category_lower in ADMIN_LABEL:
        label = 'admin'
    elif category_lower in MEDIA_LABEL:
        label = 'media'
    elif category_lower in FOLKORG_LABEL:
        label = 'folkorg'
    elif category_lower in MEDIAWORKER_LABEL:
        label = 'mediaworker'
    elif category_lower in BUSINESS_LABEL:
        label = 'business'
    elif category_lower in GOVERNMENT_LABEL:
        label = 'politician'
    else:
        label = 'other'

    return label

def classify_by_biostring(bio_string):#根据用户bio_string划分
    # bio_string_s = cc.convert(bio_string.decode('utf-8'))
    # kwdlist = cut(s, bio_string_s.encode('utf-8'))
    kwdlist = cut(s, bio_string.encode('utf-8'))

    lawyer_weight = sum([1 for keyword in kwdlist if keyword in lawyerw]) # 律师
    adminw_weight = sum([1 for keyword in kwdlist if keyword in adminw]) # 政府官员
    mediaw_weight = sum([1 for keyword in kwdlist if keyword in mediaw]) # 媒体人士
    businessw_weight = sum([1 for keyword in kwdlist if keyword in businessw]) # 商业人士

    max_weight = 0
    if max_weight < businessw_weight:
        max_weight = businessw_weight
        label = 'business'

    if max_weight < adminw_weight:
        max_weight = adminw_weight
        label = 'politician'

    if max_weight < mediaw_weight:
        max_weight = mediaw_weight
        label = 'mediaworker'

    if max_weight == 0:
        label = 'other'

    if lawyer_weight!=0:
        label = 'lawyer'

    return label

def domain_main(user_data):#facebook用户身份分类主函数
    '''
        输入数据：
        user_data用户数据字典：{'uid':{'bio_str':bio_string,'category':category,'number_of_text':number of text}...}
        bio_str:Facebook用户背景信息中的quotes、bio、about、description，用'_'链接。注意：有部分内容是英文，需要转换成中文
        category:Facebook用户背景信息中的category
        number_of_text:用户最近7天发帖数量

        输出数据：
        user_label用户身份字典:{'uid':label,'uid':label...}
    '''
    user_label={}
    uid_list = user_data.keys()
    
    if len(uid_list) == 0:
        return {}
    else:
        user_label = get_domain(user_data, user_label)
        return user_label

        
def get_domain(user_data, user_label):
    for k,v in user_data.iteritems():
        if k not in user_label:
            label = 'other'
            try:
                category = v['category']
            except KeyError:
                category = ''
            try:
                bio_string = v['bio_str']
            except KeyError:
                bio_string = ''        
            try:
                number_of_text = v['number_of_text']
            except KeyError:
                number_of_text = 0

            #根据category划分
            if category:
                label = classify_by_category(category)

            if label != 'other':
                user_label[k] = label
                continue

            #根据bio_string划分
            if bio_string:
                label = classify_by_biostring(bio_string) 
            if label != 'other':
                user_label[k] = label
                continue

            #根据发帖数量判定
            if number_of_text >= ACTIVE_COUNT:
                label = 'active'
            user_label[k] = label
    return user_label