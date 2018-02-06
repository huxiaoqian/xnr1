# -*-coding:utf-8-*-

import sys
import json

from global_utils import es_xnr as es, writing_task_index_name, writing_task_index_type

def writing_task_mappings():

	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			writing_task_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'task_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'task_name_pinyin':{
						'type':'string',
						'index':'not_analyzed'
					},
					'event_keywords':{
						'type':'string',
						'index':'not_analyzed'
					},
					'opinion_keywords':{
						'type':'string',
						'index':'not_analyzed'
					},
					'opinion_type':{
						'type':'string',
						'index':'not_analyzed'
					},
					'create_time':{
						'type':'long'
					},
					'submitter':{
						'type':'string',
						'index':'not_analyzed'
					},
					'compute_status':{
						'type':'long'
					},
					'task_source':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=writing_task_index_name):
		es.indices.create(index=writing_task_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	writing_task_mappings()

