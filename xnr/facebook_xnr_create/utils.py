#-*- coding: utf-8 -*-

'''
use to save function to create xnr info
'''
import pinyin
import json
import time
import os
import sys
import pandas as pd
from collections import Counter
import numpy as np
import random
from xnr.global_config import S_TYPE, S_DATE_FB as S_DATE
from xnr.global_utils import es_xnr as es
#facebook_user
from xnr.global_utils import r, es_fb_user_profile as es_user_profile, \
                            facebook_user_index_type as profile_index_type, \
                            facebook_user_index_name as profile_index_name
from xnr.global_utils import r, fb_xnr_index_name, fb_xnr_index_type,\
                            fb_domain_index_name, fb_domain_index_type,\
                            fb_role_index_name, fb_role_index_type, \
                            fb_xnr_fans_followers_index_name, fb_xnr_fans_followers_index_type,\
                            fb_xnr_max_no
from xnr.parameter import fb_domain_ch2en_dict,fb_domain_en2ch_dict
from xnr.parameter import ACTIVE_TIME_TOP,DAILY_INTEREST_TOP_USER,NICK_NAME_TOP,USER_LOCATION_TOP,\
                        DESCRIPTION_TOP,DAILY_INTEREST_TOP_USER,MONITOR_TOP_USER,MAX_SEARCH_SIZE
from xnr.time_utils import get_facebook_flow_text_index_list as get_flow_text_index_list, datetime2ts
from xnr.utils import user_no2fb_id, add_operate2redis
trans_path = os.path.join(os.path.abspath(os.getcwd()), 'xnr/cron/trans/')
sys.path.append(trans_path)
from trans import trans, simplified2traditional

sys.path.append(os.path.join(os.path.abspath(os.getcwd()), 'xnr/facebook/'))
from userinfo import Userinfo
from fb_operate import Operation

# from xnr.facebook.fb_operate import Operation as FbOperateAPI
# from xnr.sina.userinfo import SinaOperateAPI
from xnr.sina.change_userinfo import change_userinfo
# from xnr.sina.tools.Launcher import SinaLauncher
es_flow_text = es

def get_nick_name_unique(nick_name):
    query_body = {
        'query':{
            'term':{'nick_name':nick_name}
        }
    }
    es_profile_results = es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,body=query_body)['hits']['hits']
    es_xnr_results = es.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
    if es_profile_results and es_xnr_results:
        mark = False
    else:
        mark = True
    return mark

def get_show_domain():
    domain_name_dict = {}
    query_body = {'query':{'match_all':{}},'size':MAX_SEARCH_SIZE}
    es_results = es.search(index=fb_domain_index_name,doc_type=fb_domain_index_type,body=query_body)['hits']['hits']
    if es_results:
        for result in es_results:
            result = result['_source']
            domain_name_dict[result['domain_pinyin']] = result['domain_name']
    return domain_name_dict

def get_show_fb_xnr(submitter):
    fb_xnr_dict = {}
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'submitter':submitter}},
                    {'term':{'create_status':2}}
                ]
            }
        },
        'size':MAX_SEARCH_SIZE
    }
    es_results = es.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
    if es_results:
        for result in es_results:
            result = result['_source']
            fb_xnr_dict[result['xnr_user_no']] = result['nick_name']
    return fb_xnr_dict

def get_role_sort_list(domain_name):
    domain_pinyin = pinyin.get(domain_name, format='strip',delimiter='_')
    try:
        es_result = es.get(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=domain_pinyin)['_source']
        print 'es_result'
        print es_result
        role_sort_list_en = json.loads(es_result['role_distribute'])
        print 'role_sort_list_en'
        print role_sort_list_en
        role_sort_list_zh = []
        for item in role_sort_list_en:
            role_zh = fb_domain_en2ch_dict[item[0]]
            print 'role_zh'
            print role_zh
            role_sort_list_zh.append(role_zh)
        return role_sort_list_zh
    except:
        return []

