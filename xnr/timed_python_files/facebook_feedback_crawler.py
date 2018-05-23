# -*- coding: utf-8 -*-
import time
import sys
from facebook_feedback_mappings_timer import facebook_feedback_like_mappings,\
                                            facebook_feedback_retweet_mappings,\
                                            facebook_feedback_at_mappings,\
                                            facebook_feedback_comment_mappings,\
                                            facebook_feedback_private_mappings,\
                                            facebook_feedback_friends_mappings
sys.path.append('../')
from global_utils import es_xnr as es, fb_xnr_index_name, fb_xnr_index_type,\
                        fb_xnr_fans_followers_index_name, fb_xnr_fans_followers_index_type
from global_utils import facebook_feedback_comment_index_name_pre,facebook_feedback_comment_index_type,\
                        facebook_feedback_retweet_index_name_pre,facebook_feedback_retweet_index_type,\
                        facebook_feedback_private_index_name_pre,facebook_feedback_private_index_type,\
                        facebook_feedback_at_index_name_pre,facebook_feedback_at_index_type,\
                        facebook_feedback_like_index_name_pre,facebook_feedback_like_index_type,\
                        facebook_feedback_friends_index_name_pre,facebook_feedback_friends_index_type,\
                        facebook_feedback_friends_index_name
from time_utils import ts2datetime, datetime2ts
from facebook.feedback_like import Like
from facebook.feedback_share import Share
from facebook.feedback_mention import Mention
from facebook.feedback_comment import Comment
from facebook.feedback_message import Message
from facebook.feedback_friends import Friend

def load_xnr_info(xnr_user_no):
    friends_list = es.get(index=fb_xnr_fans_followers_index_name, doc_type=fb_xnr_fans_followers_index_type, id=xnr_user_no)['_source']['fans_list']
    res = es.get(index=fb_xnr_index_name, doc_type=fb_xnr_index_type, id=xnr_user_no)['_source']
    xnr_info = {
        'root_uid': res['uid'],
        'root_nick_name': res['nick_name'],
        'username': res['fb_phone_account'] or res['fb_mail_account'],
        'password': res['password'],
        'friends_list': friends_list,
    }
    return xnr_info

def save(index_name, doc_type, id, data):
    if es.exists(inde=index_name, doc_type=doc_type, id=id):
        es.update(inde=index_name, doc_type=doc_type, id=id, body={'doc': data})
    else:
        es.index(inde=index_name, doc_type=doc_type, id=id, body=data)

#按照互动发生的时间timestamp来存取数据，而不是爬取数据的时间updatetime
def save_retweet(xnr_info):
    share = Share(xnr_info['username'], xnr_info['password'])
    res = share.get_share()
    if res:
        for r in res:
            data = r
            timestamp = data['timestamp']
            mid = data['mid']
            #此处要去flow_text中匹配，故timestamp应是互动发生的时间
            sensitive_user = get_sensitive_user(timestamp=timestamp, uid=data['uid'])
            sensitive_info = get_sensitive_info(timestamp=timestamp,mid=mid,text=data['text'])
            facebook_type = u'陌生人'
            if uid in xnr_info['friends_list']:
                facebook_type = u'好友'
            data['root_uid'] = xnr_info['root_uid']
            data['root_nick_name'] = xnr_info['root_nick_name']
            data['facebook_type'] = facebook_type
            data['sensitive_user'] = sensitive_user
            data['sensitive_info'] = sensitive_info

            index_name = facebook_feedback_retweet_index_name_pre + ts2datetime(timestamp)
            facebook_feedback_retweet_mappings(index_name)
            save(index_name, facebook_feedback_retweet_index_type, mid, data)
    return True

#按照互动发生的时间timestamp来存取数据，而不是爬取数据的时间updatetime
def save_at(xnr_info):
    mention = Mention(xnr_info['username'], xnr_info['password'])
    res = mention.get_mention()
    if res:
        for r in res:
            data = r
            timestamp = data['timestamp']
            mid = data['mid']
            #此处要去flow_text中匹配，故timestamp应是互动发生的时间
            sensitive_user = get_sensitive_user(timestamp=timestamp, uid=data['uid'])
            sensitive_info = get_sensitive_info(timestamp=timestamp,mid=mid,text=data['text'])
            facebook_type = u'陌生人'
            if uid in xnr_info['friends_list']:
                facebook_type = u'好友'
            data['root_uid'] = xnr_info['root_uid']
            data['root_nick_name'] = xnr_info['root_nick_name']
            data['facebook_type'] = facebook_type
            data['sensitive_user'] = sensitive_user
            data['sensitive_info'] = sensitive_info

            index_name = facebook_feedback_at_index_name_pre + ts2datetime(timestamp)
            facebook_feedback_at_mappings(index_name)
            save(index_name, facebook_feedback_at_index_type, mid, data)
    return True

