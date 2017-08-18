#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_xnr
from utils import show_report_content

mod=Blueprint('weibo_xnr_report_manage',__name__,url_prefix='/weibo_xnr_report_manage')


'''
上报管理
'''
#显示上报内容
@mod.route('/show_report_content/')
def ajax_show_report_content():
	results=show_report_content()
	return json.dumps(results)