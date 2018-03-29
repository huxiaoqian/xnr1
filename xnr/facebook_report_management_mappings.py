#-*-coding:utf-8-*-
import os
import json
import time
from global_utils import es_xnr as es
from global_utils import facebook_report_management_index_name_pre,facebook_report_management_index_type,facebook_report_management_index_name
from time_utils import ts2datetime

# 上报管理
def facebook_report_management_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_report_management_index_type:{
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
					'event_name':{  #事件名称
						'type':'string',
						'index':'not_analyzed'
					},
					'report_content':{  #上报内容，存微博内容dict()
						'type':'string',
						'index':'no'
					},
					'uid':{ #人物id
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}
	now_time=int(time.time())
	facebook_report_management_index_name = facebook_report_management_index_name_pre + ts2datetime(now_time)
	if not es.indices.exists(index=facebook_report_management_index_name):
		es.indices.create(index=facebook_report_management_index_name,body=index_info,ignore=400)

if __name__ == '__main__':
	facebook_report_management_mappings()