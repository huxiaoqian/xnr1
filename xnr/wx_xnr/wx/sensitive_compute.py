# -*- coding: utf-8 -*-
import json
from DFA_filter import createWordTree, searchWord

def sensitive_check(text):
    DFA = createWordTree()
    item = {}
    count = 0
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

if __name__ == '__main__':
    text = u"知道64和达赖太阳花北京军区北京军区北京军区北京军区"
    count,item = sensitive_check(text.encode('utf8'))
    print count
    print item