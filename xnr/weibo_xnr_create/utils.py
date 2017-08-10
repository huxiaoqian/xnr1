#-*- coding: utf-8 -*-

'''
use to save function to create xnr info
'''
import pinyin
import json
import time
import os
import pandas as pd
from collections import Counter

from xnr.global_config import S_TYPE,S_DATE
from xnr.global_utils import r,weibo_target_domain_detect_queue_name,weibo_domain_index_name,weibo_domain_index_type,\
                                weibo_role_index_name,weibo_role_index_type,weibo_xnr_index_name,weibo_xnr_index_type,\
                                weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type
from xnr.global_utils import es_xnr as es
from xnr.global_utils import es_flow_text,es_user_profile,profile_index_name,profile_index_type
from xnr.parameter import topic_en2ch_dict,domain_ch2en_dict,domain_en2ch_dict,\
                        ACTIVE_TIME_TOP,DAILY_INTEREST_TOP_USER,NICK_NAME_TOP,USER_LOCATION_TOP,\
                        DESCRIPTION_TOP,DAILY_INTEREST_TOP_USER,MONITOR_TOP_USER
from xnr.time_utils import get_flow_text_index_list,datetime2ts
from xnr.utils import nickname2uid,user_no2_id,_id2user_no
'''
import sys
reload(sys)
sys.path.append('../')
from global_config import S_TYPE,S_DATE
from global_utils import r,weibo_target_domain_detect_queue_name,weibo_domain_index_name,weibo_domain_index_type,\
                                weibo_role_index_name,weibo_role_index_type
from global_utils import es_xnr as es
from parameter import topic_en2ch_dict,domain_ch2en_dict,domain_en2ch_dict,ACTIVE_TIME_TOP,\
                        DAILY_INTEREST_TOP_USER
from time_utils import get_flow_text_index_list
'''
def get_role_sort_list(domain_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    try:
        es_result = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=domain_pinyin)['_source']

        role_sort_list_en = json.loads(es_result['role_distribute'])
        role_sort_list_zh = []
        for item in role_sort_list_en:
            role_zh = domain_en2ch_dict[item[0]]
            role_sort_list_zh.append(role_zh)

        return role_sort_list_zh
    except:
        return []

def get_role2feature_info(domain_name,role_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_name_en = domain_ch2en_dict[role_name]
    _id = domain_pinyin + '_' + role_name_en
    try:
        es_result = es.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=_id)['_source']
        
        feature_info_dict = es_result        
        feature_filter_dict = dict()

        feature_filter_dict['political_side'] = json.loads(feature_info_dict['political_side'])
        try:
            feature_filter_dict['psy_feature'] = json.loads(feature_info_dict['psy_feature'])
        except:
            feature_filter_dict['psy_feature'] = []

        #print
        return feature_filter_dict

    except:
        return []

def get_recommend_step_two(task_detail):
    domain_name = task_detail['domain_name']
    role_name = task_detail['role_name']
    daily_interests_list = task_detail['daily_interests'].encode('utf-8').split('，')

    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_name_en = domain_ch2en_dict[role_name]
    _id = domain_pinyin + '_' + role_name_en

    try:
        recommend_results = dict()

        ## 根据角色信息
        es_result = es.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=_id)['_source']
        
        #### 角色实例
        try:
            role_example_list = []
            member_uids = json.loads(es_result['member_uids'])
            member_uids_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                                                    body={'ids':member_uids})['docs']
            for result in member_uids_results:
                if result['found'] == True:
                    result = result['_source']
                    role_example_list.append(result['nick_name'])
            recommend_results['role_example'] = role_example_list
        except:
            recommend_results['role_example'] = []
        
        recommend_results['active_time'] = json.loads(es_result['active_time'])[:ACTIVE_TIME_TOP]
        
        day_post_num = json.loads(es_result['day_post_num'])
        day_post_num_new = pd.Series(day_post_num)
        day_post_num_new = day_post_num_new.fillna(0)
        day_post_num_new = list(day_post_num_new)
        day_post_num_average = sum(day_post_num_new)/float(len(day_post_num_new))
        recommend_results['day_post_num_average'] = day_post_num_average
        
        ## 根据日常兴趣
        create_time = time.time()
        
        if S_TYPE == 'test':
            create_time = datetime2ts(S_DATE)
        
        index_name_list = get_flow_text_index_list(create_time)
        
        try:
            query_body = {
                'query':{
                    'filtered':{
                        'filter':{
                            'terms':{'daily_interests':daily_interests_list}
                        }
                    }
                },
                'sort':{'user_fansnum':{'order':'desc'}},
                'size':DAILY_INTEREST_TOP_USER,
                '_source':['uid']
            }

            es_results = es_flow_text.search(index=index_name_list,doc_type='text',body=query_body)['hits']['hits']
          
            daily_interest_uid_set = set()
            for result in es_results:
                daily_interest_uid_set.add(result['_source']['uid'])
            daily_interest_uid_list = list(daily_interest_uid_set)
            es_daily_interests_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                                                    body={'ids':daily_interest_uid_list})['docs']
            nick_name_list = []
            sex_list = []
            user_location_list = []
            description_list = []
           
            for result in es_daily_interests_results:
                if result['found'] == True:
                    result = result['_source']
                    nick_name_list.append(result['nick_name'])
                    sex_list.append(result['sex'])
                    user_location_list.append(result['user_location'])
                    if result['description']:
                        description_list.append(result['description'])
            sex_list_count = Counter(sex_list)
            sex_sort = sorted(sex_list_count.items(),key=lambda x:x[1],reverse=True)[:1][0][0]
          
            user_location_list_count = Counter(user_location_list)
            user_location_sort_top = sorted(user_location_list_count.items(),key=lambda x:x[1],reverse=True)[:USER_LOCATION_TOP]
            user_location_top_list = []
            for user_location in user_location_sort_top:
                user_location_top_list.append(user_location_sort[0])
            
                
            recommend_results['nick_name'] = nick_name_list[:NICK_NAME_TOP]
            recommend_results['role_example'] = recommend_results['role_example'] + nick_name_list[:NICK_NAME_TOP]
            recommend_results['sex'] = sex_sort
            recommend_results['user_location'] = user_location_top_list
            recommend_results['description'] = description_list[:DESCRIPTION_TOP]

        except:
            print '没有找到日常兴趣相符的用户'
            recommend_results['nick_name'] = ''
            recommend_results['sex'] = ''
            recommend_results['user_location'] = ''
            recommend_results['description'] = ''
        ## 年龄、职业
        recommend_results['age'] = ''
        recommend_results['career'] = ''

        return recommend_results

    except:
        return []

