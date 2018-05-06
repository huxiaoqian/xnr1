# -*- coding: utf-8 -*-
import os
import json
import time
import sys
import networkx as nx
import json,os,time,community
import numpy as np
import math
import redis
from community_find_weibo import group_evaluate
from weibo_select_community import get_community_coreuser_socail
sys.path.append('../../')

from global_utils import es_xnr,weibo_trace_community_index_name_pre,weibo_trace_community_index_type,\
                         weibo_community_index_name_pre,weibo_community_index_type,\
                         es_user_profile,profile_index_name,profile_index_type,\
                         es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                         es_retweet,retweet_index_name_pre,retweet_index_type,\
                         be_retweet_index_name_pre,be_retweet_index_type,\
                         es_comment,comment_index_name_pre,comment_index_type,\
                         be_comment_index_name_pre,be_comment_index_type,\
                         es_user_profile,weibo_bci_history_index_name,weibo_bci_history_index_type,\
                         weibo_sensitive_history_index_name,weibo_sensitive_history_index_type,\
                         es_user_portrait,weibo_bci_index_name_pre,weibo_bci_index_type


from time_utils import ts2datetime,datetime2ts
from parameter import DAY
from global_config import S_TYPE,WEIBO_COMMUNITY_DATE,R_BEGIN_TIME
from global_utils import retweet_redis_dict,comment_redis_dict

r_beigin_ts = datetime2ts(R_BEGIN_TIME)

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
    print index_name_list
    return index_name_list


#查询需跟踪社区
def get_trace_community(date_time):
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'terms':{'community_status':[1,-2]}}
                        ]
                    }
                }
            }
        }
    }
    weibo_community_index_name = get_community_index(date_time)
    try:
        community_result = es_xnr.search(index=weibo_community_index_name,\
            doc_type=weibo_community_index_type,body=query_body)['hits']['hits']
        community_list = []
        for item in community_result:
            community_list.append(item['_source'])
    except:
        community_list = []

    return community_list


def get_evaluate_max(index_name,index_type,field):
    query_body = {
        'query':{
            'match_all':{}
            },
        'size':1,
        'sort':[{field: {'order': 'desc'}}]
        }
    try:
        result = es_user_profile.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        max_evaluate = result[0]['_source'][field]
    except Exception, e:
        raise e
        max_evaluate = 1
    return max_evaluate

#计算社区指标
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = 2 - (((date_ts - r_beigin_ts) / (DAY * 7))) % 2
    #run_type
    if S_TYPE == 'test':
        db_number = 1
    return db_number


def get_sensitive_value(date_time,field_name,uid_list):
    flow_text_index_name = flow_text_index_name_pre + ts2datetime(date_time)
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[{'terms':{'uid':uid_list}}]
                    }
                }
            }
        },
        'aggs':{
            'index_field_sum':{
                'terms':{
                    'field':field_name
                }
            }
        }
    }

    try:
        result=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
            body=query_body)['aggregations']['index_field_sum']['buckets']
        index_value_list = []
        for item in result:
            index_value_list.append(item['doc_count'])
    except Exception,e:
        print '敏感度查询错误：：',e
        index_value_list = []
    return index_value_list


def get_influence_value(date_time,field_name,uid_list):
    datename = ts2datetime(date_time - DAY)
    new_datetime = datename[0:4]+datename[5:7]+datename[8:10]
    bci_index_name = weibo_bci_index_name_pre + new_datetime
    index_value_list = []
    try:
        result = es_user_portrait.mget(index=bci_index_name,doc_type=weibo_bci_index_type,body={'ids':uid_list},_source=True)['docs']
        for item in result:
           # print 'item_influence::',item
           # print 'item_type::',type(item)
            if item['found']:
                index_value_list.append(item['_source']['user_index'])
    except Exception,e:
        print '影响力查询错误：：',e
    return index_value_list


