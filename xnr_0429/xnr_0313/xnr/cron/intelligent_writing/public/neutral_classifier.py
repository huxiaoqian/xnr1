# -*- coding: utf-8 -*-

#  gathering snmp data
from __future__ import division
import os
import datetime
import random
import time
import nltk
import re
import string
#from xapian_case.utils import cut, load_scws
from global_utils_do import cut, load_scws
from gensim import corpora, models, similarities

sw = load_scws()

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

EMOTICON_CONFLICTS_FILE = os.path.join(AB_PATH, './sentiment/emoticons4conflict.txt')
DICT_FILE = os.path.join(AB_PATH, './sentiment/subjective_54W_4.dict')
EMOTICON_FILE = os.path.join(AB_PATH, './sentiment/new_emoticon_54W_4.txt')

def emoticon(pe_set, ne_set, text):
    """ Extract emoticons and define the overall sentiment"""

    emotion_pattern = r'\[(\S+?)\]'
    remotions = re.findall(emotion_pattern, text)
    p = 0
    n = 0

    if remotions:
        for e in remotions:
            if e in pe_set:
                p = 1
            elif e in ne_set:
                n = 1

    state = 0
    if p == 1 and n == 0:
        state = 1
    elif p == 0 and n == 1:
        state = 2


    return state


def remove_at(text):
    """text去除@
       text: utf-8
    """
    at_pattern = r'\/\/@(.+?):'
    text = re.sub(at_pattern, '。', text)

    return text


'''define 2 kinds of seed emoticons'''
pe_set = set([])
ne_set = set([])
with open( EMOTICON_CONFLICTS_FILE) as f:
    for l in f:
        pair = l.rstrip().split(':')
        if pair[1] == '1':
            pe_set.add(pair[0])
        else:
            ne_set.add(pair[0])

'''define subjective dictionary and subjective words weight'''
dictionary_1 =corpora.Dictionary.load(DICT_FILE)
step1_score = {}
with open(EMOTICON_FILE) as f:
    for l in f:
        lis = l.rstrip().split()
        step1_score[int(lis[0])] = [float(lis[1]),float(lis[2])]


def triple_classifier(tweet):
    """content168 以utf-8编码
    """
    sentiment = 0
    text = tweet['content168']

    if '//@' in text:
        text = text[:text.index('//@')]

    if not len(text):
        text = remove_at(tweet['content168'])

    emoticon_sentiment = emoticon(pe_set,ne_set, text)
    if emoticon_sentiment in [1,2]:
        sentiment = 1
        text = ''

    if text != '':
        entries = cut(sw, text)
        entry = [e.decode('utf-8') for e in entries]
        bow = dictionary_1.doc2bow(entry)
        s = [1,1]
        for pair in bow:
            s[0] = s[0] * (step1_score[pair[0]][0] ** pair[1])
            s[1] = s[1] * (step1_score[pair[0]][1] ** pair[1])
        if s[0] <= s[1]:
            sentiment = 1
        else:
            sentiment = 0

    return sentiment
