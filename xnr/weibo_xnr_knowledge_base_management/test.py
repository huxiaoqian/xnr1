#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import sys
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



#step 3:    change the time alert node
#explain: Carry out show_select_date_remind before change,carry out step 3.1 & 3.2
#step 3.1: show the selected time alert node
def show_select_date_remind(task_id):
    result=es.get(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)
    return result

#step 3.2: change the selected time alert node
def change_date_remind(task_id,date_name,keywords,create_type,create_time):
    date_result=es.get(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)['_source']
    content_recommend=date_result['content_recommend']
    date_time=date_result['date_time']
    #create_type=create_type
    #keywords=keywords
    #create_time=create_time

    try:
        es.update(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id,\
            body={"doc":{'date_name':date_name,'date_time':date_time,'keywords':keywords,'create_type':create_type,\
            'create_time':create_time,'content_recommend':content_recommend}})
        result=True
    except:
        result=False
    return result


#step 4:    delete the time alert node
def delete_date_remind(task_id):
    try:
        es.delete(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)
        result=True
    except:
        result=False
    return result


if __name__ == '__main__':
    rechange_date_remind()