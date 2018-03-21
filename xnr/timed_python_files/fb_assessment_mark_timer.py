# -*-coding:utf-8-*-
import json
import time
import random
from collections import Counter
from elasticsearch.helpers import scan
import sys
reload(sys)
sys.path.append('../')
from global_utils import es_xnr as es
from global_utils import R_FACEBOOK_XNR_FANS_FOLLOWERS as r_fans_followers
from global_utils import facebook_feedback_comment_index_name,facebook_feedback_comment_index_type,\
                        facebook_feedback_retweet_index_name,facebook_feedback_retweet_index_type,\
                        facebook_feedback_at_index_name,facebook_feedback_at_index_type,\
                        facebook_feedback_like_index_name,facebook_feedback_like_index_type,\
                        fb_xnr_fans_followers_index_name as facebook_xnr_fans_followers_index_name,\
                        fb_xnr_fans_followers_index_type as facebook_xnr_fans_followers_index_type,\
                        facebook_flow_text_index_type as flow_text_index_type,\
                        fb_bci_index_name_pre as facebook_bci_index_name_pre,\
                        fb_bci_index_type as facebook_bci_index_type,\
                        facebook_flow_text_index_name_pre as flow_text_index_name_pre,\
                        facebook_feedback_private_index_name,facebook_feedback_private_index_type,\
                        facebook_report_management_index_name,facebook_report_management_index_type,\
                        fb_portrait_index_name as portrait_index_name,fb_portrait_index_type as portrait_index_type,\
                        facebook_xnr_assessment_index_name,facebook_xnr_assessment_index_type,\
                        fb_xnr_index_name as facebook_xnr_index_name,fb_xnr_index_type as facebook_xnr_index_type,\
                        fb_xnr_flow_text_index_name_pre as xnr_flow_text_index_name_pre,\
                        fb_xnr_flow_text_index_type as xnr_flow_text_index_type,\
                        facebook_xnr_count_info_index_name,facebook_xnr_count_info_index_type,\
                        facebook_feedback_retweet_index_name_pre, facebook_feedback_comment_index_name_pre,\
                        facebook_feedback_like_index_name_pre, facebook_feedback_at_index_name_pre,\
                        facebook_feedback_private_index_name_pre,facebook_report_management_index_name_pre
from global_utils import r_fb_fans_uid_list_datetime_pre as r_fans_uid_list_datetime_pre,\
                        r_fb_fans_count_datetime_xnr_pre as r_fans_count_datetime_xnr_pre,\
                        r_fb_fans_search_xnr_pre as r_fans_search_xnr_pre,\
                        r_fb_followers_uid_list_datetime_pre as r_followers_uid_list_datetime_pre,\
                        r_fb_followers_count_datetime_xnr_pre as r_followers_count_datetime_xnr_pre,\
                        r_fb_followers_search_xnr_pre as r_followers_search_xnr_pre
from global_config import S_TYPE,S_DATE_FB as S_DATE,S_UID_FB as S_UID,S_DATE_BCI_FB as S_DATE_BCI
from time_utils import ts2datetime,datetime2ts,fb_get_flow_text_index_list as get_flow_text_index_list,\
                        get_fb_xnr_flow_text_index_list as get_xnr_flow_text_index_list,\
                        get_timeset_indexset_list
from parameter import WEEK,DAY,MAX_SEARCH_SIZE,TOP_ASSESSMENT_NUM,TOP_WEIBOS_LIMIT,\
                    FB_PORTRAIT_UID_LIST as PORTRAIT_UID_LIST,FB_PORTRAI_UID as PORTRAI_UID
from time_utils import get_timeset_indexset_list




from parameter import WEEK,DAY,MAX_SEARCH_SIZE,FOLLOWERS_TODAY,\
                        TOP_ASSESSMENT_NUM,ACTIVE_UID


# 影响力粉丝数
def compute_influence_num(xnr_user_no,current_time_old):

    uid = xnr_user_no2uid(xnr_user_no)
    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
        uid = S_UID
    else:
        current_time = current_time_old

    datetime = ts2datetime(current_time)
    # new_datetime = datetime[0:4]+datetime[5:7]+datetime[8:10]
    index_name = facebook_bci_index_name_pre + datetime

    try:
        
        bci_xnr = es.get(index=index_name,doc_type=facebook_bci_index_type,id=uid)['_source']['influence']
        bci_max = es.search(index=index_name,doc_type=facebook_bci_index_type,body=\
            {'query':{'match_all':{}},'sort':{'influence':{'order':'desc'}}})['hits']['hits'][0]['_source']['influence']

        influence = float(bci_xnr)/bci_max*100
        influence = round(influence,2)  # 保留两位小数
    except Exception,e:
        print e
        influence = 0

    return influence

