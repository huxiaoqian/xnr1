# -*-coding:utf-8-*-

import time
import os
import json
from collections import Counter
import sys
sys.path.append('../')
from global_utils import es_xnr, facebook_flow_text_index_name_pre as flow_text_index_name_pre,\
                        facebook_flow_text_index_type as  flow_text_index_type,\
                        fb_xnr_flow_text_index_name_pre as xnr_flow_text_index_name_pre,\
                        fb_xnr_flow_text_index_type as xnr_flow_text_index_type,\
                        fb_xnr_index_name, fb_xnr_index_type,\
                        new_fb_xnr_flow_text_index_name_pre, new_fb_xnr_flow_text_index_type
es_flow_text = es_xnr
from global_config import S_TYPE, S_DATE_FB as S_DATE
from time_utils import ts2datetime,datetime2ts
from parameter import MAX_VALUE,fb_tw_topic_en2ch_dict as topic_en2ch_dict, FB_TW_TOPIC_ABS_PATH
sys.path.append(FB_TW_TOPIC_ABS_PATH)
from config import name_list, zh_data
from test_topic import topic_classfiy
sys.path.append('../fb_tw_user_portrait')
from keyword_extraction import get_filter_keywords_for_match_function




#该函数用于爬取并存储完new_xnr_flow_text_数据后调用，以增添topic_field_first等字段
def match_flow_text(current_date):
    '''
    #mapping有误，暂时不创建及存储数据，2018-4-13 17:11:51
    new_xnr_flow_text_index_name = new_xnr_flow_text_index_name_pre + current_date
    new_weibo_xnr_flow_text_mappings(new_xnr_flow_text_index_name)
    '''

    flow_text_index_name = new_fb_xnr_flow_text_index_name_pre + current_date

    query_body = {
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE
    }
    try:
        search_results = es_xnr.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,\
                            body=query_body)['hits']['hits']
        bulk_action = []
        uid_list = []
        xnr_user_no_list = []
        count = 0
        for result in search_results:
            result = result['_source']
            if result.has_key('uid'):
                uid_list.append(result['uid'])
                xnr_user_no_list.append(result['xnr_user_no'])

        # print uid_list
        # print xnr_user_no_list
        #filter_keywords = {uid1:{mid1:{k:v, ...}...}...}
        filter_keywords = get_filter_keywords_for_match_function([flow_text_index_name], uid_list)
        for uid, content in filter_keywords.items():
            mid_list = []
            mid_weibo = {}  #（{mid1:{'key1':f1,'key2':f2...}...}）
            for mid, keywords_dict in content.items():
                for k, v in keywords_dict.items():
                    keywords_dict[k.encode('utf-8', 'ignore')] = v
                mid_list.append(mid)
                mid_weibo[mid] = keywords_dict

            #mid_topic_dict   {mid1:{'art':0.1,'social':0.2...}...}
            #mid_topic_list   {mid1:['art','social','media']...}
            mid_topic_dict, mid_topic_list = topic_classfiy(mid_list, mid_weibo)
            for mid, topic_dict in mid_topic_dict.items():
                match_item = {
                    'topic_field_first': topic_en2ch_dict[mid_topic_list[mid][0]],
                    'topic_field': '&'.join(mid_topic_list[mid]),
                    'xnr_user_no': xnr_user_no_list[uid_list.index(uid)],
                }
                action = {'update':{'_id':mid}}
                bulk_action.extend([action, {'doc': match_item}])

        if bulk_action:
            es_xnr.bulk(bulk_action,index=flow_text_index_name,doc_type=new_fb_xnr_flow_text_index_type,timeout=600)

    except Exception,e:
        print e
        return 'no tweets to update today'


if __name__ == '__main__':
    '''
    if S_TYPE == 'test':
        current_date = S_DATE
    else:
        current_time = int(time.time())
        current_date = ts2datetime(current_time)
    print match_flow_text(current_date)
    '''
    #2017-10-15     2017-10-25
    for i in range(15, 26, 1):
        date = '2017-10-' + str(i)
        match_flow_text(current_date=date)