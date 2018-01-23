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
from fb_mappings_social_sensing import mappings_social_sensing_text


reload(sys)
sys.path.append("../../../")

from global_utils import es_xnr as es
from global_utils import es_user_portrait as es_profile
from global_utils import R_SOCIAL_SENSING as r
from global_config import S_TYPE, S_DATE_FB
from time_utils import ts2datetime, datetime2ts, ts2date

from parameter import topic_value_dict, signal_sensitive_variation

MAX_SIZE = 2000
TOP_HOT_FB = 100
HOT_LOWWER = 5 # 转发量大于多少才被感知
DAY = 24*3600

flow_text_index_name_pre = "facebook_flow_text_"
flow_text_index_type = "text"
facebook_count_index_name_pre = 'facebook_count_'
profile_index_name = "weibo_user"
profile_index_type = "user"

ALL_FID_LIST = [u'475267796191808', u'10208241366871040', u'419189055166375', u'419188801833067', \
u'419188591833088', u'419188565166424', u'289087538245771', u'289098978244627', u'289085634912628', \
u'524211057922308', u'495347340833241', u'894148497417367', u'1490488047710893', u'291091254711599', \
u'1346966988763002', u'475400189511902', u'419188388499775', u'475399369511984', u'872616822902262', \
u'894173877414829', u'495348377499804', u'475412106177377', u'419277055157575', u'419279011824046', \
u'419275971824350', u'289212318233293', u'475397929512128', u'1258200004323899', u'524215471255200',\
 u'1822332657795711', u'289211698233355', u'289211384900053', u'289211231566735', u'419283268490287',\
  u'1490621081030923', u'1490620957697602', u'10155211306276025', u'289226101565248', \
  u'289225188232006', u'289222291565629', u'495406837493958', u'894065320759018', u'894040604094823',\
  u'419188985166382', u'419188331833114', u'419188251833122', u'289102974910894', u'475269136191674',\
   u'1346821812110853', u'289101541577704', u'495346774166631', u'1821821531180157', \
   u'1490424354383929', u'1822139667815010', u'346106599187653', u'1822131954482448', \
   u'1822147821147528', u'507278012960381', u'141161913186961', u'894173864081497', \
   u'1822135184482125', u'419280611823886', u'419276278490986', u'419275858491028', \
   u'419280945157186', u'419278925157388', u'419281025157178', u'1442348255801922', \
   u'894173684081515', u'872691039561507', u'894173760748174', u'1822167664478877', \
   u'10210622397378443', u'289212851566573', u'1988632054751578', u'289210074900184', \
   u'1822153741146936', u'980085275463853', u'419283098490304', u'419283688490245',\
    u'289229281564930', u'419283438490270', u'289228328231692', u'1490621111030920', \
    u'1490621037697594', u'419286428489971', u'289224688232056', u'489166918125538',\
     u'495296307505011', u'1821946567834320', u'495296094171699', u'289091321578726', \
     u'419188458499768', u'289086118245913', u'289110394910152', u'289087231579135', \
     u'475266776191910', u'1795946903750031', u'495347750833200', u'495347477499894']

def get_weibo(item):
    keys = ["text","sensitive_words_string","sensitive", "uid", "fid", "keywords_string", "timestamp"]
    results = dict()
    for key in keys:
        results[key] = item[key]
    return results


