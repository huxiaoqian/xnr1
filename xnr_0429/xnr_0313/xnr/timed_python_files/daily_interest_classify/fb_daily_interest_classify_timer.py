# -*-coding:utf-8-*-

import time
import os
import json
from collections import Counter
from daily_classifier import triple_classifier_new

import sys
sys.path.append('../')

from fb_xnr_flow_text_mappings import fb_daily_inerests_flow_text_mappings


sys.path.append('../../')

from global_utils import es_xnr, facebook_flow_text_index_name_pre, facebook_flow_text_index_type,\
					fb_daily_interest_index_name_pre,fb_daily_interest_index_type
from global_config import S_TYPE, S_DATE_FB

from time_utils import ts2datetime,datetime2ts

def read_flow_text(flow_text_index_name,current_date):
	
	#flow_text_index_name = facebook_flow_text_index_name_pre + current_date

	i = 0
	
	label_count_dict = {}
	content_dict = {}

	print '!!!'


	while True:
		
		query_body = {
			'query':{
				'bool':{
					'must':[
						
						{'term':{'sensitive':0}}
					]
				}
			},
			'size':1000,
			'from':i*1000
		}

		# 原创、sensitive为0
		#print '222'
		search_results = es_xnr.search(index=flow_text_index_name,doc_type=facebook_flow_text_index_type,\
				body=query_body)['hits']['hits']

		weibo_list = []
		
		for result in search_results:
			result = result['_source']
			weibo_list.append(result['text'].encode('utf-8'))

		label_list = triple_classifier_new(weibo_list)

		label_count = Counter(label_list)
		#print '333'
		for j in range(len(search_results)):
			
			label = label_list[j]

			try:
				if label_count_dict[label] < 20:
					content_dict[label].append(search_results[j]['_source'])
					label_count_dict[label] += 1

			except:
				content_dict[label] = [search_results[j]['_source']]

				label_count_dict[label] = 1

		i += 1

		if i % 1000 == 0:
			print 'i...',i
			print 'label_count_dict...',label_count_dict

		# 循环终止条件
		min_label_count = min(label_count_dict, key=label_count_dict.get)
		if label_count_dict[min_label_count] >= 20:
			break
	print 'label_count_dict::',label_count_dict

	for content_label,content_weibo in content_dict.iteritems():
		_id = content_label
		index_name = fb_daily_interest_index_name_pre +'_'+ current_date
		fb_daily_inerests_flow_text_mappings(index_name)
		item_dict = {}
		item_dict['timestamp'] = datetime2ts(current_date)
		item_dict['content'] = json.dumps(content_weibo)
		print es_xnr.index(index=index_name,doc_type=fb_daily_interest_index_type,id=_id,body=item_dict)
	
		print content_label,'====',len(content_weibo)



if __name__ == '__main__':

	current_date = S_DATE_FB 
	#current_time = datetime2ts(current_date)
	#current_date_last_day = ts2datetime(current_time-24*3600)
	flow_text_index_name = facebook_flow_text_index_name_pre + current_date
	#flow_text_index_name_list = ['flow_text_2016-11-20']
	t1 = time.time()
	print 'flow_text_index_name...',flow_text_index_name

	read_flow_text(flow_text_index_name,current_date)
	t2 = time.time()

	during = t2-t1

	print 'during:::',during

# facebook_flow_text_2017-10-25
# facebook_flow_text_2017-10-25








