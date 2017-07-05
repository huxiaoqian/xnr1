# -*-coding:utf-8-*-
import os
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from global_utils import r,weibo_target_domain_detect_queue_name,weibo_target_domain_analysis_queue_name


from save_utils import save_domain

'''
领域知识库计算

'''

## 渗透群体发现
# input: 领域名称
# output: 渗透群体uids

def get_create_type(domain_pinyin):


def target_domain_detect(domain_pinyin):


### 渗透领域创建方式

### 根据关键词
def detect_by_keywords(keywords):


### 根据种子用户
#use to get single user portrait attribute
#input: seed_user_dict
#output: user_portriat_dict
def get_single_user_portrait(seed_user_dict):
    if 'uid' in seed_user_dict:
        uid = seed_user_dict['uid']
        try:
            user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
        except:
            user_portrait_result = {}
    else:
        uname = seed_user_dict['uname']
        query = {'term':{'uname': uname}}
        try:
            user_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type ,\
                    body={'query':{'bool':{'must': quuery}}})['_source']
        except:
            user_portrait_result = {}

    return user_portrait_result

### 根据上传uid文件
def 

#use to get detect information from redis queue
#input: NULL
#output: task_information_dict (from redis queue---gruop_detect_task)
def get_detect_information():
    task_information_dict = {}
    try:
        task_information_string = r.rpop(weibo_target_domain_detect_queue_name)
    except:
        task_information_string = ''
    #test
    #r_group.rpush(group_detect_queue_name, task_information_string)
    if task_information_string:
        task_information_dict = json.loads(task_information_string)
    else:
        task_information_dict = {}

    return task_information_dict


def compute_domain_base():
	results = {}
	while True:
		decect_task_information = get_detect_information()
        if decect_task_information != {}:
            task_id = decect_task_information['domain_pinyin']
            print 'step:start detect task'
    		create_type = decect_task_information['create_type']
            ## create_type ----- {'按关键词''by_keywords':[],'按种子用户''by_seed_users':[],'按所有用户''by_all_users':[]}
            if create_type['by_keywords']:
                keywords = create_type['by_keywords']
                detect_results = detect_by_keywords(keywords)
            elif create_type['by_seed_users']:
                seed_users = create_type['by_seed_users']
                detect_results = detect_by_seed_users(seed_users)
            elif create_type['by_all_users']:
                all_users = create_type['by_all_users']
                detect_results = detect_by_all_users(all_users)

            if detect_results != 'task not exist':
                mark = save_detect_results(detect_results)





