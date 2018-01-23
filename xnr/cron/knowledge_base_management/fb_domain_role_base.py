# -*-coding:utf-8-*-
import os
import json
import time
import sys
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect


from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import sys
reload(sys)
sys.path.append('../../')
from global_utils import r,fb_target_domain_detect_queue_name,fb_target_domain_analysis_queue_name,\
                        es_xnr as es, es_xnr, facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
                        fb_domain_index_name, fb_domain_index_type
from parameter import MAX_DETECT_COUNT,MAX_FLOW_TEXT_DAYS
es_flow_text = es

sys.path.append('../../cron/trans/')
from trans import trans, simplified2traditional, traditional2simplified







## 引入各个分类器
from political.political_main import political_classify
from domain.test_domain_v2 import domain_classfiy
from topic.test_topic import topic_classfiy
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from character.test_ch_sentiment import classify_sentiment

from collections import Counter
import numpy as np

from utils import split_city



from parameter import MAX_DETECT_COUNT,MAX_FLOW_TEXT_DAYS,TOP_KEYWORDS_NUM,MAX_SEARCH_SIZE,SORT_FIELD,\
                        TOP_WEIBOS_LIMIT,topic_en2ch_dict,WEEK_TIME,DAY,DAY_HOURS,HOUR,SENTIMENT_DICT_NEW,\
                        WHITE_UID_PATH, WHITE_UID_FILE_NAME

from global_utils import r,weibo_target_domain_detect_queue_name,weibo_target_domain_analysis_queue_name,\
                        es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                        portrait_index_name,portrait_index_type
from global_utils import es_xnr,weibo_domain_index_name,weibo_domain_index_type,\
                        weibo_role_index_name,weibo_role_index_type

from global_utils import es_retweet, retweet_index_name_pre, retweet_index_type,\
                         be_retweet_index_name_pre, be_retweet_index_type
from global_utils import es_comment, comment_index_name_pre, comment_index_type,\
                         be_comment_index_name_pre, be_comment_index_type

from global_config import R_BEGIN_TIME,S_TYPE,S_DATE

from time_utils import get_flow_text_index_list,ts2datetime,datetime2ts

r_beigin_ts = datetime2ts(R_BEGIN_TIME)

'''
领域知识库计算

'''

#use to save detect results to es
#input: uid list (detect results)
#output: status (True/False)
def save_detect_results(detect_results, decect_task_information):
    mark = False
    task_id = decect_task_information['domain_pinyin']

    try:
        item_exist = es_xnr.get(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=task_id)['_source']
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
        es_xnr.update(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=task_id,body={'doc':item_exist})
    except Exception, e:
        item_exist = dict()
        item_exist['xnr_user_no'] = decect_task_information['xnr_user_no']
        item_exist['domain_pinyin'] = decect_task_information['domain_pinyin']
        item_exist['domain_name'] = decect_task_information['domain_name']
        item_exist['create_type'] = decect_task_information['create_type']
        item_exist['create_time'] = decect_task_information['create_time']
        item_exist['submitter'] = decect_task_information['submitter']
        item_exist['description'] = decect_task_information['description']
        item_exist['remark'] = decect_task_information['remark']
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
        es_xnr.index(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=task_id,body=item_exist)
    mark = True
    return mark

## 保存群体分析结果

def save_group_description_results(group_results,decect_task_information):
    mark = False   
    task_id = decect_task_information['domain_pinyin']

    try:
        item_exist = es_xnr.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id)['_source']
        item_exist['role_distribute'] = json.dumps(group_results['role_distribute'])
        item_exist['top_keywords'] = json.dumps(group_results['top_keywords'])
        item_exist['political_side'] = json.dumps(group_results['political_side'])
        item_exist['topic_preference'] = json.dumps(group_results['topic_preference'])
        item_exist['compute_status'] = 2  # 存入群体描述
        es_xnr.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_exist})
    except Exception, e:
        item_exist = dict()

        item_exist['xnr_user_no'] = decect_task_information['xnr_user_no']
        item_exist['domain_pinyin'] = decect_task_information['domain_pinyin']
        item_exist['domain_name'] = decect_task_information['domain_name']
        item_exist['create_type'] = decect_task_information['create_type']
        item_exist['create_time'] = decect_task_information['create_time']
        item_exist['submitter'] = decect_task_information['submitter']
        item_exist['description'] = decect_task_information['description']
        item_exist['remark'] = decect_task_information['remark']
        item_exist['role_distribute'] = json.dumps(group_results['role_distribute'])
        item_exist['top_keywords'] = json.dumps(group_results['top_keywords'])
        item_exist['political_side'] = json.dumps(group_results['political_side'])
        item_exist['topic_preference'] = json.dumps(group_results['topic_preference'])
        item_exist['compute_status'] = 2  # 存入群体描述
        es_xnr.index(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body=item_exist)
    
    mark = True

    return mark

