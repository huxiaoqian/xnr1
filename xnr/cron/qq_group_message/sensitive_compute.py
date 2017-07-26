# -*- coding=utf-8 -*-
'''
date: 2017-07-22
operator: Noah
goal: Use to search sensitive word and compute sensitive value
'''

from DFA_filter.py import createWordTree, searchWord

def sensitive_check(text):
# 待改
    DFA = createWordTree()
    count = 0
    sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
    if sensitive_words_dict:
        item['sensitive_words_string'] = "&".join(sensitive_words_dict.keys())
        item['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
    else:
        item['sensitive_words_string'] = ""
        item['sensitive_words_dict'] = json.dumps({})
     if sensitive_words_dict:
        print sensitive_words_dict.keys()[0]
        sensitive_count_string = r_cluster.hget('sensitive_'+str(ts), str(uid))
        if sensitive_count_string: #redis取空
            sensitive_count_dict = json.loads(sensitive_count_string)
            for word in sensitive_words_dict.keys():
                if sensitive_count_dict.has_key(word):
                    sensitive_count_dict[word] += sensitive_words_dict[word]
                else:
                    sensitive_count_dict[word] = sensitive_words_dict[word]
            r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_count_dict))
        else:
            r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_words_dict))