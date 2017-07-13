#-*- coding: utf-8 -*-

'''
use to save function to create xnr info
'''
import pinyin
import json
import time
import os

from xnr.global_config import S_TYPE,S_DATE
from xnr.global_utils import r,weibo_target_domain_detect_queue_name,weibo_domain_index_name,weibo_domain_index_type,\
								weibo_role_index_name,weibo_role_index_type
from xnr.global_utils import es_xnr as es
from xnr.parameter import topic_en2ch_dict,domain_ch2en_dict,domain_en2ch_dict

'''
import sys
reload(sys)
sys.path.append('../')
from global_config import S_TYPE,S_DATE
from global_utils import r,weibo_target_domain_detect_queue_name,weibo_domain_index_name,weibo_domain_index_type,\
								weibo_role_index_name,weibo_role_index_type
from global_utils import es_xnr as es
from parameter import topic_en2ch_dict,domain_ch2en_dict,domain_en2ch_dict
'''
def get_role_sort_list(domain_name):
	domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
	try:
		es_result = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=domain_pinyin)['_source']

		role_sort_list_en = json.loads(es_result['role_distribute'])
		role_sort_list_zh = []
		for item in role_sort_list_en:
			role_zh = domain_en2ch_dict[item[0]]
			role_sort_list_zh.append(role_zh)

		return role_sort_list_zh
	except:
		return []

def get_role2feature_info(domain_name,role_name):
	domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
	role_name_en = domain_ch2en_dict[role_name]
	_id = domain_pinyin + '_' + role_name_en
	try:
		es_result = es.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=_id)['_source']

		feature_info_dict = es_result
		return feature_info_dict

	except:
		return []

def get_domain_info(domain_pinyin):

	domain_info = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=domain_pinyin)['_source']

	return domain_info

def get_role_info(domain_pinyin,role_name):

	role_en = domain_ch2en_dict(role_name)

	role_info_id = domain_pinyin + '_' + role_en

	role_info = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=role_info_id)['_source']

	return role_info


def domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0):
	domain_task_dict = dict()
	if S_TYPE == 'test':
		domain_task_dict['domain_pinyin'] = pinyin.get(domain_name,format='strip',delimiter='_')
		domain_task_dict['domain_name'] = domain_name
		domain_task_dict['create_type'] = json.dumps(create_type)
		domain_task_dict['create_time'] = create_time
		domain_task_dict['submitter'] = submitter
		domain_task_dict['remark'] = remark
		domain_task_dict['compute_status'] = compute_status
	r.lpush(weibo_target_domain_detect_queue_name,json.dumps(domain_task_dict))
	#r.delete(weibo_target_domain_detect_queue_name)
	print 'success!'

if __name__ == '__main__':
	domain_name =  '维权群体'
	#domain_name =  '乌镇'
	create_type = {'by_keywords':['维权','律师'],'by_seed_users':[],'by_all_users':[]}
	#create_type = {'by_keywords':['互联网','乌镇'],'by_seed_users':[],'by_all_users':[]}
	create_time = time.time()
	submitter = 'admin@qq.com'
	remark = '这是备注'
	domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0)



