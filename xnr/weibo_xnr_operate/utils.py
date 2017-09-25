#-*- coding:utf-8 -*-
import os
import time
import json
import sys
import random
import base64
import re

#reload(sys)
#sys.path.append('../../')
from xnr.global_config import S_DATE,S_TYPE,S_DATE_BCI
from xnr.global_utils import es_xnr as es
from xnr.global_utils import weibo_hot_keyword_task_index_name,weibo_hot_keyword_task_index_type,\
                            weibo_xnr_timing_list_index_name,weibo_xnr_timing_list_index_type,\
                            weibo_xnr_index_name,weibo_xnr_index_type,es_flow_text,flow_text_index_name_pre,\
                            flow_text_index_type,es_user_profile,profile_index_name,profile_index_type,\
                            social_sensing_index_name,social_sensing_index_type,\
                            weibo_hot_content_recommend_results_index_name,\
                            weibo_hot_content_recommend_results_index_type,\
                            weibo_hot_subopinion_results_index_name,weibo_hot_subopinion_results_index_type,\
                            weibo_bci_index_name_pre,weibo_bci_index_type,portrait_index_name,portrait_index_type,\
                            es_user_portrait,es_user_profile
from xnr.global_utils import weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
                            weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
                            weibo_feedback_private_index_name,weibo_feedback_private_index_type,\
                            weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
                            weibo_feedback_like_index_name,weibo_feedback_like_index_type,\
                            weibo_feedback_fans_index_name,weibo_feedback_fans_index_type,\
                            weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
                            weibo_feedback_group_index_name,weibo_feedback_group_index_type,\
                            weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                            index_sensing,type_sensing,weibo_xnr_retweet_timing_list_index_name,\
                            weibo_domain_index_name,weibo_domain_index_type,weibo_xnr_retweet_timing_list_index_type,weibo_private_white_uid_index_name,\
                            weibo_private_white_uid_index_type

from xnr.time_utils import ts2datetime,datetime2ts,get_flow_text_index_list
from xnr.weibo_publish_func import publish_tweet_func,retweet_tweet_func,comment_tweet_func,private_tweet_func,\
                                like_tweet_func,follow_tweet_func,unfollow_tweet_func,create_group_func,\
                                reply_tweet_func #,at_tweet_func
from xnr.parameter import DAILY_INTEREST_TOP_USER,DAILY_AT_RECOMMEND_USER_TOP,TOP_WEIBOS_LIMIT,\
                        HOT_AT_RECOMMEND_USER_TOP,HOT_EVENT_TOP_USER,BCI_USER_NUMBER,USER_POETRAIT_NUMBER,\
                        MAX_SEARCH_SIZE,domain_ch2en_dict,topic_en2ch_dict,topic_ch2en_dict,FRIEND_LIST,\
                        FOLLOWERS_LIST,IMAGE_PATH,WHITE_UID_PATH,WHITE_UID_FILE_NAME
from save_to_weibo_xnr_flow_text import save_to_xnr_flow_text
from xnr.utils import uid2nick_name_photo,xnr_user_no2uid,judge_follow_type,judge_sensing_sensor,\
                        get_influence_relative

def get_show_domain():
    domain_name_dict = {}
    query_body = {'query':{'match_all':{}},'size':MAX_SEARCH_SIZE}
    es_results = es.search(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,body=query_body)['hits']['hits']
    if es_results:
        for result in es_results:
            result = result['_source']
            domain_name_dict[result['domain_pinyin']] = result['domain_name']
    return domain_name_dict

def get_image_path(image_code):

    image_code_list = image_code.encode('utf-8').split('，')
    image_path_list = []
    for image in image_code_list:
        image_new = image.replace(' ','+')
        #print 'image_new:::::',image_new
        print 'image_new::::',image_new
        print '123123'
        imgData = base64.decodestring(image_new)
        #imgData = base64.b64encode(image_new)
        time_name = time.strftime('%Y%m%d%H%M%S')
        image_path = time_name + '_%d' % random.randint(0,100)
        leniyimg = open(IMAGE_PATH+image_path+'.jpg','wb')   
        leniyimg.write(imgData)
        leniyimg.close()

        image_path_join = os.path.join(IMAGE_PATH,image_path+'.jpg')
        print 'image_path_join:::',image_path_join
        image_path_list.append(image_path_join)
    
    return image_path_list


