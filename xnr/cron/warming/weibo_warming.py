#-*- coding: utf-8 -*-
'''
weibo warming function
'''
import os
import json
import time
import sys
reload(sys)
sys.path.append('../../')
from timed_python_files.system_log_create import get_user_account_list,get_user_xnr_list
from parameter import DAY,MAX_VALUE
from global_config import S_TYPE,S_DATE_BCI
from time_utils import ts2datetime,datetime2ts,get_day_flow_text_index_list
from global_utils import es_xnr,weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                         es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                         weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
                         weibo_user_warning_index_name_pre,weibo_user_warning_index_type,\
                         weibo_xnr_index_name,weibo_xnr_index_type,\
                         weibo_speech_warning_index_name_pre,weibo_speech_warning_index_type


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

#人物行为预警
def create_personal_warning(xnr_user_no,today_datetime):
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
                    'terms':{'uid':followers_list}
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

    flow_text_index_name=get_day_flow_text_index_list(today_datetime)
    
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
        #tem_word_one = '静坐'
        #tem_word_two = '集合'
        for item in second_result:
            #sensitive_words=item['_source']['sensitive_words_string']
            #if ((sensitive_words==tem_word_one) or (sensitive_words==tem_word_two)):
            #    pass
            #else:
            s_result.append(item['_source'])

        s_result.sort(key=lambda k:(k.get('sensitive',0)),reverse=True)
        user_detail['content']=json.dumps(s_result)

        user_detail['xnr_user_no']=xnr_user_no
        user_detail['validity']=0
        user_detail['timestamp']=today_datetime

        #写入数据库
        today_date=ts2datetime(today_datetime)
        weibo_user_warning_index_name=weibo_user_warning_index_name_pre+today_date

        task_id=xnr_user_no+'_'+user_detail['uid']
        #print weibo_user_warning_index_name
        #print user_detail
        try:
            es_xnr.index(index=weibo_user_warning_index_name,doc_type=weibo_user_warning_index_type,body=user_detail,id=task_id)
            mark=True
        except:
            mark=False

        results.append(mark)

    return results

#言论内容预警
def create_speech_warning(xnr_user_no,today_datetime):
    #查询关注列表
    lookup_type='followers_list'
    followers_list=lookup_xnr_fans_followers(xnr_user_no,lookup_type)
    
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{'must':{'range':{'sensitive':{'gte':1,'lte':100}}}}
                }
            }
        },
        'size':MAX_VALUE,
        'sort':{'sensitive':{'order':'desc'}}
    }

    flow_text_index_name=get_day_flow_text_index_list(today_datetime)

    results=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    result=[]
    for item in results:
        if item['_source']['uid'] in followers_list:
            item['_source']['content_type']='follow'
        else:
            item['_source']['content_type']='unfollow'

        item['_source']['validity']=0
        item['_source']['xnr_user_no']=xnr_user_no

        task_id=xnr_user_no+'_'+item['_source']['mid']

        #写入数据库
        today_date=ts2datetime(today_datetime)
        weibo_speech_warning_index_name=weibo_speech_warning_index_name_pre+today_date
        try:
            es_xnr.index(index=weibo_speech_warning_index_name,doc_type=weibo_speech_warning_index_type,body=item['_source'],id=task_id)
            mark=True
        except:
            mark=False

        result.append(mark)
    return result


#事件预警
#def create_event_warning():

#时间预警
#def create_timing_warning():


#微博预警内容组织
def create_weibo_warning():
    #时间设置
    if S_TYPE == 'test':
        test_day_date=S_DATE_BCI
        today_datetime=datetime2ts(test_day_date)
        start_time=today_datetime - DAY
        end_time=today_datetime
        operate_date=ts2datetime(start_time)        
    else:
        now_time=int(time.time())
        today_datetime=datetime2ts(ts2datetime(now_time))
        start_time=today_datetime-DAY    #前一天0点
        end_time=today_datetime          #定时文件启动的0点
        operate_date=ts2datetime(start_time)

    account_list=get_user_account_list()
    for account in account_list:
        xnr_list=get_user_xnr_list(account)

        for xnr_user_no in xnr_list:
            #人物行为预警
            #personal_mark=create_personal_warning(xnr_user_no,today_datetime)
        	#言论内容预警
        	speech_mark=create_speech_warning(xnr_user_no,today_datetime)
        	#事件涌现预警

    return True


if __name__ == '__main__':
    create_weibo_warning()