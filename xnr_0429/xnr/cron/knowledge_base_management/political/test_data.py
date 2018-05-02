#-*-coding=utf-8-*-
#vision2
import os
import re
import sys
import json
import csv
from config import load_scws,cx_dict,single_word_whitelist,black_word,abs_path
from political_main import political_classify

def input_data():#测试输入

    sw = load_scws()
    uid_weibo = dict()
    uid_list = []
    reader = csv.reader(file('./weibo_data/uid_text_0728.csv', 'rb'))
    for mid,w_text in reader:
        if uid_weibo.has_key(str(mid)):
            uid_weibo[str(mid)] = uid_weibo[str(mid)] + '-' + w_text
        else:
            uid_weibo[str(mid)] = w_text
        if mid not in uid_list:
            uid_list.append(mid)

    uid_word = dict()
    for k,v in uid_weibo.items():
        words = sw.participle(v)
        word_list = dict()
        for word in words:
            if (word[1] in cx_dict) and 3 < len(word[0]) < 30 and (word[0] not in black_word) and (word[0] not in single_word_whitelist):#选择分词结果的名词、动词、形容词，并去掉单个词
                if word_list.has_key(word[0]):
                    word_list[word[0]] = word_list[word[0]] + 1
                else:
                    word_list[word[0]] = 1
        uid_word[k] = word_list
    
    return uid_list,uid_word

if __name__ == '__main__':
    uid_list,uid_weibo = input_data()
    domain = political_classify(uid_list,uid_weibo)
    print domain
