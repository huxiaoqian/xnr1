# -*-coding:utf-8-*-

import json
import time
from collections import Counter
import random
from xnr.global_utils import es_xnr as es
from xnr.global_utils import R_WEIBO_XNR_FANS_FOLLOWERS as r_fans_followers 
from xnr.global_utils import es_flow_text,es_user_portrait,es_user_profile,weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
                        weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
                        weibo_feedback_private_index_name,weibo_feedback_private_index_type,\
                        weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
                        weibo_feedback_like_index_name,weibo_feedback_like_index_type,\
                        weibo_feedback_fans_index_name,weibo_feedback_fans_index_type,\
                        weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
                        weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                        flow_text_index_type,weibo_bci_index_name_pre,weibo_bci_index_type,\
                        flow_text_index_name_pre,weibo_report_management_index_name,weibo_report_management_index_type,\
                        portrait_index_name,portrait_index_type,xnr_flow_text_index_type,\
                        weibo_xnr_assessment_index_name,weibo_xnr_assessment_index_type,\
                        weibo_xnr_count_info_index_name,weibo_xnr_count_info_index_type,\
                        user_domain_index_name,user_domain_index_type,\
                        weibo_xnr_count_info_index_name,weibo_xnr_count_info_index_type
                        
from xnr.global_utils import r_fans_uid_list_datetime_pre,r_fans_count_datetime_xnr_pre,r_fans_search_xnr_pre,\
                r_followers_uid_list_datetime_pre,r_followers_count_datetime_xnr_pre,r_followers_search_xnr_pre

from xnr.utils import xnr_user_no2uid,uid2nick_name_photo
from xnr.global_config import S_TYPE,S_DATE,S_UID,S_DATE_BCI
from xnr.time_utils import ts2datetime,datetime2ts,get_flow_text_index_list,get_xnr_flow_text_index_list
from xnr.parameter import WEEK,DAY,MAX_SEARCH_SIZE,PORTRAIT_UID_LIST,PORTRAI_UID,FOLLOWERS_TODAY,\
                        TOP_ASSESSMENT_NUM,ACTIVE_UID,TOP_WEIBOS_LIMIT


def get_influence_total_trend(xnr_user_no):

    fans_dict = get_influ_fans_num(xnr_user_no)
    retweet_dict = get_influ_retweeted_num(xnr_user_no)
    comment_dict = get_influ_commented_num(xnr_user_no)
    like_dict = get_influ_like_num(xnr_user_no)
    at_dict = get_influ_at_num(xnr_user_no)
    private_dict = get_influ_private_num(xnr_user_no)

    total_dict = {}
    total_dict['total_trend'] = {}
    total_dict['day_num'] = {}
    total_dict['growth_rate'] = {}


    total_dict['total_trend']['fans'] = fans_dict['total_num']
    total_dict['total_trend']['retweet'] = retweet_dict['total_num']
    total_dict['total_trend']['comment'] = comment_dict['total_num']
    total_dict['total_trend']['like'] = like_dict['total_num']
    total_dict['total_trend']['at'] = at_dict['total_num']
    total_dict['total_trend']['private'] = private_dict['total_num']

    total_dict['day_num']['fans'] = fans_dict['day_num']
    total_dict['day_num']['retweet'] = retweet_dict['day_num']
    total_dict['day_num']['comment'] = comment_dict['day_num']
    total_dict['day_num']['like'] = like_dict['day_num']
    total_dict['day_num']['at'] = at_dict['day_num']
    total_dict['day_num']['private'] = private_dict['day_num']

    total_dict['growth_rate']['fans'] = fans_dict['growth_rate']
    total_dict['growth_rate']['retweet'] = retweet_dict['growth_rate']
    total_dict['growth_rate']['comment'] = comment_dict['growth_rate']
    total_dict['growth_rate']['like'] = like_dict['growth_rate']
    total_dict['growth_rate']['at'] = at_dict['growth_rate']
    total_dict['growth_rate']['private'] = private_dict['growth_rate']

    return total_dict

