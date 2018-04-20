#-*-coding:utf-8-*-
import os
import json
import time
import random
from elasticsearch import Elasticsearch
import sys
sys.path.append('../')
from global_utils import es_xnr as es
from global_utils import facebook_feedback_comment_index_name_pre,facebook_feedback_comment_index_type,\
                        facebook_feedback_retweet_index_name_pre,facebook_feedback_retweet_index_type,\
                        facebook_feedback_private_index_name_pre,facebook_feedback_private_index_type,\
                        facebook_feedback_at_index_name_pre,facebook_feedback_at_index_type,\
                        facebook_feedback_like_index_name_pre,facebook_feedback_like_index_type,\
                        facebook_feedback_friends_index_name_pre,facebook_feedback_friends_index_type,\
                        facebook_feedback_friends_index_name
from time_utils import ts2datetime, datetime2ts
from facebook_feedback_mappings_timer import facebook_feedback_like_mappings, facebook_feedback_retweet_mappings,\
                                            facebook_feedback_at_mappings, facebook_feedback_comment_mappings,\
                                            facebook_feedback_private_mappings, facebook_feedback_friends_mappings
sys.path.append('../facebook/sensitive')
from get_sensitive import get_sensitive_info, get_sensitive_user


root_uid = '100018797745111'
root_nick_name = u'韩梦成'

def random_uid():
    return random.choice(["100023849442394", "100023545574584"])  

def load_timestamp(date):
    return datetime2ts(date) + random.randint(1,500)

def random_text():
    #普通版
    # return random.choice(["转发", "aaaaaaaaa", "好无聊啊", "别看了，我瞎填的","Love you,baby.", "祝福~", "止水桑生死成谜","达赖","达赖太阳花"])
    #敏感版  
    return random.choice(["止水桑生死成谜","达赖","达赖太阳花"])

def random_mid():
    return random.choice(["4161285573158974", "4161391865302116", "4161391957367337"])  

def random_comment_type():
    return random.choice(["make", "receive"])  

def random_private_type():
    return random.choice(["make", "receive"])  

def random_photo_url():
    return random.choice(["https://scontent-nrt1-1.xx.fbcdn.net/v/t1.0-1/p80x80/10649505_1460124810970956_1628262998961013775_n.png?_nc_cat=0&oh=fc8f06349cc4b8738b3a7fec924c35d9&oe=5B2D4748","https://scontent-nrt1-1.xx.fbcdn.net/v/t1.0-1/p80x80/18446550_164946100704038_7371507250489390884_n.jpg?_nc_cat=0&oh=667d58961b1c2cb35678f0d8386fa6af&oe=5B6FAF58"])

def random_nick_name():
    return random.choice(['國破山河在',"良知媒體","紅冰袁"])

def random_update_time(date):
    return datetime2ts(date) + random.randint(1,500)

def random_facebook_type():
    return random.choice(["好友", "陌生人"])  

def random_retweet_num():
    return random.choice([0,1,3,4,5,7,12])  

def random_like_num():
    return random.choice([0,1,3,4,5,7,12])  

def random_comment_num():
    return random.choice([0,1,3,4,5,7,12])  

def random_friends_num():
    return random.choice([0,15,32,47,52,70,125])

# 点赞
def like(date):
    facebook_feedback_like_index_name = facebook_feedback_like_index_name_pre + date
    nick_name = random_nick_name()
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': nick_name,
        'timestamp': load_timestamp(date),
        'text': nick_name + '赞同了您的帖子',
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_mid': random_mid(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'facebook_type': random_facebook_type(),
    }
    facebook_feedback_like_mappings(facebook_feedback_like_index_name)
    print es.index(index=facebook_feedback_like_index_name, doc_type=facebook_feedback_like_index_type, body=data)

