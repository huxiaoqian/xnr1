#-*- coding:utf-8 -*-
import os
import time
import json
import sys
import urllib
import urllib2

#from sina.weibo_publish import weibo_publish_main
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
                        weibo_hot_keyword_task_index_type,index_sensing,type_sensing,\
                        xnr_flow_text_index_name_pre,xnr_flow_text_index_type
from utils import save_to_fans_follow_ES,xnr_user_no2uid
from weibo_xnr_flow_text_mappings import weibo_xnr_flow_text_mappings
from time_utils import ts2datetime

## 获取实时数据表最新的timestamp
def newest_time_func(uid):
    
    query_body = {'query':{'term':{'root_uid':uid}},'sort':{'timestamp':{'order':'desc'}}}
    try:
        weibo_feedback_retweet_index_name = weibo_feedback_retweet_index_name + '_*'
        timestamp_retweet = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_retweet = 0
    
    try:    
        weibo_feedback_like_index_name = weibo_feedback_like_index_name + '_*'
        timestamp_like = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
                        body=query_body)['hits']['hits'][0]['_source']['timestamp']
    except:
        timestamp_like = 0
    #timestamp_follow = es.search(index=weibo_feedback_follow_index_name,doc_type=weibo_feedback_follow_index_type,\
                       # body=query_body)['hits']['hits'][0]['_source']['timestamp']
    #timestamp_fans = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
                        #body=query_body)['hits']['hits'][0]['_source']['timestamp']
    try:

        weibo_feedback_at_index_name = weibo_feedback_at_index_name + '_*'

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
        weibo_feedback_private_index_name = weibo_feedback_private_index_name + '_*'

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
        weibo_feedback_comment_index_name = weibo_feedback_comment_index_name + '_*'
        
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
def publish_tweet_func(account_name,password,text,p_url,rank,rankid,tweet_type,xnr_user_no):
    
    mark = 1#weibo_publish_main(account_name,password,text,p_url)

    '''
    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.rank = rank
    
    new_p_url = user.request_image_url(p_url)
    
    user.pic_ids = ' '.join(new_p_url)
    user.rankid = rankid
    
    mark = user.publish()
    '''
    
    # 保存微博
    if mark:
        try:
            save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
        except:
            print '保存微博过程遇到错误！'
            save_mark = False

    return mark

## 转发微博
def retweet_tweet_func(account_name,password,text,r_mid,tweet_type,xnr_user_no):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.r_mid = r_mid
    mark = user.retweet()

    # 保存微博
    if mark:
        try:
            save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
        except:
            print '保存微博过程遇到错误！'
            save_mark = False
    
    return mark

## 回复
def reply_tweet_func(account_name,password,text,r_mid,mid,uid):
    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.r_mid = r_mid
    # user.r_uid = xnr.uid
    user.uid = uid
    user.cid = mid
    mark = user.receive()
    return mark

## 评论微博
def comment_tweet_func(account_name,password,text,r_mid,tweet_type,xnr_user_no):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.text = text
    user.r_mid = r_mid
    mark = user.comment()
    #mark = user.receive()

    # 保存微博
    if mark:
        try:
            save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
        except:
            print '保存微博过程遇到错误！'
            save_mark = False

    return mark

# ## 私信
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
def follow_tweet_func(xnr_user_no,account_name,password,uid,trace_type):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.r_mid = uid
    mark = user.followed()
    save_type = 'followers'
    follow_type = 'follow'
    save_to_fans_follow_ES(xnr_user_no,uid,save_type,follow_type,trace_type)

    return mark

## 取消关注
def unfollow_tweet_func(xnr_user_no,account_name,password,uid):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.r_mid = uid
    mark = user.unfollowed()

    save_type = 'followers'
    follow_type = 'unfollow'
    trace_type = 'unfollow'
    save_to_fans_follow_ES(xnr_user_no,uid,save_type,follow_type,trace_type)

    return mark

## 创建群组
def create_group_func(account_name,password,group,members):
    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.group = group
    user.members = members
    mark = user.createGroup()

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
        print 'u_url::',u_url
        request = urllib2.Request(u_url)
        print 'request:::',request
        response = urllib2.urlopen(request, timeout=60)
        print 'response::',response
        content = json.loads(response.read())
        print 'content::',content
        return content
    except Exception, e:
        print "download page error!!! ", e
        return 'error'


def save_to_xnr_flow_text(tweet_type,xnr_user_no,text):
    current_time = int(time.time())
    current_date = ts2datetime(current_time)
    xnr_flow_text_index_name = xnr_flow_text_index_name_pre + current_date

    item_detail = {}
    item_detail['uid'] = xnr_user_no2uid(xnr_user_no)
    item_detail['xnr_user_no'] = xnr_user_no
    item_detail['text'] = text
    item_detail['task_source'] = tweet_type
    #item_detail['topic_field'] = ''
    item_detail['mid'] = ''
    task_id = xnr_user_no + '_' + str(current_time)
    
    #classify_results = topic_classfiy(classify_mid_list, classify_text_dict)

    try:
        print 'xnr_flow_text_index_name:::',xnr_flow_text_index_name
        result = weibo_xnr_flow_text_mappings(xnr_flow_text_index_name)
        print 'result::',result
        index_result = es.index(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,\
                id=task_id,body=item_detail)
        print 'index_result:::',index_result
        mark = True

    except:
        mark = False

    return mark


if __name__ == '__main__':

    #result = es.search(index='weibo_domain',doc_type='group',body={'query':{'match_all':{}}})['hits']['hits']
    print getUserShow(screen_name='巨星大大')
    # f_domain_data = open('domain.txt','rb')
