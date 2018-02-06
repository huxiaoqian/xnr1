#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from utils import show_report_content

mod=Blueprint('facebook_xnr_report_manage',__name__,url_prefix='/facebook_xnr_report_manage')


#上报显示新方法
@mod.route('/show_report_content/')
def ajax_show_report_content():
    report_type=request.args.get('report_type','').split(',')
    start_time=int(request.args.get('start_time',''))
    end_time=int(request.args.get('end_time',''))
    results=show_report_content(report_type,start_time,end_time)
    return json.dumps(results)   


@mod.route('/output_excel_word/') 
def ajax_output_excel_word():
    id_list=request.args.get('id_list','').split(',')
    out_type=request.args.get('out_type','')
    report_timelist=request.args.get('report_timelist','').split(',')
    results=output_excel_word(id_list,out_type,report_timelist)
    return json.dumps(results)