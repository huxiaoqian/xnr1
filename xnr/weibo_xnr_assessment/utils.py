# -*-coding:utf-8-*-

import json
import time
from xnr.global_utils import es_xnr as es 
from xnr.global_utils import weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
						weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
						weibo_feedback_private_index_name,weibo_feedback_private_index_type,\
						weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
						weibo_feedback_like_index_name,weibo_feedback_like_index_type,\
						weibo_feedback_fans_index_name,weibo_feedback_fans_index_type,\
						weibo_feedback_follow_index_name,weibo_feedback_follow_index_type
from xnr.utils import xnr_user_no2uid
from xnr.global_config import S_TYPE
from xnr.time_utils import ts2datetime,datetime2ts
from xnr.parameter import WEEK,DAY,MAX_SEARCH_SIZE

# 影响力粉丝数
def get_influ_fans_num(xnr_user_no):
	
	fans_num_dict = {}
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
								body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
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

			es_day_count = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			fans_num_day[start_ts] = es_day_count
			fans_num_total[start_ts] = es_total_count

		fans_num_dict['fans_num_day'] = fans_num_day
		fans_num_dict['fans_num_total'] = fans_num_total

		return fans_num_dict
	else:
		return ''

# 影响力 粉丝的粉丝数
def get_influ_fans_fans_num(xnr_user_no):
	return []


def get_influ_retweeted_num(xnr_user_no):

	retweeted_num_dict = {}
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
		es_update_result = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
								body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
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

			es_day_count = es.count(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			retweeted_num_day[start_ts] = es_day_count
			retweeted_num_total[start_ts] = es_total_count

		retweeted_num_dict['retweeted_num_day'] = retweeted_num_day
		retweeted_num_dict['retweeted_num_total'] = retweeted_num_total

		return retweeted_num_dict
	else:
		return ''


def get_influ_commented_num(xnr_user_no):
	# 收到的评论 comment_type : receive
	commented_num_dict = {}
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
		es_update_result = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
								body={'query':{'term':{'comment_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY 

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'comment_type':'receive'}},
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
							{'term':{'comment_type':'receive'}},
							{'term':{'update_time':update_time}},
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

		commented_num_dict['commented_num_day'] = commented_num_day
		commented_num_dict['commented_num_total'] = commented_num_total

		return commented_num_dict
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
		es_update_result = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
								body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
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

			es_day_count = es.count(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			like_num_day[start_ts] = es_day_count
			like_num_total[start_ts] = es_total_count

		like_num_dict['like_num_day'] = like_num_day
		like_num_dict['like_num_total'] = like_num_total

		return like_num_dict
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
		es_update_result = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
								body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
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

			es_day_count = es.count(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
							body=query_body_day,request_timeout=999999)['_shards']['total']

			es_total_count = es.count(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
							body=query_body_total,request_timeout=999999)['_shards']['total']

			at_num_day[start_ts] = es_day_count
			at_num_total[start_ts] = es_total_count

		at_num_dict['at_num_day'] = at_num_day
		at_num_dict['at_num_total'] = at_num_total

		return at_num_dict
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
		es_update_result = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
								body={'query':{'term':{'private_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
		update_time = es_update_result[0]['_source']['update_time']

		for i in range(WEEK): # WEEK=7
			start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
			end_ts = current_time_new - i*DAY 

			query_body_day = {
				'query':{
					'bool':{
						'must':[
							{'term':{'root_uid':uid}},
							{'term':{'private_type':'receive'}},
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
							{'term':{'private_type':'receive'}},
							{'term':{'update_time':update_time}},
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

		private_num_dict['private_num_day'] = private_num_day
		private_num_dict['private_num_total'] = private_num_total

		return private_num_dict
	else:
		return ''