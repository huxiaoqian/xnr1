#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import sys
from elasticsearch.helpers import scan
reload(sys)
sys.setdefaultencoding('utf-8')

from elasticsearch import Elasticsearch
ES_CLUSTER_HOST = ['219.224.134.213:9205', '219.224.134.214:9205',\
                   '219.224.134.215:9205']
ES_CLUSTER_PORT = '9205'
es_xnr = Elasticsearch(ES_CLUSTER_HOST, timeout=600)


#批量添加
def bulk_add_subbmitter(index_name,index_type):
    s_re = scan(es_xnr, query={'query':{'match_all':{}}, 'size':4},index=index_name, doc_type=index_type)
    bulk_action=[]
    count=0
    while  True:
        try:
            scan_re=s_re.next()
            _id=scan_re['_id']
            source={'doc':{'status':0}}
            action={'update':{'_id':_id}}
            bulk_action.extend([action,source])
            count += 1
            if count % 4 == 0:
                es_xnr.bulk(bulk_action,index=index_name,doc_type=index_type,timeout=100)
                bulk_action = []
            else:
                pass
        except:
            if bulk_action:
               es_xnr.bulk(bulk_action,index=index_name,doc_type=index_type,timeout=100)
            else:
               break

if __name__ == '__main__':
    #rechange_date_remind()
    index_name = 'opinion_corpus'
    index_type = 'text'
    bulk_add_subbmitter(index_name,index_type)