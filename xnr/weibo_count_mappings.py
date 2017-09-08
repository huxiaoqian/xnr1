# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr 
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
                    'uid':{                     # uid
                        'type':'string',
                        'index':'not_analyzed'
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