## 保存角色分析结果

def save_role_feature_analysis(role_results,role_label,domain,role_id,task_id):
    mark = False

    try:
        item_exist = es_xnr.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id)['_source']
        item_exist['role_pinyin'] = role_id
        item_exist['role_name'] = role_label
        item_exist['domains'] = domain
        item_exist['personality'] = json.dumps(role_results['personality'])
        item_exist['political_side'] = json.dumps(role_results['political_side'])
        item_exist['geo'] = json.dumps(role_results['geo'])
        item_exist['active_time'] = json.dumps(list(role_results['active_time']))
        item_exist['day_post_num'] = json.dumps(list(role_results['day_post_num']))  
        item_exist['psy_feature'] = json.dumps(role_results['psy_feature'])
        item_exist['member_uids'] = json.dumps(role_results['member_uids'])

    
        es_xnr.update(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id,body={'doc':item_exist})
    	
    	item_domain = dict()
    	item_domain['compute_status'] = 3  # 存入角色分析结果
    	es_xnr.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_domain})
    
    except Exception, e:
        item_exist = dict()
        item_exist['role_pinyin'] = role_id
        item_exist['role_name'] = role_label
        item_exist['domains'] = domain
        item_exist['personality'] = json.dumps(role_results['personality'])
        item_exist['political_side'] = json.dumps(role_results['political_side'])
        item_exist['geo'] = json.dumps(role_results['geo'])
        item_exist['active_time'] = json.dumps(list(role_results['active_time']))
        item_exist['day_post_num'] = json.dumps(list(role_results['day_post_num']))
        item_exist['psy_feature'] = json.dumps(role_results['psy_feature'])
        item_exist['member_uids'] = json.dumps(role_results['member_uids'])
       
        es_xnr.index(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id,body=item_exist)
        
        item_domain = dict()
    	item_domain['compute_status'] = 3  # 存入角色分析结果
    	es_xnr.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_domain})
    
    mark =True

    return mark

#use to change detect task process proportion
#input: task_name, proportion
#output: status (True/False)
def change_process_proportion(task_id, proportion):
    mark = False
    try:
        task_exist_result = es_xnr.get(index=weibo_domain_index_name, doc_type=weibo_domain_index_type, id=task_id)['_source']
    except:
        task_exist_result = {}
        return 'task is not exist'
    if task_exist_result != {}:
        task_exist_result['compute_status'] = proportion
        es_xnr.update(index=weibo_domain_index_name, doc_type=weibo_domain_index_type, id=task_id, body={'doc':task_exist_result})
        mark = True

    return mark


#use to get retweet/be_retweet/comment/be_comment db_number
#input: timestamp
#output: db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) % 2 + 1
    #run_type
    if S_TYPE == 'test':
        db_number = 1
    return db_number

#use to merge dict
#input: dict1, dict2, dict3...
#output: merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    
    return _total

# 为了获得流数据库的后缀日期
## input: 任务创建时间
## output: 创建日期之前的一周 ['2016-11-22','',...]
def get_flow_text_datetime_list(date_range_end_ts):
    datetime_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        datetime_list.append(date_range_start_datetime)
    return datetime_list


### 渗透领域创建方式

