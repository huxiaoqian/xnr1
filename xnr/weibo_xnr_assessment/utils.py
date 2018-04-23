# -*-coding:utf-8-*-

import json
import time
from collections import Counter
import random
from xnr.global_utils import es_xnr as es
from xnr.global_utils import R_WEIBO_XNR_FANS_FOLLOWERS as r_fans_followers 
from xnr.global_utils import es_flow_text,es_user_portrait,es_user_profile,weibo_feedback_comment_index_name_pre,weibo_feedback_comment_index_type,\
                        weibo_feedback_retweet_index_name_pre,weibo_feedback_retweet_index_type,\
                        weibo_feedback_private_index_name_pre,weibo_feedback_private_index_type,\
                        weibo_feedback_at_index_name_pre,weibo_feedback_at_index_type,\
                        weibo_feedback_like_index_name_pre,weibo_feedback_like_index_type,\
                        weibo_feedback_fans_index_name,weibo_feedback_fans_index_type,\
                        weibo_feedback_follow_index_name_pre,weibo_feedback_follow_index_type,\
                        weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                        flow_text_index_type,weibo_bci_index_name_pre,weibo_bci_index_type,\
                        flow_text_index_name_pre,weibo_report_management_index_name_pre,weibo_report_management_index_type,\
                        portrait_index_name,portrait_index_type,xnr_flow_text_index_type,\
                        weibo_xnr_assessment_index_name,weibo_xnr_assessment_index_type,\
                        weibo_xnr_count_info_index_name,weibo_xnr_count_info_index_type,\
                        user_domain_index_name,user_domain_index_type,\
                        new_xnr_flow_text_index_name_pre,xnr_flow_text_index_type,xnr_flow_text_index_name_pre
                        
from xnr.global_utils import r_fans_uid_list_datetime_pre,r_fans_count_datetime_xnr_pre,r_fans_search_xnr_pre,\
                r_followers_uid_list_datetime_pre,r_followers_count_datetime_xnr_pre,r_followers_search_xnr_pre

from xnr.utils import xnr_user_no2uid,uid2nick_name_photo
from xnr.global_config import S_TYPE,S_DATE,S_UID,S_DATE_BCI
from xnr.time_utils import ts2datetime,datetime2ts,get_flow_text_index_list,get_new_xnr_flow_text_index_list
from xnr.parameter import WEEK,DAY,MAX_SEARCH_SIZE,PORTRAIT_UID_LIST,PORTRAI_UID,FOLLOWERS_TODAY,\
                        TOP_ASSESSMENT_NUM,ACTIVE_UID,TOP_WEIBOS_LIMIT, FLOW_TEXT_START_DATE


def get_influence_total_trend(xnr_user_no,start_time,end_time):

    

    total_dict = {}
    total_dict['total_trend'] = {}
    total_dict['day_num'] = {}
    total_dict['growth_rate'] = {}

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_user_no':xnr_user_no}},
                    {'range':{
                        'timestamp':{'gte':start_time,'lt':end_time}
                    }}
                ]
            }
        },
        'size':MAX_SEARCH_SIZE
    }


    search_results = es.search(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
        body=query_body)['hits']['hits']
    
    fans_dict = {}
    fans_dict['total_num'] = {}
    fans_dict['day_num'] = {}
    fans_dict['growth_rate'] = {}

    retweet_dict = {}
    retweet_dict['total_num'] = {}
    retweet_dict['day_num'] = {}
    retweet_dict['growth_rate'] = {}

    comment_dict = {}
    comment_dict['total_num'] = {}
    comment_dict['day_num'] = {}
    comment_dict['growth_rate'] = {}

    like_dict = {}
    like_dict['total_num'] = {}
    like_dict['day_num'] = {}
    like_dict['growth_rate'] = {}

    at_dict = {}
    at_dict['total_num'] = {}
    at_dict['day_num'] = {}
    at_dict['growth_rate'] = {}

    private_dict = {}
    private_dict['total_num'] = {}
    private_dict['day_num'] = {}
    private_dict['growth_rate'] = {}


    for result in search_results:
        result = result['_source']
        timestamp = result['timestamp']

        fans_dict['total_num'][timestamp] = result['fans_total_num']
        fans_dict['day_num'][timestamp] = result['fans_day_num']
        fans_dict['growth_rate'][timestamp] = result['fans_growth_rate']

        retweet_dict['total_num'][timestamp] = result['retweet_total_num']
        retweet_dict['day_num'][timestamp] = result['retweet_day_num']
        retweet_dict['growth_rate'][timestamp] = result['retweet_growth_rate']

        comment_dict['total_num'][timestamp] = result['comment_total_num']
        comment_dict['day_num'][timestamp] = result['comment_day_num']
        comment_dict['growth_rate'][timestamp] = result['comment_growth_rate']

        like_dict['total_num'][timestamp] = result['like_total_num']
        like_dict['day_num'][timestamp] = result['like_day_num']
        like_dict['growth_rate'][timestamp] = result['like_growth_rate']

        private_dict['total_num'][timestamp] = result['private_total_num']
        private_dict['day_num'][timestamp] = result['private_day_num']
        private_dict['growth_rate'][timestamp] = result['private_growth_rate']
        
        at_dict['total_num'][timestamp] = result['at_total_num']
        at_dict['day_num'][timestamp] = result['at_day_num']
        at_dict['growth_rate'][timestamp] = result['at_growth_rate']


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

def get_influence_total_trend_today(xnr_user_no):

    current_time = int(time.time())

    fans_dict = get_influ_fans_num(xnr_user_no,current_time)
    retweet_dict = get_influ_retweeted_num(xnr_user_no,current_time)
    comment_dict = get_influ_commented_num(xnr_user_no,current_time)
    like_dict = get_influ_like_num(xnr_user_no,current_time)
    at_dict = get_influ_at_num(xnr_user_no,current_time)
    private_dict = get_influ_private_num(xnr_user_no,current_time)

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
    # print 'day8_dict::',day8_dict
    # print 'total8_dict:::',total8_dict
    for timestamp, num in day8_dict.iteritems():
        total_timestamp = timestamp - DAY
        day_num = day8_dict[timestamp]
        try:
            total_num_lastday = total8_dict[total_timestamp]
            # print 'total_num_lastday:::',total_num_lastday
            if not total_num_lastday:
                total_num_lastday = 1
            total_dict['growth_rate'][timestamp] = round(float(day_num)/total_num_lastday,2)
            total_dict['day_num'][timestamp] = day8_dict[timestamp]
            total_dict['total_num'][timestamp] = total8_dict[timestamp]
        except:
            continue

    return total_dict