def group_evaluate_trace(xnr_user_no,nodes,all_influence,all_sensitive,date_time,G=None):
    result = {}
    result['xnr_user_no'] = xnr_user_no
    result['nodes'] = nodes
    result['num'] = len(nodes)

    #从redis中获取社区转发网络
    count = 0
    scan_cursor = 1
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #get redis db number
    db_number = get_db_num(now_date_ts)
    print 'db_number:',str(db_number)
    #get redis db
    print 'retweet_dict::',retweet_redis_dict
    retweet_redis = retweet_redis_dict[str(db_number)]
    comment_redis = comment_redis_dict[str(db_number)]

    retweet_result = []
    for uid in nodes:
        item_1 = str('retweet_' + uid)
       # print 'item_lookup::',item_1,type(item_1)
        re_result = retweet_redis.hgetall(item_1)
        if re_result:
            save_dict = dict()
            save_dict['uid'] = uid
            save_dict['uid_retweet'] = re_result
            retweet_result.append(save_dict)
   # print 'test_result::',retweet_result
   # print 'aaa:::', retweet_redis.hgetall('retweet_'+str(nodes[-1]))

    #print 'retweet_redis::',retweet_redis
    #print 'comment_redis::',comment_redis
    ''' 
    re_scan = retweet_redis.scan(scan_cursor,count=10)
    for item in re_scan[1]:
       # item_list = item.split('_')
        print 'item::',item,type(item)
        item_result = retweet_redis.hgetall(item)
        print 'item_result::',item_result
   # print 'hlen::',retweet_redis.hlen()
   # print 'hgetall::',retweet_redis.hgetall()
    retweet_result = retweet_redis.hgetall(nodes)
    comment_result = comment_redis.hgetall(nodes)
    '''
   # print 'retweet_result:::',retweet_result
    #print 'comment_result:::',comment_result

    G_i = nx.Graph()
    for i in retweet_result:
        # print 'i:',i
       # if not i['found']:
       #     continue
        uid_retweet = i['uid_retweet']
        max_count = max([int(n) for n in uid_retweet.values()])
        G_i.add_weighted_edges_from([(i['uid'],j,float(uid_retweet[j])/max_count) for j in uid_retweet.keys() if j != i['uid'] and j and i['uid']])
    '''
    for i in comment_result:
        # print 'comment_i:',i
        if not i['found']:
            continue
        uid_comment = json.loads(i['_source']['uid_comment'])
        max_count = max([int(n) for n in uid_comment.values()])
        G_i.add_weighted_edges_from([(i['_source']['uid'],j,float(uid_comment[j])/max_count) for j in uid_comment.keys() if j != i['_source']['uid'] and j and i['_source']['uid']])
    '''

    sub_g = G_i.subgraph(nodes)

    result['density'] = round(nx.density(sub_g),4)
    #print 'ave_cluster::',nx.average_clustering(sub_g)
    try:
        result['cluster'] = round(nx.average_clustering(sub_g),4)
    except:
        result['cluster'] = 0
    result['transitivity'] = round(nx.transitivity(sub_g),4)


##将结果换成当天的计算结果
    influence_field = 'user_index'
    sensitive_field = 'sensitive'
    influence_result = get_influence_value(date_time,influence_field,nodes)
    sensitive_result = get_sensitive_value(date_time,sensitive_field,nodes)


    result['max_influence'] = round((max(influence_result)/float(all_influence))*100,4)
    result['mean_influence'] = round(((sum(influence_result)/len(influence_result))/float(all_influence))*100,4)

    result['max_sensitive'] = round((max(sensitive_result)/float(all_sensitive))*1,4)
    result['mean_sensitive'] = round(((sum(sensitive_result)/len(sensitive_result))/float(all_sensitive))*1,4)


    return result


#更新社区的预警等级
def update_warning_rank(community,trace_datetime):
    weibo_community_index_name = get_community_index(trace_datetime)
    # community_get = es_xnr.get(index=weibo_community_index_type,doc_type=weibo_community_index_type,id=community_id)['_source']
    # warning_
    try:
        update_result = es_xnr.update(index=weibo_community_index_name,doc_type=weibo_community_index_type,\
            id=community['community_id'],body={'doc':{'warning_rank':community['warning_rank'],\
            'warning_type':community['warning_type'],'density':community['density'],'cluster':community['cluster'],\
            'max_influence':community['max_influence'],'mean_influence':community['mean_influence'],\
            'max_sensitive':community['max_sensitive'],'mean_sensitive':community['mean_sensitive']}})
        mark = True
    except:
        mark = False
    return mark