# 获取前12个小时内转发数比较高（>=HOT_LOWWER）的帖子fid，如果没有则选取转发总数比较高的微博，共至少100条

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
            'all_fids':{
                'terms':{
                    'field':'fid',
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
    
    facebook_count_index_name_1 = facebook_count_index_name_pre + ts2datetime(end_ts)
    facebook_count_index_name_2 = facebook_count_index_name_pre + ts2datetime(end_ts-DAY)
    facebook_count_index_name_list = [facebook_count_index_name_1, facebook_count_index_name_2]

    print 'facebook_count_index_name_list...',facebook_count_index_name_list

    results = es.search(index=facebook_count_index_name_list ,doc_type='text',\
        body=query_body)['aggregations']['all_fids']['buckets']

    results_origin = copy.deepcopy(results)

    print 'start count aggs sort...'

    results.sort(key=lambda x:(x['stats_share']['max']-x['stats_share']['min']),reverse=True)
    
    fid_list = [item['key'] for item in results if (item['stats_share']['max']-item['stats_share']['min']) >= HOT_LOWWER]

    if len(fid_list) < TOP_HOT_FB:

        fid_list_2 = [item['key'] for item in results_origin[:TOP_HOT_FB - len(fid_list)]]

        fid_list.extend(fid_list_2)
    
    print 'all fid_list over...'
    print 'len..fid_list...',fid_list

    return fid_list, end_ts


def social_sensing():

    all_fid_list,end_ts= count_statis()

    if S_TYPE == 'test':
        all_fid_list = ALL_FID_LIST

    index_list = []
    for i in range(7):
        timestamp = end_ts - i*DAY
        flow_text_index_name = flow_text_index_name_pre + ts2datetime(timestamp)
        index_list.append(flow_text_index_name)
    #index_list = [flow_text_index_name_pre+date_1,flow_text_index_name_pre+date_2]
    print 'index_list...',index_list
    # 感知到的事, all_fid_list
    sensitive_text_list = []
    tmp_sensitive_warning = ""
    text_dict = dict() # 文本信息
    fid_value = dict() # 文本赋值
    duplicate_dict = dict() # 重合字典
    portrait_dict = dict() # 背景信息
    classify_text_dict = dict() # 分类文本
    classify_uid_list = []
    classify_fid_list = []
    duplicate_text_list = []
    sensitive_words_dict = dict()
    sensitive_weibo_detail = {}
    all_text_dict = dict()
    fid_ts_dict = dict() # 文本发布时间

    # 有事件发生时开始
    #if 1:

    if index_list and all_fid_list:
        query_body = {
            "query":{
                "filtered":{
                    "filter":{
                        "terms":{"fid": all_fid_list}
                    }
                }
            },
            "size": 5000
        }
        search_results = es.search(index=index_list, doc_type="text", body=query_body)['hits']['hits']
        print "search fid len: ", len(search_results)
    
        if search_results:
            for item in search_results:
                iter_uid = item['_source']['uid']
                iter_fid = item['_source']['fid']
                fid_ts_dict[iter_fid] = item["_source"]["timestamp"]
                iter_text = item['_source']['text'].encode('utf-8', 'ignore')
                iter_sensitive = item['_source'].get('sensitive', 0)
                tmp_text = get_weibo(item['_source'])
                all_text_dict[iter_fid] = tmp_text

                duplicate_text_list.append({"_id":iter_fid, "title": "", "content":iter_text.decode("utf-8",'ignore')})

                if iter_sensitive:
                    tmp_sensitive_warning = signal_sensitive_variation #涉及到敏感词的微博
                    sensitive_words_dict[iter_fid] = iter_sensitive

                keywords_dict = json.loads(item['_source']['keywords_dict'])
                personal_keywords_dict = dict()
                for k, v in keywords_dict.iteritems():
                    k = k.encode('utf-8', 'ignore')
                    personal_keywords_dict[k] = v
                classify_text_dict[iter_fid] = personal_keywords_dict
                #classify_uid_list.append(iter_uid)
                classify_fid_list.append(iter_fid)

            # 去重
            print "start duplicate"
            if duplicate_text_list:
                dup_results = duplicate(duplicate_text_list)
                for item in dup_results:
                    if item['duplicate']:
                        duplicate_dict[item['_id']] = item['same_from']

            # 分类
            print "start classify"
            fid_value = dict()
            if classify_text_dict:
                #classify_results = topic_classfiy(classify_uid_list, classify_text_dict)
                classify_results = topic_classfiy(classify_fid_list, classify_text_dict)
                
                #print "classify_results: ", classify_results

                for k,v in classify_results.iteritems(): # fid:value
                    #fid_value[k] = topic_value_dict[v[0]]
                    fid_value[k]=v[0]

    # organize data

    fid_list = all_text_dict.keys()
    print "final fid:", len(fid_list)
    print "intersection: ", len(set(fid_list)&set(all_fid_list))
    
    bulk_action = []
    count = 0

    social_sensing_index_name = "fb_social_sensing_text_" + ts2datetime(end_ts)
    mappings_social_sensing_text(social_sensing_index_name)

    for fid in fid_list:
        iter_dict = dict()

        if duplicate_dict.has_key(fid):
            iter_dict["duplicate"] = duplicate_dict[fid]
        else:
            iter_dict["duplicate"] = ""

        iter_dict["compute_status"] = 0  # 尚未计算
        iter_dict["topic_field"] = fid_value[fid]
        iter_dict["detect_ts"] = end_ts
        #iter_dict["xnr_user_no"] = xnr_user_no

        iter_dict.update(all_text_dict[fid])
        count += 1
        print 'iter_dict:::',iter_dict
        # _id = xnr_user_no + '_' + fid
        bulk_action.extend([{"index":{"_id": fid}}, iter_dict])
        if count % 500 == 0:
            es.bulk(bulk_action, index=social_sensing_index_name, doc_type="text", timeout=600)
            bulk_action = []

    if bulk_action:
        es.bulk(bulk_action, index=social_sensing_index_name, doc_type="text", timeout=600)


    return "1"

if __name__ == '__main__':

    social_sensing()