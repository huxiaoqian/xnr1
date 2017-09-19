#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from utils import create_log_list,show_log_list,delete_log_list,\
				  create_role_authority,show_authority_list,change_authority_list,delete_authority_list,\
				  create_user_account,add_user_xnraccount,show_users_account,delete_user_account,delete_user_xnraccount,change_user_account


mod = Blueprint('system_manage', __name__, url_prefix='/system_manage')

####日志管理
#添加日志内容
#http://219.224.134.213:9209/system_manage/create_log_list/?user_id=001&user_name=admin01@qq.com&login_time=1504922400&login_ip=127.0.0.1&operate_time=1504922400&operate_content=创建群体
@mod.route('/create_log_list/')
def ajax_create_log_list():
	user_id=request.args.get('user_id','')
	user_name=request.args.get('user_name','')
	login_time=request.args.get('login_time','')
	login_ip=request.args.get('login_ip','')
	operate_time=request.args.get('operate_time','')
	operate_content=request.args.get('operate_content','')
	log_info=[user_id,user_name,login_time,login_ip,operate_time,operate_content]
	results=create_log_list(log_info)
	return json.dumps(results)

#显示日志内容
#http://219.224.134.213:9209/system_manage/show_log_list
@mod.route('/show_log_list/')
def ajax_show_log_list():
	results=show_log_list()
	return json.dumps(results)

#删除日志内容
#http://219.224.134.213:9209/system_manage/delete_log_list/?log_id=0011504922400
@mod.route('/delete_log_list/')
def ajax_delete_log_list():
	log_id=request.args.get('log_id','')
	results=delete_log_list(log_id)
	return json.dumps(results)


###权限管理
#添加权限管理数据
#http://219.224.134.213:9209/system_manage/create_role_authority/?role_name=超级管理员&description=可以使用该系统所有权限，包括创建虚拟人、虚拟人日常行为控制等
#http://219.224.134.213:9209/system_manage/create_role_authority/?role_name=业务操作员&description=仅能对已经建立的管理员的日常行为进行控制
@mod.route('/create_role_authority/')
def ajax_create_role_authority():
	role_name=request.args.get('role_name','')
	description=request.args.get('description','')
	results=create_role_authority(role_name,description)
	return json.dumps(results)

#展示权限管理内容
#http://219.224.134.213:9209/system_manage/show_authority_list
@mod.route('/show_authority_list/')
def ajax_show_authority_list():
	results=show_authority_list()
	return json.dumps(results)

#修改权限
#http://219.224.134.213:9209/system_manage/change_authority_list/?role_name=业务操作员&description=对已经建立的业务管理员的日常行为进行控制
@mod.route('/change_authority_list/')
def ajax_change_authority_list():
	role_name=request.args.get('role_name','')
	description=request.args.get('description','')
	results=change_authority_list(role_name,description)
	return json.dumps(results)

#删除权限
#http://219.224.134.213:9209/system_manage/delete_authority_list/?role_name=业务操作员
@mod.route('/delete_authority_list/')
def ajax_delete_authority_list():
	role_name=request.args.get('role_name','')
	results=delete_authority_list(role_name)
	return json.dumps(results)

###账户管理
#添加账户
#http://219.224.134.213:9209/system_manage/create_user_account/?user_id=001&user_name=admin01@qq.com&my_xnrs=WXNR0001,WXNR0002
@mod.route('/create_user_account/')
def ajax_create_user_account():
	user_id=request.args.get('user_id','')
	user_name=request.args.get('user_name','')
	my_xnrs=request.args.get('my_xnrs','').split(',')
	user_account_info=[user_id,user_name,my_xnrs]
	results=create_user_account(user_account_info)
	return json.dumps(results)

#给指定账户添加虚拟人
#http://219.224.134.213:9209/system_manage/add_user_xnraccount/?account_id=001&xnr_accountid=WXNR0002,WXNR0003
@mod.route('/add_user_xnraccount/')
def ajax_add_user_xnraccount():
	account_id=request.args.get('account_id','')
	xnr_accountid=request.args.get('xnr_accountid','').split(',')
	results=add_user_xnraccount(account_id,xnr_accountid)
	return json.dumps(results)

#显示所有账户信息
#http://219.224.134.213:9209/system_manage/show_users_account
@mod.route('/show_users_account/')
def ajax_show_users_account():
	results=show_users_account()
	return json.dumps(results)

#删除账户
#http://219.224.134.213:9209/system_manage/delete_user_account/?account_id=001
@mod.route('/delete_user_account/')
def ajax_delete_user_account():
	account_id=request.args.get('account_id','')
	results=delete_user_account(account_id)
	return json.dumps(results)

#删除指定账户的某个虚拟人
#http://219.224.134.213:9209/system_manage/delete_user_xnraccount/?account_id=001&xnr_accountid=WXNR0001
@mod.route('/delete_user_xnraccount/')
def ajax_delete_user_xnraccount():
	account_id=request.args.get('account_id','')
	xnr_accountid=request.args.get('xnr_accountid','')
	results=delete_user_xnraccount(account_id,xnr_accountid)
	return json.dumps(results)

#修改账户信息
#http://219.224.134.213:9209/system_manage/change_user_account/?user_id=001&user_name=admin02@qq.com&my_xnrs=WXNR0001,WXNR0002,WXNR0003,WXNR0004
@mod.route('/change_user_account/')
def ajax_change_user_account():
	change_detail=dict()
	change_detail['user_id']=request.args.get('user_id','')
	change_detail['user_name']=request.args.get('user_name','')
	change_detail['my_xnrs']=request.args.get('my_xnrs').split(',')
	results=change_user_account(change_detail)
	return json.dumps(results)