#-*- coding: utf-8 -*-

import os
import json
import time
import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es
from global_utils import weibo_date_remind_index_name,weibo_date_remind_index_name_test,weibo_date_remind_index_type,\
                         weibo_hidden_expression_index_name,weibo_hidden_expression_index_name_test,weibo_hidden_expression_index_type



def show_date_remind():
    query_body={
        'query':{
            'match_all':{}
        },
        'size':10000
    }
    result=es.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']

    fw = file('date_remind.json', 'w')
    fw.write(json.dumps(result))
    fw.close()
    # return results

def update_date_remind():
    res = []
    with open('date_remind.json') as f:
    	res = json.loads(f.read())
    index = 0
    bulk_action = []
    for cdr in res:
        index += 1
        action = {"index": {"_id": cdr['_id']}}
        bulk_action.extend([action, cdr['_source']])
        if index % 1000 == 0:        
            es.bulk(bulk_action, index=weibo_date_remind_index_name, doc_type = weibo_date_remind_index_type)
            bulk_action = []  
    if bulk_action:
        es.bulk(bulk_action, index=weibo_date_remind_index_name, doc_type = weibo_date_remind_index_type)
    print 'finish insert'

def show_hidden_expression():
    query_body={
        'query':{
            'match_all':{}
        },
        'size':10000
    }
    result=es.search(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,body=query_body)['hits']['hits']
    fw = file('hidden_expression.json', 'w')
    fw.write(json.dumps(result))
    fw.close()

def update_hidden_expression():
    res = []
    with open('hidden_expression.json') as f:
    	res = json.loads(f.read())
    index = 0
    bulk_action = []
    for cdr in res:
        index += 1
        action = {"index": {"_id": cdr['_id']}}
        bulk_action.extend([action, cdr['_source']])
        if index % 1000 == 0:        
            es.bulk(bulk_action, index=weibo_hidden_expression_index_name, doc_type = weibo_hidden_expression_index_type)
            bulk_action = []  
    if bulk_action:
        es.bulk(bulk_action, index=weibo_hidden_expression_index_name, doc_type = weibo_hidden_expression_index_type)
    print 'finish insert'


if __name__ == '__main__':
	# show_date_remind()
	update_date_remind()
	# show_hidden_expression()
	update_hidden_expression()