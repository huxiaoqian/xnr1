# -*-coding:utf-8-*-

import sys
import time
import json
import math
from elasticsearch.helpers import scan
from fb_tw_bci_mappings import tw_bci_mappings,fb_bci_mappings
sys.path.append('../')
from global_config import S_DATE_FB,S_TYPE
from global_utils import es_xnr as es,facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
								facebook_count_index_name_pre,facebook_count_index_type,\
								facebook_user_index_name,facebook_user_index_type,\
								facebook_feedback_friends_index_name,facebook_feedback_friends_index_type,\
								fb_bci_index_name_pre,fb_bci_index_type
from parameter import DAY
from time_utils import ts2datetime,datetime2ts

def influence_active(uid,index_name):
	query_body = {
		'query':{
			'term':{'uid':uid}
		}
	}
	
	#index_name = facebook_flow_text_index_name_pre + ts2datetime(current_time)

	es_count = es.count(index=index_name,doc_type=facebook_flow_text_index_type,body=query_body)

	if es_count['_shards']['successful'] != 0:
		active_num = es_count['count']
	else:
		active_num = 0

	return active_num

def influence_propagate(fid,index_name):
	query_body = {
		'query':{
			'term':{'fid':fid}
		},
		'sort':{'update_time':{'order':'desc'}}
	}
	#index_name = facebook_flow_text_index_name_pre + ts2datetime(current_time)
	search_results = es.search(index=index_name,doc_type=facebook_count_index_type,\
		body=query_body)['hits']['hits']

	if not search_results:
		propagate_num = 0
	else:
		result = search_results[0]['_source']
		share = result['share']
		comment = result['comment']
		favorite = result['favorite']

		propagate_num = 5*share + 3*comment + 2*favorite

	return propagate_num
		
def influence_cover(uid,current_time):
	#index_name = facebook_feedback_friends_index_name
	# 没有列表
	
	try:
		es_search = es.get(index=facebook_user_index_name,doc_type=facebook_user_index_type,\
						id=uid)['_source']
		try:
			likes = es_search['likes']
		except:
			likes = 0

		try:
			talking_about_count = es_search['talking_about_count']
		except:
			talking_about_count = 0

		cover_num = likes + talking_about_count
		if not cover_num:
			cover_num = 1

	except:
		cover_num = 1   # 取log之后为0

	return cover_num

def influence_trust(uid):

	try:
		es_search = es.get(index=facebook_user_index_name,doc_type=facebook_user_index_type,\
						id=uid)['_source']
		
		if 'category' in es_search:
			influence_trust = 1
		
		else:
			influence_trust = 0

	except:
		influence_trust = 0

	return influence_trust


def influence_cal_fb(current_time):

	# if S_TYPE == 'test' :
	# 	current_time = datetime2ts(S_DATE_FB)

	current_date = ts2datetime(current_time)
	current_time = datetime2ts(current_date)
	
	flow_text_index_name = facebook_flow_text_index_name_pre + current_date
	count_index_name = facebook_count_index_name_pre + current_date
	fb_bci_index_name = fb_bci_index_name_pre + current_date

	fb_bci_mappings(fb_bci_index_name)

	uid_fid_dict = {}
	bulk_action = []

	# 找出要计算活跃的uids -- 流数据
	query_body_text = {
		'query':{
			'match_all':{}
		}
	}

	es_scan_result = scan(es,index=flow_text_index_name,doc_type=facebook_flow_text_index_type,\
							query=query_body_text,size=1000)
	#print 'es_scan_result...',es_scan_result
	while 1:
		try:
			scan_data = es_scan_result.next()
			item = scan_data['_source']
			uid = item['uid']
			fid = item['fid']

			try:
				uid_fid_dict[uid].append(fid)
			except:
				uid_fid_dict[uid] = [fid]

		except StopIteration:
			break

	# 
	query_body_count = {
		'query':{
			'match_all':{}
		}
	}

	es_scan_result_count = scan(es,index=count_index_name,doc_type=facebook_count_index_type,\
							size=1000,query=query_body_count)

	while 1:
		try:
			scan_data_count = es_scan_result_count.next()
			item = scan_data_count['_source']
			fid = item['fid']
			uid = item['uid']
			try:
				if fid in uid_fid_dict[uid]:
					continue
				else:
					uid_fid_dict[uid].append(fid)
			except:
				uid_fid_dict[uid] = [fid]

		except StopIteration:
			break

	count  = 0

	
	for uid, fid_list in uid_fid_dict.iteritems():

		# 活跃度 -- 每天活跃数
		active_num = influence_active(uid,flow_text_index_name)
		#active_num = len(fid_list)

		# 传播力 -- 每天收到反馈数
		propagate_num_sum = 1
		for fid in fid_list:
			propagate_num = influence_propagate(fid,count_index_name)
			propagate_num_sum += propagate_num

		# 覆盖度 -- 活跃粉丝数
		cover_num = influence_cover(uid,flow_text_index_name)

		# 可信度 -- category（团体组织）是否为空，不为空则1，为空则0。
		trust_num = influence_trust(uid)
		# print 'propagate_num_sum..',propagate_num_sum
		# print 'cover_num..',cover_num
		
		influence_mark = (active_num + math.log10(propagate_num_sum) + math.log10(cover_num) + trust_num) * 10

		action = {'index':{'_id':uid}}

		user_items = {}
		user_items['active'] = active_num
		user_items['propagate'] = propagate_num_sum
		user_items['cover'] = cover_num
		user_items['trust'] = trust_num
		user_items['influence'] = influence_mark
		user_items['uid'] = uid
		user_items['timestamp'] = current_time

		bulk_action.extend([action,user_items])

		count += 1

		if count % 1000:
			es.bulk(bulk_action,index=fb_bci_index_name,doc_type=fb_bci_index_type,timeout=400)
			bulk_action = []

	if bulk_action:
		es.bulk(bulk_action,index=fb_bci_index_name,doc_type=fb_bci_index_type,timeout=400)


if __name__ == '__main__':

	current_date_end = '2017-10-25'
	current_date_start = '2017-10-12'

	current_time_st = datetime2ts(current_date_start)
	current_time_ed = datetime2ts(current_date_end)

	day_num = (current_time_ed - current_time_st)/DAY + 1

	for i in range(day_num):
		current_time = current_time_st + i*DAY
		print ts2datetime(current_time)
		influence_cal_fb(current_time)




			



