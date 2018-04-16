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
root_nick_name = u'韩梦成'
root_user_name = 'feifanhanmc1'

def random_uid():
    return random.choice(["864789252629909504", "845341840618536960"])  

def load_timestamp(date):
    return datetime2ts(date) + random.randint(1,500)

def random_text():
    return random.choice(["转发", "aaaaaaaaa", "好无聊啊", "别看了，我瞎填的","Love you,baby.", "祝福~", "止水桑生死成谜"])  

def random_mid():
    return random.choice(["919556871287054337", "919542838899097602", "919370711944359936"])  

def random_comment_type():
    return random.choice(["make", "receive"])  

def random_private_type():
    return random.choice(["make", "receive"])  

def random_photo_url():
    return random.choice(["http://pbs.twimg.com/profile_images/864796502580903936/bbrV5eOj.jpg","http://pbs.twimg.com/profile_images/735118185494515712/cSP28zQR.jpg"])

def random_nick_name():
    return random.choice(['何頻',"龙场悟道","周锋锁 Fengsuo Zhou"])

def random_user_name():
    return random.choice(['ZhouFengSuo',"yangjufeng","lihlii"])

def random_update_time(date):
    return datetime2ts(date) + random.randint(1,500)

def random_twitter_type():
    return random.choice(["好友", "陌生人"])  

def random_retweet_num():
    return random.choice([0,1,3,4,5,7,12])  

def random_like_num():
    return random.choice([0,1,3,4,5,7,12])  

def random_comment_num():
    return random.choice([0,1,3,4,5,7,12])  

def random_fans_num():
    return random.choice([0,15,32,47,52,70,125])

def random_follows_num():
    return random.choice([0,15,32,47,52,70,125])

# 点赞
def like(date):
    twitter_feedback_like_index_name = twitter_feedback_like_index_name_pre + date
    nick_name = random_nick_name()
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'user_name': random_user_name(),
        'nick_name': nick_name,
        'timestamp': load_timestamp(date),
        'text': nick_name + '赞同了您的帖子',
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_mid': random_mid(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'root_user_name': root_user_name,
        'twitter_type': random_twitter_type(),
    }
    twitter_feedback_like_mappings(twitter_feedback_like_index_name)
    print es.index(index=twitter_feedback_like_index_name, doc_type=twitter_feedback_like_index_type, body=data)

# 分享
def retweet(date):
    twitter_feedback_retweet_index_name = twitter_feedback_retweet_index_name_pre + date
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'user_name': random_user_name(),
        'mid': random_mid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_mid': random_mid(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'root_user_name': root_user_name,
        'twitter_type': random_twitter_type(),
        'retweet': random_retweet_num(),
        'comment': random_comment_num(),
        'like': random_like_num(),
    }
    twitter_feedback_retweet_mappings(twitter_feedback_retweet_index_name)
    print es.index(index=twitter_feedback_retweet_index_name, doc_type=twitter_feedback_retweet_index_type, body=data)

# 标记
def at(date):
    twitter_feedback_at_index_name = twitter_feedback_at_index_name_pre + date
    nick_name = random_nick_name()
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': nick_name,
        'user_name': random_user_name(), 
        'mid': random_mid(),
        'timestamp': load_timestamp(date),
        'text': nick_name + '提到了你',
        'update_time': random_update_time(date),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'root_user_name': root_user_name,
        'twitter_type': random_twitter_type(),
    }
    twitter_feedback_at_mappings(twitter_feedback_at_index_name)
    print es.index(index=twitter_feedback_at_index_name, doc_type=twitter_feedback_at_index_type, body=data)

# 评论
def comment(date):
    twitter_feedback_comment_index_name = twitter_feedback_comment_index_name_pre + date
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'user_name': random_user_name(),
        'mid': random_mid(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_mid': random_mid(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'root_user_name': root_user_name,
        'twitter_type': random_twitter_type(),
        'comment_type': random_comment_type(),
    }
    twitter_feedback_comment_mappings(twitter_feedback_comment_index_name)
    print es.index(index=twitter_feedback_comment_index_name, doc_type=twitter_feedback_comment_index_type, body=data)

# 私信
def private(date):
    twitter_feedback_private_index_name = twitter_feedback_private_index_name_pre + date
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'user_name': random_user_name(),
        'timestamp': load_timestamp(date),
        'text': random_text(),
        'update_time': random_update_time(date),
        'root_text': random_text(),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'root_user_name': root_user_name,
        'twitter_type': random_twitter_type(),
        'private_type': random_private_type(),
    }
    twitter_feedback_private_mappings(twitter_feedback_private_index_name)
    print es.index(index=twitter_feedback_private_index_name, doc_type=twitter_feedback_private_index_type, body=data)


# 粉丝列表
def fans(date):
    user_name = random_user_name()
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'user_name': user_name,
        'profile_url': 'https://twitter.com/' + user_name,
        'update_time': random_update_time(date),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'root_user_name': root_user_name,
        'twitter_type': '好友',
    }
    twitter_feedback_fans_mappings()
    print es.index(index=twitter_feedback_fans_index_name, doc_type=twitter_feedback_fans_index_type, body=data)

# 关注列表
def follow(date):
    user_name = random_user_name()
    data = {
        'uid': random_uid(),
        'photo_url': random_photo_url(),
        'nick_name': random_nick_name(),
        'user_name': user_name,
        'profile_url': 'https://twitter.com/' + user_name,
        'update_time': random_update_time(date),
        'root_uid': root_uid,
        'root_nick_name': root_nick_name,
        'root_user_name': root_user_name,
        'twitter_type': '好友',
    }
    twitter_feedback_follow_mappings()
    print es.index(index=twitter_feedback_follow_index_name, doc_type=twitter_feedback_follow_index_type, body=data)


if __name__ == '__main__':
    #2017-10-15     2017-10-30
    for i in range(16, 31, 1):
        date = '2017-10-' + str(i)
        print 'date', date
        for i in range(random.randint(2,5)):
            like(date)
            retweet(date)
            at(date)
            comment(date)
            private(date)
            fans(date)
            follow(date)