def get_role2feature_info(domain_name,role_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_name_en = fb_domain_ch2en_dict[role_name]
    _id = domain_pinyin + '_' + role_name_en
    try:
        es_result = es.get(index=fb_role_index_name,doc_type=fb_role_index_type,id=_id)['_source']
        
        feature_info_dict = es_result        
        feature_filter_dict = dict()

        feature_filter_dict['political_side'] = json.loads(feature_info_dict['political_side'])
        try:
            feature_filter_dict['psy_feature'] = json.loads(feature_info_dict['psy_feature'])
        except:
            feature_filter_dict['psy_feature'] = []
        return feature_filter_dict

    except:
        return []

def get_recommend_step_two(task_detail):
    domain_name = task_detail['domain_name']
    role_name = task_detail['role_name']
    # daily_interests_list = task_detail['daily_interests'].encode('utf-8').split('，')

    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_name_en = fb_domain_ch2en_dict[role_name]
    _id = domain_pinyin + '_' + role_name_en

    recommend_results = dict()
    ## 根据角色信息
    es_result = es.get(index=fb_role_index_name,doc_type=fb_role_index_type,id=_id)['_source']
    #### 角色实例
    nick_name_list = []
    user_location_top_list = []
    description_list = []
    sex_list = []
    role_example_dict = {}
    member_uids = json.loads(es_result['member_uids'])
    member_uids_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                                            body={'ids':member_uids})['docs']
    count = 0
    for result in member_uids_results:
        if result['found'] == True:
            result = result['_source'] 
            person_url = "https://www.facebook.com/profile.php?id=" + str(result['uid'])
            if result.has_key('name'):
                nick_name = result['name']
                nick_name_list.append(nick_name)
            if result.has_key('gender'):
                if result['gender'] == 'male':
                    sex = 1
                elif result['gender'] == 'female':
                    sex = 2
                sex_list.append(sex)
            if result.has_key('description'):
                description_list.append(result['description'])

            role_example_dict[result['uid']] = [nick_name,person_url]
            count += 1
            if count > NICK_NAME_TOP:
                break
    recommend_results['role_example'] = role_example_dict
    active_time_list_np = np.array(json.loads(es_result['active_time']))
    active_time_list_np_sort = list(np.argsort(-active_time_list_np)[:ACTIVE_TIME_TOP])
    
    recommend_results['active_time'] = active_time_list_np_sort
    
    day_post_num = json.loads(es_result['day_post_num'])
    day_post_num_new = pd.Series(day_post_num)
    day_post_num_new = day_post_num_new.fillna(0)
    day_post_num_new = list(day_post_num_new)
    day_post_num_average = sum(day_post_num_new)/float(len(day_post_num_new))
    recommend_results['day_post_num_average'] = day_post_num_average
    
    sex_sort = ''
    if sex_list:
        sex_list_count = Counter(sex_list)
        sex_sort = sorted(sex_list_count.items(),key=lambda x:x[1],reverse=True)[:1][0][0]  
    recommend_results['nick_name'] = '&'.join(nick_name_list)
    recommend_results['role_example'] = recommend_results['role_example']
    recommend_results['sex'] = sex_sort
    recommend_results['user_location'] = '&'.join(user_location_top_list)
    recommend_results['description'] = '&'.join(description_list[:DESCRIPTION_TOP])
    recommend_results['age'] = ''
    recommend_results['career'] = ''
    return recommend_results

