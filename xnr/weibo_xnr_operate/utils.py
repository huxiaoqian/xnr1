#-*- coding:utf-8 -*-
import os
import time
import json
import sys

#reload(sys)
#sys.path.append('../../')
from xnr.global_utils import es_xnr as es
from xnr.global_utils import weibo_hot_keyword_task_index_name,weibo_hot_keyword_task_index_type

def push_keywords_task(task_detail):

	print 'task_detail::',task_detail

	try:
		task_id = task_detail['task_id']
		keywords_string = '&'.join(task_detail['keywords_string'].encode('utf-8').split('，'))
		task_detail['keywords_string'] = keywords_string
		es.index(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
				id=task_id,body=task_detail)
		mark = True
	except:
		mark = False

	return mark

