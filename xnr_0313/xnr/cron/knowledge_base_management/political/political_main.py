# -*- coding: utf-8 -*-

import os
import csv
import time
import heapq
import math
import random
from decimal import *
from config import DOMAIN_DICT,labels,LEFT_STA,RIGHT_STA

getcontext().prec = 50

def com_p(word_list,domain_dict):

    p = 0
    test_word = set(word_list.keys())
    train_word = set(domain_dict.keys())
    c_set = test_word & train_word
    p = sum([Decimal(domain_dict[k])*Decimal(word_list[k]) for k in c_set])

    return p

def political_classify(uid_list,uid_weibo):
    '''
    用户政治倾向分类主函数
    输入数据示例：
    uid_list:uid列表 [uid1,uid2,uid3,...]
    uid_weibo:分词之后的词频字典  {uid1:{'key1':f1,'key2':f2...}...}

    输出数据示例：
    domain：政治倾向标签字典
    {uid1:label,uid2:label2...}
    '''
    if not len(uid_weibo) and len(uid_list):
        domain = dict()
        r_domain = dict()
        for uid in uid_list:
            domain[uid] = 'mid'
        return domain
    elif len(uid_weibo) and not len(uid_list):
        uid_list = uid_weibo.keys()
    elif not len(uid_weibo) and not len(uid_list):
        domain = dict()
        return domain
    else:
        pass

    domain_dict = dict()
    r_domain = dict()
    for k,v in uid_weibo.items():
        dis = 0
        l = 'mid'
        r_dict = dict()
        for la in labels:
            re_weight = com_p(DOMAIN_DICT[la],v)
            r_dict[la] = re_weight
            if la == 'left' and re_weight >= LEFT_STA and re_weight > dis:
                dis = re_weight
                l = la
            if la == 'right' and re_weight >= RIGHT_STA and re_weight > dis:
                dis = re_weight
                l = la
        domain_dict[k] = l
        r_domain[k] = r_dict
    
    for uid in uid_list:
        if not domain_dict.has_key(uid):
            domain_dict[uid] = 'mid'

    return domain_dict
 
if __name__ == '__main__':
    #get_word()
    #main(5)
    political_classify('sensitive_uid_list')
