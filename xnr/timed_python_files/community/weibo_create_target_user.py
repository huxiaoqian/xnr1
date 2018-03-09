#-*-coding:utf-8-*-
import os
import json
import time
import sys
sys.path.append('../../')
import gensim
import numpy as np
from collections import Counter
from parameter import DAY,MIN_TARGET_USER_NUM,COMMUNITY_TERM,TARGET_KEYWORD_NUM,WORD2VEC_PATH,MAX_DETECT_COUNT
from time_utils import ts2datetime,datetime2ts
from global_config import S_TYPE,R_BEGIN_TIME,S_DATE

from global_utils import es_xnr,xnr_flow_text_index_name_pre,xnr_flow_text_index_type,\
                         weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                         es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                         be_retweet_index_name_pre,be_retweet_index_type,\
                         retweet_index_name_pre,retweet_index_type,\
                         comment_index_name_pre,comment_index_type,\
                         be_comment_index_name_pre,be_comment_index_type

r_beigin_ts = datetime2ts(R_BEGIN_TIME)

sys.path.append('../../cron/trans/')
from trans import trans, simplified2traditional, traditional2simplified

sys.path.append('../../timed_python_files/community/')
from weibo_publicfunc import get_compelete_wbxnr

#use to merge dict
#input: dict1, dict2, dict3...
#output: merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    
    return _total
    
#查找虚拟人发布的关键词
def get_xnr_keywords(xnr_user_no,datetime_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{'must':{'term':{'xnr_user_no':xnr_user_no}}}
                }
            }
        },
        'size':TARGET_KEYWORD_NUM,
        'sort':[
            {'sensitive':{'order':'desc'}},
            {'retweeted':{'order':'desc'}}
        ]
    }

    xnr_flow_text_index_name_list = []
    for date_name in datetime_list:
        xnr_flow_text_index_name = xnr_flow_text_index_name_pre + date_name
        if es_xnr.indices.exists(index=xnr_flow_text_index_name):
            xnr_flow_text_index_name_list.append(xnr_flow_text_index_name)
        else:
            pass

    #添加容错
    #try:
    es_results = es_xnr.search(index = xnr_flow_text_index_name_list,doc_type = xnr_flow_text_index_type,body=query_body)['hits']['hits']
    keywords_list = []
    for item in es_results:
        keywords_string = item['_source']['keywords_string']
        if keywords_string:
            keywords_list.extend(keywords_string.split('&'))
        else:
            pass
    #except:
        #keywords_list=[]
    return keywords_list


#查找虚拟人的关注用户或好友
def get_xnr_relationer(xnr_user_no):
    try:
        xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
        lookup_list=xnr_result['followers_list']
    except:
        lookup_list=[]
    return lookup_list


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


### 根据关键词
# input：关键词（指虚拟人发布的关键词），任务创建时间
# output：近期facebook包含上述关键词的用户群体的uid
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
# input：种子用户uid(即虚拟人的关注用户为初始，或返回用户初始循环），任务创建时间
# output：近期与种子用户有转发和评论关系的用户群体的画像数据
def detect_by_seed_users(seed_users):
    retweet_mark = 1 #1目前只有部分数据
    comment_mark = 0 #暂无数据

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
            retweet_result = es_flow_text.mget(index=retweet_index_name, doc_type=retweet_index_type, \
                                             body={'ids':seed_users}, _source=True)['docs']
        except:
            retweet_result = []
        
        #mget be_retweet
        try:
            be_retweet_result = es_flow_text.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type, \
                                                body={'ids':seed_users} ,_source=True)['docs']
        except:
            be_retweet_result = []
    
    #step2: mget comment and be_comment
    if comment_mark == 1:
        comment_index_name = comment_index_name_pre + str(db_number)
        be_comment_index_name = be_comment_index_name_pre + str(db_number)
        #mget comment
        try:
            comment_result = es_flow_text.mget(index=comment_index_name, doc_type=comment_index_type, \
                                             body={'ids':seed_users}, _source=True)['docs']
        except:
            comment_result = []
        #mget be_comment
        try:
            be_comment_result = es_flow_text.mget(index=be_comment_index_name, doc_type=be_comment_index_type, \
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
        # union four type user set
        
        union_result = union_dict(uid_retweet_dict, uid_be_retweet_dict, uid_comment_dict, uid_be_comment_dict)
        # union_result = uid_be_comment_dict
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



#基于关键词和种子用户扩展用户
def get_expand_userid_list(xnr_keywords,xnr_relationer,datetime_list):
    origin_keywords_uidlist = detect_by_keywords(xnr_keywords,datetime_list)
    origin_relationer_uidlist = detect_by_seed_users(xnr_relationer)
    origin_relationer_uidlist.extend(origin_keywords_uidlist)

    expand_userid_list = origin_relationer_uidlist
    uid_num = len(expand_userid_list)

    while uid_num >= MIN_TARGET_USER_NUM:
        temp_uidlist = detect_by_seed_users(expand_userid_list)
        expand_userid_list.extend(temp_uidlist)
        uid_num = len(expand_userid_list)

    return expand_userid_list


def create_xnr_targetuser(xnr_user_no):
    # #step1:查找虚拟人列表
    # xnr_user_no_list = get_compelete_wbxnr()

    #step2：设置时间范围
    if S_TYPE == 'test':
        now_time = datetime2ts(S_DATE)
    else:
        now_time = int(time.time())
    end_ts = datetime2ts(ts2datetime(now_time))
    start_ts = end_ts - COMMUNITY_TERM*DAY
    datetime_list = []
    if start_ts != end_ts:
        iter_date_ts = end_ts
        while iter_date_ts >= start_ts:
            start_date = ts2datetime(iter_date_ts)
            datetime_list.append(start_date)
            iter_date_ts = iter_date_ts - DAY
    else:
        start_date = ts2datetime(start_ts)
        datetime_list.append(start_date)


    #step3：分虚拟人创建种子用户
    # for xnr_user_no in xnr_user_no_list:

    #step3.1：查找虚拟人发布的关键词
    xnr_keywords = get_xnr_keywords(xnr_user_no,datetime_list)

    #step3.2：查找虚拟人的关注用户或好友
    xnr_relationer = get_xnr_relationer(xnr_user_no)

    #step3.3：基于关键词和种子用户扩展用户
    expand_userid_list = get_expand_userid_list(xnr_keywords,xnr_relationer,datetime_list)


    return expand_userid_list 


if __name__ == '__main__':
    xnr_user_no = 'WXNR0004'
    start_time = int(time.time())
    uid_list = create_xnr_targetuser(xnr_user_no)
    end_time =  int(time.time())
    print 'uid_list:',uid_list
    print 'cost_time:',end_time - start_time