def push_keywords_task(task_detail):

    print 'task_detail::',task_detail

    try:
        task_id = task_detail['task_id']
        xnr_user_no = task_detail['xnr_user_no']
        keywords_string = '&'.join(task_detail['keywords_string'].encode('utf-8').split('，'))
        task_detail['keywords_string'] = keywords_string
        _id = xnr_user_no+'_'+task_id
        es.index(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                id=_id,body=task_detail)
        mark = True
    except:
        mark = False

    return mark

def get_submit_tweet(task_detail):
    print 'task_detail[p_url]:::',task_detail['p_url']
    text = task_detail['text']
    tweet_type = task_detail['tweet_type']
    #operate_type = task_detail['operate_type']
    xnr_user_no = task_detail['xnr_user_no']
    p_url = task_detail['p_url'].encode('utf-8')
    rank = task_detail['rank']
    rankid = task_detail['rankid']

    es_xnr_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    
    weibo_mail_account = es_xnr_result['weibo_mail_account']
    weibo_phone_account = es_xnr_result['weibo_phone_account']
    password = es_xnr_result['password']
    
    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    # 发布微博

    mark = publish_tweet_func(account_name,password,text,p_url,rank,rankid)
    #execute(account_name,password,text.encode('utf-8'))

    # 保存微博
    try:
        save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark

def save_to_tweet_timing_list(task_detail):

    item_detail = dict()

    #item_detail['uid'] = task_detail['uid']
    item_detail['xnr_user_no'] = task_detail['xnr_user_no']
    item_detail['task_source'] = task_detail['task_source']
    #item_detail['operate_type'] = task_detail['operate_type']
    item_detail['create_time'] = task_detail['create_time']
    item_detail['post_time'] = task_detail['post_time']
    item_detail['text'] = task_detail['text']
    item_detail['task_status'] = task_detail['task_status'] # 0-尚未发送，1-已发送
    item_detail['remark'] = task_detail['remark']
    #item_detail['task_status'] = 0 

    task_id = task_detail['xnr_user_no'] + '_'+str(item_detail['create_time'])+'_'+ str(task_detail['post_time'])
    # task_id: uid_提交时间_发帖时间

    try:
        es.index(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id,body=item_detail)
        mark = True
    except:
        mark = False

    return mark

## 日常发帖@用户推荐

def get_recommend_at_user(xnr_user_no):
    #_id  = user_no2_id(user_no)
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    print 'es_result:::',es_result
    if es_result:
        uid = es_result['uid']
        daily_interests = es_result['daily_interests']
    if S_TYPE == 'test':
        now_ts = datetime2ts(S_DATE)    
    else:
        now_ts = int(time.time())
    datetime = ts2datetime(now_ts-24*3600)

    index_name = flow_text_index_name_pre + datetime
    nest_query_list = []
    daily_interests_list = daily_interests.split('&')
    '''
    ## daily_interests 字段为多个值
    for interest in daily_interests_list:
        nest_query_list.append({'wildcard':{'daily_interests':'*'+interest+'*'}})


    es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
                        body={'query':{'bool':{'must':nest_query_list}},'size':DAILY_INTEREST_TOP_USER,\
                        'sort':{'user_fansnum':{'order':'desc'}}})['hits']['hits']
    '''
    ## daily_interests 字段为单个值
    # query_body = {
    #     'query':{
    #         'filtered':{
    #             'filter':{
    #                 'terms':{'daily_interests':daily_interests_list}
    #             }
    #         }
    #     },
    #     'size':MAX_SEARCH_SIZE
    # }
    # #print '!!!!!!!!!!!!!!!!!!!!!!!!:::'
    # es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
    #                     body=query_body)['hits']['hits']

    #print 'es_results_len::',len(es_results)
    #if not es_results:
    if S_TYPE != 'test':
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'terms':{'daily_interests':daily_interests_list}
                    }
                }
            },
            'size':MAX_SEARCH_SIZE
        }
        #print '!!!!!!!!!!!!!!!!!!!!!!!!:::'
        es_results_daily = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
                            body=query_body)['hits']['hits']
        # es_results_daily = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
        #                     body={'query':{'match_all':{}},'size':DAILY_INTEREST_TOP_USER,\
        #                     'sort':{'user_fansnum':{'order':'desc'}}})['hits']['hits']
    else:

        es_results_daily = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
                            body={'query':{'match_all':{}},'size':1000,\
                            'sort':{'user_fansnum':{'order':'desc'}}})['hits']['hits']

    uid_list = []
    if es_results_daily:
        for result in es_results_daily:
            result = result['_source']
            uid_list.append(result['uid'])

    ## 根据uid，从weibo_user中得到 nick_name
    uid_nick_name_dict = dict()  # uid不会变，而nick_name可能会变
    es_results_user = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':uid_list})['docs']
    i = 0
    for result in es_results_user:

        if result['found'] == True:
            result = result['_source']
            uid = result['uid']
            nick_name = result['nick_name']
            if nick_name:
                i += 1
                uid_nick_name_dict[uid] = nick_name
        if i >= DAILY_AT_RECOMMEND_USER_TOP:
            break

    return uid_nick_name_dict