#存储社区至数据库
def save_community_detail(community_detail,xnr_user_no):
    try:
        es_community = es_xnr.index(index=weibo_trace_community_index_name_pre+xnr_user_no.lower(),\
            doc_type=weibo_trace_community_index_type,body=community_detail,id=community_detail['community_id']+'_'+community_detail['trace_date'])
        mark = True
    except:
        mark = False
    return mark


#预警-滑动平均模型，设置上下界
def get_bound_uplowerlist(community_id,xnr_user_no,bound_type,bound_value):
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
        'size':7,
        'sort':{'trace_time':{'order':'asc'}}
    }
    try:
        es_community = es_xnr.search(index=weibo_trace_community_index_name_pre+xnr_user_no.lower(),\
            doc_type=weibo_trace_community_index_type,body=query_body)['hits']['hits']
        index_list = []
        for item in es_community:
            index_list.append(item['_source'][bound_type])
    except:
        index_list = []

    if index_list:
        mean_index = np.mean(index_list)
        std_index = np.std(index_list)
        index_len = len(index_list)

        lower_bound = mean_index - (1.95*std_index)/math.sqrt(index_len)
        upper_bound = mean_index + (1.95*std_index)/math.sqrt(index_len)
    else:
        lower_bound = bound_value
        upper_bound = bound_value
    return lower_bound,upper_bound

#预警判断
def get_warning_judge(warning_value,lower_bound,upper_bound):
    if warning_value > upper_bound:
        warning_mark = 1
    elif warning_value < lower_bound:
        warning_mark = -1
    else:
        warning_mark = 0

    return warning_mark


# #新社区预警内容跟踪
# def get_newcommunity_warning(community):


#人物信息
def get_user_info(uid_list):
    user_list = []
    user_result = es_user_profile.mget(index = profile_index_name,doc_type = profile_index_type,body = {'ids':uid_list})['docs']
    core_user = []
    for item in user_result:
        user_dict = dict()
        user_dict['uid'] = item['_id']

        if item['found']:
            user_dict['photo_url']=item['_source']['photo_url']            
            user_dict['nick_name']=item['_source']['nick_name']
            user_dict['sex']=item['_source']['sex']
            user_dict['friendsnum']=item['_source']['friendsnum']
            user_dict['fansnum']=item['_source']['fansnum']
            user_dict['user_location']=item['_source']['user_location']
        else:
            user_dict['photo_url']=''            
            user_dict['nick_name']=''
            user_dict['sex']=''
            user_dict['friendsnum']=''
            user_dict['fansnum']=''
            user_dict['user_location']=''

        user_list.append(user_dict)
    return json.loads(user_list)

#人物预警
def get_person_warning(community_id,new_nodes):
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
        'size':1,
        'sort':{'trace_time':{'order':'asc'}}
    }   
    try:
        es_community = es_xnr.search(index=weibo_trace_community_index_name_pre+xnr_user_no.lower(),\
            doc_type=weibo_trace_community_index_type,body=query_body)['hits']['hits']
        for item in es_community:
            old_nodes = item['_source']['nodes']
    except:
        old_nodes = []

    add_nodes = list(set(new_nodes) - set(new_nodes)&set(old_nodes))
    warning_content = get_user_info(add_nodes)
    warning_descp = u'人物突增预警：社区人数由'+str(len(old_nodes))+u'人上升至'+str(len(new_nodes)) +u'人！'

    return warning_descp,warning_content


