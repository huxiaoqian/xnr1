# -*-coding:utf-8-*-
import os
import time
import json
import sys

from facebook.fb_operate import Operation
from timed_python_files.fb_xnr_flow_text_mappings import fb_xnr_flow_text_mappings
from global_utils import es_xnr as es, fb_xnr_index_name, fb_xnr_index_type,\
                        fb_xnr_flow_text_index_name_pre,fb_xnr_flow_text_index_type
from utils import fb_save_to_fans_follow_ES

def fb_save_to_xnr_flow_text(tweet_type,xnr_user_no,text, message_type):

    current_time = int(time.time())
    current_date = ts2datetime(current_time)
    xnr_flow_text_index_name = fb_xnr_flow_text_index_name_pre + current_date

    item_detail = {}
    item_detail['uid'] = fb_xnr_user_no2uid(xnr_user_no)
    item_detail['xnr_user_no'] = xnr_user_no
    item_detail['text'] = text
    item_detail['task_source'] = tweet_type
    item_detail['message_type'] = message_type
    #item_detail['topic_field'] = ''
    item_detail['fid'] = ''
    task_id = xnr_user_no + '_' + str(current_time)
    
    #classify_results = topic_classfiy(classify_mid_list, classify_text_dict)

    try:
        
        result = fb_xnr_flow_text_mappings(xnr_flow_text_index_name)
        
        index_result = es.index(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,\
                id=task_id,body=item_detail)
        
        mark = True

    except:
        mark = False

    return mark


# 发帖
def fb_publish(account_name, password, text, tweet_type, xnr_user_no):

    operation = Operation(account_name,password)
    
    #try:
    print 'fb111'
    print operation.publish(text)
    print 'fb222'
    mark = True
    # except:
    #     mark = False

    message_type = 1 # 原创

    try:
        save_mark = fb_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark


# 评论
def fb_comment(account_name, password, _id, uid, text, tweet_type, xnr_user_no):

    operation = Operation(account_name,password)
    
    #try:
    print operation.comment(_id, uid,text)
    mark = True
    # except:
    #     mark = False

    message_type = 2 # 评论
    
    # try:
    #     save_mark = fb_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    # except:
    #     print '保存微博过程遇到错误！'
    #     save_mark = False

    return mark


# 转发
def fb_retweet(account_name, password, _id, uid, text, tweet_type, xnr_user_no):

    operation = Operation(account_name,password)
    
    #try:
    print operation.share(_id, uid,text)
    mark = True
    # except:
    #     mark = False

    message_type = 3 # 转发
    
    # try:
    #     save_mark = fb_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    # except:
    #     print '保存微博过程遇到错误！'
    #     save_mark = False

    return mark

# 关注
def fb_follow(account_name, password, uid, xnr_user_no, trace_type):

    operation = Operation(account_name,password)
    
    #try:
    print '11111'
    operation.follow(uid)
    print '22222'
    mark = True
    # except:
    #     mark = False

    #save_type = 'followers'
    follow_type = 'follow'
    # trace_type = 'trace_follow' or 'ordinary_follow'
    if trace_type == 'trace_follow':
        fb_save_to_fans_follow_ES(xnr_user_no,uid,follow_type,trace_type)

    return mark


# 取消关注
def fb_unfollow(account_name, password, uid, xnr_user_no):

    operation = Operation(account_name,password)
    
    # try:
    print operation.not_follow(uid)
    mark = True
    # except:
    #     mark = False

    #save_type = 'friends'
    follow_type = 'unfollow'
    # trace_type = 'trace_follow' or 'ordinary_follow'
    trace_type = 'trace_follow'

    # fb_save_to_fans_follow_ES(xnr_user_no,uid,follow_type,trace_type)

    return mark

# 点赞
def fb_like(account_name,password, _id, uid):
    # uid: 原贴用户id
    operation = Operation(account_name,password)
    
    #try:
    operation.like(_id,uid)
    mark = True
    # except:
    #     mark = False

   
    return mark


# 提到

def fb_mention(account_name,password, user_name, text, xnr_user_no, tweet_type):
    # uid: 原贴用户id
    operation = Operation(account_name,password)
    
    #try:

    print operation.mention(user_name, text)
    mark = True
    # except:
    #     mark = False
    
    message_type = 4 # 提到
    
    # try:
    #     save_mark = fb_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    # except:
    #     print '保存微博过程遇到错误！'
    #     save_mark = False

    return mark


# 私信

# 私信
def fb_message(account_name,password, text, uid):

    operation = Operation(account_name,password)
    
    #try:
    print operation.send_message(uid, text)
    mark = True
    # except:
    #     mark = False

    return mark


'''
operation = Operation('8617078448226','xnr123456')
#operation.publish('12.24 test')
#operation.mention('xerxes','12.24 test')
operation.follow('100022568024116')
#operation.not_follow('100022568024116')
#operation.like('tl_unit_-8182132709408758851','100022568024116')
#operation.comment('tl_unit_-8182132709408758851','100022568024116','12.26 test')
#operation.share('tl_unit_-8182132709408758851','100022568024116','12.26 test')
'''


