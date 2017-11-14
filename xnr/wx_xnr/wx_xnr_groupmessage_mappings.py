# -*-coding:utf-8-*-
import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_xnr as es
from global_utils import wx_group_message_index_name_pre, wx_group_message_index_type

from global_config import WX_S_DATE

def wx_group_message_mappings(date):
    index_name = wx_group_message_index_name_pre + str(date)
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            wx_group_message_index_type:{
                'properties':{
                    'wx_group_puid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'wx_group_nickname':{
                         'type':'string',
                         'index':'not_analyzed'
                    },
                    'type':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'text':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'speaker_wx_puid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'speaker_wx_nickname':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'timestamp':{
                        'type':'long'
                        
                    },
                    'xnr_wx_id':{
                        'type':'string',
                        'index': 'not_analyzed'
                    },
                    'xnr_wx_puid':{
                        'type':'string',
                        'index': 'not_analyzed'
                    },
                    'xnr_wx_nickname':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_value':{
                        'type':'long'
                    },
                    'sensitive_words_string':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_flag':{
                        'type':'long'
                    },
                    'at_flag':{
                        'type':'long'
                    }
                }

            }
        },
    }
    print index_name
    if not es.indices.exists(index=index_name):
        print es.indices.create(index=index_name,body=index_info,ignore=400)

if __name__ == '__main__':
    date = WX_S_DATE
    wx_group_message_mappings(date)