#获取旧社区指标
def get_index_olddiff(community_id,index_type,index_value,xnr_user_no):
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
        'size':1,
        'sort':{'trace_time':{'order':'asc'}}
    }  
    old_index = 0
    try:
        es_community = es_xnr.search(index=weibo_trace_community_index_name_pre+xnr_user_no.lower(),\
            doc_type=weibo_trace_community_index_type,body=query_body)['hits']['hits']
        for item in es_community:
            old_index = item['_source'][index_type]
    except:
        old_index = 0 
    print 'community_id::',community_id
    print 'index_type::',index_type
    print 'index_value::',index_value
    print 'old_index::',old_index
    index_diff = index_value - old_index
    return old_index,index_diff


#获取预警内容
def get_warning_content(nodes,content_type,trace_datetime):
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'terms':{'uid':nodes}},
                        {'range':{content_type:{'gt':0}}}
                        ]
                    }
                }
            }
        },
        'size':50,
        'sort':{content_type:{'order':'desc'}}
    }
    flow_text_index_name = flow_text_index_name_pre + ts2datetime(trace_datetime)
    print 'flow_text_index_name::',flow_text_index_name
    print 'content_type::',content_type
    try:
        es_content = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
        warning_content = []
        for item in es_content:
            warning_content.append(item['_source'])
    except:
        warning_content = []

    return warning_content


#敏感度预警
def get_sensitive_warning(community,trace_datetime):
    #step 1:计算敏感度变化值
    max_sensitive_type = 'max_sensitive'
    old_max_sensitive,max_sensitive_diff = get_index_olddiff(community['community_id'],max_sensitive_type,community['max_sensitive'],community['xnr_user_no'])

    mean_sensitive_type = 'mean_sensitive'
    old_mean_sensitive,mean_sensitive_diff = get_index_olddiff(community['community_id'],mean_sensitive_type,community['mean_sensitive'],community['xnr_user_no'])

    if mean_sensitive_diff > 0:
        mean_sensitive_desp = u'社区平均敏感度上升了' + str(mean_sensitive_diff) + u'，由'+ str(old_mean_sensitive) + u'上升至' + str(community['mean_sensitive']) +u'；'
    else:
        mean_sensitive_desp = u'社区平均敏感度下降了' + str(abs(mean_sensitive_diff)) + u'，由'+ str(old_mean_sensitive) + u'下降至' + str(community['mean_sensitive']) +u'；'

    if max_sensitive_diff > 0:
        max_sensitive_desp = u'社区最大敏感度上升了' + str(max_sensitive_diff) + u'，由'+ str(old_max_sensitive) + u'上升至' + str(community['max_sensitive']) +u'。'
    else:
        max_sensitive_desp = u'社区最大敏感度下降了' + str(abs(max_sensitive_diff)) + u'，由'+ str(old_max_sensitive) + u'下降至' + str(community['max_sensitive']) +u'。'

    warning_descp = mean_sensitive_desp + max_sensitive_desp

    #step 2:获取敏感内容
    content_type = 'sensitive'
    warning_content = get_warning_content(community['nodes'],content_type,trace_datetime)
    # print 'sensitive_warning_descrp::',warning_descp
    # print 'sensitive_warning_content::',warning_content

    return warning_descp,json.dumps(warning_content)


#影响力预警
def get_influence_warning(community,trace_datetime):
    #step 1:计算影响力变化值
    max_influence_type = 'max_influence'
    old_max_influence,max_influence_diff = get_index_olddiff(community['community_id'],max_influence_type,community['max_influence'],community['xnr_user_no'])

    mean_influence_type = 'mean_influence'
    old_mean_influence,mean_influence_diff = get_index_olddiff(community['community_id'],mean_influence_type,community['mean_influence'],community['xnr_user_no'])

    if mean_influence_diff > 0:
        mean_influence_desp = u'社区平均敏感度上升了' + str(mean_influence_diff) + u'，由'+ str(old_mean_influence) + u'上升至' + str(community['mean_influence']) +u'；'
    else:
        mean_influence_desp = u'社区平均敏感度下降了' + str(abs(mean_influence_diff)) + u'，由'+ str(old_mean_influence) + u'下降至' + str(community['mean_influence']) +u'；'

    if max_influence_diff > 0:
        max_influence_desp = u'社区最大敏感度上升了' + str(max_influence_diff) + u'，由'+ str(old_max_influence) + u'上升至' + str(community['max_influence']) +u'。'
    else:
        max_influence_desp = u'社区最大敏感度下降了' + str(abs(max_influence_diff)) + u'，由'+ str(old_max_influence) + u'下降至' + str(community['max_influence']) +u'。'

    warning_descp = mean_influence_desp + max_influence_desp

    #step 2:获取影响力内容
    content_type = 'retweeted'
    warning_content = get_warning_content(community['nodes'],content_type,trace_datetime)

    return warning_descp,json.dumps(warning_content)


