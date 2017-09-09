#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
use to caculate_history information
'''
import os
import time
import datetime
import json
from xnr.global_utils import es_xnr,weibo_xnr_index_name,weibo_xnr_index_type

#统计信息表
def weibo_xnr_history_info_count(xnr_user_no,now_time)

def wxnr_history_count(xnr_user_no,startdate,enddate):
	if startdate=='' and enddate=='':
		now_time=int(time.time())
		weibo_xnr_flow_text_listname=get_xnr_feedback_index_listname(xnr_flow_text_index_name_pre,now_time)
		#print weibo_xnr_flow_text_listname
	else:
		weibo_xnr_flow_text_listname=get_timeset_indexset_list(xnr_flow_text_index_name_pre,startdate,enddate)
		#print weibo_xnr_flow_text_listname

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'xnr_user_no':xnr_user_no}
				}
			}
		},
		'aggs':{
			'all_task_source':{
				'terms':{
					'field':'task_source'
				}
			}
		}
	}
	xnr_user_info=[]
	for index_name in weibo_xnr_flow_text_listname:
		xnr_user_detail=dict()
		#时间
		xnr_user_detail['date_time']=index_name[-10:]
		try:			
			xnr_result=es_xnr.search(index=index_name,doc_type=xnr_flow_text_index_type,body=query_body)
			#今日总粉丝数
			for item in xnr_result['hits']['hits']:
				xnr_user_detail['user_fansnum']=item['_source']['user_fansnum']
			# daily_post-日常发帖,hot_post-热点跟随,business_post-业务发帖
			for item in xnr_result['aggregations']['all_task_source']['buckets']:
				if item['key'] == 'daily_post':
					xnr_user_detail['daily_post_num']=item['doc_count']
				elif item['key'] == 'business_post':
					xnr_user_detail['business_post_num']=item['doc_count']
				elif item['key'] == 'hot_post':
					xnr_user_detail['hot_follower_num']=item['doc_count']
			#总发帖量
			xnr_user_detail['total_post_sum']=xnr_user_detail['daily_post_num']+xnr_user_detail['business_post_num']+xnr_user_detail['hot_follower_num']

			#查找影响力、渗透力、安全性
			xnr_assess_id=xnr_user_no+xnr_user_detail['date_time']
			xnr_assess_result=es_xnr.get(index=weibo_xnr_assessment_index_name,doc_type=weibo_xnr_assessment_index_type,id=xnr_assess_id)['_source']
			xnr_user_detail['influence']=xnr_assess_result['influence']
			xnr_user_detail['penetration']=xnr_assess_result['penetration']
			xnr_user_detail['safe']=xnr_assess_result['safe']

		except:
			xnr_user_detail['total_post_sum']=0
			xnr_user_detail['influence']=0
			xnr_user_detail['penetration']=0
			xnr_user_detail['safe']=0
		xnr_user_info.append(xnr_user_detail)
	
	#对xnr_user_info进行排序
	xnr_user_info.sort(key=lambda k:(k.get('date_time',0)),reverse=True)
	
	#累计统计
	Cumulative_statistics_dict=dict()
	if xnr_user_no:		
		Cumulative_statistics_dict['date_time']='累计统计'
		Cumulative_statistics_dict['user_fansnum']=xnr_user_info[0]['user_fansnum']
		total_post_sum=0
		daily_post_num=0
		business_post_num=0
		hot_follower_num=0
		influence_sum=0
		penetration_sum=0
		safe_sum=0
		number=len(xnr_user_info)
		for item in xnr_user_info:
			total_post_sum=total_post_sum+item['total_post_sum']
			daily_post_num=daily_post_num+item['daily_post_num']
			business_post_num=business_post_num+item['business_post_num']
			hot_follower_num=hot_follower_num+item['hot_follower_num']
			influence_sum=influence_sum+item['influence']
			penetration_sum=penetration_sum+item['penetration']
			safe_sum=safe_sum+item['safe']

		Cumulative_statistics_dict['total_post_sum']=total_post_sum
		Cumulative_statistics_dict['daily_post_num']=daily_post_num
		Cumulative_statistics_dict['business_post_num']=business_post_num
		Cumulative_statistics_dict['hot_follower_num']=hot_follower_num
		Cumulative_statistics_dict['influence']=influence_sum/number
		Cumulative_statistics_dict['penetration']=penetration_sum/number
		Cumulative_statistics_dict['safe']=safe_sum/number
	else:
		Cumulative_statistics_dict=dict()
	return Cumulative_statistics_dict,xnr_user_info