def get_modify_userinfo(task_detail):
    item_dict = {}
    nick_name = task_detail['nick_name']
    location_list = task_detail['location'].encode('utf-8').split('，')
    try:
        item_dict['location_province'] = location_list[0]
        item_dict['location_city'] = location_list[1]
    except:
        item_dict['location_province'] = location_list[0]
        item_dict['location_city'] = location_list[0]

    item_dict['description'] = task_detail['description']
    gender = task_detail['gender']
    if gender == u'男':
        item_dict['gender'] = 'man'
    else:
        item_dict['gender'] = 'woman'

    age = task_detail['age']
    birth_year = time.localtime().tm_year - int(age)
    month = '%02d'%random.randint(0,13)
    day = '%02d'%random.randint(0,29)
    item_dict['birth'] = [str(birth_year),month,day]

    query_body = {  
        'query':{
            'filtered':{
                'filter':{
                    'term':{'nick_name':nick_name}
                }
            }
        }
    }
    es_results = es.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
    xnr_result = es_results[0]['_source']
    try:
        fb_mail_account = xnr_result['fb_mail_account']
    except:
        fb_mail_account = ''
    try:
        fb_phone_account = xnr_result['fb_phone_account']
    except:
        fb_phone_account = ''

    if fb_mail_account:
        account_name = fb_mail_account
    else:
        account_name = fb_phone_account
    password = xnr_result['password']
    uid = xnr_result['uid']
    try:
        result = change_userinfo(account_name, password,uid, item_dict)
    except:
        result = False
    return result

def get_recommend_follows(task_detail):
    recommend_results = dict()
    # daily_interests_list = task_detail['daily_interests'].split('，')
    monitor_keywords_list = task_detail['monitor_keywords'].split('，')
    create_time = time.time()        
    if S_TYPE == 'test':
        create_time = datetime2ts(S_DATE)
    index_name_list = get_flow_text_index_list(create_time)
    '''#FB flow_text中没有daily_interests字段
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
            # 'sort':{'user_fansnum':{'order':'desc'}},
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
        nick_name_dict = {} 
        es_daily_interests_results = es_daily_interests_results[:max(NICK_NAME_TOP,len(es_daily_interests_results))]
        for result in es_daily_interests_results:
            if result['found'] == True:
                result = result['_source']
                nick_name_dict[result['uid']] = result['nick_name']
            else:
                continue
        recommend_results['daily_interests'] = nick_name_dict

    except Exception,e:
        print e
        print '没有找到日常兴趣相符的用户'
        recommend_results['daily_interests'] = {}
    '''
    ## 监测词关注
    nest_query_list = []
    #文本中可能存在英文或者繁体字，所以都匹配一下
    monitor_en_keywords_list = trans(monitor_keywords_list, target_language='en')
    for i in range(len(monitor_keywords_list)):
        monitor_keyword = monitor_keywords_list[i]
        monitor_traditional_keyword = simplified2traditional(monitor_keyword)
        
        if len(monitor_en_keywords_list) == len(monitor_keywords_list): #确保翻译没出错
            monitor_en_keyword = monitor_en_keywords_list[i]
            nest_query_list.append({'wildcard':{'keywords_string':'*'+monitor_en_keyword+'*'}})
        
        nest_query_list.append({'wildcard':{'keywords_string':'*'+monitor_keyword+'*'}})
        nest_query_list.append({'wildcard':{'keywords_string':'*'+monitor_traditional_keyword+'*'}})
    try:
        query_body_monitor = {
            'query':{
                'bool':{
                    # 'must':nest_query_list
                    'should':nest_query_list
                }     
            },
            # 'sort':{'user_fansnum':{'order':'desc'}},
            'size':MONITOR_TOP_USER,
            '_source':['uid']
        }
        es_results = es_flow_text.search(index=index_name_list,doc_type='text',body=query_body_monitor)['hits']['hits']
        monitor_keywords_uid_set = set()
        for result in es_results:
            monitor_keywords_uid_set.add(result['_source']['uid'])
        monitor_keywords_uid_list = list(monitor_keywords_uid_set)

        es_monitor_keywords_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                                                body={'ids':monitor_keywords_uid_list})['docs']
        nick_name_dict = {}   
        es_monitor_keywords_results = es_monitor_keywords_results[:max(NICK_NAME_TOP,len(es_monitor_keywords_results))]     
        for result in es_monitor_keywords_results:
            if result['found'] == True:
                result = result['_source']
                nick_name_dict[result['uid']] = result['name']
            else:
                continue
        recommend_results['monitor_keywords'] = nick_name_dict
    except Exception,e:
        print e
        print '没有找到监测词相符的用户'
        recommend_results['monitor_keywords'] = {}
    return recommend_results

