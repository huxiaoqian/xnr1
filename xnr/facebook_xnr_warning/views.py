#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

#from utils import show_personnal_warning,show_speech_warning
                  #show_event_warning,\                  
				  #,addto_speech_warning,\
				  #show_date_warning,report_warning_content,get_hashtag


mod = Blueprint('facebook_xnr_warning', __name__, url_prefix='/facebook_xnr_warning')

# #人物行为预警
# #http://219.224.134.213:9209/facebook_xnr_warning/show_personnal_warning/?xnr_user_no=WXNR0004&start_time=1511755200&end_time=1511857583
# @mod.route('/show_personnal_warning/')
# def ajax_show_personnal_warning():
# 	xnr_user_no=request.args.get('xnr_user_no','')
# 	start_time=int(request.args.get('start_time',''))
# 	end_time=int(request.args.get('end_time',''))
# 	results=show_personnal_warning(xnr_user_no,start_time,end_time)
# 	return json.dumps(results)


# #言论内容预警
# #show_type=0,全部用户；1，关注用户；2，未关注用户
# #http://219.224.134.213:9209/facebook_xnr_warning/show_speech_warning/?xnr_user_no=WXNR0004&show_type=0&start_time=1511755200&end_time=1511857583
# @mod.route('/show_speech_warning/')
# def ajax_show_speech_warning():
# 	xnr_user_no=request.args.get('xnr_user_no','')
# 	show_type=int(request.args.get('show_type',''))
# 	start_time=int(request.args.get('start_time',''))
# 	end_time=int(request.args.get('end_time',''))   
# 	results=show_speech_warning(xnr_user_no,show_type,start_time,end_time)
# 	return json.dumps(results)