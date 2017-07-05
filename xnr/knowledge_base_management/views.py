# -*-coding:utf-8-*-
import os
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import 

'''
领域知识库
1.创建
2.查询展示
'''

### 创建方式

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