def get_save_step_one(task_detail):
    es_results = es.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body={'query':{'match_all':{}},\
                    'sort':{'user_no':{'order':'desc'}}})['hits']['hits']
    if es_results:
        user_no_max = es_results[0]['_source']['user_no']
        user_no_current = user_no_max + 1 
    else:
        user_no_current = 1
    task_detail['user_no'] = user_no_current
    task_id = user_no2fb_id(user_no_current)  #五位数 WXNR0001
    print 'task_id'
    print task_id
    try:    
        item_exist = dict()
        item_exist['user_no'] = task_detail['user_no']
        item_exist['domain_name'] = task_detail['domain_name']
        item_exist['role_name'] = task_detail['role_name']
        item_exist['psy_feature'] = '&'.join(task_detail['psy_feature'].encode('utf-8').split('，'))
        item_exist['political_side'] = task_detail['political_side']
        item_exist['business_goal'] = '&'.join(task_detail['business_goal'].encode('utf-8').split('，'))
        # item_exist['daily_interests'] = '&'.join(task_detail['daily_interests'].encode('utf-8').split('，'))
        item_exist['monitor_keywords'] = '&'.join(task_detail['monitor_keywords'].encode('utf-8').split('，'))
        item_exist['create_status'] = 0 # 第一步完成
        print es.index(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=task_id,body=item_exist)
        mark = True
    except:
        mark = False
    return mark

def get_fb_xnr_no():
    user_no_max = 0
    if not r.exists(fb_xnr_max_no): #如果当前redis没有记录，则去es数据库查找补上
        es_results = es.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body={'query':{'match_all':{}},\
                    'sort':{'user_no':{'order':'desc'}}})['hits']['hits']
        if es_results:
            user_no_max = es_results[0]['_source']['user_no']
    else:   #如果当前redis有记录，则取用
        user_no_max = int(r.get(fb_xnr_max_no))
    return user_no_max
    
def get_save_step_two(task_detail):
    #update
    user_no_max = get_fb_xnr_no()
    user_no_current = user_no_max + 1
    r.set(fb_xnr_max_no, user_no_current)
    
    task_detail['user_no'] = user_no_current
    task_id = user_no2fb_id(user_no_current)  #五位数 FXNR0001
    
    item_exist = dict()
    item_exist['submitter'] = task_detail['submitter']
    item_exist['user_no'] = task_detail['user_no']
    item_exist['domain_name'] = task_detail['domain_name']
    item_exist['role_name'] = task_detail['role_name']
    item_exist['psy_feature'] = '&'.join(task_detail['psy_feature'].encode('utf-8').split('，'))
    item_exist['political_side'] = task_detail['political_side']
    item_exist['business_goal'] = '&'.join(task_detail['business_goal'].encode('utf-8').split('，'))
    # item_exist['daily_interests'] = '&'.join(task_detail['daily_interests'].encode('utf-8').split('，'))
    item_exist['monitor_keywords'] = ','.join(task_detail['monitor_keywords'].encode('utf-8').split('，'))

    item_exist['active_time'] = '&'.join(task_detail['active_time'].split('-'))
    item_exist['day_post_average'] = json.dumps(task_detail['day_post_average'].split('-'))
    item_exist['create_status'] = 1 # 第二步完成
    item_exist['xnr_user_no'] = task_id # 虚拟人编号
    item_exist['create_time'] = int(time.time())
    print es.index(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=task_id,body=item_exist)
    mark = True
    return mark,task_id

def get_xnr_info(task_detail):
    nick_name = task_detail['nick_name']
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'nick_name':nick_name}
                }
            }
        }
    }
    es_results = es.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
    return es_results

