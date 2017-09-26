#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import pinyin
import numpy as np
from xnr.global_config import S_TYPE
from xnr.global_utils import es_xnr as es
from xnr.global_utils import es_user_portrait
from xnr.global_utils import r,weibo_target_domain_detect_queue_name,es_user_portrait,portrait_index_name,portrait_index_type,weibo_date_remind_index_name,weibo_date_remind_index_type,\
                            weibo_sensitive_words_index_name,weibo_sensitive_words_index_type,\
                            weibo_hidden_expression_index_name,weibo_hidden_expression_index_type,\
                            weibo_xnr_corpus_index_name,weibo_xnr_corpus_index_type,\
                            weibo_domain_index_name,weibo_domain_index_type,weibo_role_index_name,\
                            weibo_role_index_type,weibo_example_model_index_name,\
                            weibo_example_model_index_type,profile_index_name,profile_index_type
from xnr.time_utils import ts2datetime
from xnr.parameter import MAX_VALUE,MAX_SEARCH_SIZE,domain_ch2en_dict,topic_en2ch_dict,domain_en2ch_dict,\
                        EXAMPLE_MODEL_PATH,TOP_ACTIVE_TIME
from xnr.utils import uid2nick_name_photo,judge_sensing_sensor,judge_follow_type,get_influence_relative

'''
领域知识库
'''

#use to merge dict
#input: dict1, dict2, dict3...
#output: merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    
    return _total

def get_generate_example_model(xnr_user_no,domain_name,role_name):

    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_en = domain_ch2en_dict[role_name]

    task_id = domain_pinyin + '_' + role_en

    es_result = es.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=task_id)['_source']
    item = es_result

    role_group_uids = json.loads(item['member_uids'])

    mget_results = es_user_portrait.mget(index=portrait_index_name,doc_type=portrait_index_type,body={'ids':role_group_uids})['docs']

    topic_list = []
    for mget_item in mget_results:
        
        if mget_item['found']:
            keywords_list = json.loads(mget_item['_source']['keywords'])
            topic_list.extend(keywords_list)
    
    topic_keywords_dict = {}
    for topic_item in topic_list:
        keyword = topic_item[0]
        keyword_count = topic_item[1]
        try:
            topic_keywords_dict[keyword] += keyword_count
        except:
            topic_keywords_dict[keyword] = keyword_count

    monitor_keywords_list = []
    for i in range(3):
        
        keyword_max = max(topic_keywords_dict,key=topic_keywords_dict.get)
        monitor_keywords_list.append(keyword_max)
        del topic_keywords_dict[keyword_max]

    item['monitor_keywords'] = '&'.join(monitor_keywords_list)

    for mget_item in mget_results:
        if mget_item['found']:
            item['nick_name'] = mget_item['_source']['uname']
            item['location'] = mget_item['_source']['location']
            item['gender'] = mget_item['_source']['gender']
            uid = mget_item['_source']['uid']
            try:
                profile_results = es_user_portrait.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
                if profile_results['description']:
                    item['description'] = profile_results['description']
                    break
            except:
                pass

    item['business_goal'] = u'渗透'
    item['daily_interests'] = u'数码'
    # if S_TYPE == 'test':
    #     user_mget_results = es.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':role_group_uids})['docs']
    #     if user_mget_results
    item['age'] = 30
    item['career'] = u'自由职业'

    active_time_list_np = np.array(json.loads(item['active_time']))
    active_time_list_np_sort = np.argsort(-active_time_list_np)[:TOP_ACTIVE_TIME]
    item['active_time'] = active_time_list_np_sort.tolist()

    day_post_num_list = np.array(json.loads(item['day_post_num']))
    item['day_post_num'] = np.mean(day_post_num_list).tolist()
    
    example_model_file_name = EXAMPLE_MODEL_PATH + task_id + '.json'
    
    try:
        with open(example_model_file_name,"w") as dump_f:
            json.dump(item,dump_f)

        
        item_dict = dict()
        item_dict['xnr_user_no'] = xnr_user_no
        item_dict['domain_name'] = domain_name
        item_dict['role_name'] = role_name

        es.index(index=weibo_example_model_index_name,doc_type=weibo_example_model_index_type,\
            body=item_dict,id=task_id)

        mark = True
    except:
        mark = False

    return mark

