# -*-coding:utf-8-*-

import os
import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es
from global_utils import fb_hot_keyword_task_index_name,fb_hot_keyword_task_index_type

def recommend_subopinion_keyword_task_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			fb_hot_keyword_task_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'task_id':{  ## 当前事件代表微博的mid
						'type':'string',
						'index':'not_analyzed'
					},
					'keywords_string':{  ##  string：keyword1&keyword2&keyword3..... 以 & 连接
						'type':'string',
						'index':'not_analyzed'
					},
					'submit_time':{
						'type':'long'
					},
					'submit_user':{
						'type':'string',
						'index':'not_analyzed'
					},
					'compute_status':{   # 计算状态  0-尚未计算，1-内容推荐计算完成 2-子观点分析计算完成  应该改到social_sensing_text这个表中的compute_status
						'type':'long'
					}
				}
			}
		}
	}


	if not es.indices.exists(index=fb_hot_keyword_task_index_name):
		es.indices.create(index=fb_hot_keyword_task_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	recommend_subopinion_keyword_task_mappings()