def get_add_other_info(task_detail):
    fb_mail_account = task_detail['fb_mail_account']
    fb_phone_account = task_detail['fb_phone_account']
    if fb_mail_account:
        account_name = fb_mail_account
    else:
        account_name = fb_phone_account
    password = task_detail['password']
    nick_name = str(task_detail['nick_name'])
    try:
        user = Userinfo(account_name, password)
        info_dict = user.getUserinfo()
    except Exception,e:
        print e
        return 'account error'
    item_dict = {}
    if user:
        item_dict['nick_name'] = nick_name
        item_dict['id'] = info_dict['id']
        item_dict['location'] = info_dict['location']
        item_dict['age'] = info_dict['age']
        item_dict['description'] = info_dict['description']
        item_dict['career'] = info_dict['career']
    new_task_detail = dict(task_detail,**item_dict)
    return new_task_detail

def get_save_step_three_1(task_detail):
    task_id = task_detail['task_id']
    # query_body = {'query':{'match_all':{}},'sort':{'user_no':{'order':'desc'}}}
    # es_result = es.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
    # task_id = es_result[0]['_source']['xnr_user_no']
    item_exist = es.get(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=task_id)['_source']
    
    item_exist['uid'] = task_detail['id']
    item_exist['nick_name'] = task_detail['nick_name']
    item_exist['fb_mail_account'] = task_detail['fb_mail_account']
    item_exist['fb_phone_account'] = task_detail['fb_phone_account']
    item_exist['password'] = task_detail['password']
    item_exist['career'] = task_detail['career']
    item_exist['description'] = task_detail['description']
    item_exist['age'] = task_detail['age']
    item_exist['location'] = task_detail['location']
    item_exist['create_status'] = 2 # 创建完成
    # 更新 fb_xnr表
    print es.update(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=task_id,body={'doc':item_exist})        
    mark =True
    return mark

def get_save_step_three_2(task_detail):
    task_id = task_detail['task_id']
    # nick_name = task_detail['nick_name']
    try:
        item_fans_followers = dict()
        followers_uids = list(set(task_detail['followers_uids'].split('，')))
        item_fans_followers['followers_list'] = followers_uids
        item_fans_followers['xnr_user_no'] = task_id
        print es.index(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,id=task_id,body=item_fans_followers)
        #把关注任务加到redis队列中
        for followers_uid in followers_uids:
            queue_dict = {
                'channel': 'facebook',
                'operate_type': 'add',
                'content': {
                    'xnr_user_no': task_id,
                    'uid': followers_uid
                }
            }
            if not add_operate2redis(queue_dict):
                mark = False
                return mark
        mark = True
    except:        
        mark = False
    return mark

def get_xnr_info_new(xnr_user_no):
    results = es.get(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=xnr_user_no)['_source']
    return results

def get_modify_base_info(task_detail):
    xnr_user_no = task_detail['xnr_user_no']
    item_exists = es.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']
    if task_detail.has_key('active_time'):
        item_exists['active_time'] = task_detail['active_time']
    if task_detail.has_key('day_post_average'): 
        day_post_average = task_detail['day_post_average'].split('-')
        item_exists['day_post_average'] = json.dumps(day_post_average)
    if task_detail.has_key('monitor_keywords'): 
        item_exists['monitor_keywords'] = task_detail['monitor_keywords']
    try:
        es.update(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,body={'doc':item_exists}, id=xnr_user_no)
        mark = True
    except Exception,e:
        print e
        mark = False
    return mark

def get_domain_info(domain_pinyin):
    domain_info = es.get(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=domain_pinyin)['_source']
    return domain_info

def get_role_info(domain_pinyin,role_name):
    role_en = fb_domain_ch2en_dict(role_name)
    role_info_id = domain_pinyin + '_' + role_en
    role_info = es.get(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=role_info_id)['_source']
    return role_info

def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    return _total

if __name__ == '__main__':
    '''
    domain_name =  '维权群体'
    
    #domain_name =  '乌镇'
    create_type = {'by_keywords':['维权','律师'],'by_seed_users':[],'by_all_users':[]}
    #create_type = {'by_keywords':['互联网','乌镇'],'by_seed_users':[],'by_all_users':[]}
    create_time = time.time()
    submitter = 'admin@qq.com'
    remark = '这是备注'
    domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0)
    '''
    print get_fb_xnr_no()
