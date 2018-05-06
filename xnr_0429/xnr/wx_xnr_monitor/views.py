# -*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from xnr.parameter import MAX_VALUE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts
from utils import utils_search, utils_show_sensitive_users, utils_report_warning_content,\
		utils_report_warning_content_new

mod = Blueprint('wx_xnr_monitor', __name__, url_prefix='/wx_xnr_monitor')

#默认加载最近30天的数据
@mod.route('/search/')
def search():
    wxbot_id = request.args.get('wxbot_id', '')
    period = request.args.get('period', '')
    startdate = request.args.get('startdate', '')   #str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id:
        if period or (startdate and enddate):
            res = utils_search(wxbot_id, period, startdate, enddate)
            if res:
                return json.dumps(res)
    return json.dumps({})  

@mod.route('/show_sensitive_users/')
def show_sensitive_users():
    wxbot_id = request.args.get('wxbot_id', '')
    period = request.args.get('period', '')
    startdate = request.args.get('startdate', '')	#str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id:
        if period or (startdate and enddate):
            res = utils_show_sensitive_users(wxbot_id, period, startdate, enddate)
            if res:
                return json.dumps(res)
    return json.dumps({}) 

@mod.route('/report_warning_content/')
def report_warning_content():
    report_time = int(time.time())
    wxbot_id = request.args.get('wxbot_id', '')
    report_type = request.args.get('report_type', '') #content/user
    speaker_id = request.args.get('speaker_id', '')# sensitive speaker puid
    wx_content_info_str = request.args.get('report_content', '')
    if wxbot_id and report_type and speaker_id and wx_content_info_str:
        res = utils_report_warning_content(wxbot_id, report_type, report_time, speaker_id, wx_content_info_str)
        if res:
            return json.dumps(res)
    return json.dumps({}) 
    
    #test
    '''
    wx_content_info = [{'speaker_id':'841319111', "sensitive_value": 1,\
            "sensitive_words_string": "\u8fbe\u8d56", "text": "\u8fbe\u8d56",\
            "speaker_nickname": "hxq", "timestamp": 1506567359, \
            "group_puid": "531811289"}]
    '''

@mod.route('/report_warning_content_new/', methods=['POST'])
def report_warning_content_new():
    if request.method == 'POST':
	data = request.form
	if not data:
	    data = json.loads(request.data)
	report_time = int(time.time())
        wxbot_id = data['wxbot_id']
        report_type = data['report_type'] #人物/言论
    	speaker_id = data['speaker_id']# sensitive speaker puid
    	wx_content_info_str = data['report_content']
    	if wxbot_id and report_type and speaker_id and wx_content_info_str:
            res = utils_report_warning_content(wxbot_id, report_type, report_time, speaker_id, wx_content_info_str)
            if res:
                return json.dumps(res)
    return json.dumps({})

