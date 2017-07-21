#-*-coding:utf-8-*-
import os
import json

from global_utils import es_xnr as es
from global_utils import weibo_report_management_index_name,weibo_report_management_index_type

# 上报管理
def weibo_report_management_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_report_management_index_type:{
				'properties':{
					'report_type':{ # 三类：事件，人物，言论
						'type':'string',
						'index':'not_analyzed'
					},
					'report_time':{  # 上报时间
						'type':'long'
					},
					'xnr_user_no':{  # WXNR0001,WXNR0002,...
						'type':'string',
						'index':'not_analyzed'
					},
					'event_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'uid':{
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

	if not es.indices.exists(index=weibo_report_management_index_name):
		es.indices.create(index=weibo_report_management_index_name,body=weibo_report_management_index_type,ignore=400)

if __name__ == '__main__':
	weibo_report_management_mappings()
