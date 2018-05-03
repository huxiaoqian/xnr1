# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import time
import heapq
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from textrank4zh import TextRank4Keyword, TextRank4Sentence
sys.path.append('../')
from global_utils import es_flow_text,flow_text_index_name_pre,flow_text_index_type
from global_config import S_DATE
from time_utils import get_flow_text_index_list

abs_path = './'
K1 = 1.5
B = 0.75
K3 = 500
MAX_SIZE = 999999
OPINION_CLUSTER = 5

index_list = get_flow_text_index_list(int(time.mktime(time.strptime(S_DATE, "%Y-%m-%d"))))

##对微博文本进行预处理

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

##微博文本预处理结束

## 加载分词工具

SCWS_ENCODING = 'utf-8'
SCWS_RULES = '/usr/local/scws/etc/rules.utf8.ini'
CHS_DICT_PATH = '/usr/local/scws/etc/dict.utf8.xdb'
CHT_DICT_PATH = '/usr/local/scws/etc/dict_cht.utf8.xdb'
IGNORE_PUNCTUATION = 1
ABSOLUTE_DICT_PATH = os.path.abspath(os.path.join(abs_path, './dict'))
CUSTOM_DICT_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'userdic.txt')
EXTRA_STOPWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'stopword.txt')
EXTRA_EMOTIONWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'emotionlist.txt')
EXTRA_ONE_WORD_WHITE_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'one_word_white_list.txt')
EXTRA_BLACK_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'black.txt')

cx_dict = ['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@']#关键词词性词典

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_EMOTIONWORD_PATH)]
    return one_words

def load_black_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
black_word = set(load_black_words())

def load_scws():
    s = scws.Scws()
    s.set_charset(SCWS_ENCODING)

    s.set_dict(CHS_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CHT_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CUSTOM_DICT_PATH, scws.XDICT_TXT)

    # 把停用词全部拆成单字，再过滤掉单字，以达到去除停用词的目的
    s.add_dict(EXTRA_STOPWORD_PATH, scws.XDICT_TXT)
    # 即基于表情表对表情进行分词，必要的时候在返回结果处或后剔除
    s.add_dict(EXTRA_EMOTIONWORD_PATH, scws.XDICT_TXT)

    s.set_rules(SCWS_RULES)
    s.set_ignore(IGNORE_PUNCTUATION)
    return s

SW = load_scws()

def cut_des(text_str):

    text = re_cut(text_str)
    tks = set()
    for token in SW.participle(text):
        if token[1] in cx_dict and token[0] not in black_word and len(token[0]) > 3 and token[0] not in tks:
            tks.add(token[0])

    return tks

##加载分词工具结束

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

def cut_by_textrank(text):#利用textrank切词

    w_text = re_cut(text)
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=w_text, lower=True, window=4)
    k_dict = tr4w.get_keywords(5, word_min_len=2)
    word_list = []
    for item in k_dict:
        word = item.word.encode('utf-8')
        if word not in black_word and len(word) > 3 and word not in word_list and not word.isdigit():
            word_list.append(word)

    return word_list

def summary_text(text_list):#利用textrank获取文本摘要

    text_str = ''
    for text in text_list:
        re_t = re_cut(text)
        if not len(re_t):
            continue
        re_t.replace('【','')
        re_t.replace('】','。')
        if re_t[-1] != '。':
            text_str = text_str + re_t + '。'
        else:
            text_str = text_str + re_t
    #print text_str
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text_str, lower=True, source = 'all_filters')

    n = int(0.1*len(text_list))
    if n < 1:
        n = 1
    
    result = []
    for item in tr4s.get_key_sentences(num=n):
        result.append(item.sentence)

    return '。'.join(result)

#以下是设置cluto的路径
INPUT_FOLDER = "/home/ubuntu8/yuanshi/verified_user/cluto"
VCLUTO = "/home/ubuntu8/yuanshi/verified_user/cluto-2.1.2/Linux-i686/vcluster"

