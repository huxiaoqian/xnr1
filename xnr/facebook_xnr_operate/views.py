#-*- coding:utf-8 -*-

import os
import time
import json
import random
from flask import Flask, Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from xnr.global_config import S_TYPE
from xnr.time_utils import datetime2ts, ts2datetime
from utils import get_submit_tweet_fb, fb_save_to_tweet_timing_list, get_recommend_at_user,\
                get_daily_recommend_tweets, get_hot_sensitive_recommend_at_user, push_keywords_task, \
                get_hot_subopinion, get_bussiness_recomment_tweets,get_comment_operate_fb, \
                get_retweet_operate_fb, get_at_operate_fb, get_like_operate_fb, get_follow_operate_fb, \
                get_unfollow_operate_fb, get_private_operate_fb, get_add_friends, get_confirm_friends,\
                get_delete_friend, get_hot_recommend_tweets, get_trace_follow_operate, \
                get_un_trace_follow_operate, get_show_trace_followers,\
                get_show_retweet_timing_list, get_show_retweet_timing_list_future, get_robot_reply
from xnr.utils import add_operate2redis

mod = Blueprint('facebook_xnr_operate', __name__, url_prefix='/facebook_xnr_operate')

'''
日常发帖
'''

# 发帖

@mod.route('/submit_tweet/')
def ajax_submit_daily_tweet():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    # 参数传对应英文 (以下所有url一样)
    #u'日常发帖':'daily_post',u'热门发帖':'hot_post',u'业务发帖':'business_post',\
    #u'跟随转发':'trace_post',u'智能发帖':'intel_post', u'信息监测':'info_detect'，u'预警': 'info_warning'
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').decode('utf-8')

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'publish'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_submit_tweet_fb(task_detail)

    return json.dumps(mark)


# 提交定时任务
@mod.route('/submit_timing_post_task/')
def ajax_submit_timing_post_task():
    task_detail = dict()
    #task_detail['uid'] = request.args.get('uid','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['tweet_type'] = request.args.get('tweet_type','')

    current_ts = int(time.time())
    task_detail['create_time'] = current_ts

    post_time_sts = int(request.args.get('post_time_sts',''))
    post_time_ets = int(request.args.get('post_time_ets',''))
    range_ts = post_time_ets - post_time_sts
    post_time = post_time_sts + random.randint(0,range_ts)    # 随机生成发帖时间

    task_detail['post_time'] = post_time

    task_detail['text'] = request.args.get('text','').encode('utf-8')
    #task_detail['task_status'] = request.args.get('task_status','')

    task_detail['task_status'] = 0
    task_detail['remark'] = request.args.get('remark','')

    mark = fb_save_to_tweet_timing_list(task_detail)

    return json.dumps(mark)  # True False

# # 日常@用户推荐
# @mod.route('/daily_recommend_at_user/')
# def ajax_recommend_at_user():
#     xnr_user_no = request.args.get('xnr_user_no','')
#     uid_nick_name_dict = get_recommend_at_user(xnr_user_no)
#     return json.dumps(uid_nick_name_dict)  # {'uid1':'nick_name1','uid2':'nick_name2',...}


# # 日常语料推荐
# # fb 暂无？？？？  # 遵照微博的url
# @mod.route('/daily_recommend_tweets/')
# def ajax_daily_recommend_tweets():
#     theme = request.args.get('theme','') # 默认日常兴趣主题
#     sort_item = request.args.get('sort_item','timestamp')  # timestamp-按时间, retweeted-按热度
#     tweets = get_daily_recommend_tweets(theme,sort_item)
#     return json.dumps(tweets)

'''
热点跟随
'''

# 热门@用户推荐
#http://219.224.134.213:9999/facebook_xnr_operate/hot_sensitive_recommend_at_user/?sort_item=share

@mod.route('/hot_sensitive_recommend_at_user/')
def ajax_hot_sensitive_recommend_at_user():
    sort_item = request.args.get('sort_item','')  # share- 热点跟随  sensitive- 业务发帖  # 先按     sort_item = 'sensitive', sort_item_2 = 'timestamp'
    uid_nick_name_dict = get_hot_sensitive_recommend_at_user(sort_item)
    return json.dumps(uid_nick_name_dict)  # {'uid1':'nick_name1','uid2':'nick_name2',...}


