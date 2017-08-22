#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_xnr
from utils import show_report_content,show_report_typecontent,\
				  get_weibohistory_retweet,get_weibohistory_comment,get_weibohistory_like

mod=Blueprint('weibo_xnr_report_manage',__name__,url_prefix='/weibo_xnr_report_manage')


'''
上报管理
'''
#默认显示上报内容-不分类
@mod.route('/show_report_content/')
def ajax_show_report_content():
	results=show_report_content()
	return json.dumps(results)

#按类别显示上报内容
@mod.route('/show_report_typecontent/')
def ajax_show_report_typecontent():
	report_type=request.args.get('report_type','')
	results=show_report_typecontent(report_type)
	return json.dumps(results)


#############微博相关操作########

#转发
@mod.route('/get_weibohistory_retweet/')
def ajax_get_weibohistory_retweet():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','')    #text指转发时发布的内容
    results=get_weibohistory_retweet(task_detail)
    return json.dumps(results)

#评论
@mod.route('/get_weibohistory_comment/')
def ajax_get_weibohistory_comment():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','')    #text指转发时发布的内容
    results=get_weibohistory_comment(task_detail)
    return json.dumps(results)

#赞
@mod.route('/get_weibohistory_like/')
def ajax_get_weibohistory_like():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    results=get_weibohistory_like(task_detail)
    return json.dumps(results)
