# -*-coding:utf-8-*-

import sys
reload(sys)
sys.path.append("../../")
import json
from time_utils import ts2datetime, datetime2ts

from elasticsearch import Elasticsearch

es = Elasticsearch("219.224.134.216:9201", timeout=600)
topic_field_dict = {'art':1,'computer':2,'economic':3, 'education':4,'environment':5, 'medicine':6,\
                    'military':7,'politics':8,'sports':9,'traffic':10,'life':11,'anti-corruption':12,\
                     'employment':13,'fear-of-violence':14, 'house':15,'law':16,'peace':17,\
                     'religion':18,'social-security':19,'null':20}

def function_1():
    mid_list = []
    mid_dict = dict()
    with open("fff.txt", "r") as f:
        for line in f:
            line = line.strip()
            tmp_list = line.split(" ")
            if tmp_list[1] in set(["life",'sports','computer','art','traffic']):
                continue
            mid_list.append(tmp_list[0])
            mid_dict[tmp_list[0]] = tmp_list[1]


    lenth = len(mid_list)

    len_1000 = lenth/1000
    print lenth
    true_list = []


    f = open("mid_list.txt", "w")

    for i in range(len_1000):
        tmp_mid_list = mid_list[i*1000:(i+1)*1000]
        if tmp_mid_list:
            es_results = es.mget(index="flow_text_2016-11-18", doc_type="text", body={"ids":tmp_mid_list})["docs"]
            for item in es_results:
                if item["found"]:
                    true_list.append(item["_id"])
                    f.write(str(item["_id"])+'\n')
    f.close()
    print len(true_list)



def extract_feature(mid):
    f_feature = open("feature_13.txt", "a")
    f_value = open("value_13.txt", "a")
    count = 0
    result = es.get(index="flow_text_2016-11-20", doc_type="text", id=mid)["_source"]
    ts = result["timestamp"]
    index_list = []
    for i in range(7):
        index_list.append("flow_text_"+ts2datetime(ts+i*24*3600))

    query_body = {
        "query":{
            "term":{"root_mid":mid}
        }
    }
    #total_weibo
    count = es.count(index=index_list, doc_type="text", body=query_body)["count"]

    query_body_uid = {
        "query":{
            "term":{"root_mid":mid}
        },
        "aggs":{
            "uid_count":{
                "cardinality":{"field": "uid"}
            }
        }
    }
    # total_uid
    total_uid_count = es.search(index=index_list, doc_type="text", body=query_body_uid)['aggregations']["uid_count"]["value"]



    feature_list = []
    feature_list.append(result["user_fansnum"])
    query_body_ts = {
        "query":{
            "bool":{
                "must":[
                    {"term":{"root_mid":mid}},
                    {"range":{
                        "timestamp":{
                            "lt": ts + 3600*10
                        }
                    }}
                ]
            }
        },
        "aggs":{
            "weibo_type":{
                "terms":{"field": "message_type"}
            }
        }
    }
    comment = 0
    retweet = 0
    tmp_count = es.search(index=index_list, doc_type="text", body=query_body_ts)['aggregations']["weibo_type"]["buckets"]
    if tmp_count:
        for item in tmp_count:
            if int(item["key"]) == 2:
                comment = item["doc_count"]
            elif int(item["key"]) == 3:
                retweet = item["doc_count"]
    feature_list.append(comment+retweet)
    feature_list.append(retweet)
    feature_list.append(comment)
    feature_list.append(retweet/float(comment+retweet+1))
    feature_list.append(comment/float(comment+retweet+1))
    query_body_uid = {
        "query":{
            "bool":{
                "must":[
                    {"term":{"root_mid":mid}},
                    {"range":{
                        "timestamp":{
                            "lt": ts + 3600*10
                        }
                    }}
                ]
            }
        },
        "aggs":{
            "uid_count":{
                "cardinality":{"field": "uid"}
            }
        }
    }
    uid_count = es.search(index=index_list, doc_type="text", body=query_body_uid)['aggregations']["uid_count"]["value"]
    feature_list.append(uid_count)
    #feature_list.append(topic_field_dict[mid_dict[mid]])
    f_feature.write(json.dumps(feature_list)+"\n")
    f_value.write(json.dumps([count, total_uid_count])+"\n")
    print feature_list, [count, total_uid_count]

    f_feature.close()
    f_value.close()


