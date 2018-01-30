#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_xnr
from utils import show_report_content,show_report_typecontent,\
				  get_weibohistory_retweet,get_weibohistory_comment,get_weibohistory_like,\
                  show_reportcontent_new

mod=Blueprint('weibo_xnr_report_manage',__name__,url_prefix='/weibo_xnr_report_manage')


'''
上报管理
'''
#默认显示上报内容-不分类
#http://219.224.134.213:9209/weibo_xnr_report_manage/show_report_content
@mod.route('/show_report_content/')
def ajax_show_report_content():
	results=show_report_content()
	return json.dumps(results)

#按类别显示上报内容
#http://219.224.134.213:9209/weibo_xnr_report_manage/show_report_typecontent/?report_type=事件
@mod.route('/show_report_typecontent/')
def ajax_show_report_typecontent():
	report_type=request.args.get('report_type','').split(',')
	results=show_report_typecontent(report_type)
	return json.dumps(results)


#上报显示新方法
@mod.route('/show_reportcontent_new/')
def ajax_show_reportcontent_new():
    report_type=request.args.get('report_type','').split(',')
    start_time=int(request.args.get('start_time',''))
    end_time=int(request.args.get('end_time',''))
    results=show_reportcontent_new(report_type,start_time,end_time)
    return json.dumps(results)    

#############微博相关操作########

#转发
#http://219.224.134.213:9209/weibo_xnr_report_manage/get_weibohistory_retweet/?xnr_user_no=WXNR0003&r_mid=4143645403880308&text=下雨了，吼吼\(^o^)/~
@mod.route('/get_weibohistory_retweet/')
def ajax_get_weibohistory_retweet():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','').encode('utf-8')     #text指转发时发布的内容
    results=get_weibohistory_retweet(task_detail)
    return json.dumps(results)

#评论
#http://219.224.134.213:9209/weibo_xnr_report_manage/get_weibohistory_comment/?xnr_user_no=WXNR0003&r_mid=4143645403880308&text=蓝天白云
@mod.route('/get_weibohistory_comment/')
def ajax_get_weibohistory_comment():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','').encode('utf-8')    #text指转发时发布的内容
    results=get_weibohistory_comment(task_detail)
    return json.dumps(results)

#赞
#http://219.224.134.213:9209/weibo_xnr_report_manage/get_weibohistory_like/?xnr_user_no=WXNR0004&r_mid=4143645403880308&uid=6346321407&nick_name=巨星大大&text=下雨了，吼吼\(^o^)/~&timestamp=1503405480
@mod.route('/get_weibohistory_like/')
def ajax_get_weibohistory_like():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['uid']=request.args.get('uid')   #点赞对象的uid
    task_detail['nick_name']=request.args.get('nick_name','') #点赞对象昵称
    task_detail['text']=request.args.get('text','').encode('utf-8')    #text指点赞的内容
    task_detail['timestamp']=int(request.args.get('timestamp',''))
    task_detail['update_time']=int(time.time())
    task_detail['photo_url']=request.args.get('photo_url','')
    results=get_weibohistory_like(task_detail)
    return json.dumps(results)



