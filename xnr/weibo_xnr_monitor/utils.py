# -*- coding:utf-8 -*-

'''
weibo information monitor function about database task
'''
import sys
#import time,datetime
from xnr.time_utils import ts2datetime,datetime2ts
from xnr.global_utils import es_flow_text,flow_text_index_name_pre,flow_text_index_type
from xnr.parameter import MAX_VALUE,DAY


#lookup all weibo users
def lookup_weibo_users():
    query_body={
            'query':{
                'match_all':{}
                },
            }
    results=es_flow_text.search(index='weibo_user',doc_type='user',body=query_body)['hits']['hits']
    weibo_users=[]
    for item in results:
        weibo_users.append(item['_source']['uid'])
    return weibo_users



#lookup weibo_xnr concerned users
#def lookup_weiboxnr_concernedusers(weiboxnr_id):



#lookup weibo_xnr unattended users
#def lookup_weiboxnr_unattendedusers(weiboxnr_id):

#lookup keywords_string limit with xnr concerned users and time ranges
#input:from_ts,to_ts,weiboxnr_id
#output:keywords_dict,it's used to create wordcloud
def lookup_weibo_keywordstring(from_ts,to_ts,weiboxnr_id):
    
    #step 1 :adjust the time condition for time
    from_date_ts=datetime2ts(ts2datetime(from_ts))
    to_date_ts=datetime2ts(ts2datetime(to_ts))
    range_time_list=[]
    if from_date_ts != to_date_ts:
        iter_date_ts=from_date_ts
        while iter_date_ts <= to_date_ts:
            iter_next_date_ts=iter_date_ts+DAY
            range_time_list.append({'range':{'timestamp':{'gte':iter_date_ts,'lt':iter_next_date_ts}}})
            iter_date_ts=iter_next_date_ts
        if range_time_list[0]['range']['timestamp']['gte']<from_ts:
            range_time_list[0]['range']['timestamp']['gte']=from_ts
        if range_time_list[-1]['range']['timestamp']['lt']>to_ts:
            range_time_list[-1]['range']['timestamp']['lt']=to_ts

    else:
        # lookup from_ts and to_ts ranges in the same index
        range_time_list=[{'range':{'timestamp':{'gte':from_ts,'lt':to_ts}}}]

    #step 2 :select the range of users
    #lookup xnr concerned userslist
    #userslist=lookup_weiboxnr_concernedusers(weiboxnr_id)
    userslist=lookup_weibo_users()

    user_condition_list=[{'terms':{'uid':userslist}}]

    #step 3:lookup the content
    for range_item in range_time_list:
        iter_condition_list=[item for item in user_condition_list]
        #iter_condition_list=user_condition_list
        iter_condition_list.append(range_item)

        range_from_ts=range_item['range']['timestamp']['gte']
        range_from_date=ts2datetime(range_from_ts)
        flow_text_index_name=flow_text_index_name_pre+range_from_date

        print flow_text_index_name
        print iter_condition_list
        
        query_body={
            'query':{
                'bool':{
                    'must':iter_condition_list
                }
            },
            'aggs':{
                'keywords':{
                    'terms':{
                        'field':'keywords_string'
                    }
                }
            }
        }

        try:
            flow_text_exist=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                body=query_body)['aggregations']['keywords']['buckets']
        except:
            flow_text_exist=[]
    return flow_text_exist


###################################################################################
#测试代码，可删除，暂时保留作为参考
###################################################################################
def aggs_test():
    condition_list=[{'terms':{'uid':[6024035247,6011381738,5064359977]}},{'range':{'timestamp':{'gte':1479569396,'lt':1479569398}}}]
    query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':condition_list
                        }
                    }
                }
                
                
            },
            'aggs':{
                'keywords':{
                    'terms':{
                        'field':'keywords_string'
                    }
                }
            }
        }

    flow_text_exist=es_flow_text.search(index='flow_text_2016-11-19',doc_type=flow_text_index_type,\
            body=query_body)['aggregations']['keywords']['buckets']

        #scan the flow_text_exist content and change the from to keywords dict
    return flow_text_exist

###################################################################################
###################################################################################

