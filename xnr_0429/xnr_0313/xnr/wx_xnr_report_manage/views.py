#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect
from utils import utils_show_report_content

mod=Blueprint('wx_xnr_report_manage',__name__,url_prefix='/wx_xnr_report_manage')

@mod.route('/show_report_content/')
def show_report_content():
    wxbot_id = request.args.get('wxbot_id', '')
    report_type = request.args.get('report_type', '')
    period = request.args.get('period', '')
    startdate = request.args.get('startdate', '')   #str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id and report_type:
        if period or (startdate and enddate):
            res = utils_show_report_content(wxbot_id, report_type, period, startdate, enddate)
            if res:
                return json.dumps(res)
    return None 


