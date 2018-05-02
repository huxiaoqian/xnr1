#-*-coding:utf-8-*-
import os
import json
import time
import sys
sys.path.append('../')
from global_utils import es_xnr,fb_xnr_index_name,fb_xnr_index_type
from parameter import MAX_SEARCH_SIZE

def get_compelete_fbxnr():
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'create_status':2}}
                        ]
                    }
                }
            }
        },
        'size':MAX_SEARCH_SIZE
    }
    try:
        user_result=es_xnr.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
        xnr_list=[]
        for item in user_result:
            xnr_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_list=[]
    return xnr_list