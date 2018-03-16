# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import tw_xnr_timing_list_index_name,tw_xnr_timing_list_index_type

def tw_xnr_timing_list_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			tw_xnr_timing_list_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'task_source':{  # daily_post-日常发帖，hot_post-热点跟随，business_post-业务发帖
						'type':'string',
						'index':'not_analyzed'
					},
					'operate_type':{  # origin-原创，comment-评论，retweet-转发
						'type':'string',
						'index':'not_analyzed'
					},
					'create_time':{ # 提交时间
						'type':'long'
					},
					'post_time':{ # 发帖时间
						'type':'long'
					},
					'text':{  # 发帖内容
						'type':'string',
						'index':'not_analyzed'
					},
					'remark':{
						'type':'string',
						'index':'not_analyzed'
					},
					'task_status':{ # 0-尚未发送，1-已发送，-1 -撤销任务
						'type':'long'
					},
					'p_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'rank':{
						'type':'string',
						'index':'not_analyzed'
					},
					'rankid':{
						'type':'string',
						'index':'not_analyzed'
					}

				}
			}		
		}
	}

	if not es.indices.exists(index=tw_xnr_timing_list_index_name):
		es.indices.create(index=tw_xnr_timing_list_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	tw_xnr_timing_list_mappings()