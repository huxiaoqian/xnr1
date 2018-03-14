#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.parameter import MAX_VALUE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts

from utils import lookup_weibo_keywordstring,lookup_hot_posts,lookup_active_user,addto_twitter_corpus
 

mod = Blueprint('twitter_xnr_monitor', __name__, url_prefix='/twitter_xnr_monitor')


#关键词云
#http://219.224.134.213:9209/twitter_xnr_monitor/lookup_weibo_keywordstring/?from_ts=1514736000&to_ts=1514908800&xnr_no=TXNR0001
@mod.route('/lookup_weibo_keywordstring/')
def ajax_lookup_weibo_keywordstring():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    xnr_no=request.args.get('xnr_no','')
    result=lookup_weibo_keywordstring(int(from_ts),int(to_ts),xnr_no)
    return json.dumps(result)


#热门帖子
#排序order_id，按时间排序：1，按热度排序：2，按敏感度排序：3，默认按时间排序
#分类classify_id，全部用户 0，关注 1，非关注-1
#默认时间范围：一周内
#http://219.224.134.213:9209/twitter_xnr_monitor/lookup_hot_posts/?from_ts=1514736000&to_ts=1514908800&xnr_no=TXNR0001&classify_id=0&order_id=1
@mod.route('/lookup_hot_posts/')
def ajax_lookup_hot_posts():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    xnr_no=request.args.get('xnr_no','')
    classify_id=int(request.args.get('classify_id',''))
    order_id=int(request.args.get('order_id',''))
    result=lookup_hot_posts(float(from_ts),float(to_ts),xnr_no,classify_id,order_id)
    return json.dumps(result)


#活跃用户
#http://219.224.134.213:9209/twitter_xnr_monitor/lookup_active_user/?from_ts=1514736000&to_ts=1514908800&xnr_no=TXNR0001&classify_id=0
@mod.route('/lookup_active_user/')
def ajax_lookup_active_user():
    xnr_no=request.args.get('xnr_no','')
    classify_id=int(request.args.get('classify_id',''))
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    result=lookup_active_user(classify_id,xnr_no,int(from_ts),int(to_ts))
    return json.dumps(result)


#加入语料库
@mod.route('/addto_twitter_corpus/')
def ajax_addto_twitter_corpus():
    task_detail=dict()
    task_detail['corpus_type']=request.args.get('corpus_type','')
    task_detail['theme_daily_name']=request.args.get('theme_daily_name','').split(',')
    task_detail['uid']=request.args.get('uid','')
    task_detail['tid']=request.args.get('tid','')
    task_detail['timestamp']=int(request.args.get('timestamp',''))
    task_detail['create_type']=request.args.get('create_type','')
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['create_time']=int(time.time())
    results=addto_twitter_corpus(task_detail)
    return json.dumps(results)
