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
                             weibo_date_remind_index_name,weibo_date_remind_index_type,\
                             facebook_count_index_name_pre,facebook_count_index_type,\
                             facebook_user_index_name,facebook_user_index_type,\
                             facebook_event_warning_index_name_pre,facebook_event_warning_index_type


from xnr.parameter import MAX_SEARCH_SIZE,MAX_VALUE,DAY,SPEECH_WARMING_NUM,MAX_WARMING_SIZE,\
                          FOLLOWER_INFLUENCE_MAX_JUDGE,NOFOLLOWER_INFLUENCE_MIN_JUDGE
from xnr.global_config import S_TYPE,FACEBOOK_FLOW_START_DATE

#查询用户昵称
def get_user_nickname(uid):
    try:
        result=es_xnr.get(index=facebook_user_index_name,doc_type=facebook_user_index_type,id=uid)
        user_name=result['_source']['username']
    except:
        user_name=''
    return user_name


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


#查询fid的comment、favorite、retweet等字段的数值
def lookup_fid_attend_index(fid,today_datetime):
    facebook_count_index_name=get_timets_set_indexset_list(facebook_count_index_name_pre,today_datetime,today_datetime)
    
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{'must':{'term':{'fid':fid}}}
                }
            }
        },
        'size':MAX_WARMING_SIZE,
        'sort':{'update_time':{'order':'desc'}}
    }
    try:
        result=es_xnr.search(index=facebook_count_index_name,doc_type=facebook_count_index_type,body=query_body)['hits']['hits']
        print result
        fid_result=[]
        for item in result:
            fid_result.append(item['_source'])
    except:
        fid_result=[]
    return fid_result
 
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
        'size':MAX_WARMING_SIZE
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
        # 'query':{
        #     'filtered':{
        #         'filter':{
        #             'terms':{'uid':friends_list}
        #         }
        #     }
        # },
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
        'size':MAX_SEARCH_SIZE
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
            friends_mark=judge_user_type(user_dict['uid'],friends_list)
            user_dict['sensitive']=user_sensitive*friends_mark
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
        user_detail['user_name']=get_user_nickname(user['uid'])

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
            second_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        except:
            second_result=[]

        s_result=[]
        for item in second_result:
            #查询三个指标字段
            fid_result=lookup_fid_attend_index(item['_source']['fid'],start_time)
            if fid_result:
                item['_source']['comment']=fid_result['comment']
                item['_source']['share']=fid_result['share']
                item['_source']['favorite']=fid_result['favorite']
            else:
                item['_source']['comment']=0
                item['_source']['share']=0
                item['_source']['favorite']=0 
            #查询用户昵称
            item['_source']['nick_name']=get_user_nickname(item['_source']['uid'])   
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

    warming_list=[]
    user_uid_list=[]
   
    for item in user_warming:
        user_uid=item['uid']
        item['content']=json.loads(item['content'])
        if user_uid in user_uid_list:
            old_user=[user for user in warming_list if user['uid'] == user_uid][0]
            new_warming_list = [user for user in warming_list if user['uid'] != user_uid]
            old_user['content'].extend(item['content'])
            old_user['user_sensitive']=old_user['user_sensitive']+item['user_sensitive']
            new_warming_list.append(old_user)
            warming_list = new_warming_list
        else:          
            warming_list.append(item)
            user_uid_list.append(user_uid)

    if warming_list:
        warming_list.sort(key=lambda k:(k.get('user_sensitive',0)),reverse=True)
    else:
        pass

    return warming_list

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
            #查询三个指标字段
            fid_result=lookup_fid_attend_index(item['_source']['fid'],today_datetime)
            if fid_result:
                item['_source']['comment']=fid_result['comment']
                item['_source']['share']=fid_result['share']
                item['_source']['favorite']=fid_result['favorite']
            else:
                item['_source']['comment']=0
                item['_source']['share']=0
                item['_source']['favorite']=0
             #查询用户昵称
            item['_source']['nick_name']=get_user_nickname(item['_source']['uid'])    
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
            # print 'index_name:',index_name
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
        'size':MAX_WARMING_SIZE
    }
    if facebook_timing_warning_index_name_list:
        result=es_xnr.search(index=facebook_timing_warning_index_name_list,doc_type=facebook_timing_warning_index_type,body=query_body)['hits']['hits']
        print 'facebook_timing_warning_index_name_list:',facebook_timing_warning_index_name_list
        warming_content=[]
        for item in result:
            print 'item:',item['_source']['date_name'],item['_source']['date_time']
            warming_content.extend(json.loads(item['_source']['facebook_date_warming_content']))
    else:
        warming_content=[]

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
        'size':MAX_WARMING_SIZE
    }
    try:
        temp_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        date_result=[]
        for item in temp_result:
            #查询三个指标字段
            fid_result=lookup_fid_attend_index(item['_source']['fid'],today_datetime)
            if fid_result:
                item['_source']['comment']=fid_result['comment']
                item['_source']['share']=fid_result['share']
                item['_source']['favorite']=fid_result['favorite']
            else:
                item['_source']['comment']=0
                item['_source']['share']=0
                item['_source']['favorite']=0 
            #查询用户昵称
            item['_source']['nick_name']=get_user_nickname(item['_source']['uid'])   
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

    event_warming_list=get_xnr_warming_index_listname(facebook_event_warning_index_name_pre,start_time,end_time)

    #try:
    temp_results=es_xnr.search(index=event_warming_list,doc_type=facebook_event_warning_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in temp_results:
        results.append(item['_source'])
    results.sort(key=lambda k:(k.get('event_influence',0)),reverse=True)
    #except:
    #    results=[]
    #print results
    return results  



#今日事件预警
#事件预警
def get_hashtag(today_datetime):
    
    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,today_datetime,today_datetime)
    query_body={
        'query':{
            'filtered':{
                'filter':{
                'bool':{
                    'must':[
                        {'range':{'sensitive':{'gte':1}}}
                    ]
                }}
            }
        },
        'aggs':{
            'all_hashtag':{
                'terms':{'field':'hashtag'},
                'aggs':{'sum_sensitive':{
                    'sum':{'field':'sensitive'}
                }
                }
            }
        },
        'size':5
    }
    flow_text_exist=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,\
                body=query_body)['aggregations']['all_hashtag']['buckets']
    #print 'flow_text_exist:',flow_text_exist
    
    hashtag_list = []
    for item in flow_text_exist:
        event_dict=dict()
        if item['key']:
            event_dict['event_name'] = item['key']
            event_dict['event_count'] = item['doc_count']
            event_dict['event_sensitive'] = item['sum_sensitive']['value']
            hashtag_list.append(event_dict)
        else:
            pass

    hashtag_list.sort(key=lambda k:(k.get('event_sensitive',0),k.get('event_count',0)),reverse=True)
    # print hashtag_list
    return hashtag_list