# 影响力粉丝数
def get_influ_fans_num(xnr_user_no,current_time):
    fans_dict = {}
    # fans_num_day = {}  # 每天增量统计
    # fans_num_total = {} # 截止到当天总量统计

    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-07')
    else:
        current_time = int(time.time())
    # if S_TYPE == 'test':
    #     current_time = datetime2ts('2017-10-7')
    # else:
    #     current_time = int(time.time())
    #current_time = int(time.time()-DAY)
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    #for i in range(WEEK+1):
        # timestamp = current_time_new - (i+1)*DAY  # DAY=3600*24
        # datetime = ts2datetime(timestamp)
    r_fans_count = r_fans_count_datetime_xnr_pre + current_date + '_' + xnr_user_no
    r_fans_uid_list = r_fans_uid_list_datetime_pre + current_date

    datetime_count = r_fans_followers.get(r_fans_count)
    fans_uid_list = r_fans_followers.hget(r_fans_uid_list,xnr_user_no)

    if not datetime_count:
        datetime_count = 0

    if not fans_uid_list:
        datetime_total = 0
    else:
        datetime_total = len(json.loads(fans_uid_list))
    fans_dict['day_num'] = {}
    fans_dict['total_num'] = {}
    fans_dict['growth_rate'] = {}
    fans_dict['day_num'][current_time_new] = datetime_count
    fans_dict['total_num'][current_time_new] = datetime_total

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,id=_id_last_day)['_source']
    fans_total_num_last = get_result['fans_total_num']
    if not fans_total_num_last:
        fans_total_num_last = 1

    fans_dict['growth_rate'][current_time_new] = round(float(datetime_count)/fans_total_num_last,2)

    #total_dict = compute_growth_rate_total(fans_num_day,fans_num_total)

    return fans_dict

def get_influ_retweeted_num(xnr_user_no,current_time):

    retweet_dict = {}

    # retweeted_num_day = {}  # 每天增量统计
    # retweeted_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    # if xnr_user_no:

    #     if S_TYPE == 'test':
    #         current_time = datetime2ts('2017-10-07')
    #     else:
    #         current_time = int(time.time())
    #current_time = int(time.time()-DAY)
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
    #es_update_result = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
    #                        body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
    #update_time = es_update_result[0]['_source']['update_time']

    #for i in range(WEEK): # WEEK=7
        # start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
        # end_ts = current_time_new - i*DAY 

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}}
                ]
            }
        }
    }

    weibo_feedback_retweet_index_name = weibo_feedback_retweet_index_name_pre + current_date

    es_day_count_result = es.count(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        #return 'es_day_count_found_error'
        es_day_count = 0

    retweet_dict['day_num'] = {}
    retweet_dict['total_num'] = {}
    retweet_dict['growth_rate'] = {}

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,id=_id_last_day)['_source']
    retweet_total_num_last = get_result['retweet_total_num']

    if not retweet_total_num_last:
        retweet_total_num_last = 1

    retweet_dict['day_num'][current_time_new] = es_day_count
    retweet_dict['total_num'][current_time_new] = retweet_total_num_last + es_day_count

    retweet_dict['growth_rate'][current_time_new] = round(float(es_day_count)/retweet_total_num_last,2)

    
    return retweet_dict

def get_influ_commented_num(xnr_user_no,current_time):
    # 收到的评论 comment_type : receive
    comment_dict = {}
    # commented_num_day = {}  # 每天增量统计
    # commented_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    #if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
        #                         body={'query':{'term':{'comment_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()

    # if S_TYPE == 'test':
    #     current_time = datetime2ts('2017-10-07')
    # else:
    #     current_time = int(time.time())
    #current_time = int(time.time()-DAY)
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
    #es_update_result = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
    #                        body={'query':{'term':{'comment_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
    #update_time = es_update_result[0]['_source']['update_time']

    #for i in range(WEEK): # WEEK=7
        # start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
        # end_ts = current_time_new - i*DAY 

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'comment_type':'receive'}},
                ]
            }
        }
    }

    weibo_feedback_comment_index_name = weibo_feedback_comment_index_name_pre + current_date
    es_day_count_result = es.count(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        #return 'es_day_count_found_error'
        es_day_count = 0


    comment_dict['day_num'] = {}
    comment_dict['total_num'] = {}
    comment_dict['growth_rate'] = {}



    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,id=_id_last_day)['_source']
    comment_total_num_last = get_result['comment_total_num']

    if not comment_total_num_last:
        comment_total_num_last = 1

    comment_dict['day_num'][current_time_new] = es_day_count
    comment_dict['total_num'][current_time_new] = comment_total_num_last + es_day_count
    comment_dict['growth_rate'][current_time_new] = round(float(es_day_count)/comment_total_num_last,2)

    return comment_dict

def get_influ_like_num(xnr_user_no,current_time):

    like_dict = {}

    # like_num_dict = {}
    # like_num_day = {}  # 每天增量统计
    # like_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    #if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
        #                         body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()
        
    # if S_TYPE == 'test':
    #     current_time = datetime2ts('2017-10-07')
    # else:
    #     current_time = int(time.time())
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
    #es_update_result = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
    #                        body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
    #update_time = es_update_result[0]['_source']['update_time']

    #for i in range(WEEK): # WEEK=7
    # start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
    # end_ts = current_time_new - i*DAY 

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}}
                ]
            }
        }
    }
    weibo_feedback_like_index_name = weibo_feedback_like_index_name_pre + current_date
    es_day_count_result = es.count(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        #return 'es_day_count_found_error'
        es_day_count = 0


    like_dict['day_num'] = {}
    like_dict['total_num'] = {}
    like_dict['growth_rate'] = {}

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,id=_id_last_day)['_source']
    like_total_num_last = get_result['like_total_num']

    if not like_total_num_last:
        like_total_num_last = 1

    like_dict['day_num'][current_time_new] = es_day_count
    like_dict['total_num'][current_time_new] = like_total_num_last + es_day_count

    like_dict['growth_rate'][current_time_new] = round(float(es_day_count)/like_total_num_last,2)

    return like_dict

def get_influ_at_num(xnr_user_no,current_time):
    at_dict = {}
    # at_num_dict = {}
    # at_num_day = {}  # 每天增量统计
    # at_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    #if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
        #                         body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()
        
        # if S_TYPE == 'test':
        #     current_time = datetime2ts('2017-10-07')
        # else:
        #     current_time = int(time.time())

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
    #es_update_result = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
    #                        body={'query':{'match_all':{}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
    #update_time = es_update_result[0]['_source']['update_time']

    # for i in range(WEEK): # WEEK=7
    # start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
    # end_ts = current_time_new - i*DAY 

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}}
                ]
            }
        }
    }

    weibo_feedback_at_index_name = weibo_feedback_at_index_name_pre + current_date
    es_day_count_result = es.count(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        #return 'es_day_count_found_error'
        es_day_count = 0



    at_dict['day_num'] = {}
    at_dict['total_num'] = {}
    at_dict['growth_rate'] = {}


    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,id=_id_last_day)['_source']
    at_total_num_last = get_result['at_total_num']

    if not at_total_num_last:
        at_total_num_last = 1

    at_dict['day_num'][current_time_new] = es_day_count
    at_dict['total_num'][current_time_new] = at_total_num_last + es_day_count

    at_dict['growth_rate'][current_time_new] = round(float(es_day_count)/at_total_num_last,2)


    return at_dict

