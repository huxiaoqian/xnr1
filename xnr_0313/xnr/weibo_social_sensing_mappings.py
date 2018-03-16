# -*- coding:utf-8 -*-
import sys
import json
from global_utils import es_xnr as es
from global_utils import weibo_social_sensing_task_index_name,weibo_social_sensing_task_index_type,\
                        weibo_social_sensing_results_index_name,weibo_social_sensing_results_index_type

def social_sensing_task_mappings():
    index_info = {
        "settings":{
            "number_of_replicas": 0,
            'number_of_shards':5
        },
        "mappings":{
            weibo_social_sensing_task_index_type:{
                "properties":{
                    "task_name":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "task_type":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "last_time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "create_by":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "processing_status":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "stop_time":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "remark":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "social_sensors":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "history_status":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "create_at":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "warning_status":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "finish":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "burst_reason":{
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
    }

    if not es.indices.exists(index=weibo_social_sensing_task_index_name):
        es.indices.create(index=weibo_social_sensing_task_index_name,body=index_info,ignore=400)


def social_sensing_results_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            weibo_social_sensing_results_index_type:{
                'properties':{
                    'origin_weibo_number':{
                        'type':'long'
                    },
                    'duplicate_dict':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'comment_weibo_count':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'unfilter_users':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'weibo_total_number':{
                        'type':'long'
                    },
                    'mid_topic_value':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'origin_weibo_detail':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_words_dict':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'retweeted_weibo_count':{
                        'type':'long'
                    },
                    'timestamp':{
                        'type':'long'
                    },
                    'sensitive_weibo_detail':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'important_users':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'retweeted_weibo_detail':{
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }

    if not es.indices.exists(index=weibo_social_sensing_results_index_name):
        es.indices.create(index=weibo_social_sensing_results_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

    social_sensing_task_mappings()
    social_sensing_results_mappings()
