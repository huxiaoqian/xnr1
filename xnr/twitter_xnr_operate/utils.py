#-*- coding:utf-8 -*-
import os
import time
import json
import sys
import random
import re

from xnr.global_config import S_DATE_FB,S_TYPE,S_DATE_BCI_FB,SYSTEM_START_DATE
from xnr.global_utils import es_xnr as es, tw_xnr_index_name,tw_xnr_index_type,\
					tw_xnr_timing_list_index_name, tw_xnr_timing_list_index_type,\
					tw_xnr_retweet_timing_list_index_name, tw_xnr_retweet_timing_list_index_type,\
					twitter_flow_text_index_name_pre, twitter_flow_text_index_type,\
					twitter_user_index_name, twitter_user_index_type, tw_social_sensing_index_name, \
					tw_social_sensing_index_type, tw_hot_keyword_task_index_name, tw_hot_keyword_task_index_type,\
					tw_hot_subopinion_results_index_name, tw_hot_subopinion_results_index_type, \
					es_tw_user_portrait, tw_portrait_index_name, tw_portrait_index_type, \
					tw_bci_index_name_pre, tw_bci_index_type


from xnr.twitter_publish_func import tw_publish, tw_comment, tw_retweet, tw_follow, tw_unfollow, tw_like, tw_mention, tw_message
from xnr.utils import tw_uid2nick_name_photo

def get_submit_tweet(task_detail):

	text = task_detail['text']
	tweet_type = task_detail['tweet_type']
	xnr_user_no = task_detail['xnr_user_no']

	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_publish(account_name, password, text, tweet_type, xnr_user_no)

	else:
		mark = False

	return mark

def tw_save_to_tweet_timing_list(task_detail):

	item_detail = dict()

	#item_detail['uid'] = task_detail['uid']
	item_detail['xnr_user_no'] = task_detail['xnr_user_no']
	item_detail['task_source'] = task_detail['tweet_type']
	#item_detail['operate_type'] = task_detail['operate_type']
	item_detail['create_time'] = task_detail['create_time']
	item_detail['post_time'] = task_detail['post_time']
	item_detail['text'] = task_detail['text']
	item_detail['task_status'] = task_detail['task_status'] # 0-尚未发送，1-已发送
	item_detail['remark'] = task_detail['remark']
	#item_detail['task_status'] = 0 

	task_id = task_detail['xnr_user_no'] + '_'+str(item_detail['create_time'])+'_'+ str(task_detail['post_time'])
	# task_id: uid_提交时间_发帖时间

	try:
		es.index(index=tw_xnr_timing_list_index_name,doc_type=tw_xnr_timing_list_index_type,id=task_id,body=item_detail)
		mark = True
	except:
		mark = False

	return mark
	

def get_recommend_at_user(xnr_user_no):
	#_id  = user_no2_id(user_no)
	es_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']
	#print 'es_result:::',es_result
	if es_result:
		uid = es_result['uid']
		daily_interests = es_result['daily_interests']
	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE_FB)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name = twitter_flow_text_index_name_pre + datetime
	nest_query_list = []
	daily_interests_list = daily_interests.split('&')

	es_results_daily = es_flow_text.search(index=index_name,doc_type=twitter_flow_text_index_type,\
						body={'query':{'match_all':{}},'size':200,\
						'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']

	uid_list = []
	if es_results_daily:
		for result in es_results_daily:
			result = result['_source']
			uid_list.append(result['uid'])

	## 根据uid，从weibo_user中得到 nick_name
	uid_nick_name_dict = dict()  # uid不会变，而nick_name可能会变
	es_results_user = es_flow_text.mget(index=twitter_user_index_name,doc_type=twitter_user_index_type,body={'ids':uid_list})['docs']
	i = 0
	for result in es_results_user:

		if result['found'] == True:
			result = result['_source']
			uid = result['uid']
			nick_name = result['name']
			if nick_name:
				i += 1
				uid_nick_name_dict[uid] = nick_name
		if i >= DAILY_AT_RECOMMEND_USER_TOP:
			break

	return uid_nick_name_dict

def get_daily_recommend_tweets(theme,sort_item):

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE_FB)	
	else:
		now_ts = int(time.time())

	datetime = ts2datetime(now_ts)

	index_name = daily_interest_index_name_pre +'_'+ datetime

	theme_en = daily_ch2en[theme]
	es_results = es.get(index=index_name,doc_type=daily_interest_index_type,id=theme_en)['_source']
	content = json.loads(es_results['content'])

	results_all = []
	for result in content:
		#result = result['_source']
		uid = result['uid']
		nick_name,photo_url = tw_uid2nick_name_photo(uid)
		result['nick_name'] = nick_name
		result['photo_url'] = photo_url
		results_all.append(result)
	return results_all


