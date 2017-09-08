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
                    },               
                    'password':{                #密码
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'create_time':{              #创建时间
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'domain_name':{              #渗透领域
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'create_status':{        #虚拟人创建状态
                        'type':'long'           #0表示第一步完成，1表示第二步完成 2表示第三步完成，即最终完成创建。
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
