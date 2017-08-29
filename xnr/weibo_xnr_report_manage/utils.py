# -*- coding:utf-8 -*-

'''
weibo report management
'''
import sys
import json
import xlwt
import time
from xnr.global_utils import es_xnr,weibo_report_management_index_name,weibo_report_management_index_type,\
							 weibo_xnr_index_name,weibo_xnr_index_type,weibo_xnr_fans_followers_index_name,\
                             weibo_xnr_fans_followers_index_type

from xnr.weibo_publish_func import retweet_tweet_func,comment_tweet_func,like_tweet_func                             
from xnr.parameter import MAX_SEARCH_SIZE
from xnr.time_utils import ts2date
from xnr.save_weibooperate_utils import save_xnr_like

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
							'term':{'report_type':report_type}
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
            result.append(item['_source'])
    else:
        result=show_report_content()
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
    mid=root_uid+root_mid

    if uid not in followers_list:
        if uid not in fans_list:
            weibo_type='陌生人'
        else:
            weibo_type='粉丝'
    else:
        if uid not in fans_list:
            weibo_type='follow'
        else:
            weibo_type='好友'

    like_info=[uid,photo_url,nick_name,mid,timestamp,text,root_mid,root_uid,weibo_type,update_time]
    save_mark=save_xnr_like(like_info)

    return mark,save_mark

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




