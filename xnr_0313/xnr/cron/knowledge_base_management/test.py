# -*-coding:utf-8-*-
import os
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect

from time_utils import ts2datetime,datetime2ts
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from parameters import MAX_DETECT_COUNT,MAX_FLOW_TEXT_DAYS,TOP_KEYWORDS_NUM,MAX_SEARCH_SIZE,SORT_FIELD,\
                        TOP_WEIBOS_LIMIT


from utils import split_city

import sys
reload(sys)
sys.path.append('../../')

from global_utils import r,weibo_target_domain_detect_queue_name,weibo_target_domain_analysis_queue_name,\
                        es_flow_text,flow_text_index_name_pre,flow_text_index_type
from global_utils import es_xnr,weibo_domain_index_name,weibo_domain_index_type,\
                        weibo_role_index_name,weibo_role_index_type

from global_utils import es_retweet, retweet_index_name_pre, retweet_index_type,\
                         be_retweet_index_name_pre, be_retweet_index_type
from global_utils import es_comment, comment_index_name_pre, comment_index_type,\
                         be_comment_index_name_pre, be_comment_index_type
from global_config import WEEK,DAY,R_BEGIN_TIME,S_TYPE,S_DATE_2

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
        item_exist = es_xnr.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id)['_source']
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
        es_xnr.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_exist})
    except Exception, e:
        item_exist = dict()
        item_exist['domain_pinyin'] = json.dumps(decect_task_information['domain_pinyin'])
        item_exist['domain_name'] = json.dumps(decect_task_information['domain_name'])
        item_exist['create_type'] = json.dumps(decect_task_information['create_type'])
        item_exist['create_time'] = decect_task_information['create_time']
        item_exist['submitter'] = json.dumps(decect_task_information['submitter'])
        item_exist['remark'] = json.dumps(decect_task_information['remark'])
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
        es_xnr.index(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body=item_exist)
    
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
        item_exist['domain_pinyin'] = json.dumps(decect_task_information['domain_pinyin'])
        item_exist['domain_name'] = json.dumps(decect_task_information['domain_name'])
        item_exist['create_type'] = json.dumps(decect_task_information['create_type'])
        item_exist['create_time'] = json.dumps(decect_task_information['create_time'])
        item_exist['submitter'] = json.dumps(decect_task_information['submitter'])
        item_exist['remark'] = json.dumps(decect_task_information['remark'])
        item_exist['role_distribute'] = json.dumps(group_results['role_distribute'])
        item_exist['top_keywords'] = json.dumps(group_results['top_keywords'])
        item_exist['political_side'] = json.dumps(group_results['political_side'])
        item_exist['topic_preference'] = json.dumps(group_results['topic_preference'])
        item_exist['compute_status'] = 2  # 存入群体描述
        es_xnr.index(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body=item_exist)
    
    mark = True

    return mark

## 保存角色分析结果

def save_role_feature_analysis(role_results,role_label,domain,role_id):
    mark = False

    try:
        item_exist = es_xnr.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id)['_source']
        item_exist['role_pinyin'] = role_id
        item_exist['role_name'] = role_label
        item_exist['domains'] = domain
        item_exist['personality'] = role_results['personality']
        item_exist['political_tendency'] = role_results['political_tendency']
        item_exist['geo'] = role_results['geo']
        item_exist['active_time'] = role_results['active_time']
        item_exist['day_post_num'] = role_results['day_post_num']

        es_xnr.update(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id,body={'doc':item_exist})
    
    except Exception, e:
        item_exist = dict()
        item_exist['role_pinyin'] = role_id
        item_exist['role_name'] = role_label
        item_exist['domains'] = domain
        item_exist['personality'] = role_results['personality']
        item_exist['political_tendency'] = role_results['political_tendency']
        item_exist['geo'] = role_results['geo']
        item_exist['active_time'] = role_results['active_time']
        item_exist['day_post_num'] = role_results['day_post_num']

        es_xnr.index(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id,body=item_exist)
        
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
    if RUN_TYPE == 0:
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
    for i in range(days_num):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        datetime_list.append(date_range_start_datetime)

    return datetime_list


### 渗透领域创建方式

### 根据关键词
# input：关键词，任务创建时间
# output：近期微博包含上述关键词的微博用户群体的画像数据
def detect_by_keywords(keywords,datetime_list):
    keyword_list = keywords
    group_uid_list = set()

    if datetime_list == []:
        return []
    keyword_query_list = []
    query_item = 'keywords_string'
    for datetime in datetime_list:
        flow_text_index_name = flow_text_index_name_pre + datetime
        nest_query_list = []
        for keyword in keyword_list:
            nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})
        keyword_query_list.append({'bool':{'should':nest_query_list}})

        flow_text_index_name = flow_text_index_name_pre + datetime
        count = MAX_DETECT_COUNT
        es_results = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                    body={'query':{'bool':{'must':keyword_query_list}},'size':count,'sort':[{'user_fansnum':{'order':'desc'}}]})['hits']['hits']
        
        for i in range(len(es_results)):

            uid = es_results[i]['_source']['uid']
            group_uid_list.add(uid)

        

        return group_uid_list



