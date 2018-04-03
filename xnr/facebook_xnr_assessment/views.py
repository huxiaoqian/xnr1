#-*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
        abort, flash, session, redirect
from utils import get_influence_total_trend, compute_influence_num, penetration_total,\
                    compute_penetration_num,compute_safe_num, get_safe_active,\
                    get_influence_total_trend_today, penetration_total_today, get_safe_active_today,\
                    get_tweets_distribute, get_safe_tweets,get_follow_group_distribute,get_follow_group_tweets

mod = Blueprint('facebook_xnr_assessment', __name__, url_prefix='/facebook_xnr_assessment')

'''
影响力评估
'''
# 影响力分数计算
@mod.route('/influence_mark/')
def ajax_influ_mark_compute():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = compute_influence_num(xnr_user_no)

    return json.dumps(results)

# 影响力各指标
@mod.route('/influence_total/')
def ajax_influence_total_trend():
    xnr_user_no = request.args.get('xnr_user_no','')
    start_time = request.args.get('start_time','')
    end_time = request.args.get('end_time','')

    results = get_influence_total_trend(xnr_user_no,start_time,end_time)

    return json.dumps(results)


'''
渗透力评估
'''

# 渗透力分数计算
@mod.route('/penetration_mark/')
def ajax_penetration_mark_compute():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = compute_penetration_num(xnr_user_no)

    return json.dumps(results)

# 渗透力各指标
@mod.route('/penetration_total/')
def ajax_penetration_total():
    xnr_user_no = request.args.get('xnr_user_no','')
    start_time = request.args.get('start_time','')
    end_time = request.args.get('end_time','')

    results = penetration_total(xnr_user_no,start_time,end_time)

    return json.dumps(results)



'''
安全性评估
'''
# 安全性分数计算
@mod.route('/safe_mark/')
def ajax_safe_mark_compute():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = compute_safe_num(xnr_user_no)

    return json.dumps(results)

# 活跃安全性
@mod.route('/safe_active/')
def ajax_safe_active():
    xnr_user_no = request.args.get('xnr_user_no','')
    start_time = request.args.get('start_time','')
    end_time = request.args.get('end_time','')

    results = get_safe_active(xnr_user_no,start_time,end_time)

    return json.dumps(results)

# 影响力各指标 -- 今日
@mod.route('/influence_total_today/')
def ajax_influence_total_trend_today():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_influence_total_trend_today(xnr_user_no)
    return json.dumps(results)


# 渗透力各指标 -- 今日
@mod.route('/penetration_total_today/')
def ajax_penetration_total_today():
    xnr_user_no = request.args.get('xnr_user_no','')

    results = penetration_total_today(xnr_user_no)

    return json.dumps(results)

# 活跃安全性 -- 今日
@mod.route('/safe_active_today/')
def ajax_safe_active_today():
    xnr_user_no = request.args.get('xnr_user_no','')

    results = get_safe_active_today(xnr_user_no)

    return json.dumps(results)

# 发帖内容分布
@mod.route('/tweets_distribute/')
def ajax_tweets_distribute():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_tweets_distribute(xnr_user_no)
    return json.dumps(results)

# 发帖内容 --话题
@mod.route('/safe_tweets_topic/')
def ajax_safe_tweets_topic():
    xnr_user_no = request.args.get('xnr_user_no','')
    topic = request.args.get('topic',u'民生类_法律')
    sort_item = request.args.get('sort_item','timestamp')  # 按时间 -- timestamp  按热度---retweeted
    # print 'topic::::',topic
    results = get_safe_tweets(xnr_user_no,topic,sort_item)
    
    return json.dumps(results)

# 关注人群分布
@mod.route('/follow_group_distribute/')
def ajax_follow_group_distribute():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_follow_group_distribute(xnr_user_no)
    
    return json.dumps(results)

# 关注人群领域 -- 发帖内容
@mod.route('/follow_group_tweets/')
def ajax_follow_group_tweets():
    xnr_user_no = request.args.get('xnr_user_no','')
    #domain = request.args.get('domain','')
    domain = request.args.get('domain',u'法律机构及人士')
    sort_item = request.args.get('sort_item','timestamp')  # 按时间 -- timestamp  按热度---retweeted
    results = get_follow_group_tweets(xnr_user_no,domain,sort_item)
    #print 'domain:::',domain
    return json.dumps(results)



