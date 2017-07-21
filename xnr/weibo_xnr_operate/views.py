#-*- coding:utf-8 -*-
import os
import time
import json
import random
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from utils import push_keywords_task,get_submit_tweet,save_to_tweet_timing_list,get_recommend_at_user,\
				get_daily_recommend_tweets,get_hot_recommend_tweets,get_hot_content_recommend,\
				get_hot_subopinion,get_hot_sensitive_recommend_at_user,get_bussiness_recomment_tweets,\
				get_show_comment,get_reply_comment,get_show_retweet,get_reply_retweet,get_show_private,\
				get_reply_private,get_show_at,get_reply_at,get_show_follow,get_reply_follow

mod = Blueprint('weibo_xnr_operate', __name__, url_prefix='/weibo_xnr_operate')

'''
日常发帖

'''
# 日常发布微博
@mod.route('/submit_tweet/')
def ajax_submit_daily_tweet():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['uid'] = request.args.get('uid','')
    task_detail['text'] = request.args.get('text','')
    task_detail['weibo_mail_account'] = request.args.get('weibo_mail_account','')
    task_detail['weibo_phone_account'] = request.args.get('weibo_phone_account','')
    task_detail['password'] = request.args.get('password','')    

    mark = get_submit_tweet(task_detail)
    return json.dumps(mark)

# 提交定时发送任务
@mod.route('/submit_timing_post_task/')
def ajax_submit_timing_post_task():
	task_detail = dict()
	task_detail['uid'] = request.args.get('uid','')
	task_detail['user_no'] = request.args.get('user_no','')
	task_detail['task_source'] = request.args.get('task_source','')
	task_detail['operate_type'] = request.args.get('operate_type','')

	current_ts = int(time.time())
	task_detail['create_time'] = current_ts

	post_time_sts = int(request.args.get('post_time_sts',''))
	post_time_ets = int(request.args.get('post_time_ets',''))
	range_ts = post_time_ets - post_time_sts
	post_time = post_time_sts + random.randint(0,range_ts)    # 随机生成发帖时间

	task_detail['post_time'] = post_time

	task_detail['text'] = request.args.get('text','')
	task_detail['task_status'] = request.args.get('task_status','')
	task_detail['remark'] = request.args.get('remark','')

	mark = save_to_tweet_timing_list(task_detail)

	return json.dumps(mark)  # True False

# 日常@用户推荐
@mod.route('/daily_recommend_at_user/')
def ajax_recommend_at_user():
	xnr_user_no = request.args.get('xnr_user_no','')
	uid_nick_name_dict = get_recommend_at_user(xnr_user_no)
	return json.dumps(uid_nick_name_dict)  # {'uid1':'nick_name1','uid2':'nick_name2',...}

# 日常语料推荐
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
	sort_item = request.args.get('sort_item','')  # retweeted- 热点跟随  sensitive- 业务发帖
	uid_nick_name_dict = get_hot_sensitive_recommend_at_user(sort_item)
	return json.dumps(uid_nick_name_dict)  # {'uid1':'nick_name1','uid2':'nick_name2',...}

# 热点跟随微博推荐
@mod.route('/hot_recommend_tweets/')
def ajax_hot_recommend_tweets():
	topic_field = request.args.get('topic_field','') # 默认...
	sort_item = request.args.get('sort_item','timestamp')  # timestamp-按时间, finish_status-按事件完成度，event_weight-按事件权重
	tweets = get_hot_recommend_tweets(topic_field,sort_item)
	return json.dumps(tweets)

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

# 内容推荐
@mod.route('/hot_content_recommend/')
def ajax_hot_content_recommend():
	task_id = request.args.get('task_id','')  # mid
	task_id = '"'+task_id+'"'
	contents = get_hot_content_recommend(task_id)
	return json.dumps(contents)

# 子观点分析
@mod.route('/hot_subopinion/')
def ajax_hot_hot_subopinion():
	task_id = request.args.get('task_id','')  # mid
	task_id = '"'+task_id+'"'
	subopnion_results = get_hot_subopinion(task_id)
	return json.dumps(subopnion_results)

'''
业务发帖

'''

# 微博推荐
@mod.route('/bussiness_recomment_tweets/')
def ajax_bussiness_recomment_tweets():
	sort_item = request.args.get('sort_item','timestamp') 
	tweets = get_bussiness_recomment_tweets(sort_item)
	return json.dumps(tweets)

'''
社交反馈模块

'''

# 评论及回复
@mod.route('/show_comment/')
def ajax_show_comment():
	sort_item = request.args.get('sort_item','')
	results = get_show_comment(sort_item)
	return json.dumps(results)

@mod.route('/reply_comment/')
def ajax_reply_comment():
	text = request.args.get('text','')
	mid = request.args.get('mid','')
	mark = get_reply_comment(text,mid)

	return json.dumps(mark)


# 转发及回复
@mod.route('/show_retweet/')
def ajax_show_retweet():
	sort_item = request.args.get('sort_item','')
	results = get_show_retweet(sort_item)
	return json.dumps(results)

@mod.route('/reply_retweet/')
def ajax_reply_retweet():
	text = request.args.get('text','')
	mid = request.args.get('mid','')
	mark = get_reply_retweet(text,mid)

	return json.dumps(mark)


# 私信及回复
@mod.route('/show_private/')
def ajax_show_private():
	sort_item = request.args.get('sort_item','')
	results = get_show_private(sort_item)
	return json.dumps(results)

@mod.route('/reply_private/')
def ajax_reply_private():
	text = request.args.get('text','')
	mid = request.args.get('mid','')
	mark = get_reply_private(text,mid)

	return json.dumps(mark)

# @及回复
@mod.route('/show_at/')
def ajax_show_at():
	sort_item = request.args.get('sort_item','')
	results = get_show_at(sort_item)
	return json.dumps(results)

@mod.route('/reply_at/')
def ajax_reply_at():
	text = request.args.get('text','')
	mid = request.args.get('mid','')
	mark = get_reply_at(text,mid)

	return json.dumps(mark)

# 关注及回粉
@mod.route('/show_follow/')
def ajax_show_follow():
	sort_item = request.args.get('sort_item','')
	results = get_show_follow(sort_item)
	return json.dumps(results)

@mod.route('/reply_follow/')
def ajax_reply_follow():
	text = request.args.get('text','')
	mid = request.args.get('mid','')
	mark = get_reply_follow(text,mid)

	return json.dumps(mark)