# 渗透力分数
def compute_penetration_num(xnr_user_no,current_time_old):

    # if S_TYPE == 'test':
    #     current_time = datetime2ts(S_DATE) - DAY
    # else:
    current_time = current_time_old
    
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

    top_sensitive_users = es.search(index=portrait_index_name,doc_type=portrait_index_type,\
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

    es_sensitive_result = es.search(index=index_name,doc_type=flow_text_index_type,\
        body=query_body_count)['aggregations']
    sensitive_value_top_avg = es_sensitive_result['avg_sensitive']['value']

    if S_TYPE == 'test':
        if not sensitive_value_top_avg:
            sensitive_value_top_avg = 1
    print 'es_sensitive_result::',es_sensitive_result
    # 计算xnr反馈群体的敏感度

    if S_TYPE == 'test':
        current_time = current_time_old
        current_date = ts2datetime(current_time)
        timestamp = datetime2ts(current_date)


    feedback_mark_at = get_pene_feedback_sensitive(xnr_user_no,'be_at',current_time)['sensitive_info']
    feedback_mark_retweet = get_pene_feedback_sensitive(xnr_user_no,'be_retweet',current_time)['sensitive_info']
    feedback_mark_comment = get_pene_feedback_sensitive(xnr_user_no,'be_comment',current_time)['sensitive_info']

    pene_mark = 100 * float(feedback_mark_at+feedback_mark_retweet+feedback_mark_comment)/sensitive_value_top_avg
    pene_mark = round(pene_mark,2)

    print 'pene_mark'
    print pene_mark
    return pene_mark

# 安全性分数
def compute_safe_num(xnr_user_no,current_time_old):
    # if S_TYPE == 'test':
    #     current_time = datetime2ts(S_DATE) - DAY
    # else:
    current_time = current_time_old

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
    top_active_users = es.search(index=portrait_index_name,doc_type=portrait_index_type,\
                body=query_body)['hits']['hits']
    
    # print 'top_active_users'
    # print top_active_users

    top_active_uid_list = []
    for user in top_active_users:
        user = user['_source']
        top_active_uid_list.append(user['uid'])

    print 'top_active_uid_list'
    print top_active_uid_list

    query_body_count = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':top_active_uid_list}
                }
            }
        }
    }
    print 'index_name'
    print index_name
    es_count_results = es.count(index=index_name,doc_type=flow_text_index_type,body=query_body_count)

    if es_count_results['_shards']['successful'] != 0:
       tweets_count = es_count_results['count']
       tweets_top_avg = float(tweets_count)/TOP_ASSESSMENT_NUM
    else:
        print 'es index rank error'
        tweets_top_avg = 0

    print 'tweets_top_avg'
    print tweets_top_avg

    # 当前虚拟人发博数量
    uid = xnr_user_no2uid(xnr_user_no)
    # if S_TYPE == 'test':
    #     uid = ACTIVE_UID
    print 'uid'
    print uid
    xnr_query_body_count = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'uid':uid}
                }
            }
        }
    }
    es_xnr_count_results = es.count(index=index_name,doc_type=flow_text_index_type,body=xnr_query_body_count)

    if es_xnr_count_results['_shards']['successful'] != 0:
       xnr_tweets_count = es_xnr_count_results['count']

    else:
        print 'es index rank error'
        xnr_tweets_count = 0
    try:
        active_mark = float(xnr_tweets_count)/tweets_top_avg
    except:
        active_mark = 0

    print 'active_mark'
    print active_mark

    ## 计算分数
    topic_distribute_dict = get_tweets_distribute(xnr_user_no)
    domain_distribute_dict = get_follow_group_distribute(xnr_user_no)

    topic_mark = topic_distribute_dict['mark']
    domain_mark = domain_distribute_dict['mark']

    safe_mark = float(active_mark+topic_mark+domain_mark)/3
    safe_mark = round(safe_mark*100,2)
    return safe_mark

