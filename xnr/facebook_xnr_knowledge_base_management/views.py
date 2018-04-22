# -*-coding:utf-8-*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from utils import get_generate_example_model, get_show_example_model, get_export_example_model, \
                    get_create_type_content, domain_create_task, get_show_domain_group_summary, \
                    get_show_domain_group_detail_portrait, get_show_domain_description, \
                    get_show_domain_role_info, get_delete_domain,show_different_corpus,delete_corpus

mod = Blueprint('fb_xnr_knowledge_base_management', __name__, url_prefix='/fb_xnr_knowledge_base_management')

## 生成实例模板
@mod.route('/generate_example_model/')
def ajax_generate_example_model():
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    results = get_generate_example_model(domain_name,role_name)
    return json.dumps(results)

## 导出实例模板
@mod.route('/show_example_model/')
def ajax_show_example_model():
    results = get_show_example_model()
    return json.dumps(results)

@mod.route('/export_example_model/')
def ajax_export_example_model():
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    results = get_export_example_model(domain_name,role_name)
    return json.dumps(results)

## 创建领域
@mod.route('/create_domain/')
def ajax_create_domain():
    domain_name = request.args.get('domain_name','')
    create_type = request.args.get('create_type','')  # 按关键词--by_keywords  按种子用户--by_seed_users  按所有用户--by_all_users 
    keywords_string = request.args.get('keywords_string','')  # 按关键词方式，以中文逗号“，”分割。若是不是按关键词，则不传递此参数
    seed_users = request.args.get('seed_users','')  # 按种子用户方式，不同uid之间以中文逗号“，”分隔
    all_users = request.args.get('all_users','')  #按所有用户方式，传递所有uid
    create_type_new = get_create_type_content(create_type,keywords_string,seed_users,all_users)
    create_time = int(time.time())
    submitter = request.args.get('submitter','admin@qq.com')
    description = request.args.get('description','')
    remark = request.args.get('remark','')
    mark = domain_create_task(domain_name,create_type_new,create_time,submitter,description,remark)
    return json.dumps(mark)  # True False

## 展示群体摘要信息
@mod.route('/show_domain_group_summary/')
def ajax_show_domain_group_summary():
    submitter = request.args.get('submitter','admin@qq.com')
    results = get_show_domain_group_summary(submitter)
    return json.dumps(results)

## 展示群体详细画像信息
@mod.route('/show_domain_group_detail_portrait/')
def ajax_show_domain_group_detail_portrait():
    domain_name = request.args.get('domain_name','')
    results = get_show_domain_group_detail_portrait(domain_name)
    return json.dumps(results)

## 展示群体描述
@mod.route('/show_domain_description/')
def ajax_show_domain_description():
    domain_name = request.args.get('domain_name','')
    results = get_show_domain_description(domain_name)
    return json.dumps(results)

## 展示角色
@mod.route('/show_domain_role_info/')
def ajax_show_domain_role_info():
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    results = get_show_domain_role_info(domain_name,role_name)
    return json.dumps(results)

## 删除领域
@mod.route('/delete_domain/')
def ajax_delete_domain():
    domain_name = request.args.get('domain_name','')
    mark = get_delete_domain(domain_name)
    return json.dumps(mark)

#######################################################
#言论知识库
#######################################################
@mod.route('/show_different_corpus/')
def ajax_show_different_corpus():
    task_detail = dict()
    task_detail['create_type'] = request.args.get('create_type','') #my_xnrs,all_xnrs
    task_detail['corpus_status'] = int(request.args.get('corpus_status',''))    #如果是初始进入为0，其他为1
    task_detail['request_type'] = request.args.get('request_type','') #all,one
    task_detail['theme_type_1'] = request.args.get('theme_type_1','').split(',')
    task_detail['theme_type_2'] = request.args.get('theme_type_2','').split(',')
    task_detail['theme_type_3'] = request.args.get('theme_type_3','').split(',')
    results = show_different_corpus(task_detail)
    return json.dumps(results)

#显示语料库
@mod.route('/show_corpus_class/')
def ajax_show_corpus_class():
    create_type=request.args.get('create_type','')
    corpus_type=request.args.get('corpus_type','')
    results=show_corpus_class(create_type,corpus_type)
    return json.dumps(results)

#删除指定语料
@mod.route('/delete_corpus/')
def ajax_delete_corpus():
    corpus_id=request.args.get('corpus_id','')
    results=delete_corpus(corpus_id)
    return json.dumps(results)