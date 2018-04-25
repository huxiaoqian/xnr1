# -*-coding:utf-8-*-

import json
import time
import os
from DFA_filter import createWordTree, searchWord
import sys
reload(sys)
sys.path.append('../../')
from global_utils import twitter_flow_text_index_name_pre as flow_text_index_name_pre,\
                        twitter_flow_text_index_type as flow_text_index_type,\
                        es_xnr, new_tw_xnr_flow_text_index_name_pre as new_xnr_flow_text_index_name_pre,\
                        new_tw_xnr_flow_text_index_type as new_xnr_flow_text_index_type
from time_utils import ts2datetime
from parameter import sensitive_score_dict
from global_utils import R_ADMIN as r_sensitive


def compute_sensitive(text):
    score = 0
    node = createWordTree()
    sensitive_words_dict = searchWord(text.encode('utf-8'), node)
    if sensitive_words_dict:
        for k,v in sensitive_words_dict.iteritems():
            tmp_stage = r_sensitive.hget("sensitive_words", k)
            if tmp_stage:
                score += v*sensitive_score_dict[str(tmp_stage)]
    return score

def get_sensitive_info(timestamp,mid=None,text=None):
    sensitive_info = 0
    index_name = flow_text_index_name_pre + ts2datetime(timestamp)
    if mid:
        try:    #有记录就取
            item_result = es_xnr.get(index=index_name,doc_type=flow_text_index_type,id=mid)['_source']
            sensitive_info = item_result['sensitive']
            return sensitive_info
        except Exception,e: #没记录，就现算
            if text:
                sensitive_info = compute_sensitive(text)
    elif text:
        sensitive_info = compute_sensitive(text)
    else:
        pass
    return sensitive_info

def get_sensitive_user(timestamp, uid):
    score = 0
    query_body = {
        'query':{
            'term':{'uid':uid}
        },
        'size':50
    }
    index_name = flow_text_index_name_pre + ts2datetime(timestamp)
    try:
        search_results = es_xnr.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    except Exception,e:
        pass
        search_results = []
    for result in search_results:
        text = result['_source']['text'].encode('utf-8')
        node = createWordTree()
        sensitive_words_dict = searchWord(text, node)
        if sensitive_words_dict:
            sensitive_words_list = []
            for k,v in sensitive_words_dict.iteritems():
                tmp_stage = r_sensitive.hget("sensitive_words", k)
                if tmp_stage:
                    score += v*sensitive_score_dict[str(tmp_stage)]
    return score
    
if __name__ == '__main__':
    # '2017-10-15'
    # print get_sensitive_user(timestamp=1507996800, uid='100003271864059')
    print get_sensitive_info(timestamp=1507996800,mid='123124323',text=u"64和达赖太阳花")
    print get_sensitive_info(timestamp=1507996800,mid='123124323')
    print get_sensitive_info(timestamp=1507996800,text=u"64和达赖太阳花")
    print get_sensitive_info(timestamp=1507996800,)
