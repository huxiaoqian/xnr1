# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import facebook_xnr_count_info_index_name,facebook_xnr_count_info_index_type,\
                         facebook_keyword_count_index_name,facebook_keyword_count_index_type


def facebook_xnr_count_info_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            facebook_xnr_count_info_index_type:{
              'properties': {
                'fans_total_num': {
                  'type': 'long'
                },
                'fans_day_num': {
                  'type': 'long'
                },
                'fans_growth_rate': {
                  'type': 'long'
                },
                'retweet_total_num': {
                  'type': 'long'
                },
                'retweet_day_num': {
                  'type': 'long'
                },
                'retweet_growth_rate': {
                  'type': 'long'
                },
                'comment_total_num': {
                  'type': 'long'
                },
                'comment_day_num': {
                  'type': 'long'
                },
                'comment_growth_rate': {
                  'type': 'long'
                },
                'like_total_num': {
                  'type': 'long'
                },
                'like_day_num': {
                  'type': 'long'
                },
                'like_growth_rate': {
                  'type': 'long'
                },
                'at_total_num': {
                  'type': 'long'
                },
                'at_day_num': {
                  'type': 'long'
                },
                'at_growth_rate': {
                  'type': 'long'
                },
                'private_total_num': {
                  'type': 'long'
                },
                'private_day_num': {
                  'type': 'long'
                },
                'private_growth_rate': {
                  'type': 'long'
                },
                'follow_group_sensitive_info': {
                  'type': 'long'
                },
                'fans_group_sensitive_info': {
                  'type': 'long'
                },
                'self_info_sensitive_info': {
                  'type': 'long'
                },
                'warning_report_total_sensitive_info': {
                  'type': 'long'
                },
                'feedback_total_sensitive_info': {
                  'type': 'long'
                }
              }
            }
        }
    }
    exist_indice=es.indices.exists(index=facebook_xnr_count_info_index_name)
    if not exist_indice:
        es.indices.create(index=facebook_xnr_count_info_index_name,body=index_info,ignore=400)


def facebook_keyword_count_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            facebook_keyword_count_index_type:{
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
    exist_indice=es.indices.exists(index=facebook_keyword_count_index_name)
    if not exist_indice:
        es.indices.create(index=facebook_keyword_count_index_name,body=index_info,ignore=400)


if __name__=='__main__':
    facebook_xnr_count_info_mappings()
    #facebook_keyword_count_mappings()
