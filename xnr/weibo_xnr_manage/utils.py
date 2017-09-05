#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
use to save function about database
'''
import os
import time
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
                             weibo_feedback_like_index_name,weibo_feedback_like_index_type,\
                             weibo_xnr_save_like_index_name,weibo_xnr_save_like_index_type,\
                             portrait_index_name,portrait_index_type,weibo_bci_index_name_pre,weibo_bci_index_type,\
                             weibo_xnr_assessment_index_name,weibo_xnr_assessment_index_type
from xnr.parameter import MAX_VALUE,MAX_SEARCH_SIZE,DAY,FLOW_TEXT_START_DATE,REMIND_DAY
from xnr.data_utils import num2str
from xnr.time_utils import get_xnr_feedback_index_listname,ts2datetime,datetime2ts,ts2datetimestr
from xnr.weibo_publish_func import retweet_tweet_func,comment_tweet_func,like_tweet_func,unfollow_tweet_func,follow_tweet_func
from xnr.weibo_xnr_warming.utils import show_date_warming
from xnr.save_weibooperate_utils import save_xnr_like,delete_xnr_followers

##########################################
#	step 2：show weibo_xnr 	information  #
##########################################
#step 2.1: show completed weibo_xnr information 
def show_completed_weiboxnr(account_no,now_time):
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
		xnr_list['fans_num']=fans_num
		xnr_list['history_post_num']=history_post_num
		xnr_list['history_comment_num']=history_comment_num
		xnr_list['today_comment_num']=today_comment_num
		#xnr_list.extend(fans_num,history_post_num,history_comment_num,today_comment_num)
		#今日提醒
		today_remind=xnr_today_remind(xnr_user_no,now_time)
		today_remind_num=today_remind['remind_num']
		xnr_list['today_remind_num']=today_remind_num
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
def show_uncompleted_weiboxnr(account_no):
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
def wxnr_history_count(xnr_user_no):
	now_time=int(time.time())
	weibo_xnr_flow_text_listname=get_xnr_feedback_index_listname(xnr_flow_text_index_name_pre,now_time)
	
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
	xnr_user_info=[]
	for index_name in weibo_xnr_flow_text_listname:
		xnr_user_detail=dict()
		#时间
		xnr_user_detail['date_time']=index_name[-10:]
		try:			
			xnr_result=es_xnr.search(index=index_name,doc_type=xnr_flow_text_index_type,body=query_body)
			#今日总粉丝数
			for item in xnr_result['hits']['hits']:
				xnr_user_detail['user_fansnum']=item['_source']['user_fansnum']
			#日常发帖、业务发帖、热点跟随
			for item in xnr_result['aggregations']['all_task_source']['buckets']:
				if item['key'] == '日常发帖':
					xnr_user_detail['daily_post_num']=item['doc_count']
				elif item['key'] == '业务发帖':
					xnr_user_detail['business_post_num']=item['doc_count']
				elif item['key'] == '热点跟随':
					xnr_user_detail['hot_follower_num']=item['doc_count']
			#总发帖量
			xnr_user_detail['total_post_sum']=xnr_user_detail['daily_post_num']+xnr_user_detail['business_post_num']+xnr_user_detail['hot_follower_num']

			#查找影响力、渗透力、安全性
			xnr_assess_id=xnr_user_no+xnr_user_detail['date_time']
			xnr_assess_result=es_xnr.get(index=weibo_xnr_assessment_index_name,doc_type=weibo_xnr_assessment_index_type,id=xnr_assess_id)['_source']
			xnr_user_detail['influence']=xnr_assess_result['influence']
			xnr_user_detail['penetration']=xnr_assess_result['penetration']
			xnr_user_detail['safe']=xnr_assess_result['safe']
		except:
			xnr_user_info=[]
		xnr_user_info.append(xnr_user_detail)
	
	#对xnr_user_info进行排序
	xnr_user_info.sort(key=lambda k:(k.get('date_time',0)),reverse=True)
	
	#累计统计
	Cumulative_statistics_dict=dict()
	try:		
		Cumulative_statistics_dict['date_time']='累计统计'
		Cumulative_statistics_dict['user_fansnum']=xnr_user_info[0]['user_fansnum']
		total_post_sum=0
		daily_post_num=0
		business_post_num=0
		influence_sum=0
		penetration_sum=0
		safe_sum=0
		number=len(xnr_user_info)
		for item in xnr_user_info:
			total_post_sum=total_post_sum+item['total_post_sum']
			daily_post_num=daily_post_num+item['daily_post_num']
			business_post_num=business_post_num+item['business_post_num']
			hot_follower_num=hot_follower_num+item['hot_follower_num']
			influence_sum=influence_sum+item['influence']
			penetration_sum=penetration_sum+item['penetration']
			safe_sum=safe_sum+item['safe']

		Cumulative_statistics_dict['total_post_sum']=total_post_sum
		Cumulative_statistics_dict['daily_post_num']=daily_post_num
		Cumulative_statistics_dict['business_post_num']=business_post_num
		Cumulative_statistics_dict['hot_follower_num']=hot_follower_num
		Cumulative_statistics_dict['influence']=influence_sum/number
		Cumulative_statistics_dict['penetration']=penetration_sum/number
		Cumulative_statistics_dict['safe']=safe_sum/number
	except:
		Cumulative_statistics_dict=dict()
	return Cumulative_statistics_dict,xnr_user_info

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
	results=es_xnr.search(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,body=query_body)['hits']['hits']
	result=[]
	for item in results:
		item['_source']['id']=item['_id']
		result.append(item['_source'])
	return result

###########针对任务进行操作——查看##############
def wxnr_timing_tasks_lookup(task_id):
	result=es_xnr.get(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id)['_source']
	return result

###########针对任务进行操作——修改##############
def wxnr_timing_tasks_change(task_id,task_change_info):
	task_source=task_change_info[0]
	operate_type=task_change_info[1]
	create_time=task_change_info[2]
	post_time=int(task_change_info[3])
	text=task_change_info[4]
	remark=task_change_info[5]

	try:
		es_xnr.update(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id,\
			body={"doc":{'task_source':task_source,'operate_type':operate_type,'create_time':create_time,\
			'post_time':post_time,'text':text,'remark':remark}})
		result=True
	except:
		result=False
	return result

###########针对任务进行操作——撤销##############
def wxnr_timing_tasks_revoked(task_id):
	task_result=es_xnr.get(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id)['_source']
	task_status=task_result['task_status']
	#撤销操作即调整任务状态，将task_status状态设置为-1，只有未发送的任务可以撤销
	
	if task_status == 0:
		task_status = -1
		try:
			es_xnr.update(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,id=task_id,\
				body={"doc":{'task_status':task_status}})
			result=True
		except:
			result=False
	else:
		result=False

	return result

#step 4.3: history information
#step 4.3.1:show history posting
def show_history_posting(require_detail):
	xnr_user_no=require_detail['xnr_user_no']	
	task_source=require_detail['task_source']
	es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	uid=es_result['uid']

	date_range_end_ts=require_detail['now_time']
	weibo_xnr_flow_text_listname=get_xnr_feedback_index_listname(xnr_flow_text_index_name_pre,date_range_end_ts)

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'bool':{
						'must':[
							{'term':{'uid':uid}},
							{'terms':{'task_source':task_source}}
						]
					}					
				}
			}
		},
		'sort':{'timestamp':{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}

	try:
		result=es_xnr.search(index=weibo_xnr_flow_text_listname,doc_type=xnr_flow_text_index_type,body=query_body)['hits']['hits']
		results=[]
		for item in result:
			results.append(item['_source'])
	except:
		results=[]
	return results

#step 4.3.2:show at content
def show_at_content(require_detail):
	xnr_user_no=require_detail['xnr_user_no']
	es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	uid=es_result['uid']

	#content_type='weibo'表示@我的微博，='at'表示@我的评论
	content_type=require_detail['content_type']

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'uid':uid}
				}
			}
		},
		'sort':{'timestamp':{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}


	index_name_list=[]
	index_type_list=[]
	for i in xrange(0,len(content_type)):
		if content_type[i]=='weibo':
			index_name_list.append(weibo_feedback_retweet_index_name)
			index_type_list.append(weibo_feedback_retweet_index_type)
		elif content_type[i]=='at':
			index_name_list.append(weibo_feedback_at_index_name)
			index_type_list.append(weibo_feedback_at_index_type)

	results=[]
	for j in xrange(0,len(index_name_list)):
		try:
			r_result=es_xnr.search(index=index_name_list[j],doc_type=index_type_list[j],body=query_body)['hits']['hits']
			result=[]
			for item in r_result:
				result.append(item['_source'])
		except:
			result=[]
		results.append(result)
	return results


#step 4.3.3:show comment content
def show_comment_content(require_detail):
	xnr_user_no=require_detail['xnr_user_no']
	comment_type=require_detail['comment_type']
	es_result = es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
	uid = es_result['uid']

	query_body={
		'query':{
			'filtered':{
				'filter':{
					'bool':{
						'must':[
							{'term':{'uid':uid}},
							{'terms':{'comment_type':comment_type}}
						]
					}
				}
			}
		},
		'sort':{'timestamp':{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}
	try:
		result=es_xnr.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,body=query_body)['hits']['hits']
		results=[]
		for item in result:
			results.append(item['_source'])
	except:
		results=[]
	return results



#step 4.3.4:show like content
def show_like_content(require_detail):
    xnr_user_no=require_detail['xnr_user_no']
    es_result = es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    uid = es_result['uid']
    like_type=require_detail['like_type']

    condition_list=[]
    query_body={
        'query':{
            'filtered':{
                'filter':condition_list
            }
        },
        'sort':{'timestamp':{'order':'desc'}},
        'size':MAX_SEARCH_SIZE
    }
    results=[]
    for i in xrange(0,len(like_type)):
        if like_type[i] == 'receive':
            condition_list=[]
            condition_list.append({'term':{'uid':uid}})
            result=es_xnr.search(index=weibo_feedback_like_index_name,doc_type=weibo_feedback_like_index_type,body=query_body)['hits']['hits']
        elif like_type[i] == 'send':
            condition_list=[]
            condition_list.append({'term':{'root_uid':uid}})
            result=es_xnr.search(index=weibo_xnr_save_like_index_name,doc_type=weibo_xnr_save_like_index_type,body=query_body)['hits']['hits']
        result_temp=[]
        for item in result:
            result_temp.append(item['_source'])
        results.append(result_temp)
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

#收藏
#——暂无公共函数调用

#查看对话
####root_mid之间的数据关系可能存在问题
def show_comment_dialog(mid):
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'bool':{
						'must':[
							{'term':{'root_mid':mid}}
						]
					}
				}
			}
		},
		'sort':{'timestamp':{'order':'desc'}},
		'size':MAX_SEARCH_SIZE
	}
	es_result=es_xnr.search(index=weibo_feedback_comment_index_name,doc_type=weibo_feedback_comment_index_type,body=query_body)['hits']['hits']
	results=[]
	for item in es_result:
		results.append(item['_source'])
	return results



#回复
#——回复即调用评论函数

#取消关注
def cancel_follow_user(task_detail):
    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    follower_uid=task_detail['uid']

    #调用取消关注函数
    mark=unfollow_tweet_func(account_name,password,follower_uid)
    #修改关注列表
    if mark:
        save_mark=delete_xnr_followers(xnr_user_no,follower_uid)
    else:
        save_mark=False
    return mark,save_mark

#直接关注
def attach_fans_follow(task_detail):
    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    follower_uid=task_detail['uid']

    #调用关注函数
    mark=follow_tweet_func(account_name,password,follower_uid)
    #保存至关注列表
    if mark:
        save_mark=save_xnr_followers(xnr_user_no,follower_uid)
    else:
        save_mark=False

    return mark,save_mark

#查看详情
def lookup_detail_weibouser(uid):
	result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
	return result

#step 4.4: list of concerns
def wxnr_list_concerns(user_id,order_type):        
	result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=user_id)
	followers_list=result['_source']['followers_list']
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'terms':{'uid':followers_list}
				}
			}

		},
		'size':MAX_SEARCH_SIZE
	}
	concern_result=es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,body=query_body)['hits']['hits']

	user_result=[]
	for item in concern_result:
		uid=item['_source']['uid']
		try:
			temp_user_result=es_user_profile.get(index=portrait_index_name,doc_type=portrait_index_type,id=uid)['_source']
			item['_source']['topic_string']=temp_user_result['topic_string']
			item['_source']['sensitive']=temp_user_result['sensitive']
		except:
			item['_source']['topic_string']=''
			item['_source']['sensitive']=0
		#计算影响力
		item['_source']['influence']=count_weibouser_influence(uid)
		#组合结果
		user_result.append(item['_source'])

	#对结果按要求排序
	user_result.sort(key=lambda k:(k.get(order_type,0)),reverse=True)
	return user_result

#计算影响力
def count_weibouser_influence(uid):
    now_time=int(time.time())
    date_time=ts2datetimestr(now_time-DAY)
    index_name=weibo_bci_index_name_pre+date_time
    
    query_body={
        'query':{
            'match_all':{}
        },
        'size':1,
        'sort':{'user_index':{'order':'desc'}}
    }
    try:
        max_result=es_user_profile.search(index=index_name,doc_type=weibo_bci_index_type,body=query_body)['hits']['hits']
        for item in max_result:
           max_user_index=item['_source']['user_index']

        user_result=es_user_profile.get(index=index_name,doc_type=weibo_bci_index_type,id=uid)['_source']
        user_index=user_result['user_index']
        infulence_value=user_index/max_user_index*100
    except:
        infulence_value=0
    return infulence_value


#step 4.5: list of fans
def wxnr_list_fans(user_id,order_type):
	result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=user_id)
	fans_list=result['_source']['fans_list']
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'terms':{'uid':fans_list}
				}
			}

		},
		'size':MAX_SEARCH_SIZE
	}
	fans_result=es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,body=query_body)['hits']['hits']
	user_result=[]
	for item in fans_result:
		uid=item['_source']['uid']
		try:
			temp_user_result=es_user_profile.get(index=portrait_index_name,doc_type=portrait_index_type,id=uid)['_source']
			item['_source']['sensitive']=temp_user_result['sensitive']
		except:
			item['_source']['sensitive']=0
		#计算影响力
		item['_source']['influence']=count_weibouser_influence(uid)
		#组合结果
		user_result.append(item['_source'])
	#对结果按要求排序
	user_result.sort(key=lambda k:(k.get(order_type,0)),reverse=True)
	return user_result



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
