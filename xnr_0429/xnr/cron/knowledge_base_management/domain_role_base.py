# -*-coding:utf-8-*-
import os
import json
import time
import gensim
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect


from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

## 引入各个分类器

from political.political_main import political_classify
from domain.test_domain_v2 import domain_classfiy
from topic.test_topic import topic_classfiy
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from character.test_ch_sentiment import classify_sentiment

from collections import Counter
import numpy as np

from utils import split_city

import sys
reload(sys)
sys.path.append('../../')

from parameter import MAX_DETECT_COUNT,MAX_FLOW_TEXT_DAYS,TOP_KEYWORDS_NUM,MAX_SEARCH_SIZE,SORT_FIELD,\
                        TOP_WEIBOS_LIMIT,topic_en2ch_dict,WEEK_TIME,DAY,DAY_HOURS,HOUR,SENTIMENT_DICT_NEW,\
                        WHITE_UID_PATH, WHITE_UID_FILE_NAME, WORD2VEC_PATH

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
        item_exist = es_xnr.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id)['_source']
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
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

    keyword_list = []
    print 'keywords...',keywords
    model = gensim.models.KeyedVectors.load_word2vec_format(WORD2VEC_PATH,binary=True)
    
    for word in keywords:
	try:
            simi_list = model.most_similar(word,topn=20)
	except:
	    continue
        for simi_word in simi_list:
            keyword_list.append(simi_word[0])

    group_uid_list = set()

    if datetime_list == []:
        return []
    #keyword_query_list = []
    query_item = 'text'
    flow_text_index_name_list = []
    for datetime in datetime_list:
        flow_text_index_name = flow_text_index_name_pre + datetime
        flow_text_index_name_list.append(flow_text_index_name)

    nest_query_list = []
    for keyword in keyword_list:
        #nest_query_list.append({'match':{query_item:keyword}})
        nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})
        
    #keyword_query_list.append({'bool':{'must':nest_query_list}})

    
    count = MAX_DETECT_COUNT

    white_uid_path = WHITE_UID_PATH + WHITE_UID_FILE_NAME
    white_uid_list = []
    with open(white_uid_path,'r') as f:
        for line in f:
            line = line.strip()
            white_uid_list.append(line)

    white_uid_list = list(set(white_uid_list))
    #print 'white_uid_list:::',white_uid_list
    if len(nest_query_list) == 1:
        SHOULD_PERCENT = 1  # 绝对数量。 保证至少匹配一个词
    else:
        SHOULD_PERCENT = '3'  # 相对数量。 2个词时，保证匹配2个词，3个词时，保证匹配2个词
    
    query_body = {
        'query':{
            'bool':{
                'should':nest_query_list,
                'minimum_should_match': SHOULD_PERCENT,
                'must_not':{'terms':{'uid':white_uid_list}}
            }
        },
        'aggs':{
            'all_uids':{
                'terms':{
                    'field':'uid',
                    'order':{'_count':'desc'},
                    'size':count
                }
            }
        }
    }
    es_results = es_flow_text.search(index=flow_text_index_name_list,doc_type=flow_text_index_type,\
                body=query_body,request_timeout=999999)['aggregations']['all_uids']['buckets']

    #'must_not':{'terms':{'uid':white_uid_list}},

    for i in range(len(es_results)):
        #print 'es_results..',es_results
        #print 'es_results[i]..',es_results[i]
        uid = es_results[i]['key']
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
        r.lpush(weibo_target_domain_detect_queue_name,json.dumps(decect_task_information))
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
            if i % 1000 == 0:
                print i
            if label == 'character':
                text = es_weibo_results[i]['_source']['text']
                timestamp = es_weibo_results[i]['_source']['timestamp']
                uid_weibo.append([uid,text,timestamp])
            
            '''
            ## 合并相同id的关键词字典
            
            if uid in uid_weibo_keywords_dict.keys():
                uid_weibo_keywords_dict[uid] = dict(Counter(uid_weibo_keywords_dict[uid])+Counter(keywords_dict))
            else:
                uid_weibo_keywords_dict[uid] = keywords_dict

            ## 合并所有用户的关键词字典
            keywords_dict_all_users = dict(Counter(keywords_dict_all_users)+Counter(keywords_dict))
            '''
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
    #print 'uid_weibo_keywords_dict::::',uid_weibo_keywords_dict
    #print 'uid_weibo_keywords_dict.keys()::::::',uid_weibo_keywords_dict.keys()
    #print 'type：：：：：：：',type(uid_weibo_keywords_dict)
    ## 群体政治倾向
    political_side_count_sort = political_classify_sort(uids_list,uid_weibo_keywords_dict)
    
    # political_side_count_sort格式： [(label1,num1),(label2,num2),...] 按num降序

    ## 群体常用关键词
    keywords_dict_all_users_sort = sorted(keywords_dict_all_users.items(),key=lambda x:x[1], reverse=True)[:TOP_KEYWORDS_NUM]

    ## 群体角色分布
    
    r_domain = dict()

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
        if len(uids_list):
            day_hour_counts.append(hour_counts/float(len(uids_list)))  
        else:
            day_hour_counts.append(0)                     
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
    day_hour_counts_aver = np.mean(day_hour_counts_all_np,axis=0).astype(np.int)  ## 对二维数组按列求均值

    #day_hour_counts_aver_time = np.argsort(-day_hour_counts_aver)   ### np.argsort(-x)  按从大到小的数据的索引排列
 
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
        print '领域知识库和角色知识库计算开始！'
        if decect_task_information != {}:

            task_id = decect_task_information['domain_pinyin']
            domain = decect_task_information['domain_name']
            print task_id
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
                detect_results = detect_by_seed_users(seed_users)
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
    compute_domain_base()
    print 'end_time::',time.ctime()
    #create_time = datetime2ts(S_DATE)
    #uids_list = [u'1423850780', u'1726417911', u'1213687703', u'1753033432', u'1899373067', u'2328516855', u'1102939912', u'2784472192', u'5689647207', u'2321615032', u'1565668374', u'2058162745', u'2607972104', u'2658334301', u'1559383255', u'1210417191', u'1419741773', u'5556883816', u'1652377855', u'1964169017', u'2454862903', u'5156313848', u'1261340881', u'5245906107', u'1863675294', u'3266943013', u'2435703477', u'1220861753', u'1642512402', u'2404885340', u'5631552860', u'2865753583', u'2313365637', u'5237295433', u'1410834893', u'1544593902', u'1400229064', u'2899078547', u'1066995495', u'1498635641', u'1749785873', u'3217459400', u'1223354542', u'1941624714', u'3268047813', u'1944655140', u'1045529987', u'1789217487', u'1820201245', u'2080244437', u'2811244260', u'5313077864', u'1736574887', u'1711530911', u'2101413011', u'2119480393', u'1935084477', u'3550995170', u'2086220694', u'1265591123', u'3170247223', u'2355658474', u'5865684347', u'1973957620', u'2683689883', u'5089634923', u'1701401324', u'3775056661', u'5122654941', u'1120664271', u'3810651093', u'2973655904', u'2454236790', u'1402551940', u'1405296973', u'1405759702', u'1735882701', u'1776361441', u'1377801857', u'2793242114', u'3940994964', u'2180978342', u'1710495347', u'3194463860', u'2071544747', u'1896650227', u'1808530283', u'3596701994', u'3173633817', u'5660364135', u'1923390687', u'1221045561', u'3314280193', u'1111566084', u'5325071667', u'2236171720', u'3183107112', u'1912150611', u'2717140112', u'1400447140', u'2829934482', u'1700648435', u'2611342603', u'1642703337', u'2963114251', u'1901692317', u'1288764341', u'2104693617', u'5604447018', u'1410242783', u'2315355472', u'3176804502', u'1959437653', u'5698521016', u'3495612870', u'2656215113', u'3568201030', u'1773958670', u'2445204367', u'1665681810', u'2662050853', u'1243477063', u'2050690913', u'1912234472', u'3219381715', u'2109287495', u'1636263050', u'1427412531', u'3172988254', u'2147458001', u'5762497058', u'1912388967', u'3788626080', u'5834323866', u'1685802840', u'1688221335', u'2140415420', u'1423155224', u'3320127782', u'2019719255', u'5044717223', u'1642591402', u'3708524475', u'1336056181', u'1110840514', u'1885240921', u'1407219330', u'2667258534', u'1254230710', u'3334836752', u'2265781063', u'1910597850', u'1048355927', u'2707274307', u'2208160981', u'1935716045', u'1280846847', u'2980316265', u'2292881562', u'1198071662', u'1916460463', u'1723216063', u'2294316500', u'2781170547', u'2138008382', u'1197153650', u'1567762360', u'1553416024', u'2698228511', u'5612237200', u'1980768563', u'2485659250', u'1277061984', u'1746575865', u'2128372947', u'1890872744', u'2202692513', u'5743525008', u'1999404300', u'1580368313', u'1763270164', u'1631499041', u'1342828732', u'1739713671', u'1655746665', u'2201109250', u'1772440677', u'2023821012', u'1919675342', u'3407518320', u'1658719205', u'5795387210', u'5234473891', u'2079591603', u'1640571365', u'1713033565', u'3675736060', u'1650111241', u'1587473341', u'1840402115', u'2634877355', u'1737737970', u'2886336191', u'1783541537', u'1687442645', u'1241282897', u'2458371534', u'1681901143', u'1891503444', u'2827102952', u'1006550592', u'3210670957', u'1270296285', u'3096944547', u'2269443552', u'1854343754', u'1318252980', u'3362148360', u'5093590656', u'1837869620', u'1707924411', u'1132422373', u'1803570001', u'1337010854', u'2757691921', u'1102543581', u'1313360064', u'1708242847', u'5018637328', u'2490780034', u'2374428350', u'2288486705', u'3446441254', u'2195715901', u'2105431670', u'1560442584', u'1471143571', u'3195538854', u'5711710471', u'2335769290', u'5014862797', u'5666929142', u'1405906767', u'5891357995', u'3557501047', u'1494768740', u'5460202851', u'3823554401', u'1377886141', u'2104296815', u'1425721431', u'1807436544', u'1975995305', u'3794240230', u'2165401830', u'2189978113', u'5113416326', u'1893082634', u'1798787475', u'3542663900', u'1497575844', u'1424099140', u'2176657302', u'1672392695', u'1632259570', u'2614553844', u'2087875965', u'2096522211', u'1681993644', u'1676582524', u'1998412373', u'1694061470', u'1271403002', u'1215468900', u'5281491251', u'5426756023', u'1567560777', u'2429058367', u'1730107171', u'1459272740', u'2700138820', u'1807715644', u'2027773605', u'2432550377', u'1311641560', u'2275024227', u'1745538963', u'2286908003', u'1581391555', u'1634118445', u'6032762013', u'2280198017', u'1704832685', u'3749541574', u'1791010393', u'1746383931', u'2705944663', u'1909203062', u'5900035466', u'5500491427', u'1785254947', u'3268761462', u'2418279900', u'5321387246', u'1195031270', u'3937348351', u'1962748933', u'2790685082', u'1401678702', u'5041556773', u'1371580593', u'1457699772', u'1652811601', u'5067914848', u'1800457345', u'1220562903', u'1420157965', u'1351183294', u'2664572983', u'1863185713', u'3187525994', u'5318016019', u'1757000951', u'2636952191', u'1684452940', u'2746922325', u'2288735533', u'1215031834', u'5614572422', u'1479040710', u'1364905923', u'3701555977', u'1830716584', u'5222772559', u'1717833412', u'2782830277', u'3163782211', u'2031805397', u'1924585171', u'1131224560', u'2615059833', u'3352759880', u'5346360022', u'2075787667', u'5720846370', u'2144789105', u'3881380517', u'3719069393', u'3279745033', u'2645833223', u'3881168244', u'1222221682', u'1767364203', u'1940696741', u'1283201960', u'2268603763', u'2687582663', u'1749111457', u'2408714590', u'3128832561', u'1898786143', u'2634947861', u'1642420854', u'5053469079', u'2542011901', u'5446004161', u'2132089917', u'3485209423', u'5592294260', u'1985324940', u'1812032970', u'1231668867', u'1977460817', u'2533574257', u'2700797874', u'1461899984', u'3514732862', u'1676559025', u'3879531223', u'1152369551', u'2715357317', u'1472459833', u'1400582340', u'1581544960', u'5837587459', u'2792675770', u'2291429207', u'1862891690', u'1436819583', u'1049328060', u'1686307120', u'1998988241', u'1692110027', u'2308794260', u'2631016945', u'2284997417', u'1778181617', u'1416237723', u'1895682211', u'1668391692', u'2961949875', u'1751714412', u'1993192353', u'1245369991', u'2232625672', u'1933626242', u'2704737004', u'2375456772', u'1801817195']
    #get_psy_feature_sort(uids_list,create_time)
    #active_time_compute(uids_list,'2016-11-20')
    #day_post_num_compute(uids_list,'2016-11-20')

    #uid_weibo_keywords_dict,keywords_dict_all_users = uid_list_2_uid_keywords_dict(uids_list,datetime_list)
