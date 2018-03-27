# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import xnr_map_index_name,xnr_map_index_type

def xnr_map_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			xnr_map_index_type:{
				'properties':{
					'main_user':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo_xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo_xnr_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'qq_xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'qq_xnr_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weixin_xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weixin_xnr_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_xnr_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'twitter_xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'twitter_xnr_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{ # 时间戳
						'type':'long'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=xnr_map_index_name):
		es.indices.create(index=xnr_map_index_name,body=index_info,ignore=400)


if __name__ == '__main__':
	xnr_map_mappings()

