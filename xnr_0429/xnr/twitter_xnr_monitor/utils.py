# -*- coding:utf-8 -*-

'''
facebook information monitor function about database task
'''
import sys
import json
import time,datetime
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,get_timets_set_indexset_list,\
        ts2datetimestr,get_xnr_flow_text_index_listname,get_xnr_feedback_index_listname
from xnr.global_utils import es_xnr_2 as es_xnr,twitter_keyword_count_index_name,twitter_keyword_count_index_type,\
                             tw_xnr_fans_followers_index_name,tw_xnr_fans_followers_index_type,\
                             twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
                             tw_xnr_index_name,tw_xnr_index_type,\
                             twitter_count_index_name_pre,twitter_count_index_type,\
                             tw_bci_index_name_pre,tw_bci_index_type,\
                             twitter_user_index_name,twitter_user_index_type,\
                             twitter_xnr_corpus_index_name,twitter_xnr_corpus_index_type

from xnr.parameter import MAX_FLOW_TEXT_DAYS,MAX_VALUE,DAY,MID_VALUE,MAX_SEARCH_SIZE,HOT_WEIBO_NUM,INFLUENCE_MIN,\
                          MAX_HOT_POST_SIZE
from xnr.global_config import S_TYPE,S_DATE_TW

#查询用户昵称
def get_user_nickname(uid):
    try:
        result=es_xnr.get(index=twitter_user_index_name,doc_type=twitter_user_index_type,id=uid)
        user_name=result['_source']['username']
    except:
        user_name=''
    return user_name
    
#查询虚拟人的关注用户列表
def lookup_xnr_concernedusers(xnr_user_no):
    try:
        result=es_xnr.get(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,id=xnr_user_no)
        followers_list=result['_source']['followers_list']
    except:
        followers_list=[]
    return followers_list


#合并dict
def union_dict(*objs):
    _keys=set(sum([obj.keys() for obj in objs],[]))
    _total={}

    for _key in _keys:
        _total[_key]=sum([int(obj.get(_key,0)) for obj in objs])

    return _total


#查询历史词云信息
def lookup_history_keywords(from_ts,to_ts,xnr_user_no):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[{'term':{'xnr_user_no':xnr_user_no}},
                        {'range':{'timestamp':{'gte':from_ts,'lte':to_ts}}}]
                    }
                }
            }
        }
    }
    es_result=es_xnr.search(index=twitter_keyword_count_index_name,\
            doc_type=twitter_keyword_count_index_type,body=query_body)['hits']['hits']
    if not es_result:
        es_result = dict()
        return es_result
    all_keywords_dict=dict()
    for item in es_result:
        keywords_dict = json.loads(item['_source']['keyword_value_string'])
        all_keywords_dict=union_dict(all_keywords_dict,keywords_dict)
    return all_keywords_dict

#查询今日词云
def lookup_today_keywords(from_ts,to_ts,xnr_user_no):
    userslist=lookup_xnr_concernedusers(xnr_user_no)
    query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'terms':{'uid':userslist}},
                                {'range':{'timestamp':{'gte':from_ts,'lte':to_ts}}}
                            ]
                        }
                    }
                }
            },
            'aggs':{
                'keywords':{
                    'terms':{
                        'field':'keywords_string',
                        'size': 50
                    }
                }
            }
        }
    flow_text_index_name = twitter_flow_text_index_name_pre + ts2datetime(to_ts)
    flow_text_exist=es_xnr.search(index=flow_text_index_name,doc_type=twitter_flow_text_index_type,\
                body=query_body)['aggregations']['keywords']['buckets']

    word_dict = dict()
    for item in flow_text_exist:
        word = item['key']
        count = item['doc_count']
        word_dict[word] = count
    return word_dict


