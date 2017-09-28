#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
import urllib
import urllib2
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import get_domain_info,get_role_info,get_role_sort_list,\
                get_role2feature_info,get_recommend_step_two,get_recommend_follows,\
                get_save_step_one,get_save_step_two,get_save_step_three_1,get_save_step_three_2,\
                get_xnr_info,get_show_domain,get_show_weibo_xnr,get_nick_name_unique,\
                get_add_other_info,get_modify_userinfo
#from weibo_publish_func import getUserShow
from weibo_publish_func import newest_time_func
#from utils import get_user_data
import os
from xnr.global_config import PATH_ROOT

mod = Blueprint('weibo_xnr_create', __name__, url_prefix='/weibo_xnr_create')

# 昵称不能重复
@mod.route('/nick_name_unique/')
def ajax_nick_name_unique():
    nick_name = request.args.get('nick_name','')
    mark = get_nick_name_unique(nick_name)

    return json.dumps(mark)  # True表示 可用，没有重复。False表示 不可用，有冲突。

# 返回渗透领域
@mod.route('/show_domain/')
def ajax_show_domain():
    #xnr_user_no = request.args.get('xnr_user_no','')
    domain_name_dict = get_show_domain()
    return json.dumps(domain_name_dict)

# 返回虚拟人
@mod.route('/show_weibo_xnr/')
def ajax_show_weibo_xnr():
    submitter = request.args.get('submitter','admin@qq.com')
    weibo_xnr_dict = get_show_weibo_xnr(submitter)
    return json.dumps(weibo_xnr_dict)

# 根据虚拟人推荐角色顺序
@mod.route('/domain2role/')  
def ajax_domain2role():
    #xnr_user_no = request.args.get('xnr_user_no','')
    domain_name = request.args.get('domain_name','')
    role_sort_list = get_role_sort_list(domain_name)

    return json.dumps(role_sort_list)

#根据选定角色推荐政治倾向和心理状态
@mod.route('/role2feature_info/')
def ajax_role2feature_info():
    #xnr_user_no = request.args.get('xnr_user_no','')
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    feature_filter_dict = get_role2feature_info(domain_name,role_name)
    return json.dumps(feature_filter_dict)

#根据第一步选择推荐第二步信息
@mod.route('/recommend_step_two/')
def ajax_recommend_step_two():
    task_detail = dict()

    #xnr_user_no = request.args.get('xnr_user_no','')
    task_detail['domain_name'] = request.args.get('domain_name','')
    task_detail['role_name'] = request.args.get('role_name','')
    task_detail['daily_interests'] = request.args.get('daily_interests','') # 提交的日常兴趣，以中文逗号分隔“，”
    #task_detail['monitor_keywords'] = request.args.get('monitor_keywords','')  # 提交的关键词，以中文逗号分隔“，”
    recommend_results = get_recommend_step_two(task_detail)
    return json.dumps(recommend_results)

# 根据昵称填充其他信息
@mod.route('/add_other_info/')
def ajax_add_other_info():

    nick_name = request.args.get('nick_name','')
    results = get_add_other_info({'nick_name':nick_name})

    return json.dumps(results)

# 修改第二步信息
@mod.route('/modify_userinfo/')
def ajax_modify_userinfo():
    task_detail = {}
    task_detail['nick_name'] = request.args.get('nick_name','')
    task_detail['age'] = request.args.get('age','')
    task_detail['description'] = request.args.get('description','')
    task_detail['location'] = request.args.get('location','')
    task_detail['gender'] = request.args.get('gender','')


    results = get_modify_userinfo(task_detail)

    return json.dumps(results)

#第三步绑定账户关注用户推荐
@mod.route('/recommend_follows/')
def ajax_recommend_followers():
    task_detail = dict()
    task_detail['daily_interests'] = request.args.get('daily_interests','') # 提交的日常兴趣，以中文逗号分隔“，”
    task_detail['monitor_keywords'] = request.args.get('monitor_keywords','')  # 提交的关键词，以中文逗号分隔“，”

    recommend_results = get_recommend_follows(task_detail)
    return json.dumps(recommend_results)
'''
# 保存第一步信息
@mod.route('/save_step_one/')
def ajax_save_step_one():
    task_detail = dict()
    task_detail['domain_name'] = request.args.get('domain_name','') # 渗透领域
    task_detail['role_name'] = request.args.get('role_name','') # 角色定位
    task_detail['psy_feature'] = request.args.get('psy_feature','') # 心理特征，以中文逗号 “，”连接
    task_detail['political_side'] = request.args.get('political_side','') # 政治倾向
    task_detail['business_goal'] = request.args.get('business_goal','') # 业务目标,以中文逗号 “，”连接
    task_detail['daily_interests'] = request.args.get('daily_interests','') # 提交的日常兴趣，以中文逗号分隔“，”
    task_detail['monitor_keywords'] = request.args.get('monitor_keywords','')  # 提交的关键词，以中文逗号分隔“，”

    mark = get_save_step_one(task_detail)
    return json.dumps(mark)  #True：保存成功  False：保存失败
'''