# 热点跟随帖子推荐
#http://219.224.134.213:9999/facebook_xnr_operate/hot_recommend_tweets/?xnr_user_no=FXNR0003&topic_field=军事类&sort_item=sensitive

@mod.route('/hot_recommend_tweets/')
def ajax_hot_recommend_tweets():

    xnr_user_no = request.args.get('xnr_user_no','') # 当前虚拟人 
    topic_field = request.args.get('topic_field','') # 默认...
    sort_item = request.args.get('sort_item','timestamp')  # timestamp-按时间, sensitive-按敏感度
    tweets = get_hot_recommend_tweets(xnr_user_no,topic_field,sort_item)
    return json.dumps(tweets)

# 热点跟随子观点分析的提交关键词任务
#http://219.224.134.213:9999/facebook_xnr_operate/submit_hot_keyword_task/?xnr_user_no=FXNR0003&task_id=894173877414829&keywords_string=中共&submit_user=admin@qq.com

@mod.route('/submit_hot_keyword_task/')
def ajax_submit_hot_keyword_task():
    #mark = True
    task_detail = dict()

    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','') # 当前虚拟人 
    task_detail['task_id'] = request.args.get('task_id','') # 当前代表微博的mid 
    task_detail['keywords_string'] = request.args.get('keywords_string','') # 提交的关键词，以中文逗号分隔“，”
    task_detail['compute_status'] = 0 # 尚未计算
    task_detail['submit_time'] = int(time.time()) # 当前时间
    task_detail['submit_user'] = request.args.get('submit_user','admin@qq.com') 

    mark = push_keywords_task(task_detail)

    return json.dumps(mark)  # 建立成功为True,失败为False


# 子观点分析
#http://219.224.134.213:9999/facebook_xnr_operate/hot_subopinion/?xnr_user_no=FXNR0003&task_id=894173877414829

@mod.route('/hot_subopinion/')
def ajax_hot_hot_subopinion():
    xnr_user_no = request.args.get('xnr_user_no','')  # 当前虚拟人
    task_id = request.args.get('task_id','')  # mid
    subopnion_results = get_hot_subopinion(xnr_user_no,task_id)
    return json.dumps(subopnion_results)


'''
业务发帖
'''

# 帖子推荐
# http://219.224.134.213:9999/facebook_xnr_operate/bussiness_recomment_tweets/?xnr_user_no=FXNR0003&sort_item=timestamp
# sort_item: 按时间-timestamp， 按信息敏感度 - sensitive_info， 按人物敏感度 - sensitive_user
#            按信息影响力 - influence_info， 按人物影响力 - influence_user

@mod.route('/bussiness_recomment_tweets/')
def ajax_bussiness_recomment_tweets():
    xnr_user_no = request.args.get('xnr_user_no','')
    sort_item = request.args.get('sort_item','timestamp') 
    tweets = get_bussiness_recomment_tweets(xnr_user_no,sort_item)
    return json.dumps(tweets)

'''
跟随转发
'''

# 展示跟随转发定时列表
# http://219.224.134.213:9090/facebook_xnr_operate/show_retweet_timing_list/?xnr_user_no=FXNR0003

@mod.route('/show_retweet_timing_list/')
def ajax_show_retweet_timing_list():
    xnr_user_no = request.args.get('xnr_user_no','')
    start_ts = request.args.get('start_ts','')
    end_ts = request.args.get('end_ts','')

    results = get_show_retweet_timing_list(xnr_user_no,start_ts,end_ts)

    return json.dumps(results)

# 展示跟随转发定时列表（未来）
# http://219.224.134.213:9090/facebook_xnr_operate/show_retweet_timing_list_future/?xnr_user_no=FXNR0003

@mod.route('/show_retweet_timing_list_future/')
def ajax_show_retweet_timing_list_future():
    
    xnr_user_no = request.args.get('xnr_user_no','')

    results = get_show_retweet_timing_list_future(xnr_user_no)

    return json.dumps(results)


# 展示重点关注用户信息
# http://219.224.134.213:9090/facebook_xnr_operate/show_trace_followers/?xnr_user_no=FXNR0003
@mod.route('/show_trace_followers/')
def ajax_show_trace_followers():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_show_trace_followers(xnr_user_no)

    return json.dumps(results)