#lookup hot posts
#input:from_ts,to_ts,weiboxnr_id,classify_id,search_content,order_id
#output:weibo hot_posts content
def lookup_hot_posts(from_ts,to_ts,weiboxnr_id,classify_id,search_content,order_id):
    #step 1 :adjust the time condition for time
    from_date_ts=datetime2ts(ts2datetime(from_ts))
    to_date_ts=datetime2ts(ts2datetime(to_ts))
    if from_date_ts != to_date_ts:
        iter_date_ts=from_date_ts
        while iter_date_ts <= to_date_ts:
            iter_next_date_ts=iter_date_ts+DAY
            range_time_list.append({'range':{'timestamp':{'gte':iter_date_ts,'lt':iter_next_date_ts}}})
            iter_date_ts=iter_next_date_ts
        if range_time_list[0]['range']['timestamp']['gte']<from_ts:
            range_time_list[0]['range']['timestamp']['gte']=from_ts
        if range_time_list[-1]['range']['timestamp']['lt']>to_ts:
            range_time_list[-1]['range']['timestamp']['lt']=to_ts

    else:
        # lookup from_ts and to_ts ranges in the same index
        range_time_list=[{'range':{'timestamp':{'gte':from_ts,'lt':to_ts}}}]

    #step2: users condition
    #make sure the users range by classify choice
    if classify_id==0:
        userlist=lookup_weibo_users()
    elif classify_id==1:
        userlist=lookup_weiboxnr_concernedusers(weiboxnr_id)
    elif classify_id==2:
        userlist=lookup_weoboxnr_unattendedusers(weiboxnr_id)
    else:
        userlist=lookup_weibo_users()
    user_condition_list=[{'terms':{'uid':userlist}}]

    #step 3:keyword condition
    if search_content:
        keyword_condition_list=[{'match':{'text':{'query':search_content}}}]
    else:
        keyword_condition_list=[]

    #step 4:sort order condition set
    #if order_id==1:
        #sort_condition_list=[{'timestamp':{'order':'desc'}}]
    #elif order_id==2:
        #sort_condition_list=[{'hot':{'order':'desc'}}]
    #elif order_id==3:
        #sort_condition_list=[{'mingan':{'order':'desc'}}]
    #else:
    sort_condition_list=[{'timestamp':{'order':'desc'}}]

    #step 5:lookup the content
    for range_item in range_time_list:
        iter_condition_list=[item for item in user_condition_list]
        iter_condition_list.append(keyword_condition_list)
        iter_condition_list.append(range_item)

        range_from_ts=range_item['range']['timestamp']['gte']
        range_from_date=ts2datetime(range_from_ts)
        flow_text_index_name=flow_text_index_name_pre+range_from_date
        
        query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':iter_condition_list
                            }
                        }
                    }
                },
            'size':MAX_VALUE,
            'sort':sort_condition_list
            }
        try:
            flow_text_exist=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                body=query_body)['hits']['hits']
        except:
            flow_text_exist=[]
        #scan the flow_text_exist content and change the from to hot posts
        return flow_text_exist
###############################################################

#lookup acitve_user
#input:classify_id,weiboxnr_id
#output:active weibo_user info list
def lookup_active_weibouser(classify_id,weiboxnr_id):
    #step1: users condition
    #make sure the users range by classify choice
    if classify_id==0:
        userlist=lookup_weibo_users()
    elif classify_id==1:
        userlist=lookup_weiboxnr_concernedusers(weiboxnr_id)
    elif classify_id==2:
        userlist=lookup_weoboxnr_unattendedusers(weiboxnr_id)
    else:
        userlist=lookup_weibo_users()
    user_condition_list=[{'terms':{'uid':userlist}}]

    #step 2:lookup users and ranked by infuluence
    query_body={
            '_source':{
                'include':[
                    'id',            #用户ID
                    'nick_name',     #昵称
                    'user_location', #注册地
                    'fansum',        #粉丝数
                    'weibosum',      #微博数，该字段暂未创建
                    'infulence',     #影响力，该字段需创建然后计算
                ]
            },
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':iter_condition_list
                            }
                        }
                    }
                },
            'size':MAX_VALUE,
            'sort':{'infuluence':{'order':'desc'}}    #根据影响力排名
            }
    try:
        flow_text_exist=es_flow_text.search(index='weibo_user',doc_type='user',body=query_body)['hits']['hits']
    except:
        flow_text_exist=[]

    return flow_text_exist






######################
#lookup weibo info based on userlist and time
######################
def lookup_weibo_info(ts_first,ts_second,userlist):
    time1=time.mktime(ts_first.timetuple())
    time2=time.mktime(ts_second.timetuple())
    query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'terms':{'uid':userlist}},
                                {'range':{
                                    'timestamp':{
                                        'gte':time1,
                                        'lte':time2
                                        }
                                    }}
                                ]
                            }
                        }
                    }
                },
           #'size':999999
            'size':MAX_VALUE
            }

    datetime_1=ts2datetime(time1)
    datetime_2=ts2datetime(time2)
    index_name_1=flow_text_index_name_pre+datetime_1
    print index_name_1
    exist_es_1=es_flow_text.indices.exists(index_name_1)
    index_name_2=flow_text_index_name_pre+datetime_2
    exist_es_2=es_flow_text.indices.exists(index_name_2)


    if datetime_1 == datetime_2 and exist_es_1:
        search_results=es_flow_text.search(index=index_name_1,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    elif datetime_1 !=datetime_2 and exist_es_2:
        search_results=es_flow_text.search(index=index_name_2,doc_tyoe=flow_text_index_type,body=query_body)['hits']['hits']
    else:
        search_results=[]
   # search_results=es_flow_text.search(index=index_name_1,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
   # print search_results
    keyword_list=[]
    if search_results:
        for item in search_results:
            keyword_list.append(item['_source']['keywords_string'])

   # return search_results
    return keyword_list


#count the keyword 
def count_weiboxnr_keyword(keyword_list):
    word_list=[]
    for item in keyword_list:
        words=item.split('&')
        word_list.extend(words)
    keyword_dict={}
    for word in word_list:
        keyword_dict[word]=word_list.count(word)
    return keyword_dict
#########################################

#########################################



            


