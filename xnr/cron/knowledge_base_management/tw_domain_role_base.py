# -*-coding:utf-8-*-
import os
import json
import time
import sys
import gensim
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from collections import Counter
import numpy as np
reload(sys)
sys.path.append('../../')
from global_utils import r,tw_target_domain_detect_queue_name,tw_target_domain_analysis_queue_name,\
                        es_xnr as es, es_xnr, twitter_flow_text_index_name_pre as flow_text_index_name_pre,\
                        twitter_flow_text_index_type as flow_text_index_type,\
                        tw_domain_index_name, tw_domain_index_type, twitter_user_index_name, twitter_user_index_type,\
                        tw_role_index_name, tw_role_index_type,\
                        tw_portrait_index_name, tw_portrait_index_type,\
                        tw_be_retweet_index_name_pre as be_retweet_index_name_pre, tw_be_retweet_index_type as be_retweet_index_type
from global_config import S_TYPE,S_DATE_TW as S_DATE, R_BEGIN_TIME
from parameter import MAX_DETECT_COUNT,MAX_FLOW_TEXT_DAYS,MAX_SEARCH_SIZE, FB_TW_TOPIC_ABS_PATH, TW_DOMAIN_ABS_PATH,\
                    DAY, WEEK, fb_tw_topic_en2ch_dict as topic_en2ch_dict, SENTIMENT_DICT_NEW, SORT_FIELD,\
                    TOP_KEYWORDS_NUM,TOP_WEIBOS_LIMIT,WEEK_TIME,DAY,DAY_HOURS,HOUR,\
                    fb_tw_topic_ch2en_dict as topic_ch2en_dict, WORD2VEC_PATH
from time_utils import get_twitter_flow_text_index_list as get_flow_text_index_list,ts2datetime,datetime2ts
from utils import split_city    #tw 没有geo信息 不可用

sys.path.append('../../cron/trans/')
from trans import trans, simplified2traditional, traditional2simplified

sys.path.append(FB_TW_TOPIC_ABS_PATH)
from test_topic import topic_classfiy
from config import name_list, zh_data

sys.path.append(TW_DOMAIN_ABS_PATH)
from domain_classify import domain_main

sys.path.append('../../fb_tw_user_portrait/')
from keyword_extraction import get_filter_keywords


## 引入各个分类器
from political.political_main import political_classify
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from character.test_ch_sentiment import classify_sentiment

#
es_flow_text = es
r_beigin_ts = datetime2ts(R_BEGIN_TIME)


def save_data2es(data):
    update_uid_list = []
    create_uid_list = []
    try:
        for uid, d in data.items():
            if es.exists(index=tw_portrait_index_name, doc_type=tw_portrait_index_type, id=uid):
                update_uid_list.append(uid)
            else:
                create_uid_list.append(uid)
        #bulk create
        bulk_create_action = []
        if create_uid_list:
            for uid in create_uid_list:
                create_action = {'index':{'_id': uid}}
                bulk_create_action.extend([create_action, data[uid]])
            result = es.bulk(bulk_create_action, index=tw_portrait_index_name, doc_type=tw_portrait_index_type)
            if result['errors'] :
                print result
                return False
        #bulk update
        if update_uid_list:
            bulk_update_action = []
            for uid in update_uid_list:
                update_action = {'update':{'_id': uid}}
                bulk_update_action.extend([update_action, {'doc': data[uid]}])
            result = es.bulk(bulk_update_action, index=tw_portrait_index_name, doc_type=tw_portrait_index_type)
            if result['errors'] :
                print result
                return False
    except Exception,e:
        print e
        return False
    return True