# 分享
def retweet(date):
    facebook_feedback_retweet_index_name = facebook_feedback_retweet_index_name_pre + date
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'mid': random_mid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_mid': random_mid(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'facebook_type': random_facebook_type(),
        'retweet': random_retweet_num(),
        'comment': random_comment_num(),
        'like': random_like_num(),
    }
    facebook_feedback_retweet_mappings(facebook_feedback_retweet_index_name)
    print es.index(index=facebook_feedback_retweet_index_name, doc_type=facebook_feedback_retweet_index_type, body=data)

# 标记
def at(date):
    facebook_feedback_at_index_name = facebook_feedback_at_index_name_pre + date
    nick_name = random_nick_name()
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': nick_name, 
        'mid': random_mid(),
        'timestamp': load_timestamp(date),
        'text': nick_name + '提到了你',
        'update_time': random_update_time(date),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'facebook_type': random_facebook_type(),
    }
    facebook_feedback_at_mappings(facebook_feedback_at_index_name)
    print es.index(index=facebook_feedback_at_index_name, doc_type=facebook_feedback_at_index_type, body=data)

# 评论
def comment(date):
    facebook_feedback_comment_index_name = facebook_feedback_comment_index_name_pre + date
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'mid': random_mid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_mid': random_mid(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'facebook_type': random_facebook_type(),
        'comment_type': random_comment_type(),
    }
    facebook_feedback_comment_mappings(facebook_feedback_comment_index_name)
    print es.index(index=facebook_feedback_comment_index_name, doc_type=facebook_feedback_comment_index_type, body=data)

# 私信
def private(date):
    facebook_feedback_private_index_name = facebook_feedback_private_index_name_pre + date
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'facebook_type': random_facebook_type(),
        'private_type': random_private_type(),
    }
    facebook_feedback_private_mappings(facebook_feedback_private_index_name)
    print es.index(index=facebook_feedback_private_index_name, doc_type=facebook_feedback_private_index_type, body=data)

# 好友列表
def friends(date):
    uid = random_uid()
    data = {
        'uid': uid,
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'friends': random_friends_num(),
        'profile_url': 'https://www.facebook.com/profile.php?id=' + uid,
        'update_time': random_update_time(date),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'facebook_type': '好友',
    }
    facebook_feedback_friends_mappings()
    print es.index(index=facebook_feedback_friends_index_name, doc_type=facebook_feedback_friends_index_type, body=data)


def sensitive_func(index_name, ts):
    bulk_action = []
    query_body = {
        'query':{
            'match_all':{}
        },
        'size': 999,
    }
    res = es.search(index=index_name, doc_type='text', body=query_body)['hits']['hits']
    for r in res:
        _id = r['_id']
        uid = r['_source']['uid']
        mid = ''
        if r['_source'].has_key('mid'):
            mid = r['_source']['mid']
        text = ''
        if r['_source'].has_key('text'):
            text = r['_source']['text']
        sensitive_info = get_sensitive_info(ts, mid, text)
        sensitive_user = get_sensitive_user(ts, uid)
        item = {
            'sensitive_info': sensitive_info,
            'sensitive_user': sensitive_user,
        }

        action = {'update':{'_id':_id}}
        bulk_action.extend([action, {'doc': item}])
    if bulk_action:
        print es.bulk(bulk_action,index=index_name,doc_type='text',timeout=600)

if __name__ == '__main__':
    '''
    #create
    #2017-10-15     2017-10-30
    for i in range(15, 31, 1):
        date = '2017-10-' + str(i)
        print 'date', date
        for i in range(random.randint(2,5)):
            like(date)
            retweet(date)
            at(date)
            comment(date)
            private(date)
            friends(date)
    
    '''
    #update
    #2017-10-15     2017-10-30
    
    bulk_action = []
    for i in range(15, 31, 1):
        date = '2017-10-' + str(i)
        ts = datetime2ts(date)
        for index_name_pre in ['facebook_feedback_at_', 'facebook_feedback_comment_', 'facebook_feedback_retweet_', 'facebook_feedback_private_', 'facebook_feedback_like_']:
            index_name = index_name_pre + date
            sensitive_func(index_name, ts)
        sensitive_func('facebook_feedback_friends', ts)
    
        