def get_recommend_follows(task_detail):
    recommend_results = dict()
    daily_interests_list = task_detail['daily_interests'].encode('utf-8').split('，')
    monitor_keywords_list = task_detail['monitor_keywords'].encode('utf-8').split('，')
    print 'daily_interests_list::',daily_interests_list
    create_time = time.time()        
    if S_TYPE == 'test':
        create_time = datetime2ts(S_DATE)
    
    index_name_list = get_flow_text_index_list(create_time)
    
    ## 日常兴趣关注
    try:
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'terms':{'daily_interests':daily_interests_list}
                    }
                }
            },
            'sort':{'user_fansnum':{'order':'desc'}},
            'size':DAILY_INTEREST_TOP_USER,
            '_source':['uid']
        }

        es_results = es_flow_text.search(index=index_name_list,doc_type='text',body=query_body)['hits']['hits']
      
        daily_interest_uid_set = set()
        for result in es_results:
            daily_interest_uid_set.add(result['_source']['uid'])
        daily_interest_uid_list = list(daily_interest_uid_set)
        es_daily_interests_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                                                body={'ids':daily_interest_uid_list})['docs']
        nick_name_list = []        
        for result in es_daily_interests_results:
            if result['found'] == True:
                result = result['_source']
                nick_name_list.append(result['nick_name'])
            else:
                continue
        recommend_results['daily_interests'] = nick_name_list[:NICK_NAME_TOP]

    except:
        print '没有找到日常兴趣相符的用户'
        recommend_results['daily_interests'] = ''

    ## 监测词关注
    nest_query_list = []
    print 'monitor_keywords_list:::',monitor_keywords_list
    for monitor_keyword in monitor_keywords_list:
        nest_query_list.append({'wildcard':{'keywords_string':'*'+monitor_keyword+'*'}})
    print 'nest_query_list::',nest_query_list
    try:
        query_body_monitor = {
            'query':{
                        'bool':{
                            'must':nest_query_list
                        }     
            },
            'sort':{'user_fansnum':{'order':'desc'}},
            'size':MONITOR_TOP_USER,
            '_source':['uid']
        }
        print '123'
        es_results = es_flow_text.search(index=index_name_list,doc_type='text',body=query_body_monitor)['hits']['hits']
        print 'es_results::',es_results
        monitor_keywords_uid_set = set()
        for result in es_results:
            monitor_keywords_uid_set.add(result['_source']['uid'])
        monitor_keywords_uid_list = list(monitor_keywords_uid_set)

        es_monitor_keywords_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                                                body={'ids':monitor_keywords_uid_list})['docs']
        nick_name_list = []        
        for result in es_monitor_keywords_results:
            if result['found'] == True:
                result = result['_source']
                nick_name_list.append(result['nick_name'])
            else:
                continue
        recommend_results['monitor_keywords'] = nick_name_list[:NICK_NAME_TOP]

    except:
        print '没有找到监测词相符的用户'
        recommend_results['monitor_keywords'] = ''


    return recommend_results

