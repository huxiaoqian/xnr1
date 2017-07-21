#-*- coding:utf-8 -*-
import os
import time
import json
import sys

#reload(sys)
#sys.path.append('../../')
from xnr.global_config import S_DATE,S_TYPE,S_DATE_BCI
from xnr.global_utils import es_xnr as es
from xnr.global_utils import weibo_hot_keyword_task_index_name,weibo_hot_keyword_task_index_type,\
                            weibo_xnr_timing_list_index_name,weibo_xnr_timing_list_index_type,\
                            weibo_xnr_index_name,weibo_xnr_index_type,es_flow_text,flow_text_index_name_pre,\
                            flow_text_index_type,es_user_profile,profile_index_name,profile_index_type,\
                            social_sensing_index_name,social_sensing_index_type,\
                            weibo_hot_content_recommend_results_index_name,\
                            weibo_hot_content_recommend_results_index_type,\
                            weibo_hot_subopinion_results_index_name,weibo_hot_subopinion_results_index_type,\
                            weibo_bci_index_name_pre,weibo_bci_index_type,portrait_index_name,portrait_index_type,\
                            es_user_portrait,es_user_profile

from xnr.time_utils import ts2datetime,datetime2ts
from xnr.weibo_publish_func import publish_tweet_func
from xnr.parameter import DAILY_INTEREST_TOP_USER,DAILY_AT_RECOMMEND_USER_TOP,TOP_WEIBOS_LIMIT,\
						HOT_AT_RECOMMEND_USER_TOP,HOT_EVENT_TOP_USER,BCI_USER_NUMBER,USER_POETRAIT_NUMBER
from save_to_weibo_xnr_flow_text import save_to_xnr_flow_text

def push_keywords_task(task_detail):

    print 'task_detail::',task_detail

    try:
        task_id = task_detail['task_id']
        keywords_string = '&'.join(task_detail['keywords_string'].encode('utf-8').split('，'))
        task_detail['keywords_string'] = keywords_string
        es.index(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                id=task_id,body=task_detail)
        mark = True
    except:
        mark = False

    return mark

def get_submit_tweet(task_detail):

    text = task_detail['text']
    tweet_type = task_detail['tweet_type']
    uid = task_detail['uid']
    weibo_mail_account = task_detail['weibo_mail_account']
    weibo_phone_account = task_detail['weibo_phone_account']
    password = task_detail['password']
    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False
    # 发布微博
    try:
        publish_tweet_func(account_name,password,text)
        mark = True
    except:
        print '微博发布过程遇到错误！'
        mark = False

    # 保存微博
    try:
        save_mark = save_to_xnr_flow_text(tweet_type,uid,text)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark

def save_to_tweet_timing_list(task_detail):

    item_detail = dict()

    item_detail['uid'] = task_detail['uid']
    item_detail['user_no'] = task_detail['user_no']
    item_detail['task_source'] = task_detail['task_source']
    item_detail['operate_type'] = task_detail['operate_type']
    item_detail['create_time'] = task_detail['create_time']
    item_detail['post_time'] = task_detail['post_time']
    item_detail['text'] = task_detail['text']
    item_detail['task_status'] = task_detail['task_status']
    item_detail['remark'] = task_detail['remark']
    item_detail['task_status'] = 0 # 0-尚未发送，1-已发送


    task_id = task_detail['uid'] + '_'+ str(task_detail['post_time'])
    # task_id: uid_提交时间_发帖时间

    try:
        es.index(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id,body=item_detail)
        mark = True
    except:
        mark = False

    return mark

## 日常发帖@用户推荐

