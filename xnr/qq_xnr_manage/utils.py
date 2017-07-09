# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import sys
from xnr.global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type
from xnr.parameter import MAX_VALUE

def create_qq_xnr(xnr_info):
# xnr_info = [qq_number,qq_groups,nickname,active_time]
    qq_number = xnr_info[0]
    qq_groups = xnr_info[1]
    nickname = xnr_info[2]
    active_time = xnr_info[3]
    try:
        es_xnr.index(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number, \
        body={'qq_number':qq_number,'nickname':nickname,'qq_groups':qq_groups,'active_time':active_time})
        result = 'Insert sucessful'
    except:
        result = 'Not sucessful'
    return result

def show_qq_xnr(MAX_VALUE):
    query_body = {
        'query':{
            'match_all':{}
        },
    }
    result = es_xnr.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, body=query_body)
    
    return result

def delete_qq_xnr(qq_number):
    try:
        es_xnr.delete(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number)
        result = 'Sucessful deleted'
    except:
        result = 'Not successful'
    return result

def change_qq_xnr(xnr_info):
    qq_number = xnr_info[0]
    qq_groups = xnr_info[1]
    try:
        es_xnr.update(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number,  \
            body={"doc":{'qq_groups':qq_groups,}})
        result = 'Successfully changed'
    except:
        result = 'Changing Failed'
    return result

def search_qq_xnr(qq_number):
    query_body = {
    "query": {
        "filtered":{
            "filter":{
                "term":{"qq_number": qq_number}
            }
        }
    },
    'size':MAX_VALUE
}

    result = es_xnr.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, body=query_body)
    
    return result