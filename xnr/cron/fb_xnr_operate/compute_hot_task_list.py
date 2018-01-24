# -*-coding:utf-8-*-

import os
import json
import time

from cron_compute_hot import rpop_compute_recommend_subopnion

import sys
reload(sys)
sys.path.append('../../')

from global_utils import es_xnr as es
from global_utils import R_RECOMMEND_SUBOPINION_KEYWORD_TASK as r_r
from global_utils import fb_hot_keyword_task_index_name,fb_hot_keyword_task_index_type,\
						fb_recommend_subopinion_keywords_task_queue_name

def lpush_recommend_subopinion_keyword_task_list():

	compute_status = 0
	es_results = es.search(index=fb_hot_keyword_task_index_name,doc_type=fb_hot_keyword_task_index_type,\
							body={'query':{'term':{'compute_status':compute_status}}})['hits']['hits']

	print 'es_results:::',es_results
	count = 0
	if es_results:
		for item in es_results:
			print 'count::::',count
			item = item['_source']
			task_dict = {}
			task_dict['xnr_user_no'] = item['xnr_user_no']
			task_dict['mid'] = item['task_id']
			print 'mid:::',task_dict['mid']
			task_dict['task_id'] = item['xnr_user_no'] + '_' + item['task_id']
			task_dict['keywords_string'] = item['keywords_string']

			r_r.lpush(fb_recommend_subopinion_keywords_task_queue_name,json.dumps(task_dict))
			count += 1
			print '开始把任务push到队列中......'


if __name__ == '__main__':

	lpush_recommend_subopinion_keyword_task_list()
	rpop_compute_recommend_subopnion()
