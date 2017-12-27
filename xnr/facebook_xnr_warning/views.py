#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_personnal_warning,show_speech_warning,show_date_warning,show_event_warming,\
                  update_fb_flow_text

mod = Blueprint('facebook_xnr_warning', __name__, url_prefix='/facebook_xnr_warning')

#人物行为预警
#http://219.224.134.213:9209/facebook_xnr_warning/show_personnal_warning/?xnr_user_no=FXNR0001&start_time=1511755200&end_time=1511857583
@mod.route('/show_personnal_warning/')
def ajax_show_personnal_warning():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	results=show_personnal_warning(xnr_user_no,start_time,end_time)
	return json.dumps(results)


#言论内容预警
#show_type=0,全部用户；1，关注用户；2，未关注用户
#http://219.224.134.213:9209/facebook_xnr_warning/show_speech_warning/?xnr_user_no=FXNR0001&show_type=0&start_time=1511755200&end_time=1511857583
@mod.route('/show_speech_warning/')
def ajax_show_speech_warning():
	xnr_user_no=request.args.get('xnr_user_no','')
	show_type=int(request.args.get('show_type',''))
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))   
	results=show_speech_warning(xnr_user_no,show_type,start_time,end_time)
	return json.dumps(results)


#时间预警
#http://219.224.134.213:9209/facebook_xnr_warning/show_date_warning/?account_name=admin@qq.com&start_time=1504195200&end_time=1512389253
@mod.route('/show_date_warning/')
def ajax_show_date_warning():
	account_name=request.args.get('account_name','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_date_warning(account_name,start_time,end_time)
	return json.dumps(results)


###事件涌现预警
#http://219.224.134.213:9209/facebook_xnr_warning/show_event_warming/?xnr_user_no=FXNR0001&start_time=1511755200&end_time=1511857583
@mod.route('/show_event_warming/')
def ajax_show_event_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_event_warming(xnr_user_no,start_time,end_time)
	return json.dumps(results)



#http://219.224.134.213:9209/facebook_xnr_warning/update_fb_flow_text
@mod.route('/update_fb_flow_text/')
def ajax_update_fb_flow_text():
	#task_id='328762654255381'
	#task_id='328760217588958'
	#task_id='1555096127914839'
	#task_id='1554860021271783'
	task_id='1554849701272815'
	sensitive=1
	results=update_fb_flow_text(task_id,sensitive)
	return json.dumps(results)