#社区聚集预警
def get_density_warning(community,trace_datetime):
    #计算聚集系数变化值
    density_type = 'density'
    old_density,density_diff = get_index_olddiff(community['community_id'],density_type,community['density'],community['xnr_user_no'])
    if density_diff > 0:
        density_desp = u'社区聚集系数上升了' + str(density_diff) + u',由' + str(old_density) + u'上升至' + str(community['density']) + u'。'
    else:
        density_desp = u'社区聚集系数下降了' + str(abs(density_diff)) + u',由' + str(old_density) + u'下降至' + str(community['density']) + u'。'


    core_uidlist,outer_uidlist,core_user_socail,core_outer_socail = get_community_coreuser_socail(community['nodes'],trace_datetime)
    return density_desp,json.dumps(core_user_socail)
    
#预警处理
def get_warning_reslut(community,trace_datetime):   
    # #新旧社区，区分预警
    # if community['community_status'] == 0 and community['warning_rank'] > 0:
    #     community_result = get_newcommunity_warning(community)
    # else:
    #     community_result = get_tracecommunity_warning(community)

    #备注：暂时不考虑新社区含预警的跟踪，在前端页面对有预警的内容进行提示跟踪
    warning_result = dict()
    warning_type_list = []
    
    num_bound_type = 'num'
    num_lower_bound,num_upper_bound = get_bound_uplowerlist(community['community_id'],community['xnr_user_no'],num_bound_type,community['num'])
    warning_result['num_warning'] = get_warning_judge(community['num'],num_lower_bound,num_upper_bound)
    if warning_result['num_warning'] == 1:
        warning_result['num_warning_descrp'],\
        warning_result['num_warning_content'] = get_person_warning(community['community_id'],community['nodes'])
        num_warning = '人物突增预警'
        warning_type_list.append(num_warning)
    else:
        warning_result['num_warning_descrp'] = ''
        warning_result['num_warning_content'] = ''

    mean_sensitive = 'mean_sensitive'
    max_sensitive = 'max_sensitive'
    mean_sensitive_lower_bound,mean_sensitive_upper_bound = get_bound_uplowerlist(community['community_id'],community['xnr_user_no'],mean_sensitive,community['mean_sensitive'])
    max_sensitive_lower_bound,max_sensitive_upper_bound = get_bound_uplowerlist(community['community_id'],community['xnr_user_no'],max_sensitive,community['max_sensitive'])
    mean_sensitive_mark = get_warning_judge(community['mean_sensitive'],mean_sensitive_lower_bound,mean_sensitive_upper_bound)
    max_sensitive_mark = get_warning_judge(community['max_sensitive'],max_sensitive_lower_bound,max_sensitive_upper_bound)
    if mean_sensitive_mark == 1 or max_sensitive_mark == 1:
        warning_result['sensitive_warning'] = 1
        warning_result['sensitive_warning_descrp'],\
        warning_result['sensitive_warning_content'] = get_sensitive_warning(community,trace_datetime)
        sensitive_warning = '敏感度剧增预警'
        warning_type_list.append(sensitive_warning)
    else:
        warning_result['sensitive_warning'] = mean_sensitive_mark + max_sensitive_mark
        warning_result['sensitive_warning_descrp'] = ''
        warning_result['sensitive_warning_content'] =  ''

    mean_influence = 'mean_influence'
    max_influence = 'max_influence'
    mean_influence_lower_bound,mean_influence_upper_bound = get_bound_uplowerlist(community['community_id'],community['xnr_user_no'],mean_influence,community['mean_influence'])
    max_influence_lower_bound,max_influence_upper_bound = get_bound_uplowerlist(community['community_id'],community['xnr_user_no'],max_influence,community['max_influence'])
    mean_influence_mark = get_warning_judge(community['mean_influence'],mean_influence_lower_bound,mean_influence_upper_bound)
    max_influence_mark = get_warning_judge(community['max_influence'],max_influence_lower_bound,max_influence_upper_bound)
    if mean_influence_mark == 1 or max_influence_mark == 1:
        warning_result['influence_warning'] = 1
        warning_result['influence_warning_descrp'],\
        warning_result['influence_warning_content'] = get_influence_warning(community,trace_datetime)
        influence_warning = '影响力剧增预警'
        warning_type_list.append(influence_warning)
    else:
        warning_result['influence_warning'] = mean_influence_mark + max_influence_mark
        warning_result['influence_warning_descrp'] = ''
        warning_result['influence_warning_content'] = ''      

    # cluster = 'cluster'
    density = 'density'
    # cluster_lower_bound,cluster_upper_bound = get_bound_uplowerlist(community['community_id'],community['xnr_user_no'],cluster,community['cluster'])
    density_lower_bound,density_upper_bound = get_bound_uplowerlist(community['community_id'],community['xnr_user_no'],density,community['density'])
    # cluster_mark = get_warning_judge(community['cluster'],cluster_lower_bound,cluster_upper_bound)
    density_mark = get_warning_judge(community['density'],density_lower_bound,density_upper_bound)
    if density_mark == 1:     
        warning_result['density_warning'] = 1
        warning_result['density_warning_descrp'],\
        warning_result['density_warning_content'] = get_density_warning(community,trace_datetime)
        density_warning = '社区聚集预警'
        warning_type_list.append(density_warning)
    else:
        warning_result['density_warning'] = density_mark
        warning_result['density_warning_descrp'] = ''
        warning_result['density_warning_content'] = ''

    warning_result['warning_type'] = warning_type_list
    return warning_result

    
