# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv

sys.path.append('../../')
from parameter import TW_DOMAIN_ABS_PATH as abs_path

##加载领域标签

labels = ['university', 'admin', 'inner_admin', 'outer_admin', 'media', 'inner_media', 'outer_media', \
          'lawyer', 'politician', 'mediaworker', 'activer', 'other', 'business']
zh_labels = ['高校', '组织', '境内组织', '境外组织', '媒体', '境内媒体', '境外媒体', '法律机构及人士', \
             '政府机构及人士', '媒体人士', '活跃人士',  '其他', '商业人士']

##领域标签加载结束

##加载特定身份的词典

def getGovWords():
    adminw = []
    f = open(abs_path+'/domain_dict/adw_new.txt', 'r')
    for line in f:
        w = line.strip()
        adminw.append(w) # 政府职位相关词汇
    f.close()

    return adminw

govw = getGovWords()

def getMediaworkerWords():
    mediaworkerw = []
    mediaf = open(abs_path+'/domain_dict/mediaworker_new.txt','r')
    for line in mediaf:
        mediaworkerw.append(line.strip()) # 媒体相关词汇

    return mediaworkerw

mediaworkerw = getMediaworkerWords()

def getBusinessWords():
    businessw = []
    f = open(abs_path+'/domain_dict/businessw_new.txt', 'r')
    for line in f:
        businessw.append(line.strip()) # 商业人士词汇

    return businessw

businessw = getBusinessWords()

def getAdminWords():
    adminw = []
    f = open(abs_path+'/domain_dict/admin_new.txt', 'r')
    for line in f:
        w = line.strip()
        adminw.append(w) # 政府职位相关词汇
    f.close()

    return adminw

adminw = getAdminWords()

def getLawyerWords():
    lawyerw = []
    mediaf = open(abs_path+'/domain_dict/lawyer_new.txt','r')
    for line in mediaf:
        lawyerw.append(line.strip()) # 媒体相关词汇

    return lawyerw

lawyerw = getLawyerWords()

def getMediaWords():
    mediaw = []
    f = open(abs_path+'/domain_dict/media_new.txt', 'r')
    for line in f:
        mediaw.append(line.strip()) # 商业人士词汇

    return mediaw

mediaw = getMediaWords()

def getUniversityWords():
    universityw = []
    f = open(abs_path+'/domain_dict/university_new.txt', 'r')
    for line in f:
        universityw.append(line.strip()) # 商业人士词汇

    return universityw

universityw = getUniversityWords()

ACTIVE_COUNT = 50
DICT_LENGTH = {'university':len(universityw),'admin':len(adminw), 'media':len(mediaw),\
          'lawyer':len(lawyerw), 'politician':len(govw), 'mediaworker':len(mediaworkerw), 'business':len(businessw)}

def getCityWords():
    city = []
    f = open(abs_path+'/domain_dict/inner_city.txt', 'r')
    for line in f:
        city.append(line.strip()) # 中国城市列表词汇

    return city

inner_city = getCityWords()

##加载特定身份的词典结束

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
    if w_text == u'转发微博':
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

cx_dict = ['an','Ng','n','nr','ns','nt','nz','vn','@']#关键词词性词典

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

def cut(s, text, f=None, cx=False):
    if f:
        tks = [token for token
               in s.participle(cut_filter(text))
               if token[1] in f and (3 < len(token[0]) < 30 or token[0] in single_word_whitelist)]
    else:
        tks = [token for token
               in s.participle(cut_filter(text))
               if 3 < len(token[0]) < 30 or token[0] in single_word_whitelist]
    if cx:
        return tks
    else:
        return [tk[0] for tk in tks]
##加载分词工具结束

####标准化领域字典
##def start_p():
##
##    domain_p = dict()
##    for name in txt_labels:
##        domain_p[name] = 0
##
##    return domain_p
##
##DOMAIN_P = start_p()
####标准化结束
