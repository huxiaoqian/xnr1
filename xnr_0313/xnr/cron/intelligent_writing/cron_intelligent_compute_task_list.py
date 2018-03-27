# -*-coding:utf-8-*-

import os
import json
import time

from cron_intelligent_compute import rpop_compute_intelligent_writing

import sys
reload(sys)
sys.path.append('../../')

from global_utils import es_xnr as es
from global_utils import R_WRITING as r_r
from global_utils import writing_task_index_name, writing_task_index_type, writing_task_queue_name

def lpush_intelligent_writing_task_list():

	compute_status = 0
	es_results = es.search(index=writing_task_index_name,doc_type=writing_task_index_type,\
							body={'query':{'term':{'compute_status':compute_status}}})['hits']['hits']

	# es_results = es.search(index=writing_task_index_name,doc_type=writing_task_index_type,\
	# 						body={'query':{'match_all':{}}})['hits']['hits']


	print 'es_results:::',es_results
	count = 0
	if es_results:
		for item in es_results:
			
			item = item['_source']
			task_dict = {}
			task_dict['task_source'] = item['task_source']
			task_dict['xnr_user_no'] = item['xnr_user_no']
			task_dict['task_id'] = item['task_id']
			task_dict['event_keywords'] = item['event_keywords']
			task_dict['opinion_keywords'] = item['opinion_keywords']
			task_dict['opinion_type'] = item['opinion_type']
			task_dict['create_time'] = item['create_time']
			task_dict['task_name'] = item['task_name']
			task_dict['task_name_pinyin'] = item['task_name_pinyin']

			r_r.lpush(writing_task_queue_name,json.dumps(task_dict))
			count += 1
			print '开始把任务push到队列中......'


if __name__ == '__main__':

	lpush_intelligent_writing_task_list()
	start_ts = int(time.time())
	rpop_compute_intelligent_writing()
	end_ts = int(time.time())
	print 'time..cost..',end_ts - start_ts
