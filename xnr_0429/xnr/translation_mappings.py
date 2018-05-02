# -*-coding:utf-8-*-
import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_translation as es
from global_utils import translation_index_name, translation_index_type

def translation_mappings(index_name=translation_index_name):
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5,
            'analysis':{
                'analyzer':{
                    'my_analyzer':{
                    'type': 'pattern',
                    'pattern': '&'
                        }
                    }
                }
        },
        "mappings": {
          translation_index_type: {
            "properties": {
              "translation": {
                "type": "string",
                "index": "not_analyzed"
              },
            }
          }
        }
    }
    if not es.indices.exists(index=index_name):
        print es.indices.create(index=index_name,body=index_info,ignore=400)

if __name__ == '__main__':
    translation_mappings()
