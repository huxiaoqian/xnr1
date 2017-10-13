#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from utils import show_completed_weiboxnr,show_uncompleted_weiboxnr,delete_weibo_xnr,\
                  xnr_today_remind,change_continue_xnrinfo,show_timing_tasks,\
                  wxnr_timing_tasks_lookup,wxnr_timing_tasks_change,wxnr_timing_tasks_revoked,\
				  show_history_posting,show_at_content,show_comment_content,show_like_content,\
				  wxnr_list_concerns,wxnr_list_fans,count_weibouser_influence,show_history_count
from utils import get_weibohistory_retweet,get_weibohistory_comment,get_weibohistory_like,\
                  show_comment_dialog,cancel_follow_user,attach_fans_follow,lookup_detail_weibouser,\
                  delete_history_count,create_history_count,lookup_xnr_assess_info,\
                  get_xnr_detail,\
                  create_xnr_flow_text,update_weibo_count,create_send_like
from xnr.time_utils import datetime2ts

mod = Blueprint('weibo_xnr_manage', __name__, url_prefix='/weibo_xnr_manage')

#添加虚拟人
#首次添加——跳转至虚拟人定制第一步
#继续创建，传虚拟人id，跳转至虚拟人定制第二步

#已有虚拟人
#暂未完成测试
#test:http://219.224.134.213:9209/weibo_xnr_manage/show_completed_weiboxnr/?account_no=admin@qq.com
@mod.route('/show_completed_weiboxnr/')
def ajax_show_completed_weiboxnr():
	now_time=int(time.time())
	account_no=request.args.get('account_no','')
	results=show_completed_weiboxnr(account_no,now_time)
	return json.dumps(results)

#进入虚拟人中心，返回虚拟人信息
#http://219.224.134.213:9209/weibo_xnr_manage/get_xnr_detail/?xnr_user_no=WXNR0003
@mod.route('/get_xnr_detail/')
def ajax_get_xnr_detail():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=get_xnr_detail(xnr_user_no)
	return json.dumps(results)

#未完成虚拟人
#test:http://219.224.134.213:9209/weibo_xnr_manage/show_uncompleted_weiboxnr/?account_no=admin@qq.com
@mod.route('/show_uncompleted_weiboxnr/')
def ajax_show_uncompleted_weiboxnr():
	account_no=request.args.get('account_no','')
	results=show_uncompleted_weiboxnr(account_no)
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

#历史统计
'''
#http://219.224.134.213:9209/weibo_xnr_manage/wxnr_history_count/?xnr_user_no=WXNR0004&startdate=2017-09-01&enddate=2017-09-05
@mod.route('/wxnr_history_count/')
def ajax_wxnr_history_count():
	startdate=request.args.get('startdate','')
	enddate=request.args.get('enddate','')
	xnr_user_no=request.args.get('xnr_user_no','')
	results=wxnr_history_count(xnr_user_no,startdate,enddate)
	return json.dumps(results)
'''

#按时间条件显示历史统计结果
#http://219.224.134.213:9209/weibo_xnr_manage/show_history_count/?xnr_user_no=WXNR0004&type=today&start_time=0&end_time=1505044800
#http://219.224.134.213:9209/weibo_xnr_manage/show_history_count/?xnr_user_no=WXNR0004&type=''&start_time=1504526400&end_time=1505044800
#http://219.224.134.213:9209/weibo_xnr_manage/show_history_count/?xnr_user_no=WXNR0004&type=&start_time=1506182400&end_time=1506433221
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

#http://219.224.134.213:9209/weibo_xnr_manage/delete_history_count/?task_id=WXNR0004_2017-09-27
@mod.route('/delete_history_count/')
def ajax_delete_history_count():
	task_id=request.args.get('task_id','')
	results=delete_history_count(task_id)
	return json.dumps(results)

#http://219.224.134.213:9209/weibo_xnr_manage/create_history_count/?xnr_user_no=WXNR0004&date_time=2017-09-24&safe=18.12&daily_post_num=4&user_fansnum=2&business_post_num=1&influence=1.45&penetration=20.99&total_post_sum=8&hot_follower_num=2
@mod.route('/create_history_count/')
def ajax_create_history_count():
	task_detail=dict()
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['date_time']=request.args.get('date_time','')
	#task_detail['safe']=long(request.args.get('safe',''))
	task_detail['safe']=15.12
	task_detail['daily_post_num']=int(request.args.get('daily_post_num',''))
	task_detail['user_fansnum']=int(request.args.get('user_fansnum',''))
	task_detail['business_post_num']=int(request.args.get('business_post_num',''))
	task_detail['timestamp']=datetime2ts(request.args.get('date_time',''))
	#task_detail['influence']=long(request.args.get('influence',''))
	#task_detail['penetration']=long(request.args.get('penetration',''))
	task_detail['influence']=2.45
	task_detail['penetration']=25.99
	task_detail['total_post_sum']=int(request.args.get('total_post_sum',''))
	task_detail['hot_follower_num']=int(request.args.get('hot_follower_num',''))
	results=create_history_count(task_detail)
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
#http://219.224.134.213:9209/weibo_xnr_manage/show_timing_tasks/?xnr_user_no=WXNR0004&start_time=1500108142&end_time=1500108142
@mod.route('/show_timing_tasks/')
def ajax_show_timing_tasks():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	results=show_timing_tasks(xnr_user_no,start_time,end_time)
	return json.dumps(results)