def get_show_example_model(xnr_user_no):
    print 'es::',es
    print 'weibo_example_model_index_name:::',weibo_example_model_index_name
    print 'weibo_example_model_index_type:::',weibo_example_model_index_type
    print 'xnr_user_no::',xnr_user_no
    #print '!!!!!',{'query':{'term':{'xnr_user_no':xnr_user_no}}}
    es_results = es.search(index=weibo_example_model_index_name,doc_type=weibo_example_model_index_type,\
        body={'query':{'term':{'xnr_user_no':xnr_user_no}}})['hits']['hits']

    result_all = []
    for result in es_results:
        result = result['_source']
        result_all.append(result)
        
    return result_all


def get_export_example_model(domain_name,role_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_en = domain_ch2en_dict[role_name]

    task_id = domain_pinyin + '_' + role_en
    example_model_file_name = EXAMPLE_MODEL_PATH + task_id + '.json'
    with open(example_model_file_name,"r") as dump_f:
        es_result = json.load(dump_f)

    return es_result

def get_create_type_content(create_type,keywords_string,seed_users,all_users):

    create_type_new = {}
    create_type_new['by_keywords'] = []
    create_type_new['by_seed_users'] = []
    create_type_new['by_all_users'] = []

    if create_type == 'by_keywords':
        create_type_new['by_keywords'] = keywords_string.encode('utf-8').split('，')
    elif create_type == 'by_seed_users':
        create_type_new['by_seed_users'] = seed_users.encode('utf-8').split('，')
    else:
        create_type_new['all_users'] = all_users.encode('utf-8').split('，')

    return create_type_new

def domain_create_task(xnr_user_no,domain_name,create_type,create_time,submitter,description,remark,compute_status=0):
    
    try:
        domain_task_dict = dict()

        domain_task_dict['xnr_user_no'] = xnr_user_no
        domain_task_dict['domain_pinyin'] = pinyin.get(domain_name,format='strip',delimiter='_')
        domain_task_dict['domain_name'] = domain_name
        domain_task_dict['create_type'] = json.dumps(create_type)
        domain_task_dict['create_time'] = create_time
        domain_task_dict['submitter'] = submitter
        domain_task_dict['description'] = description
        domain_task_dict['remark'] = remark
        domain_task_dict['compute_status'] = compute_status

        r.lpush(weibo_target_domain_detect_queue_name,json.dumps(domain_task_dict))

        item_exist = dict()
        
        item_exist['xnr_user_no'] = domain_task_dict['xnr_user_no']
        item_exist['domain_pinyin'] = domain_task_dict['domain_pinyin']
        item_exist['domain_name'] = domain_task_dict['domain_name']
        item_exist['create_type'] = domain_task_dict['create_type']
        item_exist['create_time'] = domain_task_dict['create_time']
        item_exist['submitter'] = domain_task_dict['submitter']
        item_exist['description'] = domain_task_dict['description']
        item_exist['remark'] = domain_task_dict['remark']
        item_exist['group_size'] = ''
        
        item_exist['compute_status'] = 0  # 存入创建信息
        es.index(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=item_exist['domain_pinyin'],body=item_exist)


        mark = True
    except:
        mark =False

    return mark

def get_show_domain_group_summary(xnr_user_no):

    es_result = es.search(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,\
                body={'query':{'term':{'xnr_user_no':xnr_user_no}}})['hits']['hits']

    if es_result:
        result_all = []
        for result in es_result:
            item = {}
            result = result['_source']
            print 'result::',result
            item['group_size'] = result['group_size']
            item['domain_name'] = result['domain_name']
            item['create_time'] = result['create_time']
            item['compute_status'] = result['compute_status']
            item['create_type'] = result['create_type']
            item['remark'] = result['remark']
            item['description'] = result['description']

            create_type = json.loads(result['create_type'].encode('utf-8'))

            # if not create_type['by_keywords']:
            #     item['create_type'] = 'by_keywords'
            # elif not create_type['by_seed_users']:
            #     item['create_type'] = 'by_seed_users'
            # elif not create_type['by_all_users']:
            #     item['create_type'] = 'by_all_users'

            result_all.append(item)
    else:
        return '当前虚拟人尚未创建渗透领域'

    return result_all


## 查看群体画像信息
def get_show_domain_group_detail_portrait(xnr_user_no,domain_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    es_result = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,\
                id=domain_pinyin)['_source']

    member_uids = es_result['member_uids']

    es_mget_result = es_user_portrait.mget(index=portrait_index_name,doc_type=portrait_index_type,\
                    body={'ids':member_uids})['docs']
    result_all = []
    for result in es_mget_result:
        item = {}
        if result['found']:
            result = result['_source']
            item['uid'] = result['uid']
            item['nick_name'] = result['uname']
            item['photo_url'] = result['photo_url']
            item['domain'] = result['domain']
            item['sensitive'] = result['sensitive']
            item['location'] = result['location']
            item['fans_num'] = result['fansnum']
            item['friends_num'] = result['friendsnum']
            item['gender'] = result['gender']
            item['home_page'] = 'http://weibo.com/'+result['uid']+'/profile?topnav=1&wvr=6&is_all=1'
            item['sensor_mark'] = judge_sensing_sensor(xnr_user_no,item['uid'])
            item['weibo_type'] = judge_follow_type(xnr_user_no,item['uid'])
            item['influence'] = get_influence_relative(item['uid'],result['influence'])

        else:
            item['uid'] = result['_id']
            item['nick_name'] = ''
            item['photo_url'] = ''
            item['domain'] = ''
            item['sensitive'] = ''
            item['location'] = ''
            item['fans_num'] = ''
            item['friends_num'] = ''
            item['gender'] = ''
            item['home_page'] = 'http://weibo.com/'+result['_id']+'/profile?topnav=1&wvr=6&is_all=1'
            item['sensor_mark'] = judge_sensing_sensor(xnr_user_no,result['_id'])
            item['weibo_type'] = judge_follow_type(xnr_user_no,result['_id'])
            item['influence'] = ''
        
        result_all.append(item)

    return result_all


def get_show_domain_description(xnr_user_no,domain_name):

    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    es_result = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,\
                id=domain_pinyin)['_source']
    item = {}

    item['group_size'] = es_result['group_size']
    item['description'] = es_result['description']
    topic_preference_list = json.loads(es_result['topic_preference'])
    topic_preference_list_chinese = []
    for topic_preference_item in topic_preference_list:
        topic_preference_item_chinese = topic_en2ch_dict[topic_preference_item[0]]
        topic_preference_list_chinese.append([topic_preference_item_chinese,topic_preference_item[1]])

    item['topic_preference'] = topic_preference_list_chinese
    item['word_preference'] = json.loads(es_result['top_keywords'])
    role_distribute_list = json.loads(es_result['role_distribute'])
    role_distribute_list_chinese = []
    for role_distribute_item in role_distribute_list:
        role_distribute_item_chinese = domain_en2ch_dict[role_distribute_item[0]]
        role_distribute_list_chinese.append([role_distribute_item_chinese,role_distribute_item[1]])

    item['role_distribute'] = role_distribute_list_chinese
    political_side_list = json.loads(es_result['political_side'])
    political_side_list_chinese = []
    for political_side_item in political_side_list:
        if political_side_item[0] == 'mid':
            political_side_list_chinese.append([u'中立',political_side_item[1]])
        elif political_side_item[0] == 'right':
            political_side_list_chinese.append([u'右倾',political_side_item[1]])
        else:
            political_side_list_chinese.append([u'左倾',political_side_item[1]])

    item['political_side'] = political_side_list_chinese

    return item

