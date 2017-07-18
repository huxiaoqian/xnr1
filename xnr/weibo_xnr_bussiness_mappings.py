# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_date_remind_index_name,weibo_date_remind_index_type,\
						weibo_sensitive_words_index_name,weibo_sensitive_words_index_type,\
						weibo_hidden_expression_index_name,weibo_hidden_expression_index_type

def weibo_date_remind_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_date_remind_index_type:{
				'properties':{
					'date_time':{
						'type':'string',
						'index':'not_analyzed'
					},
					'keywords':{
						'type':'string',
						'index':'not_analyzed'
					},
					'create_type':{  # all_xnrs - 所有虚拟人  my_xnrs -我管理的虚拟人
						'type':'string',  
						'index':'not_analyzed'
					},
					'create_time':{
						'type':'long'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_date_remind_index_name):
		es.indices.create(index=weibo_date_remind_index_name,body=index_info,ignore=400)

def weibo_sensitive_words_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_sensitive_words_index_type:{
				'properties':{
					'rank':{
						'type':'long'
					},
					'sensitive_words':{
						'type':'string',
						'index':'not_analyzed'
					},
					'create_type':{  # all_xnrs - 所有虚拟人  my_xnrs - 我管理的虚拟人
						'type':'string',  
						'index':'not_analyzed'
					},
					'create_time':{
						'type':'long'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_sensitive_words_index_name):
		es.indices.create(index=weibo_sensitive_words_index_name,body=index_info,ignore=400)


def weibo_hidden_expression_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_hidden_expression_index_type:{
				'properties':{
					'origin_word':{
						'type':'string',
						'index':'not_analyzed'
					},
					'evolution_words_string':{
						'type':'string',
						'index':'not_analyzed'
					},
					'create_type':{  # all_xnrs - 所有虚拟人  my_xnrs - 我管理的虚拟人
						'type':'string',  
						'index':'not_analyzed'
					},
					'create_time':{
						'type':'long'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_hidden_expression_index_name):
		es.indices.create(index=weibo_hidden_expression_index_name,body=index_info,ignore=400)




if __name__ == '__main__':

	weibo_date_remind_mappings()
	weibo_sensitive_words_mappings()
	weibo_hidden_expression_mappings()