#查看某一具体任务
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks_lookup/?task_id=1234567890_1500108198
@mod.route('/wxnr_timing_tasks_lookup/')
def ajax_wxnr_timing_tasks_lookup():
	task_id=request.args.get('task_id','')
	results=wxnr_timing_tasks_lookup(task_id)
	return json.dumps(results)

#修改某一具体任务
#说明：点击修改这一操作时，首先是执行查看某一具体任务这一功能，然后修改页面内容后，提交时调用该修改函数
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks_change/?task_id=1234567890_1500108198&task_source=日常发帖&operate_type=origin&create_time=1500110468&post_time=1500108142&text=明天有一起参加夜跑的吗？我想参加&remark=待定
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
#http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks_revoked/?task_id=1234567890_1500108198
@mod.route('/wxnr_timing_tasks_revoked/')
def ajax_wxnr_timing_tasks_revoked():
	task_id=request.args.get('task_id','') 
	results=wxnr_timing_tasks_revoked(task_id)
	return json.dumps(results)

#step 4.3: history information
#step 4.3.1:show history posting
#http://219.224.134.213:9209/weibo_xnr_manage/show_history_posting/?xnr_user_no=WXNR0004&task_source=daily_post,business_post&start_time=1504540800&end_time=1504627140
@mod.route('/show_history_posting/')
def ajax_show_history_posting():
	require_detail=dict()
	require_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	# daily_post-日常发帖,hot_post-热点跟随,business_post-业务发帖
	require_detail['task_source']=request.args.get('task_source','').split(',')
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

'''
微博相关操作
'''
#转发
#http://219.224.134.213:9209/weibo_xnr_manage/get_weibohistory_retweet/?xnr_user_no=WXNR0003&r_mid=4143645403880308&text=下雨了，吼吼\(^o^)/~
@mod.route('/get_weibohistory_retweet/')
def ajax_get_weibohistory_retweet():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','').encode('utf-8')     #text指转发时发布的内容
    results=get_weibohistory_retweet(task_detail)
    return json.dumps(results)

#评论
#http://219.224.134.213:9209/weibo_xnr_manage/get_weibohistory_comment/?xnr_user_no=WXNR0003&r_mid=4143645403880308&text=蓝天白云
@mod.route('/get_weibohistory_comment/')
def ajax_get_weibohistory_comment():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','').encode('utf-8')    #text指转发时发布的内容
    results=get_weibohistory_comment(task_detail)
    return json.dumps(results)

#赞
#http://219.224.134.213:9209/weibo_xnr_manage/get_weibohistory_like/?xnr_user_no=WXNR0004&r_mid=4143645403880308&uid=6346321407&nick_name=巨星大大&text=下雨了，吼吼\(^o^)/~&timestamp=1503405480
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

#收藏
############暂无公共函数可调用#########

#查看对话
#http://219.224.134.213:9209/weibo_xnr_manage/show_comment_dialog/?mid=4142135114307228
@mod.route('/show_comment_dialog/')
def ajax_show_comment_dialog():
	mid=request.args.get('mid','')
	results=show_comment_dialog(mid)
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

#step 4.4: list of concerns
#http://219.224.134.213:9209/weibo_xnr_manage/wxnr_list_concerns/?user_id=WXNR0004&order_type=influence
@mod.route('/wxnr_list_concerns/')
def ajax_wxnr_list_concerns(): 
	user_id=request.args.get('user_id','')
	#order_type 影响力:ifluence  敏感度:sensitive
	order_type=request.args.get('order_type','')
	results=wxnr_list_concerns(user_id,order_type)
	return json.dumps(results)
 
#step 4.5: list of fans
#http://219.224.134.213:9209/weibo_xnr_manage/wxnr_list_fans/?user_id=WXNR0004&order_type=influence
@mod.route('/wxnr_list_fans/')
def ajax_wxnr_list_fans():
	user_id=request.args.get('user_id','')
	order_type=request.args.get('order_type','')
	results=wxnr_list_fans(user_id,order_type)
	return json.dumps(results)


#按指标查询评估信息
#assess_type=influence,safe,penetration
#http://219.224.134.213:9209/weibo_xnr_manage/lookup_xnr_assess_info/?xnr_user_no=WXNR0004&start_time=1506096000&end_time=1506441600&assess_type=influence
@mod.route('/lookup_xnr_assess_info/')
def ajax_lookup_xnr_assess_info():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	assess_type=request.args.get('assess_type','')
	results=lookup_xnr_assess_info(xnr_user_no,start_time,end_time,assess_type)
	return json.dumps(results)