def my_topic_classfiy(uid_list, datetime_list):
    topic_dict_results = {}
    topic_string_results = {}
    #将处理后的结果保存到数据库中，并在处理前查询数据库中是否已经有了相应内容之前存储的结果，以提高效率
    uids = uid_list
    unresolved_uids = []
    res = es.mget(index=tw_portrait_index_name, doc_type=tw_portrait_index_type, body={'ids': uids})['docs']
    for r in res:
        uid = r['_id']
        if r.has_key('found'): 
            found = r['found']
            if found and r['_source'].has_key('topic'):
                topic = r['_source']['topic']
                topic_string = r['_source']['topic_string']
                topic_dict_results[uid] = json.loads(topic)
                topic_string_results[uid] = [topic_ch2en_dict[ch_topic] for ch_topic in topic_string.split('&')]
            else:
                unresolved_uids.append(uid)
        else:   #es表中目前无任何记录 
            unresolved_uids.append(uid)

    #未在数据库中的进行计算并存储
    user_topic_dict = {}
    user_topic_list = {}
    if unresolved_uids:
        tw_flow_text_index_list = []
        for datetime in datetime_list:
            tw_flow_text_index_list.append(flow_text_index_name_pre + datetime)
        user_topic_data = get_filter_keywords(tw_flow_text_index_list, unresolved_uids)
        user_topic_dict, user_topic_list = topic_classfiy(unresolved_uids, user_topic_data)

        user_topic_string = {}
        for uid, topic_list in user_topic_list.items():
            li = []
            for t in topic_list:
                li.append(zh_data[name_list.index(t)].decode('utf8'))
            user_topic_string[uid] = '&'.join(li)
        user_topic = {}
        for uid in unresolved_uids:
            if uid in user_topic_dict:
                user_topic[uid] = {
                    'filter_keywords': json.dumps(user_topic_data[uid]),
                    'topic': json.dumps(user_topic_dict[uid]),
                    'topic_string': user_topic_string[uid]
                }
            else:
                user_topic[uid] = {
                    'filter_keywords': json.dumps({}),
                    'topic': json.dumps({}),
                    'topic_string': ''
                }
        save_data2es(user_topic)

    #整合
    user_topic_dict.update(topic_dict_results)
    user_topic_list.update(topic_string_results)
    return user_topic_dict, user_topic_list

def count_text_num(uid_list, tw_flow_text_index_list):
    count_result = {}
    #QQ那边好像就是按照用户来count的    https://github.com/huxiaoqian/xnr1/blob/82ff9704792c84dddc3e2e0f265c46f3233a786f/xnr/qq_xnr_manage/qq_history_count_timer.py
    for uid in uid_list:
        textnum_query_body = {
            'query':{
                "filtered":{
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"uid": uid}},
                            ]
                         }
                    }
                }
            }
        }
        text_num = 0
        for index_name in tw_flow_text_index_list:
            result = es.count(index=index_name, doc_type=flow_text_index_type,body=textnum_query_body)
            if result['_shards']['successful'] != 0:
                text_num += result['count']
        count_result[uid] = text_num
    return count_result

def trans_bio_data(bio_data):
    count = 1.0
    while True:
        translated_bio_data = trans(bio_data)
        if len(translated_bio_data) == len(bio_data):
            break
        else:
            print 'sleep start ...'
            time.sleep(count)
            count = count*1.1
            print 'sleep over ...'
    return translated_bio_data

