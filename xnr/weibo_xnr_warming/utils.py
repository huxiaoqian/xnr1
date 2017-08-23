#-*- coding: utf-8 -*-
'''
weibo_xnr warming function
'''
import os
import json
from xnr.global_utils import es_xnr,weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                             es_flow_text,flow_text_index_type
from xnr.time_utils import get_flow_text_index_list
from xnr.parameter import USER_NUM,MAX_SEARCH_SIZE,USER_CONTENT_NUM
###################################################################
###################       personal warming       ##################
###################################################################

#思路：获取虚拟人的关注列表用户，从流数据中查询计算这些用户的敏感度，返回敏感度前100的用户及该用户敏感度最高的3条微博内容
#show the personal wariming content
def show_personnal_warming(xnr_user_no,day_time):
	#查询关注列表
	es_xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
	followers_list=es_xnr_result['followers_list']
	followers_list=json.loads(followers_list)

	flow_text_index_list=get_flow_text_index_list(int(day_time))

    #计算敏感度排名靠前的用户
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'terms':{'uid':followers_list}
				}
			}
		},
		'aggs':{
			'followers_sensitive_num':{
				'terms':{'field':'uid'},
				'aggs':{
					'sensitive_num':{
						'sum':{'field':'sensitive'}
					}
				}						
			}
			},
		'size':MAX_SEARCH_SIZE
	}
	first_sum_result=es_flow_text.search(index=flow_text_index_list,doc_type=flow_text_index_type,\
		body=query_body)['aggregations']['followers_sensitive_num']['buckets']
	top_userlist=[]
	if USER_NUM < len(first_sum_result):
		temp_num=USER_NUM
	else:
		temp_num=len(first_sum_result)
	#print temp_num
	for i in xrange(0,temp_num):
		top_userlist.append(first_sum_result[i]['key'])

	#查询敏感用户的最敏感微博内容
	results=[]
	for user in top_userlist:
		#print user
		query_body={
			'query':{
				'filtered':{
					'filter':{
						'term':{'uid':user}
					}
				}
			},
			'size':USER_CONTENT_NUM,
			'sort':{'sensitive':{'order':'desc'}}
		}
		second_result=es_flow_text.search(index=flow_text_index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
		results.extend([user,second_result])
	return results



###################################################################
###################       speech warming       ##################
###################################################################

#show the speech wariming content
def show_speech_warming(xnr_user_no,show_type,day_time):
	flow_text_index_list=get_flow_text_index_list(int(day_time))
	#关注用户
	es_xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
	followers_list=es_xnr_result['followers_list']
	followers_list=json.loads(followers_list)

	if show_type == 1:
		show_condition_list=[{'bool':{'must':{'terms':{'uid':followers_list}}}}]
	else:
		show_condition_list=[{'bool':{'must_not':{'terms':{'uid':followers_list}}}}]

	query_body={
		'query':{
			'filtered':{
				'filter':show_condition_list
			}
		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'sensitive':{'order':'desc'}}
	}

	results=es_flow_text.search(index=flow_text_index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
	return results



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
###################       微博操作公共函数       ##################
###################################################################