def get_show_domain_role_info(domain_name,role_name):

    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_en = domain_ch2en_dict[role_name]

    task_id = domain_pinyin + '_' + role_en

    es_result = es.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=task_id)['_source']

    return es_result

def get_delete_domain(domain_name):

    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    try:
        es.delete(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=domain_pinyin)
        mark = True
    except:
        mark = False

    return mark

###################################################################
###################   Business Knowledge base    ##################
###################################################################

###########functional module 1: sensitive words manage  ###########

#step 1:    create sensitive words
def get_create_sensitive_words(rank,sensitive_words,create_type,create_time):
    task_detail = dict()
    task_detail['rank'] = rank
    task_detail['sensitive_words'] = sensitive_words
    task_detail['create_type'] = create_type
    task_detail['create_time'] = create_time
    task_id = sensitive_words
    try:
        es.index(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=task_id,body=task_detail)
        mark = True
    except:
        mark = False

    return mark

#step 2:    show the list of sensitive words
#step 2.1:  show the list of sensitive words default
def show_sensitive_words_default():
    query_body={
        'query':{
            'match_all':{}
        },
        'size':MAX_SEARCH_SIZE,
        'sort':{'create_time':{'order':'desc'}}
    }
    result=es.search(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        results.append(item['_source'])
    return results

#step 2.2:  show the list of sensitive words according to the condition
def show_sensitive_words_condition(create_type,rank):
    show_condition_list=[]
    if create_type and rank:
       show_condition_list.append({'term':{'create_type':create_type}})    
       show_condition_list.append({'term':{'rank':rank}})
    elif create_type:
        show_condition_list.append({'term':{'create_type':create_type}})    
    elif rank:
        show_condition_list.append({'term':{'rank':rank}})

    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':show_condition_list
                        }
                    }
                
            }

        },
        'size':MAX_SEARCH_SIZE,
        'sort':{'create_time':{'order':'desc'}}
    }
    #print query_    
    if create_type or rank:
        results=es.search(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,body=query_body)['hits']['hits']
        result=[]
        for item in results:
            result.append(item['_source'])
    else:
        result=show_sensitive_words_default()
    return result


