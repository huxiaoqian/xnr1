# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_xnr_index_name,weibo_xnr_index_type,weibo_xnr_count_index_name,weibo_xnr_count_index_type

def weibo_xnr_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_xnr_index_type:{
				'properties':{
					'user_no':{					#虚拟人编号，即用户ID
						'type':'string',
						'index':'not_analyzed'
					},
					'username':{				#昵称
						'type':'string',
						'index':'not_analyzed'
					},
					'password':{				#密码
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
					'political_tendency':{		 #政治倾向
						'type':'string',
						'index':'not_analyzed'
					},
					'psychological_characteristics':{  #心理特征
						'type':'string',
						'index':'not_analyzed'
					},
					'business_goal':{			#业务目标
						'type':'string',
						'index':'not_analyzed'
					},
					'weiboxnr_age':{			#年龄
						'type':'long'
					},
					'weiboxnr_sex':{			#性别
						'type':'string',
						'index':'not_analyzed'
					},
					'weiboxnr_location':{		#所在地
						'type':'string',
						'index':'not_analyzed'
					},
					'weiboxnr_career':{			#职业
						'type':'string',
						'index':'not_analyzed'
					},
					'weiboxnr_descript':{		#个人描述
						'type':'string',
						'index':'not_analyzed'
					},
					'active_time':{              #活跃时间 
						'type':'string',
						'index':'not_analyzed'
					},
					'day_post_sum':{			#日发帖量设置：从不，1-2，3-5……
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo_ID':{				#所绑定的微博账号
						'type':'string',
						'index':'not_analyzed'
					},					
					'xnrcreate_status':{		#虚拟人创建状态
						'type':'long'           #0表示创建未完成，1表示创建完成
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


def weibo_xnr_count_mappings():
	index_info={
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_xnr_count_index_type:{
				'properties':{
					'user_no':{					#虚拟人编号，即用户ID
						'type':'string',
						'index':'not_analyzed'
					},
					'fan_sum':{					 #粉丝数
						'type':'long'
					},
					'all_post_sum':{			 #历史发帖量
						'type':'long'				
					},
					'all_comment_sum':{			 #历史评论数
						'type':'long'					
					},
					'today_post_sum':{			#今日发帖量
						'type':'long'			
					},
					'fan_list':{				#粉丝列表
						'type':'string',
						'index':'not_analyzed'
					},
					'focus_list':{				#关注列表
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}
	exist_indice=es.indices.exists(index=weibo_xnr_count_index_name)
	if exist_indice:
		#delete
		es.indices.delete(index='weibo_xnr_count',timeout=100)
	#create
	es.indices.create(index=weibo_xnr_count_index_name,body=index_info,ignore=400)

if __name__=='__main__':
	weibo_xnr_mappings()
	weibo_xnr_count_mappings()