def get_recommend_at_user(xnr_user_no):
	#_id  = user_no2_id(user_no)
	es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	
	if es_result:
		uid = es_result['uid']
		daily_interests = es_result['daily_interests']
	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name = flow_text_index_name_pre + datetime
	nest_query_list = []
	daily_interests_list = daily_interests.split('&')
	'''
	## daily_interests 字段为多个值
	for interest in daily_interests_list:
		nest_query_list.append({'wildcard':{'daily_interests':'*'+interest+'*'}})


	es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
						body={'query':{'bool':{'must':nest_query_list}},'size':DAILY_INTEREST_TOP_USER,\
						'sort':{'user_fansnum':{'order':'desc'}}})['hits']['hits']
	'''
	## daily_interests 字段为单个值
	query_body = {
		'query':{
			'filtered':{
				'filter':{
					'terms':{'daily_interests':daily_interests_list}
				}
			}
		}
	}

	es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
						body=query_body)['hits']['hits']

	if not es_results:
		if S_TYPE != 'test':
			es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
								body={'query':{'match_all':{}},'size':DAILY_INTEREST_TOP_USER,\
								'sort':{'user_fansnum':{'order':'desc'}}})['hits']['hits']
		else:
			es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
								body={'query':{'match_all':{}},'size':1000,\
								'sort':{'user_fansnum':{'order':'desc'}}})['hits']['hits']

	uid_list = []
	if es_results:
		for result in es_results:
			result = result['_source']
			uid_list.append(result['uid'])

	## 根据uid，从weibo_user中得到 nick_name
	uid_nick_name_dict = dict()  # uid不会变，而nick_name可能会变
	es_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':uid_list})['docs']
	i = 0
	for result in es_results:
		if result['found'] == True:
			result = result['_source']
			uid = result['uid']
			nick_name = result['nick_name']
			if nick_name:
				i += 1
				uid_nick_name_dict[uid] = nick_name
		if i >= DAILY_AT_RECOMMEND_USER_TOP:
			break

	return uid_nick_name_dict

def get_daily_recommend_tweets(theme,sort_item):
	query_body = {
		'query':{
			'filtered':{
				'filter':{
					'term':{'daily_interests':theme}
				}
			}
		},
		'sort':{sort_item:{'order':'desc'}},
		'size':TOP_WEIBOS_LIMIT
	}

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name = flow_text_index_name_pre + datetime

	es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

	if not es_results:
		es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
								body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
								'sort':{sort_item:{'order':'desc'}}})['hits']['hits']
	return es_results

def get_hot_sensitive_recommend_at_user(sort_item):

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name = flow_text_index_name_pre + datetime

	query_body = {
		'query':{
			'match_all':{}
		},
		'sort':{sort_item:{'order':'desc'}},
		'size':HOT_EVENT_TOP_USER,
		'_source':['uid','user_fansnum','retweeted']
	}

	if sort_item == 'retweeted':
		sort_item_2 = 'timestamp'
	else:
		sort_item_2 = 'retweeted'

	es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
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
	es_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':uid_list})['docs']
	i = 0
	for result in es_results:
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

def get_hot_recommend_tweets(topic_field,sort_item):
	query_body = {
		'query':{
			'filtered':{
				'filter':{
					'term':{'topic_field':topic_field}
				}
			}
		},
		'sort':{sort_item:{'order':'desc'}},
		'size':TOP_WEIBOS_LIMIT
	}


	es_results = es.search(index=social_sensing_index_name,doc_type=social_sensing_index_type,body=query_body)['hits']['hits']
	print 'aaa'
	if not es_results:
		print 'bbb'
		es_results = es.search(index=social_sensing_index_name,doc_type=social_sensing_index_type,\
								body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
								'sort':{sort_item:{'order':'desc'}}})['hits']['hits']
	return es_results

def get_hot_content_recommend(task_id):

	es_task = es.get(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id)['_source']
	if es_task:
		if es_task['compute_status'] != 1:
			return '正在计算'
	else:

		es_result = es.get(index=weibo_hot_content_recommend_results_index_name,doc_type=weibo_hot_content_recommend_results_index_type,\
							id=task_id)['_source']

		if es_result:
			contents = json.loads(es_result['content_recommend'])

		return contents