### 根据关键词
# input：关键词，任务创建时间
# output：近期微博包含上述关键词的微博用户群体的画像数据
def detect_by_keywords(keywords,datetime_list):
    keywords_list = keywords

    group_uid_list = set()

    if datetime_list == []:
        return []
    
    flow_text_index_name_list = []
    for datetime in datetime_list:
        flow_text_index_name = facebook_flow_text_index_name_pre + datetime
        flow_text_index_name_list.append(flow_text_index_name)

    nest_query_list = []
    #文本中可能存在英文或者繁体字，所以都匹配一下
    en_keywords_list = trans(keywords_list, target_language='en')
    for i in range(len(keywords_list)):
        keyword = keywords_list[i]
        traditional_keyword = simplified2traditional(keyword)
        
        if len(en_keywords_list) == len(keywords_list): #确保翻译没出错
            en_keyword = en_keywords_list[i]
            nest_query_list.append({'wildcard':{'keywords_string':'*'+en_keyword+'*'}})
        
        nest_query_list.append({'wildcard':{'keywords_string':'*'+keyword+'*'}})
        nest_query_list.append({'wildcard':{'keywords_string':'*'+traditional_keyword+'*'}})

    count = MAX_DETECT_COUNT
    query_body = {
        'query':{
            'bool':{
                'should':nest_query_list,
            }
        },
        'size':count,
        'sort':[{'user_fansnum':{'order':'desc'}}]
    }
    es_results = es_flow_text.search(index=flow_text_index_name_list,doc_type=facebook_flow_text_index_type,\
                body=query_body)['hits']['hits']
    for i in range(len(es_results)):
        uid = es_results[i]['_source']['uid']
        group_uid_list.add(uid)
    group_uid_list = list(group_uid_list)
    return group_uid_list

### 根据种子用户
# input：种子用户uid，任务创建时间
# output：近期与种子用户有转发和评论关系的微博用户群体的画像数据

def detect_by_seed_users(seed_users):
    retweet_mark = 1
    comment_mark = 1

    group_uid_list = set()
    all_union_result_dict = {}
    #get retweet/comment es db_number
    now_ts = time.time()
    db_number = get_db_num(now_ts)

    #step1: mget retweet and be_retweet
    if retweet_mark == 1:
        retweet_index_name = retweet_index_name_pre + str(db_number)
        be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
        #mget retwet
        try:
            retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type, \
                                             body={'ids':seed_users}, _source=True)['docs']
        except:
            retweet_result = []
        #mget be_retweet
        try:
            be_retweet_result = es_retweet.mget(index=be_retweet_index_name, doc_type=be_retweet_type, \
                                                body={'ids':seed_users} ,_source=True)['docs']
        except:
            be_retweet_result = []
    #step2: mget comment and be_comment
    if comment_mark == 1:
        comment_index_name = comment_index_name_pre + str(db_number)
        be_comment_index_name = be_comment_index_name_pre + str(db_number)
        #mget comment
        try:
            comment_result = es_comment.mget(index=comment_index_name, doc_type=comment_index_type, \
                                             body={'ids':seed_users}, _source=True)['docs']
        except:
            comment_result = []
        #mget be_comment
        try:
            be_comment_result = es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type, \
                                            body={'ids':seed_users}, _source=True)['docs']
        except:
            be_comment_result = []
    
    #step3: union retweet/be_retweet/comment/be_comment result
    union_count = 0
    
    for iter_search_uid in seed_users:
        try:
            uid_retweet_dict = json.loads(retweet_result[union_count]['_source']['uid_retweet'])
        except:
            uid_retweet_dict = {}
        try:
            uid_be_retweet_dict = json.loads(be_retweet_result[union_count]['_source']['uid_be_retweet'])
        except:
            uid_be_retweet_dict = {}
        try:
            uid_comment_dict = json.loads(comment_result[union_count]['_source']['uid_comment'])
        except:
            uid_comment_dict = {}
        try:
            uid_be_comment_dict = json.loads(be_comment_result[union_count]['_source']['uid_be_comment'])
        except:
            uid_be_comment_dict = {}
        #union four type user set
        union_result = union_dict(uid_retweet_dict, uid_be_retweet_dict, uid_comment_dict, uid_be_comment_dict)
        all_union_result_dict[iter_search_uid] = union_result

   
    '''
    !!!! 有一个转化提取 
    从 all_union_result_dict   中提取 所有的uid
    '''
    for seeder_uid,inter_dict in all_union_result_dict.iteritems():
        for uid, inter_count in inter_dict.iteritems():
            group_uid_list.add(uid)

    group_uid_list = list(group_uid_list)

    return group_uid_list


### 根据所有输入用户
# input：所有用户uid
# output：微博用户群体的画像数据

def detect_by_all_users(all_users):
    ## 获取所有输入文件的uid

    return all_users
    ### 直接批量提取群体用户画像

