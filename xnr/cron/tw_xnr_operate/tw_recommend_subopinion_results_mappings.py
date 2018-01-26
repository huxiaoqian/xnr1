# -*-coding:utf-8-*-
import os
import sys
import json

reload(sys)
sys.path.append('../../')

from global_utils import es_xnr as es
from global_utils import tw_hot_content_recommend_results_index_name,\
							tw_hot_content_recommend_results_index_type,\
							tw_hot_subopinion_results_index_name,tw_hot_subopinion_results_index_type


def content_recommend_results_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			tw_hot_content_recommend_results_index_type:{
				'properties':{
					'mid':{  ## 代表性微博的mid
						'type':'string',
						'index':'not_analyzed'
					},
					'xnr_user_no':{  ## 当前虚拟人
						'type':'string',
						'index':'not_analyzed'
					},
					'content_recommend':{
						'type':'string',
						'index':'no'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=tw_hot_content_recommend_results_index_name):
		es.indices.create(index=tw_hot_content_recommend_results_index_name,body=index_info,ignore=400)


def subopinion_results_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			tw_hot_subopinion_results_index_type:{
				'properties':{
					'mid':{  ## 代表性微博的mid
						'type':'string',
						'index':'not_analyzed'
					},
					'xnr_user_no':{  ## 当前虚拟人
						'type':'string',
						'index':'not_analyzed'
					},
					'subopinion_tw':{  ## 子话题对应的文本，{topic1:[text1,text2,...],topic2:[text1,text2,..],..}
						'type':'string',
						'index':'no'
					}
				}
			}
		}
	}

	#if not es.indices.exists(index=tw_hot_subopinion_results_index_name):
	es.indices.create(index=tw_hot_subopinion_results_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	content_recommend_results_mappings()
	subopinion_results_mappings()