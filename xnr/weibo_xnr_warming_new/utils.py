#-*- coding: utf-8 -*-
'''
weibo_xnr warming function
'''
import os
import json
import time
from xnr.time_utils import ts2datetime,datetime2ts,get_day_flow_text_index_list
from xnr.global_utils import es_xnr,weibo_user_warning_index_name_pre,weibo_user_warning_index_type,\
                             weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                             es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                             weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
                             weibo_xnr_index_name,weibo_xnr_index_type,\
                             weibo_speech_warning_index_name_pre,weibo_speech_warning_index_type

from xnr.parameter import HOT_WEIBO_NUM,MAX_VALUE,MAX_SEARCH_SIZE,DAY,FLOW_TEXT_START_DATE,REMIND_DAY
from xnr.parameter import USER_NUM,MAX_SEARCH_SIZE,USER_CONTENT_NUM,DAY,UID_TXT_PATH,MAX_VALUE,SPEECH_WARMING_NUM,REMIND_DAY,WARMING_DAY
from xnr.global_config import S_TYPE,S_DATE,S_DATE_BCI,S_DATE_EVENT_WARMING


##获取索引
def get_xnr_warming_index_listname(index_name_pre,date_range_start_ts,date_range_end_ts):
    index_name_list=[]
    if ts2datetime(date_range_start_ts) != ts2datetime(date_range_end_ts):
        iter_date_ts=date_range_end_ts
        while iter_date_ts >= date_range_start_ts:
            date_range_start_date=ts2datetime(iter_date_ts)
            index_name=index_name_pre+date_range_start_date
            if es_xnr.indices.exists(index=index_name):
                index_name_list.append(index_name)
            else:
                pass
            iter_date_ts=iter_date_ts-DAY
    else:
        date_range_start_date=ts2datetime(date_range_start_ts)
        index_name=index_name_pre+date_range_start_date
        if es_xnr.indices.exists(index=index_name):
            index_name_list.append(index_name)
        else:
            pass
    return index_name_list

 
###################################################################
###################       personal warming       ##################
###################################################################

###查询历史人物预警信息
def lookup_history_user_warming(xnr_user_no,start_time,end_time):
    query_body={
       'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no}},
                            {'range':{
                            	'timestamp':{
                            		'gte':start_time,
                            		'lte':end_time
                            	}
                            }}
                        ]
                    }
                }
            }
        },
        'sort':{'user_sensitive':{'order':'asc'}} ,
        'size':MAX_SEARCH_SIZE
    }

    user_warming_list=get_xnr_warming_index_listname(weibo_user_warning_index_name_pre,start_time,end_time)

    try:
        temp_results=es_xnr.search(index=user_warming_list,doc_type=weibo_user_warning_index_type,body=query_body)['hits']['hits']
        results=[]
        for item in temp_results:
            results.append(item['_source'])
        results.sort(key=lambda k:(k.get('user_sensitive',0)),reverse=True)
    except:
        results=[]
    #print results
    return results   



#查询关注列表或者粉丝列表
#lookup_type='followers_list'或者'fans_list'
def lookup_xnr_fans_followers(user_id,lookup_type):
    try:
        xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=user_id)['_source']
        lookup_list=xnr_result[lookup_type]
    except:
        lookup_list=[]
    return lookup_list

#查询虚拟人uid
def lookup_xnr_uid(xnr_user_no):
    try:
        xnr_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
        xnr_uid=xnr_result['uid']
    except:
        xnr_uid=''
    return xnr_uid


