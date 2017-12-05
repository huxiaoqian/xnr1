# -*-coding:utf-8-*-

import sys
import json
import time
from time_utils import ts2datetime,ts2yeartime,datetime2ts
from parameter import WARMING_DAY,MAX_VALUE,DAY
from global_config import S_TYPE,S_DATE_BCI,S_DATE_WARMING
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_user_warning_index_name_pre,weibo_user_warning_index_type,\
						weibo_event_warning_index_name_pre,weibo_event_warning_index_type,\
						weibo_speech_warning_index_name_pre,weibo_speech_warning_index_type,\
						weibo_timing_warning_index_name_pre,weibo_timing_warning_index_type,\
						weibo_date_remind_index_name,weibo_date_remind_index_type

NOW_DATE=ts2datetime(int(time.time()))

def weibo_user_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_user_warning_index_type:{
				'properties':{
					'xnr_user_no':{  # 虚拟人  
						'type':'string',
						'index':'not_analyzed'
					},
					'user_name':{    #预警用户昵称
						'type':'string',
						'index':'not_analyzed'
					},
					'uid':{     #预警用户id
						'type':'string',
						'index':'not_analyzed'
					},
					'user_sensitive':{  #预警用户敏感度
						'type':'long'
					},
					'validity':{   #用户预警有效性，有效1，无效-1
						'type':'long'
					},
					'content':{     #敏感言论内容
						'type':'string',
						'index':'no'
					},
					'timestamp':{    #预警生成时间
						'type':'long'
					}
				}
			}
		}
	}
	if S_TYPE == 'test':
		weibo_user_warning_index_name=weibo_user_warning_index_name_pre + S_DATE_BCI
	else:
		weibo_user_warning_index_name=weibo_user_warning_index_name_pre + NOW_DATE
	if not es.indices.exists(index=weibo_user_warning_index_name):
		es.indices.create(index=weibo_user_warning_index_name,body=index_info,ignore=400)


def weibo_event_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_event_warning_index_type:{
				'properties':{
					'xnr_user_no':{  #虚拟人
						'type':'string',
						'index':'not_analyzed'
					},
					'event_name':{   #事件名称
						'type':'string',
						'index':'not_analyzed'
					},
					'main_user_info':{ #主要参与用户信息列表
						'type':'string',
						'index':'no'
					},
					'event_time':{ #事件时间
						'type':'long'
					},
					'main_weibo_info':{ #典型微博信息
						'type':'string',
						'index':'no'
					},
					'event_influence':{
						'type':'string',
						'index':'not_analyzed'
					},
					'validity':{   #预警有效性，有效1，无效-1
						'type':'long'
					},
					'timestamp':{
						'type':'long'
					}
				}
			}
		}
	}
	if S_TYPE == 'test':
		weibo_event_warning_index_name = weibo_event_warning_index_name_pre + S_DATE_BCI
	else:
		weibo_event_warning_index_name = weibo_event_warning_index_name_pre + NOW_DATE
	if not es.indices.exists(index=weibo_event_warning_index_name):
		es.indices.create(index=weibo_event_warning_index_name,body=index_info,ignore=400)