def get_influ_private_num(xnr_user_no,current_time):
    # 收到的私信 private_type : receive
    private_dict = {}

    # private_num_dict = {}
    # private_num_day = {}  # 每天增量统计
    # private_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    #if xnr_user_no:
        # if S_TYPE == 'test':
        #     es_results = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
        #                         body={'query':{'term':{'private_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
        #     current_time = es_results[0]['_source']['timestamp']
        # else:
        #     current_time = time.time()
        # if S_TYPE == 'test':
        #     current_time = datetime2ts('2017-10-07')
        # else:
        #     current_time = int(time.time())

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
    #es_update_result = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
    #                        body={'query':{'term':{'private_type':'receive'}},'sort':{'update_time':{'order':'desc'}}})['hits']['hits']
    #update_time = es_update_result[0]['_source']['update_time']

    # for i in range(WEEK): # WEEK=7
    # start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
    # end_ts = current_time_new - i*DAY 

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'private_type':'receive'}}
                ]
            }
        }
    }

    weibo_feedback_private_index_name = weibo_feedback_private_index_name_pre + current_date
    es_day_count_result = es.count(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        #return 'es_day_count_found_error'
        es_day_count = 0



    private_dict['day_num'] = {}
    private_dict['total_num'] = {}
    private_dict['growth_rate'] = {}


    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,id=_id_last_day)['_source']
    private_total_num_last = get_result['private_total_num']

    if not private_total_num_last:
        private_total_num_last = 1

    private_dict['day_num'][current_time_new] = es_day_count
    private_dict['total_num'][current_time_new] = private_total_num_last + es_day_count

    private_dict['growth_rate'][current_time_new] = round(float(es_day_count)/private_total_num_last,2)

    return private_dict



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
            'bool':{
                'must':[
                    {'term':{'xnr_user_no':xnr_user_no}},
                    {'range':{
                        'timestamp':{'gte':start_time,'lt':end_time}
                    }}
                ]
            }
        },
        'size':MAX_SEARCH_SIZE
    }

    search_results = es.search(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
        body=query_body)['hits']['hits']

    follow_group = {}
    fans_group = {}
    self_info = {}
    warning_report_total = {}
    feedback_total = {}


    for result in search_results:
        result = result['_source']
        timestamp = result['timestamp']
        follow_group[timestamp] = result['follow_group_sensitive_info']
        fans_group[timestamp] = result['fans_group_sensitive_info']
        self_info[timestamp] = result['self_info_sensitive_info']
        warning_report_total[timestamp] = result['warning_report_total_sensitive_info']
        feedback_total[timestamp] = result['feedback_total_sensitive_info']

    total_dict['follow_group'] = follow_group
    total_dict['fans_group'] = fans_group
    total_dict['self_info'] = self_info
    total_dict['warning_report_total'] = warning_report_total
    total_dict['feedback_total'] = feedback_total

    return total_dict

def penetration_total_today(xnr_user_no):

    total_dict = {}

    current_time = int(time.time())

    follow_group = get_pene_follow_group_sensitive(xnr_user_no,current_time)
    fans_group = get_pene_fans_group_sensitive(xnr_user_no,current_time)
    self_info = get_pene_infor_sensitive(xnr_user_no,current_time)
    
    feedback_at = get_pene_feedback_sensitive(xnr_user_no,'be_at',current_time)
    feedback_retweet = get_pene_feedback_sensitive(xnr_user_no,'be_retweet',current_time)
    feedback_commet = get_pene_feedback_sensitive(xnr_user_no,'be_comment',current_time)

    feedback_total = {}
    total_dict['follow_group'] = {}
    total_dict['fans_group'] = {}
    total_dict['self_info'] = {}
    total_dict['warning_report_total'] = {}
    total_dict['feedback_total'] = {}
    #feedback_total['sensitive_info'] = {}

    #for timestamp in feedback_at['sensitive_info']:
    feedback_total['sensitive_info'] = float(feedback_at['sensitive_info'] + \
        feedback_retweet['sensitive_info'] + feedback_commet['sensitive_info'])/3
    
    warning_report = get_pene_warning_report_sensitive(xnr_user_no,current_time)

    warning_report_total = round(float(warning_report['event']+ \
        warning_report['user'] + warning_report['tweet'])/3,2)

    # total_dict['follow_group'] = round(follow_group['sensitive_info'],2)
    # total_dict['fans_group'] = round(fans_group['sensitive_info'],2)
    # total_dict['self_info'] = round(self_info['sensitive_info'],2)
    # total_dict['warning_report_total'] = round(warning_report_total,2)
    # total_dict['feedback_total'] = round(feedback_total['sensitive_info'],2)

    total_dict['follow_group'][current_time] = follow_group['sensitive_info']
    total_dict['fans_group'][current_time] = fans_group['sensitive_info']
    total_dict['self_info'][current_time] = self_info['sensitive_info']
    total_dict['warning_report_total'][current_time] = warning_report_total
    total_dict['feedback_total'][current_time] = feedback_total['sensitive_info']

    return total_dict

def get_pene_follow_group_sensitive(xnr_user_no,current_time_old):

    #if xnr_user_no:
    es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                            id=xnr_user_no)["_source"]
    try:
        followers_list = es_results['followers_list']
    except:
        followers_list = []

    
    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
    else:
        current_time = current_time_old
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    #current_time_new_8 = current_time_new - 8*DAY # 统计8天，计算增长率要用
    #current_date_new_8 = ts2datetime(current_time_new_8)

    #index_name_list = get_flow_text_index_list(current_time_new)
    index_name = flow_text_index_name_pre + current_date
    #index_name_8 = flow_text_index_name_pre + current_date_new_8
    #index_name_list.append(index_name_8)

    follow_group_sensitive = {}
    #follow_group_sensitive['sensitive_info'] = {}
    #follow_group_sensitive['sensitive_user'] = {}

    #for index_name in index_name_list:

    query_body_info = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':followers_list}
                }
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive'
                }
            }
        }
    }
    es_sensitive_result = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
        body=query_body_info)['aggregations']
    sensitive_value = round(es_sensitive_result['avg_sensitive']['value'],2)

    if sensitive_value == None:
        sensitive_value = 0.0
    follow_group_sensitive['sensitive_info'] = sensitive_value

    return follow_group_sensitive

