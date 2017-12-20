#-*- coding: utf-8 -*-
'''
twitter warming function
'''
import os
import json
import time
import sys
reload(sys)
sys.path.append('../../')
from timed_python_files.system_log_create import get_user_account_list
from parameter import DAY,MAX_VALUE,WARMING_DAY,USER_XNR_NUM,MAX_WARMING_SIZE,MAX_SEARCH_SIZE
from global_config import S_TYPE,TWITTER_FLOW_START_DATE
from time_utils import ts2datetime,datetime2ts,get_day_flow_text_index_list,ts2yeartime,get_timets_set_indexset_list
from global_utils import es_xnr,tw_xnr_index_name,tw_xnr_index_type,weibo_date_remind_index_name,weibo_date_remind_index_type,\
                         tw_xnr_fans_followers_index_name,tw_xnr_fans_followers_index_type,\
                         twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
                         twitter_speech_warning_index_name_pre,twitter_speech_warning_index_type,\
                         twitter_feedback_fans_index_name,twitter_feedback_fans_index_type,\
                         twitter_feedback_follow_index_name,twitter_feedback_follow_index_type,\
                         twitter_user_warning_index_name_pre,twitter_user_warning_index_type,\
                         twitter_timing_warning_index_name_pre,twitter_timing_warning_index_type,\
                         twitter_count_index_name_pre,twitter_count_index_type,\
                         twitter_user_index_name,twitter_user_index_type

 
#虚拟人列表
def get_user_xnr_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'submitter':user_account}},
                        {'term':{'create_status':2}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list                         

#查询虚拟人uid
def lookup_xnr_uid(xnr_user_no):
    try:
        xnr_result=es_xnr.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']
        xnr_uid=xnr_result['uid']
    except:
        xnr_uid=''
    return xnr_uid


#查询关注者或粉丝列表
def lookup_xnr_fans_followers(xnr_user_no,lookup_type):
    try:
        xnr_result=es_xnr.get(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
        lookup_list=xnr_result[lookup_type]
    except:
        lookup_list=[]
    return lookup_list


#查询tid的comment、favorite、retweet等字段的数值
def lookup_tid_attend_index(tid,today_datetime):
    twitter_count_index_name=get_timets_set_indexset_list(twitter_count_index_name_pre,today_datetime,today_datetime)
    
    query_body={
    	'query':{
    		'filtered':{
    			'filter':{
    				'bool':{'must':{'term':{'tid':tid}}}
    			}
    		}
    	},
    	'size':MAX_WARMING_SIZE,
    	'sort':{'update_time':{'order':'desc'}}
    }
    try:
        result=es_xnr.search(index=twitter_count_index_name,doc_type=twitter_count_index_type,body=query_body)['hits']['hits']
        print result
        tid_result=[]
        for item in result:
            tid_result.append(item['_source'])
    except:
        tid_result=[]
    return tid_result

#################################################
#言论内容预警
def create_speech_warning(xnr_user_no,today_datetime):
    #查询关注列表
    lookup_type='followers_list'
    followers_list=lookup_xnr_fans_followers(xnr_user_no,lookup_type)
    
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{'must':{'range':{'sensitive':{'gte':1}}}}
                }
            }
        },
        'size':MAX_SEARCH_SIZE,
        'sort':{'sensitive':{'order':'desc'}}
    }
    twitter_flow_text_index_name=get_timets_set_indexset_list(twitter_flow_text_index_name_pre,today_datetime,today_datetime)
    #print twitter_flow_text_index_name
    results=es_xnr.search(index=twitter_flow_text_index_name,doc_type=twitter_flow_text_index_type,body=query_body)['hits']['hits']
    #print results
    result=[]
    for item in results:
        if item['_source']['uid'] in followers_list:
            item['_source']['content_type']='follow'
        else:
            item['_source']['content_type']='unfollow'

        item['_source']['validity']=0
        item['_source']['xnr_user_no']=xnr_user_no

        #查询三个指标字段
        tid_result=lookup_tid_attend_index(item['_source']['tid'],today_datetime)
        if tid_result:
            item['_source']['comment']=tid_result['comment']
            item['_source']['share']=tid_result['share']
            item['_source']['favorite']=tid_result['favorite']
        else:
            item['_source']['comment']=0
            item['_source']['share']=0
            item['_source']['favorite']=0        	

        task_id=xnr_user_no+'_'+item['_source']['tid']

        #写入数据库
        today_date=ts2datetime(today_datetime)
        twitter_speech_warning_index_name=twitter_speech_warning_index_name_pre+today_date
        # try:
        es_xnr.index(index=twitter_speech_warning_index_name,doc_type=twitter_speech_warning_index_type,body=item['_source'],id=task_id)
        mark=True
        # except:
        #     mark=False

        result.append(mark)
    return result


