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
                        DESCRIPTION_TOP,DAILY_INTEREST_TOP_USER,MONITOR_TOP_USER,MAX_SEARCH_SIZE
from xnr.time_utils import get_flow_text_index_list,datetime2ts
from xnr.utils import nickname2uid,user_no2_id,_id2user_no
#from xnr.weibo_publish_func import getUserShow
from xnr.sina.userinfo import SinaOperateAPI
from xnr.sina.get_userinfo import get_userinfo
from xnr.sina.change_userinfo import change_userinfo
#from xnr.test_tianjin import get_user_portrait_data
from xnr.sina.tools.Launcher import SinaLauncher
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

def get_xnr_info_new(xnr_user_no):

    results = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']

    return results

def get_modify_base_info(task_detail):

    xnr_user_no = task_detail['xnr_user_no']

    item_exists = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,xnr_user_no=xnr_user_no)['_source']

    item_exists['active_time'] = task_detail['active_time']
    item_exists['day_post_average'] = task_detail['day_post_average']
    item_exists['daily_interests'] = task_detail['daily_interests']
    item_exists['monitor_keywords'] = task_detail['monitor_keywords']
    try:
        es.update(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body={'doc':item_exist})
        mark = True
    except:
        mark = False
        
    return mark


def get_modify_userinfo(task_detail):
    item_dict = {}
    nick_name = task_detail['nick_name']
    location_list = task_detail['location'].encode('utf-8').split('，')
    item_dict['location_province'] = location_list[0]
    item_dict['location_city'] = location_list[1]
    item_dict['description'] = task_detail['description']
    gender = task_detail['gender']
    if gender == u'男':
        item_dict['gender'] = 'man'
    else:
        item_dict['gender'] = 'woman'

    age = task_detail['age']
    birth_year = time.localtime().tm_year - age
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
    es_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']

    xnr_result = es_results[0]

    weibo_mail_account = xnr_result['weibo_mail_account']
    weibo_phone_account = xnr_result['weibo_phone_account']

    if weibo_mail_account:
        account_name = weibo_mail_account
    else:
        account_name = weibo_phone_account

    password = xnr_result['password']


    result = change_userinfo(account_name, password, item_dict)

    return result

def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    
    return _total

def get_add_other_info(task_detail):

    
    weibo_mail_account = task_detail['weibo_mail_account']
    weibo_phone_account = task_detail['weibo_phone_account']

    if weibo_mail_account:
        account_name = weibo_mail_account
    else:
        account_name = weibo_phone_account

    password = task_detail['password']
    
    nick_name = str(task_detail['nick_name'])
    print 'nick_name:', nick_name, type(nick_name)
    #print 'account_name:',account_name
    #print 'password::',password
    try:
    # # xnr = SinaLauncher(account_name,password)
    # # xnr.login()
    # # uid = xnr.uid
    # # print 'xnr::',xnr
    #     user = SinaOperateAPI().getUserShow(screen_name=nick_name)
    #     uid = user['uid']
    # #nick_name = xnr.screen_name
        user = SinaOperateAPI().getUserShow(screen_name=nick_name)
    except:
    #     #return '账户名或密码输入错误，请检查后输入！！'
    #     #return '昵称输入错误，请检查后输入！！'
        return 'nick_name error'
    
    #user = get_userinfo(account_name, password)
    print 'user:::',user
    item_dict = {}
    
    if user:
        print 'user::',user
        item_dict['nick_name'] = user['screen_name']
        item_dict['location'] = user['location']
        if user['gender']=='m':
            item_dict['gender'] = u'男'
        elif user['gender']=='f':
            item_dict['gender'] = u'女'
        #item_dict['gender'] = user['gender']
        #now_year = int(time.strftime('%Y',time.localtime(time.time())))
        #age = now_year - int(user['birth'][:4])
        #item_dict['age'] = age
        item_dict['age'] = '0'
        item_dict['description'] = user['description']
        item_dict['career'] = ''
    # print 'item_dict:::',item_dict
    # print 'task_detail:::',task_detail
    #new_task_detail = union_dict(task_detail,item_dict)
    new_task_detail = dict(task_detail,**item_dict)
    
    return new_task_detail

