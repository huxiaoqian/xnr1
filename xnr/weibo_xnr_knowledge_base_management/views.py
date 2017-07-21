# -*-coding:utf-8-*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import get_create_sensitive_words,show_sensitive_words_default,show_sensitive_words_rank,delete_sensitive_words,show_select_sensitive_words,change_sensitive_words,\
                  get_create_date_remind,show_date_remind,show_select_date_remind,change_date_remind,delete_date_remind,\
                  get_create_hidden_expression,show_hidden_expression,show_select_hidden_expression,change_hidden_expression,delete_hidden_expression

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
#添加敏感词
@mod.route('/create_sensitive_words/')
def ajax_create_sensitive_words():
    rank = request.args.get('rank','')
    sensitive_words = request.args.get('sensitive_words','')
    sensitive_words_string = '&'.join(sensitive_words.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())
    mark = get_create_sensitive_words(rank,sensitive_words_string,create_type,create_time)

    return json.dumps(mark)

#默认显示敏感词列表
@mod.route('/show_sensitive_words_default/')
def ajax_show_sensitive_words_default():
    results=show_sensitive_words_default()
    return json.dumps(results)

#按等级显示敏感词列表
@mod.route('/show_sensitive_words_rank/')
def ajax_show_sensitive_words_rank():
    rank_value=request.args.get('rank_value','')
    results=show_sensitive_words_rank(rank_value)
    return json.dumps(results)

#删除指定敏感词
@mod.route('/delete_sensitive_words/')
def ajax_delete_sensitive_words():
    words_id=request.args.get('words_id','')
    results=delete_sensitive_words(words_id)
    return json.dumps(results)


#修改指定敏感词
#显示指定修改的敏感词信息
@mod.route('/show_select_sensitive_words/')
def ajax_show_select_sensitive_words():
    words_id=request.args.get('words_id','')
    results=show_select_sensitive_words(words_id)
    return json.dumps(results)

#对指定敏感词进行修改
@mod.route('/change_sensitive_words/')
def ajax_change_sensitive_words():
    words_id=request.args.get('words_id','')
    rank=request.args.get('rank','')
    sensitive_words=request.args.get('sensitive_words','')
    create_type=request.args.get('create_type','')
    create_time=request.args.get('create_time','')
    change_info=[rank,sensitive_words,create_type,create_time]
    results=change_sensitive_words(words_id,change_info)
    return json.dumps(results)

## 时间节点预警
#添加时间节点预警
@mod.route('/create_date_remind/')
def ajax_create_date_remind():
    timestamp = request.args.get('timestamp','')
    keywords = request.args.get('keywords','')
    keywords_string = '&'.join(keywords.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())
    
    mark = get_create_date_remind(timestamp,keywords_string,create_type,create_time)

    return json.dumps(mark)

#显示时间节点预警列表
@mod.route('/show_date_remind/')
def ajax_show_date_remind():
    results=show_date_remind()
    return json.dumps(results)


#显示指定的时间节点内容，用于修改
@mod.route('/show_select_date_remind/')
def ajax_show_select_date_remind():
    task_id=request.args.get('task_id','')
    results=show_select_date_remind(task_id)
    return json.dumps(results)

#修改指定的时间节点预警内容
@mod.route('/change_date_remind/')
def ajax_change_date_remind():
    task_id=request.args.get('task_id','')
    date_time=request.args.get('date_time','')
    keywords=request.args.get('keywords','')
    create_type=request.args.get('create_type','')
    create_time=request.args.get('create_time','')
    change_info=[date_time,keywords,create_type,create_time]
    results=change_date_remind(task_id,change_info)
    return json.dumps(results)


#删除指定的时间节点预警内容
@mod.route('/delete_date_remind/')
def ajax_delete_date_remind():
    task_id=request.args.get('task_id','')
    results=delete_date_remind(task_id)
    return json.dumps(results)



## 隐喻式表达
#添加隐喻式表达
@mod.route('/create_hidden_expression/')
def ajax_create_hidden_expression():
    origin_word = request.args.get('origin_word','')
    evolution_words = request.args.get('evolution_words','')
    evolution_words_string = '&'.join(evolution_words.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())

    mark = get_create_hidden_expression(origin_word,evolution_words_string,create_type,create_time)

    return json.dumps(mark)

#显示隐喻式表达列表
@mod.route('/show_hidden_expression/')
def ajax_show_hidden_expression():
    results=show_hidden_expression()
    return json.dumps(results)


#显示指定的隐喻式表达，用于修改
@mod.route('/show_select_hidden_expression/')
def ajax_show_select_hidden_expression():
    express_id=request.args.get('express_id','')
    results=show_select_hidden_expression(express_id)
    return json.dumps(results)

#修改指定的隐喻式表达内容
@mod.route('/change_hidden_expression/')
def ajax_change_hidden_expression():
    express_id=request.args.get('express_id','')
    origin_word=request.args.get('origin_word','')
    evolution_words_string=request.args.get('evolution_words_string','')
    create_type=request.args.get('create_type','')
    create_time=request.args.get('create_time','')
    change_info=[origin_word,evolution_words_string,create_type,create_time]
    results=change_hidden_expression(express_id,change_info)
    return json.dumps(results)

#删除指定的隐喻式表达内容
@mod.route('/delete_hidden_expression/')
def ajax_delete_hidden_expression():
    express_id=request.args.get('express_id','')
    results=delete_hidden_expression(express_id)
    return json.dumps(results)