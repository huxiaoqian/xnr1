#-*-coding:utf-8-*-
import os
import json
import time
import sys
sys.path.append('../../')
from parameter import DAY
from time_utils import ts2datetime
from global_config import S_TYPE,FACEBOOK_COMMUNITY_DATE
from global_utils import es_xnr as es
from global_utils import facebook_community_target_user_index_name_pre,facebook_community_target_user_index_type,\
                         facebook_select_community_index_name_pre,facebook_select_community_index_type,\
                         facebook_detail_community_index_name_pre,facebook_detail_community_index_type

def facebook_community_target_user_mappings(date_name):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_community_target_user_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
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


	facebook_community_target_user_index_name=facebook_community_target_user_index_name_pre + date_name
	if not es.indices.exists(index=facebook_community_target_user_index_name):
		es.indices.create(index=facebook_community_target_user_index_name,body=index_info,ignore=400)


def facebook_select_community_mappings(date_name):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_select_community_index_type:{
				'properties':{
					'xnr_user_no':{                     # xnr_user_no
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'community_id':{                #社区编号
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'community_name':{           #社区名称
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'create_time':{            #创建时间
                    	'type':'long'
                    },
                    'num':{              #用户数量
                    	'type':'long'
                    },
                    'nodes':{              #用户uid信息
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'density':{       #社区紧密度
                    	'type':'long'
                    },
                    'cluster':{    #社区平均聚集系数
                    	'type':'long'
                    },
                    'max_influence':{ #社区最大影响力
                    	'type':'long'
                    },
                    'mean_influence':{ #社区平均影响力
                    	'type':'long'
                    },
                    'max_sensitive':{  #社区最大敏感度
                    	'type':'long'
                    },
                    'mean_sensitive':{  #社区平均敏感度
                    	'type':'long'
                    }
				}
			}
		}
	}


	facebook_select_community_index_name=facebook_select_community_index_name_pre + date_name
	if not es.indices.exists(index=facebook_select_community_index_name):
		es.indices.create(index=facebook_select_community_index_name,body=index_info,ignore=400)



def facebook_detail_community_mappings(date_name):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_detail_community_index_type:{
				'properties':{
					'xnr_user_no':{                     # xnr_user_no
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'community_id':{                #社区编号
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'community_name':{           #社区名称
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'create_time':{            #创建时间
                    	'type':'long'
                    },
                    'num':{              #用户数量
                    	'type':'long'
                    },
                    'nodes':{              #用户uid信息
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'density':{       #社区紧密度
                    	'type':'long'
                    },
                    'cluster':{    #社区平均聚集系数
                    	'type':'long'
                    },
                    'max_influence':{ #社区最大影响力
                    	'type':'long'
                    },
                    'mean_influence':{ #社区平均影响力
                    	'type':'long'
                    },
                    'max_sensitive':{  #社区最大敏感度
                    	'type':'long'
                    },
                    'mean_sensitive':{  #社区平均敏感度
                    	'type':'long'
                    },
                    ##############detail############
                    'community_status':{  #社区状态：0 新社区，1 跟踪社区，-1 放弃跟踪社区
                    	'type':'long'
                    },
                    'trace_remind':{   #跟踪提示，-2 强制跟踪，-1 放弃跟踪，0 忽略提示、系统处理，正数1、2、3、4表示未预警周期数
                    	'type':'long'
                    },
                    'origin_time':{  #初次创建时间
                    	'type':'long'
                    },
                    'core_user':{   #核心人物信息
                    	'type':'string',
                    	'index':'no'
                    },
                    'core_user_change':{ #核心人物变化信息dict形式{'add_user':[{},{}……],'delete_user':[{},{}……]}
                    	'type':'string',
                    	'index':'no'
                    }
                    'core_user_socail':{ #核心成员外部网络交换信息
                    	'type':'string',
                    	'index':'no'
                    },
                    'outer_user':{ #与核心人物互动频繁的外部人员信息
                    	'type':'string',
                    	'index':'no'
                    }
				}
			}
		}
	}


	facebook_detail_community_index_name=facebook_detail_community_index_name_pre + date_name
	if not es.indices.exists(index=facebook_detail_community_index_name):
		es.indices.create(index=facebook_detail_community_index_name,body=index_info,ignore=400)


if __name__ == '__main__':
	if S_TYPE == 'test':
		date_name = FACEBOOK_COMMUNITY_DATE
	else:
		now_time = int(time.time())
		date_name = ts2datetime(now_time)

	facebook_community_target_user_mappings(date_name)
	facebook_select_community_mappings(date_name)

	facebook_detail_community_mappings(date_name)