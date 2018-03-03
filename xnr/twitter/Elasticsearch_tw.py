#!/usr/bin/env python
#encoding: utf-8

import json
import elasticsearch
from elasticsearch import Elasticsearch
import sys
sys.path.append('../')
from timed_python_files.twitter_feedback_mappings_timer import *

class Es_twitter():
	def __init__(self):
		self.es = Elasticsearch('219.224.134.213:9205',timeout=600)

	def ts2datetime(self, ts):
		return time.strftime('%Y-%m-%d', time.localtime(ts))

	def executeES(self,indexName,typeName,data_list):
		for list_data in data_list:

			if indexName == 'twitter_feedback_fans':
				es.index(index=indexName, doc_type=typeName, id=list_data['uid'], body=list_data)


			elif indexName == 'twitter_feedback_follow':
				es.index(index=indexName, doc_type=typeName, id=list_data['uid'], body=list_data)


			elif indexName == 'twitter_feedback_retweet':
				date_time = self.ts2datetime(list_data['timestamp'])
				indexName_date = indexName + '_' + date_time

				mappings_func = twitter_feedback_retweet_mappings
				mappings_func(date_time)
				es.index(index=indexName_date, doc_type=typeName, id=list_data['mid'], body=list_data)


			elif indexName == 'twitter_feedback_at':
				date_time = self.ts2datetime(list_data['timestamp'])
				indexName_date = indexName + '_' + date_time

				mappings_func = twitter_feedback_at_mappings
				mappings_func(date_time)
				es.index(index=indexName_date, doc_type=typeName, id=list_data['mid'], body=list_data)


			elif indexName == 'twitter_feedback_like':
				date_time = self.ts2datetime(list_data['timestamp'])
				indexName_date = indexName + '_' + date_time

				mappings_func = twitter_feedback_like_mappings
				mappings_func(date_time)
				es.index(index=indexName_date, doc_type=typeName, id=list_data['mid'], body=list_data)


			elif indexName == 'twitter_feedback_private':
				date_time = self.ts2datetime(list_data['timestamp'])
				indexName_date = indexName + '_' + date_time

				mappings_func = twitter_feedback_private_mappings
				mappings_func(date_time)
				es.index(index=indexName_date, doc_type=typeName, id=list_data['mid'], body=list_data)











