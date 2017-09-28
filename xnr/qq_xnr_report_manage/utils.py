#-*- coding: utf-8 -*-
'''
qq_xnr report manage function
'''
import os
import json
import time
from xnr.global_utils import es_xnr,qq_report_management_index_name,\
        qq_report_management_index_type
from xnr.time_utils import ts2yeartime,ts2datetime,datetime2ts
from xnr.parameter import USER_NUM, MAX_SEARCH_SIZE
from xnr.global_config import S_TYPE


def show_report_content(report_type, start_ts, end_ts, qq_xnr_no):
    result = []
    query_body = {
            'query':{
                        'bool':{
                            'must':[
                                {'term':{'report_type': report_type}},
                                {'range':{'report_time':{'gt':start_ts, 'lt':end_ts}}},
                                {'term':{'xnr_user_no': qq_xnr_no}}
                                ]
                            }
                },
            'size': MAX_SEARCH_SIZE,
            'sort': [{'report_time':{'order':'desc'}}]
            }
    es_result = es_xnr.search(index=qq_report_management_index_name, \
            doc_type=qq_report_management_index_type, body=query_body)['hits']['hits']
    print 'es_result:', es_result
    if es_result:
        result = [item['_source'] for item in es_result]
    return result



