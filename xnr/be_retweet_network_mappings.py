#-*-coding:utf-8-*-

import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es

#use to mappings for be_retweet es
def be_retweet_es_mappings(db_number,ft_type):
    index_info = {
            'settings':{
                'number_of_shards': 5,
                'number_of_replicas':0
                },
            'mappings':{
                'user':{
                    'properties':{
                    'uid':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'uid_be_retweet':{
                        'type': 'string',
                        'index': 'no'
                        }
                    }
                    }
                }
        }

    if ft_type == 'fb':

        index_name = 'fb_be_retweet_'+db_number
    else:
        index_name = 'tw_be_retweet_'+db_number

    exist_indice = es.indices.exists(index=index_name)

    if not exist_indice:
        #es.indices.delete(index=index_name)
        es.indices.create(index=index_name, body=index_info, ignore=400)
    return True

if __name__ == '__main__':

    db_number_list = ['1', '2']
    ft_type_list = ['fb', 'tw']
    for db_number in db_number_list:
        for ft_type in ft_type_list:
            be_retweet_es_mappings(db_number,ft_type)