# -*-coding:utf-8-*-

import json
import time
from collections import Counter
import sys
reload(sys)
sys.path.append('../')
from global_utils import es_xnr as es
from global_utils import R_WEIBO_XNR_FANS_FOLLOWERS as r_fans_followers 
from global_utils import es_flow_text,es_user_portrait,es_user_profile,weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
                        weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
                        weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
                        weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                        flow_text_index_type,weibo_bci_index_name_pre,weibo_bci_index_type,\
                        flow_text_index_name_pre,\
                        portrait_index_name,portrait_index_type,\
                        weibo_xnr_assessment_index_name,weibo_xnr_assessment_index_type,\
                        weibo_xnr_index_name,weibo_xnr_index_type,xnr_flow_text_index_name_pre,\
                        xnr_flow_text_index_type,\
                        weibo_xnr_count_info_index_name,weibo_xnr_count_info_index_type
                        
from global_utils import r_fans_uid_list_datetime_pre,r_fans_count_datetime_xnr_pre,r_fans_search_xnr_pre,\
                r_followers_uid_list_datetime_pre,r_followers_count_datetime_xnr_pre,r_followers_search_xnr_pre

#from utils import xnr_user_no2uid,uid2nick_name_photo
from global_config import S_TYPE,S_DATE,S_UID,S_DATE_BCI
from time_utils import ts2datetime,datetime2ts,get_flow_text_index_list,get_xnr_flow_text_index_list,\
                        get_timeset_indexset_list
from parameter import WEEK,DAY,MAX_SEARCH_SIZE,PORTRAIT_UID_LIST,PORTRAI_UID,FOLLOWERS_TODAY,\
                        TOP_ASSESSMENT_NUM,ACTIVE_UID,TOP_WEIBOS_LIMIT


# 影响力粉丝数
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
    if S_TYPE == 'test':
        current_time = int(time.time())
        current_date = ts2datetime(current_time)
        timestamp = datetime2ts(current_date) - DAY

    #try:

    feedback_mark_at = get_pene_feedback_sensitive(xnr_user_no,'be_at')['sensitive_info'][timestamp]
    feedback_mark_retweet = get_pene_feedback_sensitive(xnr_user_no,'be_retweet')['sensitive_info'][timestamp]
    feedback_mark_comment = get_pene_feedback_sensitive(xnr_user_no,'be_comment')['sensitive_info'][timestamp]
    # except:
    #     feedback_mark_at = 0.0839
    #     feedback_mark_retweet = 0.1199
    #     feedback_mark_comment = 0.01311
    # try:
    #   report_management_mark_tweet = get_pene_warning_report_sensitive(xnr_user_no)['tweet'][timestamp]
    #   report_management_mark_event = get_pene_warning_report_sensitive(xnr_user_no)['event'][timestamp]
    # except:
    #   report_management_mark_tweet = 0
    #   report_management_mark_event = 0
    # pene_mark = 100*float(follow_group_mark+fans_group_mark+feedback_mark_at+feedback_mark_retweet+\
    #             feedback_mark_comment+report_management_mark_tweet+report_management_mark_event)/sensitive_value_top_avg
    pene_mark = 100 * float(feedback_mark_at+feedback_mark_retweet+feedback_mark_comment)/sensitive_value_top_avg
    pene_mark = round(pene_mark,2)

    return pene_mark

# def get_pene_feedback_sensitive(xnr_user_no,sort_item):
    
#     uid = xnr_user_no2uid(xnr_user_no)

#     if sort_item == 'be_at':
#         index_name_sort = weibo_feedback_at_index_name
#         index_type_sort = weibo_feedback_at_index_type
#     elif sort_item == 'be_retweet':
#         index_name_sort = weibo_feedback_retweet_index_name
#         index_type_sort = weibo_feedback_retweet_index_type
#     elif sort_item == 'be_comment':
#         index_name_sort = weibo_feedback_comment_index_name
#         index_type_sort = weibo_feedback_comment_index_type

#     # if S_TYPE == 'test':
#     #     current_time = datetime2ts(S_DATE)
#     # else:
#     #     current_time = time.time()
#     current_time = int(time.time())
#     current_date = ts2datetime(current_time)
#     current_time_new = datetime2ts(current_date)
    
