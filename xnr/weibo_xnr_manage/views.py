#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from utils import show_completed_weiboxnr,show_uncompleted_weiboxnr,delete_weibo_xnr,change_continue_xnrinfo,\
				wxnr_timing_tasks,wxnr_timing_tasks_lookup,wxnr_timing_tasks_change,wxnr_timing_tasks_revoked,\
				show_history_posting,show_at_content,show_comment_content,show_like_content,\
				wxnr_list_concerns,wxnr_list_fans,xnr_today_remind
from utils import get_weibohistory_retweet,get_weibohistory_comment,get_weibohistory_like,show_comment_dialog,\
					cancel_follow_user,attach_fans_follow,lookup_detail_weibouser

mod = Blueprint('weibo_xnr_manage', __name__, url_prefix='/weibo_xnr_manage')

#添加虚拟人
#首次添加——跳转至虚拟人定制第一步
#继续创建，传虚拟人id，跳转至虚拟人定制第二步

#已有虚拟人
#暂未完成测试
#test:http://219.224.134.213:9209/weibo_xnr_manage/show_completed_weiboxnr/
@mod.route('/show_completed_weiboxnr/')
def ajax_show_completed_weiboxnr():
	now_time=int(time.time())
	results=show_completed_weiboxnr(now_time)
	return json.dumps(results)

#未完成虚拟人
#test:http://219.224.134.213:9209/weibo_xnr_manage/show_uncompleted_weiboxnr/
@mod.route('/show_uncompleted_weiboxnr/')
def ajax_show_uncompleted_weiboxnr():
	results=show_uncompleted_weiboxnr()
	return json.dumps(results)

#删除虚拟人
#test:http://219.224.134.213:9209/weibo_xnr_manage/delete_weibo_xnr/?xnr_user_no=WXNR0001
@mod.route('/delete_weibo_xnr/')
def ajax_delete_weibo_xnr():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=delete_weibo_xnr(xnr_user_no)
	return json.dumps(results)

#今日提醒
#http://219.224.134.213:9209/weibo_xnr_manage/xnr_today_remind/?xnr_user_no=WXNR0004
@mod.route('/xnr_today_remind/')
def ajax_xnr_today_remind():
	now_time=int(time.time())
	xnr_user_no=request.args.get('xnr_user_no','')
	results=xnr_today_remind(xnr_user_no,now_time)
	return json.dumps(results)

#继续创建和修改虚拟人——跳转至目标定制第二步，传送目前已有的信息至前端
#input:xnr_user_no
#http://219.224.134.213:9209/weibo_xnr_manage/change_continue_xnrinfo/?xnr_user_no=WXNR0003
@mod.route('/change_continue_xnrinfo/')
def ajax_change_continue_xnrinfo():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=change_continue_xnrinfo(xnr_user_no)
	return json.dumps(results)

#step 4.2:timing task list
#获取定时发送任务列表
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks/?user_id=WXNR0004
@mod.route('/wxnr_timing_tasks/')
def ajax_wxnr_timing_tasks():
	user_id=request.args.get('user_id','')
	results=wxnr_timing_tasks(user_id)
	return json.dumps(results)

#查看某一具体任务
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks_lookup/?task_id=1234567890_1500108142
@mod.route('/wxnr_timing_tasks_lookup/')
def ajax_wxnr_timing_tasks_lookup():
	task_id=request.args.get('task_id','')
	results=wxnr_timing_tasks_lookup(task_id)
	return json.dumps(results)

#修改某一具体任务
#说明：点击修改这一操作时，首先是执行查看某一具体任务这一功能，然后修改页面内容后，提交时调用该修改函数
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks_change/?task_id=1234567890_1500108142&task_source='日常发帖'&operate_type='origin'&create_time=1500110468&post_time=1500108142&text='明天有一起参加夜跑的吗？我想参加'&remark='待定'
@mod.route('/wxnr_timing_tasks_change/')
def ajax_wxnr_timing_tasks_change():
	task_id=request.args.get('task_id','')      #指_id这个字段
	#对任务具体内容进行修改
	task_source=request.args.get('task_source','')
	operate_type=request.args.get('operate_type','')
	create_time=request.args.get('create_time','')
	post_time=request.args.get('post_time','')
	text=request.args.get('text','')
	remark=request.args.get('remark','')
	task_change_info=[task_source,operate_type,create_time,post_time,text,remark]
	results=wxnr_timing_tasks_change(task_id,task_change_info)
	return json.dumps(results)

