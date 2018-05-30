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
                            {'term':{'xnr_user_no':xnr_user_no}},
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
        }
    }
    id_list = []
    try:
        temp_results=es_xnr.search(index=weibo_trace_community_index_name_pre + xnr_user_no,doc_type=weibo_trace_community_index_type,body=query_body)['hits']['hits']
        for item in temp_results:
            print item['_id']
            if mark == True:
                es_xnr.delete(index=weibo_trace_community_index_name_pre + xnr_user_no,doc_type=weibo_trace_community_index_type,id=item['_id'])
                print 'delete!!!!______'+item['_id']
    except:
    	print 'failed!!'

if __name__ == '__main__':
    xnr_user_no = 'wxnr0004'
    start_time = 1480089600
    end_time = 1480176000
    lookup_id_delete(xnr_user_no,start_time,end_time)