#查询今日人物行为预警
def lookup_today_personal_warming(xnr_user_no,start_time,end_time):
    #查询关注列表
    lookup_type='followers_list'
    followers_list=lookup_xnr_fans_followers(xnr_user_no,lookup_type)

    #查询虚拟人uid
    xnr_uid=lookup_xnr_uid(xnr_user_no)

    #计算敏感度排名靠前的用户
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'uid':followers_list}},
                            {'range':{
                                'timestamp':{
                                    'gte':start_time,
                                    'lte':end_time
                                }
                            }}
                        ]
                    }                    
                }
            }
        },
        'aggs':{
            'followers_sensitive_num':{
                'terms':{'field':'uid'},
                'aggs':{
                    'sensitive_num':{
                        'sum':{'field':'sensitive'}
                    }
                }                        
            }
            },
        'size':MAX_VALUE
    }

    flow_text_index_name=get_day_flow_text_index_list(end_time)
    
    try:   
        first_sum_result=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
        body=query_body)['aggregations']['followers_sensitive_num']['buckets']
    except:
        first_sum_result=[]

    #print first_sum_result
    top_userlist=[]
    for i in xrange(0,len(first_sum_result)):
        user_sensitive=first_sum_result[i]['sensitive_num']['value']
        if user_sensitive > 0:
            user_dict=dict()
            user_dict['uid']=first_sum_result[i]['key']
            user_dict['sensitive']=user_sensitive
            top_userlist.append(user_dict)
        else:
            pass

    #查询敏感用户的敏感微博内容
    results=[]
    for user in top_userlist:
        #print user
        user_detail=dict()
        user_detail['uid']=user['uid']
        user_detail['user_sensitive']=user['sensitive']
        user_lookup_id=xnr_uid+'_'+user['uid']
        print user_lookup_id
        try:
            user_result=es_xnr.get(index=weibo_feedback_follow_index_name,doc_type=weibo_feedback_follow_index_type,id=user_lookup_id)['_source']
            #user_result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=user['uid'])['_source']
            user_detail['user_name']=user_result['nick_name']
        except:
            user_detail['user_name']=''

        query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'term':{'uid':user['uid']}},
                                {'range':{'sensitive':{'gte':1,'lte':100}}}
                            ]
                        }
                    }
                }
            },
            'size':MAX_VALUE,
            'sort':{'sensitive':{'order':'desc'}}
        }

        try:
            second_result=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
        except:
            second_result=[]

        s_result=[]
        for item in second_result:
            s_result.append(item['_source'])

        s_result.sort(key=lambda k:(k.get('sensitive',0)),reverse=True)
        user_detail['content']=json.dumps(s_result)

        user_detail['xnr_user_no']=xnr_user_no
        user_detail['validity']=0
        user_detail['timestamp']=end_time

        results.append(user_detail)

    results.sort(key=lambda k:(k.get('user_sensitive',0)),reverse=True)
    return results


def show_personnal_warming(xnr_user_no,start_time,end_time):
    if S_TYPE == 'test':
        test_today_date = S_DATE_EVENT_WARMING
        test_time_gap = end_time - start_time
        today_datetime = datetime2ts(test_today_date)
        end_time = today_datetime
        start_time = end_time - test_time_gap
        end_datetime = datetime2ts(ts2datetime(end_time))
        start_datetime = datetime2ts(ts2datetime(start_time))
        print ts2datetime(end_time),ts2datetime(start_time)
        print end_time,start_time
    else:
        now_time = int(time.time())
        today_datetime = datetime2ts(ts2datetime(now_time))
        end_datetime = datetime2ts(ts2datetime(end_time))
        start_datetime = datetime2ts(ts2datetime(start_time))

    user_warming=[]
    if today_datetime > end_datetime :
        #print 'aaaa'
        user_warming = lookup_history_user_warming(xnr_user_no,start_time,end_time)
    else:
        if end_datetime == start_datetime:
            #print 'bbbbb'
            user_warming = lookup_today_personal_warming(xnr_user_no,start_time,end_time)
            #print user_warming
        else:
            #print 'cccc'
            today_user_warming = lookup_today_personal_warming(xnr_user_no,today_datetime,end_time)
            history_user_warming = lookup_history_user_warming(xnr_user_no,start_time,today_datetime)
            history_user_warming.extend(today_user_warming)
            user_warming = history_user_warming
            #print today_user_warming
            #print history_user_warming
            #print user_warming

    if user_warming:
        user_warming.sort(key=lambda k:(k.get('user_sensitive',0)),reverse=True)
    else:
        pass

    return user_warming