#组织词云内容查询
def lookup_weibo_keywordstring(from_ts,to_ts,xnr_id):
    now_time=int(time.time())
    time_gap = to_ts - from_ts
    test_time_gap = datetime2ts(ts2datetime(now_time)) - datetime2ts(S_DATE_TW)
    if S_TYPE == 'test':
        today_date_time = datetime2ts(S_DATE_TW)
        from_ts = from_ts - test_time_gap
        to_ts = to_ts - test_time_gap
    else:
        today_date_time= datetime2ts(ts2datetime(now_time))

    print from_ts,to_ts

    xnr_user_no=xnr_id

    keywords_dict=dict()
    if to_ts > today_date_time:
        #今日词云信息统计
        today_kewords_dict=lookup_today_keywords(from_ts,to_ts,xnr_user_no)
        history_keywords_dict=lookup_history_keywords(from_ts,today_date_time,xnr_user_no)
        keywords_dict=union_dict(today_kewords_dict,history_keywords_dict)
    else:
        keywords_dict=lookup_history_keywords(from_ts,to_ts,xnr_user_no)
    return keywords_dict 


#热门帖子
#查询tid的comment、favorite、retweet等字段的数值
def lookup_tid_attend_index(tid,from_ts,to_ts):
    twitter_count_index_name=get_timets_set_indexset_list(twitter_count_index_name_pre,from_ts,to_ts)
    
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{'must':{'term':{'tid':tid}}}
                }
            }
        },
        'size':1,
        'sort':{'update_time':{'order':'desc'}}
    }
    try:
        result=es_xnr.search(index=twitter_count_index_name,doc_type=twitter_count_index_type,body=query_body)['hits']['hits']
        # print 'result:',result,twitter_count_index_name
        tid_result=[]
        for item in result:
            tid_result.append(item['_source'])
    except:
        tid_result=[]
    return tid_result


def lookup_hot_posts(from_ts,to_ts,xnr_id,classify_id,order_id):
    time_gap = to_ts - from_ts
    now_time = time.time()
    test_time_gap = datetime2ts(ts2datetime(now_time)) - datetime2ts(S_DATE_TW)
    if S_TYPE == 'test':
        today_date_time = datetime2ts(S_DATE_TW)
        from_ts = from_ts - test_time_gap
        to_ts = to_ts - test_time_gap

    from_date_ts=datetime2ts(ts2datetime(from_ts))
    to_date_ts=datetime2ts(ts2datetime(to_ts))
    # print 'from_date_ts, to_date_ts:', ts2date(from_date_ts), ts2date(to_date_ts)
    # print from_date_ts,to_date_ts

    flow_text_index_name_list=get_timets_set_indexset_list(twitter_flow_text_index_name_pre,from_ts,to_ts)
    # print 'flow_text_index_name:',flow_text_index_name_list
    userslist=lookup_xnr_concernedusers(xnr_id)
    #全部用户 0，好友 1，非好友-1
    range_time_list={'range':{'timestamp':{'gte':int(from_ts),'lt':int(to_ts)}}}
    # print range_time_list

    user_condition_list=[]
    if classify_id == 1:
        user_condition_list=[{'bool':{'must':[{'terms':{'uid':userslist}},range_time_list]}}]
    elif classify_id == 2:
        user_condition_list=[{'bool':{'must':[range_time_list],'must_not':[{'terms':{'uid':userslist}}]}}]
    elif classify_id == 0:
        user_condition_list=[{'bool':{'must':[range_time_list]}}]

    query_body={
        'query':{
            'filtered':{
                'filter':user_condition_list
            }

        },
        'size':MAX_HOT_POST_SIZE,     
        'sort':{'timestamp':{'order':'desc'}}
        }

    # try:
    es_result=es_xnr.search(index=flow_text_index_name_list,doc_type=twitter_flow_text_index_type,\
        body=query_body)['hits']['hits']
    hot_result=[]
    for item in es_result:
        #查询三个指标字段
        tid_result=lookup_tid_attend_index(item['_source']['tid'],from_ts,to_ts)
        if tid_result:
            item['_source']['comment']=tid_result['comment']
            item['_source']['share']=tid_result['share']
            item['_source']['favorite']=tid_result['favorite']
        else:
            item['_source']['comment']=0
            item['_source']['share']=0
            item['_source']['favorite']=0 
        #查询用户昵称
        item['_source']['nick_name']=get_user_nickname(item['_source']['uid'])
        hot_result.append(item['_source'])
    # except:
        # hot_result=[]

    if order_id==1:         #按时间排序
        sort_condition='timestamp'        
    elif order_id==2:       #按热度排序
        sort_condition='retweeted'
    elif order_id==3:       #按敏感度排序
        sort_condition='sensitive'
    else:                   #默认设为按时间排序
        sort_conditiont='timestamp'
    if hot_result:
        hot_result.sort(key=lambda k:(k.get(sort_condition,0)),reverse=True)
        hot_result=hot_result[:50]
    return hot_result


