# -*- coding:utf-8 -*-

import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
reload(sys)
sys.path.append("../../../")
from global_utils import es_xnr as es

def mappings_sensing_task(task_name):
    index_info = {
        "settings":{
            "number_of_replicas": 0
        },
        "mappings":{
            task_name:{
                "properties":{
                    "origin_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "retweeted_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "comment_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "weibo_total_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_origin_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_retweeted_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_comment_weibo_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sensitive_weibo_total_number":{
                        "type": "long",
                        "index": "no"
                    },
                    "sentiment_distribution":{
                        "type": "string",
                        "index": "no"
                    },
                    "trendline_dict":{
                        "type": "string",
                        "index": "no"
                    },
                    "uid_prediction_dict":{
                        "type": "string",
                        "index": "no"
                    },
                    "weibo_prediction_dict":{
                        "type": "string",
                        "index": "no"
                    },
                    "origin_weibo_detail":{
                        "type": "string",
                        "index": "no"
                    },
                    "retweeted_weibo_detail":{
                        "type": "string",
                        "index": "no"
                    },
                    "sensitive_weibo_detail":{
                        "type": "string",
                        "index": "no"
                    },
                    "unfilter_users":{
                        "type": "string",
                        "index": "no"
                    },
                    "important_users":{
                        "type": "string",
                        "index": "no"
                    },
                    "timestamp":{
                        "type": "long",
                    },
                    "burst_reason":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "geo":{
                        "type": "string",
                        "index": "no"
                    },
                    "clustering_topic":{
                        "type": "string",
                        "index": "no"
                    },
                    "create_by":{
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
    }

    es.indices.create(index="social_sensing_task", body=index_info, ignore=400)

    return "1"

def manage_sensing_task():
    index_info = {
        "settings":{
            "number_of_replicas": 0
        },
        "mappings":{
            "sensing_task":{
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
                    },
                    'xnr_user_no':{     # 增加虚拟人
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }

    es.indices.create(index="manage_sensing_task", body=index_info, ignore=400)

def mappings_social_sensing_text():
    index_info = {
        "settings":{
            "number_of_replicas": 0
        },
        "mappings":{
            "text":{
                "properties":{
                    "trendline":{
                        "type": "string",
                        "index": "no"
                    },
                    "duplicate":{
                        "type": "float",
                        "index": "no"
                    },
                    "uid_prediction":{
                        "type": "float",
                        "index": "no"
                    },
                    "weibo_prediction":{
                        "type": "float",
                        "index": "no"
                    },
                    "mid_topic_value":{
                        "type": "float",
                    },
                    "detect_ts":{
                        "type": "long",
                    },
                    "text":{
                        "type": "string",
                        "index": "no"
                    },
                    "sensitive_words_string":{
                        "type": "string",
                        "index": "no"
                    },
                    "sensitive":{
                        "type": "float",
                    },
                    "uid":{
                        "type": "string",
                    },
                    "user_fansnum":{
                        "type": "long"
                    },
                    "mid":{
                        "type": "string"
                    },
                    "keyswords_string":{
                        "type": "string",
                        "index": "no"
                    },
                    "geo":{
                        "type": "string",
                        "index": "no"
                    },
                    "ip":{
                        "type": "string",
                        "index": "no"
                    },
                    "timestamp":{
                        "type": "long"
                    },
                    "message_type":{
                        "type": "long"
                    },
                    "type":{
                        "type": "long"
                    },
                    'topic_field':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'compute_status':{   # 0- 尚未计算， 1-正在计算，2- 计算王成
                        'type':'long'
                    },
                    'xnr_user_no':{    # 增加虚拟人
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }

    es.indices.create(index="social_sensing_text",body=index_info, ignore=400)


if __name__ == "__main__":
    #manage_sensing_task()
    #mappings_sensing_task("social_sensing")
    mappings_social_sensing_text()