def get_hot_subopinion(task_id):

	es_task = es.get(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id)['_source']
	if es_task:
		if es_task['compute_status'] != 2:
			return '正在计算'
	else:
		es_result = es.get(index=weibo_hot_subopinion_results_index_name,doc_type=weibo_hot_subopinion_results_index_type,\
							id=task_id)['_source']

		if es_result:
			contents = json.loads(es_result['subopinion_weibo'])
		if S_TYPE == 'test':
			return []
		else:
			return contents

def get_tweets_from_flow(sort_item_new):

	query_body = {
		'query':{
			'match_all':{}
		},
		'sort':{sort_item_new:{'order':'desc'}},
		'size':TOP_WEIBOS_LIMIT
	}

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name = flow_text_index_name_pre + datetime

	es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

	if not es_results:
		es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
								body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
								'sort':{sort_item:{'order':'desc'}}})['hits']['hits']
	return es_results

def uid_lists2weibo_from_flow_text(uid_list):

	query_body = {
		'query':{
			'filtered':{
				'filter':{
					'terms':{'uid':uid_list}
				}
			}
		},
		'size':TOP_WEIBOS_LIMIT
	}

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE)	
	else:
		now_ts = int(time.time())
	datetime = ts2datetime(now_ts-24*3600)

	index_name_flow = flow_text_index_name_pre + datetime

	es_results = es_flow_text.search(index=index_name_flow,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

	return es_results

def get_tweets_from_bci(sort_item_new):

	if S_TYPE == 'test':
		now_ts = datetime2ts(S_DATE_BCI)	
	else:
		now_ts = int(time.time())

	datetime = ts2datetime(now_ts-24*3600)
	datetime_new = datetime[0:4]+datetime[5:7]+datetime[8:10]

	index_name = weibo_bci_index_name_pre + datetime_new

	query_body = {
		'query':{
			'match_all':{}
		},
		'sort':{sort_item_new:{'order':'desc'}},
		'size':BCI_USER_NUMBER
	}

	es_results_bci = es_user_portrait.search(index=index_name,doc_type=weibo_bci_index_type,body=query_body)['hits']['hits']

	uid_set = set()

	if es_results_bci:
		for result in es_results_bci:
			uid = result['_id']
			uid_set.add(uid)
	uid_list = list(uid_set)

	es_results = uid_lists2weibo_from_flow_text(uid_list)

	return es_results

def get_tweets_from_user_portrait(sort_item_new):

	query_body = {
		'query':{
			'match_all':{}
		},
		'sort':{sort_item_new:{'order':'desc'}},
		'size':USER_POETRAIT_NUMBER
	}

	es_results_portrait = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,body=query_body)['hits']['hits']

	uid_set = set()

	if es_results_portrait:
		for result in es_results_portrait:
			result = result['_source']
			uid = result['uid']
			uid_set.add(uid)
	uid_list = list(uid_set)

	es_results = uid_lists2weibo_from_flow_text(uid_list)
	
	return es_results

def get_bussiness_recomment_tweets(sort_item):
	print 'sort_item::',sort_item
	#sort_item_new = ''
	if sort_item == 'retweeted':
		sort_item_new = 'retweeted'
		es_results = get_tweets_from_flow(sort_item_new)
	elif sort_item == 'sensitive_info':
		sort_item_new = 'sensitive'
		es_results = get_tweets_from_flow(sort_item_new)
	elif sort_item == 'sensitive_user':
		sort_item_new = 'user_index'
		es_results = get_tweets_from_bci(sort_item_new)
	elif sort_item == 'influence_info':
		sort_item_new = 'retweeted'
		es_results = get_tweets_from_flow(sort_item_new)
	elif sort_item == 'influence_user':
		sort_item_new = 'influence'
		es_results = get_tweets_from_user_portrait(sort_item_new)

	return es_results

'''
社交反馈
'''

def get_show_comment():
	return []

def get_reply_comment():
	return []

def get_show_retweet():
	return[]

def get_reply_retweet():
	return []

def get_show_private():
	return []

def get_reply_private():
	return []

def get_show_at():
	return []

def get_reply_at():
	return []

def get_show_follow():
	return []

def get_reply_follow():
	return []







