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
from global_utils import weibo_community_status_index_name,weibo_community_status_index_type

sys.path.append('../../../timed_python_files/community/')
from weibo_publicfunc import get_compelete_wbxnr

def weibo_community_status_mappings():
     index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_community_status_index_type:{
				'properties':{
					'xnr_user_no':{                     # xnr_user_no
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'status':{            #社区状态
                    'type':'long'
                    },
                    'datetime':{            #跟踪时间
                    'type':'long'
                    },
                    'date':{            #跟踪日期
                    'type':'string',
                    'index':'not_analyzed'
                    }     
				}
			}
		}
     }



     if not es.indices.exists(index=weibo_community_status_index_name):
          mark=es.indices.create(index=weibo_community_status_index_name,body=index_info,ignore=400)



if __name__ == '__main__':
	weibo_community_status_mappings()