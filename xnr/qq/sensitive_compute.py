# -*- coding=utf-8 -*-
'''
date: 2017-07-22
operator: Noah
goal: Use to search sensitive word and compute sensitive value
'''

import json
from DFA_filter import createWordTree, searchWord

def sensitive_check(text):
# 待改
    DFA = createWordTree()
    item = {}
    count = 0
    # sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
    sensitive_words_dict = searchWord(text, DFA)
    if sensitive_words_dict:
        item['sensitive_words_string'] = "&".join(sensitive_words_dict.keys())
        item['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
    else:
        item['sensitive_words_string'] = ""
        item['sensitive_words_dict'] = json.dumps({})
    for i in sensitive_words_dict:
        count += sensitive_words_dict[i]

    return count,item
    # if sensitive_words_dict:
    #     print sensitive_words_dict.keys()[0]
    #     sensitive_count_string = r_cluster.hget('sensitive_'+str(ts), str(uid))
    #     if sensitive_count_string: #redis取空
    #         sensitive_count_dict = json.loads(sensitive_count_string)
    #         for word in sensitive_words_dict.keys():
    #             if sensitive_count_dict.has_key(word):
    #                 sensitive_count_dict[word] += sensitive_words_dict[word]
    #             else:
    #                 sensitive_count_dict[word] = sensitive_words_dict[word]
    #         r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_count_dict))
    #     else:
    #         r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_words_dict))



if __name__ == '__main__':
    count,item = sensitive_check("知道64和达赖太阳花北京军区北京军区北京军区北京军区")
    print count
    print item