def compute_growth_rate_total(day8_dict,total8_dict):
    total_dict = {}
    total_dict['growth_rate'] = {}
    total_dict['day_num'] = {}
    total_dict['total_num'] = {}
    print 'day8_dict::',day8_dict
    print 'total8_dict:::',total8_dict
    for timestamp, num in day8_dict.iteritems():
        total_timestamp = timestamp - DAY
        day_num = day8_dict[timestamp]
        try:
            total_num_lastday = total8_dict[total_timestamp]
            print 'total_num_lastday:::',total_num_lastday
            if not total_num_lastday:
                total_num_lastday = 1
            total_dict['growth_rate'][timestamp] = round(float(day_num)/total_num_lastday,2)
            total_dict['day_num'][timestamp] = day8_dict[timestamp]
            total_dict['total_num'][timestamp] = total8_dict[timestamp]
        except:
            continue

    return total_dict

# 影响力粉丝数
def get_influ_fans_num(xnr_user_no):
    
    fans_num_day = {}  # 每天增量统计
    fans_num_total = {} # 截止到当天总量统计

    # if S_TYPE == 'test':
    #     current_time = datetime2ts(S_DATE)
    # else:
    #     current_time = int(time.time())
    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-7')
    else:
        current_time = int(time.time())
    
    current_time_new = datetime2ts(ts2datetime(current_time))

    for i in range(WEEK+1):
        timestamp = current_time_new - (i+1)*DAY  # DAY=3600*24
        datetime = ts2datetime(timestamp)
        r_fans_count = r_fans_count_datetime_xnr_pre + datetime + '_' + xnr_user_no
        r_fans_uid_list = r_fans_uid_list_datetime_pre + datetime

        datetime_count = r_fans_followers.get(r_fans_count)
        fans_uid_list = r_fans_followers.hget(r_fans_uid_list,xnr_user_no)

        if not datetime_count:
            datetime_count = 0

        if not fans_uid_list:
            datetime_total = 0
        else:
            datetime_total = len(json.loads(fans_uid_list))

        fans_num_day[timestamp] = datetime_count
        fans_num_total[timestamp] = datetime_total

    total_dict = compute_growth_rate_total(fans_num_day,fans_num_total)

    return total_dict
# def get_influ_fans_num(xnr_user_no):
    
#     fans_num_day = {}  # 每天增量统计
#     fans_num_total = {} # 截止到当天总量统计

#     uid = xnr_user_no2uid(xnr_user_no)
#     print 'uid:::',uid
#     if xnr_user_no:
#         if S_TYPE == 'test':
#             es_results = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
#                                 body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
#             current_time = es_results[0]['_source']['timestamp']
        
#         else:
#             current_time = time.time()
    
#         current_date = ts2datetime(current_time)
#         current_time_new = datetime2ts(current_date)

#         # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
#         es_update_result = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
#                                 body={'query':{'match_all':{}},'sort':{'timestamp':'desc'}})['hits']['hits']
#         update_time = es_update_result[0]['_source']['update_time']
#         print 'update_time:::',update_time
#         for i in range(WEEK+1): # WEEK=7
#             start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
#             end_ts = current_time_new - i*DAY

#             query_body_day = {
#                 'query':{
#                     'bool':{
#                         'must':[
#                             {'term':{'root_uid':uid}},
#                             {'term':{'update_time':update_time}},
#                             {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
#                         ]
#                     }
#                 }
#             }

#             query_body_total = {
#                 'query':{
#                     'bool':{
#                         'must':[
#                             {'term':{'root_uid':uid}},
#                             {'term':{'update_time':update_time}},
#                             {'range':{'timestamp':{'lt':end_ts}}}
#                         ]
#                     }
#                 }
#             }

#             es_day_count_result = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
#                             body=query_body_day,request_timeout=999999)
#             print 'es_day_count_result::',es_day_count_result
#             if es_day_count_result['_shards']['successful'] != 0:
#                 es_day_count = es_day_count_result['count']
#             else:
#                 return 'es_day_count_found_error'
            
#             es_total_count_result = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
#                             body=query_body_total,request_timeout=999999)

#             if es_total_count_result['_shards']['successful'] != 0:
#                 es_total_count = es_total_count_result['count']
#             else:
#                 return 'es_total_count_found_error'

#             fans_num_day[start_ts] = es_day_count
#             fans_num_total[start_ts] = es_total_count
#             print 'fans_num_day::',fans_num_day
#             print 'fans_num_total::',fans_num_total

