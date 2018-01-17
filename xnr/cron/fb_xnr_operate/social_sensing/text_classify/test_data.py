#-*-coding=utf-8-*-
#vision2
import os
import re
import sys
import json
import csv
from config import load_scws,cx_dict,single_word_whitelist,black_word,abs_path,re_cut
from test_topic import topic_classfiy

def input_data():#测试输入

    sw = load_scws()
    uid_weibo = dict()
    uid_list = []
    reader = csv.reader(file(abs_path+'/weibo_data/uid_text_0728.csv', 'rb'))
    #print 'reader::',reader
    for mid,w_text in reader:
        print 'mid:::',mid
        print 'w_text:::',w_text
        v = re_cut(w_text.decode('utf-8'))
        words = sw.participle(v.encode('utf-8'))
        word_list = dict()
        for word in words:
            if (word[1] in cx_dict) and 3 < len(word[0]) < 30 and (word[0] not in black_word) and (word[0] not in single_word_whitelist):#选择分词结果的名词、动词、形容词，并去掉单个词
                if word_list.has_key(word[0]):
                    word_list[word[0]] = word_list[word[0]] + 1
                else:
                    word_list[word[0]] = 1
        uid_list.append(mid)
        uid_weibo[mid] = word_list
    
    return uid_list,uid_weibo

if __name__ == '__main__':

    uid_list,uid_weibo = input_data()
    uid_topic = topic_classfiy(uid_list,uid_weibo)
    print uid_topic
