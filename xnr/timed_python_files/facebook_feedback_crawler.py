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
from global_utils import es_xnr as es
from global_utils import facebook_feedback_comment_index_name_pre,facebook_feedback_comment_index_type,\
                        facebook_feedback_retweet_index_name_pre,facebook_feedback_retweet_index_type,\
                        facebook_feedback_private_index_name_pre,facebook_feedback_private_index_type,\
                        facebook_feedback_at_index_name_pre,facebook_feedback_at_index_type,\
                        facebook_feedback_like_index_name_pre,facebook_feedback_like_index_type,\
                        facebook_feedback_friends_index_name_pre,facebook_feedback_friends_index_type,\
                        facebook_feedback_friends_index_name
from time_utils import ts2datetime
from facebook.feedback_like import Like
from facebook.feedback_share import Share
from facebook.feedback_mention import Mention
from facebook.feedback_comment import Comment
from facebook.feedback_message import Message
from facebook.feedback_friends import Friend


def save_like(username, password, date):
    index_name = facebook_feedback_like_index_name_pre + date
    facebook_feedback_like_mappings(index_name)
    like = Like(username, password)
    res = like.get_like()
    for r in res:
        facebook_type = u'陌生人'
        if r['facebook_type'] == u'好友':
            facebook_type = u'好友'
        data = {
            'update_time': time.time(), 
            'uid': r['uid'], 
            'sensitive_info': '', 
            'facebook_type': facebook_type, 
            'photo_url': r['photo_url'], 
            'timestamp': r['timestamp'], 
            'root_uid': r['id'], 
            'nick_name': r['nick_name'], 
            'mid': '', 
            'text': '', 
            'sensitive_user': '', 
            'root_mid': '',
        }
    print es.index(index=index_name, doc_type=facebook_feedback_like_index_type, body=data)

def save_retweet(username, password, date):
    index_name = facebook_feedback_retweet_index_name_pre + date
    facebook_feedback_retweet_mappings(index_name)
    share = Share(username, password)
    res = share.get_share()
    for r in res:
        facebook_type = u'陌生人'
        if r['facebook_type'] == u'好友':
            facebook_type = u'好友'
        data = {
        }
    print es.index(index=index_name, doc_type=facebook_feedback_retweet_index_type, body=data)

if __name__ == '__main__':
    username = ''
    password = ''
    date = ts2datetime(time.time())
    # save_like(username password, date)







