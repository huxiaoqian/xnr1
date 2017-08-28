#-*- coding: utf-8 -*-
'''
weibo_xnr warming function
'''
import os
import json
from xnr.global_utils import es_xnr,weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                             es_flow_text,flow_text_index_type,weibo_date_remind_index_name,weibo_date_remind_index_type,\
                             weibo_report_management_index_name,weibo_report_management_index_type,\
                             weibo_speech_warning_index_name,weibo_speech_warning_index_type
from xnr.time_utils import get_flow_text_index_list,ts2yeartime,ts2datetime,datetime2ts
from xnr.parameter import USER_NUM,MAX_SEARCH_SIZE,USER_CONTENT_NUM,DAY
###################################################################
###################       personal warming       ##################
###################################################################

#思路：获取虚拟人的关注列表用户，从流数据中查询计算这些用户的敏感度，返回敏感度前100的用户及该用户敏感度最高的3条微博内容
#show the personal wariming content
def show_personnal_warming(xnr_user_no,day_time):
	#查询关注列表
	es_xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
	followers_list=es_xnr_result['followers_list']
	followers_list=json.loads(followers_list)

	flow_text_index_list=get_flow_text_index_list(int(day_time))

    #计算敏感度排名靠前的用户
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'terms':{'uid':followers_list}
				}
			}
		},
		'aggs':{
			'followers_sensitive_num':{
				'terms':{'field':'uid'},
				'aggs':{
					'sensitive_num':{
						'sum':{'field':'sensitive'}
					}
				}						
			}
			},
		'size':MAX_SEARCH_SIZE
	}
	first_sum_result=es_flow_text.search(index=flow_text_index_list,doc_type=flow_text_index_type,\
		body=query_body)['aggregations']['followers_sensitive_num']['buckets']
	top_userlist=[]
	if USER_NUM < len(first_sum_result):
		temp_num=USER_NUM
	else:
		temp_num=len(first_sum_result)
	#print temp_num
	for i in xrange(0,temp_num):
		top_userlist.append(first_sum_result[i]['key'])

	#查询敏感用户的最敏感微博内容
	results=[]
	for user in top_userlist:
		#print user
		query_body={
			'query':{
				'filtered':{
					'filter':{
						'term':{'uid':user}
					}
				}
			},
			'size':USER_CONTENT_NUM,
			'sort':{'sensitive':{'order':'desc'}}
		}
		second_result=es_flow_text.search(index=flow_text_index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
		results.extend([user,second_result])
	return results



###################################################################
###################       speech warming       ##################
###################################################################

#show the speech wariming content
def show_speech_warming(xnr_user_no,show_type,day_time):
	flow_text_index_list=get_flow_text_index_list(int(day_time))
	#关注用户
	es_xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
	followers_list=es_xnr_result['followers_list']
	followers_list=json.loads(followers_list)

	if show_type == 0:
		show_condition_list=[{'bool':{'must_not':{'terms':{'uid':followers_list}}}}]
	else:
		show_condition_list=[{'bool':{'must':{'terms':{'uid':followers_list}}}}]

	query_body={
		'query':{
			'filtered':{
				'filter':show_condition_list
			}
		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'sensitive':{'order':'desc'}}
	}

	results=es_flow_text.search(index=flow_text_index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
	return results


#加入预警库
#speech_info=[content_type,uid,text,mid,timestamp,retweeted,comment,like,uid_list]
def addto_speech_warming(xnr_user_no,speech_info):
    speech_dict=dict()
    speech_dict['xnr_user_no']=xnr_user_no
    speech_dict['content_type']=speech_info[0]
    speech_dict['uid']=speech_info[1]
    speech_dict['text']=speech_info[2]
    speech_dict['mid']=speech_info[3]
    speech_dict['timestamp']=speech_info[4]
    speech_dict['retweeted']=speech_info[5]
    speech_dict['comment']=speech_info[6]
    speech_dict['like']=speech_info[7]

    uid_list=speech_info[8].encode('utf-8').split(',')
    speech_dict['uid_list']=uid_list
    speech_id=xnr_user_no+'_'+str(speech_info[4])

    try:
        es_xnr.index(index=weibo_speech_warning_index_name,doc_type=weibo_speech_warning_index_name,id=speech_id,body=speech_dict)
        mark=True
    except:
        mark=False
    return mark

###################################################################
###################         event warming        ##################
###################################################################

#show the event wariming content
def show_event_warming():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'timestamp':{'order':'desc'}}
	}
	result=True
	return result



