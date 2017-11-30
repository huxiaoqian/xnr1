# -*-coding:utf-8-*-

import sys
import json
import time
from time_utils import ts2datetime
from global_config import S_TYPE,S_DATE_BCI
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_user_warning_index_name_pre,weibo_user_warning_index_type,\
						weibo_event_warning_index_name_pre,weibo_event_warning_index_type,\
						weibo_speech_warning_index_name_pre,weibo_speech_warning_index_type

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
						'index':'not_analyzed'
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
						'index':'not_analyzed'
					},
					'event_time':{ #事件时间
						'type':'long'
					},
					'main_weibo_info':{ #典型微博信息
						'type':'string',
						'index':'not_analyzed'
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


def weibo_timing_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_timing_warning_index_type:{
				'properties':{
					'xnr_user_no':{  #虚拟人
						'type':'string',
						'index':'not_analyzed'
					},
					'date_name':{   #时间节点名称
						'type':'string',
						'index':'not_analyzed'
					},
					'main_user_info':{ #主要参与用户信息列表
						'type':'string',
						'index':'not_analyzed'
					},
					'event_time':{ #事件时间
						'type':'long'
					},
					'main_weibo_info':{ #典型微博信息
						'type':'string',
						'index':'not_analyzed'
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
		weibo_timing_warning_index_name = weibo_timing_warning_index_name_pre + S_DATE_BCI
	else:
		weibo_timing_warning_index_name = weibo_timing_warning_index_name_pre + NOW_DATE
	if not es.indices.exists(index=weibo_timing_warning_index_name):
		es.indices.create(index=weibo_timing_warning_index_name,body=index_info,ignore=400)



if __name__ == '__main__':
	#weibo_user_warning_mappings()
	#weibo_event_warning_mappings()
	#weibo_speech_warning_mappings()


