# -*- coding:UTF-8 -*-
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type,\
                    qq_xnr_history_count_index_name,qq_xnr_history_count_index_type,\
                    qq_xnr_history_be_at_index_type,qq_xnr_history_sensitive_index_type

def qq_xnr_mappings():
    index_info = {
        'settings':{
            'number_of_shards':5,
            'number_of_replicas':0,
            },
        'mappings':{
            qq_xnr_index_type:{
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
                    'qq_groups_num':{
                        'type':'long',
                        'index':'not_analyzed'
                    },
                    'create_ts':{                    # 创建时间
                        'type':'long'
                    },
                    'qqbot_port':{
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
                    'access_id':{
                        'type':'string',
                        'index':'no'
                    },
                    'submitter':{
                        'type':'string',
                        'index':'not_analyzed'
                    }     
                }
            }
        }
    }
    exist_indice = es_xnr.indices.exists(index=qq_xnr_index_name)
    
    if not exist_indice:
        es_xnr.indices.create(index=qq_xnr_index_name, body=index_info, ignore=400)

def qq_xnr_history_count_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{    
            qq_xnr_history_count_index_type:{
                'properties':{
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'qq_number':{
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

    exist_indice = es_xnr.indices.exists(index=qq_xnr_history_count_index_name)
    
    if not exist_indice:

        es_xnr.indices.create(index=qq_xnr_history_count_index_name, body=index_info, ignore=400)

def qq_xnr_history_be_at_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{    
            qq_xnr_history_be_at_index_type:{
                'properties':{
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'qq_number':{
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

    exist_indice = es_xnr.indices.exists(index=qq_xnr_history_count_index_name)
    
    if not exist_indice:

        es_xnr.indices.create(index=qq_xnr_history_count_index_name, body=index_info, ignore=400)

def qq_xnr_history_sensitive_mappings():
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
                    'qq_number':{
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

    exist_indice = es_xnr.indices.exists(index=qq_xnr_history_count_index_name)
    
    if not exist_indice:

        es_xnr.indices.create(index=qq_xnr_history_count_index_name, body=index_info, ignore=400)


if __name__ == '__main__':

    qq_xnr_mappings()
    qq_xnr_history_count_mappings()
    qq_xnr_history_sensitive_mappings()
    qq_xnr_history_be_at_mappings()

    # es_xnr.indices.put_mapping(index=qq_xnr_index_name, doc_type='user', \
    #         body={'properties':{'qqbot_port': {'type': 'string', 'index':'not_analyzed'}}}, ignore=400)

