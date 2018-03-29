#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_trace_community,show_new_community,get_community_warning,get_community_detail


mod = Blueprint('weibo_xnr_community', __name__, url_prefix='/weibo_xnr_community')


##社区预警主页
# 跟踪社区列表
# 输入：xnr_user_no
# 输出：
@mod.route('/show_trace_community/')
def ajax_show_trace_community():
    xnr_user_no = request.args.get('xnr_user_no','')
    now_time = int(time.time())
    result = show_trace_community(xnr_user_no,now_time)
    return json.dumps(result)


#新社区列表
@mod.route('/show_new_community/')
def ajax_show_new_community():
    xnr_user_no = request.args.get('xnr_user_no','')
    now_time = int(time.time())
    result = show_new_community(xnr_user_no,now_time)
    return json.dumps(result)

## 预警详情
@mod.route('/get_community_warning/')
def ajax_get_community_warning():
    xnr_user_no = request.args.get('xnr_user_no','')
    community_id = request.args.get('community_id','')
    result = get_community_warning(xnr_user_no,community_id)
    return json.dumps(result)

## 社区详情
@mod.route('/get_community_detail/')
def ajax_get_community_detail():
    now_time = int(time.time())
    model = request.args.get('model','')
    community_id = request.args.get('community_id','')	
    result = get_community_detail(now_time,community_id)
    return json.dumps(result)
 