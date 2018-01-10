#-*-coding:utf-8-*-
import os
import json
import time
from global_config import S_TYPE,S_DATE_BCI
from parameter import DAY
from time_utils import ts2datetime
from global_utils import es_xnr as es
from global_utils import weibo_community_target_user_index_name_pre,weibo_community_target_user_index_type

NOW_DATE=ts2datetime(int(time.time())-DAY)

def weibo_community_target_user_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_community_target_user_index_type:{
				'properties':{
					'uid':{                     # uid
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive':{
                    	'type':'long'
                    },
                    'influence':{
                    	'type':'long'
                    },
                    'keywords':{
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'community_id':{   #社区ID
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
					'timestamp':{
						'type':'long'
					}
				}
			}
		}
	}

	if S_TYPE == 'test':
		weibo_community_target_user_index_name=weibo_community_target_user_index_name_pre + S_DATE_BCI
	else:
		weibo_community_target_user_index_name=weibo_community_target_user_index_name_pre + NOW_DATE
	if not es.indices.exists(index=weibo_community_target_user_index_name):
		es.indices.create(index=weibo_community_target_user_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	weibo_community_target_user_mappings()