#step 3:    delete the sensitive word
def delete_sensitive_words(words_id):
    try:
        es.delete(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=words_id)
        result=True
    except:
        result=False
    return result

#step 4:    change the sensitive word

#step 4.2: change the selected sensitive word
def change_sensitive_words(words_id,change_info):
    rank=change_info[0]
    sensitive_words=change_info[1]
    create_type=change_info[2]
    create_time=change_info[3]

    try:
        es.update(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=words_id,\
            body={"doc":{'rank':rank,'sensitive_words':sensitive_words,'create_type':create_type,'create_time':create_time}})
        result=True
    except:
        result=False
    return result


###########  functional module 2: time alert node manage #########

#step 1:    add time alert node 
def get_create_date_remind(date_name,timestamp,keywords,create_type,create_time,content_recommend):
    task_detail = dict()
    #task_detail['date_time'] = ts2datetime(int(timestamp))[5:10]
    task_detail['date_name']=date_name
    task_detail['date_time']=timestamp[5:10]
    task_detail['keywords'] = keywords
    task_detail['create_type'] = create_type
    task_detail['create_time'] = create_time
    task_detail['content_recommend']=content_recommend

    task_id = create_time
    try:
        es.index(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id,body=task_detail)
        mark = True
    except:
        mark = False

    return mark

#step 2:    show the time alert node list
def show_date_remind():
    query_body={
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE,
        'sort':{'create_time':{'order':'desc'}}
    }
    result=es.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results

def show_date_remind_condition(create_type):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'create_type':create_type}
                }
            }
        },
        'size':MAX_VALUE,
        'sort':{'create_time':{'order':'desc'}}
    }
    result=es.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
    print result
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results

#step 3:    change the time alert node
#explain: Carry out show_select_date_remind before change,carry out step 3.1 & 3.2
#step 3.1: show the selected time alert node
def show_select_date_remind(task_id):
    result=es.get(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)
    return result

#step 3.2: change the selected time alert node
def change_date_remind(task_id,date_name,keywords,create_type,create_time):
    date_result=es.get(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)['_source']
    content_recommend=date_result['content_recommend']
    date_time=date_result['date_time']
    #create_type=create_type
    #keywords=keywords
    #create_time=create_time

    try:
        es.update(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id,\
            body={"doc":{'date_name':date_name,'date_time':date_time,'keywords':keywords,'create_type':create_type,\
            'create_time':create_time,'content_recommend':content_recommend}})
        result=True
    except:
        result=False
    return result


#step 4:    delete the time alert node
def delete_date_remind(task_id):
    try:
        es.delete(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)
        result=True
    except:
        result=False
    return result

###########        functional module 3: metaphorical expression     ###########

