#-*- coding:utf-8 -*-
import json
import time
import sys
reload(sys)
sys.path.append('../../')

from time_utils import ts2datetime,datetime2ts
from global_utils import es_xnr,weibo_trace_community_index_name_pre,weibo_trace_community_index_type

def lookup_id_delete(xnr_user_no,start_time,end_time,mark=False):
    query_body={
       'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'community_name':'心灵_赞赞'}},
                            {'range':{
                            	'trace_time':{
                            		'gte':start_time,
                            		'lte':end_time
                            	}
                            }}
                        ]
                    }
                }
            }
        },
        'size':100
    }
    id_list = []
   # try:
    temp_results=es_xnr.search(index=weibo_trace_community_index_name_pre + xnr_user_no,doc_type=weibo_trace_community_index_type,body=query_body)['hits']['hits']
    for item in temp_results:
        print item['_id'],item['_source']['community_id']
            #commu_id = 'WXNR0009_2018-04-29幸福_有希'
        max_sensitive = item['_source']['max_sensitive']
        if mark and (max_sensitive > 100):
            es_xnr.update(index=weibo_trace_community_index_name_pre + xnr_user_no,doc_type=weibo_trace_community_index_type,id=item['_id'],body={'doc':{'max_sensitive':100.0000}})
            print 'delete!!!!______'+item['_id']
   # except:
    #	print 'failed!!'


def lookup_detail():
    index_name = 'weibo_community_2018-05-20'
    index_type = 'community'
    task_id = 'WXNR0009_2018-04-29富贵_师兄'
    result = es_xnr.update(index=index_name,doc_type=index_type,id=task_id,body={'doc':{'community_status':1}})
    #ommunity_user_change = result['community_user_change']
    #eturn community_user_change

    #result = es_xnr.update(index=index_name,\
    #    doc_type=index_type,id=task_id,body={'doc':{'max_sensitive':100.0000}})
    print result

def update_change(xnr_user_no,user_change,task_id,mark):
    result = es_xnr.update(index=weibo_trace_community_index_name_pre + xnr_user_no,\
        doc_type=weibo_trace_community_index_type,id=task_id,body={'doc':{'num_warning_content':user_change}})
    print result


def update_sensitive_desp(xnr_user_no,task_id):
    es_result = es_xnr.get(index=weibo_trace_community_index_name_pre + xnr_user_no,doc_type=weibo_trace_community_index_type,id=task_id)['_source']
    print 'aaaa:::',es_result['sensitive_warning_descrp']
    descp = '社区平均敏感度上升了6.9144，由10.7951上升至17.7095；社区最大敏感度上升了46.2689，由53.7311上升至100.0000。'
    result =  es_xnr.update(index=weibo_trace_community_index_name_pre + xnr_user_no,doc_type=weibo_trace_community_index_type,id=task_id,body={'doc':{'sensitive_warning_descrp':descp}})
   # print result
if __name__ == '__main__':
    xnr_user_no = 'wxnr0009'
    start_time = 1525618800
    end_time = int(time.time())
    #lookup_id_delete(xnr_user_no,start_time,end_time,mark=True)
    user_change = lookup_detail()
    #print 'user_change::',type(user_change)
    task_id = 'WXNR0009_2018-04-29幸福_有希_2018-05-21'
    #update_change(xnr_user_no,user_change,task_id,mark=True)
    #update_sensitive_desp(xnr_user_no,task_id) 