def get_daily_recommend_tweets(theme,sort_item):
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'daily_interests':theme}
                }
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':TOP_WEIBOS_LIMIT
    }

    if S_TYPE == 'test':
        now_ts = datetime2ts(S_DATE)    
    else:
        now_ts = int(time.time())
    datetime = ts2datetime(now_ts-24*3600)

    index_name = flow_text_index_name_pre + datetime

    es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

    if not es_results:
        es_results_recommend = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
                                body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
                                'sort':{sort_item:{'order':'desc'}}})['hits']['hits']
    results_all = []
    for result in es_results_recommend:
        result = result['_source']
        uid = result['uid']
        nick_name,photo_url = uid2nick_name_photo(uid)
        result['nick_name'] = nick_name
        result['photo_url'] = photo_url
        results_all.append(result)
    return results_all

def get_hot_sensitive_recommend_at_user(sort_item):

    if S_TYPE == 'test':
        now_ts = datetime2ts(S_DATE)    
    else:
        now_ts = int(time.time())
    datetime = ts2datetime(now_ts-24*3600)

    index_name = flow_text_index_name_pre + datetime

    query_body = {
        'query':{
            'match_all':{}
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':HOT_EVENT_TOP_USER,
        '_source':['uid','user_fansnum','retweeted','timestamp']
    }

    if sort_item == 'retweeted':
        sort_item_2 = 'timestamp'
    else:
        sort_item_2 = 'retweeted'

    es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    
    uid_fansnum_dict = dict()
    if es_results:
        for result in es_results:
            result = result['_source']
            uid = result['uid']
            uid_fansnum_dict[uid] = {}
            uid_fansnum_dict[uid][sort_item_2] = result[sort_item_2]

    uid_fansnum_dict_sort_top = sorted(uid_fansnum_dict.items(),key=lambda x:x[1][sort_item_2],reverse=True)

    uid_set = set()

    for item in uid_fansnum_dict_sort_top:
        uid_set.add(item[0])

    uid_list = list(uid_set)


    ## 根据uid，从weibo_user中得到 nick_name
    uid_nick_name_dict = dict()  # uid不会变，而nick_name可能会变
    es_results_user = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':uid_list})['docs']
    i = 0
    for result in es_results_user:
        if result['found'] == True:
            result = result['_source']
            uid = result['uid']
            nick_name = result['nick_name']
            if nick_name:
                i += 1
                uid_nick_name_dict[uid] = nick_name
        if i >= HOT_AT_RECOMMEND_USER_TOP:
            break

    return uid_nick_name_dict

def get_hot_recommend_tweets(xnr_user_no,topic_field,sort_item):
    
    topic_field_en = topic_ch2en_dict[topic_field]
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {
                        'filtered':{
                            'filter':{
                                'term':{'topic_field':topic_field_en}
                            }
                        }
                    },
                     {
                        'filtered':{
                            'filter':{
                                'term':{'xnr_user_no':xnr_user_no}
                            }
                        }
                    }
                ]
            }
            
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':TOP_WEIBOS_LIMIT
    }


    es_results = es.search(index=social_sensing_index_name,doc_type=social_sensing_index_type,body=query_body)['hits']['hits']
    if not es_results:    
        es_results = es.search(index=social_sensing_index_name,doc_type=social_sensing_index_type,\
                                body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
                                'sort':{sort_item:{'order':'desc'}}})['hits']['hits']
    results_all = []
    for result in es_results:
        result = result['_source']
        uid = result['uid']
        nick_name,photo_url = uid2nick_name_photo(uid)
        result['nick_name'] = nick_name
        result['photo_url'] = photo_url
        results_all.append(result)
    return results_all

def get_hot_content_recommend(xnr_user_no,task_id):
    task_id_new = xnr_user_no+'_'+task_id
    es_task = es.get(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id_new)['_source']
    if es_task:
        if es_task['compute_status'] == 0:
            return '尚未计算'
        else:
            es_result = es.get(index=weibo_hot_content_recommend_results_index_name,doc_type=weibo_hot_content_recommend_results_index_type,\
                            id=task_id_new)['_source']

            if es_result:
                contents = json.loads(es_result['content_recommend'])

            return contents