#活跃用户
def lookup_active_user(classify_id,xnr_id,start_time,end_time):
    time_gap = end_time - start_time
    now_time = time.time()
    test_time_gap = datetime2ts(ts2datetime(now_time)) - datetime2ts(S_DATE_TW)
    if S_TYPE == 'test':
        today_date_time = datetime2ts(S_DATE_TW)
        start_time = start_time - test_time_gap
        end_time = end_time - test_time_gap

    from_date_ts=datetime2ts(ts2datetime(start_time))
    to_date_ts=datetime2ts(ts2datetime(end_time))
    
    bci_index_name = tw_bci_index_name_pre + ''.join(ts2datetime(today_date_time))

    userlist = lookup_xnr_concernedusers(xnr_id)

    if classify_id == 1:      
        condition_list=[{'bool':{'must':{'terms':{'uid':userlist}}}}]
    elif classify_id == 2:    
        condition_list=[{'bool':{'must_not':[{'terms':{'uid':userlist}}]}}] 
    elif classify_id == 0:
        condition_list=[{'match_all':{}}]
    print userlist,classify_id,condition_list

    results = []
    for item in condition_list:
        query_body={
            'query':item,
            'size':HOT_WEIBO_NUM,       #查询影响力排名前50的用户即可
            'sort':{'influence':{'order':'desc'}}
            }
        try:
            flow_text_exist=es_xnr.search(index=bci_index_name,\
                    doc_type=tw_bci_index_type,body=query_body)['hits']['hits']
            search_uid_list = [item['_source']['uid'] for item in flow_text_exist]
            user_exist = es_xnr.search(index=twitter_user_index_name,\
                    doc_type=twitter_user_index_type,body={'query':{'terms':{'uid':search_uid_list}}})['hits']['hits']

            user_dict = dict()
            for item in user_exist:
                uid = item['_source']['uid']
                user_dict[uid] = item['_source']
            for item in flow_text_exist:
                influence = item['_source']['influence']
                active = item['_source']['active']
                uid = item['_source']['uid']
                try:
                    user_info = user_dict[uid]
                    uname = user_info['name']
                    location = user_info['locale']
                    link = user_info['link']
                except:
                    uname = ''
                    location = ''
                    link = ''
                results.append({'uid':uid, 'influence':influence, 'active':active, \
                        'uname': uname, 'location':location, 'link': link})
        except Exception,e:
            raise e

    return results


#加入语料库
def addto_twitter_corpus(task_detail):
    flow_text_index_name = twitter_flow_text_index_name_pre + ts2datetime(task_detail['timestamp'])
    try:
        corpus_result = es_xnr.get(index=flow_text_index_name,doc_type=twitter_flow_text_index_type,id=task_detail['tid'])['_source']
        task_detail['text']=corpus_result['text']
        
        #查询三个指标字段
        tid_result=lookup_tid_attend_index(task_detail['tid'],task_detail['timestamp'],task_detail['timestamp'])
        if tid_result:
            task_detail['comment']=tid_result['comment']
            task_detail['share']=tid_result['share']
            task_detail['favorite']=tid_result['favorite']
        else:
            task_detail['comment']=0
            task_detail['share']=0
            task_detail['favorite']=0 

            #查询用户昵称
        task_detail['nick_name']=get_user_nickname(item['_source']['uid'])

    except:
        mark=False

    try:
        es_xnr.index(index=twitter_xnr_corpus_index_name,doc_type=twitter_xnr_corpus_index_type,id=task_detail['tid'],body=task_detail)
        mark=True
    except:
        mark=False
    return mark