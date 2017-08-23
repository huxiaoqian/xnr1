#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_personnal_warming,\
				  show_event_warming,\
				  show_speech_warming


mod = Blueprint('weibo_xnr_warming', __name__, url_prefix='/weibo_xnr_warming')

###人物行为预警
#显示预警内容
#http://219.224.134.213:9209/weibo_xnr_warming/show_personnal_warming/?xnr_user_no=WXNR0002&day_time=1480176000
@mod.route('/show_personnal_warming/')
def ajax_show_personnal_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	day_time=request.args.get('day_time','')
	#day_time=time.time()
	results=show_personnal_warming(xnr_user_no,day_time)
	return json.dumps(results)

###言论内容预警
#显示预警内容
@mod.route('/show_speech_warming/')
def ajax_show_speech_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	show_type
	day_time=request.args.get('day_time','') 
	#day_time=time.time()     
	results=show_speech_warming(xnr_user_no,show_type,day_time)
	return json.dumps(results)


###事件涌现预警
#显示预警内容
@mod.route('/show_event_warming/')
def ajax_show_event_warming():
	results=show_event_warming()
	return json.dumps(results)


