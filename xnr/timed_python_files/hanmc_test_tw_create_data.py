#-*-coding:utf-8-*-
import os
import json
import time
import random
from elasticsearch import Elasticsearch
import sys
sys.path.append('../')
from global_utils import es_xnr as es,twitter_feedback_comment_index_name_pre,twitter_feedback_comment_index_type,\
                        twitter_feedback_retweet_index_name_pre,twitter_feedback_retweet_index_type,\
                        twitter_feedback_private_index_name_pre,twitter_feedback_private_index_type,\
                        twitter_feedback_at_index_name_pre,twitter_feedback_at_index_type,\
                        twitter_feedback_like_index_name_pre,twitter_feedback_like_index_type,\
                        twitter_feedback_fans_index_name,twitter_feedback_fans_index_type,\
                        twitter_feedback_follow_index_name, twitter_feedback_follow_index_type
from time_utils import ts2datetime, datetime2ts
from twitter_feedback_mappings_timer import twitter_feedback_like_mappings, twitter_feedback_retweet_mappings,\
                                            twitter_feedback_at_mappings, twitter_feedback_comment_mappings,\
                                            twitter_feedback_private_mappings, twitter_feedback_fans_mappings,\
                                            twitter_feedback_follow_mappings


root_uid = '747226658457927680'

def random_uid():
    return random.choice(["943290911039029250", "864789252629909504", "827724832380825601"])  

def load_timestamp(date):
    return datetime2ts(date) + random.randint(1,500)

def random_text():
    return random.choice(["转发", "aaaaaaaaa", "好无聊啊", "别看了，我瞎填的","Love you,baby.", "祝福~", "止水桑生死成谜"])  

def random_mid():
    return random.choice(["378922805758132224", "920318962453352448", "920319215151677440"])  

def random_comment_type():
    return random.choice(["make", "receive"])  

def random_private_type():
    return random.choice(["make", "receive"])  

# 点赞
def like(date):
    twitter_feedback_like_index_name = twitter_feedback_like_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    twitter_feedback_like_mappings(twitter_feedback_like_index_name)
    print es.index(index=twitter_feedback_like_index_name, doc_type=twitter_feedback_like_index_type, body=data)

# 分享
def retweet(date):
    twitter_feedback_retweet_index_name = twitter_feedback_retweet_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    twitter_feedback_retweet_mappings(twitter_feedback_retweet_index_name)
    print es.index(index=twitter_feedback_retweet_index_name, doc_type=twitter_feedback_retweet_index_type, body=data)

# 标记
def at(date):
    twitter_feedback_at_index_name = twitter_feedback_at_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    twitter_feedback_at_mappings(twitter_feedback_at_index_name)
    print es.index(index=twitter_feedback_at_index_name, doc_type=twitter_feedback_at_index_type, body=data)

# 评论
def comment(date):
    twitter_feedback_comment_index_name = twitter_feedback_comment_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'comment_type': random_comment_type(),
    }
    twitter_feedback_comment_mappings(twitter_feedback_comment_index_name)
    print es.index(index=twitter_feedback_comment_index_name, doc_type=twitter_feedback_comment_index_type, body=data)

# 私信
def private(date):
    twitter_feedback_private_index_name = twitter_feedback_private_index_name_pre + date
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'private_type': random_private_type(),
    }
    twitter_feedback_private_mappings(twitter_feedback_private_index_name)
    print es.index(index=twitter_feedback_private_index_name, doc_type=twitter_feedback_private_index_type, body=data)

# 粉丝列表
def fans(date):
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    twitter_feedback_fans_mappings()
    print es.index(index=twitter_feedback_fans_index_name, doc_type=twitter_feedback_fans_index_type, body=data)

# 关注列表
def follow(date):
    data = {
        'root_uid': root_uid,
        'uid': random_uid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
    }
    twitter_feedback_follow_mappings()
    print es.index(index=twitter_feedback_follow_index_name, doc_type=twitter_feedback_follow_index_type, body=data)

if __name__ == '__main__':
    #2017-10-25     2017-10-31 
    date = '2017-10-31'
    for i in range(random.randint(2,5)):
        like(date)
        retweet(date)
        at(date)
        comment(date)
        private(date)
        fans(date)
        follow(date)