def get_nick_name_unique(nick_name):
    query_body = {
        'query':{
            'term':{'nick_name':nick_name}
        }
    }
    es_profile_results = es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,body=query_body)['hits']['hits']
    es_xnr_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']

    if es_profile_results and es_xnr_results:
        mark = False
    else:
        mark = True
    return mark

def get_show_domain():
    domain_name_dict = {}
    query_body = {'query':{'match_all':{}},'size':MAX_SEARCH_SIZE}
    es_results = es.search(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,body=query_body)['hits']['hits']
    if es_results:
        for result in es_results:
            result = result['_source']
            domain_name_dict[result['domain_pinyin']] = result['domain_name']
    return domain_name_dict

def get_show_weibo_xnr(submitter):
    weibo_xnr_dict = {}
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

    #query_body = {'query':{'term':{'create_status':2}},'size':MAX_SEARCH_SIZE}
    es_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
    if es_results:
        for result in es_results:
            #try:
            print 'result!!!',result
            result = result['_source']
            weibo_xnr_dict[result['xnr_user_no']] = result['nick_name']
            # except:
            #     print 'result::',result
            #     continue
    return weibo_xnr_dict

def get_role_sort_list(domain_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    try:
        es_result = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=domain_pinyin)['_source']

        #role_sort_list_en = json.loads(es_result['role_distribute'])
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
    print 'task_detail:::',task_detail
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
        nick_name_list = []
        user_location_top_list = []
        description_list = []
        sex_list = []
        #try:
        role_example_dict = {}
        member_uids = json.loads(es_result['member_uids'])
        member_uids_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
                                                body={'ids':member_uids})['docs']
        count = 0
        for result in member_uids_results:
            if result['found'] == True:
                result = result['_source'] 
                person_url = 'http://weibo.com/u/'+str(result['uid'])+'/home'
                nick_name = result['nick_name']
                nick_name_list.append(nick_name)
                sex_list.append(result['sex'])
                description_list.append(result['description'])
                role_example_dict[result['uid']] = [nick_name,person_url]
                count += 1
                if count > NICK_NAME_TOP:
                    break

        recommend_results['role_example'] = role_example_dict
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
    # create_time = time.time()
    
    # if S_TYPE == 'test':
    #     create_time = datetime2ts(S_DATE)
    
    # index_name_list = get_flow_text_index_list(create_time)
    
    # try:
    # query_body = {
    #     'query':{
    #         'filtered':{
    #             'filter':{
    #                 'terms':{'daily_interests':daily_interests_list}
    #             }
    #         }
    #     },
    #     'sort':{'user_fansnum':{'order':'desc'}},
    #     'size':DAILY_INTEREST_TOP_USER,
    #     '_source':['uid']
    # }

    # es_results = es_flow_text.search(index=index_name_list,doc_type='text',body=query_body)['hits']['hits']
  
    # daily_interest_uid_set = set()
    # for result in es_results:
    #     daily_interest_uid_set.add(result['_source']['uid'])
    # daily_interest_uid_list = list(daily_interest_uid_set)
    # es_daily_interests_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,\
    #                                         body={'ids':daily_interest_uid_list})['docs']
    # nick_name_list = []
    # sex_list = []
    # user_location_list = []
    # description_list = []
   
    # for result in es_daily_interests_results:
    #     if result['found'] == True:
    #         result = result['_source']
    #         nick_name_list.append(result['nick_name'])
    #         sex_list.append(result['sex'])
    #         user_location_list.append(result['user_location'])
    #         if result['description']:
    #             description_list.append(result['description'])
    sex_list_count = Counter(sex_list)
    print 'sex_list_count:::',sex_list_count
    sex_sort = sorted(sex_list_count.items(),key=lambda x:x[1],reverse=True)[:1][0][0]
  
    # user_location_list_count = Counter(user_location_list)
    # user_location_sort_top = sorted(user_location_list_count.items(),key=lambda x:x[1],reverse=True)[:USER_LOCATION_TOP]
    # user_location_top_list = []
    # for user_location in user_location_sort_top:
    #     user_location_top_list.append(user_location_sort[0])
    
        
    recommend_results['nick_name'] = '&'.join(nick_name_list)
    recommend_results['role_example'] = recommend_results['role_example']
    recommend_results['sex'] = sex_sort
    recommend_results['user_location'] = '&'.join(user_location_top_list)
    recommend_results['description'] = '&'.join(description_list[:DESCRIPTION_TOP])

    # except:
    #     print '没有找到日常兴趣相符的用户'
    #     recommend_results['nick_name'] = ''
    #     recommend_results['sex'] = ''
    #     recommend_results['user_location'] = ''
    #     recommend_results['description'] = ''
    ## 年龄、职业
    recommend_results['age'] = ''
    recommend_results['career'] = ''

    return recommend_results

    # except:
    #     return []

