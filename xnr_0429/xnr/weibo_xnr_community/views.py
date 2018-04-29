#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_trace_community,show_new_community,get_community_warning,get_community_detail,\
                  update_trace_status,delete_community,upadate_community,\
                  delete_opnions_corpus,upadate_opnions_corpus

from global_config import S_TYPE,WEIBO_COMMUNITY_DATE
from time_utils import ts2datetime,datetime2ts

mod = Blueprint('weibo_xnr_community', __name__, url_prefix='/weibo_xnr_community')


##社区预警主页
# 跟踪社区列表
# 输入：xnr_user_no
# 输出：
#http://219.224.134.213:9207/weibo_xnr_community/show_trace_community/?xnr_user_no=WXNR0004
@mod.route('/show_trace_community/')
def ajax_show_trace_community():
    xnr_user_no = request.args.get('xnr_user_no','')
    now_time = int(time.time())
    result = show_trace_community(xnr_user_no,now_time)
    return json.dumps(result)


#操作：取消跟踪和强制跟踪
#http://219.224.134.213:9207/weibo_xnr_community/update_trace_status/?community_id=WXNR0004_2016-11-20宝宝_一道&trace_status=-2
@mod.route('/update_trace_status/')
def ajax_update_trace_status():
    community_id = request.args.get('community_id','')
    trace_status = int(request.args.get('trace_status',''))   #1 跟踪社区，-1 放弃跟踪社区，-2 强制跟踪
    now_time = int(time.time())
    # print 'trace_status:',trace_status
    # print 'community_id:',community_id
    result = update_trace_status(community_id,trace_status,now_time)
    return json.dumps(result)


#新社区列表
#http://219.224.134.213:9207/weibo_xnr_community/show_new_community/?xnr_user_no=WXNR0004
@mod.route('/show_new_community/')
def ajax_show_new_community():
    xnr_user_no = request.args.get('xnr_user_no','')
    now_time = int(time.time())
    result = show_new_community(xnr_user_no,now_time)
    return json.dumps(result)


## 预警详情
#http://219.224.134.213:9207/weibo_xnr_community/get_community_warning/?xnr_user_no=WXNR0004&community_id=WXNR0004_2016-11-20宝宝_一道&start_time=1521728241&end_time=1522333041
@mod.route('/get_community_warning/')
def ajax_get_community_warning():
    xnr_user_no = request.args.get('xnr_user_no','')
    community_id = request.args.get('community_id','')
    #时间默认进入界面时传当前时间为end_time；start_time为当前时间-7天（即前7天）
    start_time = int(request.args.get('start_time','')) 
    end_time = int(request.args.get('end_time',''))
    result = get_community_warning(xnr_user_no,community_id,start_time,end_time)
    return json.dumps(result)


## 社区详情
#输入：
#     model——'user','content','netgragh'
#     order_by——'sensitive','retweeted','timestamp'
#     community_id——社区编号
#输出：
#测试：
#http://219.224.134.213:9207/weibo_xnr_community/get_community_detail/?model=content&order_by=sensitive&community_id=WXNR0004_2016-11-20宝宝_一道
#http://219.224.134.213:9207/weibo_xnr_community/get_community_detail/?model=user&order_by=retweeted&community_id=WXNR0004_2016-11-20宝宝_一道
#http://219.224.134.213:9207/weibo_xnr_community/get_community_detail/?model=netgragh&order_by=timestamp&community_id=WXNR0004_2016-11-20宝宝_一道

@mod.route('/get_community_detail/')
def ajax_get_community_detail():
    if S_TYPE == 'test':
        now_time = datetime2ts(WEIBO_COMMUNITY_DATE)
    else:
        now_time = int(time.time())
    model = request.args.get('model','')
    community_id = request.args.get('community_id','')
    order_by = request.args.get('order_by','')
    result = get_community_detail(now_time,model,community_id,order_by)
    return json.dumps(result)
 


# 社交网络中的用户信息
@mod.route('/get_user_detail/')
def ajax_get_user_detail():
	uid = request.args.get('uid','')
	result = get_user_detail(uid)
	return json.dumps(result)


#不需要连接
#http://219.224.134.213:9207/weibo_xnr_community/delete_community/?community_id=WXNR0004_2016-11-20哆啦_绿茶_2016-11-19
@mod.route('/delete_community/')
def ajax_delete_community():
    community_id = request.args.get('community_id','')    
    result = delete_community(community_id)
    return json.dumps(result)

#http://219.224.134.213:9207/weibo_xnr_community/upadate_community/?community_id=WXNR0004_2016-11-20峰峰_丸子_2016-11-27
@mod.route('/upadate_community/')
def ajax_upadate_community():
    community_id = request.args.get('community_id','')    
    result = upadate_community(community_id)
    return json.dumps(result)

#http://219.224.134.213:9207/weibo_xnr_community/delete_opnions_corpus/?task_id=1_2_3
@mod.route('/delete_opnions_corpus/')
def ajax_delete_opnions_corpus():
    task_id = request.args.get('task_id','')    
    result = delete_opnions_corpus(task_id)
    return json.dumps(result)

#http://219.224.134.213:9207/weibo_xnr_community/upadate_opnions_corpus/?task_id=chuang_ye
@mod.route('/upadate_opnions_corpus/')
def ajax_upadate_opnions_corpus():
    task_id = request.args.get('task_id','')      
    result = upadate_opnions_corpus(task_id)
    return json.dumps(result)