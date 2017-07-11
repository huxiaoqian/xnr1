# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_xnr_index_name,weibo_xnr_index_type

def weibo_xnr_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_xnr_index_type:{
				'properties':{
					'username':{
						'type':'string',
						'index':'not_analyzed'
					},
					'password':{
						'type':'string',
						'index':'not_analyzed'
					},
					''
				}
			}
		}
	}