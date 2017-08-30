#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
use to save function about database
'''
import os
import datetime
import json
from xnr.global_utils import es_xnr,weibo_xnr_index_name,weibo_xnr_index_type,\
                             weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                             es_user_profile,profile_index_name,profile_index_type,\
                             weibo_xnr_timing_list_index_name,weibo_xnr_timing_list_index_type,\
                             xnr_flow_text_index_name_pre,xnr_flow_text_index_type,\
                             weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
                             weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
                             weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
                             weibo_feedback_like_index_name,weibo_feedback_like_index_type
from xnr.parameter import MAX_VALUE,MAX_SEARCH_SIZE,DAY,FLOW_TEXT_START_DATE,REMIND_DAY
from xnr.data_utils import num2str
from xnr.time_utils import get_xnr_feedback_index_listname,ts2datetime,datetime2ts
from xnr.weibo_publish_func import retweet_tweet_func,comment_tweet_func,like_tweet_func,unfollow_tweet_func,follow_tweet_func
from xnr.weibo_xnr_warming.utils import show_date_warming
##########################################
#	step 2：show weibo_xnr 	information  #
##########################################
#step 2.1: show completed weibo_xnr information 
def show_completed_weiboxnr(now_time):
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'create_status':2}
				}
			}

		},
		'size':MAX_VALUE
	}
	results=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
	result=[]
	for item in results:
		xnr_list=item['_source']
		xnr_user_no=item['_source']['xnr_user_no']
		uid=item['_source']['uid']
		#粉丝数
		fans_num=count_fans_num(xnr_user_no)
		#历史发帖量
		history_post_num=count_history_post_num(xnr_user_no,now_time)
		#历史评论数
		history_comment_num=count_history_comment_num(uid)
		#今日发帖量
		today_comment_num=count_today_comment_num(xnr_user_no,now_time)
		xnr_list.extend(fans_num,history_post_num,history_comment_num,today_comment_num)
		result.append(xnr_list)
	return result


#计算粉丝数
def count_fans_num(xnr_user_no):
    result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
    followers_list=result['followers_list']
    number=len(followers_list)
    return number

#计算历史发帖量
def count_history_post_num(xnr_user_no,now_time):
    #获取检索列表
    weibo_xnr_flow_text_listname=get_xnr_feedback_index_listname(xnr_flow_text_index_name_pre,now_time)
    #定义检索规则
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_user_no':xnr_user_no}
                }
            }
        },
        'aggs':{
            'history_post_num':{
                'terms':{
                    'field':'xnr_user_no'
                }
            }
        }
    }
    try:
        results=es_xnr.search(index=weibo_xnr_flow_text_listname,doc_type=xnr_flow_text_index_type,\
            body=query_body)['aggregations']['history_post_num']['buckets']
        number=result[0]['doc_count']
    except:
        number=0
    return number

#计算今日发帖量
def count_today_comment_num(xnr_user_no,now_time):
    #对时间进行处理，确定查询范围
    date_time=ts2datetime(now_time)
    weibo_xnr_flow_text_listname=xnr_flow_text_index_name_pre+date_time
    star_time=datetime2ts(date_time)
    #定义检索规则
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'xnr_user_no':xnr_user_no},
                    'range':{
                        'timestamp':{
                            'gte':star_time,
                            'lte':now_time
                        }
                    }
                }
            }
        },
        'aggs':{
            'today_post_num':{
                'terms':{
                    'field':'xnr_user_no'
                }
            }
        }
    }
    try:
        results=es_xnr.search(index=weibo_xnr_flow_text_listname,doc_type=xnr_flow_text_index_type,\
            body=query_body)['aggregations']['today_post_num']['buckets']
        number=result[0]['doc_count']
    except:
        number=0
    return number

#计算历史评论数
def count_history_comment_num(uid):
    #定义检索规则
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'uid':uid}
                }
            }
        },
        'aggs':{
            'history_comment_num':{
                'terms':{
                    'field':'uid'
                }
            }
        }
    }
    try:
        result=es_xnr.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,\
    		body=query_body)['aggregations']['history_comment_num']['buckets']
        number=result[0]['doc_count']
    except:
    	number=0
    return number

#step 2.2: show uncompleted weibo_xnr information 
def show_uncompleted_weiboxnr():
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'range':{
						'create_status':{
						'gte':0,
						'lte':1
						}
					}
				}
			}

		},
		'size':MAX_VALUE
	}
	results=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
	result=[]
	for item in results:
		result.append(item['_source'])
	return result

#######################################
#	step 3：today remind (今日提醒)   #
#######################################
def xnr_today_remind(xnr_user_no,now_time):
	##发帖提醒
	#当前发帖量
    complete_num=count_today_comment_num(xnr_user_no,now_time)
    xnr_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    day_post_average_list=json.loads(xnr_result['day_post_average'])
    #最小目标发帖量
    min_post_num=min(int(day_post_average_list[0].encode('utf-8')),int(day_post_average_list[-1].encode('utf-8')))
    #目标发帖差额
    post_dvalue=min_post_num-complete_num

    if post_dvalue>0:
    	post_remind_content='尚未完成发帖目标，今日请至少再发'+str(post_dvalue)+'条帖子！'
    	post_remind_flag=1
    else:
    	post_remind_content=''
    	post_remind_flag=0
    post_remind=[post_remind_flag,post_remind_content]

    ##日历提醒
    date_remind_flag=0
    date_remind_content=[]
    date_result=show_date_warming(now_time)
    for date_item in date_result:
        if (date_item[-1]['countdown_days']>0) and (date_item[-1]['countdown_days']<REMIND_DAY):
            date_remind_flag=date_remind_flag+1
            date_remind_content_temp=str(date_item[-1]['countdown_days'])+'天后是'+date_item[0]['keywords'].encode('utf-8')+'，请注意！'
            date_remind_content.append(date_remind_content_temp)
    date_remind=[date_remind_flag,date_remind_content]

    #设置提醒内容
    remind_content=dict()
    #显示消息条数
    remind_num=post_remind_flag+date_remind_flag
    remind_content['remind_num']=remind_num
    #发帖提醒设置
    remind_content['post_remind_content']=post_remind_content
    #日期提醒设置：
    remind_content['date_remind_content']=date_remind_content
    return remind_content



#############################################
#	step 4：operate count (进入，操作统计)  #
#############################################
#step 4.1：history count


#step 4.2: timing task list
###########获取定时发送任务列表##############
def wxnr_timing_tasks(user_id):
	#获取虚拟人编号
	user_no_str=user_id[4:8]
	#print user_no_str
	user_no=long(user_no_str)
	#print user_no
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'user_no':user_no}
				}
			}

		},
		'size':MAX_VALUE,
		'sort':{'post_time':{'order':'desc'}} 	#按发送时间排序
	}
	result=es_xnr.search(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,body=query_body)['hits']['hits']
	return result

###########针对任务进行操作——查看##############
def wxnr_timing_tasks_lookup(task_id):
	result=es_xnr.get(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id)
	return result

###########针对任务进行操作——修改##############
def wxnr_timing_tasks_change(task_id,task_change_info):
	task_source=task_change_info[0]
	operate_type=task_change_info[1]
	create_time=task_change_info[2]
	post_time=task_change_info[3]
	text=task_change_info[4]
	remark=task_change_info[5]

	try:
		es_xnr.update(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id,\
			body={"doc":{'task_source':task_source,'operate_type':operate_type,'create_time':create_time,\
			'post_time':post_time,'text':text,'remark':remark}})
		result='change success!'
	except:
		result='change failed!'
	return result

###########针对任务进行操作——撤销##############
def wxnr_timing_tasks_revoked(task_id):
	#撤销操作即调整任务状态，将task_status状态设置为-1，只有未发送的任务可以撤销
	if task_status == 0:
		task_status=-1
		try:
			es_xnr.update(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id,\
				body={"doc":{'task_status':task_status}})
			result='revoked success!'
		except:
			result='revoked failed!'
	else:
		result='The task can not be revoked!'
	return result

#step 4.3: history information
#step 4.3.1:show history posting
def show_history_posting(require_detail):
	xnr_user_no=require_detail['xnr_user_no']	
	task_source=require_detail['task_source']
	es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	uid=es_result['uid']

	date_range_end_ts=datetime.datetime.now()
	weibo_xnr_flow_text_listname=get_xnr_feedback_index_listname(xnr_flow_text_index_name_pre,date_range_end_ts)

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'uid':uid},
					'term':{'task_source':task_source}
				}
			}
		},
		'sort':{timestamp:{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}

	try:
		results=es_xnr.search(index=weibo_xnr_flow_text_listname,doc_type=xnr_flow_text_index_type,body=query_body)['hits']['hits']
	except:
		results='There is no history posting!'
	return results

#step 4.3.2:show at content
def show_at_content(require_detail):
	xnr_user_no=require_detail['xnr_user_no']
	es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	uid=es_result['uid']

	#content_type='weibo'表示@我的微博，='at'表示@我的评论
	content_type=require_detail['content_type']

	if content_type=='weibo':
		index_name=weibo_feedback_retweet_index_name
		index_type=weibo_feedback_retweet_index_type
	elif content_type=='at':
		index_name=weibo_feedback_at_index_name
		index_type=weibo_feedback_at_index_type

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'uid':uid}
				}
			}
		},
		'sort':{timestamp:{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}
	try:
		results=es_xnr.search(index=index_name,doc_type=index_type,body=query_body)['hits']['hits']
	except:
		results='There is no history @ content!'
	return results


#step 4.3.3:show comment content
def show_comment_content(require_detail):
	xnr_user_no=require_detail['xnr_user_no']
	weibo_type=require_detail['weibo_type']
	es_result = es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	uid = es_result['uid']

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'uid':uid},
					'term':{'weibo_type':weibo_type}
				}
			}
		},
		'sort':{timestamp:{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}
	try:
		results=es_xnr.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,body=query_body)['hits']['hits']
	except:
		results='There is no history comment!'
	return results



#step 4.3.4:show like content
def show_like_content(xnr_user_no ):
	es_result = es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	uid = es_result['uid']

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'uid':uid}
					#'range':{'timestamp':{'gte':FLOW_TEXT_START_DATE,'lte':datetime.datetime.now()}}
				}
			}
		},
		'sort':{timestamp:{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}
	try:
		results=es_xnr.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,body=query_body)['hits']['hits']
	except:
		results='There is no history like!'
	return results


###########################################################################
#	step 4.3 & 4.4 & 4.5：微博相关操作，调用公共函数                      #
# (转发，评论，点赞，收藏，查看对话，回复，取消关注，直接关注，查看详情)  #  
###########################################################################

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

#收藏
#——暂无公共函数调用

#查看对话
####root_mid之间的数据关系可能存在问题
def show_comment_dialog(mid):
	es_result=es_xnr.get(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,id=mid)['_source']
	father_mid=es_result['root_mid']
	dialog_list=es_result

	while father_mid:
		try:
			dialog_result=es_xnr.get(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,id=father_mid)['_source']
			dialog_list.append(dialog_result)
			father_mid=dialog_result['root_mid']
		except:
			break
	return dialog_list

#回复
#——回复即调用评论函数

#取消关注
def cancel_follow_user(task_detail):
	xnr_user_no=task_detail['xnr_user_no']
	xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	account_name=xnr_es_result['weibo_mail_account']
	password=xnr_es_result['password']

	uid=task_detail['uid','']

	#调用取消关注函数
	mark=unfollow_tweet_func(account_name,password,uid)
	#if mark 修改关注列表
	#######################
	return mark

#直接关注
def attach_fans_follow(task_detail):
	xnr_user_no=task_detail['xnr_user_no']
	xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	account_name=xnr_es_result['weibo_mail_account']
	password=xnr_es_result['password']

	uid=task_detail['uid','']

	#调用关注函数
	mark=follow_tweet_func(account_name,password,uid)
	#if mark:
		#保存至关注列表
	#######################
	return mark

#查看详情
def lookup_detail_weibouser(uid):
	result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
	return result

#step 4.4: list of concerns
def wxnr_list_concerns(user_id,order_id):        
    if order_id==1:       #按影响力排序
        sort_condition_list=[{'infulence':{'order':'desc'}}]
    elif order_id==2:       #按敏感度排序
        sort_condition_list=[{'mingan':{'order':'desc'}}]
    else:					#默认设为按影响力排序
    	sort_condition_list=[{'infulence':{'order':'desc'}}]

	result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=user_id)
	followers_list=result['_source']['followers_list']
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'uid':followers_list}
				}
			}

		},
		'size':MAX_VALUE,
		'sort':sort_condition_list
	}
	concern_result=es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,body=query_body)['hits']['hits']
	return concern_result

#step 4.5: list of fans
def wxnr_list_fans(user_id,order_id):
    if order_id==1:       #按影响力排序
        sort_condition_list=[{'infulence':{'order':'desc'}}]
    elif order_id==2:       #按敏感度排序
        sort_condition_list=[{'mingan':{'order':'desc'}}]
    else:					#默认设为按影响力排序
        sort_condition_list=[{'infulence':{'order':'desc'}}]

	result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=user_id)
	fans_list=result['_source']['fans_list']
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'uid':fans_list}
				}
			}

		},
		'size':MAX_VALUE,
		'sort':sort_condition_list
	}
	fans_result=es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,body=query_body)['hits']['hits']
	return fans_result



#########################################################
#	step 5：change    and   continue                    #
#########################################################
def change_continue_xnrinfo(xnr_user_no):
	result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	return result


###############################
#	step 6：delete_weibo_xnr  #
###############################
def delete_weibo_xnr(xnr_user_no):
	try:
		es_xnr.delete(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)
		result=True
	except:
		result=False
	return result