def get_hot_subopinion(xnr_user_no,task_id):
    
    task_id_new = xnr_user_no+'_'+task_id
    es_task = []
    try:
        es_task = es.get(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id_new)['_source']
    except:
        return '尚未提交计算'

    if es_task:
        if es_task['compute_status'] != 2:
            return '正在计算'
        else:
            es_result = es.get(index=weibo_hot_subopinion_results_index_name,doc_type=weibo_hot_subopinion_results_index_type,\
                                id=task_id_new)['_source']

            if es_result:
                contents = json.loads(es_result['subopinion_weibo'])
            
                return contents

def get_tweets_from_flow(sort_item_new):

    query_body = {
        'query':{
            'match_all':{}
        },
        'sort':{sort_item_new:{'order':'desc'}},
        'size':TOP_WEIBOS_LIMIT
    }

    if S_TYPE == 'test':
        now_ts = datetime2ts(S_DATE)    
    else:
        now_ts = int(time.time())
    datetime = ts2datetime(now_ts-24*3600)

    index_name = flow_text_index_name_pre + datetime

    es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

    if not es_results:
        es_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
                                body={'query':{'match_all':{}},'size':TOP_WEIBOS_LIMIT,\
                                'sort':{sort_item:{'order':'desc'}}})['hits']['hits']
    results_all = []
    for result in es_results:
        result = result['_source']
        uid = result['uid']
        nick_name,photo_url = uid2nick_name_photo(uid)
        result['nick_name'] = nick_name
        result['photo_url'] = photo_url
        results_all.append(result)
    return results_all

def uid_lists2weibo_from_flow_text(uid_list):

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':uid_list}
                }
            }
        },
        'size':TOP_WEIBOS_LIMIT
    }

    if S_TYPE == 'test':
        now_ts = datetime2ts(S_DATE)    
    else:
        now_ts = int(time.time())
    datetime = ts2datetime(now_ts-24*3600)

    index_name_flow = flow_text_index_name_pre + datetime

    es_results = es_flow_text.search(index=index_name_flow,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

    results_all = []
    for result in es_results:
        result = result['_source']
        uid = result['uid']
        nick_name,photo_url = uid2nick_name_photo(uid)
        result['nick_name'] = nick_name
        result['photo_url'] = photo_url
        results_all.append(result)
    return results_all

def get_tweets_from_bci(sort_item_new):

    if S_TYPE == 'test':
        now_ts = datetime2ts(S_DATE_BCI)    
    else:
        now_ts = int(time.time())

    datetime = ts2datetime(now_ts-24*3600)
    datetime_new = datetime[0:4]+datetime[5:7]+datetime[8:10]

    index_name = weibo_bci_index_name_pre + datetime_new

    query_body = {
        'query':{
            'match_all':{}
        },
        'sort':{sort_item_new:{'order':'desc'}},
        'size':BCI_USER_NUMBER
    }

    es_results_bci = es_user_portrait.search(index=index_name,doc_type=weibo_bci_index_type,body=query_body)['hits']['hits']
    #print 'es_results_bci::',es_results_bci
    print 'index_name::',index_name
    #print ''
    uid_set = set()

    if es_results_bci:
        for result in es_results_bci:
            uid = result['_id']
            uid_set.add(uid)
    uid_list = list(uid_set)

    es_results = uid_lists2weibo_from_flow_text(uid_list)

    return es_results

def get_tweets_from_user_portrait(sort_item_new):

    query_body = {
        'query':{
            'match_all':{}
        },
        'sort':{sort_item_new:{'order':'desc'}},
        'size':USER_POETRAIT_NUMBER
    }

    es_results_portrait = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,body=query_body)['hits']['hits']

    uid_set = set()

    if es_results_portrait:
        for result in es_results_portrait:
            result = result['_source']
            uid = result['uid']
            uid_set.add(uid)
    uid_list = list(uid_set)

    es_results = uid_lists2weibo_from_flow_text(uid_list)
    
    return es_results

