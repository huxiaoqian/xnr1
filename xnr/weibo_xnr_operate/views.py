#-*- coding:utf-8 -*-
from flask import Flask
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
                get_reply_private,get_show_at,get_reply_at,get_show_follow,get_reply_follow,get_like_operate,\
                get_reply_unfollow,get_direct_search,get_related_recommendation,get_create_group,get_show_group,\
                get_show_fans,get_add_sensor_user,get_delete_sensor_user,get_create_group_show_fans,\
                get_trace_follow_operate,get_un_trace_follow_operate,get_show_retweet_timing_list,\
                get_show_trace_followers,get_image_path,get_reply_total,get_show_domain

mod = Blueprint('weibo_xnr_operate', __name__, url_prefix='/weibo_xnr_operate')
#from xnr import create_app

'''
日常发帖

'''

# Create app
# app = Flask(__name__)

# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
# UPLOAD_FOLDER = os.path.join(APP_ROOT, 'xnr/weibo_images/') 
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @mod.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @mod.route('/upload/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # return redirect(url_for('uploaded_file',
#             #                         filename=filename))
#             path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             return path
#

# 返回渗透领域
@mod.route('/show_domain_second/')
def ajax_show_domain():
    #xnr_user_no = request.args.get('xnr_user_no','')
    domain_name_dict = get_show_domain()
    return json.dumps(domain_name_dict)

# 获取图片路径
@mod.route('/get_image_path/')
def ajax_get_image_path():
    image_code = request.args.get('image_code','') # 以中文逗号隔开
    print 'image_code::',image_code
    results = get_image_path(image_code)
    return json.dumps(results)

@mod.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# 日常发布微博
@mod.route('/submit_tweet/')
def ajax_submit_daily_tweet():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','') # 日常发帖、热点跟随、业务发帖
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    #task_detail['operate_type'] = request.args.get('operate_type','') # 原创、转发、评论
    task_detail['p_url']  = json.loads(json.dumps(request.args.get('p_url','').encode('utf-8')))  
    task_detail['rank'] = request.args.get('rank','')
    task_detail['rankid'] = request.args.get('rankid','')

    mark = get_submit_tweet(task_detail)
    return json.dumps(mark)

# 提交定时发送任务
@mod.route('/submit_timing_post_task/')
def ajax_submit_timing_post_task():
    task_detail = dict()
    #task_detail['uid'] = request.args.get('uid','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['task_source'] = request.args.get('task_source','')

    current_ts = int(time.time())
    task_detail['create_time'] = current_ts

    post_time_sts = int(request.args.get('post_time_sts',''))
    post_time_ets = int(request.args.get('post_time_ets',''))
    range_ts = post_time_ets - post_time_sts
    post_time = post_time_sts + random.randint(0,range_ts)    # 随机生成发帖时间

    task_detail['post_time'] = post_time

    task_detail['text'] = request.args.get('text','')
    #task_detail['task_status'] = request.args.get('task_status','')
    
    task_detail['p_url']  = json.loads(json.dumps(request.args.get('p_url','').encode('utf-8')))  
    task_detail['rank'] = request.args.get('rank','')
    task_detail['rankid'] = request.args.get('rankid','')

    task_detail['task_status'] = 0
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

## 返回群列表
@mod.route('/show_group/')
def ajax_show_group():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_show_group(xnr_user_no)

    return json.dumps(results)

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

    xnr_user_no = request.args.get('xnr_user_no','') # 当前虚拟人 
    topic_field = request.args.get('topic_field','') # 默认...
    sort_item = request.args.get('sort_item','timestamp')  # timestamp-按时间, finish_status-按事件完成度，event_weight-按事件权重
    tweets = get_hot_recommend_tweets(xnr_user_no,topic_field,sort_item)
    return json.dumps(tweets)

## 热点跟随：内容推荐和子观点分析的提交关键词任务
@mod.route('/submit_hot_keyword_task/')
def ajax_submit_hot_keyword_task():
    #mark = True
    task_detail = dict()

    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','') # 当前虚拟人 
    task_detail['mid'] = request.args.get('task_id','') # 当前代表微博的mid 
    task_detail['keywords_string'] = request.args.get('keywords_string','') # 提交的关键词，以中文逗号分隔“，”
    task_detail['compute_status'] = 0 # 尚未计算
    task_detail['submit_time'] = int(time.time()) # 当前时间
    task_detail['submit_user'] = request.args.get('submit_user','admin@qq.com') 

    mark = push_keywords_task(task_detail)

    return json.dumps(mark)  # 建立成功为True,失败为False

# 内容推荐
@mod.route('/hot_content_recommend/')
def ajax_hot_content_recommend():

    xnr_user_no = request.args.get('xnr_user_no','')  # 当前虚拟人
    task_id = request.args.get('task_id','')  # mid
    contents = get_hot_content_recommend(xnr_user_no,task_id)
    return json.dumps(contents)

# 子观点分析
@mod.route('/hot_subopinion/')
def ajax_hot_hot_subopinion():
    xnr_user_no = request.args.get('xnr_user_no','')  # 当前虚拟人
    task_id = request.args.get('task_id','')  # mid
    subopnion_results = get_hot_subopinion(xnr_user_no,task_id)
    return json.dumps(subopnion_results)

# 添加人物传感器
@mod.route('/add_sensor_user/')
def ajax_add_sensor_user():
    xnr_user_no = request.args.get('xnr_user_no','')
    sensor_uid_list = request.args.get('sensor_uid_list','')  # 以中文逗号“，”隔开
    
    results = get_add_sensor_user(xnr_user_no,sensor_uid_list)   # True  False

    return json.dumps(results)    


# 删除人物传感器
@mod.route('/delete_sensor_user/')
def ajax_delete_sensor_user():
    xnr_user_no = request.args.get('xnr_user_no','')
    sensor_uid_list = request.args.get('sensor_uid_list','')  # 以中文逗号“，”隔开
    
    results = get_delete_sensor_user(xnr_user_no,sensor_uid_list)   # True  False

    return json.dumps(results)

'''
业务发帖

'''

# 微博推荐
@mod.route('/bussiness_recomment_tweets/')
def ajax_bussiness_recomment_tweets():
    xnr_user_no = request.args.get('xnr_user_no','')
    sort_item = request.args.get('sort_item','timestamp') 
    tweets = get_bussiness_recomment_tweets(xnr_user_no,sort_item)
    return json.dumps(tweets)

'''
社交反馈模块

'''

## 转发、评论、at回复
@mod.route('/reply_total/')
def ajax_reply_total():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['r_mid'] = request.args.get('r_mid','')
    task_detail['mid'] = request.args.get('mid','')
    task_detail['uid'] = request.args.get('uid','')
    task_detail['retweet_option'] = request.args.get('retweet_option','')

    mark = get_reply_total(task_detail)

    return json.dumps(mark)

# 评论及回复
@mod.route('/show_comment/')
def ajax_show_comment():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    results = get_show_comment(task_detail)
    return json.dumps(results)

@mod.route('/reply_comment/')
def ajax_reply_comment():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['r_mid'] = request.args.get('mid','')

    mark = get_reply_comment(task_detail)

    return json.dumps(mark)


# 转发及回复
@mod.route('/show_retweet/')
def ajax_show_retweet():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    results = get_show_retweet(task_detail)
    return json.dumps(results)

@mod.route('/reply_retweet/')
def ajax_reply_retweet():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['r_mid'] = request.args.get('mid','')

    mark = get_reply_retweet(task_detail)

    return json.dumps(mark)

# 私信及回复
@mod.route('/show_private/')
def ajax_show_private():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    results = get_show_private(task_detail)
    return json.dumps(results)

@mod.route('/reply_private/')
def ajax_reply_private():
    task_detail = dict()
    task_detail['tweet_type'] = request.args.get('tweet_type','') # 日常发帖、热点跟随、业务发帖
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['text'] = request.args.get('text','').encode('utf-8')
    task_detail['uid'] = request.args.get('uid','')

    mark = get_reply_private(task_detail)

    return json.dumps(mark)

# @及回复
@mod.route('/show_at/')
def ajax_show_at():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    results = get_show_at(task_detail)
    return json.dumps(results)

@mod.route('/reply_at/')
def ajax_reply_at():
    text = request.args.get('text','')
    mid = request.args.get('mid','')
    mark = get_reply_at(text,mid)

    return json.dumps(mark)

# 关注及回粉

@mod.route('/show_fans/')
def ajax_show_fans():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    results = get_show_fans(task_detail)
    return json.dumps(results)

@mod.route('/show_follow/')
def ajax_show_follow():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','')
    results = get_show_follow(task_detail)
    return json.dumps(results)

@mod.route('/follow_operate/')
def ajax_reply_follow():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')
    task_detail['trace_type'] = request.args.get('trace_type','')  # 跟随关注 -trace_follow，普通关注-ordinary_follow
    mark = get_reply_follow(task_detail)

    return json.dumps(mark)

@mod.route('/unfollow_operate/')
def ajax_unfollow_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['uid'] = request.args.get('uid','')
    mark = get_reply_unfollow(task_detail)

    return json.dumps(mark)

## 点赞
@mod.route('/like_operate/')
def ajax_like_operate():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['mid'] = request.args.get('mid','')

    mark = get_like_operate(task_detail)

    return json.dumps(mark)


'''
主动社交

'''

# 直接搜索
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
@mod.route('/related_recommendation/')
def ajax_related_recommendation():
    task_detail = dict()
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','')
    task_detail['sort_item'] = request.args.get('sort_item','influence')
    
    results = get_related_recommendation(task_detail)

    return json.dumps(results)

# 显示粉丝
@mod.route('/create_group_show_fans/')
def ajax_create_group_show_fans():
    
    xnr_user_no = request.args.get('xnr_user_no','')

    results = get_create_group_show_fans(xnr_user_no)

    return json.dumps(results)

# 创建群组
@mod.route('/create_group/')
def ajax_create_group():
    task_detail = dict()
    #task_detail['weibo_mail_account'] = request.args.get('weibo_mail_account','')
    #task_detail['weibo_phone_account'] = request.args.get('weibo_phone_account','')
    task_detail['xnr_user_no'] = request.args.get('xnr_user_no','') 
    task_detail['group'] = request.args.get('group','')  # 群名字
    task_detail['members'] = request.args.get('members','')  # 群成员id，多个用','分开

    results = get_create_group(task_detail)

    return json.dumps(results)

# 展示跟随转发定时列表
@mod.route('/show_retweet_timing_list/')
def ajax_show_retweet_timing_list():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_show_retweet_timing_list(xnr_user_no)

    return json.dumps(results)

# 展示重点关注用户信息
@mod.route('/show_trace_followers/')
def ajax_show_trace_followers():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_show_trace_followers(xnr_user_no)

    return json.dumps(results)

# 重点关注
@mod.route('/trace_follow/')
def ajax_trace_follow_operate():
    xnr_user_no = request.args.get('xnr_user_no','')
    uid_string = request.args.get('uid_string','')    # 不同uid之间用中文逗号“，”隔开
    nick_name_string = request.args.get('nick_name_string','')  # 不同昵称之间用中文逗号分隔
    results = get_trace_follow_operate(xnr_user_no,uid_string,nick_name_string)

    return json.dumps(results)   # [mark,fail_nick_name_list]  fail_nick_name_list为添加失败，原因是背景信息库没有这些人，请换成对应uid试试。

# 取消重点关注
@mod.route('/un_trace_follow/')
def ajax_un_trace_follow_operate():
    xnr_user_no = request.args.get('xnr_user_no','')
    uid_string = request.args.get('uid_string','')    # 不同uid之间用中文逗号“，”隔开
    nick_name_string = request.args.get('nick_name_string','')  # 不同昵称之间用中文逗号分隔
    results = get_un_trace_follow_operate(xnr_user_no,uid_string,nick_name_string)

    return json.dumps(results)  # [mark,fail_uids,fail_nick_name_list]  fail_uids - 取消失败的uid  fail_nick_name_list -- 原因同上