# #查询事件内容

def create_event_warning(xnr_user_no,today_datetime,write_mark=False):
    #获取事件名称
    hashtag_list = get_hashtag(today_datetime)
    #print 'hashtag_list/:',hashtag_list

    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,today_datetime,today_datetime)

    #虚拟人的好友列表
    friends_list=lookup_xnr_friends(xnr_user_no)

    event_warming_list=[]
    for event_item in hashtag_list:
        event_warming_content=dict()     #事件名称、主要参与用户、典型微博、事件影响力、事件平均时间
        event_warming_content['event_name']=event_item['event_name']
        event_influence_sum=0
        event_time_sum=0       
        query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'term':{'hashtag':event_item['event_name']}},
                                {'range':{'sensitive':{'gte':1}}}
                            ]
                        }
                    }
                }
            },
            'size':MAX_WARMING_SIZE,
            'sort':{'sensitive':{'order':'desc'}}
        }       
        event_results=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        if event_results:
            facebook_result=[]
            friends_num_dict=dict()
            alluser_num_dict=dict()
            #print 'sencond_time:::',int(time.time())
            for item in event_results:
                            #查询三个指标字段
                fid_result=lookup_fid_attend_index(item['_source']['fid'],today_datetime)
                if fid_result:
                    item['_source']['comment']=fid_result['comment']
                    item['_source']['share']=fid_result['share']
                    item['_source']['favorite']=fid_result['favorite']
                else:
                    item['_source']['comment']=0
                    item['_source']['share']=0
                    item['_source']['favorite']=0   
                #print 'event_content:',item['_source']['text']          
                #统计用户信息
                if alluser_num_dict.has_key(str(item['_source']['uid'])):
                    friends_mark=set_intersection(item['_source']['uid'],friends_list)
                    if friends_mark > 0:
                        alluser_num_dict[str(item['_source']['uid'])]=alluser_num_dict[str(item['_source']['uid'])]+1*2
                    else:
                        alluser_num_dict[str(item['_source']['uid'])]=alluser_num_dict[str(item['_source']['uid'])]+1
                else:
                    alluser_num_dict[str(item['_source']['uid'])]=1
                                   

                #计算影响力
                origin_influence_value=(1+item['_source']['comment']+item['_source']['share']+item['_source']['favorite'])*(1+item['_source']['sensitive'])
                friends_value=judge_user_type(item['_source']['uid'],friends_list)
                item['_source']['facebook_influence_value']=origin_influence_value*friends_value
                
                #查询用户昵称
                item['_source']['nick_name']=get_user_nickname(item['_source']['uid']) 
                facebook_result.append(item['_source'])

                #统计影响力、时间
                event_influence_sum=event_influence_sum+item['_source']['facebook_influence_value']
                event_time_sum=event_time_sum+item['_source']['timestamp']            
        
            # print 'third_time:::',int(time.time())
            #典型信息
            facebook_result.sort(key=lambda k:(k.get('facebook_influence_value',0)),reverse=True)
            event_warming_content['main_facebook_info']=json.dumps(facebook_result)

            #事件影响力和事件时间
            number=len(event_results)
            event_warming_content['event_influence']=event_influence_sum/number
            event_warming_content['event_time']=event_time_sum/number


        #对用户进行排序
            alluser_num_dict=sorted(alluser_num_dict.items(),key=lambda d:d[1],reverse=True)
            main_userid_list=[]
            for i in xrange(0,len(alluser_num_dict)):
                main_userid_list.append(alluser_num_dict[i][0])

        #主要参与用户信息
            main_user_info=[]
            user_es_result=es_xnr.mget(index=facebook_user_index_name,doc_type=facebook_user_index_type,body={'ids':main_userid_list})['docs']
            # print 'user_es_result:',user_es_result
            for item in user_es_result:

                user_dict=dict()
                if item['found']:
                    user_dict['uid']=item['_id']
                    user_dict['username']=item['_source']['username']
                    if item['_source'].has_key('talking_about_count'):
                        user_dict['talking_about_count']=item['_source']['talking_about_count']
                    else:
                        user_dict['talking_about_count']=0
                    if item['_source'].has_key('likes'):
                        user_dict['likes']=item['_source']['likes']
                    else:
                        user_dict['likes']=0
                    if item['_source'].has_key('category'):
                        user_dict['category']=item['_source']['category']
                    else:
                        user_dict['category']=''
                else:
                    # user_dict['icon']=''
                    user_dict['uid']=item['_id']
                    user_dict['username']=''
                    user_dict['talking_about_count']=0
                    user_dict['likes']=0
                    user_dict['category']=''
                main_user_info.append(user_dict)
            event_warming_content['main_user_info']=json.dumps(main_user_info)



            # print 'fourth_time:::',int(time.time())
            event_warming_content['xnr_user_no']=xnr_user_no
            event_warming_content['validity']=0
            event_warming_content['timestamp']=today_datetime
            now_time=int(time.time())
            task_id=xnr_user_no+'_'+str(now_time) 
        
            #写入数据库           
            if write_mark:
                # print 'today_datetime:::',ts2datetime(today_datetime)
                mark=write_envent_warming(today_datetime,event_warming_content,task_id)
                event_warming_list.append(mark)
            else:
                event_warming_list.append(event_warming_content)

        else:
            pass
        # print 'fifth_time:::',int(time.time())
    return event_warming_list