def get_save_step_one(task_detail):

    es_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body={'query':{'match_all':{}},\
                    'sort':{'user_no':{'order':'desc'}}})['hits']['hits']
    if es_results:
        user_no_max = es_results[0]['_source']['user_no']
        user_no_current = user_no_max + 1 
    else:
        user_no_current = 1

    task_detail['user_no'] = user_no_current
    task_id = user_no2_id(user_no_current)  #五位数 WXNR0001

    try:    
        item_exist = dict()
        item_exist['user_no'] = task_detail['user_no']
        item_exist['domain_name'] = task_detail['domain_name']
        item_exist['role_name'] = task_detail['role_name']
        item_exist['psy_feature'] = '&'.join(task_detail['psy_feature'].encode('utf-8').split('，'))
        item_exist['political_side'] = task_detail['political_side']
        item_exist['business_goal'] = '&'.join(task_detail['business_goal'].encode('utf-8').split('，'))
        item_exist['daily_interests'] = '&'.join(task_detail['daily_interests'].encode('utf-8').split('，'))
        item_exist['monitor_keywords'] = '&'.join(task_detail['monitor_keywords'].encode('utf-8').split('，'))
        item_exist['create_status'] = 0 # 第一步完成
        
        es.index(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id,body=item_exist)

        mark = True
    except:
        
        mark = False

    return mark

def get_save_step_two(task_detail):

    task_id = task_detail['task_id']
    #try:    
    item_exist = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id)['_source']
    item_exist['nick_name'] = task_detail['nick_name']
    item_exist['age'] = task_detail['age']
    item_exist['location'] = task_detail['location']
    item_exist['career'] = task_detail['career']
    item_exist['description'] = task_detail['description']
    item_exist['active_time'] = '&'.join(task_detail['active_time'].split('-'))
    item_exist['day_post_average'] = json.dumps(task_detail['day_post_average'].split('-'))
    item_exist['create_status'] = 1 # 第二步完成

    es.update(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id,body={'doc':item_exist})        
    mark = True
    #except:        
    #    mark = False

    return mark

    
def get_save_step_three_1(task_detail):
    task_id = task_detail['task_id']
    print '1212'
    try:    
        item_exist = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id)['_source']
        item_exist['weibo_mail_account'] = task_detail['weibo_mail_account']
        item_exist['weibo_phone_account'] = task_detail['weibo_phone_account']
        item_exist['password'] = task_detail['password']
        item_exist['uid'] = task_detail['uid']
        item_exist['create_status'] = 2 # 创建完成
        # 更新 weibo_xnr表
        es.update(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id,body={'doc':item_exist})        
        print '2323'
        mark =True
        
    except:        
        mark = False

    return mark

def get_save_step_three_2(task_detail):
    task_id = task_detail['task_id']
    
    #插入 weibo_xnr_fans_followers表
    try:
        item_fans_followers = dict()
        followers_nickname_list = task_detail['followers_nickname'].encode('utf-8').split('，')
        print 'followers_nickname_list::',followers_nickname_list
        print '111'
        followers_list = nickname2uid(followers_nickname_list)
        #print 'followers_list::',followers_list
        item_fans_followers['followers_list'] = json.dumps(followers_list)
        print '5656'
        item_fans_followers['user_no'] = _id2user_no(task_id.encode('utf-8'))

        print 'item_fans_followers::',item_fans_followers
        print '123'

        es.index(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=task_id,body=item_fans_followers)
        print '4545'
        mark = True
    except:        
        mark = False

  
    return mark
    

def get_domain_info(domain_pinyin):

    domain_info = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=domain_pinyin)['_source']

    return domain_info

def get_role_info(domain_pinyin,role_name):

    role_en = domain_ch2en_dict(role_name)

    role_info_id = domain_pinyin + '_' + role_en

    role_info = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=role_info_id)['_source']

    return role_info


def domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0):
    domain_task_dict = dict()
    if S_TYPE == 'test':
        domain_task_dict['domain_pinyin'] = pinyin.get(domain_name,format='strip',delimiter='_')
        domain_task_dict['domain_name'] = domain_name
        domain_task_dict['create_type'] = json.dumps(create_type)
        domain_task_dict['create_time'] = create_time
        domain_task_dict['submitter'] = submitter
        domain_task_dict['remark'] = remark
        domain_task_dict['compute_status'] = compute_status
    r.lpush(weibo_target_domain_detect_queue_name,json.dumps(domain_task_dict))
    #r.delete(weibo_target_domain_detect_queue_name)
    print 'success!'

if __name__ == '__main__':
    domain_name =  '维权群体'
    #domain_name =  '乌镇'
    create_type = {'by_keywords':['维权','律师'],'by_seed_users':[],'by_all_users':[]}
    #create_type = {'by_keywords':['互联网','乌镇'],'by_seed_users':[],'by_all_users':[]}
    create_time = time.time()
    submitter = 'admin@qq.com'
    remark = '这是备注'
    domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0)



