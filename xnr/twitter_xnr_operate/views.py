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
from utils import get_submit_tweet, tw_save_to_tweet_timing_list, get_recommend_at_user,\
				get_daily_recommend_tweets, get_hot_sensitive_recommend_at_user, push_keywords_task, \
				get_hot_subopinion, get_bussiness_recomment_tweets,get_comment_operate, \
				get_retweet_operate, get_at_operate, get_like_operate, get_follow_operate, \
				get_unfollow_operate

mod = Blueprint('twitter_xnr_operate', __name__, url_prefix='/twitter_xnr_operate')

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
    #u'跟随转发':'trace_post',u'智能发帖':'intel_post'
	task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
	task_detail['text'] = request.args.get('text','').encode('utf-8')
    # print 'task_detail...',task_detail
	mark = get_submit_tweet(task_detail)

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

    mark = tw_save_to_tweet_timing_list(task_detail)

    return json.dumps(mark)  # True False

# 日常@用户推荐
@mod.route('/daily_recommend_at_user/')
def ajax_recommend_at_user():
    xnr_user_no = request.args.get('xnr_user_no','')
    uid_nick_name_dict = get_recommend_at_user(xnr_user_no)
    return json.dumps(uid_nick_name_dict)  # {'uid1':'nick_name1','uid2':'nick_name2',...}


# 日常语料推荐
# tw 暂无？？？？
@mod.route('/daily_recommend_tweets/')
def ajax_daily_recommend_tweets():
    theme = request.args.get('theme','') # 默认日常兴趣主题
    sort_item = request.args.get('sort_item','timestamp')  # timestamp-按时间, retweeted-按热度
    tweets = get_daily_recommend_tweets(theme,sort_item)
    return json.dumps(tweets)

'''
热点跟随
'''

# 热门@用户推荐
@mod.route('/hot_sensitive_recommend_at_user/')
def ajax_hot_sensitive_recommend_at_user():
    sort_item = request.args.get('sort_item','')  # retweeted- 热点跟随  sensitive- 业务发帖  # 先按     sort_item = 'sensitive', sort_item_2 = 'timestamp'
    uid_nick_name_dict = get_hot_sensitive_recommend_at_user(sort_item)
    return json.dumps(uid_nick_name_dict)  # {'uid1':'nick_name1','uid2':'nick_name2',...}


# 热点跟随帖子推荐
@mod.route('/hot_recommend_tweets/')
def ajax_hot_recommend_tweets():

    xnr_user_no = request.args.get('xnr_user_no','') # 当前虚拟人
    topic_field = request.args.get('topic_field','') # 默认...
    sort_item = request.args.get('sort_item','timestamp')  # timestamp-按时间, compute_status-按事件完成度
    tweets = get_hot_recommend_tweets(xnr_user_no,topic_field,sort_item)
    return json.dumps(tweets)

# 热点跟随子观点分析的提交关键词任务
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
@mod.route('/bussiness_recomment_tweets/')
def ajax_bussiness_recomment_tweets():
    xnr_user_no = request.args.get('xnr_user_no','')
    sort_item = request.args.get('sort_item','timestamp')
    tweets = get_bussiness_recomment_tweets(xnr_user_no,sort_item)
    return json.dumps(tweets)


# 除发帖外其他操作

# 评论
@mod.route('/comment_operate/')
def ajax_comment_operate():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['r_fid'] = request.args.get('fid','') # 被转发帖子
    task_detail['r_uid'] = request.args.get('uid','') # 被转发帖子的用户

    mark = get_comment_operate(task_detail)

    return json.dumps(mark)

# 转发
@mod.route('/retweet_operate/')
def ajax_retweet_operate():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['r_fid'] = request.args.get('fid','') # 被转发帖子
    task_detail['r_uid'] = request.args.get('uid','') # 被转发帖子的用户

    mark = get_retweet_operate(task_detail)

    return json.dumps(mark)


# @/提到
@mod.route('/at_operate/')
def ajax_at_operate():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['nick_name'] = request.args.get('nick_name','')

    mark = get_at_operate(task_detail)

    return json.dumps(mark)

# 点赞
@mod.route('/like_operate/')
def ajax_like_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['r_fid'] = request.args.get('fid','') # 被转发帖子
    task_detail['r_uid'] = request.args.get('uid','') # 被转发帖子的用户

    mark = get_like_operate(task_detail)

    return json.dumps(mark)

# 关注
@mod.route('/follow_operate/')
def ajax_follow_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')
    task_detail['trace_type'] = request.args.get('trace_type','')  # 跟随关注 -trace_follow，普通关注-ordinary_follow
    mark = get_follow_operate(task_detail)

    return json.dumps(mark)

# 取消关注
@mod.route('/unfollow_operate/')
def ajax_unfollow_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')
    mark = get_unfollow_operate(task_detail)

    return json.dumps(mark)