#use to add task to redis queue when the task  detect process fail
#input: decect_task_information
#output: status
def add_task_2_queue(decect_task_information):
    status = True
    try:
        r.lpush(fb_target_domain_detect_queue_name,json.dumps(decect_task_information))
    except:
        status = False
    return status

def political_classify_sort(uids_list,uid_weibo_keywords_dict):

    political_side_results = political_classify(uids_list,uid_weibo_keywords_dict)
    political_side_list = political_side_results.values()
    #print 'political_side_list::::::::::',political_side_list
    political_side_set = ['mid','left','right']
    political_side_count = dict()
    for side in political_side_set:
    	try:
        	side_count = political_side_list.count(side)
        	political_side_count[side] = side_count
        except:
        	political_side_count[side] = 0

    political_side_count_sort = sorted(political_side_count.items(),key=lambda x:x[1], reverse=True)

    return political_side_count_sort 

def topic_classfiy_sort(uids_list,uid_weibo_keywords_dict):

    result_data,uid_topic = topic_classfiy(uids_list,uid_weibo_keywords_dict)
    #print 'uid_weibo_keywords_dict::::::',uid_weibo_keywords_dict
    #print 'uid_topic::::::',uid_topic

    topic_list = []
    for uid,topic in uid_topic.iteritems():
        topic_list = topic_list + topic
    topic_count_dict = dict()
    #topic_set = set(topic_list)
    topic_set = topic_en2ch_dict.keys()
    for topic in topic_set:
    	try:
        	topic_count = topic_list.count(topic)
        	topic_count_dict[topic] = topic_count
        except:
        	topic_count_dict[topic] = 0

    topic_count_dict_sort = sorted(topic_count_dict.items(),key=lambda x:x[1],reverse=True)

    return topic_count_dict_sort

## 根据uids_list获取 分类器输入需要的字典，即 uid_keywords字典。
def uid_list_2_uid_keywords_dict(uids_list,datetime_list,label='other'):
    uid_weibo_keywords_dict = dict()
    keywords_dict_all_users = dict()
    uid_weibo = [] # [[uid1,text1,ts1],[uid2,text2,ts2],...]

    for datetime in datetime_list:
        flow_text_index_name = facebook_flow_text_index_name_pre + datetime
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'terms':{
                            'uid':uids_list
                        }
                    }
                }
            },
            'size':MAX_SEARCH_SIZE
        }
        es_weibo_results = es_flow_text.search(index=flow_text_index_name,doc_type=facebook_flow_text_index_type,\
                                            body=query_body)['hits']['hits']
        print len(es_weibo_results)
        for i in range(len(es_weibo_results)):
            uid = es_weibo_results[i]['_source']['uid']
            keywords_dict = es_weibo_results[i]['_source']['keywords_dict']
            keywords_dict = json.loads(keywords_dict)
            if i % 1000 == 0:
                print i
            if label == 'character':
                text = es_weibo_results[i]['_source']['text']
                timestamp = es_weibo_results[i]['_source']['timestamp']
                uid_weibo.append([uid,text,timestamp])

#keywords需要进行转成简体中文的操作？
            ## 统计用户所有词频
            if uid in uid_weibo_keywords_dict.keys():
                for keyword, count in keywords_dict.iteritems():
                    if keyword in uid_weibo_keywords_dict[uid].keys():
                        uid_weibo_keywords_dict[uid][keyword] += count
                    else:
                        uid_weibo_keywords_dict[uid][keyword] = count
            else:
                uid_weibo_keywords_dict[uid] = keywords_dict

            ## 合并所有用户的关键词字典
            for keyword, count in keywords_dict.iteritems():
                try:
                    keywords_dict_all_users[keyword] += count
                except:
                    keywords_dict_all_users[keyword] = count

    if label == 'character':
        return uid_weibo_keywords_dict,keywords_dict_all_users,uid_weibo
    else:
        return uid_weibo_keywords_dict,keywords_dict_all_users