def get_pene_fans_group_sensitive(xnr_user_no,current_time_old):

    #if xnr_user_no:
    es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                            id=xnr_user_no)["_source"]
    try:
        fans_list = es_results['fans_list']
    except:
        fans_list = []

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
    else:
        current_time = current_time_old
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    #index_name_list = get_flow_text_index_list(current_time_new)
    index_name = flow_text_index_name_pre + current_date

    fans_group_sensitive = {}
    # fans_group_sensitive['sensitive_info'] = {}

    # for index_name in index_name_list:
    #     datetime = index_name[-10:]
    #     timestamp = datetime2ts(datetime)
    query_body_info = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':fans_list}
                }
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive'
                }
            }
        }
    }
    es_sensitive_result = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
        body=query_body_info)['aggregations']
    sensitive_value = es_sensitive_result['avg_sensitive']['value']

    if sensitive_value == None:
        sensitive_value = 0.0
    fans_group_sensitive['sensitive_info'] = sensitive_value

    return fans_group_sensitive

def get_pene_infor_sensitive(xnr_user_no,current_time_old):
    
    uid = xnr_user_no2uid(xnr_user_no)

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
        uid = S_UID
    else:
        current_time = current_time_old
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    #index_name_list = get_flow_text_index_list(current_time_new)
    index_name = flow_text_index_name_pre + current_date

    my_info_sensitive = {}
    # my_info_sensitive['sensitive_info'] = {}

    # for index_name in index_name_list:
    #     datetime = index_name[-10:]
    #     timestamp = datetime2ts(datetime)
    query_body_info = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'uid':uid}
                }
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive'
                }
            }
        }
    }
    es_sensitive_result = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
        body=query_body_info)['aggregations']
    sensitive_value = es_sensitive_result['avg_sensitive']['value']

    if sensitive_value == None:
        sensitive_value = 0.0
    my_info_sensitive['sensitive_info'] = sensitive_value

    return my_info_sensitive

def get_pene_feedback_sensitive(xnr_user_no,sort_item,current_time_old):
    
    uid = xnr_user_no2uid(xnr_user_no)

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE) #current_time_old
    else:
        current_time = current_time_old

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    

    if sort_item == 'be_at':
        index_name_sort = weibo_feedback_at_index_name_pre + current_date
        index_type_sort = weibo_feedback_at_index_type
    elif sort_item == 'be_retweet':
        index_name_sort = weibo_feedback_retweet_index_name_pre + current_date
        index_type_sort = weibo_feedback_retweet_index_type
    elif sort_item == 'be_comment':
        index_name_sort = weibo_feedback_comment_index_name_pre + current_date
        index_type_sort = weibo_feedback_comment_index_type


    feedback_sensitive_dict = {}

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}}
                ]
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive_info'
                }
            }
        }
    }

    es_sensitive_result = es.search(index=index_name_sort,doc_type=index_type_sort,body=query_body)['aggregations']

    sensitive_value = es_sensitive_result['avg_sensitive']['value']

    if sensitive_value == None:
        sensitive_value = 0.0
    feedback_sensitive_dict['sensitive_info'] = sensitive_value

    return feedback_sensitive_dict

def get_pene_warning_report_sensitive(xnr_user_no,current_time_old):

    sensitive_report_dict = {}
    # sensitive_report_dict['event'] = {}
    # sensitive_report_dict['user'] = {}
    # sensitive_report_dict['tweet'] = {}

    report_type_list = [u'人物',u'事件',u'言论']
    

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
    else:
        current_time = current_time_old

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)


    mid_event_list = []
    mid_tweet_list = []
    uid_list = []

    for report_type in report_type_list:
        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'xnr_user_no':xnr_user_no}},
                        {'term':{'report_type':report_type}}
                    ]
                }
            },
            'size':MAX_SEARCH_SIZE
            
        }
        weibo_report_management_index_name = weibo_report_management_index_name_pre + current_date
        
        try:
            es_sensitive_result = es.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,\
            body=query_body)['hits']['hits']
        except:
            es_sensitive_result = []


        if es_sensitive_result:    
            if report_type == u'事件':
                for result in es_sensitive_result:
                    result = result['_source']
                    report_content = json.loads(result['report_content'])
                    weibo_list = report_content['weibo_list']
                    for weibo in weibo_list:
                        mid_event_list.append(weibo['mid'])
            elif report_type == u'人物':
                for result in es_sensitive_result:
                    result = result['_source']
                    report_content = json.loads(result['report_content'])
                    user_list = report_content['user_list']
                    for user in user_list:
                        uid_list.append(user['uid'])
            elif report_type == u'言论':
                for result in es_sensitive_result:
                    result = result['_source']
                    report_content = json.loads(result['report_content'])
                    weibo_list = report_content['weibo_list']
                    for weibo in weibo_list:
                        mid_tweet_list.append(weibo['mid'])

    ## 事件平均敏感度
    
    query_body_event = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'mid':mid_event_list}
                }
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive'
                }
            }
        }
    }

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)

    index_name_list = get_flow_text_index_list(current_time)

    es_result_event = es_flow_text.search(index=index_name_list,doc_type=flow_text_index_type,\
        body=query_body_event)['aggregations']
    event_sensitive_avg = es_result_event['avg_sensitive']['value']

    if event_sensitive_avg == None:
        event_sensitive_avg = 0.0


    ## 人物平均敏感度
    query_body_user = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':uid_list}
                }
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive'
                }
            }
        }
    }

    es_result_user = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,\
        body=query_body_user)['aggregations']
    user_sensitive_avg = es_result_user['avg_sensitive']['value']

    if user_sensitive_avg == None:
        user_sensitive_avg = 0.0

    ## 言论平均敏感度
    query_body_tweet = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'mid':mid_tweet_list}
                }
            }
        },
        'aggs':{
            'avg_sensitive':{
                'avg':{
                    'field':'sensitive'
                }
            }
        }
    }

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
    index_name_list = get_flow_text_index_list(current_time)

    es_result_tweet = es_flow_text.search(index=index_name_list,doc_type=flow_text_index_type,\
        body=query_body_tweet)['aggregations']
    tweet_sensitive_avg = es_result_tweet['avg_sensitive']['value']
    if tweet_sensitive_avg == None:
        tweet_sensitive_avg = 0.0

    if S_TYPE == 'test':
        event_sensitive_avg = round(random.random(),2)
        user_sensitive_avg = round(random.random(),2)
        tweet_sensitive_avg = round(random.random(),2)

    sensitive_report_dict['event'] = event_sensitive_avg
    sensitive_report_dict['user'] = user_sensitive_avg
    sensitive_report_dict['tweet'] = tweet_sensitive_avg

    return sensitive_report_dict 


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

