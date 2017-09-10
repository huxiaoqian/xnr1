# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_xnr_count_info_index_name,weibo_xnr_count_info_index_type


def weibo_xnr_count_info_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            weibo_xnr_count_info_index_type:{
                'properties':{            
                    'xnr_user_no':{               # 虚拟人编号
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'date_time':{                #时间，例如：2017-09-07
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'fans_num':{                #粉丝数
                        'type':'long'
                    },
                    'total_post_sum':{        #
                        'type':'long'
                    },
                    'daily_post_num':{
                         'type':'long'
                    },
                    'business_post_num':{
                         'type':'long'
                    },
                    'hot_follower_num':{
                         'type':'long'
                    }
                }
            }
        }
    }
    exist_indice=es.indices.exists(index=weibo_xnr_count_info_index_name)
    if not exist_indice:
        es.indices.create(index=weibo_xnr_count_info_index_name,body=index_info,ignore=400)


if __name__=='__main__':
	weibo_xnr_count_info_mappings()