def my_domain_classfiy(uid_list, datetime_list):
    domain_results = {}
    #将处理后的结果保存到数据库中，并在处理前查询数据库中是否已经有了相应内容之前存储的结果，以提高效率
    uids = uid_list
    unresolved_uids = []
    res = es.mget(index=tw_portrait_index_name, doc_type=tw_portrait_index_type, body={'ids': uids})['docs']
    for r in res:
        uid = r['_id']
        if r.has_key('found'): 
            found = r['found']
            if found and r['_source'].has_key('domain'):
                domain = r['_source']['domain']
                domain_results[uid] = domain
            else:
                unresolved_uids.append(uid)
        else:   #es表中目前无任何记录 
            unresolved_uids.append(uid)

    #未在数据库中的进行计算并存储
    user_domain = {}
    user_domain_temp = {}
    if unresolved_uids:
        tw_flow_text_index_list = []
        for datetime in datetime_list:
            tw_flow_text_index_list.append(flow_text_index_name_pre + datetime)

        user_domain_data = {}
        #load num of text
        count_result = count_text_num(unresolved_uids, tw_flow_text_index_list)
        #load baseinfo
        tw_user_query_body = {
            'query':{
                "filtered":{
                    "filter": {
                        "bool": {
                            "must": [
                                {"terms": {"uid": unresolved_uids}},
                            ]
                         }
                    }
                }
            },
            'size': MAX_SEARCH_SIZE,
            "fields": ["location", "username", "description", "uid"]
        }
        try:
            search_results = es.search(index=twitter_user_index_name, doc_type=twitter_user_index_type, body=tw_user_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_domain_data:
                    text_num = count_result[uid]
                    user_domain_data[uid] = {
                        'location': '',
                        'username': '',
                        'description': '',
                        'number_of_text': text_num
                    }
                if content.has_key('location'):
                    location = content.get('location')[0]
                else:
                    location = ''
                if content.has_key('description'):
                    description = content.get('description')[0][:1000]
                else:
                    description = ''
                if content.has_key('username'):
                    username = content.get('username')[0]
                else:
                    username = '' 
                user_domain_data[uid]['location'] = location
                user_domain_data[uid]['username'] = username
                user_domain_data[uid]['description'] = description
        except Exception,e:
            print e
        #由于一个用户请求一次翻译太耗时，所以统一批量翻译
        trans_uid_list = []
        untrans_bio_data = []
        cut = 100
        n = len(user_domain_data)/cut
        for uid, content in user_domain_data.items():
            trans_uid_list.append(uid)
            untrans_bio_data.extend([content['location'] ,content['description']])
            if n:
                if len(trans_uid_list)%cut == 0:
                    temp_trans_bio_data = trans_bio_data(untrans_bio_data)
                    for i in range(len(trans_uid_list)):
                        uid = trans_uid_list[i]
                        user_domain_data[uid]['location'] = '_'.join(temp_trans_bio_data[2*i])
                        user_domain_data[uid]['description'] = '_'.join(temp_trans_bio_data[2*i+1])
                    trans_uid_list = []
                    untrans_bio_data = []
                    n = n - 1
            else:
                if len(trans_uid_list) == (len(user_domain_data)%cut):
                    temp_trans_bio_data = trans_bio_data(untrans_bio_data)
                    for i in range(len(trans_uid_list)):
                        uid = trans_uid_list[i]
                        user_domain_data[uid]['location'] = '_'.join(temp_trans_bio_data[2*i])
                        user_domain_data[uid]['description'] = '_'.join(temp_trans_bio_data[2*i+1])
                    trans_uid_list = []
                    untrans_bio_data = []
        #domian计算
        user_domain_temp = domain_main(user_domain_data)    
        for uid in unresolved_uids:
            if uid in user_domain_temp:
                user_domain[uid] = {'domain': user_domain_temp[uid]}
            else:
                user_domain_temp[uid] = 'other'
                user_domain[uid] = {'domain': 'other'}
        save_data2es(user_domain)
    #整合
    user_domain_temp.update(domain_results)
    return user_domain_temp

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
        item_exist = es_xnr.get(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id)['_source']
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
        es_xnr.update(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id,body={'doc':item_exist})
    except Exception, e:
        print e
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
        es_xnr.index(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id,body=item_exist)
    mark = True
    return mark

## 保存群体分析结果
def save_group_description_results(group_results,decect_task_information):
    mark = False   
    task_id = decect_task_information['domain_pinyin']

    try:
        item_exist = es_xnr.get(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id)['_source']
        item_exist['role_distribute'] = json.dumps(group_results['role_distribute'])
        item_exist['top_keywords'] = json.dumps(group_results['top_keywords'])
        item_exist['political_side'] = json.dumps(group_results['political_side'])
        item_exist['topic_preference'] = json.dumps(group_results['topic_preference'])
        item_exist['compute_status'] = 2  # 存入群体描述
        es_xnr.update(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id,body={'doc':item_exist})
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
        es_xnr.index(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id,body=item_exist)
    
    mark = True

    return mark

## 保存角色分析结果

def save_role_feature_analysis(role_results,role_label,domain,role_id,task_id):
    mark = False

    try:
        item_exist = es_xnr.get(index=tw_role_index_name,doc_type=tw_role_index_type,id=role_id)['_source']
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

    
        es_xnr.update(index=tw_role_index_name,doc_type=tw_role_index_type,id=role_id,body={'doc':item_exist})
        
        item_domain = dict()
        item_domain['compute_status'] = 3  # 存入角色分析结果
        es_xnr.update(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id,body={'doc':item_domain})
    
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
       
        es_xnr.index(index=tw_role_index_name,doc_type=tw_role_index_type,id=role_id,body=item_exist)
        
        item_domain = dict()
        item_domain['compute_status'] = 3  # 存入角色分析结果
        es_xnr.update(index=tw_domain_index_name,doc_type=tw_domain_index_type,id=task_id,body={'doc':item_domain})
    
    mark =True

    return mark

#use to change detect task process proportion
#input: task_name, proportion
#output: status (True/False)
def change_process_proportion(task_id, proportion):
    mark = False
    try:
        task_exist_result = es_xnr.get(index=tw_domain_index_name, doc_type=tw_domain_index_type, id=task_id)['_source']
    except:
        task_exist_result = {}
        return 'task is not exist'
    if task_exist_result != {}:
        task_exist_result['compute_status'] = proportion
        es_xnr.update(index=tw_domain_index_name, doc_type=tw_domain_index_type, id=task_id, body={'doc':task_exist_result})
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
    keywords_list = []
    model = gensim.models.KeyedVectors.load_word2vec_format(WORD2VEC_PATH,binary=True)
    for word in keywords:
        simi_list = model.most_similar(word,topn=20)
        for simi_word in simi_list:
            keywords_list.append(simi_word[0])

    group_uid_list = set()
    if datetime_list == []:
        return []

    query_item = 'text'
    flow_text_index_name_list = []
    for datetime in datetime_list:
        flow_text_index_name = flow_text_index_name_pre + datetime
        flow_text_index_name_list.append(flow_text_index_name)

    nest_query_list = []
    #文本中可能存在英文或者繁体字，所以都匹配一下
    en_keywords_list = trans(keywords_list, target_language='en')
    for i in range(len(keywords_list)):
        keyword = keywords_list[i]
        traditional_keyword = simplified2traditional(keyword)
        
        if len(en_keywords_list) == len(keywords_list): #确保翻译没出错
            en_keyword = en_keywords_list[i]
            nest_query_list.append({'wildcard':{query_item:'*'+en_keyword+'*'}})
        
        nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})
        nest_query_list.append({'wildcard':{query_item:'*'+traditional_keyword+'*'}})

    count = MAX_DETECT_COUNT
    if len(nest_query_list) == 1:
        SHOULD_PERCENT = 1  # 绝对数量。 保证至少匹配一个词
    else:
        SHOULD_PERCENT = '3'  # 相对数量。 2个词时，保证匹配2个词，3个词时，保证匹配2个词

    query_body = {
        'query':{
            'bool':{
                'should':nest_query_list,
                'minimum_should_match': SHOULD_PERCENT,
                # 'must_not':{'terms':{'uid':white_uid_list}}
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

    for i in range(len(es_results)):
        uid = es_results[i]['key']
        group_uid_list.add(uid)
    group_uid_list = list(group_uid_list)
    return group_uid_list


### 根据种子用户
# input：种子用户uid，任务创建时间
# output：近期与种子用户有转发和评论关系的微博用户群体的画像数据
def detect_by_seed_users(seed_users):
    retweet_mark = 1 #目前只有部分数据
    comment_mark = 0 #暂无数据

    group_uid_list = set()
    all_union_result_dict = {}
    #get retweet/comment es db_number
    now_ts = time.time()
    db_number = get_db_num(now_ts)

    #step1: mget retweet and be_retweet
    if retweet_mark == 1:
        # retweet_index_name = retweet_index_name_pre + str(db_number)
        be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
        #mget retwet
        '''
        try:
            retweet_result = es.mget(index=retweet_index_name, doc_type=retweet_index_type, \
                                             body={'ids':seed_users}, _source=True)['docs']
        except:
            retweet_result = []
        '''
        #mget be_retweet
        try:
            be_retweet_result = es.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type, \
                                                body={'ids':seed_users} ,_source=True)['docs']
        except:
            be_retweet_result = []
    '''
    #step2: mget comment and be_comment
    if comment_mark == 1:
        comment_index_name = comment_index_name_pre + str(db_number)
        be_comment_index_name = be_comment_index_name_pre + str(db_number)
        #mget comment
        try:
            comment_result = es.mget(index=comment_index_name, doc_type=comment_index_type, \
                                             body={'ids':seed_users}, _source=True)['docs']
        except:
            comment_result = []
        #mget be_comment
        try:
            be_comment_result = es.mget(index=be_comment_index_name, doc_type=be_comment_index_type, \
                                            body={'ids':seed_users}, _source=True)['docs']
        except:
            be_comment_result = []
    '''
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
        r.lpush(tw_target_domain_detect_queue_name,json.dumps(decect_task_information))
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

def topic_classfiy_sort(uids_list,datetime_list):

    result_data,uid_topic = my_topic_classfiy(uids_list,datetime_list)

    topic_list = []
    for uid,topic in uid_topic.iteritems():
        topic_list = topic_list + topic
    topic_count_dict = dict()

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

    ts_up_limit = datetime2ts(datetime_list[0]) + 24*3600
    ts_down_limit = datetime2ts(datetime_list[-1])
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
        
        for i in range(len(es_weibo_results)):
            uid = es_weibo_results[i]['_source']['uid']
            keywords_dict = {}
            if es_weibo_results[i]['_source'].has_key('keywords_dict'):
                keywords_dict = es_weibo_results[i]['_source']['keywords_dict']
                keywords_dict = json.loads(keywords_dict)
            if i % 1000 == 0:
                print i
            if label == 'character':
                text = es_weibo_results[i]['_source']['text']
                timestamp = es_weibo_results[i]['_source']['timestamp']

                if timestamp >=ts_down_limit and timestamp < ts_up_limit:  #确保时间戳确实在datetime_list范围内，因为真的有存储错误的记录。。。
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

    # domain,r_domain = domain_classfiy(uids_list,uid_weibo_keywords_dict)
    r_domain = my_domain_classfiy(uids_list, datetime_list)


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
        try:
            role_uids_dict[role].append(uid)
        except:
            role_uids_dict[role] = [uid]

    ## 群体话题偏好
    topic_count_dict_sort = topic_classfiy_sort(uids_list,datetime_list)

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
       
        for weibo in mtype_weibo:  #对于每条微博
            
            try:
                geo = weibo['_source']['geo'].encode('utf8')
                print 'geo'
                print geo
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
        sen_no = str(item['key'])
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
    topic_count_dict_sort = topic_classfiy_sort(uids_list,datetime_list)

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
        task_information_string = r.rpop(tw_target_domain_detect_queue_name)
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
    # uid_list = ['1140849537', '443835769306299', '288733581614500']
    # create_time = datetime2ts(S_DATE)
    # datetime_list = get_flow_text_datetime_list(create_time)
    # # my_domain_classfiy(uid_list, datetime_list)

    # print detect_by_keywords([u'中国', u'党'], datetime_list)
    # print active_time_compute(uid_list,datetime_list[0])