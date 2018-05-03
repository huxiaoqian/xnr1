# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_xnr_count_info_index_name,weibo_xnr_count_info_index_type,\
                         weibo_keyword_count_index_name,weibo_keyword_count_index_type


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
                    'date_time':{                #日期，例如：2017-09-07
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'fans_num':{                #粉丝数
                        'type':'long'
                    },
                    'total_post_sum':{          #总发帖量
                        'type':'long'
                    },
                    'daily_post_num':{          #日常发帖量
                        'type':'long'
                    },
                    'business_post_num':{       #业务发帖量
                        'type':'long'
                    },
                    'hot_follower_num':{        #热点追踪量
                        'type':'long'
                    },
                    'influence':{  # 影响力
                        'type':'long'
                    },
                    'penetration':{  # 渗透力
                        'type':'long'
                    },
                    'safe':{   # 安全性
                        'type':'long'
                    },
                    'timestamp':{ # 时间戳
                        'type':'long'
                    }
                }
            }
        }
    }
    exist_indice=es.indices.exists(index=weibo_xnr_count_info_index_name)
    if not exist_indice:
        es.indices.create(index=weibo_xnr_count_info_index_name,body=index_info,ignore=400)


def weibo_keyword_count_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            weibo_keyword_count_index_type:{
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
    exist_indice=es.indices.exists(index=weibo_keyword_count_index_name)
    if not exist_indice:
        es.indices.create(index=weibo_keyword_count_index_name,body=index_info,ignore=400)


if __name__=='__main__':
    weibo_xnr_count_info_mappings()
    weibo_keyword_count_mappings()
    
    es.indices.put_mapping(index=weibo_xnr_count_info_index_name, doc_type=weibo_xnr_count_info_index_type, \
            body={'properties':{'fans_total_num': {'type': 'long'},'fans_day_num': {'type': 'long'},'fans_growth_rate': {'type': 'long'},\
            'retweet_total_num': {'type': 'long'},'retweet_day_num': {'type': 'long'},'retweet_growth_rate': {'type': 'long'},\
            'comment_total_num': {'type': 'long'},'comment_day_num': {'type': 'long'},'comment_growth_rate': {'type': 'long'},\
            'like_total_num': {'type': 'long'},'like_day_num': {'type': 'long'},'like_growth_rate': {'type': 'long'},\
            'at_total_num': {'type': 'long'},'at_day_num': {'type': 'long'},'at_growth_rate': {'type': 'long'},\
            'private_total_num': {'type': 'long'},'private_day_num': {'type': 'long'},'private_growth_rate': {'type': 'long'},\
            'follow_group_sensitive_info': {'type': 'long'},'fans_group_sensitive_info': {'type': 'long'},'self_info_sensitive_info': {'type': 'long'},\
            'warning_report_total_sensitive_info': {'type': 'long'},'feedback_total_sensitive_info': {'type': 'long'},\
            }}, ignore=400)