def get_safe_active(xnr_user_no,start_time,end_time):


    safe_active_dict = {}

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'xnr_user_no':xnr_user_no}},
                    {'range':{
                        'timestamp':{'gte':start_time,'lt':end_time}
                    }}
                ]
            }
        },
        'size':MAX_SEARCH_SIZE
    }

    search_results = es.search(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
        body=query_body)['hits']['hits']

    for result in search_results:
        result = result['_source']
        timestamp = result['timestamp']
        safe_active_dict[timestamp] = result['total_post_sum']
    
    return safe_active_dict

def get_safe_active_today(xnr_user_no):

    query_body = {
        'query':{
            'term':{'xnr_user_no':xnr_user_no}
        }
    }

    # if S_TYPE == 'test':
    #     current_time = datetime2ts('2017-10-11')
    # else:
    #     current_time = int(time.time())
    current_time = int(time.time())
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    safe_active_dict = {} 
    xnr_flow_text_index_name = new_xnr_flow_text_index_name_pre + current_date
    try:
        search_result = es.count(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,body=query_body)

        if search_result['_shards']['successful'] != 0:
            result = search_result['count']
        else:
            print 'es index rank error'
            result = 0
    except:
        result = 0
    safe_active_dict[current_time_new] = result

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
    #print 'topic_list_followers_count:::',topic_list_followers_count

    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-08')
    else:
        current_time = int(time.time())


    index_name_list = get_new_xnr_flow_text_index_list(current_time)
    topic_string = []

    for index_name_day in index_name_list:

        query_body = {
            'query':{
                'bool':{
                    'must':[
                        
                        {'term':{'xnr_user_no':xnr_user_no}}
                    ]
                }
            },
            'size':TOP_WEIBOS_LIMIT,
            'sort':{'timestamp':{'order':'desc'}}
        }
        try:
            #print 'index_name_day:::',index_name_day

            es_results = es.search(index=index_name_day,doc_type=xnr_flow_text_index_type,body=query_body)['hits']['hits']
            #print 'es_results::',es_results
            for topic_result in es_results:
                #print 'topic_result::',topic_result
                topic_result = topic_result['_source']
                topic_field = topic_result['topic_field_first'][:3]
            topic_string.append(topic_field)

        except:
            continue

    topic_xnr_count = Counter(topic_string)
    #print 'topic_xnr_count:::',topic_xnr_count
    #except:
        #topic_xnr_count = {}
        
    # 整理雷达图数据
    # if topic_xnr_count:
    #     for topic, value in topic_xnr_count.iteritems():
    #         try:
    #             topic_value = float(value)/(topic_list_followers_count[topic])
    #         except:
    #             continue
    #         topic_distribute_dict['radar'][topic] = topic_value
    #print 'topic_distribute_dict:::',topic_distribute_dict
    #print 'topic_xnr_count:::',topic_xnr_count
    if topic_xnr_count:
        for topic, value in topic_list_followers_count.iteritems():
            topic_xnr_count[topic] = min([topic_xnr_count[topic],value])
            try:
                topic_value = round(float(topic_xnr_count[topic])/value,2)
            except:
                continue
            topic_distribute_dict['radar'][topic] = topic_value
            
    # 整理仪表盘数据
    mark = 0
    
    if topic_xnr_count:
        n_topic = len(topic_list_followers_count.keys())
        for topic,value in topic_xnr_count.iteritems():

            try:
                mark += float(value)/(topic_list_followers_count[topic]*n_topic)
                # print topic 
                # print mark
            except:
                continue
    # print 'mark::',mark
    topic_distribute_dict['mark'] = round(mark,4)

    return topic_distribute_dict


def get_safe_tweets(xnr_user_no,topic,sort_item):


    if S_TYPE == 'test':
        current_time = 1507362127  # 10月7日

    else:
        current_time = int(time.time())

    index_name_list = get_new_xnr_flow_text_index_list(current_time)
    es_results_all = []
    
    for index_name_day in index_name_list:

        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'topic_field_first':topic}},
                        {'term':{'xnr_user_no':xnr_user_no}}
                    ]
                }
            },
            'size':TOP_WEIBOS_LIMIT,
            'sort':{sort_item:{'order':'desc'}}
        }
        try:
            es_results = es.search(index=index_name_day,doc_type=xnr_flow_text_index_type,body=query_body)['hits']['hits']
            es_results_all.extend(es_results)

        except:
            continue

    
    results_all = []
    for result in es_results_all:
        result = result['_source']
        uid = result['uid']
        nick_name,photo_url = uid2nick_name_photo(uid)
        result['nick_name'] = nick_name
        result['photo_url'] = photo_url
        results_all.append(result)
    return results_all

def get_follow_group_distribute(xnr_user_no):
    
    domain_distribute_dict = {}
    domain_distribute_dict['radar'] = {}

    # if S_TYPE == 'test':
    #     followers_list=PORTRAIT_UID_LIST
    #     followers_list_today = FOLLOWERS_TODAY
    # else:
    # 获取所有关注者
    es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                            id=xnr_user_no)["_source"]
    followers_list = es_results['followers_list']

    # 获取今日关注者
    if S_TYPE == 'test':
        current_time = datetime2ts('2017-10-02')  # 10月7日

    else:
        current_time = int(time.time())
    current_date = ts2datetime(current_time)
    r_uid_list_datetime_index_name = r_followers_uid_list_datetime_pre + current_date
    followers_results = r_fans_followers.hget(r_uid_list_datetime_index_name,xnr_user_no)
    # print 'followers_results::',followers_results
    if followers_results != None:
        followers_list_today = json.loads(followers_results)
    else:
        followers_list_today = []

    # 所有关注者领域分布

    results = es.mget(index=user_domain_index_name,doc_type=user_domain_index_type,\
        body={'ids':followers_list})['docs']
    
    domain_list_followers = []

    for result in results:
        if result['found'] == True:
            result = result['_source']
            domain_name = result['domain_name']
            domain_list_followers.append(domain_name)

    domain_list_followers_count = Counter(domain_list_followers)

    #domain_distribute_dict['domain_follower'] = domain_list_followers_count
    
    # 今日关注者
    #followers_list_today = FOLLOWERS_TODAY
    try:
        today_results = es.mget(index=user_domain_index_name,doc_type=user_domain_index_type,\
            body={'ids':followers_list_today})['docs']
        #print 'today_results:::',today_results
        domain_list_followers_today = []

        for result in today_results:
            if result['found'] == True:
                result = result['_source']
                domain_name = result['domain_name']
                domain_list_followers_today.append(domain_name)

        domain_list_followers_today_count = Counter(domain_list_followers_today)

    except:
        domain_list_followers_today_count = {}


    # 整理雷达图数据
    # if domain_list_followers_today_count:
    #     for domain, value in domain_list_followers_today_count.iteritems():
    #         try:
    #             domain_value = float(value)/(domain_list_followers_count[domain])
    #         except:
    #             continue
    #         domain_distribute_dict['radar'][domain] = domain_value

    
    for domain, value in domain_list_followers_count.iteritems():
        
        if domain_list_followers_today_count:
            try:
            
                domain_value = round(float(domain_list_followers_today_count[domain])/value,2)
            except:
                domain_value = 0
        else:
            domain_value = 0
            # try:
            #     domain_value = float(domain_list_followers_today_count[domain])/value
            # except:
            #     continue
        domain_value = min([domain_value,value])
        domain_distribute_dict['radar'][domain] = domain_value

    # 整理仪表盘数据
    mark = 0

    if domain_list_followers_today_count:
        n_domain = len(domain_list_followers_count.keys())
        for domain,value in domain_list_followers_today_count.iteritems():
            try:
                mark += float(value)/(domain_list_followers_count[domain]*n_domain)
            except:
                continue
    domain_distribute_dict['mark'] = round(mark,4)

    return domain_distribute_dict

