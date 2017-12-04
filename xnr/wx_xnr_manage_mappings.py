# -*- coding:UTF-8 -*-
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_xnr,wx_xnr_index_name,wx_xnr_index_type,\
                    wx_xnr_history_count_index_name,wx_xnr_history_count_index_type,\
                    wx_xnr_history_be_at_index_type,wx_xnr_history_sensitive_index_type

def wx_xnr_mappings():
    index_info = {
        'settings':{
            'number_of_shards':5,
            'number_of_replicas':0,
            },
        'mappings':{
            wx_xnr_index_type:{
                'properties':{
                    'wx_id':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'puid':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'nickname':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'wx_groups_nickname':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'wx_groups_puid':{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'wx_groups_num':{
                        'type':'long',
                        'index':'not_analyzed'
                    },
                    'create_ts':{                    # 创建时间
                        'type':'long'
                    },
                    'wxbot_port':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'user_no':{
                        'type':'long'
                    },
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'password':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'remark':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'mail':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'access_id':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'submitter':{
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }
    exist_indice = es_xnr.indices.exists(index=wx_xnr_index_name)
    if not exist_indice:
        es_xnr.indices.create(index=wx_xnr_index_name, body=index_info, ignore=400)

def wx_xnr_history_count_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            wx_xnr_history_count_index_type:{
                'properties':{
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'puid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'date_time':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'daily_post_num':{
                        'type':'long'
                    },
                    'total_post_num':{
                        'type':'long'
                    },
                    'timestamp':{
                        'type':'long'
                    }
                }
            }
        }
    }

    exist_indice = es_xnr.indices.exists(index=wx_xnr_history_count_index_name)
    if not exist_indice:
        es_xnr.indices.create(index=wx_xnr_history_count_index_name, body=index_info, ignore=400)

def wx_xnr_history_be_at_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            wx_xnr_history_be_at_index_type:{
                'properties':{
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'puid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'date_time':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'daily_be_at_num':{
                        'type':'long'
                    },
                    'total_be_at_num':{
                        'type':'long'
                    },
                    'timestamp':{
                        'type':'long'
                    }
                }
            }
        }
    }

    exist_indice = es_xnr.indices.exists(index=wx_xnr_history_count_index_name)
    if not exist_indice:
        es_xnr.indices.create(index=wx_xnr_history_count_index_name, body=index_info, ignore=400)

def wx_xnr_history_sensitive_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            qq_xnr_history_sensitive_index_type:{
                'properties':{
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'puid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'date_time':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'daily_sensitive_num':{
                        'type':'long'
                    },
                    'total_sensitive_num':{
                        'type':'long'
                    },
                    'timestamp':{
                        'type':'long'
                    }
                }
            }
        }
    }

    exist_indice = es_xnr.indices.exists(index=wx_xnr_history_count_index_name)
    if not exist_indice:
        es_xnr.indices.create(index=wx_xnr_history_count_index_name, body=index_info, ignore=400)


if __name__ == '__main__':
    # wx_xnr_mappings()
    print