### 根据种子用户
# input：种子用户uid，任务创建时间
# output：近期与种子用户有转发和评论关系的微博用户群体的画像数据

def detect_by_seed_users(seed_users):
    retweet_mark == 1
    comment_mark == 1

    group_uid_list = []
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
        r.lpush(weibo_target_domain_detect_queue_name,json.dumps(decect_task_information))
    except:
        status = False

    return status


def political_classify_sort(uids_list,uid_weibo_keywords_dict):

    political_side_results = political_classify(uids_list,uid_weibo_keywords_dict)
    political_side_list = political_side_results.values()
    political_side_set = set(political_side_list)
    political_side_count = dict()
    for side in political_side_set:
        side_count = political_side_list.count(side)
        political_side_count[side] = side_count
    political_side_count_sort = sorted(political_side_count.items(),key=lambda x:x[1], reverse=True)

    return political_side_count_sort 

def topic_classfiy_sort(uids_list,uid_weibo_keywords_dict):

    result_data,uid_topic = topic_classfiy(uids_list,uid_weibo_keywords_dict)

    topic_list = []
    for uid,topic in uid_topic.iteritems():
        topic_list = topic_list + topic
    topic_count_dict = dict()
    topic_set = set(topic_list)
    for topic in topic_set:
        topic_count = topic_list.count(topic)
        topic_count_dict[topic] = topic_count
    topic_count_dict_sort = sorted(topic_count_dict.items(),key=lambda x:x[1],reverse=True)

    return topic_count_dict_sort

## 根据uids_list获取 分类器输入需要的字典，即 uid_keywords字典。
def uid_list_2_uid_keywords_dict(uids_list,datetime_list,label='other'):
    uid_weibo_keywords_dict = dict()
    keywords_dict_all_users = dict()
    uid_weibo = [] # [[uid1,text1,ts1],[uid2,text2,ts2],...]

    for datetime in datetime_list:
        flow_text_index_name = flow_text_index_name_pre + datetime
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
        es_weibo_results = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                                            body=query_body)['hits']['hits']
        print len(es_weibo_results)

        for i in range(len(es_weibo_results)):
            
            uid = es_weibo_results[i]['_source']['uid']
            keywords_dict = es_weibo_results[i]['_source']['keywords_dict']
            keywords_dict = json.loads(keywords_dict)

            if label == 'character':
                text = es_weibo_results[i]['_source']['text']
                timestamp = es_weibo_results[i]['_source']['timestamp']
                uid_weibo.append([uid,text,timestamp])
            
            ## 合并相同id的关键词字典
            if uid in uid_weibo_keywords_dict.keys():
                uid_weibo_keywords_dict[uid] = dict(Counter(uid_weibo_keywords_dict[uid])+Counter(keywords_dict))
            else:
                uid_weibo_keywords_dict[uid] = keywords_dict

            ## 合并所有用户的关键词字典
            keywords_dict_all_users = dict(Counter(keywords_dict_all_users)+Counter(keywords_dict))
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

    # political_side_count_sort格式： [(label1,num1),(label2,num2),...] 按num降序

    ## 群体常用关键词
    keywords_dict_all_users_sort = sorted(keywords_dict_all_users.items(),key=lambda x:x[1], reverse=True)[:TOP_KEYWORDS_NUM]

    ## 群体角色分布
    domain,r_domain = domain_classfiy(uids_list,uid_weibo_keywords_dict)
    role_list = r_domain.values()
    role_set = set(role_list)
    role_count_dict = dict()

    for role in role_set:
        role_count = role_list.count(role)
        role_count_dict[role] = role_count
    role_count_dict_sort = sorted(role_count_dict.items(),key=lambda x:x[1], reverse=True)

    role_uids_dict = dict()

    for uid, role in r_domain.iteritems():
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
    print 'group_description_analysis_results:::',group_description_analysis_results

    return group_description_analysis_results,role_uids_dict

## 提取地理位置信息

def cityTopic(flow_text_index_name,n_limit=TOP_WEIBOS_LIMIT):
    if flow_text_index_name and flow_text_index_name != '':

        geo_cityTopic_results = {}
        geo_cityTopic_results['geo_weibos'] = {}
        geo_cityTopic_results['geo_cityCount'] = {}
        
        province_dict = {}
        
        first_item = {}

        query_body = {   
            'query':{
                'match_all':{}
            },
            'sort':{SORT_FIELD:{"order":"desc"}},
            'size':n_limit
            }
        mtype_weibo = weibo_es.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
        #save_ws_results(topic, end_ts, during, n_limit, mtype_weibo)    
        #微博直接保存下来
        #if len(mtype_weibo) == 0:
        #    continue
        first_item = mtype_weibo[0]['_source']
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

    es_weibo_counts = es_flow_text.count(index=flow_text_index_name,doc_type=flow_text_index_type,\
                                body={'query':{'match_all':{}}})
    if es_weibo_counts['_shards']['successful'] != 0:
        weibo_counts = es_weibo_counts['count']
    else:
        print 'es_weibo_counts error'
        weibo_counts = 0
    print weibo_counts

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
    
    print len(es_uid_counts)

    print float(weibo_counts)/len(es_uid_counts)

