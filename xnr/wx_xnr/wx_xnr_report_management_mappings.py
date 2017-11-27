#-*-coding:utf-8-*-
import os
import json
from xnr.wx_xnr.global_utils import es_xnr,wx_report_management_index_name,wx_report_management_index_type

# 上报管理
def wx_report_management_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			wx_report_management_index_type:{
				'properties':{
					'report_type':{ # 二类：人物，言论
						'type':'string',
						'index':'not_analyzed'
					},
					'report_time':{  # 上报时间
						'type':'long'
					},
					'xnr_user_no':{  # WXXNR0001,WXXNR0002,...
						'type':'string',
						'index':'not_analyzed'
					},
					'xnr_puid':{  
						'type':'string',
						'index':'not_analyzed'
					},
					'report_content':{  #上报内容，存wx内容dict()
						'type':'string',
						'index':'no'
					},
					'speaker_id':{ #speaker puid
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es_xnr.indices.exists(index=wx_report_management_index_name):
		es_xnr.indices.create(index=wx_report_management_index_name,body=index_info,ignore=400)

if __name__ == '__main__':
	wx_report_management_mappings()
