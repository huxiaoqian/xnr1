# -*- coding: utf-8 -*-
import json
import time
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
from sensitive.get_sensitive import get_sensitive_info,get_sensitive_user

es = Elasticsearch("http://219.224.134.213:9205/")

def executeES(indexName, typeName, listData):
    #current_time = time.time()
    #indexName += '_' + ts2datetime(current_time)

    for list in listData:
        data = {}
        jsonData = json.loads(list)
        for key, val in jsonData.items():
            # print key, '====', val
            # print type(val)
            data[key] = val

        data['sensitive_info'] = get_sensitive_info(data['timestamp'],data['mid'])
        data['sensitive_user'] = get_sensitive_user(data['uid'])

        es.index(index=indexName, doc_type=typeName, id=data["mid"], body=data)
    print 'update %s ES done' % indexName

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))
