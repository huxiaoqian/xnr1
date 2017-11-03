#-*- coding: utf-8 -*-
from elasticsearch import Elasticsearch


ES_CLUSTER_HOST = ['219.224.134.213:9205', '219.224.134.214:9205',\
                   '219.224.134.215:9205']

wx_xnr_index_name = 'wx_xnr'
wx_xnr_index_type = 'user'
es_xnr = Elasticsearch(ES_CLUSTER_HOST, timeout=600)


body={'doc':{'access_id': 'xxxxxx'}}


id = 'WXXNR0004'
print es_xnr.update(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, body=body, id=id)