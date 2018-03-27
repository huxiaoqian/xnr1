# -*-coding:utf-8-*-

import time
import os
import json
from collections import Counter
from daily_classifier import triple_classifier_new
 
import sys
sys.path.append('../../')

from global_utils import es_xnr,es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
					daily_interest_index_name_pre,daily_interest_index_type
from global_config import S_TYPE, S_DATE
from weibo_xnr_flow_text_mappings import daily_inerests_flow_text_mappings
from time_utils import ts2datetime,datetime2ts

def read_flow_text(flow_text_index_name,current_date):
	
	#flow_text_index_name = flow_text_index_name_pre + current_date

	i = 0
	
	label_count_dict = {}
	content_dict = {}

	while True:
		
		query_body = {
			'query':{
				'bool':{
					'must':[
						{'term':{'message_type':1}},
						{'term':{'sensitive':0}}
					]
				}
			},
			'size':1000,
			'from':i*1000,
			'sort':{'user_fansnum':{'order':'desc'}}
		}
		# 原创、sensitive为0
		search_results = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
				body=query_body)['hits']['hits']

		weibo_list = []
		
		for result in search_results:
			result = result['_source']
			weibo_list.append(result['text'].encode('utf-8'))

		label_list = triple_classifier_new(weibo_list)

		label_count = Counter(label_list)

		for j in range(len(search_results)):
			
			label = label_list[j]
			search_results[j]['_source']['label'] = label
			try:
				if label_count_dict[label] < 20:
					content_dict[label].append(search_results[j]['_source'])
					label_count_dict[label] += 1

			except:
				content_dict[label] = [search_results[j]['_source']]

				label_count_dict[label] = 1

		i += 1

		print 'i..',i

		# 循环终止条件
		min_label_count = min(label_count_dict, key=label_count_dict.get)
		if label_count_dict[min_label_count] >= 20:
			break
	print 'label_count_dict::',label_count_dict

	for content_label,content_weibo in content_dict.iteritems():
		#_id = content_label
		current_date_new = ts2datetime(datetime2ts(current_date)+24*3600)
		index_name = daily_interest_index_name_pre +'_'+ current_date_new
		daily_inerests_flow_text_mappings(index_name)
		#item_dict = {}
		#item_dict['timestamp'] = datetime2ts(current_date)
		#item_dict['content'] = json.dumps(content_weibo)
		for daily_weibo in content_weibo:
			mid = daily_weibo['mid']
			print es_xnr.index(index=index_name,doc_type=daily_interest_index_type,id=mid,body=daily_weibo)
		
		print content_label,'====',len(content_weibo)



if __name__ == '__main__':

	if S_TYPE == 'test':

		current_date = S_DATE 
	else:
		current_time = int(time.time()-24*3600)
		current_date = ts2datetime(current_time)

	#current_time = datetime2ts(current_date)
	#current_date_last_day = ts2datetime(current_time-24*3600)
	flow_text_index_name = flow_text_index_name_pre + current_date
	#flow_text_index_name_list = ['flow_text_2016-11-20']
	t1 = time.time()
	read_flow_text(flow_text_index_name,current_date)
	t2 = time.time()

	during = t2-t1

	print 'during:::',during










