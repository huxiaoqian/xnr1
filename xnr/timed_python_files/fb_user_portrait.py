#-*- coding: utf-8 -*-
import time
import sys
sys.path.append('../')
from global_config import S_DATE_FB, S_DATE_TW
from global_utils import es_fb_user_portrait as es, \
                         fb_portrait_index_name, fb_portrait_index_type, \
                         facebook_user_index_name, facebook_user_index_type, \
                         facebook_flow_text_index_name_pre, facebook_flow_text_index_type
from time_utils import get_facebook_flow_text_index_list, datetime2ts, ts2datetime
from parameter import MAX_SEARCH_SIZE

def load_fb_user():
    fb_user = {}
    # fb_user_query_body = {'size': MAX_SEARCH_SIZE}
    fb_user_query_body = {'size': 3}
    try:
        search_results = es.search(index=facebook_user_index_name, doc_type=facebook_user_index_type, body=fb_user_query_body)['hits']['hits']
        for item in search_results:
            user = item['_source']
            fb_user[user['uid']] = {
                # 'location': user['location'],
                'uname': user['username'],
            }
    except Exception,e:
        print e
    return fb_user

def load_fb_flow_text(fb_flow_text_index_list, uid_list):
    print uid_list
    fb_flow_text_query_body = {
        'query':{
            "filtered":{
                "filter": {
                    "bool": {
                        "must": [
                            {"terms": {"uid": uid_list}},
                        ]
                     }
                }
            }
        },
        'size': MAX_SEARCH_SIZE,
        "sort": {"timestamp": {"order": "desc"}},
    }
    fb_flow_text = {}
    for index_name in fb_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=facebook_flow_text_index_type, body=fb_flow_text_query_body)['hits']['hits']
            for item in search_results:
                content = item['_source']
                uid = content['uid']
                if not uid in fb_flow_text:
                    fb_flow_text[uid] = {
                        'keywords_dict': {},
                        
                    }

                fb_flow_text[content['uid']] = {
                    'uname': user['username'],
                }

        except Exception,e:
            print e
    return fb_flow_text

def merge_dict(x, y):
    for k, v in y.items():
        if k in x.keys():
            x[k] += v
        else:
            x[k] = v
    return x

def compute_attribute():
    pass

def save_compute_result():
    pass

def main(type='RT'):
    if type == 'test':
        timestamp =  datetime2ts(S_DATE_FB)
    else:
        timestamp = time.time()
    fb_user = load_fb_user()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(timestamp)    #获取不包括今天在内的最近7天的表的index_name
    fb_flow_text = load_fb_flow_text(fb_flow_text_index_list, fb_user.keys())
    compute_attribute()
    save_compute_result()

if __name__ == '__main__':
    main('test')