#http://219.224.134.213:9209/weibo_xnr_manage/create_xnr_flow_text/?task_source=daily_post&xnr_user_no=WXNR0004&uid=6346321407&text=下雨了，吼吼\(^o^)/~&user_fansnum=9&weibos_sum=47&mid=4143645403880308&timestamp=1503405480&comment=5&sensitive=1&retweeted=2
#http://219.224.134.213:9209/weibo_xnr_manage/create_xnr_flow_text/?task_source=business_post&xnr_user_no=WXNR0004&uid=6346321407&text=国足加油~给力！&user_fansnum=9&weibos_sum=47&mid=4143645403880309&timestamp=1504615080&comment=115&sensitive=3&retweeted=255
#http://219.224.134.213:9209/weibo_xnr_manage/create_xnr_flow_text/?task_source=hot_post&xnr_user_no=WXNR0004&uid=6346321407&text=孕妇跳楼案广受关注！&user_fansnum=9&weibos_sum=47&mid=4143645403880319&timestamp=1504625080&comment=185&sensitive=5&retweeted=255
#http://219.224.134.213:9209/weibo_xnr_manage/create_xnr_flow_text/?task_source=hot_post&xnr_user_no=WXNR0004&uid=6346321407&text=918事件广受关注！&user_fansnum=9&weibos_sum=47&mid=4143645403880320&timestamp=1505685600&comment=1185&sensitive=10&retweeted=1255
@mod.route('/create_xnr_flow_text/')
def ajax_create_xnr_flow_text():
	task_id='WXNR0004_1507730704'
	task_detail=dict()
	task_detail['task_source']='trace_follow_tweet'
	task_detail['xnr_user_no']='WXNR0004'
	task_detail['uid']='6346321407'
	task_detail['text']='放过他老人家吧//@传媒老王:今天一整天要在当年毛泽东领导秋收起义的出发地，现在的国家生态县，中国红豆杉之乡铜鼓采风。铜鼓县，位于湘鄂赣三省交界处，是赣西门户。'
	task_detail['picture_url']=''
	task_detail['vedio_url']=''
	task_detail['user_fansnum']=10
	task_detail['weibos_sum']=88
	task_detail['mid']=''
	task_detail['ip']=''
	task_detail['directed_uid']=''
	task_detail['directed_uname']=''
	task_detail['timestamp']=1507730727
	task_detail['sentiment']=''
	task_detail['geo']=''
	task_detail['keywords_dict']=''
	task_detail['keywords_string']=''
	task_detail['sensitive_words_dict']=''
	task_detail['sensitive_words_string']=''
	task_detail['message_type']=''
	task_detail['root_uid']=''
	task_detail['origin_text']=''
	task_detail['origin_keywords_dict']=''
	task_detail['origin_keywords_string']=''
	task_detail['comment']=0
	task_detail['sensitive']=0
	task_detail['sensitive_words_dict']=''
	task_detail['retweeted']=0

	results=create_xnr_flow_text(task_detail,task_id)
	return json.dumps(results)





@mod.route('/update_weibo_count/')
def ajax_update_weibo_count():
    task_id='WXNR0004_2017-10-01'
    task_detail=dict()
    task_detail['date_time']='2017-10-01'
    task_detail['safe']=19.22
    task_detail['daily_post_num']=1
    task_detail['user_fansnum']=8
    task_detail['business_post_num']=0
    task_detail['timestamp']=1506787200
    task_detail['xnr_user_no']='WXNR0004'
    task_detail['influence']=1.04
    task_detail['penetration']=21.69
    task_detail['total_post_sum']=1
    task_detail['hot_follower_num']=0
    results=update_weibo_count(task_detail,task_id)
    return json.dumps(results)


@mod.route('/create_send_like/')
def ajax_create_send_like():
	task_id='6346321407_1507451940'
	task_detail=dict()
	task_detail['update_time']=1507452240      #点赞时间
	task_detail['uid']=''           #6340301597'       #点赞对象uid
	task_detail['root_uid']='6346321407'
	task_detail['nick_name']='巨星大大'
	task_detail['text']='鹿晗关晓彤\
关晓彤工作室\
鹿晗工作室\
陈翔哭了\
陈翔 说散就散\
鹿晗 有了女朋友一定会公开\
陈赫点赞\
鹿晗关晓彤踢球\
鹿晗掉粉\
关晓彤爸爸\
关晓彤会解二元一次方程\
什么乱七八糟滴……微博出问题了吧！\
我们还在景区 堵着呢…… http://t.cn/RObS6p0'
	task_detail['mid']=''
	task_detail['weibo_type']='stranger'
	task_detail['timestamp']=1507451940       #微博时间
	task_detail['root_mid']=''
	task_detail['photo_url']=''
	results=create_send_like(task_detail,task_id)
	return json.dumps(results)