#撤销未发送的任务
@mod.route('/wxnr_timing_tasks_revoked/')
def ajax_wxnr_timing_tasks_revoked():
	task_id=request.args.get('task_id','') 
	results=wxnr_timing_tasks_revoked(task_id)
	return json.dumps(results)

#step 4.3: history information
#step 4.3.1:show history posting
@mod.route('/show_history_posting/')
def ajax_show_history_posting():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	require_detail['task_source']=request.args.get('task_source','')    #日常 or 业务 or 热门
	results=show_history_posting(require_detail)
	return json.dumps(results)

#step 4.3.2:show at content
@mod.route('/show_at_content/')
def ajax_show_at_content():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	#content_type='weibo'表示@我的微博，='at'表示@我的评论
	require_detail['content_type']=request.args.get('content_type','')
	results=show_at_content(require_detail)
	return json.dumps(results)

#step 4.3.3: show comment content
@mod.route('/show_comment_content/')
def ajax_show_comment_content():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	require_detail['weibo_type']=request.args.get('weibo_type','')    #收到的 or 发出的
	results=show_comment_content(require_detail)
	return json.dumps(results)

#step 4.3.4:show like content
@mod.route('/show_like_content/')
def ajax_show_like_content():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=show_like_content(xnr_user_no)
	return json.dumps(results)

'''
微博相关操作
'''
#转发
@mod.route('/get_weibohistory_retweet/')
def ajax_get_weibohistory_retweet():
	task_detail=dict()
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
	task_detail['text']=request.args.get('text','')	   #text指转发时发布的内容
	results=get_weibohistory_retweet(task_detail)
	return json.dumps(results)

#评论
@mod.route('/get_weibohistory_comment/')
def ajax_get_weibohistory_comment():
	task_detail=dict()
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
	task_detail['text']=request.args.get('text','')	   #text指转发时发布的内容
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

#收藏
############暂无公共函数可调用#########

#查看对话
#test:http://219.224.134.213:9209/weibo_xnr_manage/show_comment_dialog/?mid=3427464480701983
@mod.route('/show_comment_dialog/')
def ajax_show_comment_dialog():
	mid=request.args.get('mid','')
	results=show_comment_dialog(mid)
	return json.dumps(results)

#回复
#——与评论操作一致
@mod.route('/get_weibohistory_comment_reply/')
def ajax_get_weibohistory_comment_reply():
	task_detail=dict()
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
	task_detail['text']=request.args.get('text','')	   #text指转发时发布的内容
	results=get_weibohistory_comment(task_detail)
	return json.dumps(results)

#取消关注
@mod.route('/cancel_follow_user/')
def ajax_cancel_follow_user():
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['uid']=request.args.get('uid','')
	results=cancel_follow_user(task_detail)
	return json.dumps(results)

#直接关注
@mod.route('/attach_fans_follow/')
def ajax_attach_fans_follow():
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['uid']=request.args.get('uid','')
	results=attach_fans_follow(task_detail)
	return json.dumps(results)

#查看详情
@mod.route('/lookup_detail_weibouser/')
def ajax_lookup_detail_weibouser():
	uid=request.args.get('uid','')
	results=lookup_detail_weibouser(uid)
	return json.dumps(results)

#step 4.4: list of concerns
@mod.route('/wxnr_list_concerns/')
def ajax_wxnr_list_concerns(): 
	user_id=request.args.get('user_id','')
	order_id=request.args.get('order_id','')
	results=wxnr_list_concerns(user_id,order_id)
	return json.dumps(results)
 
#step 4.5: list of fans
@mod.route('/wxnr_list_fans/')
def ajax_wxnr_list_fans():
	user_id=request.args.get('user_id','')
	order_id=request.args.get('order_id','')
	results=wxnr_list_fans(user_id,order_id)
	return json.dumps(results)