def active_time_compute(datetime):
    flow_text_index_name = flow_text_index_name_pre+datetime
    query_body = {
        'query':{
            'match_all':{}
        },
        'aggs':{
            'hour_counts':{
                'date_histogram':{
                    'field':'timestamp',
                    'interval':'hour'
                }
            }
        }
    }


    active_hour_counts = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)\
                                            ['aggregations']['all_uids']['buckets']
    print active_hour_counts
    return active_hour_counts                                    


### 角色特征分析
## input: role_label, uids_list 
def role_feature_analysis(role_label, uids_list,datetime_list):

    role_feature_analysis_results = dict()

    uid_weibo_keywords_dict,keywords_dict_all_users,uid_weibo = uid_list_2_uid_keywords_dict(uids_list,datetime_list,label='character')
    
    ## 常用关键词
    keywords_dict_all_users_sort = sorted(keywords_dict_all_users.items(),key=lambda x:x[1], reverse=True)[:TOP_KEYWORDS_NUM]

    ## 政治倾向
    political_side_count_sort = political_classify_sort(uids_list,uid_weibo_keywords_dict)

    ## 话题偏好
    topic_count_dict_sort = topic_classfiy_sort(uids_list,uid_weibo_keywords_dict)

    ## 性格特征
    start_date = datetime_list[:1]
    end_date = datetime_list[0]
    flag = 1
    com_result = classify_sentiment(uids_list,uid_weibo,start_date,end_date,flag)

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
        geo_cityTopic_results_datetime = cityTopic(flow_text_index_name)
        geo_cityTopic_results[datetime] = geo_cityTopic_results_datetime
        province_set = province_set | geo_cityTopic_results_datetime.keys()  ## 求集合并集

    geo_cityTopic_results_merge = dict()

    for datetime,province_city_dict in geo_cityTopic_results.iteritems():
        for province in province_set:
            try:
                geo_cityTopic_results_merge = dict(Counter(geo_cityTopic_results_merge[province])+Counter(province_city_dict[province]))
            except:
                geo_cityTopic_results_merge[province] = province_city_dict[province]


    ## 日发帖量
    for datetime in datetime_list:
        day_post_num_datetime = day_post_num_compute(uids_list,datetime)



    ## 活跃时间
 
    role_feature_analysis_results['top_keywords'] = keywords_dict_all_users_sort
    role_feature_analysis_results['political_side'] = political_side_count_sort
    role_feature_analysis_results['topic_preference'] = topic_count_dict_sort
    role_feature_analysis_results['personality'] = character_result_dict_sort
    role_feature_analysis_results['geo'] = geo_cityTopic_results_merge


  
#use to get detect information from redis queue
#input: NULL
#output: task_information_dict (from redis queue---gruop_detect_task)
def get_detect_information():
    task_information_dict = {}
    try:
        task_information_string = r.rpop(weibo_target_domain_detect_queue_name)
    except:
        task_information_string = ''
    #test
    #r_group.rpush(group_detect_queue_name, task_information_string)
    if task_information_string:
        task_information_dict = json.loads(task_information_string)
    else:
        task_information_dict = {}

    return task_information_dict


def compute_domain_base():
    results = {}
    while True:
        decect_task_information = get_detect_information()
        print 'start!'
        if decect_task_information != {}:

            task_id = decect_task_information['domain_pinyin']
            domain = decect_task_information['domain_name']
            print task_id
            create_time = decect_task_information['create_time']
            if S_TYPE == 'test':
                create_time = datetime2ts(S_DATE_2)
            
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

            print 'step 1: 开始群体描述计算'

            group_results,role_uids_dict = group_description_analysis(detect_results,datetime_list)

            if group_results:
                print 'step 1: 保存群体描述分析结果'
                mark = save_group_description_results(group_results,decect_task_information)
                if mark == False:
                    status = add_task_2_queue(decect_task_information)

            print 'step 2: 开始角色分析计算'

            for role_label, uids_list in role_uids_dict.iteritems():
                role_id = task_id + role_label
                role_results = role_feature_analysis(role_label, uids_list,datetime_list)
                print 'step 2: 保存角色分析结果'
                mark = save_role_feature_analysis(role_results,role_label,domain,role_id)


        else:
            break
 


if __name__ == '__main__':
    print 'qqqq'
    #compute_domain_base()
    #active_time_compute('2016-11-20')
    uids_list = 
    day_post_num_compute(uids_list,'2016-11-20')