def get_follow_group_tweets(xnr_user_no,domain,sort_item):

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
    else:
        current_time = int(time.time())

    es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                            id=xnr_user_no)["_source"]
    followers_list = es_results['followers_list']

    domain_query_body = {
        'query':{
            'bool':{
                'must':[
                    {'terms':{'uid':followers_list}},
                    {'term':{'domain_name':domain}}
                ]
            }
        }
    }

    domain_search_results = es.search(index=user_domain_index_name,\
        doc_type=user_domain_index_type,body=domain_query_body)['hits']['hits']

    domain_uid_list = []

    for domain_result in domain_search_results:
        domain_result = domain_result['_source']
        domain_uid_list.append(domain_result['uid'])

    results_all = []

    index_name_list = get_flow_text_index_list(current_time)

    query_body_flow_text = {
        'query':{
            'bool':{
                'must':[
                    {'terms':{'uid':domain_uid_list}},
                    {'terms':{'message_type':[1,3]}}
                ]
            }
        },
        'size':TOP_WEIBOS_LIMIT,
        'sort':{sort_item:{'order':'desc'}}
    }

    flow_text_results = es_flow_text.search(index=index_name_list,doc_type=flow_text_index_type,\
                        body=query_body_flow_text)['hits']['hits']

    results_all = []
    for result in flow_text_results:
        result = result['_source']
        uid = result['uid']
        nick_name,photo_url = uid2nick_name_photo(uid)
        result['nick_name'] = nick_name
        result['photo_url'] = photo_url
        results_all.append(result)
    return results_all


def create_xnr_history_info_count_today(xnr_user_no):
    
    #create_date=ts2datetime(create_time)

    current_date = ts2datetime(time.time())

    weibo_xnr_flow_text_name=xnr_flow_text_index_name_pre+current_date

    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_user_no':xnr_user_no}
                }
            }
        },
        'aggs':{
            'all_task_source':{
                'terms':{
                    'field':'task_source'
                }
            }
        }
    }

    xnr_user_detail=dict()
    #时间
    xnr_user_detail['date_time']=current_date

    try:

        xnr_result=es.search(index=weibo_xnr_flow_text_name,doc_type=xnr_flow_text_index_type,body=query_body)
        

        # daily_post-日常发帖,hot_post-热点跟随,business_post-业务发帖
        for item in xnr_result['aggregations']['all_task_source']['buckets']:
            if item['key'] == 'daily_post':
                xnr_user_detail['daily_post_num']=item['doc_count']
            elif item['key'] == 'business_post':
                xnr_user_detail['business_post_num']=item['doc_count']
            elif item['key'] == 'hot_post':
                xnr_user_detail['hot_follower_num']=item['doc_count']
            elif item['key'] =='trace_follow_tweet':
                xnr_user_detail['trace_follow_tweet_num']=item['doc_count']
        #总发帖量
        if xnr_user_detail.has_key('daily_post_num'):
            pass
        else:
            xnr_user_detail['daily_post_num']=0
        
        if xnr_user_detail.has_key('business_post_num'):
            pass
        else:
            xnr_user_detail['business_post_num']=0

        if xnr_user_detail.has_key('hot_follower_num'):
            pass
        else:
            xnr_user_detail['hot_follower_num']=0

        if xnr_user_detail.has_key('trace_follow_tweet_num'):
            pass
        else:
            xnr_user_detail['trace_follow_tweet_num']=0

        #xnr_user_detail['total_post_sum']=xnr_user_detail['daily_post_num']+xnr_user_detail['business_post_num']+xnr_user_detail['hot_follower_num']+xnr_user_detail['trace_follow_tweet_num']
    except:
        
        xnr_user_detail['daily_post_num']=0
        xnr_user_detail['business_post_num']=0
        xnr_user_detail['hot_follower_num']=0
        #xnr_user_detail['total_post_sum']=0
        xnr_user_detail['trace_follow_tweet_num']=0

    xnr_user_detail['xnr_user_no']=xnr_user_no

    return xnr_user_detail

def get_compare_assessment(xnr_user_no_list, dim, start_time, end_time):

    results_all = {}
    results_all['trend'] = {}
    results_all['table'] = []


    xnr_user_no_list = xnr_user_no_list.split(',')

    day_num = (end_time - start_time)/(24*3600)

    timestamp_list = []

    for i in range(day_num):
        timestamp_list.append(start_time + i*24*3600)


    for xnr_user_no in xnr_user_no_list:
        #xnr_user_no = 'WXNR0044'
        results_all['trend'][xnr_user_no] = {}
        
        table_result = {}
        
        for timestamp in timestamp_list:
            date = ts2datetime(timestamp)
            _id = xnr_user_no + '_' + date
            #print '_id...',_id
            try:
                get_result = es.get(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
                    id=_id)['_source']

            except:
                get_result = {}

            #print 'get_result...',get_result
            if get_result:

                if dim == 'influence':

                    results_all['trend'][xnr_user_no][timestamp] = get_result['influence']
                    
                    # 最新时间
                    #print 'comment_total.....',get_result['comment_total_num']
                    table_result['comment_total_num'] = get_result['comment_total_num']
                    table_result['like_total_num'] = get_result['like_total_num']
                    table_result['private_total_num'] = get_result['private_total_num']
                    table_result['at_total_num'] = get_result['at_total_num']
                    table_result['retweet_total_num'] = get_result['retweet_total_num']
                    table_result['xnr'] = xnr_user_no

                    #print 'table_result....',table_result

                elif dim == 'penetration':

                    results_all['trend'][xnr_user_no][timestamp] = get_result['penetration']
                    
                    table_result['follow_group_sensitive_info'] = get_result['follow_group_sensitive_info']
                    table_result['fans_group_sensitive_info'] = get_result['fans_group_sensitive_info']
                    table_result['self_info_sensitive_info'] = get_result['self_info_sensitive_info']
                    table_result['feedback_total_sensitive_info'] = get_result['feedback_total_sensitive_info']
                    table_result['warning_report_total_sensitive_info'] = get_result['warning_report_total_sensitive_info']
                    table_result['xnr'] = xnr_user_no

                else:

                    results_all['trend'][xnr_user_no][timestamp] = get_result['safe']
