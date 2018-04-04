#-*-coding:utf-8-*-
import os
import json
import time
import sys
sys.path.append('../../../')
from parameter import DAY
from time_utils import ts2datetime
from global_config import S_TYPE,S_DATE
from global_utils import es_xnr as es
from global_utils import weibo_trace_community_index_name_pre,weibo_trace_community_index_type

sys.path.append('../../../timed_python_files/community/')
from weibo_publicfunc import get_compelete_wbxnr

def weibo_trace_community_mappings(xnr_user_no):
     index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_trace_community_index_type:{
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
                    'num_warning':{ #人数预警标识,0-无预警，1-有预警
                         'type':'long'
                    },
                    'num_warning_descrp':{ #人物预警描述
                         'type':'string',
                         'index':'not_analyzed'
                    },
                    'num_warning_content':{ #人物预警内容 
                         'type':'string',
                         'index':'no'
                    },
                    'sensitive_warning':{ #敏感预警标识,0-无预警，1-有预警
                         'type':'long'
                    },
                    'sensitive_warning_descrp':{ #敏感预警描述
                         'type':'string',
                         'index':'not_analyzed'
                    },
                    'sensitive_warning_content':{ #敏感预警内容
                         'type':'string',
                         'index':'no'
                    },
                    'influence_warning':{ #影响力预警标识,0-无预警，1-有预警
                         'type':'long'
                    },
                    'influence_warning_descrp':{ #影响力预警描述
                         'type':'string',
                         'index':'not_analyzed'
                    },
                    'influence_warning_content':{ #影响力预警内容
                         'type':'string',
                         'index':'no'
                    },
                    'density_warning':{ #紧密度预警标识,0-无预警，1-有预警
                         'type':'long'
                    },
                    'density_warning_descrp':{ #紧密度预警描述
                         'type':'string',
                         'index':'not_analyzed'
                    },
                    'density_warning_content':{ #紧密度预警内容
                         'type':'string',
                         'index':'no'
                    },
                    'warning_rank':{ #预警等级
                         'type':'long'
                    },
                    'warning_type':{ #预警类型：人物突增预警；影响力剧增预警；敏感度剧增预警；社区聚集预警
                          'type':'string',
                          'index':'not_analyzed'
                    }                  
				}
			}
		}
     }


     weibo_trace_community_index_name=weibo_trace_community_index_name_pre + xnr_user_no.lower()
     if not es.indices.exists(index=weibo_trace_community_index_name):
          mark=es.indices.create(index=weibo_trace_community_index_name,body=index_info,ignore=400)
          # print 'finiesh !!'
          # print weibo_trace_community_index_name
          # print 'mark',mark


if __name__ == '__main__':
	if S_TYPE == 'test':
		xnr_user_no_list = ['WXNR0004']
	else:
		xnr_user_no_list = get_compelete_wbxnr()

	for xnr_user_no in xnr_user_no_list:
		weibo_trace_community_mappings(xnr_user_no)