## 群体描述分析
## input: uids, flow_text后缀日期列表
## output: 群体描述分析结果 {'role_distribute'：[] , 'top_keywords':[], 'political_side':[], 'topic_preference':[]}
def group_description_analysis(detect_results,datetime_list):
    uids_list = detect_results  ## uid列表  ['uid1','uid2',...]
    group_description_analysis_results = dict()
    
    uid_weibo_keywords_dict,keywords_dict_all_users = uid_list_2_uid_keywords_dict(uids_list,datetime_list)
    ## 群体政治倾向
    political_side_count_sort = political_classify_sort(uids_list,uid_weibo_keywords_dict)
    print 'political_side_count_sort::::',political_side_count_sort


    ## 群体常用关键词
    keywords_dict_all_users_sort = sorted(keywords_dict_all_users.items(),key=lambda x:x[1], reverse=True)[:TOP_KEYWORDS_NUM]

    ## 群体角色分布
    
    r_domain = dict()

    domain,r_domain = domain_classfiy(uids_list,uid_weibo_keywords_dict)


    role_list = r_domain.values()
    #print 'r_domain::::::',r_domain
    role_set = set(role_list)
    role_count_dict = dict()

    for role in role_set:
        role_count = role_list.count(role)
        role_count_dict[role] = role_count
    role_count_dict_sort = sorted(role_count_dict.items(),key=lambda x:x[1], reverse=True)

    role_uids_dict = dict()

    for uid, role in r_domain.iteritems():
    	#print 'role::::',role
    	#print 'role_type:::::',type(role)
        try:
            role_uids_dict[role].append(uid)
        except:
            role_uids_dict[role] = [uid]

    ## 群体话题偏好
    topic_count_dict_sort = topic_classfiy_sort(uids_list,uid_weibo_keywords_dict)

    group_description_analysis_results['role_distribute'] = role_count_dict_sort
    group_description_analysis_results['top_keywords'] = keywords_dict_all_users_sort
    group_description_analysis_results['political_side'] = political_side_count_sort
    group_description_analysis_results['topic_preference'] = topic_count_dict_sort
    #print 'group_description_analysis_results:::',group_description_analysis_results

    return group_description_analysis_results,role_uids_dict


## 提取地理位置信息

def cityTopic(uids_list,flow_text_index_name,n_limit=TOP_WEIBOS_LIMIT):
    if flow_text_index_name and flow_text_index_name != '':

        geo_cityTopic_results = {}
        geo_cityTopic_results['geo_weibos'] = {}
        geo_cityTopic_results['geo_cityCount'] = {}
        
        province_dict = {}
        
        #first_item = {}

        query_body = {   
            'query':{
                'filtered':{
                    'filter':{
                        'terms':{
                            'uid':uids_list
                        }
                    }
                }
            },
            'sort':{SORT_FIELD:{"order":"desc"}},
            'size':n_limit
            }
        mtype_weibo = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
        #save_ws_results(topic, end_ts, during, n_limit, mtype_weibo)    
        #微博直接保存下来
        #if len(mtype_weibo) == 0:
        #    continue
        #first_item = mtype_weibo[0]['_source']
        #数每个地方的不同类型的数量
        
        for weibo in mtype_weibo:  #对于每条微博
            
            try:
                geo = weibo['_source']['geo'].encode('utf8')
            except:
                continue
            #print geo,type(geo)
            province,city = split_city(geo)
            #print province,city

            if province != 'unknown':
                try:
                    province_dict[province][city] += 1  
                except:
                    try:

                        province_dict[province][city] = 1
                    except:
                        province_dict[province] = {city:1}

                       
                try:
                    province_dict[province]['total'] += 1
                except:
                    try:
                        province_dict[province]['total'] = 1
                    except:
                        province_dict[province] = {'total': 1}
                    

        geo_cityTopic_results = province_dict
               
        return geo_cityTopic_results

def day_post_num_compute(uids_list,datetime):
    flow_text_index_name = flow_text_index_name_pre+datetime

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{
                        'uid':uids_list
                    }
                }
            }
        },
        'aggs':{
            'all_uids':{
                'terms':{
                    'field':'uid',
                    'size':MAX_SEARCH_SIZE
                }
            }
        }
    }

    es_uid_counts = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                    body=query_body)['aggregations']['all_uids']['buckets']
    uid_count_list = []  # 所有uid的日发帖量组成list
    for uid_count in es_uid_counts:
        uid_count_list.append(uid_count['doc_count'])

    uid_count_list_np = np.array(uid_count_list)
    day_post_median = np.median(uid_count_list_np)  ## 日发帖量的中位数

    return day_post_median