def get_tweets_distribute(xnr_user_no):

    topic_distribute_dict = {}
    topic_distribute_dict['radar'] = {}

    uid = xnr_user_no2uid(xnr_user_no)

    if xnr_user_no:
        es_results = es.get(index=facebook_xnr_fans_followers_index_name,doc_type=facebook_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        followers_list = []
        if es_results.has_key('followers_list'):
            followers_list = es_results['followers_list']


    if S_TYPE == 'test':
        uid=PORTRAI_UID
        followers_list=PORTRAIT_UID_LIST

    # 关注者topic分布

    results = es.mget(index=portrait_index_name,doc_type=portrait_index_type,\
        body={'ids':followers_list})['docs']

    topic_list_followers = []

    for result in results:
        if result['found'] == True:
            result = result['_source']
            topic_string_first = result['topic_string'].split('&')
            topic_list_followers.extend(topic_string_first)

    topic_list_followers_count = Counter(topic_list_followers)

    print 'topic_list_followers_count'
    print topic_list_followers_count

    # 虚拟人topic分布
    try:
        xnr_results = es.get(index=portrait_index_name,doc_type=portrait_index_type,\
            id=uid)['_source']
        topic_string = xnr_results['topic_string'].split('&')
        topic_xnr_count = Counter(topic_string)
    except:
        topic_xnr_count = {}

    print 'topic_xnr_count'
    print topic_xnr_count

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
    print 'topic_distribute_dict'
    print topic_distribute_dict
    return topic_distribute_dict

def get_follow_group_distribute(xnr_user_no):
    
    domain_distribute_dict = {}
    domain_distribute_dict['radar'] = {}

    if S_TYPE == 'test':
        followers_list=PORTRAIT_UID_LIST
        followers_list_today = FOLLOWERS_TODAY
    else:
        # 获取所有关注者
        es_results = es.get(index=facebook_xnr_fans_followers_index_name,doc_type=facebook_xnr_fans_followers_index_type,\
                                id=xnr_user_no)["_source"]
        followers_list = es_results['followers_list']

        # 获取今日关注者
        current_time = int(time.time()-DAY)
        current_date = ts2datetime(current_time)
        r_uid_list_datetime_index_name = r_followers_uid_list_datetime_pre + current_date
        followers_results = r_fans_followers.hget(r_uid_list_datetime_index_name,xnr_user_no)
        followers_list_today = json.loads(followers_results)

    # 所有关注者领域分布

    results = es.mget(index=portrait_index_name,doc_type=portrait_index_type,\
        body={'ids':followers_list})['docs']
    
    domain_list_followers = []

    for result in results:
        if result['found'] == True:
            result = result['_source']
            domain_name = result['domain']
            domain_list_followers.append(domain_name)

    domain_list_followers_count = Counter(domain_list_followers)

    
    try:
        today_results = es.mget(index=portrait_index_name,doc_type=portrait_index_type,\
            body={'ids':followers_list_today})['docs']

        print 'today_results'
        print today_results

        domain_list_followers_today = []

        for result in today_results:
            if result['found'] == True:
                result = result['_source']
                domain_name = result['domain']
                domain_list_followers_today.append(domain_name)

        domain_list_followers_today_count = Counter(domain_list_followers_today)

    except Exception,e:
        print e
        domain_list_followers_today_count = {}


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

def xnr_user_no2uid(xnr_user_no):
    try:
        result = es.get(index=facebook_xnr_index_name,doc_type=facebook_xnr_index_type,id=xnr_user_no)['_source']
        uid = result['uid']
    except:
        uid = ''
    return uid

def uid2nick_name_photo(uid):
    uname_photo_dict = {}
    try:
        user = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
        nick_name = user['nick_name']
        photo_url = user['photo_url']
    except:
        nick_name = ''
        photo_url = ''
        
    return nick_name,photo_url

#统计信息表
def create_xnr_history_info_count(xnr_user_no,current_date):
    #create_date=ts2datetime(create_time)
    facebook_xnr_flow_text_name=xnr_flow_text_index_name_pre+current_date

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
        xnr_result=es.search(index=facebook_xnr_flow_text_name,doc_type=xnr_flow_text_index_type,body=query_body)
    except Exception,e:
        xnr_result = []
        print e



    if xnr_result:
        #今日总粉丝数
        for item in xnr_result['hits']['hits']:
            xnr_user_detail['user_fansnum']=item['_source']['user_fansnum']
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

    if xnr_user_detail.has_key('user_fansnum'):
        pass
    else:
        xnr_user_detail['user_fansnum']=0
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

    xnr_user_detail['total_post_sum']=xnr_user_detail['daily_post_num']+xnr_user_detail['business_post_num']+xnr_user_detail['hot_follower_num']+xnr_user_detail['trace_follow_tweet_num']


    if xnr_user_detail['user_fansnum'] == 0:
        yesterday_date=ts2datetime(datetime2ts(current_date)-DAY)
        count_id=xnr_user_no+'_'+yesterday_date
        try:
            xnr_count_result=es.get(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,id=count_id)['_source']
            xnr_user_detail['user_fansnum']=xnr_count_result['user_fansnum']
        except Exception,e:
            print e
            xnr_user_detail['user_fansnum']=0
    else:
        pass
    xnr_user_detail['xnr_user_no']=xnr_user_no

    print 'xnr_user_detail'
    print xnr_user_detail

    return xnr_user_detail

## 影响力评估各指标
def get_influence_total_trend(xnr_user_no,current_time):

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

# 影响力粉丝数
def get_influ_fans_num(xnr_user_no,current_time):
    fans_dict = {}

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

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

    fans_dict['day_num'] = datetime_count
    fans_dict['total_num'] = datetime_total

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    try:
        get_result = es.get(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,id=_id_last_day)['_source']
        fans_total_num_last = get_result['fans_total_num']
    except Exception,e:
        print e
        fans_total_num_last = 0

    if not fans_total_num_last:
        fans_total_num_last = 1

    fans_dict['growth_rate'] = round(float(datetime_count)/fans_total_num_last,2)

    #total_dict = compute_growth_rate_total(fans_num_day,fans_num_total)

    return fans_dict

def get_influ_retweeted_num(xnr_user_no,current_time):

    retweet_dict = {}


    uid = xnr_user_no2uid(xnr_user_no)
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name_day = facebook_feedback_retweet_index_name_pre + current_date
    index_name_total = get_timeset_indexset_list(index_name_pre=facebook_feedback_retweet_index_name_pre,startdate=S_DATE,enddate=current_date)

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    # {'range':{'timestamp':{'gte':current_time_new,'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }

    query_body_total = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'range':{'timestamp':{'gte':0,'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }

    try:
        print 'index_name_day'
        print index_name_day
        es_day_count_result = es.count(index=index_name_day, doc_type=facebook_feedback_retweet_index_type,\
                    body=query_body_day,request_timeout=999999)
        if es_day_count_result['_shards']['successful'] != 0:
            es_day_count = es_day_count_result['count']
        else:
            return 'es_day_count_found_error'
    except Exception,e:
        print e
        es_day_count = 0


    try:
        print 'index_name_total'
        print index_name_total
        es_total_count_result = es.count(index=index_name_total,doc_type=facebook_feedback_retweet_index_type,\
                        body=query_body_total,request_timeout=999999)

        if es_total_count_result['_shards']['successful'] != 0:
            es_total_count = es_total_count_result['count']
        else:
            return 'es_total_count_found_error'
    except Exception,e:
        print e
        es_total_count = 0

    retweet_dict['day_num'] = es_day_count
    retweet_dict['total_num'] = es_total_count

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    try:
        get_result = es.get(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,id=_id_last_day)['_source']
        retweet_total_num_last = get_result['retweet_total_num']
    except Exception,e:
        print e
        retweet_total_num_last = 0
        
    if not retweet_total_num_last:
        retweet_total_num_last = 1

    retweet_dict['growth_rate'] = round(float(es_day_count)/retweet_total_num_last,2)

    print 'retweet_dict'
    print retweet_dict

    return retweet_dict

def get_influ_commented_num(xnr_user_no,current_time):
    # 收到的评论 comment_type : receive
    comment_dict = {}
    # commented_num_day = {}  # 每天增量统计
    # commented_num_total = {} # 截止到当天总量统计

    uid = xnr_user_no2uid(xnr_user_no)

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name_day = facebook_feedback_comment_index_name_pre + current_date
    index_name_total = get_timeset_indexset_list(index_name_pre=facebook_feedback_comment_index_name_pre,startdate=S_DATE,enddate=current_date)

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'comment_type':'receive'}},
                    # {'range':{'timestamp':{'gte':current_time_new,'lt':(current_time_new+DAY)}}}
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
                    # {'range':{'timestamp':{'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }

    es_day_count_result = es.count(index=index_name_day,doc_type=facebook_feedback_comment_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        return 'es_day_count_found_error'


    es_total_count_result = es.count(index=index_name_total,doc_type=facebook_feedback_comment_index_type,\
                    body=query_body_total,request_timeout=999999)

    if es_total_count_result['_shards']['successful'] != 0:
        es_total_count = es_total_count_result['count']
    else:
        return 'es_total_count_found_error'

    comment_dict['day_num'] = es_day_count
    comment_dict['total_num'] = es_total_count

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    try:
        get_result = es.get(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,id=_id_last_day)['_source']
        comment_total_num_last = get_result['comment_total_num']
        if not comment_total_num_last:
            comment_total_num_last = 1
    except Exception,e:
        print e
        comment_total_num_last = 1
    

    comment_dict['growth_rate'] = round(float(es_day_count)/comment_total_num_last,2)

    return comment_dict

def get_influ_like_num(xnr_user_no,current_time):

    like_dict = {}


    uid = xnr_user_no2uid(xnr_user_no)

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name_day = facebook_feedback_like_index_name_pre + current_date
    index_name_total = get_timeset_indexset_list(index_name_pre=facebook_feedback_like_index_name_pre,startdate=S_DATE,enddate=current_date)

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    # {'range':{'timestamp':{'gte':current_time_new,'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }
    
    query_body_total = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    # {'range':{'timestamp':{'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }

    es_day_count_result = es.count(index=index_name_day,doc_type=facebook_feedback_like_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        return 'es_day_count_found_error'

    es_total_count_result = es.count(index=index_name_total,doc_type=facebook_feedback_like_index_type,\
                    body=query_body_total,request_timeout=999999)

    if es_total_count_result['_shards']['successful'] != 0:
        es_total_count = es_total_count_result['count']
    else:
        return 'es_total_count_found_error'

    like_dict['day_num'] = es_day_count
    like_dict['total_num'] = es_total_count

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    try:
        get_result = es.get(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,id=_id_last_day)['_source']
        like_total_num_last = get_result['like_total_num']
        if not like_total_num_last:
            like_total_num_last = 1
    except Exception,e:
        print e
        like_total_num_last = 1
    like_dict['growth_rate'] = round(float(es_day_count)/like_total_num_last,2)

    return like_dict

def get_influ_at_num(xnr_user_no,current_time):
    at_dict = {}

    uid = xnr_user_no2uid(xnr_user_no)

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name_day = facebook_feedback_at_index_name_pre + current_date
    index_name_total = get_timeset_indexset_list(index_name_pre=facebook_feedback_at_index_name_pre,startdate=S_DATE,enddate=current_date)

    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    # {'range':{'timestamp':{'gte':current_time_new,'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }

    query_body_total = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    # {'range':{'timestamp':{'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }

    es_day_count_result = es.count(index=index_name_day,doc_type=facebook_feedback_at_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        return 'es_day_count_found_error'

    es_total_count_result = es.count(index=index_name_total,doc_type=facebook_feedback_at_index_type,\
                    body=query_body_total,request_timeout=999999)

    if es_total_count_result['_shards']['successful'] != 0:
        es_total_count = es_total_count_result['count']
    else:
        return 'es_total_count_found_error'

    at_dict['day_num'] = es_day_count
    at_dict['total_num'] = es_total_count

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day

    try:
        get_result = es.get(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,id=_id_last_day)['_source']
        at_total_num_last = get_result['at_total_num']

        if not at_total_num_last:
            at_total_num_last = 1
    except Exception,e:
        print e
        at_total_num_last = 1

    at_dict['growth_rate'] = round(float(es_day_count)/at_total_num_last,2)


    return at_dict

def get_influ_private_num(xnr_user_no,current_time):
    # 收到的私信 private_type : receive
    private_dict = {}

    uid = xnr_user_no2uid(xnr_user_no)


    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name_day = facebook_feedback_private_index_name_pre + current_date
    index_name_total = get_timeset_indexset_list(index_name_pre=facebook_feedback_private_index_name_pre,startdate=S_DATE,enddate=current_date)
    
    query_body_day = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    {'term':{'private_type':'receive'}},
                    # {'range':{'timestamp':{'gte':current_time_new,'lt':(current_time_new+DAY)}}}
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
                    # {'range':{'timestamp':{'lt':(current_time_new+DAY)}}}
                ]
            }
        }
    }

    es_day_count_result = es.count(index=index_name_day,doc_type=facebook_feedback_private_index_type,\
                    body=query_body_day,request_timeout=999999)

    if es_day_count_result['_shards']['successful'] != 0:
        es_day_count = es_day_count_result['count']
    else:
        return 'es_day_count_found_error'


    es_total_count_result = es.count(index=index_name_total,doc_type=facebook_feedback_private_index_type,\
                    body=query_body_total,request_timeout=999999)

    if es_total_count_result['_shards']['successful'] != 0:
        es_total_count = es_total_count_result['count']
    else:
        return 'es_total_count_found_error'

    private_dict['day_num'] = es_day_count
    private_dict['total_num'] = es_total_count

    last_day = ts2datetime(current_time_new - DAY)
    _id_last_day = xnr_user_no + '_' + last_day
    try:
        get_result = es.get(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,id=_id_last_day)['_source']
        private_total_num_last = get_result['private_total_num']

        if not private_total_num_last:
            private_total_num_last = 1
    except Exception,e:
        print e
        private_total_num_last = 1

    private_dict['growth_rate'] = round(float(es_day_count)/private_total_num_last,2)

    return private_dict


