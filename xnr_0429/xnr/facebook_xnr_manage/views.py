#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_xnr
es_flow_text = es_xnr
from xnr.time_utils import datetime2ts
from utils import show_completed_fbxnr,show_uncompleted_fbxnr,delete_fb_xnr, get_xnr_detail,\
					 show_history_count, lookup_xnr_assess_info

from utils import show_timing_tasks,wxnr_timing_tasks_lookup,wxnr_timing_tasks_change,wxnr_timing_tasks_revoked,\
                  wxnr_list_friends,show_history_posting,show_at_content,show_comment_content,show_like_content
'''
from utils import xnr_today_remind,change_continue_xnrinfo,show_timing_tasks,\
                  wxnr_timing_tasks_lookup,wxnr_timing_tasks_change,wxnr_timing_tasks_revoked,\
				  show_history_posting,show_at_content,show_comment_content,show_like_content,\
				  wxnr_list_concerns,wxnr_list_fans,count_weibouser_influence,show_history_count
from utils import get_weibohistory_retweet,get_weibohistory_comment,get_weibohistory_like,\
                  show_comment_dialog,cancel_follow_user,attach_fans_follow,lookup_detail_weibouser,\
                  delete_history_count,create_history_count,lookup_xnr_assess_info,\
                  get_xnr_detail,\
                  create_xnr_flow_text,update_weibo_count,create_send_like,delete_weibo_count,delete_receive_like,delete_xnr_flow_text
'''

mod = Blueprint('facebook_xnr_manage', __name__, url_prefix='/facebook_xnr_manage')

#添加虚拟人
#首次添加——跳转至虚拟人定制第一步
#继续创建，传虚拟人id，跳转至虚拟人定制第二步

#已有虚拟人
#暂未完成测试
#test:http://219.224.134.213:9209/facebook_xnr_manage/show_completed_fbxnr/?account_no=admin@qq.com
@mod.route('/show_completed_fbxnr/')
def ajax_show_completed_weiboxnr():
	now_time=int(time.time())
	account_no=request.args.get('account_no','')
	results=show_completed_fbxnr(account_no,now_time)
	return json.dumps(results)

#进入虚拟人中心，返回虚拟人信息
#http://219.224.134.213:9209/facebook_xnr_manage/get_xnr_detail/?xnr_user_no=FXNR0005
@mod.route('/get_xnr_detail/')
def ajax_get_xnr_detail():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=get_xnr_detail(xnr_user_no)
	return json.dumps(results)

#未完成虚拟人
#test:http://219.224.134.213:9209/facebook_xnr_manage/show_uncompleted_fbxnr/?account_no=admin@qq.com
@mod.route('/show_uncompleted_fbxnr/')
def ajax_show_uncompleted_weiboxnr():
	account_no=request.args.get('account_no','')
	results=show_uncompleted_fbxnr(account_no)
	return json.dumps(results)

#删除虚拟人
#test:http://219.224.134.213:9209/weibo_xnr_manage/delete_weibo_xnr/?xnr_user_no=WXNR0001
@mod.route('/delete_fb_xnr/')
def ajax_delete_fb_xnr():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=delete_fb_xnr(xnr_user_no)
	return json.dumps(results)


#按指标查询评估信息
#assess_type=influence,safe,penetration
#http://219.224.134.213:9209/facebook_xnr_manage/lookup_xnr_assess_info/?xnr_user_no=FXNR0004&start_time=1506096000&end_time=1506441600&assess_type=influence
@mod.route('/lookup_xnr_assess_info/')
def ajax_lookup_xnr_assess_info():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	assess_type=request.args.get('assess_type','')
	results=lookup_xnr_assess_info(xnr_user_no,start_time,end_time,assess_type)
	return json.dumps(results)