#step 1:    add metaphorical expression 
def get_create_hidden_expression(origin_word,evolution_words_string,create_type,create_time):
    task_detail = dict()
    task_detail['origin_word'] = origin_word
    task_detail['evolution_words_string'] = evolution_words_string
    task_detail['create_type'] = create_type
    task_detail['create_time'] = create_time
    task_id = origin_word
    try:
        es.index(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=task_id,body=task_detail)
        mark = True
    except:
        mark = False

    return mark

#step 2:    show the metaphorical expression list
def show_hidden_expression():
    query_body={
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE,
        'sort':{'create_time':{'order':'desc'}}
    }
    result=es.search(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results

def show_hidden_expression_condition(create_type):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'create_type':create_type}
                }
            }
        },
        'size':MAX_VALUE,
        'sort':{'create_time':{'order':'desc'}}
    }
    result=es.search(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results

    
#step 3:    change the metaphorical expression
#step 3.1: show the selected hidden expression
def show_select_hidden_expression(express_id):
    result=es.get(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=express_id)
    return result

#step 3.2: change the selected hidden expression
def change_hidden_expression(express_id,change_info):
    origin_word=change_info[0]
    evolution_words_string=change_info[1]
    create_type=change_info[2]
    create_time=change_info[3]

    try:
        es.update(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=express_id,\
            body={"doc":{'origin_word':origin_word,'evolution_words_string':evolution_words_string,'create_type':create_type,'create_time':create_time}})
        result=True
    except:
        result=False
    return result

#step 4:    delete the metaphorical expression
def delete_hidden_expression(express_id):
    try:
        es.delete(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=express_id)
        result=True
    except:
        result=False
    return result




###################################################################
###################   weibo_corpus Knowledge base    ##################
###################################################################

#step 1:create corpus
#corpus_info=[corpus_type,theme_daily_name,text,uid,mid,timestamp,retweeted,comment,like,create_type]
#subject corpus:corpus_type='主题语料'
#daily corpus:corpus_type='日常语料'
def create_corpus(corpus_info):
    corpus_detail=dict()
    corpus_detail['corpus_type']=corpus_info[0]
    corpus_detail['theme_daily_name']=corpus_info[1]
    corpus_detail['text']=corpus_info[2]
    corpus_detail['uid']=corpus_info[3]
    corpus_detail['mid']=corpus_info[4]
    corpus_detail['timestamp']=corpus_info[5]
    corpus_detail['retweeted']=corpus_info[6]
    corpus_detail['comment']=corpus_info[7]
    corpus_detail['like']=corpus_info[8]
    corpus_detail['create_type']=corpus_info[9]
    corpus_id=corpus_info[4]  #mid
    print corpus_info
    try:
        es.index(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id,body=corpus_detail)
        mark=True
    except:
        mark=False

    return mark


#step 2: show corpus
def show_corpus(corpus_type):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'corpus_type':corpus_type}
                }
            }

        },
        'size':MAX_VALUE
    }
    result=es.search(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results


def show_corpus_class(create_type,corpus_type):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'corpus_type':corpus_type},
                    'term':{'create_type':create_type}
                }
            }

        },
        'size':MAX_VALUE
    }
    result=es.search(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results

    
#step 3: change the corpus
#explain:carry out show_select_corpus before change,carry out step 3.1 & 3.2
#step 3.1: show the selected corpus
def show_select_corpus(corpus_id):
    result=es.get(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id)
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results

#step 3.2: change the selected corpus
def change_select_corpus(corpus_id,corpus_type,theme_daily_name,create_type):
    corpus_result=es.get(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id)['_source']
    text=corpus_result['text']
    uid=corpus_result['uid']
    mid=corpus_result['mid']
    timestamp=corpus_result['timestamp']
    retweeted=corpus_result['retweeted']
    comment=corpus_result['comment']
    like=corpus_result['like']

    corpus_type=corpus_type
    theme_daily_name=theme_daily_name
    create_type=create_type

    try:
        es.update(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id,\
            body={"doc":{'corpus_type':corpus_type,'theme_daily_name':theme_daily_name,'text':text,\
            'uid':uid,'mid':mid,'timestamp':timestamp,'retweeted':retweeted,'comment':comment,'like':like,'create_type':create_type}})
        result=True
    except:
        result=False
    return result


#step 4: delete the corpus
def delete_corpus(corpus_id):
    try:
        es.delete(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id)
        result=True
    except:
        result=False
    return result
