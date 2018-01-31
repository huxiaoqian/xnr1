# -*- coding:utf-8 -*-

'''
weibo report management
'''
import sys
import json
import xlwt
import time
from xnr.global_utils import es_xnr,weibo_report_management_index_name_pre,weibo_report_management_index_name,weibo_report_management_index_type,\
							 weibo_xnr_index_name,weibo_xnr_index_type,weibo_xnr_fans_followers_index_name,\
                             weibo_xnr_fans_followers_index_type

from xnr.weibo_publish_func import retweet_tweet_func,comment_tweet_func,like_tweet_func                             
from xnr.parameter import MAX_SEARCH_SIZE
from xnr.time_utils import ts2datetime
from xnr.save_weibooperate_utils import save_xnr_like
from xnr.utils import add_operate2redis

#show report content default
def show_report_content():
    query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'report_time':{'order':'desc'}}
	}
    results=es_xnr.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,body=query_body)['hits']['hits']
    result=[]
    for item in results:
        item['_source']['_id']=item['_id']
        item['_source']['report_content']=json.loads(item['_source']['report_content'])
        result.append(item['_source'])
    return result

#show report content by report_type
def show_report_typecontent(report_type):
    print report_type
    query_body={
		'query':{
			'filtered':{
				'filter':{
					'bool':{
						'must':{
							'terms':{'report_type':report_type}
						}
					}					
				}
			}

		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'report_time':{'order':'desc'}}
	}
    if report_type:
        results=es_xnr.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,body=query_body)['hits']['hits']
        result=[]
        for item in results:
            item['_source']['_id']=item['_id']    
            item['_source']['report_content']=json.loads(item['_source']['report_content'])
            result.append(item['_source'])
    else:
        result=show_report_content()
    return result



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


def show_reportcontent_new(report_type,start_time,end_time):
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
    report_management_index_name = get_xnr_reportment_index_listname(weibo_report_management_index_name_pre,start_time,end_time)
    result=[]
    try:
        results=es_xnr.search(index=report_management_index_name,doc_type=weibo_report_management_index_type,body=query_body)['hits']['hits']
        for item in results:
            item['_source']['_id']=item['_id']    
            item['_source']['report_content']=json.loads(item['_source']['report_content'])
            result.append(item['_source'])
    except:
        result=[]
    return result


#pubic function:like ,retweet ,comment
#################微博操作##########
#转发微博
def get_weibohistory_retweet(task_detail):
    text=task_detail['text']
    r_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    print text,r_mid,xnr_user_no
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    print text,r_mid,xnr_user_no,account_name,password
    #调用转发微博函数
    mark=retweet_tweet_func(account_name,password,text,r_mid)
    
    # 保存微博，将转发微博保存至flow_text_表
    ###########################################
    return mark

#评论
def get_weibohistory_comment(task_detail):
    text=task_detail['text']
    r_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    #调用评论微博函数
    mark=comment_tweet_func(account_name,password,text,r_mid)
    
    # 保存评论，将评论内容保存至表
    ###########################################
    return mark

#赞
def get_weibohistory_like(task_detail):
    root_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    #print 'xnr_user_no',xnr_user_no
    if not xnr_user_no:
        mark =False
        save_mark=False
        #print mark,save_mark
        return mark,save_mark
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']
    root_uid=xnr_es_result['uid']

    xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
    if xnr_result['followers_list']:
        followers_list=xnr_result['followers_list']
    else:
        followers_list=[]

    if xnr_result['fans_list']:
        fans_list=xnr_result['fans_list']
    else:
        fans_list=[]

    #调用点赞函数
    mark=like_tweet_func(account_name,password,root_mid)

    #保存点赞信息至表
    uid=task_detail['uid']
    photo_url=task_detail['photo_url']
    nick_name=task_detail['nick_name']
    timestamp=task_detail['timestamp']
    text=task_detail['text']
    update_time=task_detail['update_time']
    mid=root_uid+'_'+root_mid

    if uid not in followers_list:
        if uid not in fans_list:
            weibo_type='stranger'
        else:
            weibo_type='fans'
    else:
        if uid not in fans_list:
            weibo_type='follow'
        else:
            weibo_type='friend'

    like_info=[uid,photo_url,nick_name,mid,timestamp,text,root_mid,root_uid,weibo_type,update_time]
    save_mark=save_xnr_like(like_info)

    return mark,save_mark






