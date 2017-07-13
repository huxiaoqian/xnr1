#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import domain_create_task,get_domain_info,get_role_info,get_role_sort_list,\
                get_role2feature_info,get_recommend_step_two,get_recommend_follows


mod = Blueprint('weibo_xnr_create', __name__, url_prefix='/weibo_xnr_create')

# 根据虚拟人推荐角色顺序
@mod.route('/domain2role/')  
def ajax_domain2role():
    domain_name = request.args.get('domain_name','')
    role_sort_list = get_role_sort_list(domain_name)

    return json.dumps(role_sort_list)

#根据选定角色推荐政治倾向和心理状态
@mod.route('/role2feature_info/')
def ajax_role2feature_info():
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    feature_filter_dict = get_role2feature_info(domain_name,role_name)
    return json.dumps(feature_filter_dict)

#根据第一步选择推荐第二步信息
@mod.route('/recommend_step_two/')
def ajax_recommend_step_two():
    task_detail = dict()
    task_detail['domain_name'] = request.args.get('domain_name','')
    task_detail['role_name'] = request.args.get('role_name','')
    task_detail['daily_interests'] = request.args.get('daily_interests','') # 提交的日常兴趣，以中文逗号分隔“，”
    #task_detail['monitor_keywords'] = request.args.get('monitor_keywords','')  # 提交的关键词，以中文逗号分隔“，”
    recommend_results = get_recommend_step_two(task_detail)
    return json.dumps(recommend_results)

#第三步绑定账户关注用户推荐
@mod.route('/recommend_follows/')
def ajax_recommend_followers():
    task_detail = dict()
    task_detail['daily_interests'] = request.args.get('daily_interests','') # 提交的日常兴趣，以中文逗号分隔“，”
    task_detail['monitor_keywords'] = request.args.get('monitor_keywords','')  # 提交的关键词，以中文逗号分隔“，”

    recommend_results = get_recommend_follows(task_detail)
    return json.dumps(recommend_results)

@mod.route('/show_register_info/')
def ajax_show_register_info():
    
    return json.dumps(results)

@mod.route('/save_register_info/')
def ajax_save_register_info():

    return json.dumps(results)

@mod.route('/bind_info/')
def ajax_bind_indo():

    return json.dumps(results)
