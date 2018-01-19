# -*-coding:utf-8-*-
import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_xnr as es
from global_utils import fb_domain_index_name,fb_domain_index_type,\
                        fb_role_index_name,fb_role_index_type


def domain_base_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            fb_domain_index_type:{
                'properties':{
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'domain_pinyin':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'domain_name':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'create_type':{  # {'by_keywords':[],'by_seed_users':[],'by_all_users':[]}
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'description':{
                        'type':'string',
                        'index':'no'
                    },
                    'create_time':{
                        'type':'long'
                    },
                    'group_size':{
                        'type':'long'
                    },
                    'member_uids':{     #用户uid_list  ['23123452','342212332',...]
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'submitter':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'remark':{
                        'type':'string',
                        'index':'no'
                    },
                    'compute_status':{   # 0-尚未计算，1-已存入uid，2-已存入群体描述，3-已存入角色分析
                        'type':'long' 
                    },
                    'role_distribute':{  # list
                        'type':'string',
                        'index':'no'
                    },
                    'top_keywords':{   # list
                        'type':'string',
                        'index':'no'
                    },
                    'political_side':{  #list
                        'type':'string',
                        'index':'no'
                    },
                    'topic_preference':{ #list
                        'type':'string',
                        'index':'no'
                    }
                }
            }
        }

    }
    if not es.indices.exists(index=fb_domain_index_name):
        print es.indices.create(index=fb_domain_index_name,body=index_info,ignore=400)


def role_base_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            fb_role_index_type:{
                'properties':{
                    'role_pinyin':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'role_name':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'domains':{   # dict
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'personality':{    # dict
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'political_side':{   # dict
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'geo':{      # dict
                        'type':'string',
                        'index':'no'
                    },
                    'active_time':{   #  [['开始时间','终止时间'],['13122343','132342523'],['132424352','1359083212'],...] 
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'day_post_num':{  # 最近一周  [['日期','帖子数'],['145099983','9'],['145990333','9'],...]
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }

    if not es.indices.exists(index=fb_role_index_name):
        print es.indices.create(index=fb_role_index_name,body=index_info,ignore=400)

if __name__ == '__main__':
    domain_base_mappings()
    role_base_mappings()