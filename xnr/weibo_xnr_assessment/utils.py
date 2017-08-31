# -*-coding:utf-8-*-

import json
import time
from collections import Counter
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
                        portrait_index_name,portrait_index_type,xnr_flow_text_index_type
                        
from global_utils import r_fans_uid_list_datetime_pre,r_fans_count_datetime_xnr_pre,r_fans_search_xnr_pre,\
                r_followers_uid_list_datetime_pre,r_followers_count_datetime_xnr_pre,r_followers_search_xnr_pre

from xnr.utils import xnr_user_no2uid,uid2nick_name_photo
from xnr.global_config import S_TYPE,S_DATE,S_UID,S_DATE_BCI
from xnr.time_utils import ts2datetime,datetime2ts,get_flow_text_index_list,get_xnr_flow_text_index_list
from xnr.parameter import WEEK,DAY,MAX_SEARCH_SIZE,PORTRAIT_UID_LIST,PORTRAI_UID,FOLLOWERS_TODAY,\
                        TOP_ASSESSMENT_NUM,ACTIVE_UID,TOP_WEIBOS_LIMIT

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
            total_dict['growth_rate'][timestamp] = float(day_num)/total_num_lastday
            total_dict['day_num'][timestamp] = day8_dict[timestamp]
            total_dict['total_num'][timestamp] = total8_dict[timestamp]
        except:
            continue
            #print '123123'

    return total_dict

