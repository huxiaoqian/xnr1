#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_flow_text
from utils import lookup_weibo_keywordstring,lookup_full_keywordstring,lookup_hot_posts,lookup_active_weibouser,\
                  weibo_user_detail,addto_weibo_corpus,get_weibohistory_retweet,get_weibohistory_comment,\
                  get_weibohistory_like,attach_fans_follow,addto_weibo_corpus,attach_fans_batch,new_addto_weibo_corpus

mod=Blueprint('weibo_xnr_monitor',__name__,url_prefix='/weibo_xnr_monitor')

#function 1:lookup_weibo_keywordstiing to create wordcloud
#test:http://219.224.134.213:9209/weibo_xnr_monitor/lookup_weibo_keywordstring/?from_ts=1479513600&to_ts=1479981600&weiboxnr_id=WXNR0002
#http://219.224.134.213:9209/weibo_xnr_monitor/lookup_weibo_keywordstring/?from_ts=1479513600&to_ts=1479600000&weiboxnr_id=WXNR0002
@mod.route('/lookup_weibo_keywordstring/')
def ajax_lookup_weibo_keywordstring():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    weiboxnr_id=request.args.get('weiboxnr_id','')
    result=lookup_weibo_keywordstring(float(from_ts),float(to_ts),weiboxnr_id)
    return json.dumps(result)


#全网词云
@mod.route('/lookup_full_keywordstring/')
def ajax_lookup_full_keywordstring():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    result=lookup_full_keywordstring(int(from_ts),int(to_ts))
    return json.dumps(result)


#热门帖子
#classify_id=全部用户 0，已关注用户 1，未关注用户-1
#order_id=1,表示按时间排序，order_id=2，表示按热度排序，order_id=3，表示按敏感度排序，默认按时间排序
#test:http://219.224.134.213:9209/weibo_xnr_monitor/lookup_hot_posts/?from_ts=1479513600&to_ts=1479981600&weiboxnr_id=WXNR0002&classify_id=0&order_id=1
@mod.route('/lookup_hot_posts/')
def ajax_lookup_hot_posts():
    from_ts=request.args.get('from_ts','')
    to_ts=request.args.get('to_ts','')
    print 'from_ts, to_ts:', from_ts, to_ts
    weiboxnr_id=request.args.get('weiboxnr_id','')
    classify_id=int(request.args.get('classify_id',''))
    order_id=int(request.args.get('order_id',''))
    result=lookup_hot_posts(float(from_ts),float(to_ts),weiboxnr_id,classify_id,order_id)
    return json.dumps(result)

#############微博相关操作########

#转发
#http://219.224.134.213:9209/weibo_xnr_monitor/get_weibohistory_retweet/?xnr_user_no=WXNR0003&r_mid=4143645403880308&text=下雨了，吼吼\(^o^)/~
@mod.route('/get_weibohistory_retweet/')
def ajax_get_weibohistory_retweet():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','').encode('utf-8')    #text指转发时发布的内容
    results=get_weibohistory_retweet(task_detail)
    return json.dumps(results)

#评论
#http://219.224.134.213:9209/weibo_xnr_monitor/get_weibohistory_comment/?xnr_user_no=WXNR0003&r_mid=4143645403880308&text=嘻嘻hahha
@mod.route('/get_weibohistory_comment/')
def ajax_get_weibohistory_comment():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['text']=request.args.get('text','').encode('utf-8')    #text指转发时发布的内容
    results=get_weibohistory_comment(task_detail)
    return json.dumps(results)

#赞
#http://219.224.134.213:9209/weibo_xnr_monitor/get_weibohistory_like/?xnr_user_no=WXNR0004&r_mid=4143645403880308&uid=6346321407&nick_name=巨星大大&text=下雨了，吼吼\(^o^)/~&timestamp=1503405480
@mod.route('/get_weibohistory_like/')
def ajax_get_weibohistory_like():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['r_mid']=request.args.get('r_mid','')  #r_mid指原微博的mid
    task_detail['uid']=request.args.get('uid')   #点赞对象的uid
    task_detail['nick_name']=request.args.get('nick_name','') #点赞对象昵称
    task_detail['text']=request.args.get('text','').encode('utf-8')    #text指点赞的内容
    task_detail['timestamp']=int(request.args.get('timestamp',''))
    task_detail['update_time']=int(time.time())
    task_detail['photo_url']=request.args.get('photo_url','')
    results=get_weibohistory_like(task_detail)
    return json.dumps(results)

