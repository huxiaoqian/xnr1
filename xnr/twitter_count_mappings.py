# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import twitter_keyword_count_index_name,twitter_keyword_count_index_type

def twitter_keyword_count_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            twitter_keyword_count_index_type:{
                'properties':{            
                    'xnr_user_no':{               # 虚拟人编号
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'date_time':{                #日期，例如：2017-09-07
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'keyword_value_string':{                #关键词统计结果
                        'type':'string',
                        'index':'no'
                    },
                    'timestamp':{ # 时间戳
                        'type':'long'
                    }
                }
            }
        }
    }
    exist_indice=es.indices.exists(index=twitter_keyword_count_index_name)
    if not exist_indice:
        es.indices.create(index=twitter_keyword_count_index_name,body=index_info,ignore=400)


if __name__=='__main__':
    twitter_keyword_count_mappings()