#         total_dict = compute_growth_rate_total(fans_num_day,fans_num_total)
#         print 'total_dict::',total_dict
#         return total_dict
#     else:
#         return ''

'''
# 影响力 粉丝的粉丝数
def get_influ_fans_fans_num(xnr_user_no):
    if S_TYPE == 'test':
        uid = S_UID
        current_time = datetime2ts(S_DATE)
    else:
        uid = xnr_user_no2uid(xnr_user_no)
        current_time = int(time.time())
    
    fans_follow_es_result = es.search(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_name,\
        id=xnr_user_no)['_source']
    fans_list = fans_follow_es_result['fans_list']

    index_name_list = get_flow_text_index_list(current_time)
    index_name_list = index_name_list.reverse()
    i = 0
    for index_name in index_name_list:
        es_flow_results = es_flow_text.mget(index=index_name,doc_type=flow_text_index_type,body={'uids':fans_list})['docs']
        for result in es_flow_results:
            if not result['found']:
                while True:
                current_time_second = datetime2ts(index_name)
                index_name_list_second = get_flow_text_index_list(current_time_second)

    return []
'''

def get_influ_retweeted_num(xnr_user_no):

    retweeted_num_day = {}  # 每天增量统计
    retweeted_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
        #                         body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()

        if S_TYPE == 'test':
            current_time = datetime2ts('2017-10-07')
        else:
            current_time = int(time.time())

        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
        #es_update_result = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
        #                        body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
        #update_time = es_update_result[0]['_source']['update_time']

        for i in range(WEEK): # WEEK=7
            start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
            end_ts = current_time_new - i*DAY 

            query_body_day = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }

            query_body_total = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'range':{'timestamp':{'gte':0,'lt':end_ts}}}
                        ]
                    }
                }
            }

            print 'end_ts:::',end_ts

            es_day_count_result = es.count(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
                            body=query_body_day,request_timeout=999999)

            if es_day_count_result['_shards']['successful'] != 0:
                es_day_count = es_day_count_result['count']
            else:
                return 'es_day_count_found_error'
            print 'es_day_count:::',es_day_count

            es_total_count_result = es.count(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
                            body=query_body_total,request_timeout=999999)

            if es_total_count_result['_shards']['successful'] != 0:
                es_total_count = es_total_count_result['count']
            else:
                return 'es_total_count_found_error'

            print 'es_total_count:::',es_total_count
            retweeted_num_day[start_ts] = es_day_count
            retweeted_num_total[start_ts] = es_total_count

        total_dict = compute_growth_rate_total(retweeted_num_day,retweeted_num_total)

        return total_dict
    else:
        return ''


def get_influ_commented_num(xnr_user_no):
    # 收到的评论 comment_type : receive
    commented_num_day = {}  # 每天增量统计
    commented_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
        #                         body={'query':{'term':{'comment_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()

        if S_TYPE == 'test':
            current_time = datetime2ts('2017-10-07')
        else:
            current_time = int(time.time())

        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
        #es_update_result = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
        #                        body={'query':{'term':{'comment_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
        #update_time = es_update_result[0]['_source']['update_time']

        for i in range(WEEK): # WEEK=7
            start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
            end_ts = current_time_new - i*DAY 

            query_body_day = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'term':{'comment_type':'receive'}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }

            query_body_total = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'term':{'comment_type':'receive'}},
                            {'range':{'timestamp':{'lt':end_ts}}}
                        ]
                    }
                }
            }

            es_day_count_result = es.count(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
                            body=query_body_day,request_timeout=999999)

            if es_day_count_result['_shards']['successful'] != 0:
                es_day_count = es_day_count_result['count']
            else:
                return 'es_day_count_found_error'
            print 'es_day_count:::',es_day_count


            es_total_count_result = es.count(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
                            body=query_body_total,request_timeout=999999)

            if es_total_count_result['_shards']['successful'] != 0:
                es_total_count = es_total_count_result['count']
            else:
                return 'es_total_count_found_error'

            print 'es_total_count:::',es_total_count

            commented_num_day[start_ts] = es_day_count
            commented_num_total[start_ts] = es_total_count

        total_dict = compute_growth_rate_total(commented_num_day,commented_num_total)

        return total_dict
    else:
        return ''


