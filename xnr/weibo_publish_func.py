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
def follow_tweet_func(xnr_user_no,account_name,password,uid):

    xnr = SinaLauncher(account_name,password)
    xnr.login()
    user = SinaOperateAPI(xnr.uid)
    user.r_mid = uid
    mark = user.followed()
    save_type = 'followers'
    follow_type = 'follow'
    save_to_fans_follow_ES(xnr_user_no,uid,save_type,follow_type)

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
    save_to_fans_follow_ES(xnr_user_no,uid,save_type,follow_type)

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
        request = urllib2.Request(u_url)
        response = urllib2.urlopen(request, timeout=60)
        content = json.loads(response.read())
        return content
    except Exception, e:
        print "download page error!!! ", e
        return 'error'

if __name__ == '__main__':

    es.update(index='weibo_xnr',doc_type='user',id='WXNR0004',body={'doc':{'submitter':'admin@qq.com'}})
    es.update(index='weibo_xnr',doc_type='user',id='WXNR0002',body={'doc':{'submitter':'admin@qq.com'}})
    es.update(index='weibo_xnr',doc_type='user',id='WXNR0003',body={'doc':{'submitter':'admin@qq.com'}})
    es.update(index='weibo_xnr',doc_type='user',id='WXNR0006',body={'doc':{'submitter':'admin@qq.com'}})
    es.update(index='weibo_xnr',doc_type='user',id='WXNR0005',body={'doc':{'submitter':'admin@qq.com'}})
    es.update(index='weibo_xnr',doc_type='user',id='WXNR0007',body={'doc':{'submitter':'admin@qq.com'}})
    #result = es.search(index='weibo_domain',doc_type='group',body={'query':{'match_all':{}}})['hits']['hits']

    # f_domain_data = open('domain.txt','rb')

    # for data in f_domain_data:
    #     data = json.loads(data)
    #     for domain in data:
    #         domain = domain['_source']
    #         domain_pinyin = json.loads(domain['domain_pinyin'])
    #         domain['domain_pinyin'] = domain_pinyin
    #         domain['domain_name'] = json.loads(domain['domain_name'])
    #         domain['submitter'] = json.loads(domain['submitter'])
    #         domain['political_side'] = json.loads(domain['political_side'])
    #         domain['top_keywords'] = json.loads(domain['top_keywords'])
    #         domain['role_distribute'] = json.loads(domain['role_distribute'])
    #         domain['create_type'] = json.loads(domain['create_type'])
    #         domain['topic_preference'] = json.loads(domain['topic_preference'])
    #         domain['remark'] = json.loads(domain['remark'])
    #         domain['create_time'] = int(domain['create_time'])

    #         if domain_pinyin == 'wei_quan_qun_ti':
    #             domain['xnr_user_no'] = 'WXNR0001'
    #             domain['description'] =  '追踪维权群体'
    #         else:
    #             domain['xnr_user_no'] = 'WXNR0004'
    #             domain['description'] =  '追踪乌镇群体'
    #         print 'domain:::',domain
    #         es.index(index='weibo_domain',doc_type='group',body=domain,id=domain_pinyin)

    # es.delete(index='weibo_domain',doc_type='group',id='wu_zhen')
    # es.delete(index='weibo_domain',doc_type='group',id='wei_quan_qun_ti')
    # f_domain_data.write(json.dumps(result))

    # with open('weibo_xnr.json','wb') as f:
    #     result = es.search(index='weibo_xnr',doc_type='user',body={'query':{'match_all':{}}})['hits']['hits']
    #     json.dump(result,f)

    # with open('weibo_xnr.json','rb') as f:
    #     data = json.load(f)

    #     for item in data:
    #         item = item['_source']
    #         xnr_user_no = item['xnr_user_no']
    #         es.index(index='weibo_xnr',doc_type='user',id=xnr_user_no,body=item)




