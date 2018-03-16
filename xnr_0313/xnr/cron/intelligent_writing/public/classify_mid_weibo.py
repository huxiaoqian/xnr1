# -*- coding: utf-8 -*-

import os
import csv
import re
import time
from load_settings import load_settings

settings = load_settings()
HAPPY_WORDS = settings.get('HAPPY_WORDS')
ANGRY_WORDS = settings.get('ANGRY_WORDS')
SAD_WORDS = settings.get('SAD_WORDS')
AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

def load_happy():
    happy_list = []
    reader = csv.reader(file(os.path.join(AB_PATH, HAPPY_WORDS), 'rb'))
    for line in reader:
        happy_list.append(line[0])
    return happy_list

def load_angry():
    angry_list = []
    reader = csv.reader(file(os.path.join(AB_PATH, ANGRY_WORDS), 'rb'))
    for line in reader:
        angry_list.append(line[0])
    return angry_list

def load_sad():
    sad_list = []
    reader = csv.reader(file(os.path.join(AB_PATH, SAD_WORDS), 'rb'))
    for line in reader:
        sad_list.append(line[0])
    return sad_list

happy = load_happy()
angry = load_angry()
sad = load_sad()


def mid_sentiment_classify(text):
    """
      中性情绪再分类
      1: 高兴，2：愤怒，3: 悲伤，-1：中性
        text： utf-8
    """
    label = label_classify(text)
    if label == -1:
        label = label_adjust(label,text)

    return label 

def label_adjust(label,text):
    """根据标点符号调整类别标签
    """
    n1 = text.count('！')
    n2 = text.count('？')
    if n1 == 1 and n2 == 0:
        label = 1
    elif n1 == 1 and n2 == 1:
        label = 2
    elif n1 > 1:
        label = 2
    elif n1 == 0 and n2 > 0:
        label = 2
    elif text.find('…') != -1 or text.find('...') != -1:
        label = 3
    elif text.find('//@') == 0 or text.find('/@') == 0:
        label = 1
    else:
        label = -1

    return label


def label_classify(text):
    """根据情感词表对中性文本分类
    """
    happy_count = 0
    angry_count = 0
    sad_count = 0
    for i in range(0,len(happy)):
        if happy[i] in text:
            happy_count = happy_count + 1

    for i in range(0,len(angry)):
        if angry[i] in text:
            angry_count = angry_count + 1

    for i in range(0,len(sad)):
        if sad[i] in text:
            sad_count = sad_count + 1

    happy_count = float(happy_count)/float(len(happy))
    sad_count = float(sad_count)/float(len(sad))
    angry_count = float(angry_count)/float(len(angry))

    if happy_count >= sad_count and happy_count >= angry_count and happy_count != 0:
        return 1
    elif sad_count >= happy_count and sad_count >= angry_count and sad_count != 0:
        return 3
    elif angry_count >= happy_count and angry_count >= sad_count and angry_count != 0:
        return 2
    else:
        return -1

