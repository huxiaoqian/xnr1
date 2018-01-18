# -*-coding:utf-8-*-
import os
import time

from twitter.twitter_operate import Operation
from timed_python_files.tw_xnr_flow_text_mappings import tw_xnr_flow_text_mappings
from global_utils import es_xnr as es, tw_xnr_index_name, tw_xnr_index_type,\
                        tw_xnr_flow_text_index_name_pre,tw_xnr_flow_text_index_type
from utils import tw_save_to_fans_follow_ES, tw_xnr_user_no2uid
from time_utils import ts2datetime


def tw_save_to_xnr_flow_text(tweet_type,xnr_user_no,text, message_type):

    current_time = int(time.time())
    current_date = ts2datetime(current_time)
    xnr_flow_text_index_name = tw_xnr_flow_text_index_name_pre + current_date

    item_detail = {}
    item_detail['uid'] = tw_xnr_user_no2uid(xnr_user_no)
    item_detail['xnr_user_no'] = xnr_user_no
    item_detail['text'] = text
    item_detail['task_source'] = tweet_type
    item_detail['message_type'] = message_type
    #item_detail['topic_field'] = ''
    item_detail['tid'] = ''
    task_id = xnr_user_no + '_' + str(current_time)
    
    #classify_results = topic_classfiy(classify_mid_list, classify_text_dict)

    try:
        
        result = tw_xnr_flow_text_mappings(xnr_flow_text_index_name)
        
        index_result = es.index(index=xnr_flow_text_index_name,doc_type=tw_xnr_flow_text_index_type,\
                id=task_id,body=item_detail)
    
        mark = True

    except:
        mark = False

    return mark


# 发帖
def tw_publish(account_name, password, text, tweet_type, xnr_user_no):

    operation = Operation(account_name,password)
    
    try:
        operation.publish(text)
        #print 'publish....',
        mark = True
    except:
        mark = False
    
    message_type = 1 # 原创

    try:  
        save_mark = tw_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark


# 评论
def tw_comment(account_name, password, _id, uid, text, tweet_type, xnr_user_no):

    operation = Operation(account_name,password)
    
    try:
        #screen_name = 'zhu0588'
    #operation.target(nick_name)
    # print 'comment...',operation.do_comment(_id, uid,text)
        operation.do_comment(uid,_id,text)
    
        mark = True
        
    except:
        mark = False

    message_type = 2 # 评论
    
    try:
        save_mark = tw_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark


# 转发
def tw_retweet(account_name, password, _id, uid, text, tweet_type, xnr_user_no):

    operation = Operation(account_name,password)
    
    try:
    #print operation.share(_id, uid,text)
    
        operation.do_retweet(_id)
    
        mark = True
    except:
        mark = False

    message_type = 3 # 转发
    
    try:
        save_mark = tw_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark

# 关注
def tw_follow(account_name, password, screen_name, uid, xnr_user_no, trace_type):

    operation = Operation(account_name,password)
    
    #try:
    print operation.follow(screen_name)
    mark = True
    # except:
    #     mark = False
    ###
    # ?????????  screen_name ? uid
    ####
    #save_type = 'followers'
    follow_type = 'follow'
    # trace_type = 'trace_follow' or 'ordinary_follow'
    if trace_type == 'trace_follow':
        tw_save_to_fans_follow_ES(xnr_user_no,uid,follow_type,trace_type)
        #tw_save_to_fans_follow_ES(xnr_user_no,screen_name,follow_type,trace_type)

    return mark


# 取消关注
def tw_unfollow(account_name, password, uid, xnr_user_no):

    operation = Operation(account_name,password)
    
    try:
        operation.destroy_friendship(uid)
        mark = True
    except:
        mark = False

    #save_type = 'friends'
    #follow_type = 'unfollow'
    # trace_type = 'trace_follow' or 'ordinary_follow'
    #trace_type = 'trace_follow'

    # tw_save_to_fans_follow_ES(xnr_user_no,uid,follow_type,trace_type)
    #tw_save_to_fans_follow_ES(xnr_user_no,screen_name,follow_type,trace_type)

    return mark

# 点赞
def tw_like(account_name,password, _id):
    # uid: 原贴用户id
    operation = Operation(account_name,password)
    
    try:
        operation.do_favourite(long(_id))
        mark = True
    except:
        mark = False
   
    return mark


# 提到

def tw_mention(account_name,password, text, xnr_user_no, tweet_type):
    # text = '@lvleilei1 test'
    operation = Operation(account_name,password)
    
    #try:
    print operation.mention(text)
    mark = True
    # except:
    #     mark = False
    
    message_type = 4 # 提到
    
    try:
        save_mark = tw_save_to_xnr_flow_text(tweet_type,xnr_user_no,text,message_type)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark

# 私信
def tw_message(account_name,password, text, uid):

    operation = Operation(account_name,password)
    
    try:
        operation.message(uid, text)
        mark = True
    except:
        mark = False

    return mark





