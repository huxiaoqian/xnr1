#-*- coding:utf-8 -*-

import os
import time
import json
import random
import pinyin
from flask import Flask, Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_xnr as es, es_flow_text
from xnr.global_config import S_TYPE
from xnr.time_utils import datetime2ts, ts2datetime
from utils import get_create_writing_task, get_show_writing_task, get_delete_writing_task,\
                get_topics_river, get_symbol_weibo, get_opinions_results, get_model_text_results

mod = Blueprint('intelligent_writing', __name__, url_prefix='/intelligent_writing')

'''
智能写作
'''

# 创建任务
#http://219.224.134.213:9090/intelligent_writing/create_writing_task/?task_source=facebook&xnr_user_no=FXNR0005&task_name=测试任务
#&event_keywords=十九大，习近平&opinion_keywords=十九大，习近平，常委&opinion_type=positive&submitter=admin@qq.com

@mod.route('/create_writing_task/')
def ajax_create_writing_task():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['task_name'] = request.args.get('task_name','')
    task_detail['task_name_pinyin'] = pinyin.get(task_detail['task_name'],format='strip',delimiter='_')
    task_detail['event_keywords'] = request.args.get('event_keywords','')  # 不同的关键词之间中文逗号“，”分隔。
    task_detail['opinion_keywords'] = request.args.get('opinion_keywords','')  # 不同的关键词之间中文逗号“，”分隔。
    task_detail['opinion_type'] = request.args.get('opinion_type','') # 使用英文：all - 全部  positive - 积极  negtive - 消极
    task_detail['create_time'] = int(time.time())
    task_detail['submitter'] = request.args.get('submitter','admin@qq.com') # 管理员
    task_detail['compute_status'] = 0  # 0-尚未计算 1- 正在计算 2- 计算完成
    task_detail['task_source'] = request.args.get('task_source','')  # 使用英文：weibo、facebook、twitter

    mark = get_create_writing_task(task_detail)  # exists-表示任务名称已经存在 True-成功，False-失败

    return json.dumps(mark)

# 展示任务
#http://219.224.134.213:9090/intelligent_writing/show_writing_task/?task_source=facebook&xnr_user_no=FXNR0005

@mod.route('/show_writing_task/')
def ajax_show_writing_task():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['task_source'] = request.args.get('task_source','')  # 使用英文：weibo、facebook、twitter

    results = get_show_writing_task(task_detail)

    return json.dumps(results)

# 删除任务
#http://219.224.134.213:9090/intelligent_writing/delete_writing_task/?task_id=facebook_fxnr0005_ce_shi_ren_wu

@mod.route('/delete_writing_task/')
def ajax_delete_writing_task():
    task_detail = dict()
    task_detail['task_id'] = request.args.get('task_id','')

    mark = get_delete_writing_task(task_detail)

    return json.dumps(mark) # True - 成功 False-失败


# 事件摘要 - 主题河
# http://219.224.134.213:9090/intelligent_writing/topics_river/?task_id=facebook_fxnr0005_ce_shi_ren_wu&task_source=facebook&pointInterval=3600&start_ts=1517461822&end_ts=1517893822
# http://219.224.134.213:9090/intelligent_writing/topics_river/?task_id=weibo_wxnr0004_ce_shi_ren_wu_3&task_source=weibo&pointInterval=3600&start_ts=1517461822&end_ts=1517893822

@mod.route('/topics_river/')
def topics_river():
    task_source = request.args.get('task_source','')  # weibo,facebook,twitter
    task_id = request.args.get('task_id','')
    during = request.args.get('pointInterval',60*60) # 默认查询时间粒度为3600秒
    during = int(during)
    end_ts = request.args.get('end_ts', '')  # create_time 
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '') # create_time - 5*36*2400 (因为搜的5天的流数据)
    start_ts = long(start_ts)
    #weibo_count = all_weibo_count(topic,start_ts,end_ts)
    topic_count = get_topics_river(task_source,task_id,start_ts,end_ts,during)
    return json.dumps(topic_count)

# 事件摘要 - 时间轴
#http://219.224.134.213:9090/intelligent_writing/symbol_weibos/?task_source=weibo&task_id=weibo_wxnr0004_ce_shi_ren_wu_3&task_source=weibo&pointInterval=3600&start_ts=1517461822&end_ts=1517893822

@mod.route('/symbol_weibos/')
def symbol_weibos():
    # topic = request.args.get('topic','')

    task_source = request.args.get('task_source','')
    task_id = request.args.get('task_id','')
    during = request.args.get('pointInterval',60*60) # 默认查询时间粒度为3600秒
    during = int(during)
    end_ts = request.args.get('end_ts', '')
    end_ts = long(end_ts)
    start_ts = request.args.get('start_ts', '')
    start_ts = long(start_ts)
    weibo_content = get_symbol_weibo(task_source,task_id,start_ts,end_ts,during)
    return json.dumps(weibo_content)

# 各类观点
#http://219.224.134.213:9090/intelligent_writing/opinions_all/?task_id=weibo_wxnr0004_ce_shi_ren_wu_3&intel_type=all
@mod.route('/opinions_all/')
def ajax_opinions_all():

    task_id = request.args.get('task_id','')
    intel_type = request.args.get('intel_type','') # all - 代表者观点，follow-关注者观点，influence-高影响力用户，sensitive-高敏感度用户

    results = get_opinions_results(task_id,intel_type)

    return json.dumps(results)

# 发帖模板
# 单极性：http://219.224.134.213:9090/intelligent_writing/model_text/?task_id=twitter_txnr0001_ce_shi_ren_wu___0_2_2_8&model_type=single&text_type=positive
# 双极性：http://219.224.134.213:9090/intelligent_writing/model_text/?task_id=twitter_txnr0001_ce_shi_ren_wu___0_2_2_8&model_type=double&double_order=although_positive
# 事实性陈述：http://219.224.134.213:9090/intelligent_writing/model_text/?task_id=twitter_txnr0001_ce_shi_ren_wu___0_2_2_8&model_type=news&text_type=positive

@mod.route('/model_text/')
def ajax_model_text():

    task_detail = dict()
    task_detail['task_id'] = request.args.get('task_id','')
    task_detail['model_type'] = request.args.get('model_type','') # single-单极性，double-双极性，news-事实陈述
    #task_detail['polar_type'] = request.args.get('polar_type','') # agree-赞成，object-反对
    task_detail['text_type'] = request.args.get('text_type','') # positive-正向，negtive-负向
    task_detail['double_order'] = request.args.get('double_order','') # although_positive-虽然正向，但是负向，although_negtive-虽然正向，但是负向，

    results = get_model_text_results(task_detail)

    return json.dumps(results)