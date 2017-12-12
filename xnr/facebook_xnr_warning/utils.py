#-*- coding: utf-8 -*-
'''
facebook_xnr warning function
'''
import os
import json
import time
from xnr.time_utils import ts2datetime,datetime2ts,ts2yeartime,get_timets_set_indexset_list
from xnr.global_utils import es_xnr,fb_xnr_index_name,fb_xnr_index_type,\
                             facebook_user_warning_index_name_pre,facebook_user_warning_index_type,\
                             facebook_timing_warning_index_name_pre,facebook_timing_warning_index_type,\
                             fb_xnr_fans_followers_index_name,fb_xnr_fans_followers_index_type,\
                             facebook_speech_warning_index_name_pre,facebook_speech_warning_index_type,\
                             facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
                             weibo_date_remind_index_name,weibo_date_remind_index_type


from xnr.parameter import MAX_SEARCH_SIZE,MAX_VALUE,DAY,SPEECH_WARMING_NUM
from xnr.global_config import S_TYPE,FACEBOOK_FLOW_START_DATE


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
###################       personal warning       ##################
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

    user_warming_list=get_xnr_warming_index_listname(facebook_user_warning_index_name_pre,start_time,end_time)

    try:
        temp_results=es_xnr.search(index=user_warming_list,doc_type=facebook_user_warning_index_type,body=query_body)['hits']['hits']
        results=[]
        for item in temp_results:
            results.append(item['_source'])
        results.sort(key=lambda k:(k.get('user_sensitive',0)),reverse=True)
    except:
        results=[]
    #print results
    return results   


#查询好友列表
def lookup_xnr_friends(xnr_user_no):
    try:
        xnr_result=es_xnr.get(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
        lookup_list=xnr_result['fans_list']
    except:
        lookup_list=[]
    return lookup_list


#查询虚拟人uid
def lookup_xnr_uid(xnr_user_no):
    try:
        xnr_result=es_xnr.get(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=xnr_user_no)['_source']
        xnr_uid=xnr_result['uid']
    except:
        xnr_uid=''
    return xnr_uid


#查询今日人物行为预警
def lookup_today_personal_warming(xnr_user_no,start_time,end_time):
    #查询好友列表
    friends_list=lookup_xnr_friends(xnr_user_no)

    #查询虚拟人uid
    xnr_uid=lookup_xnr_uid(xnr_user_no)

     #计算敏感度排名靠前的用户
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':friends_list}
                }
            }
        },
        'aggs':{
            'friends_sensitive_num':{
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

    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,start_time,end_time)
    
    try:   
        first_sum_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,\
        body=query_body)['aggregations']['friends_sensitive_num']['buckets']
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

    #查询敏感用户的敏感内容
    results=[]
    for user in top_userlist:
        #print user
        user_detail=dict()
        user_detail['uid']=user['uid']
        user_detail['user_sensitive']=user['sensitive']
        user_lookup_id=user['uid']
        print user_lookup_id
        try:
            user_result=es_xnr.get(index=facebook_feedback_friends_index_name,doc_type=facebook_feedback_friends_index_type,id=user_lookup_id)['_source']
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
            second_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
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


