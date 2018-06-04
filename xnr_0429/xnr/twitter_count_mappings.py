# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr_2 as es
from global_utils import twitter_keyword_count_index_name,twitter_keyword_count_index_type,\
                        twitter_xnr_count_info_index_name,twitter_xnr_count_info_index_type

def twitter_xnr_count_info_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            twitter_xnr_count_info_index_type:{
              'properties': {
                'comment_day_num': {
                  'type': 'long'
                },
                'at_total_num': {
                  'type': 'long'
                },
                'user_fansnum': {
                  'type': 'long'
                },
                'xnr_user_no': {
                  'index': 'not_analyzed',
                  'type': 'string'
                },
                'comment_total_num': {
                  'type': 'long'
                },
                'timestamp': {
                  'type': 'long'
                },
                'private_total_num': {
                  'type': 'long'
                },
                'safe': {
                  'type': 'long'
                },
                'influence': {
                  'type': 'long'
                },
                'retweet_total_num': {
                  'type': 'long'
                },
                'fans_group_sensitive_info': {
                  'type': 'long'
                },
                'feedback_total_sensitive_info': {
                  'type': 'long'
                },
                'like_growth_rate': {
                  'type': 'long'
                },
                'penetration': {
                  'type': 'long'
                },
                'at_day_num': {
                  'type': 'long'
                },
                'private_growth_rate': {
                  'type': 'long'
                },
                'private_day_num': {
                  'type': 'long'
                },
                'fans_growth_rate': {
                  'type': 'long'
                },
                'fans_total_num': {
                  'type': 'long'
                },
                'fans_num': {
                  'type': 'long'
                },
                'fans_day_num': {
                  'type': 'long'
                },
                'date_time': {
                  'index': 'not_analyzed',
                  'type': 'string'
                },
                'retweet_growth_rate': {
                  'type': 'long'
                },
                'daily_post_num': {
                  'type': 'long'
                },
                'business_post_num': {
                  'type': 'long'
                },
                'at_growth_rate': {
                  'type': 'long'
                },
                'comment_growth_rate': {
                  'type': 'long'
                },
                'trace_follow_tweet': {
                  'type': 'long'
                },
                'follow_group_sensitive_info': {
                  'type': 'long'
                },
                'like_total_num': {
                  'type': 'long'
                },
                'like_day_num': {
                  'type': 'long'
                },
                'total_post_sum': {
                  'type': 'long'
                },
                'warning_report_total_sensitive_info': {
                  'type': 'long'
                },
                'hot_follower_num': {
                  'type': 'long'
                },
                'trace_follow_tweet_num': {
                  'type': 'long'
                },
                'self_info_sensitive_info': {
                  'type': 'long'
                },
                'retweet_day_num': {
                  'type': 'long'
                }
              }
            }
        }
    }
    exist_indice=es.indices.exists(index=twitter_xnr_count_info_index_name)
    if not exist_indice:
        es.indices.create(index=twitter_xnr_count_info_index_name,body=index_info,ignore=400)

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
    # twitter_keyword_count_mappings()
    twitter_xnr_count_info_mappings()