#人物行为预警
def create_personal_warning(xnr_user_no,today_datetime):
    #查询关注列表
    lookup_type='followers_list'
    followers_list=lookup_xnr_fans_followers(xnr_user_no,lookup_type)

    #查询虚拟人uid
    xnr_uid=lookup_xnr_uid(xnr_user_no)

    #计算敏感度排名靠前的用户
    query_body={
        # 'query':{
        #     'filtered':{
        #         'filter':{
        #             'terms':{'uid':followers_list}
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

    twitter_flow_text_index_name=get_timets_set_indexset_list(twitter_flow_text_index_name_pre,today_datetime,today_datetime)
    
    try:   
        first_sum_result=es_xnr.search(index=twitter_flow_text_index_name,doc_type=twitter_flow_text_index_type,\
        body=query_body)['aggregations']['friends_sensitive_num']['buckets']
    except:
        first_sum_result=[]

    #print 'first_sum_result',first_sum_result
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
    #####################
    #如果是关注者，则用户敏感度计算值增加1.2倍
    #####################
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
            #user_result=es_xnr.get(index=twitter_feedback_friends_index_name,doc_type=twitter_feedback_friends_index_type,id=user_lookup_id)['_source']
            user_result=es_xnr.get(index=twitter_user_index_name,doc_type=twitter_user_index_type,id=user['uid'])['_source']
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
                                {'range':{'sensitive':{'gte':1}}}
                            ]
                        }
                    }
                }
            },
            'size':MAX_WARMING_SIZE,
            'sort':{'sensitive':{'order':'desc'}}
        }

        try:
            second_result=es_xnr.search(index=twitter_flow_text_index_name,doc_type=twitter_flow_text_index_type,body=query_body)['hits']['hits']
        except:
            second_result=[]

        s_result=[]
        for item in second_result:
            #查询三个指标字段
            tid_result=lookup_tid_attend_index(item['_source']['tid'],today_datetime)
            if tid_result:
                item['_source']['comment']=tid_result['comment']
                item['_source']['share']=tid_result['share']
                item['_source']['favorite']=tid_result['favorite']
            else:
                item['_source']['comment']=0
                item['_source']['share']=0
                item['_source']['favorite']=0   

            s_result.append(item['_source'])

        s_result.sort(key=lambda k:(k.get('sensitive',0)),reverse=True)
        user_detail['content']=json.dumps(s_result)

        user_detail['xnr_user_no']=xnr_user_no
        user_detail['validity']=0
        user_detail['timestamp']=today_datetime

        #写入数据库
        today_date=ts2datetime(today_datetime)
        twitter_user_warning_index_name=twitter_user_warning_index_name_pre+today_date

        task_id=xnr_user_no+'_'+user_detail['uid']
        if s_result:
            try:
                es_xnr.index(index=twitter_user_warning_index_name,doc_type=twitter_user_warning_index_type,body=user_detail,id=task_id)
                mark=True
            except:
                mark=False
        else:
            pass

        results.append(mark)

    return results