#按照互动发生的时间timestamp来存取数据，而不是爬取数据的时间updatetime
def save_comment(xnr_info):
    comment = Comment(xnr_info['username'], xnr_info['password'])
    res = comment.get_comment()
    if res:
        for r in res:
            data = r
            timestamp = data['timestamp']
            mid = data['mid']
            #此处要去flow_text中匹配，故timestamp应是互动发生的时间
            sensitive_user = get_sensitive_user(timestamp=timestamp, uid=data['uid'])
            sensitive_info = get_sensitive_info(timestamp=timestamp,mid=mid,text=data['text'])
            facebook_type = u'陌生人'
            if uid in xnr_info['friends_list']:
                facebook_type = u'好友'
            data['root_uid'] = xnr_info['root_uid']
            data['root_nick_name'] = xnr_info['root_nick_name']
            data['facebook_type'] = facebook_type
            data['sensitive_user'] = sensitive_user
            data['sensitive_info'] = sensitive_info

            index_name = facebook_feedback_comment_index_name_pre + ts2datetime(timestamp)
            facebook_feedback_comment_mappings(index_name)
            save(index_name, facebook_feedback_comment_index_type, mid, data)
    return True

#按照互动发生的时间timestamp来存取数据，而不是爬取数据的时间updatetime
def save_private(xnr_info):
    message = Message(xnr_info['username'], xnr_info['password'])
    res = message.get_message()
    if res:
        for r in res:
            data = r
            timestamp = data['timestamp']
            #此处要去flow_text中匹配，故timestamp应是互动发生的时间
            sensitive_user = get_sensitive_user(timestamp=timestamp, uid=data['uid'])
            sensitive_info = get_sensitive_info(timestamp=timestamp,text=data['text'])
            facebook_type = u'陌生人'
            if uid in xnr_info['friends_list']:
                facebook_type = u'好友'
            data['root_uid'] = xnr_info['root_uid']
            data['root_nick_name'] = xnr_info['root_nick_name']
            data['facebook_type'] = facebook_type
            data['sensitive_user'] = sensitive_user
            data['sensitive_info'] = sensitive_info

            index_name = facebook_feedback_private_index_name_pre + ts2datetime(timestamp)
            facebook_feedback_private_mappings(index_name)
            #如果当天的帖子中存在对应的记录（timestamp和text）,则pass，否则index
            query_body = {
                "query": {
                    "filtered":{
                        "filter": {
                            "bool": {
                                "must": [
                                    {"term": {"timestamp": timestamp}},
                                    {"term": {"text": data['text']}},
                                ]
                            }
                        }
                    }
                },
            }
            results = es.search(index=index_name, doc_type=facebook_feedback_private_index_type, body=query_body)['hits']['hits']
            if results:
                pass
            else:
                es.index(inde=index_name, doc_type=facebook_feedback_private_index_type, body=data)
    return True

#按照互动发生的时间timestamp来存取数据，而不是爬取数据的时间updatetime
def save_friends(xnr_info):
    friend = Friend(xnr_info['username'], xnr_info['password'])
    res = friend.get_friend()
    if res:
        for r in res:
            data = r
            facebook_type = u'陌生人'
            # if uid in xnr_info['friends_list']:
            #     facebook_type = u'好友'
            data['root_uid'] = xnr_info['root_uid']
            data['root_nick_name'] = xnr_info['root_nick_name']
            data['facebook_type'] = facebook_type

            index_name = facebook_feedback_friends_index_name
            facebook_feedback_friends_mappings(index_name)
            query_body = {
                "query": {
                    "filtered":{
                        "filter": {
                            "bool": {
                                "must": [
                                    {"term": {"uid": data['uid']}},
                                ]
                            }
                        }
                    }
                },
            }
            results = es.search(index=index_name, doc_type=facebook_feedback_friends_index_type, body=query_body)['hits']['hits']
            if results:
                es.update(inde=index_name, doc_type=facebook_feedback_friends_index_type, body={'doc': data})
            else:
                es.index(inde=index_name, doc_type=facebook_feedback_friends_index_type, body=data)
    return True

if __name__ == '__main__':
    xnr_info = load_xnr_info(xnr_user_no)
    save_retweet(xnr_info)
    save_at(xnr_info)
    save_comment(xnr_info)
    save_private(xnr_info)
    save_friends(xnr_info)


