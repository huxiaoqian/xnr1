#-*-coding:utf-8-*-
import os
import json

from global_utils import es_xnr as es
from global_utils import qq_report_management_index_name,qq_report_management_index_type

# 上报管理
def qq_report_management_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			qq_report_management_index_type:{
				'properties':{
					'report_type':{ # 二类：人物，言论
						'type':'string',
						'index':'not_analyzed'
					},
					'report_time':{  # 上报时间
						'type':'long'
					},
					'xnr_user_no':{  # QXNR0001,QXNR0002,...
						'type':'string',
						'index':'not_analyzed'
					},
					'report_content':{  #上报内容，存qq内容dict()
						'type':'string',
						'index':'no'
					},
					'qq_number':{ #QQ号
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=qq_report_management_index_name):
		es.indices.create(index=qq_report_management_index_name,body=index_info,ignore=400)

if __name__ == '__main__':
	qq_report_management_mappings()
