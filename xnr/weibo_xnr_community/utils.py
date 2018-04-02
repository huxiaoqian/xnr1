# -*- coding:utf-8 -*-

'''
weibo community function 
'''
import sys
import json
import time,datetime
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,get_flow_text_index_list
from xnr.global_utils import es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                             es_user_profile,profile_index_name,profile_index_type,\
                             es_xnr,weibo_community_index_name_pre,weibo_community_index_type,\
                             weibo_trace_community_index_name_pre,weibo_trace_community_index_type
                             

from xnr.parameter import DAY,MAX_SEARCH_SIZE
from xnr.global_config import S_TYPE,S_DATE,WEIBO_COMMUNITY_DATE
from textrank4zh import TextRank4Keyword, TextRank4Sentence


#计算当前日期周期内的community index
def get_community_index(date_time):
    date_range_end_ts = date_time
    index_name_list = []
    for i in range(0,7):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = weibo_community_index_name_pre + date_range_start_datetime
        if es_xnr.indices.exists(index = index_name):
            index_name_list.append(index_name)
        else:
        	pass
    return index_name_list


##社区详情涉及函数
#获取社区信息
def get_community_info(community_id,now_time):
    #step1:获取uid_list
    weibo_community_index_name = get_community_index(now_time)
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'community_id':community_id}}
                        ]
                    }
                }
            }
        },
        'size':1
    }
    try:
        community_result = es_xnr.search(index=weibo_community_index_name,\
            doc_type=weibo_community_index_type,body=query_body)['hits']['hits']
        # print 'community_result::',community_result
        for item in community_result:
            community = item['_source']
            # print 'community:',type(community)
    except:
        community = dict()

    return community


def extract_keywords(w_text):

    tr4w = TextRank4Keyword()
    tr4w.analyze(text=w_text, lower=True, window=4)
    k_dict = tr4w.get_keywords(100, word_min_len=2)

    return k_dict

#提取关键词词频
def get_word_count(word_content):
    word_dict = dict()

    word_dict_new = dict()

    keywords_string = ''
    for item in word_content:
        word = item['key']
        count = item['doc_count']
        word_dict[word] = count

        keywords_string += '&'
        keywords_string += item['key']

    k_dict = extract_keywords(keywords_string)

    for item_item in k_dict:
        keyword = item_item.word
        if word_dict.has_key(keyword):
            word_dict_new[keyword] = word_dict[keyword]
        else:
            word_dict_new[keyword] = 1

    return word_dict_new

#社区内容
def get_community_content(now_time,uid_list,order_by):
    #step1:获取uid_list

    #step2:生成话题词云、敏感词云、敏感帖子
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'uid':uid_list}}
                        ]
                    }
                }
            }
        },
        'aggs':{
                'sensitive_words_string':{
                    'terms':{
                        'field':'sensitive_words_string',
                        'size': 800
                    }
                }
        },
        'size':50,
        'sort':{order_by:{'order':'desc'}}
    }
    query_hashtag = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'uid':uid_list}}
                        ]
                    }
                }
            }
        },
        'aggs':{
                'hashtag':{
                    'terms':{
                        'field':'hashtag',
                        'size':800
                    }
               }
        },
        'size':50,
        'sort':{order_by:{'order':'desc'}}
    }
    flow_text_index_name_list = get_flow_text_index_list(now_time)
    flow_text_exist = es_flow_text.search(index = flow_text_index_name_list,doc_type = flow_text_index_type,\
               body = query_body)
    sensitive_keywords_result = flow_text_exist['aggregations']['sensitive_words_string']['buckets']
    content_result = flow_text_exist['hits']['hits']

    hashtag_result = es_flow_text.search(index = flow_text_index_name_list,doc_type = flow_text_index_type,\
               body = query_hashtag)['aggregations']['hashtag']['buckets']
    
    # print 'content_result:',content_result
    # print 'sensitive_keywords_result:',sensitive_keywords_result
    # print 'hashtag_result:',hashtag_result
    sensitive_keywords_dict = get_word_count(sensitive_keywords_result)
    hashtag_dict = get_word_count(hashtag_result)
    
    content_list = []
    for item in content_result:
        content_list.append(item['_source'])

    result_dict = dict()
    result_dict['topic_wordcloud'] = hashtag_dict
    result_dict['sensitive_wordcloud'] = sensitive_keywords_dict
    result_dict['content_post'] = content_list

    return result_dict



