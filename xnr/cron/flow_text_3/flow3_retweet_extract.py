# -*-coding:utf-8-*-

import IP
import re
import csv
import sys
import zmq
import time
import json
import math
import redis
from elasticsearch.helpers import scan
from save_attribute import save_retweet
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime,datetime2ts
from global_utils import es_xnr as es
from global_utils import R_CLUSTER_FLOW2 as r_cluster,twitter_flow_text_index_name_pre,\
						twitter_flow_text_index_type,facebook_flow_text_index_name_pre,\
						facebook_flow_text_index_type
from global_utils import es_xnr as es,R_UNAME2ID_FT, fb_uname2id, tw_uname2id

def uname2uid(uname,ft_type):
	uid = R_UNAME2ID_FT.hget(ft_type,uname)
	if not uid:
		uid = uname

	return uid

def get_fb_retweet_network(item):

	uid = item['uid']
	text = item['text']
	timestamp = item['timestamp']
	#text = 'Retweeted 秀才江湖 (@xiucai1911): 周小平和袁腾飞，一个不懂历史不学无术'

	if isinstance(text, str):
		text = text.decode('utf-8', 'ignore')

	if text.startswith('Retweeted '):
		#text = 'Retweeted iyouport (@iyouport_news): #AmericaChina 美国商务部周二表示'
		#RE = re.compile(u'Retweeted ([0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+) ', re.UNICODE)
		#RE2 = re.compile(u' (@[0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
		RE2 = re.compile('.*@(.*)\).*', re.UNICODE)
		
		#repost_chains = RE.findall(text)
		repost_chains2 = RE2.findall(text)
		
		if repost_chains2 != []:
			root_uname = repost_chains2[0]
			root_uid = uname2uid(root_uname,ft_type=fb_uname2id)
	elif ' shared ' in text:
		res = text.split(' shared ')
		root_con = res[1]
		if "'s" in root_con:
			root_uname = root_con.split("'s")[0]
			root_uid = uname2uid(root_uname,ft_type=fb_uname2id)
		else:
			root_uname = ''
			root_uid = ''		
	else:
		root_uname = ''
		root_uid = ''

	# if direct_uid == '':
	# 	direct_uid = root_uid
	print 'root_uid...',root_uid

	if root_uid:
		save_retweet(uid, root_uid, timestamp,'fb')


def get_tw_retweet_network(item):

	uid = item['uid']
	text = item['text']
	timestamp = item['timestamp']

	if isinstance(text, str):
		text = text.decode('utf-8', 'ignore')

	if text.startswith('RT '):
		try:
			root_uname = text.split('RT @')[1].split(':')[0]
			root_uid = uname2uid(root_uname,ft_type=tw_uname2id)
		except:
			root_uname = ''
			root_uid = ''

	else:
		root_uname = ''
		root_uid = ''

	print 'root_uid...',root_uid

	if root_uid:
		save_retweet(uid, root_uid, timestamp,'tw')

if __name__ == '__main__':

	#ft_list = ['ft', 'tw']
	ft_list = ['tw']

	for ft_item in ft_list:
		if ft_item == 'fb':
			index_name_pre = facebook_flow_text_index_name_pre
			index_type = facebook_flow_text_index_type
			get_retweet_network_func = get_fb_retweet_network
		else:
			index_name_pre = twitter_flow_text_index_name_pre
			index_type = twitter_flow_text_index_type
			get_retweet_network_func = get_tw_retweet_network

	read_count = 0

	
	start_date = '2017-09-10'
	end_date = '2017-10-25'
	#end_date = '2017-09-11'

	start_ts = datetime2ts(start_date)
	end_ts = datetime2ts(end_date)

	days_num = (end_ts - start_ts)/(24*3600)+1

	for i in range(days_num):
		current_time = start_ts + i*24*3600
		current_date = ts2datetime(current_time)
		index_name = index_name_pre + current_date
		print 'index......',index_name
		query_body = {
			'query':{
				'match_all':{}
			}
		}

		es_scan_results = scan(es,query=query_body,size=1000,index=index_name,\
			doc_type=index_type)

		while 1:
			try:
				read_count += 1
				
				scan_data = es_scan_results.next()
				item = scan_data['_source']

				#text = item['text']

				get_retweet_network_func(item)

				if read_count % 1000 == 0:
					print read_count

			except StopIteration:
				print 'over!!!!'
				break