<<<<<<< HEAD


                    if timestamp == timestamp_list[-1]:    # 结束时间

                        timestamp_start = FLOW_TEXT_START_DATE  # 开始时间(统计表的开始时间就是系统开始时间)

                        if S_TYPE == 'test':
                        
                            timestamp = datetime2ts(ts2datetime(int(time.time())))  # 为了和小主页总量保持一致
                        
                        history_result = get_safe_history_count(timestamp,timestamp_start,xnr_user_no)
                        #print 'history_result..',history_result
                        table_result['total_post_sum'] = history_result['total_post_sum']
                        table_result['daily_post_num'] = history_result['daily_post_num']
                        table_result['hot_follower_num'] = history_result['business_post_num']
                        table_result['business_post_num'] = history_result['hot_follower_num']
                        table_result['trace_follow_tweet_num'] = history_result['trace_follow_tweet_num']

                        table_result['other'] = table_result['total_post_sum'] - table_result['daily_post_num'] - table_result['hot_follower_num'] - table_result['business_post_num'] - table_result['trace_follow_tweet_num']
                        table_result['xnr'] = xnr_user_no
                        
                    # table_result['total_post_sum'] = get_result['total_post_sum']
                    # table_result['daily_post_num'] = get_result['daily_post_num']
                    # table_result['hot_follower_num'] = get_result['hot_follower_num']
                    # table_result['business_post_num'] = get_result['business_post_num']
                    # table_result['trace_follow_tweet_num'] = get_result['trace_follow_tweet_num']
                    # table_result['other'] = get_result['total_post_sum'] - get_result['daily_post_num'] - get_result['hot_follower_num'] - get_result['business_post_num'] - get_result['trace_follow_tweet_num']
                    # table_result['xnr'] = xnr_user_no
=======
                    
                    table_result['total_post_sum'] = get_result['total_post_sum']
                    table_result['daily_post_num'] = get_result['daily_post_num']
                    table_result['hot_follower_num'] = get_result['hot_follower_num']
                    table_result['business_post_num'] = get_result['business_post_num']
                    table_result['trace_follow_tweet_num'] = get_result['trace_follow_tweet_num']
                    table_result['other'] = get_result['total_post_sum'] - get_result['daily_post_num'] - get_result['hot_follower_num'] - get_result['business_post_num'] - get_result['trace_follow_tweet_num']
                    table_result['xnr'] = xnr_user_no
>>>>>>> 8c15462c1341ac4b21c690562f79c749fedb5791
                    
            else:

                if dim == 'influence':

                    results_all['trend'][xnr_user_no][timestamp] = 0
                    table_result['comment_total_num'] = 0
                    table_result['like_total_num'] = 0
                    table_result['private_total_num'] = 0
                    table_result['at_total_num'] = 0
                    table_result['retweet_total_num'] = 0
                    table_result['xnr'] = xnr_user_no

                elif dim == 'penetration':

                    results_all['trend'][xnr_user_no][timestamp] = 0
                    
                    table_result['follow_group_sensitive_info'] = 0
                    table_result['fans_group_sensitive_info'] = 0
                    table_result['self_info_sensitive_info'] = 0
                    table_result['feedback_total_sensitive_info'] = 0
                    table_result['warning_report_total_sensitive_info'] = 0
                    table_result['xnr'] = xnr_user_no


                else:

                    results_all['trend'][xnr_user_no][timestamp] = 0
                    table_result = {}
                    table_result['total_post_sum'] = 0
                    table_result['daily_post_num'] = 0
                    table_result['hot_follower_num'] = 0
                    table_result['business_post_num'] = 0
                    table_result['trace_follow_tweet_num'] = 0
                    table_result['other'] = 0
                    table_result['xnr'] = xnr_user_no

            
        results_all['table'].append(table_result)

<<<<<<< HEAD
    #print 'results_all....',results_all
    return results_all


def xnr_cumulative_statistics(xnr_date_info):
    Cumulative_statistics_dict=dict()
    Cumulative_statistics_dict['date_time']='累计统计'
    if xnr_date_info: 
        #print xnr_date_info[0]
        
        total_post_sum=0
        daily_post_num=0
        business_post_num=0
        hot_follower_num=0
        trace_follow_tweet_num=0
        influence_sum=0
        penetration_sum=0
        safe_sum=0
        number=len(xnr_date_info)
        for i in xrange(0,len(xnr_date_info)):
            #print xnr_date_info[i]['date_time']
            #total_post_sum=total_post_sum+xnr_date_info[i]['total_post_sum']
            daily_post_num=daily_post_num+xnr_date_info[i]['daily_post_num']
            business_post_num=business_post_num+xnr_date_info[i]['business_post_num']
            hot_follower_num=hot_follower_num+xnr_date_info[i]['hot_follower_num']
            trace_follow_tweet_num=trace_follow_tweet_num+xnr_date_info[i]['trace_follow_tweet_num']
            #print total_post_sum,daily_post_num

        Cumulative_statistics_dict['total_post_sum']=daily_post_num+business_post_num+hot_follower_num+trace_follow_tweet_num
        Cumulative_statistics_dict['daily_post_num']=daily_post_num
        Cumulative_statistics_dict['business_post_num']=business_post_num
        Cumulative_statistics_dict['hot_follower_num']=hot_follower_num
        Cumulative_statistics_dict['trace_follow_tweet_num']=trace_follow_tweet_num

    else:
        
        Cumulative_statistics_dict['total_post_sum']=0
        Cumulative_statistics_dict['daily_post_num']=0
        Cumulative_statistics_dict['business_post_num']=0
        Cumulative_statistics_dict['hot_follower_num']=0
        Cumulative_statistics_dict['trace_follow_tweet_num']=0

    return Cumulative_statistics_dict


