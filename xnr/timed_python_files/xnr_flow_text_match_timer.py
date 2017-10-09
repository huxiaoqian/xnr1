# -*-coding:utf-8-*-

import time
import os
import json
from collections import Counter

import sys
sys.path.append('../')

from global_utils import es_xnr,es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                        xnr_flow_text_index_name_pre,xnr_flow_text_index_type
from global_config import S_TYPE, S_DATE
from weibo_xnr_flow_text_mappings import topic_distribute_tweets_mappings
from time_utils import ts2datetime,datetime2ts
from parameter import MAX_VALUE,topic_en2ch_dict
from timed_python_files.text_classify.test_topic import topic_classfiy

def match_flow_text():

    current_time = int(time.time())
    current_date = ts2datetime(current_time)

    xnr_flow_text_index_name = xnr_flow_text_index_name_pre + current_date
    flow_text_index_name = flow_text_index_name_pre + current_date

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'mid':''}
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        search_results = es_xnr.search(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,\
                            body=query_body)['hits']['hits']

        for result in search_results:
            _id = result['_id']
            result = result['_source']
            text = result['text']
            uid = result['uid']

            match_query_body = {
                'bool':{
                    'must':[
                        {'term':{'uid':uid}},
                        {'term':{'text':text}}
                    ]
                },
                'sort':{'timestamp':{'order':'desc'}}
            }

            match_results = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                                    body=match_query_body)['hits']['hits']

            match_item = match_results[0]['_source']

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

            match_item["topic_field_first"] = topic_en2ch_dict(mid_value[mid][0])
            match_item["topic_field"] = '&'.join(mid_value[mid])

            es_xnr.update(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,\
                id=_id,body={'doc':match_item})

    except:
        return 'no tweets to update today'


if __name__ == '__main__':

    match_flow_text()