#时间预警
def create_date_warning(today_datetime):
    query_body={
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE,
        'sort':{'date_time':{'order':'asc'}}
    }
    try:
        result=es_xnr.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
        date_result=[]
        for item in result:
            #计算距离日期
            date_time=item['_source']['date_time']
            year=ts2yeartime(today_datetime)
            warming_date=year+'-'+date_time
            today_date=ts2datetime(today_datetime)
            countdown_num=(datetime2ts(warming_date)-datetime2ts(today_date))/DAY
        
            if abs(countdown_num) < WARMING_DAY:
                #根据给定的关键词查询预警微博
                print 'date_time:',date_time
                keywords=item['_source']['keywords']
                date_warming=lookup_twitter_date_warming(keywords,today_datetime)
                item['_source']['twitter_date_warming_content']=json.dumps(date_warming)
                item['_source']['validity']=0
                item['_source']['timestamp']=today_datetime   

                task_id=str(item['_source']['create_time'])+'_'+str(today_datetime)    
                #print 'task_id',task_id
                #print 'date_warming',date_warming
                #写入数据库
                
                twitter_timing_warning_index_name=twitter_timing_warning_index_name_pre+warming_date
                
                if date_warming:
                    print twitter_timing_warning_index_name
                    try:

                        es_xnr.index(index=twitter_timing_warning_index_name,doc_type=twitter_timing_warning_index_name,body=item['_source'],id=task_id)
                        mark=True
                    except:
                        mark=False
                else:
                    pass

                date_result.append(mark)
        else:
            pass

    except:
        date_result=[]
    return date_result


def lookup_twitter_date_warming(keywords,today_datetime):
    keyword_query_list=[]
    for keyword in keywords:
        #print 'keyword:',keyword
        keyword_query_list.append({'wildcard':{'text':'*'+keyword.encode('utf-8')+'*'}})

    twitter_flow_text_index_name=get_timets_set_indexset_list(twitter_flow_text_index_name_pre,today_datetime,today_datetime)

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
        temp_result=es_xnr.search(index=twitter_flow_text_index_name,doc_type=twitter_flow_text_index_type,body=query_body)['hits']['hits']
        date_result=[]
        print 'temp_result::',temp_result
        for item in temp_result:
        	#查询三个指标字段
            tid_result=lookup_tid_attend_index(item['_source']['tid'],today_datetime)
            if fid_result:
                item['_source']['comment']=tid_result['comment']
                item['_source']['share']=tid_result['share']
                item['_source']['favorite']=tid_result['favorite']
            else:
                item['_source']['comment']=0
                item['_source']['share']=0
                item['_source']['favorite']=0 
            date_result.append(item['_source'])
    except:
            date_result=[]
    return date_result






#twitter预警内容组织
def create_twitter_warning():
    #时间设置
    if S_TYPE == 'test':
        test_day_date=TWITTER_FLOW_START_DATE
        today_datetime=datetime2ts(test_day_date) - DAY
        start_time=today_datetime
        end_time=today_datetime
        operate_date=ts2datetime(start_time) 
    else:
        now_time=int(time.time())
        today_datetime=datetime2ts(ts2datetime(now_time)) - DAY 
        start_time=today_datetime    #前一天0点
        end_time=today_datetime          #定时文件启动的0点
        operate_date=ts2datetime(start_time)

    account_list=get_user_account_list()
    for account in account_list:
        #xnr_list=get_user_xnr_list(account)
        #print xnr_list
        xnr_list=['TXNR0001']
        for xnr_user_no in xnr_list:
            #人物行为预警
            personal_mark=create_personal_warning(xnr_user_no,today_datetime)
            #言论内容预警
            speech_mark=create_speech_warning(xnr_user_no,today_datetime)
            speech_mark=True
            #事件涌现预警
            # create_event_warning(xnr_user_no,today_datetime,write_mark=True)

    #时间预警
    date_mark=create_date_warning(today_datetime)

    return True


if __name__ == '__main__':
    create_twitter_warning()



