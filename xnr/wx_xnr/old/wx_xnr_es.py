# -*- coding: utf-8 -*-
import json
from elasticsearch import Elasticsearch

class WX_XNR_ES():
    def __init__(self, index_name, doc_type, host='127.0.0.1:9200'):
        self.es = Elasticsearch(host)
        self.index_name = index_name
        self.doc_type = doc_type
    
    def create_index(self, mappings={}, index_name=None, params=None):
        #create a index without replicas
        if index_name:
            self.index_name = index_name
        if not self.es.indices.exists(index=self.index_name):
            return self.es.indices.create(index=self.index_name, ignore=400, body={
                'settings':{
                    'number_of_shards':5,
                    'number_of_replicas':0,
                },
                'mappings':mappings
            })
        
    def put_mapping(self, doc_type, mapping={}, index_name=None):
        #实际上是通过put_mapping的方式规定一个doc_type的mapping，但其实有些不符合该mapping的数据也能存储进来，并改变mapping
        if index_name:
            self.index_name = index_name
        return self.es.indices.put_mapping(doc_type, body=mapping, index=self.index_name)
    
    def save_data(self, doc_type, data, data_id=None, index_name=None):
        #data(dict)
        if index_name:
            self.index_name = index_name
        return self.es.index(index=self.index_name, doc_type=doc_type, body=json.dumps(data), id=data_id)
        
    
if __name__ == '__main__':
    data = {'xnr_name': u'\u5c0f\u73c2', 'msg_type': 'Text', 'text': u'999', 'group_name': u'group_test_1', 'speaker_name': u'\u97e9\u68a6\u6210', 'group_id': u'a6285337', 'timrestamp': 1507096836, 'xnr_id': u'5c584b12', 'speaker_id': u'c97a6d12'}
    es_groupmsg = WX_XNR_ES(index_name='wx_xnr_groupmsg', doc_type='groupmsg')
    es_groupmsg.save_data(doc_type=es_groupmsg.doc_type, data=data)


  