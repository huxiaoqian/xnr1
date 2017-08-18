#-*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
        abort, flash, session, redirect
from xnr.global_utils import es_flow_text
from utils import get_influ_fans_num,get_influ_retweeted_num,\
				get_influ_commented_num,get_influ_like_num,get_influ_at_num,get_influ_private_num,\
				compute_influence_num

mod = Blueprint('weibo_xnr_assessment', __name__, url_prefix='/weibo_xnr_assessment')


'''
影响力评估
'''
# 影响力分数计算
@mod.route('/influence_mark/')
def ajax_influ_mark_compute():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = compute_influence_num(xnr_user_no)

	return json.dumps(results)

# 粉丝数
@mod.route('/influ_fans_num/')
def ajax_influ_fans_num():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influ_fans_num(xnr_user_no)
	return json.dumps(results)
'''
# 粉丝群的粉丝数
@mod.route('/influ_fans_fans_num/')
def ajax_influ_fans_fans_num():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influ_fans_fans_num(xnr_user_no)

	return json.dumps(results)
'''
# 被转发
@mod.route('/influ_retweeted_num/')
def ajax_influ_retweeted_num():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influ_retweeted_num(xnr_user_no)

	return json.dumps(results)

# 被评论
@mod.route('/influ_commented_num/')
def ajax_influ_commented_num():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influ_commented_num(xnr_user_no)

	return json.dumps(results)

# 被点赞
@mod.route('/influ_like_num/')
def ajax_influ_like_num():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influ_like_num(xnr_user_no)

	return json.dumps(results)

# 被@
@mod.route('/influ_at_num/')
def ajax_influ_at_num():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influ_at_num(xnr_user_no)

	return json.dumps(results)

# 被私信
@mod.route('/influ_private_num/')
def ajax_influ_private_num():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influ_private_num(xnr_user_no)

	return json.dumps(results)

'''
渗透力评估
'''




'''
安全性评估
'''



@mod.route('/show_safe_feature/')
def ajax_show_safe_feature():
    results = True
    return json.dumps(results)
