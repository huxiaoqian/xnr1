#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_flow_text
from utils import lookup_weibo_keywordstring,lookup_hot_posts,lookup_active_weibouser

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
    result=lookup_hot_posts(float(from_ts),float(to_ts),weiboxnr_id,classify_id,search_content,order_id)
    return json.dumps(result)

@mod.route('/lookup_active_weibouser/')
def ajax_lookup_active_weibouser():
    weiboxnr_id=request.args.get('weiboxnr_id','')
    classify_id=request.args.get('classify_id','')
    result=lookup_active_weibouser(classify_id,weiboxnr_id)
    return json.dumps(result)
