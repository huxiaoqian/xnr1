#-*-coding=utf-8-*-
#vision2
import os
import re
import sys
import json
import csv
from config import *

sw = load_scws()

def input_data(file_name):

    with open('../data/%s.json' % file_name) as json_file:
        x_data = json.load(json_file)
    json_file.close()

    topic_dict = dict()
    for item in x_data:
        uid = item['userid']
        text = item['text'].encode('utf-8')
        try:
            topic_dict[uid].append(text.strip('\n\t\r'))
        except KeyError:
            topic_dict[uid] = [text.strip('\n\t\r')]

    user_words = dict()
    for k,v in topic_dict.iteritems():
        text_str = '.'.join(v)
        words = sw.participle(text_str)
        word_dict = dict()
        for word in words:
            try:
                word_dict[word[0]] = word_dict[word[0]] + 1
            except KeyError:
                word_dict[word[0]] = 1
        user_words[k] = word_dict

    return user_words.keys(),user_words,topic_dict

    