# 保存第二步信息
@mod.route('/save_step_two/')
def ajax_save_step_two():
    task_detail = dict()
    task_detail['task_id'] = request.args.get('task_id', '') # 为空表示需要后台分配，如果有WXNR0001则更新
    task_detail['submitter'] = request.args.get('submitter','admin@qq.com') # 提交用户
    task_detail['domain_name'] = request.args.get('domain_name','') # 渗透领域
    task_detail['role_name'] = request.args.get('role_name','') # 角色定位
    task_detail['psy_feature'] = request.args.get('psy_feature','') # 心理特征，以中文逗号 “，”连接
    task_detail['political_side'] = request.args.get('political_side','') # 政治倾向
    task_detail['business_goal'] = request.args.get('business_goal','') # 业务目标,以中文逗号 “，”连接
    task_detail['daily_interests'] = request.args.get('daily_interests','') # 提交的日常兴趣，以中文逗号分隔“，”
    task_detail['monitor_keywords'] = request.args.get('monitor_keywords','')  # 提交的关键词，以中文逗号分隔“，”
    '''
    #task_detail['sex'] = request.args.get('sex','')
    #task_detail['task_id'] = request.args.get('task_id','') # 微博虚拟人编号，如：WXNR0001
    #task_detail['nick_name'] = request.args.get('nick_name','') # 昵称
    #task_detail['age'] = request.args.get('age','') # 年龄
    #task_detail['location'] = request.args.get('location','') # 所在地
    #task_detail['career'] = request.args.get('career','') # 职业
    #task_detail['description'] = request.args.get('description','') # 个人简介
    '''
    task_detail['active_time'] = request.args.get('active_time','') 
    # 活跃时间，数字，以中文逗号分隔“，”，如：9,19 表示：9:00-10:00，19:00-20:00活跃
    task_detail['day_post_average'] = request.args.get('day_post_average','') 
    # 日发帖量，以“-”分隔，如：9-12,表示每天平均发帖9到12条。从不：0-0,5条以上：5-max
    
    mark, task_id = get_save_step_two(task_detail)
    return json.dumps([mark, task_id])  #True：保存成功  False：保存失败

# 第三步返回左侧信息栏信息
@mod.route('/show_xnr_info/')
def ajax_show_xnr_info():
    task_detail = dict()
    task_detail['nick_name'] = request.args.get('nick_name','')  # 昵称

    result = get_xnr_info(task_detail)

    return json.dumps(result)

# 保存第三步信息1  绑定成功 
@mod.route('/save_step_three_1/')
def ajax_save_step_three_1():
    task_detail = dict()
    task_detail['task_id'] = request.args.get('task_id') #WXNR0001
    #task_detail['nick_name'] = request.args.get('nick_name','') # 微博虚拟人编号，如：WXNR0001
    task_detail['weibo_mail_account'] = request.args.get('weibo_mail_account','') # 邮箱
    task_detail['weibo_phone_account'] = request.args.get('weibo_phone_account','') # 手机号
    task_detail['password'] = request.args.get('password','') # 密码
    task_detail['nick_name'] = request.args.get('nick_name','') # 用户昵称
    print 'nick_name::',task_detail['nick_name']
    #step2 info
    new_task_detail = get_add_other_info(task_detail)  #nick_name, location, gender, age--0, descripriton

    #new_task_detail = dict(task_detail, **results)
    if new_task_detail == 'nick_name error':
        print 'name error!!'
        return json.dumps(new_task_detail)
        
    #results = get_user_info(task_detail)
    else:
        mark = get_save_step_three_1(new_task_detail)

        return json.dumps(mark)  #True：保存成功  False：保存失败

# 保存第三步信息2  关注成功
@mod.route('/save_step_three_2/')
def ajax_save_step_three_2():
    task_detail = dict()
    task_detail['task_id'] = request.args.get('task_id','') # 微博虚拟人编码，如：WXNR0001
    task_detail['nick_name'] = request.args.get('nick_name','') # 微博虚拟人昵称
    task_detail['followers_uids'] = request.args.get('followers_uids','') # 关注的人，昵称之间以中文逗号分隔“，”
    print 'task_detail::',task_detail
    mark = get_save_step_three_2(task_detail)
    return json.dumps(mark)  #True：保存成功  False：保存失败


@mod.route('/show_register_info/')
def ajax_show_register_info():
    
    return json.dumps(results)

@mod.route('/save_register_info/')
def ajax_save_register_info():

    return json.dumps(results)

@mod.route('/bind_info/')
def ajax_bind_indo():

    return json.dumps(results)
