#-*- coding: utf-8 -*-
'''
weibo_xnr warming function
'''
import os
from xnr.global_utils import es_xnr as es
from global_utils import weibo_user_warning_index_name,weibo_user_warning_index_type,\
						weibo_event_warning_index_name,weibo_event_warning_index_type,\
						weibo_speech_warning_index_name,weibo_speech_warning_index_type

###################################################################
###################       personal warming       ##################
###################################################################

#show the personal wariming content
def show_personnal_warming():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'timestamp':{'order':'desc'}}
	}
	result=es.search(index=weibo_user_warning_index_name,doc_type=weibo_user_warning_index_type,body=query_body)['hits']['hits']
	return result


###################################################################
###################         event warming        ##################
###################################################################

#show the event wariming content
def show_event_warming():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'timestamp':{'order':'desc'}}
	}
	result=es.search(index=weibo_event_warning_index_name,doc_type=weibo_event_warning_index_type,body=query_body)['hits']['hits']
	return result

###################################################################
###################       speech warming       ##################
###################################################################

#show the speech wariming content
def show_speech_warming():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'timestamp':{'order':'desc'}}
	}
	result=es.search(index=weibo_speech_warning_index_name,doc_type=weibo_speech_warning_index_type,body=query_body)['hits']['hits']
	return result