def get_bussiness_recomment_tweets(sort_item):
    print 'sort_item::',sort_item
    #sort_item_new = ''
    if sort_item == 'timestamp':
        sort_item_new = 'timestamp'
        es_results = get_tweets_from_flow(sort_item_new)
    elif sort_item == 'sensitive_info':
        sort_item_new = 'sensitive'
        es_results = get_tweets_from_flow(sort_item_new)
    elif sort_item == 'sensitive_user':
        sort_item_new = 'user_index'
        es_results = get_tweets_from_bci(sort_item_new)
    elif sort_item == 'influence_info':
        sort_item_new = 'retweeted'
        es_results = get_tweets_from_flow(sort_item_new)
    elif sort_item == 'influence_user':
        sort_item_new = 'influence'
        es_results = get_tweets_from_user_portrait(sort_item_new)

    return es_results

'''
社交反馈
'''

def get_reply_total(task_detail):

    text = task_detail['text']
    tweet_type = task_detail['tweet_type']
    xnr_user_no = task_detail['xnr_user_no']
    r_mid = task_detail['r_mid']
    mid = task_detail['mid']
    uid = task_detail['uid']
    retweet_option = task_detail['retweet_option']


    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']

    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    # 发布微博

    mark_reply = reply_tweet_func(account_name,password,text,r_mid,mid,uid)

    mark_retweet = ['','']

    if retweet_option == 'true':

        mark_retweet = retweet_tweet_func(account_name,password,text,r_mid)

    # 保存微博
    try:
        save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark_reply,mark_retweet


def get_show_comment(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'comment_type':'receive'}}
                ]
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    es_results = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
                            body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            results_all.append(item['_source'])

    return results_all


def get_reply_comment(task_detail):

    text = task_detail['text']
    tweet_type = task_detail['tweet_type']
    xnr_user_no = task_detail['xnr_user_no']
    r_mid = task_detail['r_mid']

    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']

    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    # 发布微博

    mark = comment_tweet_func(account_name,password,text,r_mid)

    # 保存微博
    try:
        save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark

def get_show_retweet(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'root_uid':uid}
                }
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    es_results = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
                            body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            results_all.append(item['_source'])

    return results_all

def get_reply_retweet(task_detail):
    text = task_detail['text']
    tweet_type = task_detail['tweet_type']
    xnr_user_no = task_detail['xnr_user_no']
    r_mid = task_detail['r_mid']

    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']
    
    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    mark = retweet_tweet_func(account_name,password,text,r_mid)

    # 保存微博
    try:
        save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark

def get_show_private(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']
    # white_uid_path = WHITE_UID_PATH + WHITE_UID_FILE_NAME
    # white_uid_list = []
    # with open(white_uid_path,'rb') as f:
    # 	for line in f:
    # 		line = line.strip('\n')
    # 		white_uid_list.append(line[0])

    # white_uid_list = list(set(white_uid_list))
    # print 'white_uid_list:::',white_uid_list
    try:
    	es_get = es.get(index=weibo_private_white_uid_index_name,doc_type=weibo_private_white_uid_index_type,\
    				id=xnr_user_no)['_source']
    	white_uid_list = es_get['white_uid_list']
    	
    except:
    	white_uid_list = []

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'private_type':'receive'}}
                ],
                'must_not':{'terms':{'uid':white_uid_list}}
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    es_results = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
                            body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            results_all.append(item['_source'])

    return results_all

def get_reply_private(task_detail):
    text = task_detail['text']
    xnr_user_no = task_detail['xnr_user_no']
    r_mid = task_detail['uid']

    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']
    
    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    mark = private_tweet_func(account_name,password,text,r_mid)

    return mark

def get_show_at(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'root_uid':uid}
                }
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }
    	
    es_results = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
                            body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            results_all.append(item['_source'])

    return results_all

def get_reply_at(task_detail):
    text = task_detail['text']
    xnr_user_no = task_detail['xnr_user_no']
    mid = task_detail['mid']
    r_mid = task_detail['r_mid']
    uid = task_detail['uid']

    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']
    

    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    # 发布微博

    mark = reply_tweet_func(account_name,password,text,r_mid,mid,uid)

    # 保存微博
    try:
        save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
    except:
        print '保存微博过程遇到错误！'
        save_mark = False

    return mark

def get_show_fans(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'root_uid':uid}
                }
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    es_results = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
                            body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            results_all.append(item['_source'])

    return results_all