# 影响力粉丝数
def get_influ_fans_num(xnr_user_no):
    
    fans_num_day = {}  # 每天增量统计
    fans_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)
    print 'uid:::',uid
    if xnr_user_no:
        if S_TYPE == 'test':
            es_results = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
                                body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
            current_time = es_results[0]['_source']['timestamp']
        
        else:
            current_time = time.time()
    
        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        # 以下为保证数据为最新一次抓取的，已经删除过的则不在最新抓取的数据里面
        es_update_result = es.search(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
                                body={'query':{'match_all':{}},'sort':{'timestamp':'desc'}})['hits']['hits']
        update_time = es_update_result[0]['_source']['update_time']
        print 'update_time:::',update_time
        for i in range(WEEK+1): # WEEK=7
            start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
            end_ts = current_time_new - i*DAY

            query_body_day = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'root_uid':uid}},
                            {'term':{'update_time':update_time}},
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
                            {'term':{'update_time':update_time}},
                            {'range':{'timestamp':{'lt':end_ts}}}
                        ]
                    }
                }
            }

            es_day_count_result = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
                            body=query_body_day,request_timeout=999999)
            print 'es_day_count_result::',es_day_count_result
            if es_day_count_result['_shards']['successful'] != 0:
                es_day_count = es_day_count_result['count']
            else:
                return 'es_day_count_found_error'
            
            es_total_count_result = es.count(index=weibo_feedback_fans_index_name,doc_type=weibo_feedback_fans_index_type,\
                            body=query_body_total,request_timeout=999999)

            if es_total_count_result['_shards']['successful'] != 0:
                es_total_count = es_total_count_result['count']
            else:
                return 'es_total_count_found_error'

            fans_num_day[start_ts] = es_day_count
            fans_num_total[start_ts] = es_total_count
            print 'fans_num_day::',fans_num_day
            print 'fans_num_total::',fans_num_total

        total_dict = compute_growth_rate_total(fans_num_day,fans_num_total)
        print 'total_dict::',total_dict
        return total_dict
    else:
        return ''

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
        if S_TYPE == 'test':
            es_results = es.search(index=weibo_feedback_retweet_index_name,doc_type=weibo_feedback_retweet_index_type,\
                                body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
            current_time = es_results[0]['_source']['timestamp']
        else:
            current_time = time.time()
    
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
        if S_TYPE == 'test':
            es_results = es.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
                                body={'query':{'term':{'comment_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
            current_time = es_results[0]['_source']['timestamp']
        else:
            current_time = time.time()
    
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
        if S_TYPE == 'test':
            es_results = es.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,\
                                body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
            current_time = es_results[0]['_source']['timestamp']
        else:
            current_time = time.time()
    
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
        if S_TYPE == 'test':
            es_results = es.search(index=weibo_feedback_at_index_name,doc_type=weibo_feedback_at_index_type,\
                                body={'query':{'match_all':{}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
            current_time = es_results[0]['_source']['timestamp']
        else:
            current_time = time.time()
    
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
        if S_TYPE == 'test':
            es_results = es.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,\
                                body={'query':{'term':{'private_type':'receive'}},'sort':{'timestamp':{'order':'desc'}}})['hits']['hits']
            current_time = es_results[0]['_source']['timestamp']
        else:
            current_time = time.time()
    
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

    uid = xnr_user_no2uid(xnr_user_no)


    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
        uid = S_UID
    else:
        current_time = int(time.time()) - DAY

    datetime = ts2datetime(current_time)
    new_datetime = datetime[0:4]+datetime[5:7]+datetime[8:10]
    index_name = weibo_bci_index_name_pre + new_datetime
    try:
        
        bci_xnr = es_user_portrait.get(index=index_name,doc_type=weibo_bci_index_type,id=uid)['_source']['user_index']

        bci_max = es_user_portrait.search(index=index_name,doc_type=weibo_bci_index_type,body=\
            {'query':{'match_all':{}},'sort':{'user_index':{'order':'desc'}}})['hits']['hits'][0]['_source']['user_index']

        influence = float(bci_xnr)/bci_max*100
        influence = round(influence,2)  # 保留两位小数
    except:
        influence = 0

    return influence

'''
渗透力
'''

# 渗透力分数
def compute_penetration_num(xnr_user_no):

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE) - DAY
    else:
        current_time = time.time() - DAY
    
    current_date = ts2datetime(current_time)
    timestamp = datetime2ts(current_date)

    # 找出top 敏感用户
    query_body = {
        'query':{
            'match_all':{}
        },
        'sort':{'sensitive':{'order':'desc'}},
        'size':TOP_ASSESSMENT_NUM
    }

    top_sensitive_users = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,\
                            body=query_body)['hits']['hits']
    top_sensitive_uid_list = []
    for user in top_sensitive_users:
        user = user['_source']
        top_sensitive_uid_list.append(user['uid'])

    # 计算top敏感用户的微博敏感度均值
    query_body_count = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':top_sensitive_uid_list}
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
    	index_name = get_flow_text_index_list(timestamp)
    else:
    	index_name = flow_text_index_name_pre + current_date

    es_sensitive_result = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,\
        body=query_body_count)['aggregations']
    sensitive_value_top_avg = es_sensitive_result['avg_sensitive']['value']

    if S_TYPE == 'test':
    	if not sensitive_value_top_avg:
    		sensitive_value_top_avg = 1
    print 'es_sensitive_result::',es_sensitive_result
    # 计算xnr反馈群体的敏感度
    

    #follow_group_mark = get_pene_follow_group_sensitive(xnr_user_no)['sensitive_info'][timestamp]
    #fans_group_mark = get_pene_fans_group_sensitive(xnr_user_no)['sensitive_info'][timestamp]
    try:
    	feedback_mark_at = get_pene_feedback_sensitive(xnr_user_no,'be_at')['sensitive_info'][timestamp]
    	feedback_mark_retweet = get_pene_feedback_sensitive(xnr_user_no,'be_retweet')['sensitive_info'][timestamp]
    	feedback_mark_comment = get_pene_feedback_sensitive(xnr_user_no,'be_comment')['sensitive_info'][timestamp]
    except:
    	feedback_mark_at = 0.0839
    	feedback_mark_retweet = 0.1199
    	feedback_mark_comment = 0.01311
    # try:
    # 	report_management_mark_tweet = get_pene_warning_report_sensitive(xnr_user_no)['tweet'][timestamp]
    # 	report_management_mark_event = get_pene_warning_report_sensitive(xnr_user_no)['event'][timestamp]
    # except:
    # 	report_management_mark_tweet = 0
    # 	report_management_mark_event = 0
    # pene_mark = 100*float(follow_group_mark+fans_group_mark+feedback_mark_at+feedback_mark_retweet+\
    #             feedback_mark_comment+report_management_mark_tweet+report_management_mark_event)/sensitive_value_top_avg
    pene_mark = 100 * float(feedback_mark_at+feedback_mark_retweet+feedback_mark_comment)/sensitive_value_top_avg
    pene_mark = round(pene_mark,2)

    return pene_mark

def get_pene_follow_group_sensitive(xnr_user_no):

    if xnr_user_no:
        es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        followers_list = es_results['followers_list']

    
    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
    else:
        current_time = time.time()
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    #current_time_new_8 = current_time_new - 8*DAY # 统计8天，计算增长率要用
    #current_date_new_8 = ts2datetime(current_time_new_8)

    index_name_list = get_flow_text_index_list(current_time_new)
    #index_name_8 = flow_text_index_name_pre + current_date_new_8
    #index_name_list.append(index_name_8)

    follow_group_sensitive = {}
    follow_group_sensitive['sensitive_info'] = {}
    #follow_group_sensitive['sensitive_user'] = {}

    for index_name in index_name_list:
        datetime = index_name[-10:]
        timestamp = datetime2ts(datetime)
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
        sensitive_value = es_sensitive_result['avg_sensitive']['value']
        
        if sensitive_value == None:
            sensitive_value = 0.0
        follow_group_sensitive['sensitive_info'][timestamp] = sensitive_value

    return follow_group_sensitive

def get_pene_fans_group_sensitive(xnr_user_no):

    if xnr_user_no:
        es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        fans_list = es_results['fans_list']

    
    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
    else:
        current_time = time.time()
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    index_name_list = get_flow_text_index_list(current_time_new)

    fans_group_sensitive = {}
    fans_group_sensitive['sensitive_info'] = {}

    for index_name in index_name_list:
        datetime = index_name[-10:]
        timestamp = datetime2ts(datetime)
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
        fans_group_sensitive['sensitive_info'][timestamp] = sensitive_value

    return fans_group_sensitive

def get_pene_infor_sensitive(xnr_user_no):
    
    uid = xnr_user_no2uid(xnr_user_no)

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
        uid = S_UID
    else:
        current_time = time.time()
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    index_name_list = get_flow_text_index_list(current_time_new)

    my_info_sensitive = {}
    my_info_sensitive['sensitive_info'] = {}

    for index_name in index_name_list:
        datetime = index_name[-10:]
        timestamp = datetime2ts(datetime)
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
        print 'sensitive_value::',sensitive_value
        if sensitive_value == None:
            sensitive_value = 0.0
        my_info_sensitive['sensitive_info'][timestamp] = sensitive_value

    return my_info_sensitive

def get_pene_feedback_sensitive(xnr_user_no,sort_item):
    
    uid = xnr_user_no2uid(xnr_user_no)

    if sort_item == 'be_at':
        index_name_sort = weibo_feedback_at_index_name
        index_type_sort = weibo_feedback_at_index_type
    elif sort_item == 'be_retweet':
        index_name_sort = weibo_feedback_retweet_index_name
        index_type_sort = weibo_feedback_retweet_index_type
    elif sort_item == 'be_comment':
        index_name_sort = weibo_feedback_comment_index_name
        index_type_sort = weibo_feedback_comment_index_type

    # if S_TYPE == 'test':
    #     current_time = datetime2ts(S_DATE)
    # else:
    #     current_time = time.time()
    current_time = int(time.time())
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)
    
    feedback_sensitive_dict = {}
    feedback_sensitive_dict['sensitive_info'] = {}
    for i in range(WEEK): # WEEK=7
        start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
        end_ts = current_time_new - i*DAY 

        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'root_uid':uid}},
                        {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
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
        feedback_sensitive_dict['sensitive_info'][start_ts] = sensitive_value

    return feedback_sensitive_dict

def get_pene_warning_report_sensitive(xnr_user_no):

    sensitive_report_dict = {}
    sensitive_report_dict['event'] = {}
    sensitive_report_dict['user'] = {}
    sensitive_report_dict['tweet'] = {}

    report_type_list = [u'人物',u'事件',u'言论']
    

    if S_TYPE == 'test':
        es_time_result = es.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,\
                        body={'query':{'match_all':{}},'sort':{'report_time':{'order':'desc'}}})['hits']['hits']

        current_time = es_time_result[0]['_source']['report_time']
    else:
        current_time = int(time.time())

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    for i in range(WEEK): # WEEK=7
        start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
        end_ts = current_time_new - i*DAY

        mid_event_list = []
        mid_tweet_list = []
        uid_list = []

        for report_type in report_type_list:
            query_body = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no}},
                            {'term':{'report_type':report_type}},
                            {'range':{'report_time':{'gte':start_ts,'lt':end_ts}}}
                        ]
                    }
                },
                'size':MAX_SEARCH_SIZE
                
            }

            es_sensitive_result = es.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,\
                body=query_body)['hits']['hits']

            if es_sensitive_result:    
                if report_type == u'事件':
                    for result in es_sensitive_result:
                        result = result['_source']
                        report_content = json.loads(result['report_content'])
                        weibo_list = report_content['weibo_list']
                        for weibo in weibo_list:
                            mid_event_list.append(weibo['mid'])
                elif report_content == u'人物':
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

        sensitive_report_dict['event'][start_ts] = event_sensitive_avg
        sensitive_report_dict['user'][start_ts] = user_sensitive_avg
        sensitive_report_dict['tweet'][start_ts] = tweet_sensitive_avg

    return sensitive_report_dict


