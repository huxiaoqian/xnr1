# -*-coding:utf-8-*-

import json
import time
from xnr.global_utils import es_xnr as es 
from xnr.global_utils import es_flow_text,es_user_portrait,es_user_profile,weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
						weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
						weibo_feedback_private_index_name,weibo_feedback_private_index_type,\
						weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
						weibo_feedback_like_index_name,weibo_feedback_like_index_type,\
						weibo_feedback_fans_index_name,weibo_feedback_fans_index_type,\
						weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
						weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
						flow_text_index_type,weibo_bci_index_name_pre,weibo_bci_index_type 

from xnr.utils import xnr_user_no2uid
from xnr.global_config import S_TYPE,S_DATE,S_UID,S_DATE_BCI
from xnr.time_utils import ts2datetime,datetime2ts
from xnr.parameter import WEEK,DAY,MAX_SEARCH_SIZE

def compute_growth_rate_total(day8_dict,total8_dict):
	total_dict = {}
	for timestamp, num in day8_dict.iteritems():
		total_timestamp = timestamp - DAY
		day_num = day8_dict[timestamp]
		try:
			total_num_lastday = total8_dict[total_timestamp]
			if not total_num_lastday:
				total_num_lastday = 1
			total_dict['growth_rate'][timestamp] = float(day_num)/total_num_lastday
			total_dict['day_num'][timestamp] = day8_dict[timestamp]
			total_dict['total_num'][timestamp] = total8_dict[timestamp]
		except:
			continue

	return total_dict

# 影响力粉丝数
def get_influ_fans_num(xnr_user_no):
	
	fans_num_day = {}  # 每天增量统计
	fans_num_total = {} # 截止到当天总量统计

	uid = xnr_user_no2uid(xnr_user_no)

	if xnr_user_no:
		if S_TYPE == 'test':
			es_results = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
								body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
			current_time = es_results[0]['_source']['timestamp']
		
		else:
			current_time = time.time()
	
		current_date = ts2datetime(current_time)
		current_time_new = datetime2ts(current_date)

		# 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
		es_update_result = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
								body={'query':{'match_all':{}}})['hits']['hits']
		update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK+1): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'update_time':update_time}},
							{'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
						]
					}
				}
			}

			query_body_total = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'update_time':update_time}},
							{'range':{'timestamp':{'lt':end_ts}}}
						]
					}
				}
			}

			es_day_count_result = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
							body=query_body_day,request_timeout=999999)
			print 'es_day_count_result::',es_day_count_result
			if es_day_count_result['_shards']['successful'] != 0:
				es_day_count = es_day_count_result['count']
			else:
				return 'es_day_count_found_error'
			
			es_total_count_result = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
							body=query_body_total,request_timeout=999999)

			if es_total_count_result['_shards']['successful'] != 0:
				es_total_count = es_total_count_result['count']
			else:
				return 'es_total_count_found_error'

			fans_num_day[start_ts] = es_day_count
			fans_num_total[start_ts] = es_total_count
			print 'fans_num_day::',fans_num_day
			print 'fans_num_total::',fans_num_total

		total_dict = compute_growth_rate_total(fans_num_day,fans_num_total)
		print 'total_dict::',total_dict
		return total_dict
	else:
		return ''

'''
# 影响力 粉丝的粉丝数
def get_influ_fans_fans_num(xnr_user_no):
	if S_TYPE == 'test':
		uid = S_UID
		current_time = datetime2ts(S_DATE)
	else:
		uid = xnr_user_no2uid(xnr_user_no)
		current_time = int(time.time())
	
	fans_follow_es_result = es.search(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_name,\
		id=xnr_user_no)['_source']
	fans_list = fans_follow_es_result['fans_list']

	index_name_list = get_flow_text_index_list(current_time)
	index_name_list = index_name_list.reverse()
	i = 0
	for index_name in index_name_list:
		es_flow_results = es_flow_text.mget(index=index_name,doc_type=flow_text_index_type,body={'uids':fans_list})['docs']
		for result in es_flow_results:
			if not result['found']:
				while True:
				current_time_second = datetime2ts(index_name)
				index_name_list_second = get_flow_text_index_list(current_time_second)

	return []
'''

