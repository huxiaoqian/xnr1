# -*-coding:utf-8-*-
import os
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import 

'''
领域知识库
1.创建
2.查询展示
'''

### 渗透领域创建方式

### 根据关键词


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
        task_information_string = r_group.rpop(group_detect_queue_name)
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
		


