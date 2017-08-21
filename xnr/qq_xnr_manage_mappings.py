# -*- coding:UTF-8 -*-
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_xnr,qq_xnr_index_name

def qq_xnr_mappings():
    index_info = {
        'settings':{
            'number_of_shards':5,
            'number_of_replicas':0,
            },
        'mappings':{
            'group':{
                'properties':{
                    'qq_number':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'nickname':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'qq_groups':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'active_time':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'today_speak_num':{             # 今日发言数
                        'type': 'long',
                        'index': 'not_analyzed'
                    },
                    'all_speak_num':{               # 历史发言总数
                        'type': 'long',
                        'index': 'not_analyzed'
                    },
                    'today_remind':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'create_ts':{                    # 创建时间
                        'type':'long',
                        'index':'not_analyzed'
                    },
                    'sensitive_value':{
                        'type':'long',
                        'index':'not_analyzed'      # 敏感程度
                    }                
                }
            }
        }
    }
    exist_indice = es_xnr.indices.exists(index=qq_xnr_index_name)
    if exist_indice:
        #delete
        es_xnr.indices.delete(index='qq_xnr', timeout=100)    
    #create
    es_xnr.indices.create(index=qq_xnr_index_name, body=index_info, ignore=400)

if __name__ == '__main__':
    qq_xnr_mappings()