def get_show_follow(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'root_uid':uid}
                }
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    es_results = es.search(index=weibo_feedback_follow_index_name,doc_type=weibo_feedback_follow_index_type,\
                            body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            results_all.append(item['_source'])

    return results_all

def get_reply_follow(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    uid = task_detail['uid']
    trace_type = task_detail['trace_type']
    
    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']
    
    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    mark = follow_tweet_func(xnr_user_no,account_name,password,uid,trace_type)

    return mark


def get_reply_unfollow(task_detail):

    xnr_user_no = task_detail['xnr_user_no']
    uid = task_detail['uid']

    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']
    
    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    mark = unfollow_tweet_func(xnr_user_no,account_name,password,uid)

    return mark


def get_like_operate(task_detail):

    xnr_user_no = task_detail['xnr_user_no']
    r_mid = task_detail['mid']

    es_get_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    weibo_mail_account = es_get_result['weibo_mail_account']
    weibo_phone_account = es_get_result['weibo_phone_account']
    password = es_get_result['password']
      
    if weibo_mail_account:
        account_name = weibo_mail_account
    elif weibo_phone_account:
        account_name = weibo_phone_account
    else:
        return False

    mark = like_tweet_func(account_name,password,r_mid)

    return mark


# 主动社交-直接搜索
def get_direct_search(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']  
    uid_list = task_detail['uid_list']

    if sort_item != 'friend':
        uid_list_new = uid_list
        
    else:
        if S_TYPE == 'test':
            uid_list_new = FRIEND_LIST 
            sort_item = 'sensitive'  
        else:       
            friends_list = []
            ## 得到朋友圈uid_list
            #for uid in uid_list:
            friends_list_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':uid_list})['_source']
            for result in friends_list_results:
                friends_list = friends_list + result['friend_list']
            friends_set_list = list(set(friends_list))

            uid_list_new = friends_set_list

            sort_item = 'fansnum'

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':uid_list_new}
                }
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }

    print 'uid_list_new::',uid_list_new
    es_results = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            uid = item['_source']['uid']

            weibo_type = judge_follow_type(xnr_user_no,uid)
            sensor_mark = judge_sensing_sensor(xnr_user_no,uid)

            item['_source']['weibo_type'] = weibo_type
            item['_source']['sensor_mark'] = sensor_mark
            
            influence = item['_source']['influence']
            influence_relative = get_influence_relative(uid,influence)
            item['_source']['influence'] = influence_relative
            
            if S_TYPE == 'test':
                current_time = datetime2ts(S_DATE)
            else:
                current_time = int(time.time())

            index_name = get_flow_text_index_list(current_time)

            query_body = {
                'query':{
                    'term':{'uid':uid}
                },
                'sort':{'retweeted':{'order':'desc'}}
            }

            es_weibo_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

            weibo_list = []
            for weibo in es_weibo_results:
                weibo = weibo['_source']
                weibo_list.append(weibo)
            item['_source']['weibo_list'] = weibo_list

            results_all.append(item['_source'])

    return results_all


## 主动社交- 相关推荐
def get_related_recommendation(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    sort_item = task_detail['sort_item']
    es_result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']

    if S_TYPE == 'test':
        recommend_set_list = FOLLOWERS_LIST
    
    else:
        recommend_list = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=uid)['_source']['followers_list']
        recommend_set_list = list(set(recommend_list))

    if sort_item != 'friend':
        uid_list = recommend_set_list

    else:
        if S_TYPE == 'test':
            uid_list = FRIEND_LIST
            sort_item = 'sensitive'
        else:
            friends_list_results = es_user_portrait.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':recommend_set_list})['_source']
            for result in friends_list_results:
                friends_list = friends_list + result['friend_list']
            friends_set_list = list(set(friends_list))

            uid_list = friends_set_list

            sort_item = 'fansnum'

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':uid_list}
                }
            }
        },
        'sort':{sort_item:{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }
    es_results = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,body=query_body)['hits']['hits']

    results_all = []
    if es_results:
        for item in es_results:
            uid = item['_source']['uid']
            weibo_type = judge_follow_type(xnr_user_no,uid)
            sensor_mark = judge_sensing_sensor(xnr_user_no,uid)

            item['_source']['weibo_type'] = weibo_type
            item['_source']['sensor_mark'] = sensor_mark

            influence = item['_source']['influence']
            influence_relative = get_influence_relative(uid,influence)
            item['_source']['influence'] = influence_relative

            if S_TYPE == 'test':
                current_time = datetime2ts(S_DATE)
            else:
                current_time = int(time.time())

            index_name = get_flow_text_index_list(current_time)

            query_body = {
                'query':{
                    'term':{'uid':uid}
                },
                'sort':{'retweeted':{'order':'desc'}}
            }

            es_weibo_results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

            weibo_list = []
            for weibo in es_weibo_results:
                weibo = weibo['_source']
                weibo_list.append(weibo)
            item['_source']['weibo_list'] = weibo_list
            results_all.append(item['_source'])

    return results_all


