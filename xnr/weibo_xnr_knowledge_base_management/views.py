# -*-coding:utf-8-*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import get_create_sensitive_words,get_create_date_remind,get_create_hidden_expression

mod = Blueprint('weibo_xnr_knowledge_base_management', __name__, url_prefix='/weibo_xnr_knowledge_base_management')

#根据
@mod.route('/create_weibo_xnr/')
def ajax_create_weibo_xnr():
    
    domain_name =  request.args.get('domain_name','')
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    domain_info = get_domain_info(domain_pinyin)
    
    return json.dumps(domain_info)

@mod.route('/show_role_info/')
def ajax_show_role_info():
    domain_name = request.args.get('domain_name','')
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_name = request.args.get('role_name','')
    role_info = get_role_info(domain_pinyin,role_name)

    return json.dumps(role_info)

'''
业务知识库管理
'''
## 敏感词管理
@mod.route('/create_sensitive_words/')
def ajax_create_sensitive_words():
    rank = request.args.get('rank','')
    sensitive_words = request.args.get('sensitive_words','')
    sensitive_words_string = '&'.join(sensitive_words.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())
    mark = get_create_sensitive_words(rank,sensitive_words_string,create_type,create_time)

    return json.dumps(mark)

## 时间节点预警
@mod.route('/create_date_remind/')
def ajax_create_date_remind():
    timestamp = request.args.get('timestamp','')
    keywords = request.args.get('keywords','')
    keywords_string = '&'.join(keywords.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())
    
    mark = get_create_date_remind(timestamp,keywords_string,create_type,create_time)

    return json.dumps(mark)

## 隐喻式表达
@mod.route('/create_hidden_expression/')
def ajax_create_hidden_expression():
    origin_word = request.args.get('origin_word','')
    evolution_words = request.args.get('evolution_words','')
    evolution_words_string = '&'.join(evolution_words.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())

    mark = get_create_hidden_expression(origin_word,evolution_words_string,create_type,create_time)

    return json.dumps(mark)