def get_influ_retweeted_num(xnr_user_no):

	retweeted_num_day = {}  # 每天增量统计
	retweeted_num_total = {} # 截止到当天总量统计

	uid = xnr_user_no2uid(xnr_user_no)

	if xnr_user_no:
		if S_TYPE == 'test':
			es_results = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
								body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
			current_time = es_results[0]['_source']['timestamp']
		else:
			current_time = time.time()
	
		current_date = ts2datetime(current_time)
		current_time_new = datetime2ts(current_date)

		# 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
		#es_update_result = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
		#						body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		#update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY 

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
						]
					}
				}
			}

			query_body_total = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'range':{'timestamp':{'lt':end_ts}}}
						]
					}
				}
			}

			es_day_count = es.count(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			retweeted_num_day[start_ts] = es_day_count
			retweeted_num_total[start_ts] = es_total_count

		total_dict = compute_growth_rate_total(retweeted_num_day,retweeted_num_total)

		return total_dict
	else:
		return ''


def get_influ_commented_num(xnr_user_no):
	# 收到的评论 comment_type : receive
	commented_num_day = {}  # 每天增量统计
	commented_num_total = {} # 截止到当天总量统计

	uid = xnr_user_no2uid(xnr_user_no)

	if xnr_user_no:
		if S_TYPE == 'test':
			es_results = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
								body={'query':{'term':{'comment_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
			current_time = es_results[0]['_source']['timestamp']
		else:
			current_time = time.time()
	
		current_date = ts2datetime(current_time)
		current_time_new = datetime2ts(current_date)

		# 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
		#es_update_result = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
		#						body={'query':{'term':{'comment_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		#update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY 

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'comment_type':'receive'}},
							{'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
						]
					}
				}
			}

			query_body_total = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'comment_type':'receive'}},
							{'range':{'timestamp':{'lt':end_ts}}}
						]
					}
				}
			}

			es_day_count = es.count(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			commented_num_day[start_ts] = es_day_count
			commented_num_total[start_ts] = es_total_count

		total_dict = compute_growth_rate_total(commented_num_day,commented_num_total)

		return total_dict
	else:
		return ''


def get_influ_like_num(xnr_user_no):

	like_num_dict = {}
	like_num_day = {}  # 每天增量统计
	like_num_total = {} # 截止到当天总量统计

	uid = xnr_user_no2uid(xnr_user_no)

	if xnr_user_no:
		if S_TYPE == 'test':
			es_results = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
								body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
			current_time = es_results[0]['_source']['timestamp']
		else:
			current_time = time.time()
	
		current_date = ts2datetime(current_time)
		current_time_new = datetime2ts(current_date)

		# 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
		#es_update_result = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
		#						body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		#update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY 

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
						]
					}
				}
			}

			query_body_total = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'range':{'timestamp':{'lt':end_ts}}}
						]
					}
				}
			}

			es_day_count = es.count(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			like_num_day[start_ts] = es_day_count
			like_num_total[start_ts] = es_total_count

		total_dict = compute_growth_rate_total(like_num_day,like_num_total)

		return total_dict
	else:
		return ''


def get_influ_at_num(xnr_user_no):

	at_num_dict = {}
	at_num_day = {}  # 每天增量统计
	at_num_total = {} # 截止到当天总量统计

	uid = xnr_user_no2uid(xnr_user_no)

	if xnr_user_no:
		if S_TYPE == 'test':
			es_results = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
								body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
			current_time = es_results[0]['_source']['timestamp']
		else:
			current_time = time.time()
	
		current_date = ts2datetime(current_time)
		current_time_new = datetime2ts(current_date)

		# 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
		#es_update_result = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
		#						body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		#update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY 

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
						]
					}
				}
			}

			query_body_total = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'range':{'timestamp':{'lt':end_ts}}}
						]
					}
				}
			}

			es_day_count = es.count(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			at_num_day[start_ts] = es_day_count
			at_num_total[start_ts] = es_total_count

		total_dict = compute_growth_rate_total(at_num_day,at_num_total)

		return total_dict
	else:
		return ''


def get_influ_private_num(xnr_user_no):
	# 收到的私信 private_type : receive
	private_num_dict = {}
	private_num_day = {}  # 每天增量统计
	private_num_total = {} # 截止到当天总量统计

	uid = xnr_user_no2uid(xnr_user_no)

	if xnr_user_no:
		if S_TYPE == 'test':
			es_results = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
								body={'query':{'term':{'private_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
			current_time = es_results[0]['_source']['timestamp']
		else:
			current_time = time.time()
	
		current_date = ts2datetime(current_time)
		current_time_new = datetime2ts(current_date)

		# 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
		#es_update_result = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
		#						body={'query':{'term':{'private_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		#update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY 

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'private_type':'receive'}},
							{'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
						]
					}
				}
			}

			query_body_total = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'private_type':'receive'}},
							{'range':{'timestamp':{'lt':end_ts}}}
						]
					}
				}
			}

			es_day_count = es.count(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			private_num_day[start_ts] = es_day_count
			private_num_total[start_ts] = es_total_count

		total_dict = compute_growth_rate_total(private_num_day,private_num_total)

		return total_dict
	else:
		return ''

def compute_influence_num(xnr_user_no):

	uid = xnr_user_no2uid(xnr_user_no)


	if S_TYPE == 'test':
		current_time = datetime2ts(S_DATE_BCI)
		uid = S_UID
	else:
		current_time = int(time.time()) - DAY

	datetime = ts2datetime(current_time)
	new_datetime = datetime[0:4]+datetime[5:7]+datetime[8:10]
	index_name = weibo_bci_index_name_pre + new_datetime
	try:
		
		bci_xnr = es_user_portrait.get(index=index_name,doc_type=weibo_bci_index_type,id=uid)['_source']['user_index']

		bci_max = es_user_portrait.search(index=index_name,doc_type=weibo_bci_index_type,body=\
			{'query':{'match_all':{}},'sort':{'user_index':{'order':'desc'}}})['hits']['hits'][0]['_source']['user_index']

		influence = float(bci_xnr)/bci_max*100
		influence = round(influence,2)  # 保留两位小数
	except:
		influence = 0

	return influence