#按时间条件显示历史统计结果
#http://219.224.134.213:9209/facebook_xnr_manage/show_history_count/?xnr_user_no=FXNR0004&type=today&start_time=0&end_time=1505044800
#http://219.224.134.213:9209/facebook_xnr_manage/show_history_count/?xnr_user_no=FXNR0004&type=''&start_time=1504526400&end_time=1505044800
#http://219.224.134.213:9209/facebook_xnr_manage/show_history_count/?xnr_user_no=FXNR0004&type=&start_time=1506182400&end_time=1506433221
@mod.route('/show_history_count/')
def ajax_show_history_count():
	xnr_user_no=request.args.get('xnr_user_no','')
	date_range=dict()
	#今日统计type=today,start_time=0,end_time=当前时间；其他时间条件则type=''，start_time=起始时间，end_time=终止时间
	date_range['type']=request.args.get('type','')
	date_range['start_time']=int(request.args.get('start_time',''))
	date_range['end_time']=int(request.args.get('end_time',''))
	results=show_history_count(xnr_user_no,date_range)
	return json.dumps(results)



#今日提醒
#http://219.224.134.213:9209/facebook_xnr_manage/xnr_today_remind/?xnr_user_no=FXNR0005
@mod.route('/xnr_today_remind/')
def ajax_xnr_today_remind():
	now_time=int(time.time())
	xnr_user_no=request.args.get('xnr_user_no','')
	results=xnr_today_remind(xnr_user_no,now_time)
	return json.dumps(results)

#继续创建和修改虚拟人——跳转至目标定制第二步，传送目前已有的信息至前端
#input:xnr_user_no
#http://219.224.134.213:9209/facebook_xnr_manage/change_continue_xnrinfo/?xnr_user_no=FXNR0005
@mod.route('/change_continue_xnrinfo/')
def ajax_change_continue_xnrinfo():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=change_continue_xnrinfo(xnr_user_no)
	return json.dumps(results)



############################by qxk

#step 4.2:timing task list
#获取定时发送任务列表
#http://219.224.134.213:9207/facebook_xnr_manage/show_timing_tasks/?xnr_user_no=FXNR0001&start_time=1483200000&end_time=1522641377
@mod.route('/show_timing_tasks/')
def ajax_show_timing_tasks():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	results=show_timing_tasks(xnr_user_no,start_time,end_time)
	return json.dumps(results)

#查看某一具体任务
#http://219.224.134.213:9209/facebook_xnr_manage/wxnr_timing_tasks_lookup/?task_id=FXNR0001_1514883344_1514883341
@mod.route('/wxnr_timing_tasks_lookup/')
def ajax_wxnr_timing_tasks_lookup():
	task_id=request.args.get('task_id','')
	results=wxnr_timing_tasks_lookup(task_id)
	return json.dumps(results)

#修改某一具体任务
#说明：点击修改这一操作时，首先是执行查看某一具体任务这一功能，然后修改页面内容后，提交时调用该修改函数
#http://219.224.134.213:9209/facebook_xnr_manage/wxnr_timing_tasks_change/?task_id=FXNR0005_1522641703&task_source=日常发帖&operate_type=origin&create_time=1522641377&post_time=1522651377&text=放假有一起去长城的吗？我想参加&remark=待定
@mod.route('/wxnr_timing_tasks_change/')
def ajax_wxnr_timing_tasks_change():
	task_id=request.args.get('task_id','')      #指_id这个字段
	#对任务具体内容进行修改
	task_source=request.args.get('task_source','')
	operate_type=request.args.get('operate_type','')
	create_time=int(time.time())
	post_time=request.args.get('post_time','')
	text=request.args.get('text','')
	remark=request.args.get('remark','')
	task_change_info=[task_source,operate_type,create_time,post_time,text,remark]
	results=wxnr_timing_tasks_change(task_id,task_change_info)
	return json.dumps(results)


#撤销未发送的任务
#http://219.224.134.213:9209/facebook_xnr_manage/wxnr_timing_tasks_revoked/?task_id=FXNR0005_1522641703
@mod.route('/wxnr_timing_tasks_revoked/')
def ajax_wxnr_timing_tasks_revoked():
	task_id=request.args.get('task_id','') 
	results=wxnr_timing_tasks_revoked(task_id)
	return json.dumps(results)




#step 4.4: list of concerns
#http://219.224.134.213:9209/facebook_xnr_manage/wxnr_list_concerns/?user_id=WXNR0004&order_type=influence
@mod.route('/wxnr_list_friends/')
def ajax_wxnr_list_friends(): 
	user_id=request.args.get('user_id','')
	#order_type 影响力:ifluence  敏感度:sensitive
	order_type=request.args.get('order_type','')
	results=wxnr_list_friends(user_id,order_type)
	return json.dumps(results)
 