# 重点关注
#http://219.224.134.213:9090/facebook_xnr_operate/trace_follow/?xnr_user_no=FXNR0003&uid_string=100018797745111&nick_name_string=
@mod.route('/trace_follow/')
def ajax_trace_follow_operate():
    xnr_user_no = request.args.get('xnr_user_no','')
    uid_string = request.args.get('uid_string','')    # 不同uid之间用中文逗号“，”隔开
    nick_name_string = request.args.get('nick_name_string','')  # 不同昵称之间用中文逗号分隔
    results = get_trace_follow_operate(xnr_user_no,uid_string,nick_name_string)

    return json.dumps(results)   # [mark,fail_nick_name_list]  fail_nick_name_list为添加失败，原因是背景信息库没有这些人，请换成对应uid试试。

# 取消重点关注
#http://219.224.134.213:9090/facebook_xnr_operate/un_trace_follow/?xnr_user_no=FXNR0003&uid_string=100018797745111&nick_name_string=
@mod.route('/un_trace_follow/')
def ajax_un_trace_follow_operate():
    xnr_user_no = request.args.get('xnr_user_no','')
    uid_string = request.args.get('uid_string','')    # 不同uid之间用中文逗号“，”隔开
    nick_name_string = request.args.get('nick_name_string','')  # 不同昵称之间用中文逗号分隔
    results = get_un_trace_follow_operate(xnr_user_no,uid_string,nick_name_string)

    return json.dumps(results)  # [mark,fail_uids,fail_nick_name_list]  fail_uids - 取消失败的uid  fail_nick_name_list -- 原因同上


# 除发帖外其他操作

# 评论
@mod.route('/comment_operate/')
def ajax_comment_operate():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').decode('utf-8')
    task_detail['r_fid'] = request.args.get('fid','') # 被转发帖子
    task_detail['r_uid'] = request.args.get('uid','') # 被转发帖子的用户

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'comment'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    #mark = get_comment_operate(task_detail)

    return json.dumps(mark)

# 转发
@mod.route('/retweet_operate/')
def ajax_retweet_operate():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').decode('utf-8')
    task_detail['r_fid'] = request.args.get('fid','') # 被转发帖子
    task_detail['r_uid'] = request.args.get('uid','') # 被转发帖子的用户

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'retweet'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_retweet_operate(task_detail)

    return json.dumps(mark)


# @/提到
@mod.route('/at_operate/')
def ajax_at_operate():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['nick_name'] = request.args.get('nick_name','')
    
    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'at'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_at_operate(task_detail)

    return json.dumps(mark)

# 点赞
@mod.route('/like_operate/')
def ajax_like_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['r_fid'] = request.args.get('fid','') # 被转发帖子
    task_detail['r_uid'] = request.args.get('uid','') # 被转发帖子的用户
    
    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'like'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_like_operate_fb(task_detail)

    return json.dumps(mark)

# 关注
@mod.route('/follow_operate/')
def ajax_follow_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')
    task_detail['trace_type'] = request.args.get('trace_type','')  # 跟随关注 -trace_follow，普通关注-ordinary_follow
    
    # mark = get_follow_operate(task_detail)

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'follow'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # return json.dumps(mark)

# 取消关注
@mod.route('/unfollow_operate/')
def ajax_unfollow_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'unfollow'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_unfollow_operate(task_detail)

    return json.dumps(mark)


# 私信
@mod.route('/private_operate/')
def ajax_private_operate():

    task_detail= dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')
    task_detail['text'] = request.args.get('text','')

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'private'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_private_operate(task_detail)

    return json.dumps(mark)

# 添加好友
@mod.route('/add_friends/')    
def ajax_add_friends():

    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'add'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_add_friends(task_detail)

    return json.dumps(mark)


# 确认好友请求
@mod.route('/confirm_friends/')
def ajax_confirm_friends():

    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'confirm'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_confirm_friends(task_detail)
    
    return json.dumps(mark)


# 删除好友
@mod.route('/delete_friend/')
def ajax_delete_friend():

    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')

    queue_dict = {}
    queue_dict['channel'] = 'facebook'
    queue_dict['operate_type'] = 'delete'
    queue_dict['content'] = task_detail
    mark = add_operate2redis(queue_dict)

    # mark = get_delete_friend(task_detail)
    
    return json.dumps(mark)


# 机器人回复
# http://219.224.134.213:9090/facebook_xnr_operate/robot_reply/?question=你好