def get_hot_sensitive_recommend_at_user(sort_item):

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE_FB)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	sort_item = 'sensitive'
	sort_item_2 = 'timestamp'
	index_name = twitter_flow_text_index_name_pre + datetime

	query_body = {
		'query':{
			'match_all':{}
		},
		'sort':{sort_item:{'order':'desc'}},
		'size':HOT_EVENT_TOP_USER,
		'_source':['uid','user_fansnum','retweeted','timestamp']
	}

	# if sort_item == 'retweeted':
	#	 sort_item_2 = 'timestamp'
	# else:
	#	 sort_item_2 = 'retweeted'

	es_results = es_flow_text.search(index=index_name,doc_type=twitter_flow_text_index_type,body=query_body)['hits']['hits']
	
	uid_fansnum_dict = dict()
	if es_results:
		for result in es_results:
			result = result['_source']
			uid = result['uid']
			uid_fansnum_dict[uid] = {}
			uid_fansnum_dict[uid][sort_item_2] = result[sort_item_2]

	uid_fansnum_dict_sort_top = sorted(uid_fansnum_dict.items(),key=lambda x:x[1][sort_item_2],reverse=True)

	uid_set = set()

	for item in uid_fansnum_dict_sort_top:
		uid_set.add(item[0])

	uid_list = list(uid_set)


	## 根据uid，从weibo_user中得到 nick_name
	uid_nick_name_dict = dict()  # uid不会变，而nick_name可能会变
	es_results_user = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':uid_list})['docs']
	i = 0
	for result in es_results_user:
		if result['found'] == True:
			result = result['_source']
			uid = result['uid']
			nick_name = result['nick_name']
			if nick_name:
				i += 1
				uid_nick_name_dict[uid] = nick_name
		if i >= HOT_AT_RECOMMEND_USER_TOP:
			break

	return uid_nick_name_dict

def get_hot_recommend_tweets(xnr_user_no,topic_field,sort_item):

	topic_field_en = topic_ch2en_dict[topic_field]


	query_body = {
		'query':{
			'bool':{
				'must':[
					{
						'filtered':{
							'filter':{
								'term':{'topic_field':topic_field_en}
							}
						}
					}
				]
			}
			
		},
		'sort':{sort_item:{'order':'desc'}},
		'size':TOP_WEIBOS_LIMIT
	}

	es_results = es.search(index=tw_social_sensing_index_name,doc_type=tw_social_sensing_index_type,body=query_body)['hits']['hits']

	if not es_results:	
		es_results = es.search(index=tw_social_sensing_index_name,doc_type=tw_social_sensing_index_type,\
								body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
								'sort':{sort_item:{'order':'desc'}}})['hits']['hits']
	results_all = []
	for result in es_results:
		result = result['_source']
		uid = result['uid']
		nick_name,photo_url = tw_uid2nick_name_photo(uid)
		result['nick_name'] = nick_name
		result['photo_url'] = photo_url
		results_all.append(result)
	return results_all

def push_keywords_task(task_detail):

	#print 'task_detail::',task_detail

	try:
		item_dict = {}
		item_dict['task_id'] = task_detail['task_id']
		item_dict['xnr_user_no'] = task_detail['xnr_user_no']
		keywords_string = '&'.join(task_detail['keywords_string'].encode('utf-8').split('，'))
		item_dict['keywords_string'] = keywords_string
		item_dict['compute_status'] = task_detail['compute_status']
		item_dict['submit_time'] = task_detail['submit_time']
		item_dict['submit_user'] = task_detail['submit_user']
		_id = item_dict['xnr_user_no']+'_'+task_detail['task_id']
		es.index(index=tw_hot_keyword_task_index_name,doc_type=tw_hot_keyword_task_index_type,\
				id=_id,body=item_dict)
		mark = True
	except:
		mark = False

	return mark	