################主功能函数
#跟踪社区
def show_trace_community(xnr_user_no,now_time):
    if S_TYPE == 'test':
        now_time = datetime2ts(WEIBO_COMMUNITY_DATE)
    else:
        pass
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'xnr_user_no':xnr_user_no}},
                        {'terms':{'community_status':[1,-2]}}                        
                        ]
                    }
                }
            }
        }
    }
    weibo_community_index_name = get_community_index(now_time)

    # print 'weibo_community_index_name:',weibo_community_index_name
    try:
        community_result = es_xnr.search(index = weibo_community_index_name,doc_type = weibo_community_index_type,body = query_body)['hits']['hits']
        community_list = []
        for item in community_result:
            #跟踪判断提示
            if item['_source']['warning_remind'] >= 3:
                item['_source']['trace_message'] = u'该社区已经连续3周未出现预警，请选择放弃跟踪或强制跟踪！'
            else:
                item['_source']['trace_message'] = u''
            community_list.append(item['_source'])
    except:
        community_list = []
    return community_list


#新社区
def show_new_community(xnr_user_no,now_time):
    if S_TYPE == 'test':
        now_time = datetime2ts(WEIBO_COMMUNITY_DATE)
    else:
        pass
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'xnr_user_no':xnr_user_no}},
                        {'term':{'community_status':0}}                        
                        ]
                    }
                }
            }
        }
    }
    weibo_community_index_name = get_community_index(now_time)
    
    try:
        community_result = es_xnr.search(index = weibo_community_index_name,doc_type = weibo_community_index_type,body = query_body)['hits']['hits']
        community_list = []
        for item in community_result:
            community_list.append(item['_source'])
    except:
        community_list = []
    return community_list


#社区跟踪状态更新
def update_trace_status(community_id,trace_status,now_time):
    if S_TYPE == 'test':
        now_time = datetime2ts(WEIBO_COMMUNITY_DATE)
    else:
        now_time = int(time.time())
    weibo_community_index_name = get_community_index(now_time)
    # print weibo_community_index_name
    # print 'trace_status11',trace_status
    # print 'now_time',ts2datetime(now_time)
    try:
        update_result = es_xnr.update(index=weibo_community_index_name,doc_type=weibo_community_index_type,\
            id=community_id,body={'doc':{'community_status':trace_status}})
        mark = True
    except:
        mark = False
    return mark  


#社区预警
def get_community_warning(xnr_user_no,community_id,start_time,end_time):
    if S_TYPE == 'test':
        time_gap = end_time - start_time
        end_time = datetime2ts(WEIBO_COMMUNITY_DATE)
        start_time = end_time - time_gap
    else:
        pass
    weibo_trace_community_index_name = weibo_trace_community_index_name_pre + xnr_user_no.lower()
    print 'weibo_trace_community_index_name:',weibo_trace_community_index_name
    print 'time:',ts2datetime(start_time),ts2datetime(end_time)
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'community_id':community_id}},
                            {'range':{'trace_time':{'gte':start_time,'lte':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':30,
        'sort':{'trace_time':{'order':'desc'}}
    }
    try:
        community_result = es_xnr.search(index=weibo_trace_community_index_name,\
            doc_type=weibo_trace_community_index_type,body=query_body)['hits']['hits']
        result = []
        # print 'community_result::',community_result
        for item in community_result:
            result.append(item['_source'])
    except:
        result = []
    return result


# 社区详情
def get_community_detail(now_time,model,community_id,order_by):
    community = get_community_info(community_id,now_time)
    result = dict()

    if model == 'content':
        uid_list = community['nodes']
        result = get_community_content(now_time,uid_list,order_by)
    elif model == 'user':
        result['community_user_list'] = json.loads(community['community_user_list']) #社区成员列表，标记了核心成员
        if community['community_user_change']:
            result['community_user_change'] = json.loads(community['community_user_change']) #社区成员变化列表，标记成员+、-
        else:
            result['community_user_change'] = []
    elif model == 'netgragh':
        result['core_outer_socail'] = json.loads(community['core_outer_socail'])
        result['core_user_socail'] = json.loads(community['core_user_socail'])
    # print 'result:::',result
    return result


#用户信息
def get_user_detail(uid):
    user_result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
    user_detail = dict()
    if user_result:
        user_detail['user_url'] = "http://weibo.com/" + uid 
        user_detail['uid'] = uid
        user_detail['nick_name'] = user_result['nick_name']
        user_detail['photo_url'] = user_result['photo_url']
        user_detail['user_location'] = user_result['user_location']
        user_detail['sex'] = user_result['sex']
        user_detail['fansnum'] = user_result['fansnum']
        user_detail['friendsnum'] = user_result['friendsnum']
    else:        
        user_detail['user_url'] = "http://weibo.com/" + uid 
        user_detail['uid'] = uid
        user_detail['nick_name'] = ''
        user_detail['photo_url'] = ''
        user_detail['user_location'] = ''
        user_detail['sex'] = 0
        user_detail['fansnum'] = 0
        user_detail['friendsnum'] = 0
    return user_detail

#删除社区
def delete_community(community_id):
    weibo_community_index_name = 'weibo_community_2016-11-20'
    mark = es_xnr.delete(index=weibo_community_index_name,doc_type=weibo_community_index_type,id=community_id)
    return mark