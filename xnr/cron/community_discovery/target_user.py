# -*- coding:utf-8 -*-
'''
用于社区发现，锁定目标用户
通过影响力、敏感度、关键词锁定
'''

import json
import time
import sys
reload(sys)
sys.path.append('../../')
from global_config import S_TYPE,S_DATE_BCI
from parameter import DAY,MAX_SEARCH_SIZE,MAX_CACULATE_USER_NUM,MAX_FLOW_TEXT_DAYS,MAX_TARGET_USER_NUM
from time_utils import ts2datetimestr,ts2datetime,datetime2ts,get_flow_text_index_list,datetimestr2ts
from global_utils import es_xnr,weibo_community_target_user_index_name_pre,weibo_community_target_user_index_type,\
                         es_user_portrait,es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                         weibo_bci_index_name_pre,weibo_bci_index_type


def get_bci_index_list(date_range_end_ts):
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetimestr(date_range_start_ts)
        index_name = weibo_bci_index_name_pre + date_range_start_datetime
        if es_user_portrait.indices.exists(index=index_name):
            index_name_list.append(index_name)
        else:
            pass

    return index_name_list


def caculate_inflence_user(today_datetime):
    bci_index_list=get_bci_index_list(today_datetime)
    # print 'bci_index_lsit:',bci_index_list
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'range':{'user_index':{'gt':0}}}
                        ]
                    }
                }
            }
        },
        'aggs':{
            'user_influence_sum':{
                'terms':{'field':'user','size':MAX_CACULATE_USER_NUM,'order':[{'influence_sum':'desc'}]},
                'aggs':{
                    'influence_sum':{
                        'sum':{'field':'user_index'}
                    }
                },

            }
            }
    }
    influence_uid_info=[]
    influence_uidlist=[]    
    try:   
        influence_result=es_user_portrait.search(index=bci_index_list,doc_type=weibo_bci_index_type,\
        body=query_body)['aggregations']['user_influence_sum']['buckets']
        # print influence_result
        for i in xrange(0,len(influence_result)):
            user_influence=influence_result[i]['influence_sum']['value']
            user_dict=dict()
            user_dict['uid']=influence_result[i]['key']
            user_dict['influence']=user_influence
            influence_uid_info.append(user_dict)
            influence_uidlist.append(influence_result[i]['key'])
    except:
        influence_uid_info=[]
        influence_uidlist=[] 

    return influence_uidlist,influence_uid_info


def caculate_sensitive_user(today_datetime):
    flow_text_index_list=get_flow_text_index_list(today_datetime)
    # print flow_text_index_list
    #计算敏感度排名靠前的用户
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'range':{'sensitive':{'gt':0}}}
                        ]
                    }
                }
            }
        },
        'aggs':{
            'user_sensitive_sum':{
                'terms':{'field':'uid','size':MAX_CACULATE_USER_NUM,'order':[{'sensitive_sum':'desc'}]},
                'aggs':{
                    'sensitive_sum':{
                        'sum':{'field':'sensitive'}
                    }
                }                        
            }
            }
        
    }

    sensitive_uid_info=[]
    sensitive_uidlist=[]    
    try:   
        sensitive_result=es_user_portrait.search(index=flow_text_index_list,doc_type=flow_text_index_type,\
        body=query_body)['aggregations']['user_sensitive_sum']['buckets']
        # print sensitive_result
        for i in xrange(0,len(sensitive_result)):
            user_sensitive=sensitive_result[i]['sensitive_sum']['value']
            user_dict=dict()
            user_dict['uid']=sensitive_result[i]['key']
            user_dict['sensitive']=user_sensitive
            sensitive_uid_info.append(user_dict)
            sensitive_uidlist.append(sensitive_result[i]['key'])
    except:
        sensitive_uid_info=[]
        sensitive_uidlist=[] 

    return sensitive_uidlist,sensitive_uid_info


def get_user_keywords(uid,today_datetime):
    flow_text_index_list = get_flow_text_index_list(today_datetime)
    query_body={
        '_source':['keywords_string'],
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'uid':uid}}
                        ]
                    }
                }
            }
        },
        'size':MAX_SEARCH_SIZE
    }
    results = es_flow_text.search(index=flow_text_index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    # print results
    keywords_list = []
    for item in results:
    	keywords_list.extend(item['_source']['keywords_string'].split('&'))
    temp_keywords = list(set(keywords_list))
    keywords = '&'.join(temp_keywords)
    # print keywords
    return keywords


def get_target_userinfo():
    if S_TYPE == 'test':
        today_datetime = datetime2ts(S_DATE_BCI)
        today_date = ts2datetime(today_datetime)
        now_time = today_datetime
    else:
        today_datetime = int(time.time())
        today_date = ts2datetime(today_datetime)
        now_time = int(time.time())

    influence_uidlist,influence_uid_info = caculate_inflence_user(today_datetime)
    sensitive_uidlist,sensitive_uid_info = caculate_sensitive_user(today_datetime)
    
    # print 'influence_uidlist:',len(influence_uidlist)
    # print 'sensitive_uidlist:',len(sensitive_uidlist)
    target_uidlist = list((set(influence_uidlist)) & (set(sensitive_uidlist)))
    target_temp_uidlist=list((set(influence_uidlist)) | (set(sensitive_uidlist)))
    target_uidlist.extend(target_temp_uidlist)
    target_uidlist = target_uidlist[0:MAX_TARGET_USER_NUM]
    print 'target_uidlist:',len(target_uidlist)

    # sensitive_count=0
    # influence_count=0
    mark_list = []
    community_target_user_index_name = weibo_community_target_user_index_name_pre + today_date
    for uid in target_uidlist:
        user_dict=dict()
        user_dict['uid'] = uid
        inf_list = [u['influence'] for u in influence_uid_info if u['uid'] == uid]
        user_dict['influence'] = inf_list[0] if len(inf_list) > 0 else 0.0
        sens_list = [u['sensitive'] for u in sensitive_uid_info if u['uid'] == uid]
        user_dict['sensitive'] = sens_list[0] if len(sens_list) > 0 else 0.0
        user_dict['keywords'] = get_user_keywords(uid,today_datetime)
        user_dict['timestamp'] = now_time
        user_dict['community_id'] = ''

        task_id = uid + str(now_time)

        # if user_dict['influence'] > 0 :
        #     influence_count =influence_count+1
        # if user_dict['sensitive'] > 0 :
        #     sensitive_count =sensitive_count+1

        try:
            es_xnr.index(index=community_target_user_index_name,doc_type=weibo_community_target_user_index_type,body=user_dict,id=task_id)
            mark=True
        except:
            mark=False
        mark_list.append(mark)

    # print influence_count,sensitive_count
    return target_uidlist,mark_list




if __name__ == '__main__':
    start_time=int(time.time())
    get_target_userinfo()
    end_time=int(time.time())
    print 'time_cost:',end_time - start_time
    

