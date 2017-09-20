#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
use to caculate_history information
'''
import os
import time
import datetime
import json
from xnr.global_utils import es_xnr,xnr_flow_text_index_name_pre,xnr_flow_text_index_type,\
                             weibo_xnr_count_info_index_name,weibo_xnr_count_info_index_type
from xnr.time_utils import datetime2ts,ts2datetime,DAY
from xnr.time_utils import get_timeset_indexset_list

#统计信息表
def create_xnr_history_info_count(xnr_user_no,create_time):
    create_date=ts2datetime(create_time)
    weibo_xnr_flow_text_name=xnr_flow_text_index_name_pre+create_date

    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_user_no':xnr_user_no}
                }
            }
        },
        'aggs':{
            'all_task_source':{
                'terms':{
                    'field':'task_source'
                }
            }
        }
    }

    xnr_user_detail=dict()
    #时间
    xnr_user_detail['date_time']=create_date
    try:
        xnr_result=es_xnr.search(index=weibo_xnr_flow_text_name,doc_type=xnr_flow_text_index_type,body=query_body)
        #今日总粉丝数
        for item in xnr_result['hits']['hits']:
            xnr_user_detail['user_fansnum']=item['_source']['user_fansnum']
        # daily_post-日常发帖,hot_post-热点跟随,business_post-业务发帖
        for item in xnr_result['aggregations']['all_task_source']['buckets']:
            if item['key'] == 'daily_post':
                xnr_user_detail['daily_post_num']=item['doc_count']
            elif item['key'] == 'business_post':
                xnr_user_detail['business_post_num']=item['doc_count']
            elif item['key'] == 'hot_post':
                xnr_user_detail['hot_follower_num']=item['doc_count']
        #总发帖量
        xnr_user_detail['total_post_sum']=xnr_user_detail['daily_post_num']+xnr_user_detail['business_post_num']+xnr_user_detail['hot_follower_num']
    except:
        xnr_user_detail['user_fansnum']=0
        xnr_user_detail['daily_post_num']=0
        xnr_user_detail['business_post_num']=0
        xnr_user_detail['hot_follower_num']=0
        xnr_user_detail['total_post_sum']=0

    count_id=xnr_user_no+'_'+create_date
    xnr_user_detail['xnr_user_no']=xnr_user_no

    try:
        es_xnr.index(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,body=xnr_user_detail,id=count_id)
        mark=xnr_user_detail
    except:
        mark=dict()
    return mark
'''
def create_xnr_history_info_count(xnr_user_no,now_time):
    end_time=datetime2ts(ts2datetime(now_time))
    end_date=ts2datetime(end_time-DAY)
    start_date=ts2datetime(end_time-8*DAY)

    weibo_xnr_flow_text_listname=get_timeset_indexset_list(xnr_flow_text_index_name_pre,start_date,end_date)
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_user_no':xnr_user_no}
                }
            }
        },
        'aggs':{
            'all_task_source':{
                'terms':{
                    'field':'task_source'
                }
            }
        }
    }
    mark_list=[]
    for index_name in weibo_xnr_flow_text_listname:
        xnr_user_detail=dict()
        #时间
        xnr_user_detail['date_time']=index_name[-10:]
        try:
            xnr_result=es_xnr.search(index=index_name,doc_type=xnr_flow_text_index_type,body=query_body)
            #今日总粉丝数
            for item in xnr_result['hits']['hits']:
                xnr_user_detail['user_fansnum']=item['_source']['user_fansnum']
            # daily_post-日常发帖,hot_post-热点跟随,business_post-业务发帖
            for item in xnr_result['aggregations']['all_task_source']['buckets']:
                if item['key'] == 'daily_post':
                    xnr_user_detail['daily_post_num']=item['doc_count']
                elif item['key'] == 'business_post':
                    xnr_user_detail['business_post_num']=item['doc_count']
                elif item['key'] == 'hot_post':
                    xnr_user_detail['hot_follower_num']=item['doc_count']
            #总发帖量
            xnr_user_detail['total_post_sum']=xnr_user_detail['daily_post_num']+xnr_user_detail['business_post_num']+xnr_user_detail['hot_follower_num']
        except:
            xnr_user_detail['user_fansnum']=0
            xnr_user_detail['daily_post_num']=0
            xnr_user_detail['business_post_num']=0
            xnr_user_detail['hot_follower_num']=0
            xnr_user_detail['total_post_sum']=0

        count_id=xnr_user_no+xnr_user_detail['date_time']
        xnr_user_detail['xnr_user_no']=xnr_user_no

        try:
            es_xnr.index(index=weibo_xnr_count_info_index_name,doc_type=weibo_xnr_count_info_index_type,body=xnr_user_detail,id=count_id)
            mark=True
        except:
            mark=False
        mark_list.append(mark)
    return mark_list
'''

