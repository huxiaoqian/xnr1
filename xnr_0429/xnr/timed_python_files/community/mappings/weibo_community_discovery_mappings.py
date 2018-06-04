#-*-coding:utf-8-*-
import os
import json
import time
import sys
sys.path.append('../../../')
from parameter import DAY
from time_utils import ts2datetime
from global_config import S_TYPE,S_DATE,WEIBO_COMMUNITY_DATE
from global_utils import es_xnr as es
from global_utils import weibo_community_index_name_pre,weibo_community_index_type


def weibo_community_mappings(date_name):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_community_index_type:{
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
                    'create_time':{            #初次创建时间
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
                    ##
                    # 'min_influence':{ #社区最小影响力
                    # 	'type':'long'
                    # },
                    # 'min_sensitive':{  #社区最小敏感度
                    # 	'type':'long'
                    # },
                    ##############detail############
                    'community_status':{  #社区状态：0 新社区，1 跟踪社区，-1 放弃跟踪社区，-2 强制跟踪
                    	'type':'long'
                    },
                    'warning_remind':{   #预警提示，0 忽略提示、系统处理，正数1、2、3、4表示未预警周期数
                    	'type':'long'
                    },
                    'update_time':{  #更新时间
                    	'type':'long'
                    },
                    'core_user':{   #核心人物信息
                    	'type':'string',
                    	'index':'no'
                    },
                    'core_user_change':{ #核心人物变化信息dict形式{'add_user':[{},{}……],'delete_user':[{},{}……]}
                    	'type':'string',
                    	'index':'no'
                    },
                    'core_user_socail':{ #核心成员内部网络交换信息
                    	'type':'string',
                    	'index':'no'
                    },
                    'core_outer_socail':{  #核心成员外部交换信息
                         'type':'string',
                         'index':'no'
                    },
                    'outer_user':{ #与核心人物互动频繁的外部人员信息
                    	'type':'string',
                    	'index':'no'
                    },
                    'community_user_list':{ #社区成员列表信息,需标记核心成员
                    	'type':'string',
                    	'index':'no'
                    },
                    'community_user_change':{ #社区成员变化信息，形式参考核心人物
                    	'type':'string',
                    	'index':'no'
                    },
                    'warning_rank':{   #预警级别
                    	'type':'long'
                    },
                    'total_score':{   #综合得分
                    	'type':'long'
                    },
                    'socail_keyword':{  #社区初始关键词
                    	'type':'string',
                    	'index':'not_analyzed'
                    },
                    'warning_type':{ #预警类型：人物突增预警；影响力剧增预警；敏感度剧增预警；社区聚集预警
                          'type':'string',
                          'index':'not_analyzed'
                    }

				}
			}
		}
	}


	weibo_community_index_name = weibo_community_index_name_pre + date_name
	if not es.indices.exists(index=weibo_community_index_name):
		es.indices.create(index=weibo_community_index_name,body=index_info,ignore=400)


if __name__ == '__main__':
     if S_TYPE == 'test':
          date_name = WEIBO_COMMUNITY_DATE
     else:
          now_time = int(time.time())-1*DAY 
          date_name = ts2datetime(now_time)

     weibo_community_mappings(date_name)
