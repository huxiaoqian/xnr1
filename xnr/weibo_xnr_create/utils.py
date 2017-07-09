#-*- coding: utf-8 -*-

'''
use to save function to create xnr info
'''
import pinyin
import json
import time
import os


import sys
reload(sys)
sys.path.append('../')

from global_config import S_TYPE,S_DATE_2
from global_utils import r,weibo_target_domain_detect_queue_name,weibo_domain_index_name,weibo_domain_index_type
from global_utils import es_xnr as es
from parameters import topic_en2ch_dict,domain_ch2en_dict

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
	domain_name = '乌镇' #'维权群体'
	#create_type = {'by_keywords':['维权','律师'],'by_seed_users':[],'by_all_users':[]}
	create_type = {'by_keywords':['互联网','乌镇'],'by_seed_users':[],'by_all_users':[]}
	create_time = time.time()
	submitter = 'admin@qq.com'
	remark = '这是备注'
	domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0)



