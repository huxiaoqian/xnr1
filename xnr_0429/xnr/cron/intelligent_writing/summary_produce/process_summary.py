# -*- coding: utf-8 -*-

import os
import scws
import csv
import time
import re
from textrank4zh import TextRank4Sentence
from word_cut import word_net
from text_classify import text_net
from summary_config import *

def summary_main(weibo_data):#摘要自动生成主函数
    '''
        输入数据：
        weibo列表：[weibo1,weibo2,...]
    '''

    word_result,word_weight = word_net(weibo_data,5)

    text_list = text_net(word_result,word_weight,weibo_data)
    
    text_str = ''
    for text in text_list:
        re_t = re_cut(text)
        if not len(re_t):
            continue
        if re_t[-1] != '。':
            text_str = text_str + re_t + '。'
        else:
            text_str = text_str + re_t
    #print text_str
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text_str, lower=True, source = 'all_filters')

    result = []
    for item in tr4s.get_key_sentences(num=10):
        result.append(item.sentence)

    return result

if __name__ == '__main__':

    reader = csv.reader(file('./text/text_piaojinhui.csv', 'rb'))
    weibo_data = []
    count = 0
    for mid,uid,text,ts in reader:
        weibo_data.append(text)
        count = count + 1
        if count >= 1000:
            break

    result = summary_main(weibo_data)
    print result
