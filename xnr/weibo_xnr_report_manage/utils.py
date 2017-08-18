# -*- coding:utf-8 -*-

'''
weibo report management
'''
import sys
import json
from xnr.global_utils import es_xnr,weibo_report_management_index_name,weibo_report_management_index_type
from xnr.parameter import MAX_VALUE

#show report content
def show_report_content():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'report_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,body=query_body)['hits']['hits']
	return result

#pubic function:like ,retweet ,comment

#export into excel