@mod.route('/robot_reply/')
def ajax_robot_reply():

    question = request.args.get('question','').encode('utf-8')

    answer = get_robot_reply(question)

    # return json.dumps(answer)
    return json.dumps(answer)










#####################################################################
##########################韩梦成负责以下内容###########################
#####################################################################
from utils import get_show_comment, get_show_retweet, get_show_private, \
					get_show_at,get_show_friends,get_direct_search,get_related_recommendation
# 评论及回复
# http://219.224.134.213:6659/facebook_xnr_operate/show_comment/?xnr_user_no=FXNR0001&sort_item=timestamp&start_ts=1508256000&end_ts=1508860800  #2017-10-18 2017-10-25
@mod.route('/show_comment/')
def ajax_show_comment():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    task_detail['start_ts'] = request.args.get('start_ts','')
    task_detail['end_ts'] = request.args.get('end_ts','')
    # if S_TYPE == 'test':
    #     task_detail['start_ts'] = datetime2ts('2017-10-01')
    #     task_detail['end_ts'] = datetime2ts('2017-10-07')
    results = get_show_comment(task_detail)
    return json.dumps(results)


# 转发及回复
# http://219.224.134.213:6659/weibo_xnr_operate/show_retweet/?xnr_user_no=FXNR0001&sort_item=timestamp&start_ts=1508256000&end_ts=1508860800  #2017-10-18 2017-10-25
@mod.route('/show_retweet/')
def ajax_show_retweet():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    task_detail['start_ts'] = request.args.get('start_ts','')
    task_detail['end_ts'] = request.args.get('end_ts','')
    # if S_TYPE == 'test':
    #     task_detail['start_ts'] = datetime2ts('2017-10-01')
    #     task_detail['end_ts'] = datetime2ts('2017-10-07')
    results = get_show_retweet(task_detail)
    return json.dumps(results)

# 私信及回复
# http://219.224.134.213:6659/weibo_xnr_operate/show_private/?xnr_user_no=FXNR0001&sort_item=timestamp&start_ts=1508256000&end_ts=1508860800  #2017-10-18 2017-10-25
@mod.route('/show_private/')
def ajax_show_private():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    task_detail['start_ts'] = request.args.get('start_ts','')
    task_detail['end_ts'] = request.args.get('end_ts','')
    # if S_TYPE == 'test':
    #     task_detail['start_ts'] = datetime2ts('2017-10-01')
    #     task_detail['end_ts'] = datetime2ts('2017-10-07')
    results = get_show_private(task_detail)
    return json.dumps(results)

# @及回复
# http://219.224.134.213:6659/weibo_xnr_operate/show_at/?xnr_user_no=FXNR0001&sort_item=timestamp&start_ts=1508256000&end_ts=1508860800  #2017-10-18 2017-10-25
@mod.route('/show_at/')
def ajax_show_at():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    task_detail['start_ts'] = request.args.get('start_ts','')
    task_detail['end_ts'] = request.args.get('end_ts','')
    # if S_TYPE == 'test':
    #     task_detail['start_ts'] = datetime2s('2017-10-01')
    #     task_detail['end_ts'] = datetime2s('2017-10-07')   
    results = get_show_at(task_detail)
    return json.dumps(results)

# 好友列表
# http://219.224.134.213:6659/weibo_xnr_operate/show_friends/?xnr_user_no=FXNR0001&sort_item=timestamp&start_ts=1508256000&end_ts=1508860800  #2017-10-18 2017-10-25
@mod.route('/show_friends/')
def ajax_show_friends():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    task_detail['start_ts'] = request.args.get('start_ts','')
    task_detail['end_ts'] = request.args.get('end_ts','')
    results = get_show_friends(task_detail)
    return json.dumps(results)


# 直接搜索
# http://219.224.134.213:6659/facebook_xnr_operate/direct_search/?xnr_user_no=FXNR0003&sort_item=influence&uids=24243234
@mod.route('/direct_search/')
def ajax_direct_search():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','influence')
    uids = request.args.get('uids','').encode('utf-8')
    uid_list = uids.split('，')
    task_detail['uid_list'] = uid_list
    results = get_direct_search(task_detail)
    return json.dumps(results)

# 相关推荐
# 现支持influ（share）、sensitive（sensitive）
@mod.route('/related_recommendation/')
def ajax_related_recommendation():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','influence')
    results = get_related_recommendation(task_detail)
    return json.dumps(results)