def weibo_speech_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5,
			'analysis':{
				'analyzer':{
					'my_analyzer':{
					'type': 'pattern',
					'pattern': '&'
						}
					}
				}
		},
		'mappings':{
			weibo_speech_warning_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'content_type':{  # unfollow - 未关注，follow - 已关注
						'type':'string',
						'index':'not_analyzed'
					},					
					'validity':{   #预警有效性，有效1，无效-1
						'type':'long'
					},
					'timestamp':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'directed_uid':{
						'type':'long'
					},
					'uid':{ 
						'type':'string',
						'index':'not_analyzed'
					},	
					'sentiment':{ 
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{ 
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_words_string':{
						'type': 'string',
						'analyzer': 'my_analyzer'
					},
					'text':{ 
						'type':'string',
						'index':'not_analyzed'
					},
					'user_fansnum':{
						'type':'long'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'keywords_string':{
						'type': 'string',
						'analyzer': 'my_analyzer'
					},
					'sensitive':{
						'type':'long'
					},
					'sensitive_words_dict':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'keywords_dict':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'ip':{  
						'type':'string',
						'index':'not_analyzed'
					},	
					'directed_uname':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'geo':{
						'type': 'string',
						'analyzer': 'my_analyzer'
					},
					'message_type':{
						'type':'long'
					},
					'retweeted':{
						'type':'long'
					},
					'root_mid':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}
	if S_TYPE == 'test':
		weibo_speech_warning_index_name = weibo_speech_warning_index_name_pre + S_DATE_BCI
	else:
		weibo_speech_warning_index_name = weibo_speech_warning_index_name_pre + NOW_DATE
	#print weibo_speech_warning_index_name
	if not es.indices.exists(index=weibo_speech_warning_index_name):
		es.indices.create(index=weibo_speech_warning_index_name,body=index_info,ignore=400)
		#print 'finish index'


def weibo_timing_warning_mappings(date_result):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_timing_warning_index_type:{
				'properties':{
					'submitter' : {
						'type': 'string', 
						'index':'not_analyzed'
					},
					'weibo_date_warming_content':{ #典型微博信息
						'type':'string',
						'index':'no'
					},
					'date_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'date_time':{
						'type':'string',
						'index':'not_analyzed'
					},
					'keywords':{
						'type':'string',
						'index':'not_analyzed'
					},
					'create_type':{  # all_xnrs - 所有虚拟人  my_xnrs -我管理的虚拟人
						'type':'string',  
						'index':'not_analyzed'
					},	
					'create_time':{
						'type':'long'
					},
					'content_recommend':{  # list: [text1,text2,text3,...]
						'type':'string',
						'index':'not_analyzed'
					},			
					'validity':{   #预警有效性，有效1，无效-1
						'type':'long'
					},
					'timestamp':{
						'type':'long'
					}
				}
			}
		}
	}
	for date in date_result:
		weibo_timing_warning_index_name = weibo_timing_warning_index_name_pre + date
		if not es.indices.exists(index=weibo_timing_warning_index_name):
			es.indices.create(index=weibo_timing_warning_index_name,body=index_info,ignore=400)
	
	# if S_TYPE == 'test':
	# 	weibo_timing_warning_index_name = weibo_timing_warning_index_name_pre + S_DATE_BCI
	# else:
	# 	weibo_timing_warning_index_name = weibo_timing_warning_index_name_pre + NOW_DATE
	# if not es.indices.exists(index=weibo_timing_warning_index_name):
	# 	es.indices.create(index=weibo_timing_warning_index_name,body=index_info,ignore=400)
		#print weibo_timing_warning_index_name



def lookup_date_info(today_datetime):
    query_body={
        'query':{
        	'match_all':{}
        },
        'size':MAX_VALUE,
        'sort':{'date_time':{'order':'asc'}}
    }
    try:
        result=es.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
        date_result=[]
        for item in result:
            #计算距离日期
            date_time=item['_source']['date_time']
            year=ts2yeartime(today_datetime)
            warming_date=year+'-'+date_time
            today_date=ts2datetime(today_datetime)
            countdown_num=(datetime2ts(warming_date)-datetime2ts(today_date))/DAY
            item['_source']['countdown_days']=countdown_num
            if abs(countdown_num) < WARMING_DAY:
                date_result.append(warming_date)
            else:
            	pass
    except:
        date_result=[]
    #print 'date_result',date_result
    return date_result



if __name__ == '__main__':	
	#weibo_user_warning_mappings()
	weibo_event_warning_mappings()
	#weibo_speech_warning_mappings()

	if S_TYPE == 'test':
		today_datetime=datetime2ts(S_DATE_WARMING)
	else:
		today_datetime=int(time.time())
	date_result=lookup_date_info(today_datetime)
	#weibo_timing_warning_mappings(date_result)



