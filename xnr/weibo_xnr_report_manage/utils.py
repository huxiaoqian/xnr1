# -*- coding:utf-8 -*-

'''
weibo report management
'''
import sys
import json
import xlwt
import time
from xnr.global_utils import es_xnr,weibo_report_management_index_name,weibo_report_management_index_type,\
							 weibo_xnr_index_name,weibo_xnr_index_type

from xnr.weibo_publish_func import retweet_tweet_func,comment_tweet_func,like_tweet_func                             
from xnr.parameter import MAX_SEARCH_SIZE
from xnr.time_utils import ts2date

#show report content default
def show_report_content():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'report_time':{'order':'desc'}}
	}
	result=es_xnr.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,body=query_body)['hits']['hits']
	return result

#show report content by report_type
def show_report_typecontent(report_type):
    query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'report_type':report_type}
				}
			}

		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'report_time':{'order':'desc'}}
	}
    if report_type:
        result=show_report_content()
    else:
        result=es_xnr.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,body=query_body)['hits']['hits']
    return result

#pubic function:like ,retweet ,comment
#################微博操作##########
#转发微博
def get_weibohistory_retweet(task_detail):
    text=task_detail['text']
    r_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

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
    r_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    #调用点赞函数
    mark=like_tweet_func(account_name,password,r_mid)

    #保存点赞信息至weibo_feedback_like表
    ###########################################
    return mark

#export into excel
#step 1: get the data ----获取数据，当前页面显示的数据
#step 2: write to excle file -----将数据按行列写入excel文件
#step 3: download the file ----下载文件
def get_data_toExcel(create_type):
    result=show_report_typecontent(create_type)
    return result

def export_data_toExcel(create_type):
    data_result=get_data_toExcel(create_type)

    #实例化一个workbook对象（即excel文件）
    wbk=xlwt.Workbook()    

    sheet=wbk.add_sheet('Sheet1',cell_overwrite_ok=True)
    #设置excel名
    get_time=int(time.time())
    time_name=ts2date(get_time)

    for i in xrange(len(result)):
        for j in xrange(len(result[i])):
            sheet.write(i,j,result[i][j])
    
    filename=str(time_name)+'xlsx'
    mark=wbk.save(filename)
    return mark 




