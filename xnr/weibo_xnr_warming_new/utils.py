#-*- coding: utf-8 -*-
'''
weibo_xnr warming function
'''
import os
import json
import time
from xnr.time_utils import ts2datetime,datetime2ts,get_day_flow_text_index_list,ts2yeartime
from xnr.global_utils import es_xnr,weibo_user_warning_index_name_pre,weibo_user_warning_index_type,\
                             weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                             es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                             weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
                             weibo_xnr_index_name,weibo_xnr_index_type,\
                             weibo_speech_warning_index_name_pre,weibo_speech_warning_index_type,\
                             weibo_timing_warning_index_name_pre,weibo_timing_warning_index_type,\
                             weibo_date_remind_index_name,weibo_date_remind_index_type,\
                             weibo_event_warning_index_name_pre,weibo_event_warning_index_type,\
                             es_user_profile,profile_index_name,profile_index_type



from xnr.parameter import HOT_WEIBO_NUM,MAX_VALUE,MAX_SEARCH_SIZE,DAY,FLOW_TEXT_START_DATE,REMIND_DAY,MAX_WARMING_SIZE,EVENT_COUNT
from xnr.parameter import USER_NUM,MAX_SEARCH_SIZE,USER_CONTENT_NUM,DAY,UID_TXT_PATH,MAX_VALUE,SPEECH_WARMING_NUM,REMIND_DAY,WARMING_DAY
from xnr.global_config import S_TYPE,S_DATE,S_DATE_BCI,S_DATE_EVENT_WARMING,S_DATE_WARMING
from xnr.global_utils import R_CLUSTER_FLOW2 as r_cluster


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
        'size':MAX_WARMING_SIZE
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
                            # {'terms':{'uid':followers_list}},
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
        'size':MAX_SEARCH_SIZE
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
            #user_result=es_xnr.get(index=weibo_feedback_follow_index_name,doc_type=weibo_feedback_follow_index_type,id=user_lookup_id)['_source']
            user_result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=user['uid'])['_source']
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
            'size':MAX_WARMING_SIZE,
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

    warming_list=[]
    user_uid_list=[]
    for item in user_warming:
        user_uid=item['uid']
        item['content']=json.loads(item['content'])
        if user_uid in user_uid_list:
            old_user=[user for user in warming_list if user['uid'] == user_uid][0]
            new_warming_list = [user for user in warming_list if user['uid'] != user_uid][0]
            old_user['content'].extend(item['content'])
            old_user['user_sensitive']=old_user['user_sensitive']+item['user_sensitive']
            new_warming_list.append(old_user)
            warming_list = new_warming_list
        else:          
            warming_list.append(item)
            user_uid_list.append(user_uid)

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
        show_condition_list.append({'must':[{'range':{'sensitive':{'gte':1}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type == 1: #关注用户
        show_condition_list.append({'must':[{'terms':{'uid':followers_list}},{'range':{'sensitive':{'gte':1}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})
    elif show_type ==2: #未关注用户
        show_condition_list.append({'must_not':{'terms':{'uid':followers_list}},'must':[{'range':{'sensitive':{'gte':1}}},{'range':{'timestamp':{'gte':start_time,'lte':end_time}}}]})

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
    #print 'start_time:',start_time,'end_time:',end_time
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
                item['_source']['weibo_date_warming_content']=lookup_weibo_date_warming_content(start_year,end_year,date_time,date_name,start_time,end_time,keywords)
                date_result.append(item['_source'])
            elif item['_source']['create_type'] == 'my_xnrs':
                if item['_source']['submitter'] == account_name:
                    item['_source']['weibo_date_warming_content']=lookup_weibo_date_warming_content(start_year,end_year,date_time,date_name,start_time,end_time,keywords)
                    date_result.append(item['_source'])
                else:
                    pass
        else:
            pass
    date_result.sort(key=lambda k:(k.get('countdown_num',0)),reverse=True)
    return date_result


def lookup_weibo_date_warming_content(start_year,end_year,date_time,date_name,start_time,end_time,keywords):
    weibo_timing_warning_index_name_list = []
    if start_year != end_year:
        start_year_int = int(start_year)
        end_year_int = int(end_year)
        iter_year = end_year_int
        while iter_year >= start_year_int:
            index_name = weibo_timing_warning_index_name_pre + str(start_year_int) + '-' + date_time
            if es_xnr.indices.exists(index=index_name):
                weibo_timing_warning_index_name_list.append(index_name)
            else:
                pass            
            iter_year = iter_year - 1
    else:
        index_name = weibo_timing_warning_index_name_pre + start_year + '-' + date_time
        if es_xnr.indices.exists(index=index_name):
            weibo_timing_warning_index_name_list.append(index_name)
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
    result=es_xnr.search(index=weibo_timing_warning_index_name_list,doc_type=weibo_timing_warning_index_type,body=query_body)['hits']['hits']
    warming_content=[]
    for item in result:
        warming_content.extend(json.loads(item['_source']['weibo_date_warming_content']))

    #当前时间范围内的预警信息
    now_time = int(time.time())
    if now_time >= start_time and now_time <= end_time:
        today_warming=lookup_todayweibo_date_warming(keywords,now_time)
        warming_content.extend(today_warming)
    else:
        pass
    return warming_content


def lookup_todayweibo_date_warming(keywords,today_datetime):
    keyword_query_list=[]
    for keyword in keywords:
        keyword_query_list.append({'wildcard':{'text':'*'+keyword.encode('utf-8')+'*'}})

    flow_text_index_name=get_day_flow_text_index_list(today_datetime)

    query_body={
        'query':{
            'bool':
            {
                'should':keyword_query_list,
                'must':{'range':{'sensitive':{'gte':1}}}
            }
        },
        'size':MAX_WARMING_SIZE,
        'sort':{'sensitive':{'order':'desc'}}
    }
    try:
        temp_result=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
        date_result=[]
        for item in temp_result:
            date_result.append(item['_source'])
    except:
            date_result=[]
    return date_result


def show_date_warming(account_name,start_time,end_time):
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

    result=lookup_date_info(account_name,start_time,end_time,today_datetime)
    #print 'result',result
    return result




###################################################################
###################         event warming        ##################
###################################################################
###查询历史事件预警信息
def lookup_history_event_warming(xnr_user_no,start_time,end_time):
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
        'sort':{'event_influence':{'order':'asc'}} ,
        'size':MAX_WARMING_SIZE
    }

    event_warming_list=get_xnr_warming_index_listname(weibo_event_warning_index_name_pre,start_time,end_time)

    #try:
    temp_results=es_xnr.search(index=event_warming_list,doc_type=weibo_event_warning_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in temp_results:
        results.append(item['_source'])
    results.sort(key=lambda k:(k.get('event_influence',0)),reverse=True)
    #except:
    #    results=[]
    #print results
    return results  

#今天的时间涌现预警
#create_event_warning(xnr_user_no,now_time,write_mark=False)
def get_hashtag(now_time):

    uid_list = []
    hashtag_list = {}

    with open(UID_TXT_PATH+'/uid_sensitive.txt','rb') as f:
        for line in f:
            uid = line.strip()
            uid_list.append(uid)

    for uid in uid_list:
        if S_TYPE == 'test':
            hashtag = r_cluster.hget('hashtag_' + str(datetime2ts(S_DATE_WARMING)-DAY),uid)
            #hashtag = r_cluster.hget('hashtag_'+str(datetime2ts(S_DATE)+7*DAY),uid)
        else:
            hashtag = r_cluster.hget('hashtag_' + str(now_time),uid)
            #hashtag = r_cluster.hget('hashtag_'+str((time.time()-DAY)),uid)

        if hashtag != None:
            hashtag = hashtag.encode('utf8')
            hashtag = json.loads(hashtag)

            for k,v in hashtag.iteritems():
                try:
                    hashtag_list[k] += v
                except:
                    hashtag_list[k] = v
        #r_cluster.hget('hashtag_'+str(a))

    hashtag_list = sorted(hashtag_list.items(),key=lambda x:x[1],reverse=True)[:5]

    return hashtag_list

def create_event_warning(xnr_user_no,today_datetime,write_mark):
    #获取事件名称
    hashtag_list = get_hashtag(today_datetime)
    #print 'hashtag_list::',hashtag_list

    flow_text_index_name = get_day_flow_text_index_list(today_datetime)

    #虚拟人的粉丝列表和关注列表
    try:
        es_xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
        followers_list=es_xnr_result['followers_list']
        fans_list=es_xnr_result['fans_list']
    except:
        followers_list=[]
        fans_list=[]

    event_warming_list=[]
    event_num=0
    for event_item in hashtag_list:
        if event_item[-1]>EVENT_COUNT:
            event_sensitive_count=0
            event_warming_content=dict()     #事件名称、主要参与用户、典型微博、事件影响力、事件平均时间
            event_warming_content['event_name']=event_item[0]
            #print 'event_name:',event_item[0],event_item[-1]
            event_num=event_num+1
            #print 'event_num:::',event_num
            event_influence_sum=0
            event_time_sum=0       
            query_body={
                'query':{
                    'bool':{
                        'must':[{'wildcard':{'text':'*'+event_item[0]+'*'}},
                        {'range':{'sensitive':{'gte':1}}}]
                    }
                },
                'size':MAX_WARMING_SIZE,
                'sort':{'sensitive':{'order':'desc'}}
            }
            #try: 
            #print '1::',int(time.time())        
            event_results=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
            if event_results:
                weibo_result=[]
                main_userid_list=[]
                fans_num_dict=dict()
                followers_num_dict=dict()
                alluser_num_dict=dict()
                #print '2::',int(time.time())
                for item in event_results:
                    #print 'event_content:',item['_source']['text']          
                    event_sensitive_count=event_sensitive_count+1
                    #统计用户信息
                    #print '3::',int(time.time())
                    # if alluser_num_dict.has_key(str(item['_source']['uid'])):
                    #     alluser_num_dict[str(item['_source']['uid'])]=alluser_num_dict[str(item['_source']['uid'])]+1
                    # else:
                    #     alluser_num_dict[str(item['_source']['uid'])]=1
                        
                    # for fans_uid in fans_list:                    
                    #     if fans_uid==item['_source']['uid']:
                    #         if fans_num_dict.has_key(str(fans_uid)):
                    #             fans_num_dict[str(fans_uid)]=fans_num_dict[str(fans_uid)]+1
                    #         else:
                    #             fans_num_dict[str(fans_uid)]=1
                    #     else:
                    #         pass
                        
                    # for followers_uid in followers_list:
                    #     if followers_uid==item['_source']['uid']:
                    #         if followers_num_dict.has_key(str(followers_uid)):
                    #             fans_num_dict[str(followers_uid)]=fans_num_dict[str(followers_uid)]+1
                    #         else:
                    #             fans_num_dict[str(followers_uid)]=1
                    #     else:
                    #         pass

                    #计算影响力
                    # origin_influence_value=(1+item['_source']['comment']+item['_source']['retweeted'])*(1+item['_source']['sensitive'])
                    # fans_value=judge_user_type(item['_source']['uid'],fans_list)
                    # followers_value=judge_user_type(item['_source']['uid'],followers_list)
                    # item['_source']['weibo_influence_value']=origin_influence_value*(fans_value+followers_value)
                    item['_source']['weibo_influence_value']=0
                    weibo_result.append(item['_source'])

                    main_userid_list.append(item['_source']['uid'])

                    #统计影响力、时间
                    # event_influence_sum=event_influence_sum+item['_source']['weibo_influence_value']
                    # event_time_sum=event_time_sum+item['_source']['timestamp']            

                #典型微博信息
                # weibo_result.sort(key=lambda k:(k.get('weibo_influence_value',0)),reverse=True)
                event_warming_content['main_weibo_info']=json.dumps(weibo_result)
                #event_warming_content['main_weibo_info']=weibo_result

                #事件影响力和事件时间
                # number=len(event_results)
                # event_warming_content['event_influence']=event_influence_sum/number
                # event_warming_content['event_time']=event_time_sum/number

                event_warming_content['event_influence']=0
                event_warming_content['event_time']=0

                # except:
                #     event_warming_content['main_weibo_info']=[]
                #     event_warming_content['event_influence']=0
                #     event_warming_content['event_time']=0
                
                #try:
                #print '4::',int(time.time())
                if event_sensitive_count > 0:
                #对用户进行排序
                    # temp_userid_dict=union_dict(fans_num_dict,followers_num_dict)
                    # main_userid_dict=union_dict(temp_userid_dict,alluser_num_dict)
                    # main_userid_dict=sorted(main_userid_dict.items(),key=lambda d:d[1],reverse=True)
                    # main_userid_list=[]
                    # for i in xrange(0,len(main_userid_dict)):
                    #     main_userid_list.append(main_userid_dict[i][0])

                    #主要参与用户信息
                    main_user_info=[]
                    user_es_result=es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':main_userid_list})['docs']
                    for item in user_es_result:
     
                        user_dict=dict()
                        if item['found']:
                            user_dict['photo_url']=item['_source']['photo_url']
                            user_dict['uid']=item['_id']
                            user_dict['nick_name']=item['_source']['nick_name']
                            user_dict['favoritesnum']=item['_source']['favoritesnum']
                            user_dict['fansnum']=item['_source']['fansnum']
                        else:
                            user_dict['photo_url']=''
                            user_dict['uid']=item['_id']
                            user_dict['nick_name']=''
                            user_dict['favoritesnum']=0
                            user_dict['fansnum']=0
                        main_user_info.append(user_dict)
                    event_warming_content['main_user_info']=json.dumps(main_user_info)

                else:
                    event_warming_content['main_user_info']=''
                #except:
                #    event_warming_content['main_user_info']=[]

                event_warming_content['xnr_user_no']=xnr_user_no
                event_warming_content['validity']=0
                event_warming_content['timestamp']=today_datetime
                now_time=int(time.time())
                task_id=xnr_user_no+'_'+str(now_time) 
                
                #print '5::',int(time.time())
                if event_sensitive_count > 0:
                    #print 'event_sensitive_count:::',event_sensitive_count
                    #写入数据库           
                    if write_mark:
                        #print 'today_datetime:::',ts2datetime(today_datetime)
                        mark=write_envent_warming(today_datetime,event_warming_content,task_id)
                        event_warming_list.append(mark)
                    else:
                        event_warming_list.append(event_warming_content)
                else:
                    pass
                #print '6::',int(time.time())
            else:
                pass
        else:
            pass
    return event_warming_list


#粉丝或关注用户判断
def judge_user_type(uid,user_list):
    if uid in user_list:
        mark=1.2
    else:
        mark=0.8
    return mark

def union_dict(*objs):
    #print 'objs:', objs[0]
    _keys=set(sum([obj.keys() for obj in objs],[]))
    _total={}

    for _key in _keys:
        _total[_key]=sum([int(obj.get(_key,0)) for obj in objs])

    return _total

def show_event_warming(xnr_user_no,start_time,end_time):
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

    event_warming=[]
    first_time=int(time.time())
    if today_datetime > end_datetime :
        print 'aaaa'
        event_warming = lookup_history_event_warming(xnr_user_no,start_time,end_time)
    else:
        if end_datetime == start_datetime:
            print 'bbbbb'
            event_warming = create_event_warning(xnr_user_no,end_time,write_mark=False)
        else:
            print 'cccc'
            #print 'before_time',int(time.time())

            today_event_warming = create_event_warning(xnr_user_no,end_time,write_mark=False)

            #print 'mid_time',int(time.time())
            history_event_warming = lookup_history_event_warming(xnr_user_no,start_time,today_datetime)
            #print 'final_time',int(time.time())
            #print 'today_event_warming:',today_event_warming
            #print 'history_event_warming:',history_event_warming

            history_event_warming.extend(today_event_warming)

            event_warming = history_event_warming
            #print 'event_warming:',event_warming
            #print start_datetime,end_datetime
    warming_list=[]
    event_name_list=[]
    #new_waining_list=[]
    for item in event_warming:
        event_name=item['event_name']
        #print 'event_name:::',event_name
        #print 'main_user_info_type:::',type(item['main_user_info'])
        #print 'main_weibo_info_type:::',type(item['main_weibo_info'])
        item['main_user_info']=json.loads(item['main_user_info'])
        item['main_weibo_info']=json.loads(item['main_weibo_info']) 
        if event_name in event_name_list:
            old_event=[event for event in warming_list if event['event_name'] == event_name][0]
            new_warming_list = [event for event in warming_list if event['event_name'] != event_name]
            old_event['main_user_info'].extend(item['main_user_info'])
            old_event['main_weibo_info'].extend(item['main_weibo_info'])
            old_event['event_influence']=old_event['event_influence']+item['event_influence']
            new_warming_list.append(old_event)
            warming_list = new_warming_list
        else:          
            warming_list.append(item)
            event_name_list.append(event_name)

    if warming_list:
        warming_list.sort(key=lambda k:(k.get('event_influence',0)),reverse=True)
    else:
        pass
    final_time=int(time.time())
    print 'time_coust:',final_time - first_time

    return warming_list    

