#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_personnal_warning,show_speech_warning,show_date_warning,show_event_warming,\
                  addto_warning_corpus,report_warming_content


mod = Blueprint('twitter_xnr_warning', __name__, url_prefix='/twitter_xnr_warning')

#人物行为预警
#http://219.224.134.213:9209/twitter_xnr_warning/show_personnal_warning/?xnr_user_no=TXNR0001&start_time=1511755200&end_time=1511857583
@mod.route('/show_personnal_warning/')
def ajax_show_personnal_warning():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	results=show_personnal_warning(xnr_user_no,start_time,end_time)
	return json.dumps(results)


#言论内容预警
#show_type=0,全部用户；1，关注用户；2，未关注用户
#http://219.224.134.213:9209/twitter_xnr_warning/show_speech_warning/?xnr_user_no=TXNR0001&show_type=0&start_time=1511755200&end_time=1511857583
@mod.route('/show_speech_warning/')
def ajax_show_speech_warning():
	xnr_user_no=request.args.get('xnr_user_no','')
	show_type=int(request.args.get('show_type',''))
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))   
	results=show_speech_warning(xnr_user_no,show_type,start_time,end_time)
	return json.dumps(results)


#时间预警
#http://219.224.134.213:9209/twitter_xnr_warning/show_date_warning/?account_name=admin@qq.com&start_time=1504195200&end_time=1512389253
@mod.route('/show_date_warning/')
def ajax_show_date_warning():
	account_name=request.args.get('account_name','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_date_warning(account_name,start_time,end_time)
	return json.dumps(results)

###事件涌现预警
#http://219.224.134.213:9209/twitter_xnr_warning/show_event_warming/?xnr_user_no=TXNR0001&start_time=1511755200&end_time=1511857583
@mod.route('/show_event_warming/')
def ajax_show_event_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_event_warming(xnr_user_no,start_time,end_time)
	return json.dumps(results)

#加入预警库
@mod.route('/addto_warning_corpus/')
def ajax_addto_warning_corpus():
	task_detail=dict()
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['warning_source']=request.args.get('warning_source','')
	task_detail['uid']=request.args.get('uid','')
	task_detail['tid']=request.args.get('tid','')
	task_detail['timestamp']=int(request.args.get('timestamp',''))
	task_detail['create_time']=int(time.time())
	results=addto_warning_corpus(task_detail)
	return json.dumps(results)


#上报
@mod.route('/report_warming_content/', methods=['POST'])
def ajax_report_warming_content():
	task_detail=dict()
	if request.method == 'POST':
		# print 'post method !!'
		data = json.loads(request.data)
		# print 'data:',data
		task_detail['report_type']=data['report_type'] #预警类型
		# print 'report_type:',task_detail['report_type']
		task_detail['report_time']=int(time.time())
		task_detail['xnr_user_no']=data['xnr_user_no']
		task_detail['event_name']=data['event_name']    #事件名称
		task_detail['uid']=data['uid']                 #人物预警uid

		task_detail['report_id']=data['report_id']   #上报内容的id

		#获取主要参与用户信息
		task_detail['user_info']=data['user_info']   #user_info=[uid,uid,……]	
		#获取典型信息
		task_detail['tw_info']=data['tw_info']   #tw_info=[{'tid':*,'timestamp':*},{'tid':*,'timestamp':*},……]
        
        #仅时间预警需要，其他的设为空
        task_detail['date_time']=data['date_time']
	# print 'type',type(task_detail),task_detail
	results=report_warming_content(task_detail)
	return json.dumps(results)