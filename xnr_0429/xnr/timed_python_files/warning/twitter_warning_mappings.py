# -*-coding:utf-8-*-

import sys
import json
import time
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime,datetime2ts,ts2yeartime
from parameter import MAX_VALUE,DAY,WARMING_DAY
from global_config import S_TYPE,TWITTER_FLOW_START_DATE
from elasticsearch import Elasticsearch
from global_utils import es_xnr_2 as es,es_xnr
from global_utils import twitter_user_warning_index_name_pre,twitter_user_warning_index_type,\
						twitter_event_warning_index_name_pre,twitter_event_warning_index_type,\
						twitter_speech_warning_index_name_pre,twitter_speech_warning_index_type,\
						twitter_timing_warning_index_name_pre,twitter_timing_warning_index_type,\
						weibo_date_remind_index_name,weibo_date_remind_index_type,\
						twitter_warning_corpus_index_name,twitter_warning_corpus_index_type
						

NOW_DATE=ts2datetime(int(time.time())-DAY)

def twitter_user_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			twitter_user_warning_index_type:{
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
		twitter_user_warning_index_name=twitter_user_warning_index_name_pre + TWITTER_FLOW_START_DATE
	else:
		twitter_user_warning_index_name=twitter_user_warning_index_name_pre + NOW_DATE
	if not es.indices.exists(index=twitter_user_warning_index_name):
		es.indices.create(index=twitter_user_warning_index_name,body=index_info,ignore=400)


def twitter_event_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			twitter_event_warning_index_type:{
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
					'main_facebook_info':{ #典型微博信息
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
		twitter_event_warning_index_name = twitter_event_warning_index_name_pre + TWITTER_FLOW_START_DATE
	else:
		twitter_event_warning_index_name = twitter_event_warning_index_name_pre + NOW_DATE
	if not es.indices.exists(index=twitter_event_warning_index_name):
		es.indices.create(index=twitter_event_warning_index_name,body=index_info,ignore=400)


def twitter_speech_warning_mappings():
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
			twitter_speech_warning_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'content_type':{  # friends - 好友，unfriends - 非好友
						'type':'string',
						'index':'not_analyzed'
					},					
					'validity':{   #预警有效性，有效1，无效-1
						'type':'long'
					},
					'timestamp':{
						'type':'long'
					},
					'uid':{ 
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive':{
						'type':'long'
					},	
					'sentiment':{ 
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
					'fid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'keywords_string':{
						'type': 'string',
						'analyzer': 'my_analyzer'
					},
					'sensitive_words_dict':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'keywords_dict':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}
	if S_TYPE == 'test':
		twitter_speech_warning_index_name = twitter_speech_warning_index_name_pre + TWITTER_FLOW_START_DATE
	else:
		twitter_speech_warning_index_name = twitter_speech_warning_index_name_pre + NOW_DATE
	print twitter_speech_warning_index_name
	if not es.indices.exists(index=twitter_speech_warning_index_name):
		es.indices.create(index=twitter_speech_warning_index_name,body=index_info,ignore=400)
		print 'finish index'



def twitter_timing_warning_mappings(date_result):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			twitter_timing_warning_index_type:{
				'properties':{
					'submitter' : {
						'type': 'string', 
						'index':'not_analyzed'
					},
					'facebook_date_warming_content':{ #典型微博信息
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
		twitter_timing_warning_index_name = twitter_timing_warning_index_name_pre + date
		#print 'facebook_timing_warning_index_name:',facebook_timing_warning_index_name
		if not es.indices.exists(index=twitter_timing_warning_index_name):
			es.indices.create(index=twitter_timing_warning_index_name,body=index_info,ignore=400)
	


def lookup_date_info(today_datetime):
    query_body={
        'query':{
        	'match_all':{}
        },
        'size':MAX_VALUE,
        'sort':{'date_time':{'order':'asc'}}
    }
    try:
        result=es_xnr.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
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


def twitter__warning_corpus_mappings():
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
			twitter_warning_corpus_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'content_type':{  # friends - 好友，unfriends - 非好友
						'type':'string',
						'index':'not_analyzed'
					},
					'warning_source':{       #预警来源
						'type':'string',
						'index':'not_analyzed'
					},
					'create_time':{
						'type':'long'
					},				
					'validity':{   #预警有效性，有效1，无效-1
						'type':'long'
					},
					'timestamp':{
						'type':'long'
					},
					'uid':{ 
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive':{
						'type':'long'
					},	
					'sentiment':{ 
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
					'tid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'keywords_string':{
						'type': 'string',
						'analyzer': 'my_analyzer'
					},
					'sensitive_words_dict':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'keywords_dict':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'share':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'favorite':{
						'type':'long'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=twitter_warning_corpus_index_name):
		es.indices.create(index=twitter_warning_corpus_index_name,body=index_info,ignore=400)
		print 'finish corpus index'


if __name__ == '__main__':
	twitter_user_warning_mappings()
	twitter_event_warning_mappings()
	twitter_speech_warning_mappings()

	if S_TYPE == 'test':
		today_datetime=datetime2ts(TWITTER_FLOW_START_DATE)
	else:
		today_datetime=int(time.time()) - DAY
	date_result=lookup_date_info(today_datetime)
	#print 'date_result:',date_result
	twitter_timing_warning_mappings(date_result)
	twitter__warning_corpus_mappings()


