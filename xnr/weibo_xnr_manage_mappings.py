# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_xnr_index_name,weibo_xnr_index_type

def weibo_xnr_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_xnr_index_type:{
				'properties':{
					'user_no':{					#虚拟人编号
						'type':'string',
						'index':'not_analyzed'
					},
					'username':{				#昵称
						'type':'string',
						'index':'not_analyzed'
					},
					'password':{
						'type':'string',
						'index':'not_analyzed'
					},
					'create_time':{              #创建时间
						'type':'string',
						'index':'not_analyzed'
					},
					'active_field':{			  #渗透领域
						'type':'string',
						'index':'not_analyzed'
					},
					'role_define':{				 #角色定位
						'type':'string',
						'index':'not_analyzed'
					},
					'active_time':{              #活跃时间 
						'type':'string',
						'index':'not_analyzed'
					},
					'fan_sum':{					 #粉丝数
						'type':'long',
						'index':'not_analyzed'
					},
					'all_post_sum':{			 #历史发帖量
						'type':'long',
						'index':'not_analyzed'					
					},
					'all_comment_sum':{			 #历史评论数
						'type':'long',
						'index':'not_analyzed'					
					},
					'today_post_sum':{			#今日发帖量
						'type':'long',
						'index':'not_analyzed'					
					},
					'today_remind':{			#今日提醒
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}
	exist_indice=es.indices.exists(index=weibo_xnr_index_name)
	if exist_indice:
		#delete
		es.indices.delete(index='weibo_xnr',timeout=100)
	#create
	es.indices.create(index=weibo_xnr_index_name,body=index_info,ignore=400)

if __name__=='__main__':
	weibo_xnr_mappings()