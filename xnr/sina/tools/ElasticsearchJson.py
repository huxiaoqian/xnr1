# -*- coding: utf-8 -*-
import json
import time
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
from sensitive.get_sensitive import get_sensitive_info,get_sensitive_user
import sys
sys.path.append('../../')
from utils import uid2xnr_user_no,save_to_fans_follow_ES
from global_utils import es_xnr as es

es = Elasticsearch("http://219.224.134.213:9205/")

def executeES(indexName, typeName, listData):
    current_time = int(time.time())
    #indexName += '_' + ts2datetime(current_time)

    for list_data in listData:
        data = {}
        jsonData = json.loads(list_data)
        print 'jsonData::',jsonData
        for key, val in jsonData.items():
            print key, '====', val
            # print type(val)
            data[key] = val
            # data['update_time'] = current_time

        data['sensitive_info'] = get_sensitive_info(data['timestamp'],data['mid'])
        data['sensitive_user'] = get_sensitive_user(data['uid'])
        if indexName == 'weibo_feedback_follow':
            # 修改 _id、保存至fans_followers_es表
            _id = data["root_uid"]+'_'+data["mid"]
            xnr_user_no = uid2xnr_user_no(data["root_uid"])
            print 'xnr_user_no::',xnr_user_no
            save_type = 'followers'
            if xnr_user_no:
                save_to_fans_follow_ES(xnr_user_no,data["uid"],save_type)
        
        elif indexName == 'weibo_feedback_fans':
            _id = data["root_uid"]+'_'+data["mid"]
            xnr_user_no = uid2xnr_user_no(data["root_uid"])
            save_type = 'fans'
            if xnr_user_no:
                save_to_fans_follow_ES(xnr_user_no,data["uid"],save_type)
        else:
            _id = data["mid"]
               
        print 'indexName::',indexName
        print 'data::',data
        es.index(index=indexName, doc_type=typeName, id=_id, body=data)
    print 'update %s ES done' % indexName

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))