## 渗透力评估 各指标

def penetration_total(xnr_user_no,current_time):
    
    total_dict = {}


    follow_group = get_pene_follow_group_sensitive(xnr_user_no,current_time)
    fans_group = get_pene_fans_group_sensitive(xnr_user_no,current_time)
    self_info = get_pene_infor_sensitive(xnr_user_no,current_time)
    
    feedback_at = get_pene_feedback_sensitive(xnr_user_no,'be_at',current_time)
    feedback_retweet = get_pene_feedback_sensitive(xnr_user_no,'be_retweet',current_time)
    feedback_commet = get_pene_feedback_sensitive(xnr_user_no,'be_comment',current_time)

    feedback_total = {}

    feedback_total['sensitive_info'] = float(feedback_at['sensitive_info'] + \
        feedback_retweet['sensitive_info'] + feedback_commet['sensitive_info'])/3
    
    warning_report = get_pene_warning_report_sensitive(xnr_user_no,current_time)

    warning_report_total = round(float(warning_report['event']+ \
        warning_report['user'] + warning_report['tweet'])/3,2)


    total_dict['follow_group'] = follow_group['sensitive_info']
    total_dict['fans_group'] = fans_group['sensitive_info']
    total_dict['self_info'] = self_info['sensitive_info']
    total_dict['warning_report_total'] = warning_report_total
    total_dict['feedback_total'] = feedback_total['sensitive_info']

    return total_dict

