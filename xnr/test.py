#-*- coding:utf-8 -*-
import os
import time
import json
import sys

from global_utils import es_xnr as es
from global_utils import weibo_xnr_index_name,weibo_xnr_index_type


if __name__ == '__main__':
	'''
	item = dict()
	item['create_status'] = 1
	item['monitor_keywords'] = u'维权，律师'
	item['political_side'] = u'中立'
	item['daily_interests'] = u'旅游，美食'
	item['psy_feature'] = u'积极，中立，悲伤'
	item['domain_name'] = u'维权群体'
	item['role_name'] = u'政府机构及人士'
	item['user_no'] = 1
	item['business_goal'] = u'扩大影响，渗透'
	item['user_no'] = u''
	item['user_no'] = 1
	item['user_no'] = 1
	item['user_no'] = 1
	'''
	es.update(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id='WXNR0001',body={'doc':{'uid':1447849855}})
	
	#es.delete(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id='WXNR0001')
	#es.delete(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id='WXNR0002')
	#es.delete(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id='WXNR0003')
