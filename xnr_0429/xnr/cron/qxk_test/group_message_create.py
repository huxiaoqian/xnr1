#-*- coding: utf-8 -*-

import os
import json
import time
import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es


def show_groupmessage():
    query_body={
        'query':{
            'match_all':{}
        },
        'size':100
    }
    result=es.search(index='group_message_2018-03-08',doc_type='record',body=query_body)['hits']['hits']

    fw = file('group_message_2018-03-08.json', 'w')
    fw.write(json.dumps(result))
    fw.close()
    # return results

def update_groupmessage():
    res = []
    with open('group_message_2018-03-07.json') as f:
    	res = json.loads(f.read())
    index = 0
    bulk_action = []
    for cdr in res:
        index += 1
        action = {"index": {"_id": cdr['_id']}}
        bulk_action.extend([action, cdr['_source']])
        if index % 100 == 0:        
            es.bulk(bulk_action, index='group_message_2018-03-07', doc_type = 'record')
            bulk_action = []  
    if bulk_action:
        es.bulk(bulk_action, index='group_message_2018-03-07', doc_type = 'record')
    print 'finish insert'





if __name__ == '__main__':
    # show_groupmessage()
    update_groupmessage()