def get_pene_follow_group_sensitive(xnr_user_no,current_time_old):

    #if xnr_user_no:
    es_results = es.get(index=facebook_xnr_fans_followers_index_name,doc_type=facebook_xnr_fans_followers_index_type,\
                            id=xnr_user_no)["_source"]
    followers_list = es_results['followers_list']

    
    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
    else:
        current_time = current_time_old
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name = flow_text_index_name_pre + current_date


    follow_group_sensitive = {}


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
    es_sensitive_result = es.search(index=index_name,doc_type=flow_text_index_type,\
        body=query_body_info)['aggregations']
    sensitive_value = round(es_sensitive_result['avg_sensitive']['value'],2)

    if sensitive_value == None:
        sensitive_value = 0.0
    follow_group_sensitive['sensitive_info'] = sensitive_value

    print 'follow_group_sensitive'
    print follow_group_sensitive
    return follow_group_sensitive

def get_pene_fans_group_sensitive(xnr_user_no,current_time_old):

    #if xnr_user_no:
    es_results = es.get(index=facebook_xnr_fans_followers_index_name,doc_type=facebook_xnr_fans_followers_index_type,\
                            id=xnr_user_no)["_source"]
    fans_list = es_results['fans_list']

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
    else:
        current_time = current_time_old
    
    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    index_name = flow_text_index_name_pre + current_date

    fans_group_sensitive = {}

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
    es_sensitive_result = es.search(index=index_name,doc_type=flow_text_index_type,\
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
    index_name = flow_text_index_name_pre + current_date

    my_info_sensitive = {}

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
    es_sensitive_result = es.search(index=index_name,doc_type=flow_text_index_type,\
        body=query_body_info)['aggregations']
    sensitive_value = es_sensitive_result['avg_sensitive']['value']

    if sensitive_value == None:
        sensitive_value = 0.0
    my_info_sensitive['sensitive_info'] = sensitive_value

    return my_info_sensitive

def get_pene_feedback_sensitive(xnr_user_no,sort_item,current_time_old):
    
    uid = xnr_user_no2uid(xnr_user_no)

    if sort_item == 'be_at':
        index_name_sort = facebook_feedback_at_index_name
        index_type_sort = facebook_feedback_at_index_type
    elif sort_item == 'be_retweet':
        index_name_sort = facebook_feedback_retweet_index_name
        index_type_sort = facebook_feedback_retweet_index_type
    elif sort_item == 'be_comment':
        index_name_sort = facebook_feedback_comment_index_name
        index_type_sort = facebook_feedback_comment_index_type

    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE_BCI)
    else:
        current_time = current_time_old

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)


    #到底用哪个时间？？？？
    index_name_sort = index_name_sort + '_' + ts2datetime(current_time_new)

    feedback_sensitive_dict = {}

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'root_uid':uid}},
                    # {'range':{'timestamp':{'gte':current_time_new,'lt':(current_time_new+DAY)}}}
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
    try:
        es_sensitive_result = es.search(index=index_name_sort,doc_type=index_type_sort,body=query_body)['aggregations']
        print 'index_name_sort'
        print index_name_sort
        print 'es_sensitive_result', es_sensitive_result

        sensitive_value = es_sensitive_result['avg_sensitive']['value']
        if sensitive_value == None:
            sensitive_value = 0.0
    except Exception,e:
        print e
        sensitive_value = 0.0


    feedback_sensitive_dict['sensitive_info'] = sensitive_value
    print 'feedback_sensitive_dict'
    print feedback_sensitive_dict
    return feedback_sensitive_dict

