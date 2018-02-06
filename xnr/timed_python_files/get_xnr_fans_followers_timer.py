# -*-coding:utf-8-*-

import sys
import time
import json

sys.path.append('../')
from global_utils import es_xnr, fb_xnr_index_name, fb_xnr_index_type, fb_xnr_fans_followers_index_name, fb_xnr_fans_followers_index_type,\
					tw_xnr_fans_followers_index_name, tw_xnr_fans_followers_index_type,\
					facebook_feedback_friends_index_name, facebook_feedback_friends_index_type,\
					twitter_feedback_follow_index_name, twitter_feedback_follow_index_type,\
					tw_xnr_index_name, tw_xnr_index_type

from parameter import MAX_SEARCH_SIZE

def get_fb_xnr_fans_followers():

	query_body_fb = {
		'query':{
			'term':{'create_status':2}
		},
		'size':MAX_SEARCH_SIZE
	}
	
	fb_xnrs = es_xnr.search(index=fb_xnr_index_name, doc_type=fb_xnr_index_type,\
		body=query_body_fb)['hits']['hits']

	for fb_xnr in fb_xnrs:

		root_uid = fb_xnr['_source']['uid']
		xnr_user_no = fb_xnr['_source']['xnr_user_no']

		query_body = {
			'query':{
				'term':{'root_uid':root_uid}
			},
			'size':MAX_SEARCH_SIZE
		}

		fb_results = es_xnr.search(index=facebook_feedback_friends_index_name,doc_type=facebook_feedback_friends_index_type,\
					body=query_body)['hits']['hits']
		
		friends_list = []

		for fb_result in fb_results:
			uid = fb_result['_source']['uid']
			friends_list.append(uid)

		try:
			get_results = es_xnr.get(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
				id=xnr_user_no)['_source']


			es_xnr.update(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
				id=xnr_user_no,body={'doc':{'fans_list':friends_list}})

		except:
			es_xnr.index(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
				id=xnr_user_no,body={'fans_list':friends_list})
	


def get_tw_xnr_fans_followers():

	query_body_tw = {
		'query':{
			'term':{'create_status':2}
		},
		'size':MAX_SEARCH_SIZE
	}
	
	tw_xnrs = es_xnr.search(index=tw_xnr_index_name, doc_type=tw_xnr_index_type,\
		body=query_body_tw)['hits']['hits']

	for tw_xnr in tw_xnrs:

		root_uid = tw_xnr['_source']['uid']
		xnr_user_no = tw_xnr['_source']['xnr_user_no']

		query_body = {
			'query':{
				'term':{'root_uid':root_uid}
			},
			'size':MAX_SEARCH_SIZE
		}

		tw_results = es_xnr.search(index=twitter_feedback_follow_index_name,doc_type=twitter_feedback_follow_index_type,\
					body=query_body)['hits']['hits']
		
		friends_list = []

		for tw_result in tw_results:
			uid = tw_result['_source']['uid']
			friends_list.append(uid)

		try:
			get_results = es_xnr.get(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,\
				id=xnr_user_no)['_source']


			es_xnr.update(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,\
				id=xnr_user_no,body={'doc':{'followers_list':friends_list}})

		except:
			es_xnr.index(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,\
				id=xnr_user_no,body={'followers_list':friends_list})


if __name__ == '__main__':

	get_fb_xnr_fans_followers()
	get_tw_xnr_fans_followers()