def get_hot_subopinion(xnr_user_no,task_id):
	
	task_id_new = xnr_user_no+'_'+task_id
	es_task = []
	try:
		es_task = es.get(index=tw_hot_keyword_task_index_name,doc_type=tw_hot_keyword_task_index_type,\
					id=task_id_new)['_source']
	except:
		return '尚未提交计算'

	if es_task:
		if es_task['compute_status'] != 2:
			return '正在计算'
		else:
			es_result = es.get(index=tw_hot_subopinion_results_index_name,doc_type=tw_hot_subopinion_results_index_type,\
								id=task_id_new)['_source']

			if es_result:
				contents = json.loads(es_result['subopinion_weibo'])
			
				return contents	

def get_bussiness_recomment_tweets(xnr_user_no,sort_item):
	
	get_results = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']
	
	monitor_keywords = get_results['monitor_keywords']
	monitor_keywords_list = monitor_keywords.split(',')
	
	if sort_item == 'timestamp':
		sort_item_new = 'timestamp'
		es_results = get_tweets_from_flow(monitor_keywords_list,sort_item_new)
	elif sort_item == 'sensitive_info':
		sort_item_new = 'sensitive'
		es_results = get_tweets_from_flow(monitor_keywords_list,sort_item_new)
	elif sort_item == 'sensitive_user':
		sort_item_new = 'sensitive'
		es_results = get_tweets_from_user_portrait(monitor_keywords_list,sort_item_new)  
	elif sort_item == 'influence_info':
		sort_item_new = 'retweeted'
		es_results = get_tweets_from_flow(monitor_keywords_list,sort_item_new)
	elif sort_item == 'influence_user':
		sort_item_new = 'user_index'
		es_results = get_tweets_from_bci(monitor_keywords_list,sort_item_new)
		
	return es_results			

def get_tweets_from_flow(monitor_keywords_list,sort_item_new):

	nest_query_list = []
	for monitor_keyword in monitor_keywords_list:
		nest_query_list.append({'wildcard':{'keywords_string':'*'+monitor_keyword+'*'}})

	query_body = {
		'query':{
			'bool':{
				'should':nest_query_list
			}  
		},
		'sort':[{sort_item_new:{'order':'desc'}},{'timestamp':{'order':'desc'}}],
		'size':TOP_WEIBOS_LIMIT
	}

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE_FB)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name = twitter_flow_text_index_name_pre + datetime

	es_results = es_flow_text.search(index=index_name,doc_type=twitter_flow_text_index_type,body=query_body)['hits']['hits']

	if not es_results:
		es_results = es_flow_text.search(index=index_name,doc_type=twitter_flow_text_index_type,\
								body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
								'sort':{sort_item_new:{'order':'desc'}}})['hits']['hits']
	results_all = []
	for result in es_results:
		result = result['_source']
		uid = result['uid']
		nick_name,photo_url = tw_uid2nick_name_photo(uid)
		result['nick_name'] = nick_name
		result['photo_url'] = photo_url
		results_all.append(result)
	return results_all	

def get_tweets_from_user_portrait(monitor_keywords_list,sort_item_new):

	query_body = {
		'query':{
			'match_all':{}
		},
		'sort':{sort_item_new:{'order':'desc'}},
		'size':USER_POETRAIT_NUMBER
	}
	#print 'query_body:::',query_body
	es_results_portrait = es_tw_user_portrait.search(index=tw_portrait_index_name,doc_type=tw_portrait_index_type,body=query_body)['hits']['hits']

	uid_set = set()

	if es_results_portrait:
		for result in es_results_portrait:
			result = result['_source']
			uid = result['uid']
			uid_set.add(uid)
	uid_list = list(uid_set)

	es_results = uid_lists2tw_from_flow_text(monitor_keywords_list,uid_list)
	
	return es_results	


