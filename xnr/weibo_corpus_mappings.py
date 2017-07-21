#-*-coding:utf-8-*-
import os
import json

from global_utils import es_xnr as es
from global_utils import weibo_xnr_corpus_index_name,weibo_xnr_corpus_index_type

def weibo_xnr_corpus_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_xnr_corpus_index_type:{
				'properties':{
					'corpus_type':{  # 两类：主题语料，日常语料 
						'type':'string',
						'index':'not_analyzed'
					},
					'theme_daily_name':{  # 主题，如：旅游、美食、
						'type':'string',
						'index':'not_analyzed'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'retweeted':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'like':{  # 点赞数
						'type':'long'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_xnr_corpus_index_name):
		es.indices.create(index=weibo_xnr_corpus_index_name,body=index_info,ignore=400)

if __name__ == '__main__':

	weibo_xnr_corpus_mappings()