#step 4.3: history information
#step 4.3.1:show history posting
#http://219.224.134.213:9209/weibo_xnr_manage/show_history_posting/?xnr_user_no=WXNR0004&task_source=daily_post,business_post&start_time=1504540800&end_time=1504627140
@mod.route('/show_history_posting/')
def ajax_show_history_posting():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	# message_type:1 原创，2评论，3转发
	require_detail['message_type']=request.args.get('message_type','').split(',') 
	#require_detail['now_time']=int(time.time())    
	require_detail['start_time']=int(request.args.get('start_time',''))
	require_detail['end_time']=int(request.args.get('end_time',''))
	results=show_history_posting(require_detail)
	return json.dumps(results)



#step 4.3.2:show at content
#http://219.224.134.213:9209/weibo_xnr_manage/show_at_content/?xnr_user_no=WXNR0004&content_type=weibo,at&start_time=1501948800&end_time=1504627200
@mod.route('/show_at_content/')
def ajax_show_at_content():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	#content_type='weibo'表示@我的微博，='at'表示@我的评论
	require_detail['content_type']=request.args.get('content_type','').split(',')
	require_detail['start_time']=int(request.args.get('start_time',''))
	require_detail['end_time']=int(request.args.get('end_time',''))
	results=show_at_content(require_detail)
	return json.dumps(results)

#step 4.3.3: show comment content
#http://219.224.134.213:9209/weibo_xnr_manage/show_comment_content/?xnr_user_no=WXNR0003&comment_type=make,receive&start_time=1501948800&end_time=1504627200
@mod.route('/show_comment_content/')
def ajax_show_comment_content():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	## make 发出的评论   receive 收到的评论
	require_detail['comment_type']=request.args.get('comment_type','').split(',')    
	require_detail['start_time']=int(request.args.get('start_time',''))
	require_detail['end_time']=int(request.args.get('end_time',''))
	results=show_comment_content(require_detail)
	return json.dumps(results)

#step 4.3.4:show like content
#http://219.224.134.213:9209/weibo_xnr_manage/show_like_content/?xnr_user_no=WXNR0004&like_type=send,receive&start_time=1480045631&end_time=1504627200
@mod.route('/show_like_content/')
def ajax_show_like_content():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	## send 发出的赞   receive 收到的赞
	require_detail['like_type']=request.args.get('like_type','').split(',')
	require_detail['start_time']=int(request.args.get('start_time',''))
	require_detail['end_time']=int(request.args.get('end_time',''))
	results=show_like_content(require_detail)
	return json.dumps(results)



#收藏
############暂无公共函数可调用#########

#查看对话
#http://219.224.134.213:9209/weibo_xnr_manage/show_comment_dialog/?fid=4142135114307228
@mod.route('/show_comment_dialog/')
def ajax_show_comment_dialog():
	fid=request.args.get('fid','')
	results=show_comment_dialog(fid)
	return json.dumps(results)

#回复
#——与评论操作一致

#取消关注
#http://219.224.134.213:9209/weibo_xnr_manage/cancel_follow_user/?xnr_user_no=WXNR0004&uid=6340301597
@mod.route('/cancel_follow_user/')
def ajax_cancel_follow_user():
	task_detail=dict()
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['uid']=request.args.get('uid','')
	results=cancel_follow_user(task_detail)
	return json.dumps(results)

#直接关注
#http://219.224.134.213:9209/weibo_xnr_manage/attach_fans_follow/?xnr_user_no=WXNR0004&uid=6340301597
@mod.route('/attach_fans_follow/')
def ajax_attach_fans_follow():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['uid']=request.args.get('uid','')   #关注对象的uid
    task_detail['trace_type']=request.args.get('trace_type','')
    results=attach_fans_follow(task_detail)
    return json.dumps(results)

#查看详情
#http://219.224.134.213:9209/weibo_xnr_manage/lookup_detail_weibouser/?uid=2366858840
@mod.route('/lookup_detail_weibouser/')
def ajax_lookup_detail_weibouser():
	uid=request.args.get('uid','')
	results=lookup_detail_weibouser(uid)
	return json.dumps(results)









@mod.route('/delete_receive_like/')
def ajax_delete_receive_like():
	results=delete_receive_like()
	return json.dumps(results)