def active_time_compute(uids_list,datetime):
    flow_text_index_name = flow_text_index_name_pre+datetime

    start_ts = datetime2ts(datetime)
    day_hour_counts = []
    day_hours = DAY_HOURS
    for i in range(day_hours):

        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'terms':{'uid':uids_list}},
                        {'range':{'timestamp':{'gte':start_ts+i*HOUR,'lt':start_ts+(i+1)*HOUR}}}
                    ]        
                }
            }
        }

        active_hour_counts = es_flow_text.count(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)#\
        if active_hour_counts['_shards']['successful'] != 0:
           hour_counts = active_hour_counts['count']
        else:
            print 'es_weibo_counts error'
            hour_counts = 0
        day_hour_counts.append(hour_counts)                    
    # [21,32,213,42,...] 一维数组，24个元素
    return day_hour_counts                                   

def get_psy_feature_sort(uids_list,create_time):

    index_name_list = get_flow_text_index_list(create_time)

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{
                        'uid':uids_list
                    }
                }
            }
        },
        'aggs':{
            'sentiment_all':{
                'terms':{
                    'field':'sentiment',
                    'size':MAX_SEARCH_SIZE
                }
            }
        }
    }

    es_sentiment_counts = es_flow_text.search(index=index_name_list,doc_type=flow_text_index_type,\
                                body=query_body)['aggregations']['sentiment_all']['buckets']
    sentiment_dict = dict()

    for item in es_sentiment_counts:
        sen_no = item['key']
        sen_count = item['doc_count']
        sen_zh = SENTIMENT_DICT_NEW[sen_no]
        sentiment_dict[sen_zh] = sen_count

    sentiment_sort = sorted(sentiment_dict.items(),key=lambda x:x[1],reverse=True)
    
    return sentiment_sort 


### 角色特征分析
## input: role_label, uids_list 
def role_feature_analysis(role_label, uids_list,datetime_list,create_time):

    role_feature_analysis_results = dict()

    uid_weibo_keywords_dict,keywords_dict_all_users,uid_weibo = uid_list_2_uid_keywords_dict(uids_list,datetime_list,label='character')
    
    ## 常用关键词
    keywords_dict_all_users_sort = sorted(keywords_dict_all_users.items(),key=lambda x:x[1], reverse=True)[:TOP_KEYWORDS_NUM]

    ## 政治倾向
    political_side_count_sort = political_classify_sort(uids_list,uid_weibo_keywords_dict)

    ## 话题偏好
    topic_count_dict_sort = topic_classfiy_sort(uids_list,uid_weibo_keywords_dict)

    ## 心理特征

    psy_feature_sort = get_psy_feature_sort(uids_list,create_time)

    ## 性格特征
    start_date = datetime_list[-1]
    end_date = datetime_list[0]
    flag = 1
    print 'start_date::::',start_date
    print 'end_date::::',end_date
    com_result = classify_sentiment(uids_list,uid_weibo,start_date,end_date,flag)

    print 'com_result::::',com_result

    com_result_list = com_result.values()
    com_result_set = set(com_result_list)
    character_result_dict = dict()

    for character in com_result_set:
        character_count = com_result_list.count(character)
        character_result_dict[character] = character_count
    character_result_dict_sort = sorted(character_result_dict.items(),key=lambda x:x[1], reverse=True)

    ## 地理位置
    geo_cityTopic_results = dict()
    province_set = set()
    for datetime in datetime_list:
        flow_text_index_name = flow_text_index_name_pre + datetime
        geo_cityTopic_results_datetime = cityTopic(uids_list,flow_text_index_name)
        geo_cityTopic_results[datetime] = geo_cityTopic_results_datetime
        #province_set = province_set | geo_cityTopic_results_datetime.keys()  ## 求集合并集

    geo_cityTopic_results_merge = dict()

    for datetime,province_city_dict in geo_cityTopic_results.iteritems():
        '''
        for province in province_set:
            
            try:
                geo_cityTopic_results_merge = dict(Counter(geo_cityTopic_results_merge[province])+Counter(province_city_dict[province]))
                
            except:
                geo_cityTopic_results_merge[province] = province_city_dict[province]
        '''
        ## 利用for循环
        for province, city_dict in province_city_dict.iteritems():
            if province in geo_cityTopic_results_merge.keys():
                for city, count in city_dict.iteritems():
                    if city in geo_cityTopic_results_merge[province].keys():
                        geo_cityTopic_results_merge[province][city] += count
                    else:
                        geo_cityTopic_results_merge[province][city] = count

            else:
                geo_cityTopic_results_merge[province] = city_dict

    ## 日发帖量
    day_post_median_all = []
    for datetime in datetime_list:
        day_post_median = day_post_num_compute(uids_list,datetime)
        day_post_median_all.append(day_post_median)


    ## 活跃时间
    day_hour_counts_all = []
    for datetime in datetime_list:
        day_hour_counts = active_time_compute(uids_list,datetime)
        day_hour_counts_all.append(day_hour_counts)

    day_hour_counts_all_np = np.array(day_hour_counts_all)
    day_hour_counts_aver = np.mean(day_hour_counts_all_np,axis=0).astype(np.int)  ## 对二维数组按列求和

    day_hour_counts_aver_time = np.argsort(-day_hour_counts_aver)   ### np.argsort(-x)  按从大到小的数据的索引排列
 
    role_feature_analysis_results['top_keywords'] = keywords_dict_all_users_sort
    role_feature_analysis_results['political_side'] = political_side_count_sort
    role_feature_analysis_results['topic_preference'] = topic_count_dict_sort
    role_feature_analysis_results['personality'] = character_result_dict_sort
    role_feature_analysis_results['geo'] = geo_cityTopic_results_merge
    role_feature_analysis_results['day_post_num'] = day_post_median_all
    role_feature_analysis_results['active_time'] = day_hour_counts_aver
    role_feature_analysis_results['psy_feature'] = psy_feature_sort
    role_feature_analysis_results['member_uids'] = uids_list

    return role_feature_analysis_results

