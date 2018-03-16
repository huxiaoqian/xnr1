# -*- coding:utf-8 -*-

import sys
import json
import time
from elasticsearch.helpers import scan

sys.path.append('../')
from global_utils import es_xnr as es, facebook_flow_text_index_name_pre, facebook_flow_text_index_type,\
						facebook_count_index_name_pre, facebook_count_index_type,\
						twitter_flow_text_index_name_pre, twitter_flow_text_index_type,\
						twitter_count_index_name_pre, twitter_count_index_type
from time_utils import ts2datetime, datetime2ts


def fb_count2flow_text():

	index_name = facebook_count_index_name_pre + '2017-10-12'

	query_body = {
		'query':{
			'match_all':{}
		}
	}

	scan_results = scan(es,index=index_name,doc_type=facebook_count_index_type,query=query_body,size=1000)
	
	count = 0
	t1 = time.time()

	while 1:
		
		try:

			body_dict = {}

			data = scan_results.next()
			item = data['_source']
			body_dict['comment'] = item['comment']
			body_dict['favorite'] = item['favorite']
			body_dict['share'] = item['share']
			
			body_dict['update_time'] = item['update_time']


			start_ts = datetime2ts('2017-10-10')
			end_ts = datetime2ts('2017-10-25')

			day_num = (end_ts - start_ts)/(24*3600) + 1

			count += 1
			if count % 1000 == 0:
				print 'fb..',count
				t2 = time.time()
				
				print 'time cost..',t2-t1
				t1 = t2

			for i in range(day_num):

				timestamp = start_ts + i*24*3600
				date = ts2datetime(timestamp)


				flow_text_index_name = facebook_flow_text_index_name_pre + date

				_id = item['fid']
				try:
					es.update(index=flow_text_index_name,doc_type=facebook_flow_text_index_type,\
					id=_id,body={'doc':body_dict})
					

					# count += 1

					# if count % 1000 == 0:
					# 	print 'fb..',count

				except:
					continue


		except StopIteration:
			break


	
def tw_count2flow_text():

	index_name = twitter_count_index_name_pre + '*'

	query_body = {
		'query':{
			'match_all':{}
		}
	}

	scan_results = scan(es,index=index_name,doc_type=twitter_count_index_type,query=query_body,size=1000)
	
	count = 0

	while 1:
		
		try:

			body_dict = {}

			data = scan_results.next()
			item = data['_source']
			body_dict['comment'] = item['comment']
			body_dict['favorite'] = item['favorite']
			body_dict['share'] = item['share']
			
			body_dict['update_time'] = item['update_time']


			start_ts = datetime2ts('2017-10-10')
			end_ts = datetime2ts('2017-10-25')

			day_num = (end_ts - start_ts)/(24*3600) + 1

			for i in range(day_num):

				timestamp = start_ts + i*24*3600
				date = ts2datetime(timestamp)


				flow_text_index_name = twitter_flow_text_index_name_pre + date

				_id = item['tid']

				try:
					es.update(index=flow_text_index_name,doc_type=twitter_flow_text_index_type,\
					id=_id,body={'doc':body_dict})
					

					count += 1

					if count % 1000 == 0:
						print 'tw..',count

				except:
					continue


		except StopIteration:
			break


def fb_flow_text():

	start_ts = datetime2ts('2017-10-10')
	end_ts = datetime2ts('2017-10-25')

	day_num = (end_ts - start_ts)/(24*3600) + 1

	count = 0

	for i in range(day_num):

		timestamp = start_ts + i*24*3600
		date = ts2datetime(timestamp)

		index_name = facebook_flow_text_index_name_pre + date

		#es.indices.put_mapping(index=index_name, doc_type=facebook_flow_text_index_type, body={"properties": {"share" : {"type": "long"},"comment" : {"type": "long"},"favorite" : {"type": "long"}}})

		print 'index_name..',index_name

		query_body = {
			'query':{
				'match_all':{}
			}
		}

		scan_results = scan(es,index=index_name,doc_type=facebook_flow_text_index_type,query=query_body,size=1000)
		
		bulk_action = []

		while 1:
			
			try:

				body_dict = {}

				data = scan_results.next()
				item = data['_source']
				body_dict['comment'] = 0
				body_dict['favorite'] = 0
				body_dict['share'] = 0
				
				body_dict['update_time'] = item['timestamp']

				#flow_text_index_name = twitter_flow_text_index_name_pre + ts2datetime(item['timestamp'])

				_id = item['fid']

				action={'update':{'_id':_id}}

				bulk_action.extend([action,{'doc':body_dict}])

			
				count += 1

				if count % 100 == 0 :

					print 'fb..',count

					es.bulk(bulk_action,index=index_name,doc_type=facebook_flow_text_index_type,timeout=100)

			except StopIteration:
				break
		
		if bulk_action:

			es.bulk(bulk_action,index=index_name,doc_type=facebook_flow_text_index_type,timeout=100)

	
def tw_flow_text():

	start_ts = datetime2ts('2017-10-10')
	end_ts = datetime2ts('2017-10-25')

	day_num = (end_ts - start_ts)/(24*3600) + 1

	count = 0

	for i in range(day_num):
		timestamp = start_ts + i*24*3600
		date = ts2datetime(timestamp)

		index_name = twitter_flow_text_index_name_pre + date

		query_body = {
			'query':{
				'match_all':{}
			}
		}

		scan_results = scan(es,index=index_name,doc_type=twitter_flow_text_index_type,query=query_body,size=1000)
		
		bulk_action = []

		while 1:
			
			try:

				body_dict = {}

				data = scan_results.next()
				item = data['_source']
				body_dict['comment'] = 0
				body_dict['favorite'] = 0
				body_dict['share'] = 0
				
				body_dict['update_time'] = item['timestamp']

				#flow_text_index_name = twitter_flow_text_index_name_pre + ts2datetime(item['timestamp'])

				_id = item['tid']

				action={'update':{'_id':_id}}

				bulk_action.extend([action,{'doc':body_dict}])

				count += 1

				if count % 100 == 0 :

					print 'tw..',count
					es.bulk(bulk_action,index=index_name,doc_type=twitter_flow_text_index_type,timeout=100)

			except StopIteration:
				break

		if bulk_action:
			es.bulk(bulk_action,index=index_name,doc_type=twitter_flow_text_index_type,timeout=100)

if __name__ == '__main__':

	fb_count2flow_text()
	tw_count2flow_text()
	# fb_flow_text()
	# tw_flow_text()

