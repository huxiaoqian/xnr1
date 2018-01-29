#!/usr/bin/env python
#encoding: utf-8

import json
import elasticsearch
from elasticsearch import Elasticsearch
import sys
sys.path.append('../')
from timed_python_files.facebook_feedback_mappings_timer import *

class Es_fb():
	def __init__(self):
		self.es = Elasticsearch('219.224.134.213:9205',timeout=600)

	def ts2datetime(self, ts):
		return time.strftime('%Y-%m-%d', time.localtime(ts))

	def executeES(self, indexName, typeName, data_list):
		for list_data in data_list:

				if indexName == 'facebook_feedback_friends':
					es.index(index=indexName, doc_type=typeName, id=list_data['uid'], body=list_data)

				elif indexName == 'facebook_feedback_retweet':
					date_time = self.ts2datetime(list_data['timestamp'])
					indexName_date = indexName + '_' + date_time

					mappings_func = facebook_feedback_retweet_mappings
					mappings_func(date_time)
					es.index(index=indexName_date, doc_type=typeName, body=list_data)

				elif indexName == 'facebook_feedback_at':
					date_time = self.ts2datetime(list_data['timestamp'])
					indexName_date = indexName + '_' + date_time

					mappings_func = facebook_feedback_at_mappings
					mappings_func(date_time)
					es.index(index=indexName_date, doc_type=typeName, body=list_data)

				elif indexName == 'facebook_feedback_like':
					date_time = self.ts2datetime(list_data['timestamp'])
					indexName_date = indexName + '_' + date_time

					mappings_func = facebook_feedback_like_mappings
					mappings_func(date_time)
					es.index(index=indexName_date, doc_type=typeName, body=list_data)

				elif indexName == 'facebook_feedback_private':
					date_time = self.ts2datetime(list_data['timestamp'])
					indexName_date = indexName + '_' + date_time

					mappings_func = facebook_feedback_private_mappings
					mappings_func(date_time)
					es.index(index=indexName_date, doc_type=typeName, body=list_data)

				elif indexName == 'facebook_feedback_comment':
					date_time = self.ts2datetime(list_data['timestamp'])
					indexName_date = indexName + '_' + date_time

					mappings_func = facebook_feedback_comment_mappings
					mappings_func(date_time)
					es.index(index=indexName_date, doc_type=typeName, body=list_data)







