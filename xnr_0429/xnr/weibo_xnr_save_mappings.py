#-*-coding:utf-8-*-
import os
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_xnr_save_like_index_name,weibo_xnr_save_like_index_type

def weibo_xnr_save_like_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_xnr_save_like_index_type:{
				'properties':{
					'uid':{         #操作虚拟人的uid
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{    #照片url
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{       #点赞对象昵称
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{               ## 设为空
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{       #微博发布时间
						'type':'long'
					},
					'text':{             ## 点赞内容
						'type':'string',
						'index':'not_analyzed'
					},
					'root_mid':{ #点赞微博的mid
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{     #点赞对象uid
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo_type':{   ## 点赞对象类型，follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'update_time':{      #点赞时间
						'type':'long'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_xnr_save_like_index_name):
		es.indices.create(index=weibo_xnr_save_like_index_name,body=index_info,ignore=400)

if __name__ == '__main__':
	weibo_xnr_save_like_mappings()