def get_influ_like_num(xnr_user_no):

    like_num_dict = {}
    like_num_day = {}  # 每天增量统计
    like_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
        #                         body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()
        
        if S_TYPE == 'test':
            current_time = datetime2ts('2017-10-07')
        else:
            current_time = int(time.time())

        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
        #es_update_result = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
        #                        body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
        #update_time = es_update_result[0]['_source']['update_time']

        for i in range(WEEK): # WEEK=7
            start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
            end_ts = current_time_new - i*DAY 

            query_body_day = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }
            
            query_body_total = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'range':{'timestamp':{'lt':end_ts}}}
                        ]
                    }
                }
            }

            es_day_count_result = es.count(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
                            body=query_body_day,request_timeout=999999)

            if es_day_count_result['_shards']['successful'] != 0:
                es_day_count = es_day_count_result['count']
            else:
                return 'es_day_count_found_error'
            print 'es_day_count:::',es_day_count


            es_total_count_result = es.count(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
                            body=query_body_total,request_timeout=999999)

            if es_total_count_result['_shards']['successful'] != 0:
                es_total_count = es_total_count_result['count']
            else:
                return 'es_total_count_found_error'

            print 'es_total_count:::',es_total_count


            like_num_day[start_ts] = es_day_count
            like_num_total[start_ts] = es_total_count

        total_dict = compute_growth_rate_total(like_num_day,like_num_total)

        return total_dict
    else:
        return ''


def get_influ_at_num(xnr_user_no):

    at_num_dict = {}
    at_num_day = {}  # 每天增量统计
    at_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
        #                         body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()
        
        if S_TYPE == 'test':
            current_time = datetime2ts('2017-10-07')
        else:
            current_time = int(time.time())

        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
        #es_update_result = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
        #                        body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
        #update_time = es_update_result[0]['_source']['update_time']

        for i in range(WEEK): # WEEK=7
            start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
            end_ts = current_time_new - i*DAY 

            query_body_day = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }

            query_body_total = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'range':{'timestamp':{'lt':end_ts}}}
                        ]
                    }
                }
            }

            es_day_count_result = es.count(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
                            body=query_body_day,request_timeout=999999)

            if es_day_count_result['_shards']['successful'] != 0:
                es_day_count = es_day_count_result['count']
            else:
                return 'es_day_count_found_error'
            print 'es_day_count:::',es_day_count

            es_total_count_result = es.count(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
                            body=query_body_total,request_timeout=999999)

            if es_total_count_result['_shards']['successful'] != 0:
                es_total_count = es_total_count_result['count']
            else:
                return 'es_total_count_found_error'

            print 'es_total_count:::',es_total_count

            at_num_day[start_ts] = es_day_count
            at_num_total[start_ts] = es_total_count

        total_dict = compute_growth_rate_total(at_num_day,at_num_total)

        return total_dict
    else:
        return ''


def get_influ_private_num(xnr_user_no):
    # 收到的私信 private_type : receive
    private_num_dict = {}
    private_num_day = {}  # 每天增量统计
    private_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
        #                         body={'query':{'term':{'private_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()
        if S_TYPE == 'test':
            current_time = datetime2ts('2017-10-07')
        else:
            current_time = int(time.time())

        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
        #es_update_result = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
        #                        body={'query':{'term':{'private_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
        #update_time = es_update_result[0]['_source']['update_time']

        for i in range(WEEK): # WEEK=7
            start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
            end_ts = current_time_new - i*DAY 

            query_body_day = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'term':{'private_type':'receive'}},
                            {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                }
            }

            query_body_total = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'term':{'private_type':'receive'}},
                            {'range':{'timestamp':{'lt':end_ts}}}
                        ]
                    }
                }
            }

            es_day_count_result = es.count(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
                            body=query_body_day,request_timeout=999999)

            if es_day_count_result['_shards']['successful'] != 0:
                es_day_count = es_day_count_result['count']
            else:
                return 'es_day_count_found_error'
            print 'es_day_count:::',es_day_count


            es_total_count_result = es.count(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
                            body=query_body_total,request_timeout=999999)

            if es_total_count_result['_shards']['successful'] != 0:
                es_total_count = es_total_count_result['count']
            else:
                return 'es_total_count_found_error'

            print 'es_total_count:::',es_total_count

            private_num_day[start_ts] = es_day_count
            private_num_total[start_ts] = es_total_count

        total_dict = compute_growth_rate_total(private_num_day,private_num_total)

        return total_dict
    else:
        return ''

