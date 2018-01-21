# -*-coding:utf-8-*-
import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_tw_user_portrait as es
from global_utils import tw_portrait_index_name, tw_portrait_index_name

def tw_user_portrait_mappings(index_name=tw_portrait_index_name):
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
          tw_portrait_index_name: {
            "properties": {
              "activeness": {
                "type": "double"
              },
              "activity_geo": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "activity_geo_aggs": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "activity_geo_dict": {
                "type": "string",
                "index": "not_analyzed"
              },
              "admin@qq.com-tag": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "character_sentiment": {
                "type": "string",
                "index": "not_analyzed"
              },
              "sentiment": {
                "type": "string",
                "index": "not_analyzed"
              },
              "character_text": {
                "type": "string",
                "index": "not_analyzed"
              },
              "domain": {
                "type": "string",
                "index": "not_analyzed"
              },
              "fansnum": {
                "type": "long"
              },
              "filter_keywords": {
                "type": "string"
              },
              "friendsnum": {
                "type": "long"
              },
              "gender": {
                "type": "long"
              },
              "group": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "hashtag": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "hashtag_dict": {
                "type": "string",
                "index": "not_analyzed"
              },
              "importance": {
                "type": "double"
              },
              "influence": {
                "type": "double"
              },
              "keywords": {
                "type": "string",
                "index": "not_analyzed"
              },
              "keywords_string": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "location": {
                "type": "string",
                "index": "not_analyzed"
              },
              "online_pattern": {
                "type": "string",
                "index": "not_analyzed"
              },
              "online_pattern_aggs": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "photo_url": {
                "type": "string",
                "index": "not_analyzed"
              },
              "psycho_status": {
                "type": "string",
                "index": "not_analyzed"
              },
              "remark": {
                "type": "string",
                "index": "not_analyzed"
              },
              "sensitive": {
                "type": "double"
              },
              "sensitive_dict": {
                "type": "string",
                "index": "not_analyzed"
              },
              "sensitive_string": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "statusnum": {
                "type": "long"
              },
              "topic": {
                "type": "string",
                "index": "not_analyzed"
              },
              "topic_string": {
                "type": "string",
                "analyzer": "my_analyzer"
              },
              "uid": {
                "type": "string",
                "index": "not_analyzed"
              },
              "uname": {
                "type": "string",
                "index": "not_analyzed"
              },
              "verified": {
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
    tw_user_portrait_mappings()
