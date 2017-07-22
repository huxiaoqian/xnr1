# -*- coding: utf-8 -*-
import json

import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan

es = Elasticsearch("http://219.224.134.213:9205/")


def executeES(indexName, typeName, listData):
    for list in listData:
        data = {}
        jsonData = json.loads(list)
        for key, val in jsonData.items():
            # print key, '====', val
            # print type(val)
            data[key] = val

        es.index(index=indexName, doc_type=typeName, id=data["mid"], body=data)
    print 'update %s ES done' % indexName


def deleteESForQuery():
    query_search = es.search(index="weibo_feedback_at", body={"query": {"match_all": {}}, "size": 50})
    # print query_search
    for hit in query_search['hits']['hits']:
        print hit["_id"]
        # es.delete(index="weibo_feedback_at", doc_type="text", id=hit["_id"])

if __name__ == '__main__':
    deleteESForQuery()
