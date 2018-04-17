#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver
import tweepy
from tweepy import OAuthHandler
import requests
import time
from pyvirtualdisplay import Display
from launcher import Launcher
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import random
import sys
sys.path.append('../')
from timed_python_files import new_tw_xnr_flow_text_mappings as mapping

endDate = '2017-10-25'
dateList = []
for i in range(0,11):
	date = datetime.strptime(endDate,"%Y-%m-%d") - timedelta(days=i)
	dateList.append(datetime.strftime(date,"%Y-%m-%d"))

es = Elasticsearch([{'host':'219.224.134.213','port':9205}])
# 获取已创建xnr的数据
xnrData = []
query_body = {
		"query":
		{
			"match": {
				"create_status": 2
			}
		}
}
res = es.search(index='tw_xnr', doc_type='user', body=query_body, request_timeout=100)
hits = res['hits']['hits']
for each in hits:
	if each['_source']['create_status'] == 2:
		xnrData.append(each['_source'])

for xnr in xnrData:
	# 连接api
	auth = OAuthHandler(xnr['consumer_key'], xnr['consumer_secret'])
	auth.set_access_token(xnr['access_token'], xnr['access_secret'])
	api = tweepy.API(auth)

	for num in range(1,101):
		if not api.user_timeline(page=num):
			break
		for each in api.user_timeline(page=num):
			xnr_user_no = xnr['xnr_user_no']
			uid = xnr['uid']
			text = each.text
			try:
				picture_url = each.entities['media'][0]['media_url_https']
				vedio_url = each.entities['media'][0]['media_url_https']
			except:
				picture_url = None
				vedio_url = None
			user_fansnum = each.author._json['followers_count']
			user_followersum = each.author._json['friends_count']
			weibos_sum = each.author._json['statuses_count']
			tid = each.id
			ip = None
			timestampStr = datetime.strftime(each.created_at,"%Y-%m-%d")
			#timestamp = int(time.mktime(time.strptime(timestampStr,"%Y-%m-%d")))
			timestamp = int(time.mktime(time.strptime(dateList[random.randint(1,10)],"%Y-%m-%d")))
			geo = each.geo
			retweeted = each.retweet_count
			like = each.favorite_count
			comment = None

			if each.is_quote_status:
				message_type = 2
			elif each.in_reply_to_status_id:
				message_type = 3
			else:
				message_type = 1
			if message_type == 1:
				directed_uid = None
				directed_uname = None
				root_uid = None
				root_tid = None
				origin_text = None
			elif message_type == 2:
				try:
					directed_uid = each.quoted_status['user']['id']
					directed_uname = each.quoted_status['user']['name']
					if each.quoted_status['is_quote_status']:
						root_uid = None
						root_tid = each.quoted_status['quoted_status_id']
						origin_text = None
					else:
						root_uid = each.quoted_status['user']['id']
						root_tid = each.quoted_status['id']
						origin_text = each.quoted_status['text']
				except:
					directed_uid = each.retweeted_status._json['quoted_status']['user']['id']
					directed_uname = each.retweeted_status._json['quoted_status']['user']['name']
					if each.retweeted_status._json['quoted_status']['is_quote_status']:
						root_uid = None
						root_tid = each.retweeted_status._json['quoted_status']['quoted_status_id']
						origin_text = None
					else:
						directed_uid = each.retweeted_status._json['quoted_status']['user']['id']
						directed_uname = each.retweeted_status._json['quoted_status']['user']['name']
						origin_text = each.retweeted_status._json['quoted_status']['text']

			elif message_type == 3:
				directed_uid = each.in_reply_to_user_id
				try:
					directed_uname = each.entities['user_mentions'][0]['name']
				except:
					directed_uname = None
				root_uid = each.in_reply_to_user_id
				root_tid = None
				origin_text = None
		

			dict = {"xnr_user_no":xnr_user_no, "uid":uid, "text":text,\
					 "picture_url":picture_url, "vedio_url":vedio_url,\
					  "user_fansnum":user_fansnum, "user_followersum":user_followersum,\
					   "weibos_sum":weibos_sum, "tid":tid, "ip":ip, "timestamp":timestamp,\
					    "geo":geo, "retweeted":retweeted, "like":like, "comment":comment,\
					     "message_type":message_type, "directed_uid":directed_uid,\
					      "directed_uname":directed_uname, "root_uid":root_uid, "root_tid":root_tid,\
					       "origin_text":origin_text}
			print(dict)

			index_name = mapping.new_tw_xnr_flow_text_index_name_pre + time.strftime("%Y-%m-%d",time.localtime(dict['timestamp']))
			mapping.new_tw_xnr_flow_text_mappings(index_name)
			time.sleep(2)
			es.index(index=index_name, doc_type=mapping.new_tw_xnr_flow_text_index_type, id=dict['tid'], body=dict)



