def show_condition_history_count(xnr_user_no,start_time,end_time):
    query_body={
        #'fields':['date_time','user_fansnum','total_post_sum','daily_post_num','hot_follower_num','business_post_num','influence','penetration','safe'],
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no}},
                            {'range':{
                                'timestamp':{
                                    'gte':start_time,
                                    'lt':end_time
                                }
                            }}
                        ]
                    }
                }
            }
        },
        'sort':{'timestamp':{'order':'asc'}} ,
        'size':MAX_SEARCH_SIZE
    }
    #print 'weibo_xnr_count_info_index_name::',weibo_xnr_count_info_index_name
    #try:
    xnr_count_result=es.search(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,body=query_body)['hits']['hits']
    print 'xnr_count_result...',xnr_count_result
    xnr_date_info=[]
    for item in xnr_count_result:
        xnr_date_info.append(item['_source'])
    # except:
    #     xnr_date_info=[]
    return xnr_date_info

def get_safe_history_count(end_time,start_time,xnr_user_no):

    now_time=int(time.time())
    system_start_time=FLOW_TEXT_START_DATE
    if end_time > now_time:
        end_time=now_time
    if start_time < system_start_time:
        start_time=system_start_time
    print 'condition_time:',ts2datetime(start_time),ts2datetime(end_time)
    xnr_date_info=show_condition_history_count(xnr_user_no,start_time,end_time)
    Cumulative_statistics_dict=xnr_cumulative_statistics(xnr_date_info)

    return Cumulative_statistics_dict


=======
    print 'results_all....',results_all
    return results_all


>>>>>>> 8c15462c1341ac4b21c690562f79c749fedb5791
def get_compare_assessment_today(xnr_user_no_list, dim):

    results_all = {}
    results_all['trend'] = {}
    results_all['table'] = []

<<<<<<< HEAD
    timestamp = datetime2ts(ts2datetime(int(time.time())))
    timestamp_start = FLOW_TEXT_START_DATE
=======
    timestamp = int(time.time())
>>>>>>> 8c15462c1341ac4b21c690562f79c749fedb5791

    xnr_user_no_list = xnr_user_no_list.split(',')

    for xnr_user_no in xnr_user_no_list:

        results_all['trend'][xnr_user_no] = {}
        table_result = {}


        if dim == 'influence':

            try:
                results_all['trend'][xnr_user_no][timestamp] = compute_influence_num(xnr_user_no)
        
                result = get_influence_total_trend_today(xnr_user_no)

                table_result['comment_total_num'] = list(result['total_trend']['comment'].values())[0]
                table_result['like_total_num'] = list(result['total_trend']['like'].values())[0]
                table_result['private_total_num'] = list(result['total_trend']['private'].values())[0]
                table_result['at_total_num'] = list(result['total_trend']['at'].values())[0]
                table_result['retweet_total_num'] = list(result['total_trend']['retweet'].values())[0]
                table_result['xnr'] = xnr_user_no

            except:
                results_all['trend'][xnr_user_no][timestamp] = 0
        
                table_result = {}

                table_result['comment_total_num'] = 0
                table_result['like_total_num'] = 0
                table_result['private_total_num'] = 0
                table_result['at_total_num'] = 0
                table_result['retweet_total_num'] = 0
                table_result['xnr'] = xnr_user_no

        elif dim == 'penetration':

            try:
                results_all['trend'][xnr_user_no][timestamp] = compute_penetration_num(xnr_user_no)
                

                result = penetration_total_today(xnr_user_no)

                table_result['follow_group_sensitive_info'] = list(result['follow_group'].values())[0]
                table_result['fans_group_sensitive_info'] = list(result['fans_group'].values())[0]
                table_result['self_info_sensitive_info'] = list(result['self_info'].values())[0]
                table_result['feedback_total_sensitive_info'] = list(result['feedback_total'].values())[0]
                table_result['warning_report_total_sensitive_info'] = list(result['warning_report_total'].values())[0]
                table_result['xnr'] = xnr_user_no

            except:

                results_all['trend'][xnr_user_no][timestamp] = 0
                

                table_result['follow_group_sensitive_info'] = 0
                table_result['fans_group_sensitive_info'] = 0
                table_result['self_info_sensitive_info'] = 0
                table_result['feedback_total_sensitive_info'] = 0
                table_result['warning_report_total_sensitive_info'] = 0
                table_result['xnr'] = xnr_user_no

        else:

            try:
                results_all['trend'][xnr_user_no][timestamp] = compute_safe_num(xnr_user_no)
                
                result = get_safe_active_today(xnr_user_no)
                xnr_result = create_xnr_history_info_count_today(xnr_user_no)

<<<<<<< HEAD
                today_total = list(result.values())[0]
                today_daily_post_num = xnr_result['daily_post_num']
                today_hot_follower_num = xnr_result['hot_follower_num']
                today_business_post_num = xnr_result['business_post_num']
                today_trace_follow_tweet_num = xnr_result['trace_follow_tweet_num']

                history_result = get_safe_history_count(timestamp,timestamp_start,xnr_user_no)
                #print 'history_result..',history_result
                history_total = history_result['total_post_sum']
                history_daily_post_num = history_result['daily_post_num']
                history_hot_follower_num = history_result['business_post_num']
                history_business_post_num = history_result['hot_follower_num']
                history_trace_follow_tweet_num = history_result['trace_follow_tweet_num']

                table_result['total_post_sum'] = history_total + today_total
                table_result['daily_post_num'] = history_daily_post_num + today_daily_post_num
                table_result['hot_follower_num'] = history_hot_follower_num + today_hot_follower_num
                table_result['business_post_num'] = history_business_post_num + today_business_post_num
                table_result['trace_follow_tweet_num'] = history_trace_follow_tweet_num + today_trace_follow_tweet_num

                table_result['other'] = table_result['total_post_sum'] - table_result['daily_post_num'] - table_result['hot_follower_num'] - table_result['business_post_num'] - xnr_result['trace_follow_tweet_num']
=======
                table_result['total_post_sum'] = list(result.values())[0]
                table_result['daily_post_num'] = xnr_result['daily_post_num']
                table_result['hot_follower_num'] = xnr_result['hot_follower_num']
                table_result['business_post_num'] = xnr_result['business_post_num']
                table_result['trace_follow_tweet_num'] = xnr_result['trace_follow_tweet_num']
                table_result['other'] = list(result.values())[0] - xnr_result['daily_post_num'] - xnr_result['hot_follower_num'] - xnr_result['business_post_num'] - xnr_result['trace_follow_tweet_num']
>>>>>>> 8c15462c1341ac4b21c690562f79c749fedb5791
                table_result['xnr'] = xnr_user_no

            except:

                results_all['trend'][xnr_user_no][timestamp] = 0

                table_result['total_post_sum'] = 0
                table_result['daily_post_num'] = 0
                table_result['hot_follower_num'] = 0
                table_result['business_post_num'] = 0
                table_result['trace_follow_tweet_num'] = 0
                table_result['other'] = 0
                table_result['xnr'] = xnr_user_no

        results_all['table'].append(table_result)

    return results_all