def show_personnal_warning(xnr_user_no,start_time,end_time):
    if S_TYPE == 'test':
        test_today_date = FACEBOOK_FLOW_START_DATE
        test_time_gap = end_time - start_time
        today_datetime = datetime2ts(test_today_date)
        end_time = today_datetime
        start_time = end_time - test_time_gap
        end_datetime = datetime2ts(ts2datetime(end_time))
        start_datetime = datetime2ts(ts2datetime(start_time))
        #print ts2datetime(end_time),ts2datetime(start_time)
        #print end_time,start_time
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
###################       speech warning       ##################
###################################################################
def lookup_history_speech_warming(xnr_user_no,show_type,start_time,end_time):
    show_condition_list=[]
    if show_type == 0: #全部用户
        show_condition_list.append({'must':[{'term':{'xnr_user_no':xnr_user_no}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type == 1:#好友
        show_condition_list.append({'must':[{'term':{'content_type':'friends'}},{'term':{'xnr_user_no':xnr_user_no}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type == 2:#非好友
        show_condition_list.append({'must':[{'term':{'content_type':'unfriends'}},{'term':{'xnr_user_no':xnr_user_no}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    
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

    speech_warming_list=get_xnr_warming_index_listname(facebook_speech_warning_index_name_pre,start_time,end_time)
    #print speech_warming_list
    # try:
    temp_results=es_xnr.search(index=speech_warming_list,doc_type=facebook_speech_warning_index_type,body=query_body)['hits']['hits']
    print temp_results
    results=[]
    for item in temp_results:
        results.append(item['_source'])
    #results.sort(key=lambda k:(k.get('sensitive',0)),reverse=True)
    # except:
        # results=[]
    return results   


def lookup_today_speech_warming(xnr_user_no,show_type,start_time,end_time):
    #查询好友列表
    friends_list=lookup_xnr_friends(xnr_user_no)

    show_condition_list=[]
    if show_type == 0: #全部用户
        show_condition_list.append({'must':[{'range':{'sensitive':{'gte':1,'lte':100}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type == 1: #好友
        show_condition_list.append({'must':[{'terms':{'uid':friends_list}},{'range':{'sensitive':{'gte':1,'lte':100}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type ==2: #非好友
        show_condition_list.append({'must_not':{'terms':{'uid':friends_list}},'must':[{'range':{'sensitive':{'gte':1,'lte':100}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})

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

    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,start_time,end_time)
    result=[]
    try:
        results=es_flow_text.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        for item in results:
            result.append(item['_source'])
    except:
        result=[]

    return result   


   
def show_speech_warning(xnr_user_no,show_type,start_time,end_time):
    if S_TYPE == 'test':
        test_today_date = FACEBOOK_FLOW_START_DATE
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
    
    #print start_time,end_time
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



###################################################################
###################       date warming       ##################
###################################################################
def lookup_date_info(account_name,start_time,end_time,today_datetime):
    start_year=ts2yeartime(start_time)
    end_year=ts2yeartime(end_time)

    query_body={
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE,
        'sort':{'date_time':{'order':'asc'}}
    }
    result=es_xnr.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
    date_result=[]
    for item in result:
        date_time = item['_source']['date_time']
        date_name = item['_source']['date_name']
        start_tempdate_name = start_year + '-' + date_time
        start_tempdate_time = datetime2ts(start_tempdate_name)
        end_tempdate_name = end_year + '-' + date_time
        end_tempdate_time = datetime2ts(end_tempdate_name)

        year=ts2yeartime(today_datetime)
        warming_date=year+'-'+date_time        
        item['_source']['countdown_num']=(datetime2ts(warming_date)-today_datetime)/DAY 

        keywords=item['_source']['keywords']
       # print date_time
       #print start_tempdate_time,start_time,end_time,end_tempdate_time
        if (start_tempdate_time >= start_time and start_tempdate_time <= end_time) or (end_tempdate_time >= start_time and end_tempdate_time <= end_time):
            #print 'aaaa'
            if item['_source']['create_type'] == 'all_xnrs':
                item['_source']['facebook_date_warming_content']=lookup_facebook_date_warming_content(start_year,end_year,date_time,date_name,start_time,end_time,keywords)
                date_result.append(item['_source'])
            elif item['_source']['create_type'] == 'my_xnrs':
                if item['_source']['submitter'] == account_name:
                    item['_source']['facebook_date_warming_content']=lookup_facebook_date_warming_content(start_year,end_year,date_time,date_name,start_time,end_time,keywords)
                    date_result.append(item['_source'])
                else:
                    pass
        else:
            pass
    date_result.sort(key=lambda k:(k.get('countdown_num',0)),reverse=True)
    return date_result


def lookup_facebook_date_warming_content(start_year,end_year,date_time,date_name,start_time,end_time,keywords):
    facebook_timing_warning_index_name_list = []
    if start_year != end_year:
        start_year_int = int(start_year)
        end_year_int = int(end_year)
        iter_year = end_year_int
        while iter_year >= start_year_int:
            index_name = facebook_timing_warning_index_name_pre + str(start_year_int) + '-' + date_time
            if es_xnr.indices.exists(index=index_name):
                facebook_timing_warning_index_name_list.append(index_name)
            else:
                pass            
            iter_year = iter_year - 1
    else:
        index_name = facebook_timing_warning_index_name_pre + start_year + '-' + date_time
        if es_xnr.indices.exists(index=index_name):
            facebook_timing_warning_index_name_list.append(index_name)
        else:
            pass 

    query_body={
       'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'date_name':date_name}}
                        ]
                    }
                }
            }
        },
        'sort':{'timestamp':{'order':'asc'}} ,
        'size':MAX_SEARCH_SIZE
    }
    result=es_xnr.search(index=facebook_timing_warning_index_name_list,doc_type=facebook_timing_warning_index_type,body=query_body)['hits']['hits']
    warming_content=[]
    for item in result:
        warming_content.extend(json.loads(item['_source']['facebook_date_warming_content']))

    #当前时间范围内的预警信息
    now_time = int(time.time())
    if now_time >= start_time and now_time <= end_time:
        today_warming=lookup_todayfacebook_date_warming(keywords,now_time)
        warming_content.append(today_warming)
    else:
        pass
    return warming_content



def lookup_todayfacebook_date_warming(keywords,today_datetime):
    keyword_query_list=[]
    for keyword in keywords:
        keyword_query_list.append({'wildcard':{'text':'*'+keyword.encode('utf-8')+'*'}})

    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,today_datetime,today_datetime)

    query_body={
        'query':{
            'bool':{
                'should':keyword_query_list
            }
        },
        'size':MAX_VALUE
    }
    try:
        temp_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        date_result=[]
        for item in temp_result:
            date_result.append(item['_source'])
    except:
            date_result=[]
    return date_result


def show_date_warning(account_name,start_time,end_time):
    if S_TYPE == 'test':
        test_today_date = FACEBOOK_FLOW_START_DATE
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

    result=lookup_date_info(account_name,start_time,end_time,today_datetime)
    #print 'result',result
    return result



#更新flow text数据用于测试
def update_fb_flow_text(task_id,sensitive):
    result=es_xnr.update(index='facebook_flow_text_2017-09-10',doc_type='text',id=task_id,\
                body={"doc":{'sensitive':sensitive}})


    return result