#-*- coding:utf-8 -*-
import os
import time
import json
import sys
import urllib
import urllib2

from sina.weibo_operate import SinaOperateAPI
from sina.tools.Launcher import SinaLauncher
from global_utils import es_xnr as es
from global_utils import weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
						weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
						weibo_feedback_private_index_name,weibo_feedback_private_index_type,\
						weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
						weibo_feedback_like_index_name,weibo_feedback_like_index_type,\
						weibo_feedback_fans_index_name,weibo_feedback_fans_index_type,\
						weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
                        weibo_xnr_index_name,weibo_xnr_index_type,weibo_report_management_index_name,\
                        weibo_report_management_index_type,weibo_xnr_fans_followers_index_name,\
                        weibo_xnr_fans_followers_index_type,weibo_hot_keyword_task_index_name,\
                        weibo_hot_keyword_task_index_type,index_sensing,type_sensing

## 获取实时数据表最新的timestamp
def newest_time_func(uid):
    
    query_body = {'query':{'term':{'root_uid':uid}},'sort':{'timestamp':{'order':'desc'}}}
    try:
        timestamp_retweet = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_retweet = 0
    
    try:    
        timestamp_like = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_like = 0
    #timestamp_follow = es.search(index=weibo_feedback_follow_index_name,doc_type=weibo_feedback_follow_index_type,\
                       # body=query_body)['hits']['hits'][0]['_source']['timestamp']
    #timestamp_fans = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
                        #body=query_body)['hits']['hits'][0]['_source']['timestamp']
    try:
        timestamp_at = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_at = 0
    
    query_body_private = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}}
                ]
            }
        },
        'sort':{'timestamp':{'order':'desc'}}
    }
    try:
        timestamp_private = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_private = 0
    '''
    query_body_private_make = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'private_type':'make'}}
                ]
            }
        },
        'sort':{'timestamp':{'order':'desc'}}
    }

    timestamp_private_make = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    '''

    query_body_comment_receive = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'comment_type':'receive'}}
                ]
            }
        },
        'sort':{'timestamp':{'order':'desc'}}
    }
    try:
        timestamp_comment_receive = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_comment_receive = 0

    query_body_comment_make = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'comment_type':'make'}}
                ]
            }
        },
        'sort':{'timestamp':{'order':'desc'}}
    }

    try:
        timestamp_comment_make = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_comment_make = 0
    return timestamp_retweet, timestamp_like, timestamp_at, \
        timestamp_private, timestamp_comment_receive, timestamp_comment_make

## 发布微博
def publish_tweet_func(account_name,password,text,p_url,rank,rankid):
    print 'account_name::',account_name
    print 'password:::',password
    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.rank = rank
    new_p_url = user.request_image_url(p_url)
    #print 'new_p_url::',new_p_url
    user.pic_ids = ' '.join(new_p_url)
    user.rankid = rankid
    #print 'user.pic_ids::',user.pic_ids
    mark = user.publish()

    return mark

## 转发微博
def retweet_tweet_func(account_name,password,text,r_mid):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.r_mid = r_mid
    mark = user.retweet()
    
    return mark


## 评论微博
def comment_tweet_func(account_name,password,text,r_mid):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.r_mid = r_mid
    mark = user.comment()

    return mark

## 私信
def private_tweet_func(account_name,password,text,r_mid):
    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.r_mid = r_mid
    mark = user.privmessage()

    return mark

## 点赞
def like_tweet_func(account_name,password,r_mid):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.r_mid = r_mid
    mark = user.like()

    return mark

## 关注
def follow_tweet_func(account_name,password,uid):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.r_mid = uid
    mark = user.followed()

    return mark

## 取消关注
def unfollow_tweet_func(account_name,password,uid):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.r_mid = uid
    mark = user.unfollowed()

    return mark

## 创建群组
def create_group_func(account_name,password,group,members):
    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.group = group
    user.members = members
    mark = user.createGroup()
    print 'mark::',mark
    return mark


def getUserShow(uid=None, screen_name=None):
    """
    字段说明见userinfo.txt
    :return:
    """
    u_url = 'https://api.weibo.com/2/users/show.json?access_token=2.009t4mFGWp4peBbb59564f4e5n6k6B'
    if uid:
        u_url += "&uid=" + uid
    if screen_name:
        u_url += "&screen_name=" + screen_name

    try:
        print 'ooooooo'
        request = urllib2.Request(u_url)
        response = urllib2.urlopen(request, timeout=60)
        print '343434'
        content = json.loads(response.read())
        print 'content:',content
        return content
    except Exception, e:
        print "download page error!!! ", e
        return 'error'




if __name__ == '__main__':

    #getUserShow(uid=None, screen_name=None)

    # task_detail = {}
    # task_detail['xnr_user_no'] = 'WXNR0004'
    # task_detail['mid'] = '4043503421741766'
    # task_detail['compute_status'] = 0
    # task_detail['submit_time'] = 1503057474
    # task_detail['submit_user'] = 'admin@qq.com'
    # #task_detail['task_id'] = '4043503421741766'
    # task_detail['keywords_string'] = u'朴槿惠&崔顺实'

    # _id = task_detail['xnr_user_no'] + '_' + task_detail['mid']

    # task_detail = {}
    # task_detail['xnr_user_no'] = 'WXNR0004'
    # task_detail['mid'] = '4043274014747152'
    # task_detail['compute_status'] = 0
    # task_detail['submit_time'] = 1503057589
    # task_detail['submit_user'] = 'admin@qq.com'
    # #task_detail['task_id'] = '4043450590377035'
    # task_detail['keywords_string'] = u'哈里&梅根.马克尔'
    # _id = task_detail['xnr_user_no'] + '_' + task_detail['mid']

    # task_detail = {}
    # task_detail['xnr_user_no'] = 'WXNR0004'
    # task_detail['mid'] = '4043433776005723'
    # task_detail['compute_status'] = 0
    # task_detail['submit_time'] = 1503057589
    # task_detail['submit_user'] = 'admin@qq.com'
    # #task_detail['task_id'] = '4043450590377035'
    # task_detail['keywords_string'] = u'习近平&厄瓜多尔'
    # _id = task_detail['xnr_user_no'] + '_' + task_detail['mid']

    # es.index(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
    #         id=_id,body=task_detail)

    es.delete(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
             id='WXNR0004_4043503421741766')

    es.delete(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
             id='WXNR0004_4043450590377035')

    # get_result = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
    #     id='WXNR0004')['_source']

    # followers = get_result['followers_list']
    # print 'followers::',type(followers)
    # item = {}
    # item['social_sensors'] = followers
    # item['task_name'] = '感知热门事件'
    # item['history_status'] = ''
    # item['remark'] = '感知热门事件'
    # item['xnr_user_no'] = 'WXNR0004'

    # es.index(index=index_sensing,doc_type=type_sensing,id='WXNR0004',body=item)