###################################################################
###################         date  warming        ##################
###################################################################
def show_date_warming(today_time):
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'date_time':{'order':'asc'}}
	}
	result=es_xnr.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
	#取出预警时间进行处理
	date_warming_result=[]
	for item in result:
		countdown_days=dict()
		date_time=item['_source']['date_time']
		year=ts2yeartime(today_time)
		warming_date=year+'-'+date_time
		today_date=ts2datetime(today_time)
		countdown_num=(datetime2ts(warming_date)-datetime2ts(today_date))/DAY
		countdown_days['countdown_days']=countdown_num
		temp_list=[item['_source'],countdown_days]
		#date_warming_result.extend([item['_source'],countdown_days])
		date_warming_result.append(temp_list)
		
	return date_warming_result

###################################################################
###################       微博操作公共函数       ##################
###################################################################
#一键上报
#report_info=[report_type,report_time,xnr_user_no,event_name,uid]
###report_content=[user_list,weibo_list]
#人物行为预警上报report_content=[weibo_list]
#言论内容预警上报report_content=[weibo_dict]
#事件涌现预警上报report_content=[user_list,weibo_list]
#user_dict=[uid,nick_name,fansnum,friendsnum]
#weibo_dict=[mid,text,timestamp,retweeted,like,comment]
#user_list=[user_dict,user_dict,....]
#weibo_list=[weibo_dict,weibo_dict,....]
def report_warming_content(report_info,user_info,weibo_info):
    report_dict=dict()
    report_dict['report_type']=report_info[0]
    report_dict['report_time']=int(report_info[1])
    report_dict['xnr_user_no']=report_info[2]
    report_dict['event_name']=report_info[3]
    report_dict['uid']=report_info[4]
    report_id=report_info[2]+'_'+str(report_info[1])

    #对用户信息进行
    user_list=[]
    if user_info:
    	print 'aaaaaa'
        user_info_item=user_info.encode('utf-8').split('*')
        for user_item in user_info_item:
            user_detail=user_item.split(',')
            user_dict=dict()
            user_dict['uid']=user_detail[0]
            user_dict['nick_name']=user_detail[1]
            user_dict['fansnum']=user_detail[2]
            user_dict['friendsnum']=user_detail[3]
            user_list.append(user_dict)

    #对微博信息进行处理
    weibo_list=[]
    if weibo_info:
        print 'bbbbbb'
        print 'weibo_info:::',weibo_info
        weibo_info_item=weibo_info.split('*')
        print weibo_info_item
        for weibo_item in weibo_info_item:
            print 'weibo_item：：：',weibo_item
            weibo_detail=weibo_item.split(',')
            weibo_dict=dict()
            weibo_dict['mid']=weibo_detail[0]
            weibo_dict['text']=weibo_detail[1]
            weibo_dict['timestamp']=weibo_detail[2]
            weibo_dict['retweeted']=weibo_detail[3]
            weibo_dict['like']=weibo_detail[4]
            weibo_dict['comment']=weibo_detail[5]
            weibo_list.append(weibo_dict)

    report_content=dict()
    report_content['user_list']=user_list
    report_content['weibo_list']=weibo_list

    report_dict['report_content']=json.dumps(report_content)

    try:
        es_xnr.index(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,id=report_id,body=report_dict)
        mark=True
    except:
        mark=False
    return mark


#转发

#评论

#点赞

#事件涌现#主要参与用户-查看用户详情

#导出到excel
