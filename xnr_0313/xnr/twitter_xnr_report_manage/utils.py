# -*- coding:utf-8 -*-

'''
twitter report management
'''

import sys
import json
import xlwt
import time
from xnr.global_utils import es_xnr,twitter_report_management_index_name_pre,twitter_report_management_index_type

from xnr.parameter import MAX_SEARCH_SIZE,DAY

from xnr.time_utils import ts2datetime

from xnr.reportManage.report import Report
from xnr.parameter import SCREEN_WEIBO_USERNAME,SCREEN_WEIBO_PASSWORD


##获取索引
def get_xnr_reportment_index_listname(index_name_pre,date_range_start_ts,date_range_end_ts):
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


def show_report_content(report_type,start_time,end_time):
    query_condition=[]

    if report_type:
    	query_condition.append({'terms':{'report_type':report_type}})
    else:
    	pass

    query_condition.append({'range':{'report_time':{'gte':start_time,'lte':'end_time'}}})

    query_body={
    	'query':{
    		'filtered':{
    			'filter':{
    				'bool':{
    					'must':query_condition
    				}
    			}
    		}
    	},
    	'size':MAX_SEARCH_SIZE,
    	'sort':{'report_time':{'order':'desc'}}
    }
    report_management_index_name = get_xnr_reportment_index_listname(twitter_report_management_index_name_pre,start_time,end_time)
    result=[]
    try:
        results=es_xnr.search(index=report_management_index_name,doc_type=twitter_report_management_index_type,body=query_body)['hits']['hits']
        for item in results:
            item['_source']['_id']=item['_id']    
            item['_source']['report_content']=json.loads(item['_source']['report_content'])
            result.append(item['_source'])
    except:
        result=[]
    return result


def output_excel_word(id_list,out_type,report_timelist):
    index_name_list = []
    for item in report_timelist:
        index_name = twitter_report_management_index_name_pre + ts2datetime(int(item))
        if index_name not in index_name_list:
            index_name_list.append(index_name)
        else:
            pass

    report_condition = Report(id_list,SCREEN_WEIBO_USERNAME,SCREEN_WEIBO_PASSWORD,index_name_list)
    if out_type == 'word':
        mark=report_condition.save_word()
    elif out_type == 'excel':
        mark=report_condition.save_excel()
    return mark
