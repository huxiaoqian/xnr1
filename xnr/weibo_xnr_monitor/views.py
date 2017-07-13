#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_flow_text
from utils import lookup_weibo_keywordstring,lookup_hot_posts,\
        lookup_weibo_users,lookup_weibo_info,aggs_test,\
        count_weiboxnr_keyword

mod=Blueprint('weibo_xnr_monitor',__name__,url_prefix='/weibo_xnr_monitor')

#function 1:lookup_weibo_keywordstiing to create wordcloud
@mod.route('/lookup_weibo_keywordstring/')
def ajax_lookup_weibo_keywordstring():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    weiboxnr_id=request.args.get('weiboxnr_id','')
    result=lookup_weibo_keywordstring(float(from_ts),float(to_ts),weiboxnr_id)
    return json.dumps(result)

@mod.route('/lookup_hot_posts/')
def ajax_lookup_hot_posts():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    weiboxnr_id=request.args.get('weiboxnr_id','')
    classify_id=request.args.get('classify_id','')
    search_content=request.args.get('search_content','')
    order_id=request.args.get('order_id','')
    result=lookup_hot_posts(from_ts,to_ts,weiboxnr_id,classify_id,search_content,order_id)
    return json.dumps(result)
    
#test code
@mod.route('/aggs_test/')
def ajax_aggs_test():
    results={}
    results=aggs_test()
    return json.dumps(results)

#lookup weibo_xnr info
@mod.route('/lookup_weibo_users/')
def ajax_lookup_weibo_users():
    results={}
    results=lookup_weibo_users()
    return json.dumps(results)

#lookup weibo keywordslist test
@mod.route('/lookup_weibo_keywords/')
def ajax_lookup_weibo_keywords():
    results={}
    results=lookup_weiboxnr_keywordslist()
    return json.dumps(results)

#lookup weibo info
@mod.route('/lookup_weibo_info/')
def ajax_lookup_weibo_info():
    results={}
    ts_first='2016/11/15 10:27:12'
    ts_second='2016/11/15 10:27:14'
    firsttime=datetime.datetime.strptime(ts_first,'%Y/%m/%d %H:%M:%S')
    secondtime=datetime.datetime.strptime(ts_second,'%Y/%m/%d %H:%M:%S')
    userlist=[3033874187,2604977652,3936969641,3964892488]
    results=lookup_weibo_info(firsttime,secondtime,userlist)
    word_list=count_weiboxnr_keyword(results)
    return json.dumps(word_list)