#     feedback_sensitive_dict = {}
#     feedback_sensitive_dict['sensitive_info'] = {}
#     for i in range(WEEK): # WEEK=7
#         start_ts = current_time_new - (i+1)*DAY  # DAY=3600*24
#         end_ts = current_time_new - i*DAY 

#         query_body = {
#             'query':{
#                 'bool':{
#                     'must':[
#                         {'term':{'root_uid':uid}},
#                         {'range':{'timestamp':{'gte':start_ts,'lt':end_ts}}}
#                     ]
#                 }
#             },
#             'aggs':{
#                 'avg_sensitive':{
#                     'avg':{
#                         'field':'sensitive_info'
#                     }
#                 }
#             }
#         }

#         es_sensitive_result = es.search(index=index_name_sort,doc_type=index_type_sort,body=query_body)['aggregations']

#         sensitive_value = es_sensitive_result['avg_sensitive']['value']

#         if sensitive_value == None:
#             sensitive_value = 0.0
#         feedback_sensitive_dict['sensitive_info'][start_ts] = sensitive_value

#     return feedback_sensitive_dict

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
    #for i in range(WEEK): # WEEK=7
    start_ts = current_time_new - DAY  # DAY=3600*24
    end_ts = current_time_new

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

# 安全性分数
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
    # print 'active_mark::',active_mark
    # print 'topic_mark:::',topic_mark
    # print 'domain_mark::',domain_mark

    safe_mark = float(active_mark+topic_mark+domain_mark)/3
    safe_mark = round(safe_mark*100,2)
    return safe_mark

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

def xnr_user_no2uid(xnr_user_no):
    try:
        result = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
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
        xnr_result=es_xnr.search(index=weibo_xnr_flow_text_name,doc_type=xnr_flow_text_index_type,body=query_body)
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
        #总发帖量
        xnr_user_detail['total_post_sum']=xnr_user_detail['daily_post_num']+xnr_user_detail['business_post_num']+xnr_user_detail['hot_follower_num']
    except:
        xnr_user_detail['user_fansnum']=0
        xnr_user_detail['daily_post_num']=0
        xnr_user_detail['business_post_num']=0
        xnr_user_detail['hot_follower_num']=0
        xnr_user_detail['total_post_sum']=0

    count_id=xnr_user_no+'_'+current_date
    xnr_user_detail['xnr_user_no']=xnr_user_no

    # try:
    #     es_xnr.index(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,body=xnr_user_detail,id=count_id)
    #     mark=xnr_user_detail
    # except:
    #     mark=dict()
    return xnr_user_detail

def cron_compute_mark():

    xnr_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,\
                body={'query':{'match_all':{}},'_source':['xnr_user_no'],'size':MAX_SEARCH_SIZE})['hits']['hits']
    
    if S_TYPE == 'test':
        xnr_results = [{'_source':{'xnr_user_no':'WXNR0004'}}]

    for result in xnr_results:
        xnr_user_no = result['_source']['xnr_user_no']
        #xnr_user_no = 'WXNR0004'
        influence = compute_influence_num(xnr_user_no)
        penetration = compute_penetration_num(xnr_user_no)
        safe = compute_safe_num(xnr_user_no)

        current_time = int(time.time())
        current_date = ts2datetime(current_time)
        current_time_new = datetime2ts(current_date)

        _id = xnr_user_no + '_' + current_date

        xnr_user_detail = create_xnr_history_info_count(xnr_user_no,current_date)

        #item = {}
        #xnr_user_detail['xnr_user_no'] = xnr_user_no
        xnr_user_detail['influence'] = influence
        xnr_user_detail['penetration'] = penetration
        xnr_user_detail['safe'] = safe
        #xnr_user_detail['date'] = current_date
        xnr_user_detail['timestamp'] = current_time_new

        # es.index(index=weibo_xnr_assessment_index_name,doc_type=weibo_xnr_assessment_index_type,\
        #     id=_id,body=item)

        try:

            es.index(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,\
                id=_id,body=xnr_user_detail)
            
            mark = True

        except:
            mark = False

        return mark

if __name__ == '__main__':

    cron_compute_mark()
    # es.delete(index=weibo_xnr_assessment_index_name,doc_type=weibo_xnr_assessment_index_type,\
    #     id='WXNR0004_2017-09-10')