def compute_safe_num(xnr_user_no):
    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE) - DAY
    else:
        current_time = int(time.time()-DAY)

    current_date = ts2datetime(current_time)

    index_name = flow_text_index_name_pre + current_date

    # top100活跃用户平均发博数量
    query_body = {
        'query':{
            'match_all':{}
        },
        'sort':{'activeness':{'order':'desc'}},
        'size':TOP_ASSESSMENT_NUM
    }
    top_active_users = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,\
                body=query_body)['hits']['hits']
    top_active_uid_list = []
    for user in top_active_users:
        user = user['_source']
        top_active_uid_list.append(user['uid'])

    query_body_count = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':top_active_uid_list}
                }
            }
        }
    }
    es_count_results = es_flow_text.count(index=index_name,doc_type=flow_text_index_type,body=query_body_count)

    if es_count_results['_shards']['successful'] != 0:
       tweets_count = es_count_results['count']
       tweets_top_avg = float(tweets_count)/TOP_ASSESSMENT_NUM
    else:
        print 'es index rank error'
        tweets_top_avg = 0

    # 当前虚拟人发博数量
    uid = xnr_user_no2uid(xnr_user_no)
    if S_TYPE == 'test':
        uid = ACTIVE_UID
    xnr_query_body_count = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'uid':uid}
                }
            }
        }
    }
    es_xnr_count_results = es_flow_text.count(index=index_name,doc_type=flow_text_index_type,body=xnr_query_body_count)

    if es_xnr_count_results['_shards']['successful'] != 0:
       xnr_tweets_count = es_xnr_count_results['count']

    else:
        print 'es index rank error'
        xnr_tweets_count = 0
    try:
        active_mark = float(xnr_tweets_count)/tweets_top_avg
    except:
        active_mark = 0

    ## 计算分数
    topic_distribute_dict = get_tweets_distribute(xnr_user_no)
    domain_distribute_dict = get_follow_group_distribute(xnr_user_no)

    topic_mark = topic_distribute_dict['mark']
    domain_mark = domain_distribute_dict['mark']
    print 'active_mark::',active_mark
    print 'topic_mark:::',topic_mark
    print 'domain_mark::',domain_mark

    safe_mark = float(active_mark+topic_mark+domain_mark)/3
    safe_mark = round(safe_mark*100,2)
    return safe_mark

