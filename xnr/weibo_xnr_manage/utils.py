#-*- coding: utf-8 -*-
'''
use to save function about database
'''
import os
from xnr.global_utils import es_xnr,weibo_xnr_index_name,weibo_xnr_index_type,\
                             weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                             es_user_profile,profile_index_name,profile_index_type,\
                             weibo_xnr_timing_list_index_name,weibo_xnr_timing_list_index_type
from xnr.parameter import MAX_VALUE
from xnr.data_utils import num2str

#################################
#	step 1：create a weibo_xnr 	#
#################################

#step 1.1: goal set
#create_weibo_xnr:create_wxnr_first
#wxnr_goal_info=[password,create_time,domain_name,role_name,psy_feature,political_side,business_goal,daily_interests,monitor_keywords]
def create_wxnr_first(wxnr_goal_info):
	#首先生成虚拟人ID
	#查询已经存在的虚拟人user_no，找到最大的编号值,然后在此基础上+1
	query_body={
		'_source':{
			'include':['user_no']
		},
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE
	}
	result=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
	user_no_list=[]
	for item in result:
		user_no_list.append(item['_source']['user_no'])
	max_no=max(user_no_list)
	user_no_num=max_no+1
	user_no_str=num2str(user_no_num)
	user_id='WXNR'+user_no_str

	#第一步创建虚拟人信息
	password=wxnr_goal_info[0]
	create_time=wxnr_goal_info[1]
	domain_name=wxnr_goal_info[2]
	role_name=wxnr_goal_info[3]
	psy_feature=wxnr_goal_info[4]
	political_side=wxnr_goal_info[5]
	business_goal=wxnr_goal_info[6]
	daily_interests=wxnr_goal_info[7]
	monitor_keywords=wxnr_goal_info[8]
	create_status=0

	try:
		es_xnr.index(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=user_id,\
			body={'user_no':user_no_num,'password':password,'create_time':create_time,'domain_name':domain_name,\
			'role_name':role_name,'psy_feature':psy_feature,'political_side':political_side,'business_goal':business_goal,\
			'daily_interests':daily_interests,'monitor_keywords':monitor_keywords,'create_status':create_status})
		result='First step has been completed'
	except:
		result='First step has not been completed'
	return result,user_id

#step 1.2: role create
#create_weibo_xnr:create_wxnr_second
#wxnr_role_info=[nick_name,age,sex,location,career,description,active_time,day_post_average]
def create_wxnr_second(user_id,wxnr_role_info):
	nick_name=wxnr_role_info[0]
	age=wxnr_role_info[1]
	sex=wxnr_role_info[2]
	location=wxnr_role_info[3]
	career=wxnr_role_info[4]
	description=wxnr_role_info[5]
	active_time=wxnr_role_info[6]
	day_post_average=wxnr_role_info[7]
	create_status=1

	try:
		es_xnr.update(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=user_id,\
			body={"doc":{'nick_name':nick_name,'age':age,'sex':sex,'location':location,'career':career,\
			'description':description,'active_time':active_time,'day_post_average':day_post_average,'create_status':create_status}})
		result='The second steps has been completed!'
	except:
		result='The second steps has not been completed!'
	return result

#step 1.3: attach to social account
#create_weibo_xnr:create_wxnr_third
#wxnr_account_info=[uid,weibo_mail_count,weibo_phone_count]
def create_wxnr_third(user_id,wxnr_account_info):
	uid=wxnr_account_info[0]
	weibo_mail_count=wxnr_account_info[1]
	weibo_phone_count=wxnr_account_info[2]
	create_status=2

	try:
		es_xnr.update(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=user_id,body={'doc':\
			{'uid':uid,'weibo_mail_count':weibo_mail_count,'weibo_phone_count':weibo_phone_count,'create_status':create_status}})
		result='The third steps has been completed!'
	except:
		result='The third steps has not been completed!'
	return result


##########################################
#	step 2：show weibo_xnr 	information  #
##########################################
#step 2.1: show completed weibo_xnr information 
def show_completed_weiboxnr():
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
	result=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
	return result


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
	result=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
	return result

#######################################
#	step 3：today remind (今日提醒)   #
#######################################



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
#	step 5：change                                      #
# (修改，直接调用创建虚拟人，第二步和第三步的函数即可)  #  
#########################################################



###############################
#	step 6：delete_weibo_xnr  #
###############################
def delete_weibo_xnr(user_id):
	try:
		es_xnr.delete(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=user_id)
		result='sucessful deleted'
	except:
		result='Not successful'
	return result

####################################
#  step 7：未完成虚拟人部分的继续  #
####################################
def continue_create_weiboxnr(user_id):
	result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=user_id)
	create_status=result['_source']['create_status']
	user_id=result['_id']	
	if create_status == 0 :
		status_result='continue with second step!'
	elif  create_status == 1 :
		status_result='continue with third step!'
	return status_result



##########test code ,can be delete##################
def create_wxnr_fans(user_id,fans_info):
	followers_list=fans_info
	print user_id,followers_list
	result=es_xnr.index(index='weibo_xnr_fans_followers',doc_type='uids',id=user_id,body={'followers_list':followers_list})
	#	result='Yes'
	#except:
	#	result='No'
	return result

def delete_wxnr_fans(user_id):
	try:
		es_xnr.delete(index='weibo_xnr_fans_followers',doc_type='uids',id=user_id)
		result='sucessful deleted'
	except:
		result='Not successful'
	return result