def compute_influence_num(xnr_user_no):

    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-07')
    else:
        current_time = int(time.time()-DAY)
    
    current_date = ts2datetime(current_time)

    _id = xnr_user_no + '_' + current_date
    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
            id=_id)['_source']

    influence = get_result['influence']

    return influence

'''
渗透力
'''

# 渗透力分数
def compute_penetration_num(xnr_user_no):

    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-07')
    else:
        current_time = int(time.time()-DAY)
    
    current_date = ts2datetime(current_time)

    _id = xnr_user_no + '_' + current_date
    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
            id=_id)['_source']

    pene_mark = get_result['penetration']

    return pene_mark


def penetration_total(xnr_user_no,start_time,end_time):
    
    total_dict = {}
    total_dict['follow_group'] = {}
    total_dict['fans_group'] = {}
    total_dict['feedback_total'] = {}
    total_dict['self_info'] = {}
    total_dict['warning_report_total'] = {}

    query_body = {
        'query':{
            'term':{
                'range':{'gte':start_time,'lt':end_time}
            }
        },
        'size':MAX_SEARCH_SIZE
    }

    total_dict['follow_group'] = follow_group['sensitive_info']
    total_dict['fans_group'] = fans_group['sensitive_info']
    total_dict['self_info'] = self_info['sensitive_info']
    total_dict['warning_report_total'] = warning_report_total
    total_dict['feedback_total'] = feedback_total['sensitive_info']

    return total_dict


def compute_safe_num(xnr_user_no):
    
    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-07')
    else:
        current_time = int(time.time()-DAY)
    
    current_date = ts2datetime(current_time)

    _id = xnr_user_no + '_' + current_date
    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
            id=_id)['_source']

    safe_mark = get_result['safe']

    return safe_mark

def get_safe_active(xnr_user_no):

    #uid = xnr_user_no2uid(xnr_user_no)

    # if S_TYPE == 'test':
    #     current_time = datetime2ts(S_DATE)
    #     uid = S_UID
    # else:
    
    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-07')
    else:
        current_time = (int(time.time())-DAY)
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    safe_active_dict = {}

    for i in range(WEEK):

        timestamp = current_time_new - i*DAY 
        datetime = ts2datetime(timestamp)
        _id = xnr_user_no + '_' + datetime
        result = es.get(index=weibo_xnr_count_info_index_name,\
                    doc_type=weibo_xnr_count_info_index_type,id=_id)['_source']

        safe_active_dict[timestamp] = result['total_post_sum']
    
    return safe_active_dict

def get_tweets_distribute(xnr_user_no):

    topic_distribute_dict = {}
    topic_distribute_dict['radar'] = {}

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        followers_list = es_results['followers_list']

    # if S_TYPE == 'test':
    #     uid=PORTRAI_UID
    #     followers_list=PORTRAIT_UID_LIST

    # 关注者topic分布

    results = es_user_portrait.mget(index=portrait_index_name,doc_type=portrait_index_type,\
        body={'ids':followers_list})['docs']

    topic_list_followers = []

    for result in results:
        if result['found'] == True:
            result = result['_source']
            topic_string_first = result['topic_string'].split('&')
            topic_list_followers.extend(topic_string_first)

    topic_list_followers_count = Counter(topic_list_followers)

    #topic_distribute_dict['topic_follower'] = topic_list_followers_count
    # 虚拟人topic分布
    #try:
        # xnr_results = es_user_portrait.get(index=portrait_index_name,doc_type=portrait_index_type,\
        #     id=uid)['_source']
        # topic_string = xnr_results['topic_string'].split('&')
        # topic_xnr_count = Counter(topic_string)

    current_time = int(time.time())

    index_name_list = get_xnr_flow_text_index_list(current_time)
    topic_string = []
    
    for index_name_day in index_name_list:

        query_body = {
 