"""
#2018-3-8 11:19:09

from xnr.global_utils import es as es_flow_text
from utils import get_influ_fans_num,get_influ_retweeted_num,\
                get_influ_commented_num,get_influ_like_num,get_influ_at_num,get_influ_private_num,\
                compute_influence_num,get_pene_follow_group_sensitive,get_pene_fans_group_sensitive,\
                get_pene_infor_sensitive,get_pene_feedback_sensitive,get_pene_warning_report_sensitive,\
                compute_penetration_num,compute_safe_num,get_safe_active,get_tweets_distribute,\
                get_follow_group_distribute,get_safe_tweets,get_follow_group_tweets,\
                get_influence_total_trend,penetration_total,get_influence_total_trend_today,\
                penetration_total_today,get_safe_active_today

mod = Blueprint('facebook_xnr_assessment', __name__, url_prefix='/facebook_xnr_assessment')


















# # 粉丝数
# @mod.route('/influ_fans_num/')
# def ajax_influ_fans_num():
#   xnr_user_no = request.args.get('xnr_user_no','')
#   results = get_influ_fans_num(xnr_user_no)
#   return json.dumps(results)
# '''
# # 粉丝群的粉丝数
# @mod.route('/influ_fans_fans_num/')
# def ajax_influ_fans_fans_num():
#   xnr_user_no = request.args.get('xnr_user_no','')
#   results = get_influ_fans_fans_num(xnr_user_no)

#   return json.dumps(results)
# '''
# # 被转发
# @mod.route('/influ_retweeted_num/')
# def ajax_influ_retweeted_num():
#   xnr_user_no = request.args.get('xnr_user_no','')
#   results = get_influ_retweeted_num(xnr_user_no)

#   return json.dumps(results)

# # 被评论
# @mod.route('/influ_commented_num/')
# def ajax_influ_commented_num():
#   xnr_user_no = request.args.get('xnr_user_no','')
#   results = get_influ_commented_num(xnr_user_no)

#   return json.dumps(results)

# # 被点赞
# @mod.route('/influ_like_num/')
# def ajax_influ_like_num():
#   xnr_user_no = request.args.get('xnr_user_no','')
#   results = get_influ_like_num(xnr_user_no)

#   return json.dumps(results)

# # 被@
# @mod.route('/influ_at_num/')
# def ajax_influ_at_num():
#   xnr_user_no = request.args.get('xnr_user_no','')
#   results = get_influ_at_num(xnr_user_no)

#   return json.dumps(results)

# # 被私信
# @mod.route('/influ_private_num/')
# def ajax_influ_private_num():
#   xnr_user_no = request.args.get('xnr_user_no','')
#   results = get_influ_private_num(xnr_user_no)

#   return json.dumps(results)






# 关注群体敏感度
@mod.route('/pene_follow_group_sensitive/')
def ajax_pene_follow_group_sensitive():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_pene_follow_group_sensitive(xnr_user_no)

    return json.dumps(results)

# 粉丝群体敏感度
@mod.route('/pene_fans_group_sensitive/')
def ajax_pene_fans_group_sensitive():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_pene_fans_group_sensitive(xnr_user_no)

    return json.dumps(results)

# 发布信息敏感度
@mod.route('/pene_infor_sensitive/')
def ajax_pene_infor_sensitive():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_pene_infor_sensitive(xnr_user_no)

    return json.dumps(results)

# 社交反馈敏感度
@mod.route('/pene_feedback_sensitive/')
def ajax_pene_feedback_sensitive():
    xnr_user_no = request.args.get('xnr_user_no','')
    sort_item = request.args.get('sort_item','be_at')  # 被at- be_at  被转发-be_retweet  被评论- be_comment
    results = get_pene_feedback_sensitive(xnr_user_no,sort_item)

    return json.dumps(results)

# 预警上报敏感度
@mod.route('/pene_warning_report_sensitive/')
def ajax_pene_warning_report_sensitive():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_pene_warning_report_sensitive(xnr_user_no)

    return json.dumps(results)

"""