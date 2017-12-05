#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_personnal_warming,show_speech_warming,show_date_warming
                  #show_event_warming,\                  
				  #,addto_speech_warming,\				  
				  #,report_warming_content,get_hashtag


mod = Blueprint('weibo_xnr_warming_new', __name__, url_prefix='/weibo_xnr_warming_new')

#人物行为预警
#http://219.224.134.213:9209/weibo_xnr_warming_new/show_personnal_warming/?xnr_user_no=WXNR0004&start_time=1511755200&end_time=1511857583
@mod.route('/show_personnal_warming/')
def ajax_show_personnal_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	results=show_personnal_warming(xnr_user_no,start_time,end_time)
	return json.dumps(results)


#言论内容预警
#show_type=0,全部用户；1，关注用户；2，未关注用户
#http://219.224.134.213:9209/weibo_xnr_warming_new/show_speech_warming/?xnr_user_no=WXNR0004&show_type=0&start_time=1511755200&end_time=1511857583
@mod.route('/show_speech_warming/')
def ajax_show_speech_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	show_type=int(request.args.get('show_type',''))
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))   
	results=show_speech_warming(xnr_user_no,show_type,start_time,end_time)
	return json.dumps(results)

#时间预警
#http://219.224.134.213:9209/weibo_xnr_warming_new/show_date_warming/?account_name=admin@qq.com&start_time=1511668800&end_time=1512389253
@mod.route('/show_date_warming/')
def ajax_show_date_warming():
	account_name=request.args.get('account_name','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_date_warming(account_name,start_time,end_time)
	return json.dumps(results)


###事件涌现预警
#http://219.224.134.213:9209/weibo_xnr_warming/show_event_warming/?xnr_user_no=WXNR0004&start_time=1511668800&end_time=1512389253
@mod.route('/show_event_warming/')
def ajax_show_event_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_event_warming(xnr_user_no,start_time,end_time)
	return json.dumps(results)