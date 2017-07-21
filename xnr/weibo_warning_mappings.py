# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_user_warning_index_name,weibo_user_warning_index_type,\
						weibo_event_warning_index_name,weibo_event_warning_index_type,\
						weibo_speech_warning_index_name,weibo_speech_warning_index_type

def weibo_user_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_user_warning_index_type:{
				'properties':{
					'xnr_user_no':{  # 虚拟人  WXNR0001，WXNR0002,...
						'type':'string',
						'index':'not_analyzed'
					},
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'warning_rank':{
						'type':'long'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'retweeted':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'like':{  # 点赞数
						'type':'long'
					}
				}
			}
		}
	}

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
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'event_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'warning_rank':{
						'type':'long'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'retweeted':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'like':{  # 点赞数
						'type':'long'
					},
					'uid_list':{  # 参与用户
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_event_warning_index_name):
		es.indices.create(index=weibo_event_warning_index_name,body=index_info,ignore=400)


def weibo_speech_warning_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
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
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'retweeted':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'like':{  # 点赞数
						'type':'long'
					},
					'uid_list':{  # 参与用户
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_speech_warning_index_name):
		es.indices.create(index=weibo_speech_warning_index_name,body=index_info,ignore=400)

if __name__ == '__main__':
	weibo_user_warning_mappings()
	weibo_event_warning_mappings()
	weibo_speech_warning_mappings()


