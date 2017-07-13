# -*- coding: utf-8 -*-

import re
import csv
import sys
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('../../')
from parameter import CH_ABS_PATH as abs_path,MAX_VALUE
from global_utils import es_user_portrait,es_flow_text,portrait_index_name,portrait_index_type,\
                         flow_text_index_name_pre,flow_text_index_type

def load_words():

    reader = csv.reader(file(abs_path + '/topic_dict/train_words.csv', 'rb'))
    word_dict = []
    count = 0
    for line in reader:
        f = line[0]
        f = f.strip('\xef\xbb\xbf')
        if f not in word_dict:
            word_dict.append(f)

    return word_dict

WORD_DICT = set(load_words())

TOPIC_LIST = set(['politics','anti-corruption','fear-of-violence','peace','religion'])
EVENT_STA = 500#以一周为单位计算结果
ZERO_STA = 0.04
TOTAL_STA = 0.2324412
COUNT_STA = 2#以一周为单位计算结果
MAX_SIZE = 9999999

SEN_DICT = {1:'冲动',0:'未知',2:'抑郁',3:'冲动抑郁'}
EVENT_DICT = {1:'批判',0:'未知'}

MIN_TS = 9999999999
MAX_TS = 1356969600

def cut_filter(text):
    pattern_list = [r'\（分享自 .*\）', r'http://\w*']
    for i in pattern_list:
        p = re.compile(i)
        text = p.sub('', text)
    return text

def re_cut(w_text):#根据一些规则把无关内容过滤掉
    
    w_text = cut_filter(w_text)
    w_text = re.sub(r'[a-zA-z]','',w_text)
    a1 = re.compile(r'\[.*?\]' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'回复' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'\@.*?\:' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'\@.*?\s' )
    w_text = a1.sub('',w_text)
    if w_text == '转发微博':
        w_text = ''

    return w_text
