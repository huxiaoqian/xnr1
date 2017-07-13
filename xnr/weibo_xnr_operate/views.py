#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from utils import push_keywords_task

mod = Blueprint('weibo_xnr_operate', __name__, url_prefix='/weibo_xnr_operate')


@mod.route('/submit_daily_tweet/')
def ajax_submit_daily_tweet():
    
    return json.dumps(result)

## 热点跟随：内容推荐和子观点分析的提交关键词任务
@mod.route('/submit_hot_keyword_task/')
def ajax_submit_hot_keyword_task():
	#mark = True
	task_detail = dict()
	task_detail['task_id'] = json.dumps(request.args.get('task_id','')) # 当前代表微博的mid 
	task_detail['keywords_string'] = request.args.get('keywords_string','') # 提交的关键词，以中文逗号分隔“，”
	task_detail['compute_status'] = 0 # 尚未计算
	task_detail['submit_time'] = time.time() # 当前时间
	task_detail['submit_user'] = request.args.get('submit_user','admin@qq.com') 

	mark = push_keywords_task(task_detail)

	return json.dumps(mark)  # 建立成功为True,失败为False