###################################################################
###################       speech warming       ##################
###################################################################
def lookup_history_speech_warming(xnr_user_no,show_type,start_time,end_time):
    show_condition_list=[]
    if show_type == 0: #全部用户
        show_condition_list.append({'must':[{'term':{'xnr_user_no':xnr_user_no}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type == 1:#关注用户
        show_condition_list.append({'must':[{'term':{'content_type':'follow'}},{'term':{'xnr_user_no':xnr_user_no}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type == 2:#未关注用户
        show_condition_list.append({'must':[{'term':{'content_type':'unfollow'}},{'term':{'xnr_user_no':xnr_user_no}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':show_condition_list[0]
                }
            }
        },
        'size':SPEECH_WARMING_NUM,
        'sort':{'sensitive':{'order':'desc'}}
    }

    speech_warming_list=get_xnr_warming_index_listname(weibo_speech_warning_index_name_pre,start_time,end_time)
    
    try:
        temp_results=es_xnr.search(index=speech_warming_list,doc_type=weibo_speech_warning_index_type,body=query_body)['hits']['hits']
        results=[]
        for item in temp_results:
            results.append(item['_source'])
        #results.sort(key=lambda k:(k.get('sensitive',0)),reverse=True)
    except:
        results=[]
    return results   


def lookup_today_speech_warming(xnr_user_no,show_type,start_time,end_time):
    #查询关注列表
    lookup_type='followers_list'
    followers_list=lookup_xnr_fans_followers(xnr_user_no,lookup_type)

    show_condition_list=[]
    if show_type == 0: #全部用户
        show_condition_list.append({'must':[{'range':{'sensitive':{'gte':1,'lte':100}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type == 1: #关注用户
        show_condition_list.append({'must':[{'terms':{'uid':followers_list}},{'range':{'sensitive':{'gte':1,'lte':100}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type ==2: #未关注用户
        show_condition_list.append({'must_not':{'terms':{'uid':followers_list}},'must':[{'range':{'sensitive':{'gte':1,'lte':100}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})

    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':show_condition_list[0]
                }
            }
        },
        'size':SPEECH_WARMING_NUM,
        'sort':{'sensitive':{'order':'desc'}}
    }

    flow_text_index_name=get_day_flow_text_index_list(start_time)
    result=[]
    try:
        results=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
        for item in results:
            result.append(item['_source'])
    except:
        result=[]

    return result   


   
def show_speech_warming(xnr_user_no,show_type,start_time,end_time):
    if S_TYPE == 'test':
        test_today_date = S_DATE_EVENT_WARMING
        test_time_gap = end_time - start_time
        today_datetime = datetime2ts(test_today_date)
        end_time = today_datetime
        start_time = end_time - test_time_gap
        end_datetime = datetime2ts(ts2datetime(end_time))
        start_datetime = datetime2ts(ts2datetime(start_time))
    else:
        now_time = int(time.time())
        today_datetime = datetime2ts(ts2datetime(now_time))
        end_datetime = datetime2ts(ts2datetime(end_time))
        start_datetime = datetime2ts(ts2datetime(start_time))

    speech_warming=[]
    if today_datetime > end_datetime :
        speech_warming = lookup_history_speech_warming(xnr_user_no,show_type,start_time,end_time)
    else:
        if end_datetime == start_datetime:
            speech_warming = lookup_today_speech_warming(xnr_user_no,show_type,start_time,end_time)
        else:
            today_speech_warming = lookup_today_speech_warming(xnr_user_no,show_type,today_datetime,end_time)
            history_speech_warming = lookup_history_speech_warming(xnr_user_no,show_type,start_time,today_datetime)
            history_speech_warming.extend(today_speech_warming)
            speech_warming = history_speech_warming
    if speech_warming:
        speech_warming.sort(key=lambda k:(k.get('sensitive',0)),reverse=True)
    else:
        pass

    return speech_warming