def uid_lists2tw_from_flow_text(monitor_keywords_list,uid_list):

	nest_query_list = []
	for monitor_keyword in monitor_keywords_list:
		nest_query_list.append({'wildcard':{'keywords_string':'*'+monitor_keyword+'*'}})

	query_body = {
		'query':{
			'bool':{
				'should':nest_query_list,
				'must':[
					{'terms':{'uid':uid_list}}
				]
			}  
			
		},
		'size':TOP_WEIBOS_LIMIT,
		'sort':{'timestamp':{'order':'desc'}}
	}

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE_FB)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name_flow = twitter_flow_text_index_name_pre + datetime

	es_results = es_flow_text.search(index=index_name_flow,doc_type=twitter_flow_text_index_type,body=query_body)['hits']['hits']

	results_all = []
	for result in es_results:
		result = result['_source']
		uid = result['uid']
		nick_name,photo_url = tw_uid2nick_name_photo(uid)
		result['nick_name'] = nick_name
		result['photo_url'] = photo_url
		results_all.append(result)
	return results_all


def get_tweets_from_bci(monitor_keywords_list,sort_item_new):

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE_BCI_FB)	
	else:
		now_ts = int(time.time())

	datetime = ts2datetime(now_ts-24*3600)
	datetime_new = datetime[0:4]+datetime[5:7]+datetime[8:10]

	index_name = tw_bci_index_name_pre + datetime_new

	query_body = {
		'query':{
			'match_all':{}
		},
		'sort':{sort_item_new:{'order':'desc'}},
		'size':BCI_USER_NUMBER
	}

	es_results_bci = es_flow_text.search(index=index_name,doc_type=tw_bci_index_type,body=query_body)['hits']['hits']
	#print 'es_results_bci::',es_results_bci
	#print 'index_name::',index_name
	#print ''
	uid_set = set()

	if es_results_bci:
		for result in es_results_bci:
			uid = result['_id']
			uid_set.add(uid)
	uid_list = list(uid_set)

	es_results = uid_lists2tw_from_flow_text(monitor_keywords_list,uid_list)

	return es_results


def get_comment_operate(task_detail):

	text = task_detail['text']
	tweet_type = task_detail['tweet_type']
	xnr_user_no = task_detail['xnr_user_no']
	_id = task_detail['r_fid']
	#_id = ??????
	# uid = task_detail['r_uid']
	nick_name = task_detail['nick_name']

	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_comment(account_name, password, _id, nick_name, text, tweet_type, xnr_user_no)

	else:
		mark = False

	return mark

def get_retweet_operate(task_detail):

	text = task_detail['text']
	tweet_type = task_detail['tweet_type']
	xnr_user_no = task_detail['xnr_user_no']
	_id = task_detail['r_fid']
	#_id = ??????
	uid = task_detail['r_uid']

	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_retweet(account_name, password, _id, uid, text, tweet_type, xnr_user_no)

	else:
		mark = False

	return mark


def get_at_operate(task_detail):
	
	text = task_detail['text']
	tweet_type = task_detail['tweet_type']
	xnr_user_no = task_detail['xnr_user_no']
	# user_name = task_detail['nick_name']

	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_mention(account_name,password, text, xnr_user_no, tweet_type)

	else:
		mark = False

	return mark

def get_like_operate(task_detail):

	xnr_user_no = task_detail['xnr_user_no']
	_id = task_detail['r_fid']
	#_id = ??????
	#uid = task_detail['r_uid']

	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_like(account_name,password, _id)

	else:
		mark = False

	return mark

def get_follow_operate(task_detail):

	trace_type = task_detail['trace_type']
	xnr_user_no = task_detail['xnr_user_no']
	nick_name = task_detail['nick_name']
	uid = task_detail['uid']


	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_follow(account_name, password, nick_name, uid, xnr_user_no, trace_type)

	else:
		mark = False

	return mark

def get_unfollow_operate(task_detail):

	xnr_user_no = task_detail['xnr_user_no']
	uid = task_detail['uid']

	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_unfollow(account_name, password, uid, xnr_user_no)

	else:
		mark = False

	return mark


def get_private_operate(task_detail):

	xnr_user_no = task_detail['xnr_user_no']
	text = task_detail['text']
	nick_name = task_detail['nick_name']

	es_xnr_result = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

	tw_mail_account = es_xnr_result['tw_mail_account']
	tw_phone_account = es_xnr_result['tw_phone_account']
	password = es_xnr_result['password']

	if tw_phone_account:
		account_name = tw_phone_account
	elif tw_mail_account:
		account_name = tw_mail_account
	else:
		account_name = False

	if account_name:
		mark = tw_message(account_name, password,  text, nick_name)

	else:
		mark = False

	return mark