#use to get detect information from redis queue
#input: NULL
#output: task_information_dict (from redis queue---gruop_detect_task)
def get_detect_information():
    task_information_dict = {}
    try:
        task_information_string = r.rpop(fb_target_domain_detect_queue_name)
    except:
        task_information_string = ''
    if task_information_string:
        task_information_dict = json.loads(task_information_string)
    else:
        task_information_dict = {}
    return task_information_dict


def compute_domain_base():
    results = {}
    while True:
        decect_task_information = get_detect_information()
        print '领域知识库和角色知识库计算开始！'
        if decect_task_information != {}:
            task_id = decect_task_information['domain_pinyin']
            domain = decect_task_information['domain_name']
            create_time = decect_task_information['create_time']
            if S_TYPE == 'test':
                create_time = datetime2ts(S_DATE)
            
            datetime_list = get_flow_text_datetime_list(create_time)
            print 'datetime_list::',datetime_list
            print 'step 0:开始群体发现'
            create_type = json.loads(decect_task_information['create_type'])
            ## create_type ----- {'按关键词''by_keywords':[],'按种子用户''by_seed_users':[],'按所有用户''by_all_users':[]}
            if create_type['by_keywords']:
                keywords = create_type['by_keywords']
                detect_results = detect_by_keywords(keywords,datetime_list)
            elif create_type['by_seed_users']:
                seed_users = create_type['by_seed_users']
                detect_results = detect_by_seed_users(seed_users,datetime_list)
            elif create_type['by_all_users']:
                all_users = create_type['by_all_users']
                detect_results = detect_by_all_users(all_users)

            if detect_results:
                detect_results = list(detect_results)
                print 'step 0: 保存群体发现结果（uids）'
                mark = save_detect_results(detect_results,decect_task_information)
                if mark == False:
                    status = add_task_2_queue(decect_task_information)
            #print 'detect_results:::::::',detect_results
            print 'step 1: 开始群体描述计算'
            print 'detect_results:::',detect_results
            group_results,role_uids_dict = group_description_analysis(detect_results,datetime_list)
            print 'role_uids_dict:::::',role_uids_dict
            if group_results:
                print 'step 1: 保存群体描述分析结果'
                mark = save_group_description_results(group_results,decect_task_information)
                if mark == False:
                    status = add_task_2_queue(decect_task_information)

            print 'step 2: 开始角色分析计算'
            for role_label, uids_list in role_uids_dict.iteritems():
                role_id = task_id + '_' + role_label
                role_results = role_feature_analysis(role_label, uids_list,datetime_list,create_time)
                print 'step 2: 保存角色分析结果'
                #print role_results
                mark = save_role_feature_analysis(role_results,role_label,domain,role_id,task_id)

            print '领域知识库和角色知识库计算完毕！'


        else:
            break
 


if __name__ == '__main__':
    
    print 'start_time::',time.ctime()
    print 'start!'
    # compute_domain_base()
    print 'end_time::',time.ctime()