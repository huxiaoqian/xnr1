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

def save_retweet(xnr_info, date):
    index_name = facebook_feedback_retweet_index_name_pre + date
    facebook_feedback_retweet_mappings(index_name)
    share = Share(xnr_info['username'], xnr_info['password'])
    res = share.get_share()
    bulk_create_action = []
    if res:
        for r in res:
            data = r
            sensitive_user = get_sensitive_user(timestamp=datetime2ts(date), uid=data['uid'])
            sensitive_info = get_sensitive_info(timestamp=datetime2ts(date),mid=data['mid'],text=data['text'])
            facebook_type = u'陌生人'
            if uid in xnr_info['friends_list']:
                facebook_type = u'好友'
            data['root_uid'] = xnr_info['root_uid']
            data['root_nick_name'] = xnr_info['root_nick_name']
            data['facebook_type'] = facebook_type
            data['sensitive_user'] = sensitive_user
            data['sensitive_info'] = sensitive_info
            create_action = {'index':{'_id': data['mid']}}
            bulk_create_action.extend([create_action, data])
        result = es.bulk(bulk_create_action, index=index_name, doc_type=facebook_feedback_retweet_index_type)
        print 'result: ', result
        # if result['errors'] :
        #     print result
        #     return False
    return True

'''
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
'''
if __name__ == '__main__':
    date = ts2datetime(time.time())
    xnr_info = load_xnr_info(xnr_user_no)
    save_retweet(xnr_info, date)