#跟踪社区
def trace_xnr_community(trace_datetime): #传的是ts
    #step1:获取跟踪社区list
    community_list = get_trace_community(trace_datetime)

    #针对每个社区进行处理
    all_influence = get_evaluate_max(weibo_bci_history_index_name,weibo_bci_history_index_type,'bci_week_ave')
    all_sensitive = get_evaluate_max(weibo_sensitive_history_index_name,weibo_sensitive_history_index_type,'sensitive_week_ave')
    result_mark = []
    for community in community_list:
        community_detail = dict()
        community_detail['xnr_user_no'] = community['xnr_user_no']
        community_detail['community_id'] = community['community_id']
        community_detail['community_name'] = community['community_name']
        community_detail['create_time'] = community['create_time']
        community_detail['trace_time'] = trace_datetime
        community_detail['trace_date'] = ts2datetime(trace_datetime)
        community_detail['num'] = community['num']
        community_detail['nodes'] = community['nodes']


        #判断一下，对于刚生成社区的预警，指标值取生成的
        create_date = ts2datetime(community['create_time'])
        trace_date = ts2datetime(trace_datetime)
        if create_date == trace_date:
            community_detail['density'] = community['density']
            community_detail['cluster'] = community['cluster']
            community_detail['max_influence'] = community['max_influence']
            community_detail['mean_influence'] = community['mean_influence']
            community_detail['max_sensitive'] = community['max_sensitive']
            community_detail['mean_sensitive'] = community['mean_sensitive']

            community_detail['warning_type'] = community['warning_type']

            community_detail['num_warning'] = 0
            community_detail['num_warning_descrp'] = ""
            community_detail['num_warning_content'] = ""

            community_detail['sensitive_warning'] = 0
            community_detail['sensitive_warning_descrp'] = ""
            community_detail['sensitive_warning_content'] = ""

            community_detail['influence_warning'] = 0
            community_detail['influence_warning_descrp'] = ""
            community_detail['influence_warning_content'] = ""

            community_detail['density_warning'] = 0
            community_detail['density_warning_descrp'] = ""
            community_detail['density_warning_content'] = ""  


            for item in community['warning_type']:
                if item == '人物突增预警':
                    community_detail['num_warning'] = 1
                    community_detail['num_warning_descrp'],\
                    community_detail['num_warning_content'] = get_person_warning(community['community_id'],community['nodes'])
                elif item == '影响力剧增预警':
                	community_detail['influence_warning'] = 1
                    community_detail['influence_warning_descrp'],\
                    community_detail['influence_warning_content'] = get_influence_warning(community,trace_datetime)
                elif item == '敏感度剧增预警':
                    community_detail['sensitive_warning'] = 1
                    community_detail['sensitive_warning_descrp'],\
                    community_detail['sensitive_warning_content'] = get_sensitive_warning(community,trace_datetime)
                elif item == '社区聚集预警':
                    community_detail['density_warning'] = 1
                    community_detail['density_warning_descrp'],\
                    community_detail['density_warning_content'] = get_density_warning(community,trace_datetime)         

        else:

            #trace_index_result = group_evaluate(community['xnr_user_no'],community['nodes'],all_influence,all_sensitive)
            trace_index_result = group_evaluate_trace(community['xnr_user_no'],community['nodes'],all_influence,all_sensitive,trace_datetime,G=None)
            community_detail['density'] = trace_index_result['density']
            community_detail['cluster'] = trace_index_result['cluster']
            community_detail['max_influence'] = trace_index_result['max_influence']
            community_detail['mean_influence'] = trace_index_result['mean_influence']
            community_detail['max_sensitive'] = trace_index_result['max_sensitive']
            community_detail['mean_sensitive'] = trace_index_result['mean_sensitive']

            #预警处理
            warning_result = get_warning_reslut(community_detail,trace_datetime)
            community_detail['warning_type'] = warning_result['warning_type']

            community_detail['num_warning'] = warning_result['num_warning']
            community_detail['num_warning_descrp'] = warning_result['num_warning_descrp']
            community_detail['num_warning_content'] = warning_result['num_warning_content']

            community_detail['sensitive_warning'] = warning_result['sensitive_warning']
            community_detail['sensitive_warning_descrp'] = warning_result['sensitive_warning_descrp']
            community_detail['sensitive_warning_content'] = warning_result['sensitive_warning_content']

            community_detail['influence_warning'] = warning_result['influence_warning']
            community_detail['influence_warning_descrp'] = warning_result['influence_warning_descrp']
            community_detail['influence_warning_content'] = warning_result['influence_warning_content']

            community_detail['density_warning'] = warning_result['density_warning']
            community_detail['density_warning_descrp'] = warning_result['density_warning_descrp']
            community_detail['density_warning_content'] = warning_result['density_warning_content']

            community_detail['warning_rank'] = warning_result['num_warning'] + warning_result['sensitive_warning'] + warning_result['influence_warning'] + warning_result['density_warning']
            #更新显示
            update_warningrank_mark = update_warning_rank(community_detail,trace_datetime)

        #存储至数据库
        save_community_mark = save_community_detail(community_detail,community['xnr_user_no'])

        result_mark.append(save_community_mark)

    return result_mark


if __name__ == '__main__':
    if S_TYPE == 'test':
        # test_date = WEIBO_COMMUNITY_DATE
        test_date = '2016-11-27'
        now_time = datetime2ts(test_date)
        # for i in range(0,7):
        #     test_time = now_time + i*DAY
        #     trace_xnr_community(test_time)
        #     i = i+1
    else:
        now_time = int(time.time())
    start_time = int(time.time())
    trace_xnr_community(now_time)
    end_time = int(time.time())
    print 'cost_tiime',end_time - start_time
    print 'dict',retweet_redis_dict
    