def get_pene_warning_report_sensitive(xnr_user_no,current_time_old):

    sensitive_report_dict = {}

    report_type_list = [u'人物',u'事件',u'言论']
    
    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
    else:
        current_time = current_time_old

    current_date = ts2datetime(current_time)
    current_time_new = datetime2ts(current_date)

    print 'current_date'
    print current_date
    print 'current_time_new'
    print current_time_new

    index_name = facebook_report_management_index_name_pre + current_date

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
                        {'range':{'report_time':{'gte':current_time_new,'lt':(current_time_new+DAY)}}}
                    ]
                }
            },
            'size':MAX_SEARCH_SIZE
            
        }
        try:
            es_sensitive_result = es.search(index=index_name,doc_type=facebook_report_management_index_type,\
                body=query_body)['hits']['hits']
        except Exception,e:
            print e
            es_sensitive_result = []

        if es_sensitive_result:    
            if report_type == u'事件':
                for result in es_sensitive_result:
                    result = result['_source']
                    report_content = json.loads(result['report_content'])
                    facebook_list = report_content['facebook_list']
                    for facebook in facebook_list:
                        mid_event_list.append(facebook['mid'])
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
                    facebook_list = report_content['facebook_list']
                    for facebook in facebook_list:
                        mid_tweet_list.append(facebook['mid'])

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

    es_result_event = es.search(index=index_name_list,doc_type=flow_text_index_type,\
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

    es_result_user = es.search(index=portrait_index_name,doc_type=portrait_index_type,\
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

    es_result_tweet = es.search(index=index_name_list,doc_type=flow_text_index_type,\
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

## 安全性评估 各指标


# main 函数
def cron_compute_mark(current_time):

    xnr_results = es.search(index=facebook_xnr_index_name,doc_type=facebook_xnr_index_type,\
                body={'query':{'match_all':{}},'_source':['xnr_user_no'],'size':MAX_SEARCH_SIZE})['hits']['hits']
    
    if S_TYPE == 'test':
        xnr_results = [{'_source':{'xnr_user_no':'FXNR0005'}}]
    start_time = int(time.time())
    for result in xnr_results:
        xnr_user_no = result['_source']['xnr_user_no']
        #xnr_user_no = 'FXNR0005'
        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        print 'start assessment....'
        influence = compute_influence_num(xnr_user_no,current_time)
        penetration = compute_penetration_num(xnr_user_no,current_time)
        safe = compute_safe_num(xnr_user_no,current_time)

        _id = xnr_user_no + '_' + current_date

        print 'start count......'
        xnr_user_detail = create_xnr_history_info_count(xnr_user_no,current_date)

        #item = {}
        #xnr_user_detail['xnr_user_no'] = xnr_user_no
        xnr_user_detail['influence'] = influence
        xnr_user_detail['penetration'] = penetration
        xnr_user_detail['safe'] = safe
        #xnr_user_detail['date'] = current_date
        xnr_user_detail['timestamp'] = current_time_new

        # 评估各指标
        ## 影响力
        print 'start influence.......'
        influ_total_dict = get_influence_total_trend(xnr_user_no,current_time)

        xnr_user_detail['fans_total_num'] = influ_total_dict['total_trend']['fans']
        xnr_user_detail['retweet_total_num'] = influ_total_dict['total_trend']['retweet']
        xnr_user_detail['comment_total_num'] = influ_total_dict['total_trend']['comment']
        xnr_user_detail['like_total_num'] = influ_total_dict['total_trend']['like']
        xnr_user_detail['at_total_num'] = influ_total_dict['total_trend']['at']
        xnr_user_detail['private_total_num'] = influ_total_dict['total_trend']['private']

        xnr_user_detail['fans_day_num'] = influ_total_dict['day_num']['fans']
        xnr_user_detail['retweet_day_num'] = influ_total_dict['day_num']['retweet']
        xnr_user_detail['comment_day_num'] = influ_total_dict['day_num']['comment']
        xnr_user_detail['like_day_num'] = influ_total_dict['day_num']['like']
        xnr_user_detail['at_day_num'] = influ_total_dict['day_num']['at']
        xnr_user_detail['private_day_num'] = influ_total_dict['day_num']['private']

        xnr_user_detail['fans_growth_rate'] = influ_total_dict['growth_rate']['fans']
        xnr_user_detail['retweet_growth_rate'] = influ_total_dict['growth_rate']['retweet']
        xnr_user_detail['comment_growth_rate'] = influ_total_dict['growth_rate']['comment']
        xnr_user_detail['like_growth_rate'] = influ_total_dict['growth_rate']['like']
        xnr_user_detail['at_growth_rate'] = influ_total_dict['growth_rate']['at']
        xnr_user_detail['private_growth_rate'] = influ_total_dict['growth_rate']['private'] 


        ## 渗透力
        print 'start penetration......'
        pene_total_dict = penetration_total(xnr_user_no,current_time)

        xnr_user_detail['follow_group_sensitive_info'] = pene_total_dict['follow_group']
        xnr_user_detail['fans_group_sensitive_info'] = pene_total_dict['fans_group']
        xnr_user_detail['self_info_sensitive_info'] = pene_total_dict['self_info']
        xnr_user_detail['warning_report_total_sensitive_info'] = pene_total_dict['warning_report_total']
        xnr_user_detail['feedback_total_sensitive_info'] = pene_total_dict['feedback_total']

        ## 安全性（同发帖量）
        end_time = int(time.time())
        print 'total time: ',end_time - start_time



        print 'xnr_user_detail', xnr_user_detail

        try:

            es.index(index=facebook_xnr_count_info_index_name,doc_type=facebook_xnr_count_info_index_type,\
                id=_id,body=xnr_user_detail)
            mark = True
        except Exception,e:
            print e
            mark = False
        return mark



    
if __name__ == '__main__':


    if S_TYPE == 'test':
        current_time = datetime2ts(S_DATE)
    else:
        current_time = int(time.time()-DAY)

    # current_time_now = int(time.time())
    # for i in range(11,-1,-1):

    #     current_time = current_time_now - i*24*3600
    #     print 'time......',time.strftime('%Y-%m-%d',time.localtime(current_time))

    cron_compute_mark(current_time)