## 创建群组
def get_create_group(task_detail):

    xnr_user_no = task_detail['xnr_user_no']
    group = task_detail['group']
    members = task_detail['members']
     
    result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    weibo_mail_account = result['weibo_mail_account']
    weibo_phone_account = result['weibo_phone_account']
    password = result['password']

    if weibo_mail_account:
        account_name = weibo_mail_account
    else:
        account_name = weibo_phone_account

    mark = create_group_func(account_name,password,group,members)

    return mark

def get_show_group(xnr_user_no):
    uid = xnr_user_no2uid(xnr_user_no)
    print 'uid::',uid
    query_body = {
        'query':{
            'term':{'uid':uid}
        },
        'size':MAX_SEARCH_SIZE
    }
    print 'weibo_feedback_group_index_name::',weibo_feedback_group_index_name
    print 'weibo_feedback_group_index_type::',weibo_feedback_group_index_type

    es_results = es.search(index=weibo_feedback_group_index_name,doc_type=weibo_feedback_group_index_type,body=query_body)['hits']['hits']
    print 'es_results:::',es_results
    group_dict = {}
    if es_results:
        for result in es_results:
            print 'result_keys::',result.keys()
            gid = result['_source']['gid']
            gname = result['_source']['gname']
            group_dict[gid] = gname

    return group_dict

## 展示粉丝
def get_create_group_show_fans(xnr_user_no):
    uid = xnr_user_no2uid(xnr_user_no)
    print 'xnr_user_no:::',xnr_user_no
    es_result = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
            id=xnr_user_no)['_source']

    fans_list = es_result['fans_list']

    results_all = {}

    for fans_uid in fans_list:
        nick_name,photo_url = uid2nick_name_photo(fans_uid)
        results_all[fans_uid] = [nick_name,photo_url]

    return results_all


def get_add_sensor_user(xnr_user_no,sensor_uid_list):

    mark = False
    sensor_uid_list_new = sensor_uid_list.split("，")

    exists_result = es.exists(index=index_sensing,doc_type=type_sensing,id=xnr_user_no)

    if exists_result:
        item_results = es.get(index=index_sensing,doc_type=type_sensing,id=xnr_user_no)['_source']
        social_sensors = item_results['social_sensors']
        social_sensors.extend(sensor_uid_list_new)
        social_sensors = list(set(social_sensors))
        item_results['social_sensors'] = social_sensors

        es.update(index=index_sensing,doc_type=type_sensing,id=xnr_user_no,body={'doc':item_results})

        mark = True

    else:
        item = {}
        item['xnr_user_no'] = xnr_user_no
        item['social_sensors'] = sensor_uid_list_new
        item['task_name'] = '感知'+xnr_user_no+'热门事件'
        item['history_status'] = ''
        item['remark'] = ''
        es.index(index=index_sensing,doc_type=type_sensing,id=xnr_user_no,body=item_results)

        mark = True

    return mark


def get_delete_sensor_user(xnr_user_no,sensor_uid_list):

    mark = False
    sensor_uid_list_new = sensor_uid_list.split("，")
    try:
        item_results = es.get(index=index_sensing,doc_type=type_sensing,id=xnr_user_no)['_source']
        social_sensors = item_results['social_sensors']

        social_sensors = list(set(social_sensors).difference(set(sensor_uid_list_new)))
        item_results['social_sensors'] = social_sensors

        es.update(index=index_sensing,doc_type=type_sensing,id=xnr_user_no,body={'doc':item_results})

        mark = True
    except:
        return mark

    return mark

def get_trace_follow_operate(xnr_user_no,uid_string,nick_name_string):

    mark = False
    fail_nick_name_list = []
    if uid_string:
        uid_list = uid_string.encode('utf-8').split('，')
        
    elif nick_name_string:
        nick_name_list = nick_name_string.encode('utf-8').split('，')
        uid_list = []
        
        for nick_name in nick_name_list:
            query_body = {
                'query':{
                    'filtered':{
                        'filter':{
                            'term':{'nick_name':nick_name}
                        }
                    }
                },
                '_source':['uid']
            }
            try:
                uid_results = es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,\
                            body=query_body)['hits']['hits']
                
                uid_result = uid_result[0]['_source']
                uid = uid_result['uid']
                uid_list.append(uid)

            except:
                fail_nick_name_list.append(nick_name)

    try:
        result = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                        id=xnr_user_no)['_source']

        try:
            trace_follow_list = result['trace_follow_list']
        except:
            trace_follow_list = []

        try:
            followers_list = result['followers_list']
        except:
            followers_list = []

        trace_follow_list = list(set(trace_follow_list) | set(uid_list))

        followers_list = list(set(followers_list)|set(uid_list))

        es.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no,body={'doc':{'trace_follow_list':trace_follow_list,'followers_list':followers_list}})

        mark = True
    
    except:

        item_exists = {}

        item_exists['xnr_user_no'] = xnr_user_no
        item_exists['trace_follow_list'] = uid_list
        item_exists['followers_list'] = uid_list

        es.index(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no,body=item_exists)

        mark = True

    return [mark,fail_nick_name_list]