def get_recommend_follows(task_detail):
    recommend_results = dict()
    daily_interests_list = task_detail['daily_interests'].encode('utf-8').split('，')
    monitor_keywords_list = task_detail['monitor_keywords'].encode('utf-8').split('，')
    #print 'daily_interests_list::',daily_interests_list
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
        nick_name_dict = {} 
        es_daily_interests_results = es_daily_interests_results[:max(NICK_NAME_TOP,len(es_daily_interests_results))]
        for result in es_daily_interests_results:
            if result['found'] == True:
                result = result['_source']
                nick_name_dict[result['uid']] = result['nick_name']
            else:
                continue
        recommend_results['daily_interests'] = nick_name_dict

    except:
        print '没有找到日常兴趣相符的用户'
        recommend_results['daily_interests'] = {}

    ## 监测词关注
    nest_query_list = []
    #print 'monitor_keywords_list:::',monitor_keywords_list
    for monitor_keyword in monitor_keywords_list:
        nest_query_list.append({'wildcard':{'keywords_string':'*'+monitor_keyword+'*'}})
    #print 'nest_query_list::',nest_query_list
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
        #print '123'
        es_results = es_flow_text.search(index=index_name_list,doc_type='text',body=query_body_monitor)['hits']['hits']
        #print 'es_results::',es_results
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
                nick_name_dict[result['uid']] = result['nick_name']
            else:
                continue
        recommend_results['monitor_keywords'] = nick_name_dict

    except:
        print '没有找到监测词相符的用户'
        recommend_results['monitor_keywords'] = {}

    print 'recommend_results::',recommend_results
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

    #task_id = task_detail['task_id']
    es_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body={'query':{'match_all':{}},\
                    'sort':{'user_no':{'order':'desc'}}})['hits']['hits']
    if es_results:
        user_no_max = es_results[0]['_source']['user_no']
        user_no_current = user_no_max + 1 
    else:
        user_no_current = 1

    task_detail['user_no'] = user_no_current
    task_id = user_no2_id(user_no_current)  #五位数 WXNR0001
    #try:    
    #item_exist = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id)['_source']
    item_exist = dict()
    print 'task_detail::',task_detail
    item_exist['submitter'] = task_detail['submitter']
    item_exist['user_no'] = task_detail['user_no']
    item_exist['domain_name'] = task_detail['domain_name']
    item_exist['role_name'] = task_detail['role_name']
    item_exist['psy_feature'] = '&'.join(task_detail['psy_feature'].encode('utf-8').split('，'))
    item_exist['political_side'] = task_detail['political_side']
    item_exist['business_goal'] = '&'.join(task_detail['business_goal'].encode('utf-8').split('，'))
    item_exist['daily_interests'] = '&'.join(task_detail['daily_interests'].encode('utf-8').split('，'))
    item_exist['monitor_keywords'] = '&'.join(task_detail['monitor_keywords'].encode('utf-8').split('，'))
    #item_exist['sex'] = task_detail['sex']

    # item_exist['nick_name'] = task_detail['nick_name']
    # item_exist['age'] = task_detail['age']
    # item_exist['location'] = task_detail['location']
    # item_exist['career'] = task_detail['career']
    # item_exist['description'] = task_detail['description']
    item_exist['active_time'] = '&'.join(task_detail['active_time'].split('-'))
    item_exist['day_post_average'] = json.dumps(task_detail['day_post_average'].split('-'))
    item_exist['create_status'] = 1 # 第二步完成
    item_exist['xnr_user_no'] = task_id # 虚拟人编号
    item_exist['create_time'] = int(time.time())

    es.index(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id,body=item_exist)

    mark = True
    #except:        
    #    mark = False

    return mark,task_id