def get_safe_active(xnr_user_no):

    uid = xnr_user_no2uid(xnr_user_no)

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
        uid = S_UID
    else:
        current_time = time.time()
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name_list = get_flow_text_index_list(current_time_new)

    safe_active_dict = {}

    for index_name in index_name_list:

        datetime = index_name[-10:]
        timestamp = datetime2ts(datetime)

        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'term':{'uid':uid}
                    }
                }
            }
        }

        results = es_flow_text.count(index=index_name,doc_type=flow_text_index_type,\
                            body=query_body,request_timeout=999999)

        if results['_shards']['successful'] != 0:
            es_day_count = results['count']
        else:
            return 'es_day_count_found_error'

        safe_active_dict[timestamp] = es_day_count
    
    return safe_active_dict

def get_tweets_distribute(xnr_user_no):

    topic_distribute_dict = {}
    topic_distribute_dict['radar'] = {}

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        followers_list = es_results['followers_list']

    if S_TYPE == 'test':
        uid=PORTRAI_UID
        followers_list=PORTRAIT_UID_LIST

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
    try:
        xnr_results = es_user_portrait.get(index=portrait_index_name,doc_type=portrait_index_type,\
            id=uid)['_source']
        topic_string = xnr_results['topic_string'].split('&')
        topic_xnr_count = Counter(topic_string)
        #topic_distribute_dict['topic_xnr'] = topic_xnr_count

    except:
        topic_xnr_count = {}
        #topic_distribute_dict['topic_xnr'] = topic_xnr_count

    # 整理雷达图数据
    # if topic_xnr_count:
    #     for topic, value in topic_xnr_count.iteritems():
    #         try:
    #             topic_value = float(value)/(topic_list_followers_count[topic])
    #         except:
    #             continue
    #         topic_distribute_dict['radar'][topic] = topic_value
    if topic_xnr_count:
        for topic, value in topic_list_followers_count.iteritems():
            try:
                topic_value = float(topic_xnr_count[topic])/value
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
                print topic 
                print mark
            except:
                continue
    topic_distribute_dict['mark'] = mark

    return topic_distribute_dict


