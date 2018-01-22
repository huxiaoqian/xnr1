# -*- coding:utf-8 -*-
# version 3


import sys
import time
import json
import math
import copy
import numpy as np
from elasticsearch import Elasticsearch
from text_classify.test_topic import topic_classfiy
from duplicate import duplicate
from tw_mappings_social_sensing import mappings_social_sensing_text


reload(sys)
sys.path.append("../../../")

from global_utils import es_xnr as es
from global_utils import es_user_portrait as es_profile
from global_utils import R_SOCIAL_SENSING as r
from global_config import S_TYPE, S_DATE_FB
from time_utils import ts2datetime, datetime2ts, ts2date

from parameter import topic_value_dict, signal_sensitive_variation

MAX_SIZE = 2000
TOP_HOT_FB = 1000
HOT_LOWWER = 5 # 转发量大于多少才被感知
DAY = 24*3600

flow_text_index_name_pre = "twitter_flow_text_"
flow_text_index_type = "text"
twitter_count_index_name_pre = 'twitter_count_'
profile_index_name = "weibo_user"
profile_index_type = "user"

ALL_TID_LIST = [u'922897194100826112', u'922897222663995392', u'922897591678812162', \
u'922897798223216640', u'922897971074686976', u'922897988455927808', u'922898036526739456',\
 u'922898043174731776', u'922898089588985861', u'922898154286018560', u'922898277774843904',\
  u'922898412994887680', u'922898833893453824', u'922899011329318914', u'922899134352277509',\
   u'922899564348297217', u'922899665460142081', u'922899701237714945', u'922899817302560771', \
   u'922899956888772608', u'922899973078794241', u'922899986282569728', u'922900112296341504', \
   u'922900168164327424', u'922900230009491456', u'922900364340240384', u'922900376864608257', \
   u'922900548323508224', u'922900653395070977', u'922900679739527168', u'922900744033812480', \
   u'922900991632175104', u'922901103850778626', u'922902015579185157', u'922902151994548224', \
   u'922902231900401665', u'922902332089630721', u'922902564772777985', u'922902595705847808', \
   u'922903021935316992', u'922903132740337664', u'922903188277039104', u'922903233730838528', \
   u'922903299241730048', u'922903508151443456', u'922903897173245952', u'922903923731718144', \
   u'922904026261307392', u'922904134981840896', u'922904399873056768', u'922904419041132544', \
   u'922904471730049027', u'922904575626985473', u'922904601967263745', u'922904749556379649', \
   u'922904840790880258', u'922905114494476288', u'922905182744088577', u'922905567944884224', \
   u'922905721615912962', u'922905882328948736', u'922906018820042752', u'922906056505700353', \
   u'922906055071490048', u'922906354402017280', u'922906442918608896', u'922906624829939713', \
   u'922906725811830787', u'922906789808562176', u'922906859421470720', u'922907263454527489', \
   u'922907338968723456', u'922907397882081280', u'922907574919315456', u'922908134951198720', \
   u'922855304420663296', u'922855328772845570', u'922855368102854657', u'922855369541586944', \
   u'922855404484177922', u'922855410918334464', u'922855463359623173', u'922855653680525312', \
   u'922855797733896193', u'922855233184600065', u'922855816826208263', u'922855826359906305', \
   u'922855825345073158', u'922855888502767616', u'922855893808553984', u'922856018882781185', \
   u'922856033512390657', u'922856060125290496', u'922856139385200640', u'922856209207709696', \
   u'922856234973143040', u'922856258155061248', u'922856276115185664', u'922856374031171584', \
   u'922856436064952320']

def get_weibo(item):
    keys = ["text","sensitive_words_string","sensitive", "uid", "tid", "keywords_string", "timestamp"]
    results = dict()
    for key in keys:
        results[key] = item[key]
    return results


# 获取前12个小时内转发数比较高（>=HOT_LOWWER）的帖子tid，如果没有则选取转发总数比较高的微博，共至少100条

def count_statis():

    end_ts = int(time.time())

    if S_TYPE == 'test':
        end_ts = datetime2ts(S_DATE_FB)
    
    start_ts = end_ts - 12*3600 

    query_body = {
        'query':{   
            'bool':{
                'must':[
                    {'range':{'update_time':{'gt':start_ts,'lte':end_ts}}}
                ]
            }
        },
        'aggs':{
            'all_tids':{
                'terms':{
                    'field':'tid',
                    'order':{'stats_share.max':'desc'},
                    'size':MAX_SIZE
                },
                'aggs':{
                    'stats_share':{
                        'stats':{
                            'field':'share'
                        }
                    }
                }

            }
        }
    }
    
    twitter_count_index_name_1 = twitter_count_index_name_pre + ts2datetime(end_ts)
    twitter_count_index_name_2 = twitter_count_index_name_pre + ts2datetime(end_ts-DAY)
    twitter_count_index_name_list = [twitter_count_index_name_1, twitter_count_index_name_2]

    print 'twitter_count_index_name_list...',twitter_count_index_name_list

    results = es.search(index=twitter_count_index_name_list ,doc_type='text',\
        body=query_body)['aggregations']['all_tids']['buckets']

    results_origin = copy.deepcopy(results)

    print 'start count aggs sort...'

    results.sort(key=lambda x:(x['stats_share']['max']-x['stats_share']['min']),reverse=True)
    
    tid_list = [item['key'] for item in results if (item['stats_share']['max']-item['stats_share']['min']) >= HOT_LOWWER]

    if len(tid_list) < TOP_HOT_FB:

        tid_list_2 = [item['key'] for item in results_origin[:TOP_HOT_FB - len(tid_list)]]

        tid_list.extend(tid_list_2)
    
    print 'all tid_list over...'
    print 'len..tid_list...',tid_list

    return tid_list, end_ts