def get_un_trace_follow_operate(xnr_user_no,uid_string,nick_name_string):

    mark = False
    fail_nick_name_list = []
    fail_uids = []

    if uid_string:
        uid_list = uid_string.encode('utf-8').split('，')
        
    elif nick_name_string:
        nick_name_list = nick_name_string.encode('utf-8').split('，')
        uid_list = []
        
        for nick_name in nick_name_list:
            query_body = {
                'query':{
                    'filtered':{
                        'filter':{
                            'term':{'nick_name':nick_name}
                        }
                    }
                },
                '_source':['uid']
            }
            try:
                uid_results = es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,\
                            body=query_body)['hits']['hits']
                
                uid_result = uid_result[0]['_source']
                uid = uid_result['uid']
                uid_list.append(uid)

            except:
                fail_nick_name_list.append(nick_name)

    try:
        result = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                            id=xnr_user_no)['_source']
        
        trace_follow_list = result['trace_follow_list']

        # 共同uids
        comment_uids = list(set(trace_follow_list).intersection(set(uid_list)))

        # 取消失败uid
        fail_uids = list(set(comment_uids).difference(set(uid_list)))

        # 求差
        trace_follow_list = list(set(trace_follow_list).difference(set(uid_list))) 


        es.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                            id=xnr_user_no,body={'doc':{'trace_follow_list':trace_follow_list}})

        mark = True
    except:
        mark = False

    return [mark,fail_uids,fail_nick_name_list]

def get_show_retweet_timing_list(xnr_user_no):

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_user_no':xnr_user_no}
                }
            }
        },
        'size':MAX_SEARCH_SIZE,
        'sort':[
            {'compute_status':{'order':'asc'}},   
            {'timestamp_set':{'order':'desc'}}
        ]
    }

    results = es.search(index=weibo_xnr_retweet_timing_list_index_name,\
        doc_type=weibo_xnr_retweet_timing_list_index_type,body=query_body)['hits']['hits']

    result_all = []

    for result in results:
        result = result['_source']
        result_all.append(result)

    return result_all


def get_show_trace_followers(xnr_user_no):
    
    es_get_result = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no)['_source']

    trace_follow_list = es_get_result['trace_follow_list']

    weibo_user_info = []

    # query_body = {
    #     'query':{
    #         'filtered':{
    #             'filter':{
    #                 'terms':{'uid':trace_follow_list}
    #             }
    #         }
    #     },
    #     'size':MAX_SEARCH_SIZE,
    #     'sort':{'fansnum':{'order':'desc'}}
    # }

    # results = es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,\
    #                 body=query_body)['hits']['hits']

    mget_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                            body={'ids':trace_follow_list})['docs']
    print 'mget_results::',mget_results
    for result in mget_results:
        if result['found']:
            weibo_user_info.append(result['_source'])

    return weibo_user_info

def get_add_private_white_uid(xnr_user_no,white_uid_string):

	white_uid_list = white_uid_string.encode('utf-8').split('，')
	mark = False

	try:
		get_result = es.get(index=weibo_private_white_uid_index_name,doc_type=weibo_private_white_uid_index_type,\
			id=xnr_user_no)['_source']

		white_uid_list_old = get_result['white_uid_list']
		white_uid_list_old.extend(white_uid_list)

		get_result['white_uid_list'] = white_uid_list_old

		es.update(index=weibo_private_white_uid_index_name,doc_type=weibo_private_white_uid_index_type,\
			body={'doc':get_result})

		mark = True
	
	except:
		item_dict = {}
		item_dict['xnr_user_no'] = xnr_user_no
		item_dict['white_uid_list'] = white_uid_list

		es.index(index=weibo_private_white_uid_index_name,doc_type=weibo_private_white_uid_index_type,\
			id=xnr_user_no,body=item_dict)
		
		mark = True

	return mark