def get_safe_tweets(xnr_user_no,topic,sort_item):

    if S_TYPE == 'test':

        current_time = datetime2ts(S_DATE)
        index_name_list = get_flow_text_index_list(current_time)
        query_body = {
            'query':{
                'match_all':{}
            },
            'size':TOP_WEIBOS_LIMIT,
            'sort':{sort_item:{'order':'desc'}}
        }

        es_results = es_flow_text.search(index=index_name_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    
    else:
        current_time = int(time.time())

        index_name_list = get_xnr_flow_text_index_list(current_time)

        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'topic_first':topic}},
                        {'term':{'xnr_user_no':xnr_user_no}}
                    ]
                }
            },
            'size':TOP_WEIBOS_LIMIT,
            'sort':{sort_item:{'order':'desc'}}
        }

        es_results = es.search(index=index_name_list,doc_type=xnr_flow_text_index_type,body=query_body)['hits']['hits']

    results_all = []
    for result in es_results:
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

    if S_TYPE == 'test':
        followers_list=PORTRAIT_UID_LIST
        followers_list_today = FOLLOWERS_TODAY
    else:
        # 获取所有关注者
        es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        followers_list = es_results['followers_list']

        # 获取今日关注者
        current_time = int(time.time()-DAY)
        current_date = ts2datetime(current_time)
        r_uid_list_datetime_index_name = r_followers_uid_list_datetime_pre + current_date
        followers_results = r_fans_followers.hget(r_uid_list_datetime_index_name,xnr_user_no)
        followers_list_today = json.loads(followers_results)

    # 所有关注者领域分布

    results = es_user_portrait.mget(index=portrait_index_name,doc_type=portrait_index_type,\
        body={'ids':followers_list})['docs']
    
    domain_list_followers = []

    for result in results:
        if result['found'] == True:
            result = result['_source']
            domain_name = result['domain']
            domain_list_followers.append(domain_name)

    domain_list_followers_count = Counter(domain_list_followers)

    #domain_distribute_dict['domain_follower'] = domain_list_followers_count
    
    # 今日关注者
    
    try:
        today_results = es_user_portrait.mget(index=portrait_index_name,doc_type=portrait_index_type,\
            body={'ids':followers_list_today})['docs']

        domain_list_followers_today = []

        for result in today_results:
            if result['found'] == True:
                result = result['_source']
                domain_name = result['domain']
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

    if domain_list_followers_today_count:
        for domain, value in domain_list_followers_today_count.iteritems():
            try:
                domain_value = float(domain_list_followers_today_count[domain])/value
            except:
                continue
            domain_distribute_dict['radar'][domain] = domain_value

    # 整理仪表盘数据
    mark = 0
    print 'domain_list_followers_today_count::',domain_list_followers_today_count
    print 'domain_distribute_dict::',domain_distribute_dict
    if domain_list_followers_today_count:
        n_domain = len(domain_list_followers_count.keys())
        for domain,value in domain_list_followers_today_count.iteritems():
            try:
                mark += float(value)/(domain_list_followers_count[domain]*n_domain)
            except:
                continue
    domain_distribute_dict['mark'] = mark

    return domain_distribute_dict

def get_follow_group_tweets(xnr_user_no,domain,sort_item):

    if S_TYPE == 'test':
        followers_list=PORTRAIT_UID_LIST
        current_time = datetime2ts(S_DATE)

        index_name_list = get_flow_text_index_list(current_time)
        query_body = {
            'query':{
                'match_all':{}
            },
            'size':TOP_WEIBOS_LIMIT,
            'sort':{sort_item:{'order':'desc'}}
        }

        flow_text_results = es_flow_text.search(index=index_name_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

    else:
        current_time = int(time.time())
        # 获取所有关注者
        es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        followers_list = es_results['followers_list']

        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'terms':{'uid':followers_list}},
                        {'term':{'domain':domain}}
                    ]
                }
            },
            'size':MAX_SEARCH_SIZE
        }

        followers_results = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,body=query_body)['hits']['hits']
        followers_domain_show_uid_list = []
        if followers_results:
            for follower in followers_results:
                follower = follower['_source']
                followers_domain_show_uid_list.append(follower['uid'])


        index_name_list = get_flow_text_index_list(current_time)

        query_body_flow_text = {
            'query':{
                'filtered':{
                    'filter':{
                        'terms':{'uid':followers_domain_show_uid_list}
                    }
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