def get_save_step_three_1(task_detail):
    #task_id = task_detail['task_id']
    #try:
    #print 'task_detail:::',task_detail
    print 'nick_name:::',task_detail['nick_name']
    nick_name = task_detail['nick_name'].encode('utf-8')
    operate = SinaOperateAPI()
    user_info = operate.getUserShow(screen_name=nick_name)
    uid = user_info['id']
    try:
        if task_detail['weibo_mail_account']:
            uname = task_detail['weibo_mail_account']
        else:
            uname = task_detail['weibo_phone_account']
        xnr = SinaLauncher(uname, task_detail['password'])
        xnr.login()
        uid = xnr.uid
    except:
        return '账户名或密码输入错误，请检查后输入！！'
    #uid = getUserShow(screen_name=nick_name)['data']['uid']
    #query_body = {'query':{'term':{'nick_name':nick_name}},'sort':{'user_no':{'order':'desc'}}}
    query_body = {'query':{'match_all':{}},'sort':{'user_no':{'order':'desc'}}}
    print 'query_body:::',query_body
    es_result = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
    task_id = es_result[0]['_source']['xnr_user_no']
    item_exist = es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id)['_source']
    item_exist['uid'] = uid
    item_exist['nick_name'] = task_detail['nick_name']
    item_exist['weibo_mail_account'] = task_detail['weibo_mail_account']
    item_exist['weibo_phone_account'] = task_detail['weibo_phone_account']
    item_exist['password'] = task_detail['password']
    item_exist['create_status'] = 2 # 创建完成

    # 更新 weibo_xnr表
    print es.update(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=task_id,body={'doc':item_exist})        

    mark =True
        
    #except:        
        #mark = False
    return mark

def get_save_step_three_2(task_detail):
    task_id = task_detail['task_id']
    nick_name = task_detail['nick_name']
    #query_body = {'query':{'term':{'nick_name':nick_name}},'sort':{'user_no':{'order':'desc'}}}
    #es_result = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
    #task_id = es_result[0]['_source']['xnr_user_no']
    #插入 weibo_xnr_fans_followers表

    try:
        item_fans_followers = dict()
        #followers_nickname_list = task_detail['followers_nickname'].encode('utf-8').split('，')
        #print 'followers_nickname_list::',followers_nickname_list

        #followers_list = nickname2uid(followers_nickname_list)
        #print 'followers_list::',followers_list
        followers_uids = list(set(task_detail['followers_uids'].split('，')))
        print 'followers_uids::',followers_uids
        item_fans_followers['followers_list'] = followers_uids
        item_fans_followers['xnr_user_no'] = task_id
        print 'item_fans_followers::',item_fans_followers
        es.index(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=task_id,body=item_fans_followers)
        mark = True
    except:        
        mark = False

    return mark

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

    es_results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']

    return es_results
    
        

def get_domain_info(domain_pinyin):

    domain_info = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=domain_pinyin)['_source']

    return domain_info

def get_role_info(domain_pinyin,role_name):

    role_en = domain_ch2en_dict(role_name)

    role_info_id = domain_pinyin + '_' + role_en

    role_info = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=role_info_id)['_source']

    return role_info


# def domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0):
#     domain_task_dict = dict()
#     if S_TYPE == 'test':
#         domain_task_dict['domain_pinyin'] = pinyin.get(domain_name,format='strip',delimiter='_')
#         domain_task_dict['domain_name'] = domain_name
#         domain_task_dict['create_type'] = json.dumps(create_type)
#         domain_task_dict['create_time'] = create_time
#         domain_task_dict['submitter'] = submitter
#         domain_task_dict['remark'] = remark
#         domain_task_dict['compute_status'] = compute_status
#     r.lpush(weibo_target_domain_detect_queue_name,json.dumps(domain_task_dict))
#     #r.delete(weibo_target_domain_detect_queue_name)
#     print 'success!'

if __name__ == '__main__':
    domain_name =  '维权群体'
    
    #domain_name =  '乌镇'
    create_type = {'by_keywords':['维权','律师'],'by_seed_users':[],'by_all_users':[]}
    #create_type = {'by_keywords':['互联网','乌镇'],'by_seed_users':[],'by_all_users':[]}
    create_time = time.time()
    submitter = 'admin@qq.com'
    remark = '这是备注'
    domain_create_task(domain_name,create_type,create_time,submitter,remark,compute_status=0)



