#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import pinyin
import numpy as np
from xnr.global_config import S_TYPE,S_DATE_FB as S_DATE
from xnr.global_utils import es_xnr as es
from xnr.global_utils import fb_role_index_name, fb_role_index_type
#facebook_user
from xnr.global_utils import r, es_fb_user_profile as es_user_profile, \
                            facebook_user_index_type as profile_index_type, \
                            facebook_user_index_name as profile_index_name
from xnr.global_utils import es_fb_user_portrait as es_user_portrait,\
                            fb_portrait_index_name as portrait_index_name, \
                            fb_portrait_index_type as portrait_index_type,\
                            facebook_flow_text_index_name_pre as flow_text_index_name_pre, \
                            facebook_flow_text_index_type as flow_text_index_type,\
                            fb_example_model_index_name, fb_example_model_index_type,\
                            fb_target_domain_detect_queue_name,\
                            fb_domain_index_name, fb_domain_index_type
from xnr.utils import fb_uid2nick_name_photo as uid2nick_name_photo,\
                        get_fb_influence_relative as get_influence_relative
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from xnr.parameter import MAX_VALUE,MAX_SEARCH_SIZE,fb_domain_ch2en_dict,fb_tw_topic_en2ch_dict,fb_domain_en2ch_dict,\
                        EXAMPLE_MODEL_PATH,TOP_ACTIVE_TIME,TOP_PSY_FEATURE
from xnr.time_utils import ts2datetime,datetime2ts,get_facebook_flow_text_index_list as get_flow_text_index_list
es_flow_text = es


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

def extract_keywords(w_text):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=w_text, lower=True, window=4)
    k_dict = tr4w.get_keywords(5, word_min_len=2)
    return k_dict

def get_user_location(location_dict):
    if location_dict.has_key('name'):
        location = location_dict['name']
    elif location_dict.has_key('country') and location_dict.has_key('city'):
        location = location_dict['city'] + ', ' + location_dict['country']
    else:
        location = ''
    return location

def get_generate_example_model(domain_name,role_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_en = fb_domain_ch2en_dict[role_name]
    task_id = domain_pinyin + '_' + role_en
    es_result = es.get(index=fb_role_index_name,doc_type=fb_role_index_type,id=task_id)['_source']
    item = es_result
    print 'es_result:::',es_result
    # 政治倾向
    political_side = json.loads(item['political_side'])[0][0]

    if political_side == 'mid':
        item['political_side'] = u'中立'
    elif political_side == 'left':
        item['political_side'] = u'左倾'
    else:
        item['political_side'] = u'右倾'

    # 心理特征
    psy_feature_list = []
    psy_feature = json.loads(item['psy_feature'])
    for i in range(TOP_PSY_FEATURE):
        psy_feature_list.append(psy_feature[i][0])
    item['psy_feature'] = '&'.join(psy_feature_list)
    role_group_uids = json.loads(item['member_uids'])

    if S_TYPE == 'test':
        current_time  = datetime2ts(S_DATE)
    else:
        current_time = int(time.time())

    index_name_list = get_flow_text_index_list(current_time)
    query_body_search = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':role_group_uids}
                }
            }
        },
        'size':MAX_VALUE,
        '_source':['keywords_string']
    }

    es_keyword_results = es_flow_text.search(index=index_name_list,doc_type=flow_text_index_type,\
                        body=query_body_search)['hits']['hits']
    keywords_string = ''
    for mget_item in es_keyword_results:
        keywords_string += '&'
        keywords_string += mget_item['_source']['keywords_string']
    k_dict = extract_keywords(keywords_string)
    
    monitor_keywords_list = []
    for item_item in k_dict:
        monitor_keywords_list.append(item_item.word.encode('utf-8'))
    item['monitor_keywords'] = ','.join(monitor_keywords_list)
    mget_results_user = es_user_portrait.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':role_group_uids})['docs']
    item['nick_name'] = []
    for mget_item in mget_results_user:
        if mget_item['found']:
            content = mget_item['_source']
            item['nick_name'] = ''
            if content.has_key('name'):
                item['nick_name'] = content['name']
            item['location'] = ''
            if content.has_key('location'):
                item['location'] = get_user_location(json.loads(content['location']))
            item['gender'] = 0
            if content.has_key('gender'):
                gender_str = content['gender']
                if gender_str == 'male':
                    gender = 1
                elif gender_str == 'female':
                    gender = 2
            item['description'] = ''
            if content.has_key('description'):
                item['description'] = content['description']

    item['business_goal'] = u'渗透'
    item['daily_interests'] = u'旅游'
    item['age'] = 30
    item['career'] = u'自由职业'

    active_time_list_np = np.array(json.loads(item['active_time']))
    active_time_list_np_sort = np.argsort(-active_time_list_np)[:TOP_ACTIVE_TIME]
    item['active_time'] = active_time_list_np_sort.tolist()

    day_post_num_list = np.array(json.loads(item['day_post_num']))
    item['day_post_num'] = np.mean(day_post_num_list).tolist()
    item['role_name'] = role_name
    
    task_id_new = 'fb_' + domain_pinyin + '_' + role_en
    example_model_file_name = EXAMPLE_MODEL_PATH + task_id_new + '.json'
    try:
        with open(example_model_file_name,"w") as dump_f:
            json.dump(item,dump_f)
        item_dict = dict()
        item_dict['domain_name'] = domain_name
        item_dict['role_name'] = role_name
        es.index(index=fb_example_model_index_name,doc_type=fb_example_model_index_type,\
            body=item_dict,id=task_id_new)
        mark = True
    except:
        mark = False
    return mark

