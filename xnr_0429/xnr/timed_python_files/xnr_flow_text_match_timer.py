# -*-coding:utf-8-*-

import time
import os
import json
from collections import Counter

from new_weibo_xnr_flow_text_mappings import new_weibo_xnr_flow_text_mappings, new_xnr_flow_text_index_name_pre,\
                                        new_xnr_flow_text_index_type

import sys
sys.path.append('../')

from global_utils import es_xnr,es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                        xnr_flow_text_index_name_pre,xnr_flow_text_index_type,\
                        weibo_xnr_index_name, weibo_xnr_index_type
from global_config import S_TYPE, S_DATE
from time_utils import ts2datetime,datetime2ts
from parameter import MAX_VALUE,topic_en2ch_dict
from timed_python_files.text_classify.test_topic import topic_classfiy

def match_flow_text():

    current_time = int(time.time())
    current_date = ts2datetime(current_time)

    new_xnr_flow_text_index_name = new_xnr_flow_text_index_name_pre + current_date

    new_weibo_xnr_flow_text_mappings(new_xnr_flow_text_index_name)

    #xnr_flow_text_index_name = xnr_flow_text_index_name_pre + current_date
    flow_text_index_name = flow_text_index_name_pre + current_date

    query_body = {
        'query':{
            'term':{'create_status':2}
        },
        'size':MAX_VALUE
    }

    try:
        search_results = es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,\
                            body=query_body)['hits']['hits']

        bulk_action = []
        count = 0

        for result in search_results:
            result = result['_source']
            uid = result['uid']
            xnr_user_no = result['xnr_user_no']

            match_query_body = {
		'query':{
                'bool':{
                    'must':[
                        {'term':{'uid':uid}}
                    ]
                }},
                'size':MAX_VALUE
            }

            match_results = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                                    body=match_query_body)['hits']['hits']
	    #print 'match_results..',match_results
            for match_item in match_results:

                match_item = match_item['_source']

                keyword_dict = match_item['keywords_dict']
                mid = match_item['mid']

                keywords_dict = json.loads(keyword_dict)
                personal_keywords_dict = dict()
                classify_text_dict = dict() # 分类文本
                mid_value = dict()
                for k, v in keywords_dict.iteritems():
                    k = k.encode('utf-8', 'ignore')
                    personal_keywords_dict[k] = v
                classify_text_dict[mid] = personal_keywords_dict

                if classify_text_dict:
                    classify_results = topic_classfiy([mid], classify_text_dict)
                
                for k,v in classify_results.iteritems(): # mid:value
                                
                    mid_value[k]=v

                match_item["topic_field_first"] = topic_en2ch_dict[mid_value[mid][0]]
                match_item["topic_field"] = '&'.join(mid_value[mid])
                match_item['xnr_user_no'] = xnr_user_no

                action = {'index':{'_id':mid}}
                source = match_item
                bulk_action.extend([action,source])

                count += 1
                if count%1000 == 0:
                    es_xnr.bulk(bulk_action,index=new_xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,timeout=600)

            if bulk_action:
                es_xnr.bulk(bulk_action,index=new_xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,timeout=600)

    #except:
    #    return 'no tweets to update today'


if __name__ == '__main__':

    match_flow_text()
