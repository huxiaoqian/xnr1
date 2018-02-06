# -*-coding:utf-8-*-

import os
import sys
import json

reload(sys)
sys.path.append('../../')

from global_utils import es_xnr as es
from global_utils import intel_opinion_results_index_name,intel_type_all, intel_type_follow, \
				intel_type_influence, intel_type_sensitive, \
				topic_river_index_name, topic_river_index_type, \
				timeline_index_name, timeline_index_type

def intel_opinion_results_mappings(index_type):

	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			index_type:{
				'properties':{
					'task_id':{
						'type':'string',
						'index':'not_analyzed'
					},
					'content':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}


def topic_river_results_mappings():

	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			topic_river_index_type:{
				'properties':{
					'task_id':{
						'type':'string',
						'index':'not_analyzed'
					},
					'content':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}



def timeline_results_mappings():

	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			timeline_index_type:{
				'properties':{
					'task_id':{
						'type':'string',
						'index':'not_analyzed'
					},
					'content':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}