def get_show_example_model():
    es_results = es.search(index=fb_example_model_index_name,doc_type=fb_example_model_index_type,\
        body={'query':{'match_all':{}}})['hits']['hits']
    result_all = []
    for result in es_results:
        result = result['_source']
        result_all.append(result)
    return result_all

def get_export_example_model(domain_name,role_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_en = fb_domain_ch2en_dict[role_name]
    task_id = 'fb_' + domain_pinyin + '_' + role_en
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
        create_type_new['by_all_users'] = all_users.encode('utf-8').split('，')
    return create_type_new

def domain_create_task(domain_name,create_type,create_time,submitter,description,remark,compute_status=0):
    task_id = pinyin.get(domain_name,format='strip',delimiter='_')
    try:
        es.get(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=task_id)['_source']
        return 'domain name exists!'
    except:
        try:
            domain_task_dict = dict()
            domain_task_dict['domain_pinyin'] = pinyin.get(domain_name,format='strip',delimiter='_')
            domain_task_dict['domain_name'] = domain_name
            domain_task_dict['create_type'] = json.dumps(create_type)
            domain_task_dict['create_time'] = create_time
            domain_task_dict['submitter'] = submitter
            domain_task_dict['description'] = description
            domain_task_dict['remark'] = remark
            domain_task_dict['compute_status'] = compute_status
            # print 'domain_task_dict'
            # print domain_task_dict
            # print 'before: r.lrange'
            # print r.lrange(fb_target_domain_detect_queue_name,0,100)
            r.lpush(fb_target_domain_detect_queue_name,json.dumps(domain_task_dict))
            # print 'after: r.lrange'
            # print r.lrange(fb_target_domain_detect_queue_name,0,100)
            item_exist = dict()
            item_exist['domain_pinyin'] = domain_task_dict['domain_pinyin']
            item_exist['domain_name'] = domain_task_dict['domain_name']
            item_exist['create_type'] = domain_task_dict['create_type']
            item_exist['create_time'] = domain_task_dict['create_time']
            item_exist['submitter'] = domain_task_dict['submitter']
            item_exist['description'] = domain_task_dict['description']
            item_exist['remark'] = domain_task_dict['remark']
            item_exist['group_size'] = ''
            item_exist['compute_status'] = 0  # 存入创建信息
            print es.index(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=item_exist['domain_pinyin'],body=item_exist)
            mark = True
        except Exception,e:
            print e
            mark = False
        return mark

def get_show_domain_group_summary(submitter):
    es_result = es.search(index=fb_domain_index_name,doc_type=fb_domain_index_type,\
                body={'query':{'term':{'submitter':submitter}}})['hits']['hits']
    if es_result:
        result_all = []
        for result in es_result:
            item = {}
            result = result['_source']
            item['group_size'] = result['group_size']
            item['domain_name'] = result['domain_name']
            item['create_time'] = result['create_time']
            item['compute_status'] = result['compute_status']
            item['create_type'] = result['create_type']
            item['remark'] = result['remark']
            item['description'] = result['description']
            create_type = json.loads(result['create_type'].encode('utf-8'))
            result_all.append(item)
    else:
        return '当前账户尚未创建渗透领域'
    return result_all

## 查看群体画像信息
def get_show_domain_group_detail_portrait(domain_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    es_result = es.get(index=fb_domain_index_name,doc_type=fb_domain_index_type,\
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
            # item['photo_url'] = result['photo_url']
            item['domain'] = result['domain']
            item['sensitive'] = result['sensitive']
            item['location'] = result['location']
            # item['fans_num'] = result['fansnum']
            # item['friends_num'] = result['friendsnum']
            # item['gender'] = result['gender']
            item['home_page'] = "https://www.facebook.com/profile.php?id=" + str(result['uid'])
            # item['home_page'] = 'http://weibo.com/'+result['uid']+'/profile?topnav=1&wvr=6&is_all=1'
            item['influence'] = get_influence_relative(item['uid'],result['influence'])
        else:
            item['uid'] = result['_id']
            item['nick_name'] = ''
            # item['photo_url'] = ''
            item['domain'] = ''
            item['sensitive'] = ''
            item['location'] = ''
            # item['fans_num'] = ''
            # item['friends_num'] = ''
            # item['gender'] = ''
            item['home_page'] = "https://www.facebook.com/profile.php?id=" + str(result['_id'])
            # item['home_page'] = 'http://weibo.com/'+result['_id']+'/profile?topnav=1&wvr=6&is_all=1'
            item['influence'] = ''
        result_all.append(item)
    return result_all

def get_show_domain_description(domain_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    es_result = es.get(index=fb_domain_index_name,doc_type=fb_domain_index_type,\
                id=domain_pinyin)['_source']
    item = {}
    item['group_size'] = es_result['group_size']
    item['description'] = es_result['description']
    topic_preference_list = json.loads(es_result['topic_preference'])
    topic_preference_list_chinese = []
    for topic_preference_item in topic_preference_list:
        topic_preference_item_chinese = fb_tw_topic_en2ch_dict[topic_preference_item[0]]
        topic_preference_list_chinese.append([topic_preference_item_chinese,topic_preference_item[1]])

    item['topic_preference'] = topic_preference_list_chinese
    item['word_preference'] = json.loads(es_result['top_keywords'])
    role_distribute_list = json.loads(es_result['role_distribute'])
    role_distribute_list_chinese = []
    for role_distribute_item in role_distribute_list:
        role_distribute_item_chinese = fb_domain_en2ch_dict[role_distribute_item[0]]
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
    role_en = fb_domain_ch2en_dict[role_name]
    task_id = domain_pinyin + '_' + role_en
    es_result = es.get(index=fb_role_index_name,doc_type=fb_role_index_type,id=task_id)['_source']
    return es_result

def get_delete_domain(domain_name):
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    try:
        es.delete(index=fb_domain_index_name,doc_type=fb_domain_index_type,id=domain_pinyin)
        mark = True
    except:
        mark = False
    return mark

