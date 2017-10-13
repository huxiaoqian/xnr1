#-*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from utils import get_influence_at_num,get_penetration_qq,get_safe_qq,get_influence_at_num_today,\
		get_penetration_qq_today,get_safe_qq_today

mod = Blueprint('qq_xnr_assessment', __name__, url_prefix='/qq_xnr_assessment')


# 影响力评估
@mod.route('/influence_qq/')
def ajax_influence_mark():
	xnr_user_no = request.args.get('xnr_user_no','')
	start_time = request.args.get('start_time','')
	end_time = request.args.get('end_time','')

	results = get_influence_at_num(xnr_user_no,start_time,end_time)

	return json.dumps(results)

# 影响力评估 -- 今日
@mod.route('/influence_qq_today/')
def ajax_influence_mark():
	xnr_user_no = request.args.get('xnr_user_no','')

	results = get_influence_at_num_today(xnr_user_no)

	return json.dumps(results)


# 渗透力评估
@mod.route('/penetration_qq/') 
def ajax_penetration_qq():
	xnr_user_no = request.args.get('xnr_user_no','')
	start_time = request.args.get('start_time','')
	end_time = request.args.get('end_time','')
	
	results = get_penetration_qq(xnr_user_no,start_time,end_time)

	return json.dumps(results)

# 渗透力评估 -- 今日
@mod.route('/penetration_qq_today/') 
def ajax_penetration_qq():
	xnr_user_no = request.args.get('xnr_user_no','')

	results = get_penetration_qq_today(xnr_user_no)

	return json.dumps(results)


# 安全性评估
@mod.route('/safe_qq/')
def ajax_safe_qq():
	xnr_user_no = request.args.get('xnr_user_no','')
	start_time = request.args.get('start_time','')
	end_time = request.args.get('end_time','')
	
	results = get_safe_qq(xnr_user_no,start_time,end_time)

	return json.dumps(results)

# 安全性评估 -- 今日
@mod.route('/safe_qq_today/')
def ajax_safe_qq():
	xnr_user_no = request.args.get('xnr_user_no','')

	results = get_safe_qq_today(xnr_user_no)

	return json.dumps(results)

@mod.route('/show_safe_feature/')
def ajax_show_safe_feature():
    results = True
    return json.dumps(results)
