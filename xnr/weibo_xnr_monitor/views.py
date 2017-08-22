#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_flow_text
from utils import lookup_weibo_keywordstring,lookup_hot_posts,lookup_active_weibouser,\
                  weibo_user_test,lookup_weiboxnr_concernedusers,weibo_user_detail,\
                  addto_weibo_corpus,get_weibohistory_retweet,get_weibohistory_comment,\
                  get_weibohistory_like,attach_fans_follow,addto_weibo_corpus,attach_fans_batch

mod=Blueprint('weibo_xnr_monitor',__name__,url_prefix='/weibo_xnr_monitor')

#test:http://219.224.134.213:9209/weibo_xnr_monitor/lookup_weibo_keywordstring/?from_ts=1479513600&to_ts=1479981600&weiboxnr_id=WXNR0002
#function 1:lookup_weibo_keywordstiing to create wordcloud
@mod.route('/lookup_weibo_keywordstring/')
def ajax_lookup_weibo_keywordstring():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    weiboxnr_id=request.args.get('weiboxnr_id','')
    result=lookup_weibo_keywordstring(float(from_ts),float(to_ts),weiboxnr_id)
    return json.dumps(result)

#test:http://219.224.134.213:9209/weibo_xnr_monitor/lookup_hot_posts/?from_ts=1479513600&to_ts=1479981600&weiboxnr_id=WXNR0002&classify_id=1&order_id=1
@mod.route('/lookup_hot_posts/')
def ajax_lookup_hot_posts():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    weiboxnr_id=request.args.get('weiboxnr_id','')
    classify_id=request.args.get('classify_id','')
    #search_content=request.args.get('search_content','')
    order_id=request.args.get('order_id','')
    result=lookup_hot_posts(float(from_ts),float(to_ts),weiboxnr_id,classify_id,order_id)
    return json.dumps(result)

#############微博相关操作########

#转发
@mod.route('/get_weibohistory_retweet/')
def ajax_get_weibohistory_retweet():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','')    #text指转发时发布的内容
    results=get_weibohistory_retweet(task_detail)
    return json.dumps(results)

#评论
@mod.route('/get_weibohistory_comment/')
def ajax_get_weibohistory_comment():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','')    #text指转发时发布的内容
    results=get_weibohistory_comment(task_detail)
    return json.dumps(results)

#赞
@mod.route('/get_weibohistory_like/')
def ajax_get_weibohistory_like():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    results=get_weibohistory_like(task_detail)
    return json.dumps(results)

#直接关注
@mod.route('/attach_fans_follow/')
def ajax_attach_fans_follow():
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['uid']=request.args.get('uid','')
    results=attach_fans_follow(task_detail)
    return json.dumps(results)

#加入语料库
#task_detail=[corpus_type,theme_daily_name,text,uid,mid,timestamp,retweeted,comment,like,create_type]
@mod.route('/addto_weibo_corpus/')
def ajax_addto_weibo_corpus():
    corpus_type=request.args.get('corpus_type','')
    theme_daily_name=request.args.get('theme_daily_name','')
    text=request.args.get('text','')
    uid=request.args.get('uid','')
    mid=request.args.get('mid','')
    timestamp=request.args.get('timestamp','')
    retweeted=request.args.get('retweeted','')
    comment=request.args.get('comment','')
    like=request.args.get('like','')
    create_type=request.args.get('create_type','')
    task_detail=[corpus_type,theme_daily_name,text,uid,mid,timestamp,retweeted,comment,like,create_type]
    results=addto_weibo_corpus(task_detail)
    return json.dumps(results)

#批量添加关注
@mod.route('/attach_fans_batch/')
def ajax_attach_fans_batch():
    xnr_user_no_list=request.args.get('xnr_user_no','')   #虚拟人no的list
    fans_id_list=request.args.get('fans_id','')           #勾选的活跃用户id的list
    results=attach_fans_batch(xnr_user_no_list,fans_id_list)
    return json.dumps(results)

#test:http://219.224.134.213:9209/weibo_xnr_monitor/lookup_active_weibouser/?weiboxnr_id=WXNR0001&classify_id=1
@mod.route('/lookup_active_weibouser/')
def ajax_lookup_active_weibouser():
    weiboxnr_id=request.args.get('weiboxnr_id','')
    classify_id=request.args.get('classify_id','')
    result=lookup_active_weibouser(classify_id,weiboxnr_id)
    return json.dumps(result)

#test:http://219.224.134.213:9209/weibo_xnr_monitor/weibo_user_detail/?user_id=2502058433
@mod.route('/weibo_user_detail/')
def ajax_weibo_user_detail():
    user_id=request.args.get('user_id','')
    result=weibo_user_detail(user_id)
    return json.dumps(result)

@mod.route('/weibo_user_test/')
def ajax_weibo_user_test():
    result=weibo_user_test()
    return json.dumps(result)

@mod.route('/lookup_weiboxnr_concernedusers/')
def ajax_lookup_weiboxnr_concernedusers():
    weiboxnr_id=request.args.get('weiboxnr_id','')
    result=lookup_weiboxnr_concernedusers(weiboxnr_id)
    return json.dumps(result)