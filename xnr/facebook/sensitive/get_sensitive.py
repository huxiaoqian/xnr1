# -*-coding:utf-8-*-

import json
import time
import os
from DFA_filter import createWordTree, searchWord
import sys
reload(sys)
sys.path.append('../../')
from global_utils import facebook_flow_text_index_name_pre as flow_text_index_name_pre,\
                        facebook_flow_text_index_type as flow_text_index_type,\
                        es_xnr
from time_utils import ts2datetime
from parameter import sensitive_score_dict
from global_utils import R_ADMIN as r_sensitive

def get_sensitive_info(timestamp,mid):
    index_name = flow_text_index_name_pre + ts2datetime(timestamp)
    try:
        item_result = es_xnr.get(index=index_name,doc_type=flow_text_index_type,id=mid)['_source']
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

    search_results = es_xnr.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

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
                     
    return score
    
if __name__ == '__main__':
    # '2017-10-15'
    print get_sensitive_user(timestamp=1507996800, uid='100023545574584')

        # for k,v in  r_sensitive.hgetall('sensitive_words').items():
        #     print k ,v
        # print r_sensitive.keys()
        # print tmp_stage