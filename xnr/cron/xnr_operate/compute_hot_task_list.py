# -*-coding:utf-8-*-

import os
import json
import time

from cron_compute_hot import rpop_compute_recommend_subopnion

import sys
reload(sys)
sys.path.append('../../')

from global_utils import es_xnr as es
from global_utils import R_RECOMMEND_SUBOPINION_KEYWORD_TASK as r
from global_utils import weibo_hot_keyword_task_index_name,weibo_hot_keyword_task_index_type,\
						weibo_recommend_subopinion_keywords_task_queue_name

def lpush_recommend_subopinion_keyword_task_list():

	es_results = es.search(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
							body={'query':{'match_all':{}}})['hits']['hits']

	if es_results:
		for item in es_results:
			item = item['_source']
			task_dict = {}
			task_dict['task_id'] = item['task_id']
			task_dict['keywords_string'] = item['keywords_string']
			r.lpush(weibo_recommend_subopinion_keywords_task_queue_name,json.dumps(task_dict))

			print '开始把任务push到队列中......'



if __name__ == '__main__':

	lpush_recommend_subopinion_keyword_task_list()
	rpop_compute_recommend_subopnion()
