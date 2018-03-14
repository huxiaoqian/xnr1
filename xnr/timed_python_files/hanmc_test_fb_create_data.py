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


root_uid = '100018797745111'

def random_uid():
    return random.choice(["100023849442394", "100023545574584"])  

def load_timestamp(date):
    return datetime2ts(date) + random.randint(1,500)

def random_text():
    return random.choice(["转发", "aaaaaaaaa", "好无聊啊", "别看了，我瞎填的","Love you,baby.", "祝福~", "止水桑生死成谜"])  

def random_mid():
    return random.choice(["4161285573158974", "4161391865302116", "4161391957367337"])  

def random_comment_type():
    return random.choice(["make", "receive"])  

def random_private_type():
    return random.choice(["make", "receive"])  

# 点赞
def like(date):
    facebook_feedback_like_index_name = facebook_feedback_like_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    facebook_feedback_like_mappings(facebook_feedback_like_index_name)
    print es.index(index=facebook_feedback_like_index_name, doc_type=facebook_feedback_like_index_type, body=data)

# 分享
def retweet(date):
    facebook_feedback_retweet_index_name = facebook_feedback_retweet_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    facebook_feedback_retweet_mappings(facebook_feedback_retweet_index_name)
    print es.index(index=facebook_feedback_retweet_index_name, doc_type=facebook_feedback_retweet_index_type, body=data)

# 标记
def at(date):
    facebook_feedback_at_index_name = facebook_feedback_at_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    facebook_feedback_at_mappings(facebook_feedback_at_index_name)
    print es.index(index=facebook_feedback_at_index_name, doc_type=facebook_feedback_at_index_type, body=data)

# 评论
def comment(date):
    facebook_feedback_comment_index_name = facebook_feedback_comment_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'comment_type': random_comment_type(),
    }
    facebook_feedback_comment_mappings(facebook_feedback_comment_index_name)
    print es.index(index=facebook_feedback_comment_index_name, doc_type=facebook_feedback_comment_index_type, body=data)

# 私信
def private(date):
    facebook_feedback_private_index_name = facebook_feedback_private_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'private_type': random_private_type(),
    }
    facebook_feedback_private_mappings(facebook_feedback_private_index_name)
    print es.index(index=facebook_feedback_private_index_name, doc_type=facebook_feedback_private_index_type, body=data)

# 好友列表
def friends(date):
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    facebook_feedback_friends_mappings(facebook_feedback_friends_index_name)
    print es.index(index=facebook_feedback_friends_index_name, doc_type=facebook_feedback_friends_index_type, body=data)


if __name__ == '__main__':
    #2017-10-25     2017-10-31 
    date = '2017-10-31'
    for i in range(random.randint(2,5)):
        # like(date)
        # retweet(date)
        # at(date)
        # comment(date)
        # private(date)
        friends(date)

