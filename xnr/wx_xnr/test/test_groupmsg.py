# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch


ES_CLUSTER_HOST = ['219.224.134.213:9205', '219.224.134.214:9205',\
                   '219.224.134.215:9205']
es = Elasticsearch(ES_CLUSTER_HOST, timeout=600)


xnr_puid = '85857f5f'
index_name = 'wx_group_message_2017-11-04'
wx_group_message_index_type = 'record'
msg_type = 'Text'
def aggs():
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_id": xnr_puid}},
                            {"term":{"sensitive_flag": 1}},
                            {'term':{'msg_type':'text'}}
                        ]
                    }
                }
            }
        },
        "sort":{"sensitive_value":{"order":"desc"}}
    }

    '''
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            # {"term":{"xnr_id": xnr_puid}},
                            # {"term":{"sensitive_flag": 1}},
                            {"term":{"msg_type":msg_type}},
                        ]
                    }
                }
            }
        },
        # "aggs":{
        #     "sen_users":{
        #         "terms":{"field": "speaker_id"}
        #     }
        # }
    }
    '''
    print es.search(index=index_name, doc_type=wx_group_message_index_type,body=query_body)


aggs()