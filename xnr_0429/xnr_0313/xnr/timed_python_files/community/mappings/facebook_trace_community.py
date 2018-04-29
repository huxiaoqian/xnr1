#-*-coding:utf-8-*-
import os
import json
import time
import sys
sys.path.append('../../')
from parameter import DAY
from time_utils import ts2datetime
from global_config import S_TYPE
from global_utils import es_xnr as es
from global_utils import facebook_trace_community_index_name_pre,facebook_trace_community_index_type
from timed_python_files.community.facebook_publicfunc import get_compelete_fbxnr

def facebook_trace_community_mappings(xnr_user_no):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_trace_community_index_type:{
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
                    'trace_time':{            #跟踪时间
                    	'type':'long'
                    },
                    'trace_date':{            #跟踪日期
                    	'type':'string',
                    	'index':'not_analyzed'
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
                    'min_influence':{ #社区最小影响力
                    	'type':'long'
                    },
                    'min_sensitive':{  #社区最小敏感度
                    	'type':'long'
                    }
				}
			}
		}
	}


	facebook_trace_community_index_name=facebook_trace_community_index_name_pre + xnr_user_no
	if not es.indices.exists(index=facebook_trace_community_index_name):
		es.indices.create(index=facebook_trace_community_index_name,body=index_info,ignore=400)


if __name__ == '__main__':
	if S_TYPE == 'test':
		xnr_user_no_list = ['FXNR0001']
	else:
		xnr_user_no_list = get_compelete_fbxnr()

	for xnr_user_no in xnr_user_no_list:
		facebook_trace_community_mappings(xnr_user_no)