def write_envent_warming(today_datetime,event_warming_content,task_id):
    facebook_event_warning_index_name=facebook_event_warning_index_name_pre+ts2datetime(today_datetime)
    # print 'facebook_event_warning_index_name:',facebook_event_warning_index_name
    #try:
    es_xnr.index(index=facebook_event_warning_index_name,doc_type=facebook_event_warning_index_type,body=event_warming_content,id=task_id)
    mark=True
    #except:
    #    mark=False
    return mark

#粉丝或关注用户判断
def judge_user_type(uid,user_list):
    number=set_intersection(uid,user_list)
    if number > 0:
        mark=FOLLOWER_INFLUENCE_MAX_JUDGE
    else:
        mark=NOFOLLOWER_INFLUENCE_MIN_JUDGE
    return mark

def union_dict(*objs):
    #print 'objs:', objs[0]
    _keys=set(sum([obj.keys() for obj in objs],[]))
    _total={}

    for _key in _keys:
        _total[_key]=sum([int(obj.get(_key,0)) for obj in objs])

    return _total

#交集判断
def set_intersection(str_A,list_B):
    list_A=[]
    list_A.append(str_A)
    set_A = set(list_A)
    set_B = set(list_B)
    result = set_A & set_B
    number = len(result)
    return number


def show_event_warming(xnr_user_no,start_time,end_time):
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
            today_event_warming = create_event_warning(xnr_user_no,end_time,write_mark=False)

            #print 'mid_time',int(time.time())
            history_event_warming = lookup_history_event_warming(xnr_user_no,start_time,today_datetime)

            history_event_warming.extend(today_event_warming)

            event_warming = history_event_warming

    warming_list=[]
    event_name_list=[]


    for item in event_warming:
        event_name=item['event_name']
        item['main_user_info']=json.loads(item['main_user_info'])
        item['main_facebook_info']=json.loads(item['main_facebook_info']) 

        if event_name not in event_name_list:
            print 'event_name !!!!', event_name

            event_name_list.append(event_name)
            warming_list.append(item)
        else:
            old_event=[event for event in warming_list if event['event_name'] == event_name][0]
            new_warming_list = [event for event in warming_list if event['event_name'] != event_name]
            
            old_main_user_info = [event['main_user_info'] for event in warming_list if event['event_name'] == event_name][0]
            old_main_user_uids = [user['uid'] for user in old_main_user_info]
            now_uids = [u['uid'] for u in item['main_user_info']]
            new_uids = list(set(old_main_user_uids) - (set(old_main_user_uids) & set(now_uids)))
            print 'new_uid:',new_uids
            
            new_main_user_info = []
            for uid in new_uids:
                uid_info = [u for u in item['main_user_info'] if u['uid'] == uid]
                new_main_user_info.append(uid_info[0])
            old_event['main_user_info'].extend(new_main_user_info)

            old_main_facebook_info = [event['main_facebook_info'] for event in warming_list if event['event_name'] == event_name][0]
            old_main_fids = [content['fid'] for content in old_main_facebook_info]
            now_fids = [c['fid'] for c in item['main_facebook_info']]
            new_fids = list(set(old_main_fids) - (set(old_main_fids) & set(now_fids)))
            print 'new_fids',new_fids

            new_main_facebook_info = []
            for fid in new_fids:
                fid_info = [f for f in item['main_facebook_info'] if f['fid'] == fid]
                new_main_twitter_info.append(fid_info[0])
            old_event['main_facebook_info'].extend(new_main_facebook_info)

            old_event['event_influence']=old_event['event_influence']+item['event_influence']
            new_warming_list.append(old_event)
            warming_list = new_warming_list 


    #new_waining_list=[]
    # for item in event_warming:
    #     event_name=item['event_name']
    #     item['main_user_info']=json.loads(item['main_user_info'])
    #     item['main_facebook_info']=json.loads(item['main_facebook_info']) 
    #     if event_name in event_name_list:
    #         old_event=[event for event in warming_list if event['event_name'] == event_name][0]
    #         new_warming_list = [event for event in warming_list if event['event_name'] != event_name]
    #         old_event['main_user_info'].extend(item['main_user_info'])
    #         old_event['main_facebook_info'].extend(item['main_facebook_info'])
    #         old_event['event_influence']=old_event['event_influence']+item['event_influence']
    #         new_warming_list.append(old_event)
    #         warming_list = new_warming_list
    #     else:          
    #         warming_list.append(item)
    #         event_name_list.append(event_name)

    if warming_list:
        warming_list.sort(key=lambda k:(k.get('event_influence',0)),reverse=True)
    else:
        pass
    final_time=int(time.time())
    print 'time_coust:',final_time - first_time

    return warming_list   




#更新flow text数据用于测试
def update_fb_flow_text(task_id,sensitive):
    result=es_xnr.update(index='facebook_flow_text_2017-09-11',doc_type='text',id=task_id,\
                body={"doc":{'sensitive':sensitive}})


    return result