#直接关注
#http://219.224.134.213:9209/weibo_xnr_monitor/attach_fans_follow/?xnr_user_no=WXNR0004&uid=6340301597
@mod.route('/attach_fans_follow/')
def ajax_attach_fans_follow():
    task_detail=dict()
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['uid']=request.args.get('uid','')   #关注对象的uid
    task_detail['trace_type']=request.args.get('trace_type','')
    results=attach_fans_follow(task_detail)
    return json.dumps(results)

#加入语料库
#task_detail=[corpus_type,theme_daily_name,text,uid,mid,timestamp,retweeted,comment,like,create_type]
#http://219.224.134.213:9209/weibo_xnr_monitor/addto_weibo_corpus/?corpus_type=日常语料&theme_daily_name=旅游&text=【泸州：方山观光索道11月10日-12月10日停运升级改造】方山客运观光索道已运营16个年头，机电设备已陈旧落后，为更好地保障安全营运，保护广大游客的生命财产安全，于2016年11月10至12月10日，客运观光索道电控系统设备进行提档升级更换改造，升级改造期间停止运营。&uid=2503848121&mid=4045475189951089&retweeted=0&comment=0&like=0&create_type=my_xnrs
@mod.route('/addto_weibo_corpus/')
def ajax_addto_weibo_corpus():
    corpus_type=request.args.get('corpus_type','')
    theme_daily_name=request.args.get('theme_daily_name','').split(',')
    text=request.args.get('text','')
    uid=request.args.get('uid','')
    mid=request.args.get('mid','')
    timestamp=int(time.time())
    retweeted=request.args.get('retweeted','')
    comment=request.args.get('comment','')
    like=request.args.get('like','')
    create_type=request.args.get('create_type','')
    xnr_user_no=request.args.get('xnr_user_no','')
    task_detail=[corpus_type,theme_daily_name,text,uid,mid,timestamp,retweeted,comment,like,create_type,xnr_user_no]
    results=addto_weibo_corpus(task_detail)
    return json.dumps(results)


#加入语料库新方法
@mod.route('/new_addto_weibo_corpus/')
def ajax_new_addto_weibo_corpus():
    task_detail=dict()
    task_detail['corpus_type']=request.args.get('corpus_type','')
    task_detail['theme_daily_name']=request.args.get('theme_daily_name','').split(',')
    task_detail['uid']=request.args.get('uid','')
    task_detail['mid']=request.args.get('mid','')
    task_detail['timestamp']=int(request.args.get('timestamp',''))
    task_detail['create_type']=request.args.get('create_type','')
    task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
    task_detail['create_time']=int(time.time())
    results=new_addto_weibo_corpus(task_detail)
    return json.dumps(results)


#批量添加关注
#http://219.224.134.213:9209/weibo_xnr_monitor/attach_fans_batch/?xnr_user_no_list=WXNR0004&fans_id_list=5115675150,2738743113
@mod.route('/attach_fans_batch/')
def ajax_attach_fans_batch():
    xnr_user_no_list=request.args.get('xnr_user_no_list','').split(',')   #虚拟人no的list
    fans_id_list=request.args.get('fans_id_list','').split(',')            #勾选的活跃用户id的list
    trace_type=request.args.get('trace_type','')
    results=attach_fans_batch(xnr_user_no_list,fans_id_list,trace_type)
    return json.dumps(results)


#活跃用户
#test:http://219.224.134.213:9209/weibo_xnr_monitor/lookup_active_weibouser/?weiboxnr_id=WXNR0004&classify_id=1&start_time=1504224000&end_time=1504540800
@mod.route('/lookup_active_weibouser/')
def ajax_lookup_active_weibouser():
    weiboxnr_id=request.args.get('weiboxnr_id','')
    classify_id=int(request.args.get('classify_id',''))
    start_time=int(request.args.get('start_time',''))
    end_time=int(request.args.get('end_time'))
    result=lookup_active_weibouser(classify_id,weiboxnr_id,start_time,end_time)
    return json.dumps(result)


#用户详情
#test:http://219.224.134.213:9209/weibo_xnr_monitor/weibo_user_detail/?user_id=2502058433
@mod.route('/weibo_user_detail/')
def ajax_weibo_user_detail():
    user_id=request.args.get('user_id','')
    result=weibo_user_detail(user_id)
    return json.dumps(result)

