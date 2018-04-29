# -*-coding:utf-8-*-

import json
import time
import os
from DFA_filter import createWordTree, searchWord

import sys
reload(sys)
sys.path.append('../')

from global_utils import flow_text_index_name_pre,flow_text_index_type,es_flow_text
from time_utils import ts2datetime
from parameter import sensitive_score_dict

def get_sensitive_info(timestamp,mid):
    index_name = flow_text_index_name_pre + ts2datetime(timestamp)
    try:
        item_result = es_flow_text.get(index=index_name,doc_type=flow_text_index_type,id=mid)['_source']
        sensitive_info = item_result['sensitive']
    except:
        sensitive_info = 0

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

    search_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

    for result in search_results:

        text = result['_source']['text'].encode('utf-8')

        node = createWordTree();
        sensitive_words_dict = searchWord(text, node)

        if sensitive_words_dict:
            
            sensitive_words_list = []

            for k,v in sensitive_words_dict.iteritems():
                tmp_stage = r_sensitive.hget("sensitive_words", k)
                if tmp_stage:
                    score += v*sensitive_score_dict[str(tmp_stage)]
    print '\n'    
    print '\n'    
    print '\n'    
    print '\n'
    print '\n'    
    print 'score=============',score    
    print '\n'    
    print '\n'    
    print '\n'    
    print '\n'    
    return score   
