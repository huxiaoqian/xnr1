# -*-coding:utf-8-*-
import os
import json
import time
from elasticsearch import Elasticsearch
import sys
sys.path.append('../')
from global_utils import es_xnr as es,fb_bci_index_name_pre,fb_bci_index_type,\
				tw_bci_index_name_pre,tw_bci_index_type
from time_utils import ts2datetime

def fb_bci_mappings(index_name):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			fb_bci_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'active':{
						'type':'short'
					},
					'propagate':{
						'type':'short'
					},
					'cover':{
						'type':'short'
					},
					'trust':{
						'type':'short'
					},
					'influence':{
						'type':'short'
					},
					'timestamp':{
						'type':'long'
					}
				}
			}
		}
	}

	#current_time = time.time()
	#current_date = ts2datetime(current_time)

	#index_name = fb_bci_index_name_pre + current_date

	if not es.indices.exists(index=index_name):
		es.indices.create(index=index_name,body=index_info,ignore=400)


def tw_bci_mappings(index_name):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			tw_bci_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'active':{
						'type':'short'
					},
					'propagate':{
						'type':'short'
					},
					'cover':{
						'type':'short'
					},
					'trust':{
						'type':'short'
					},
					'influence':{
						'type':'short'
					},
					'timestamp':{
						'type':'long'
					}
				}
			}
		}
	}

	#current_time = time.time()
	#current_date = ts2datetime(current_time)

	#index_name = tw_bci_index_name_pre + current_date

	if not es.indices.exists(index=index_name):
		es.indices.create(index=index_name,body=index_info,ignore=400)

if __name__ == '__main__':

	fb_bci_mappings(index_name)
	tw_bci_mappings(index_name)


