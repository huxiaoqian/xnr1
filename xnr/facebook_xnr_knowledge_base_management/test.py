#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import sys
from elasticsearch.helpers import scan
reload(sys)
sys.setdefaultencoding('utf-8')
weibo_date_remind_index_name = 'weibo_date_remind'
weibo_date_remind_index_type = 'remind'
from elasticsearch import Elasticsearch
ES_CLUSTER_HOST = ['219.224.134.213:9205', '219.224.134.214:9205',\
                   '219.224.134.215:9205']
ES_CLUSTER_PORT = '9205'
es_xnr = Elasticsearch(ES_CLUSTER_HOST, timeout=600)

#step 2:    show the time alert node list
def rechange_date_remind():
    query_body={
        'query':{
            'match_all':{}
        },
        'size':200,
    }
    result=es_xnr.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        task_id=item['_id']
        keywords=item['_source']['keywords']
        date_name=item['_source']['date_name']
        date_time=item['_source']['date_time']
        create_type=item['_source']['create_type']
        create_time=item['_source']['create_time']
        content_recommend=item['_source']['content_recommend']
        print keywords,type(keywords)
        keywords_list=[]
        for keyword in keywords:
            keywords_list.extend(keyword.split('，'))
            es_xnr.update(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id,\
            body={"doc":{'date_name':date_name,'date_time':date_time,'keywords':keywords_list,'create_type':create_type,\
            'create_time':create_time,'content_recommend':content_recommend}})
        #print '   '.join(keywords_list)
    return True








#批量添加
def bulk_add_subbmitter(index_name,index_type):
    s_re = scan(es_xnr, query={'query':{'match_all':{}}, 'size':2},index=index_name, doc_type=index_type)
    bulk_action=[]
    count=0
    while  True:
        try:
            scan_re=s_re.next()
            _id=scan_re['_id']
            source={'doc':{'user_name':'admin@qq.com'}}
            action={'update':{'_id':_id}}
            bulk_action.extend([action,source])
            count += 1
            if count % 2 == 0:
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
    index_name='weibo_log'
    index_type='log'
    bulk_add_subbmitter(index_name,index_type)