# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_xnr_assessment_index_name,weibo_xnr_assessment_index_type

def weibo_xnr_assessment_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_xnr_assessment_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'influence':{  # 影响力
						'type':'long'
					},
					'penetration':{  # 渗透力
						'type':'long'
					},
					'safe':{   # 安全性
						'type':'long'
					},
					'date':{  # 日期  2017-08-30
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

	if not es.indices.exists(index=weibo_xnr_assessment_index_name):
		es.indices.create(index=weibo_xnr_assessment_index_name,body=index_info,ignore=400)


if __name__ == '__main__':
	weibo_xnr_assessment_mappings()