def social_sensing():

    all_tid_list,end_ts= count_statis()

    if S_TYPE == 'test':
        all_tid_list = ALL_TID_LIST

    index_list = []
    for i in range(7):
        timestamp = end_ts - i*DAY
        flow_text_index_name = flow_text_index_name_pre + ts2datetime(timestamp)
        index_list.append(flow_text_index_name)
    #index_list = [flow_text_index_name_pre+date_1,flow_text_index_name_pre+date_2]
    print 'index_list...',index_list
    # 感知到的事, all_tid_list
    sensitive_text_list = []
    tmp_sensitive_warning = ""
    text_dict = dict() # 文本信息
    tid_value = dict() # 文本赋值
    duplicate_dict = dict() # 重合字典
    portrait_dict = dict() # 背景信息
    classify_text_dict = dict() # 分类文本
    classify_uid_list = []
    classify_tid_list = []
    duplicate_text_list = []
    sensitive_words_dict = dict()
    sensitive_weibo_detail = {}
    all_text_dict = dict()
    tid_ts_dict = dict() # 文本发布时间

    # 有事件发生时开始
    #if 1:

    if index_list and all_tid_list:
        query_body = {
            "query":{
                "filtered":{
                    "filter":{
                        "terms":{"tid": all_tid_list}
                    }
                }
            },
            "size": 5000
        }
        search_results = es.search(index=index_list, doc_type="text", body=query_body)['hits']['hits']
        print "search tid len: ", len(search_results)
    
        if search_results:
            for item in search_results:
                iter_uid = item['_source']['uid']
                iter_tid = item['_source']['tid']
                tid_ts_dict[iter_tid] = item["_source"]["timestamp"]
                iter_text = item['_source']['text'].encode('utf-8', 'ignore')
                iter_sensitive = item['_source'].get('sensitive', 0)
                tmp_text = get_weibo(item['_source'])
                all_text_dict[iter_tid] = tmp_text

                duplicate_text_list.append({"_id":iter_tid, "title": "", "content":iter_text.decode("utf-8",'ignore')})

                if iter_sensitive:
                    tmp_sensitive_warning = signal_sensitive_variation #涉及到敏感词的微博
                    sensitive_words_dict[iter_tid] = iter_sensitive

                keywords_dict = json.loads(item['_source']['keywords_dict'])
                personal_keywords_dict = dict()
                for k, v in keywords_dict.iteritems():
                    k = k.encode('utf-8', 'ignore')
                    personal_keywords_dict[k] = v
                classify_text_dict[iter_tid] = personal_keywords_dict
                #classify_uid_list.append(iter_uid)
                classify_tid_list.append(iter_tid)

            # 去重
            print "start duplicate"
            if duplicate_text_list:
                dup_results = duplicate(duplicate_text_list)
                for item in dup_results:
                    if item['duplicate']:
                        duplicate_dict[item['_id']] = item['same_from']

            # 分类
            print "start classify"
            tid_value = dict()
            if classify_text_dict:
                #classify_results = topic_classfiy(classify_uid_list, classify_text_dict)
                classify_results = topic_classfiy(classify_tid_list, classify_text_dict)
                
                #print "classify_results: ", classify_results

                for k,v in classify_results.iteritems(): # tid:value
                    #tid_value[k] = topic_value_dict[v[0]]
                    tid_value[k]=v[0]

    # organize data

    tid_list = all_text_dict.keys()
    print "final tid:", len(tid_list)
    print "intersection: ", len(set(tid_list)&set(all_tid_list))
    
    bulk_action = []
    count = 0

    social_sensing_index_name = "tw_social_sensing_text_" + ts2datetime(end_ts)
    mappings_social_sensing_text(social_sensing_index_name)

    for tid in tid_list:
        iter_dict = dict()

        if duplicate_dict.has_key(tid):
            iter_dict["duplicate"] = duplicate_dict[tid]
        else:
            iter_dict["duplicate"] = ""

        iter_dict["compute_status"] = 0  # 尚未计算
        iter_dict["topic_field"] = tid_value[tid]
        iter_dict["detect_ts"] = end_ts
        #iter_dict["xnr_user_no"] = xnr_user_no

        iter_dict.update(all_text_dict[tid])
        count += 1
        print 'iter_dict:::',iter_dict
        # _id = xnr_user_no + '_' + tid
        bulk_action.extend([{"index":{"_id": tid}}, iter_dict])
        if count % 500 == 0:
            es.bulk(bulk_action, index=social_sensing_index_name, doc_type="text", timeout=600)
            bulk_action = []

    if bulk_action:
        es.bulk(bulk_action, index=social_sensing_index_name, doc_type="text", timeout=600)


    return "1"

if __name__ == '__main__':

    social_sensing()