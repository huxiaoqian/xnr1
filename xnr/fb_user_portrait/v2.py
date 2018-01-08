#-*- coding: utf-8 -*-
import time
import json
from collections import Counter
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from keyword_extraction import get_filter_keywords
import sys
sys.path.append('../')
from global_config import S_DATE_FB, S_DATE_TW
from global_utils import es_fb_user_portrait as es, \
                         fb_portrait_index_name, fb_portrait_index_type, \
                         facebook_user_index_name, facebook_user_index_type, \
                         facebook_flow_text_index_name_pre, facebook_flow_text_index_type, \
                         fb_bci_index_name_pre, fb_bci_index_type
from time_utils import get_facebook_flow_text_index_list, get_fb_bci_index_list, datetime2ts, ts2datetime
from parameter import MAX_SEARCH_SIZE, FB_TW_TOPIC_ABS_PATH, FB_DOMAIN_ABS_PATH

sys.path.append('../cron')
from trans.trans import trans

sys.path.append(FB_TW_TOPIC_ABS_PATH)
from test_topic import topic_classfiy
from config import name_list, zh_data

sys.path.append(FB_DOMAIN_ABS_PATH)
from domain_classify import domain_main



def merge_dict(x, y):
    for k, v in y.items():
        if k in x.keys():
            x[k] += v
        else:
            x[k] = v
    return x

def load_uid_list():
    uid_list = []
    uid_list_query_body = {'size': MAX_SEARCH_SIZE}
    # uid_list_query_body = {'size': 3}
    try:
        search_results = es.search(index=facebook_user_index_name, doc_type=facebook_user_index_type, body=uid_list_query_body)['hits']['hits']
        for item in search_results:
            uid_list.append(item['_source']['uid'])
    except Exception,e:
        print e
    return uid_list

def load_timestamp(type='test'):
    if type == 'test':
        timestamp =  datetime2ts(S_DATE_FB)
    else:
        timestamp = time.time()
    return timestamp

def save_data2es(data):
    try:
        for uid, d in data.items():
            if es.exists(index=fb_portrait_index_name, doc_type=fb_portrait_index_type, id=uid):
                es.update(index=fb_portrait_index_name, doc_type=fb_portrait_index_type, body={'doc': d}, id=uid)
            else:
                es.index(index=fb_portrait_index_name, doc_type=fb_portrait_index_type, body=d, id=uid)
    except Exception,e:
        print e
        return False
    return True

def update_keywords(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(load_timestamp())
    keywords_query_body = {
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
        "fields": ["keywords_dict", "uid"]
    }
    user_keywords = {}
    for index_name in fb_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=facebook_flow_text_index_type, body=keywords_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_keywords:
                    user_keywords[uid] = {
                        'keywords': {}
                    }
                if content['keywords_dict'][0]:
                    user_keywords[uid]['keywords'] = merge_dict(user_keywords[uid]['keywords'], json.loads(content['keywords_dict'][0]))
        except Exception,e:
            print e

    for uid, content in user_keywords.items():
        temp_keywords = {}
        if len(content['keywords']) >= 50:
            for item in sorted(content['keywords'].items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[:50]:
                temp_keywords[item[0]] = item[1]
        else:
            temp_keywords = content['keywords']
        user_keywords[uid]['keywords'] = json.dumps(temp_keywords)
        user_keywords[uid]['keywords_string'] = '&'.join(temp_keywords.keys())
    return save_data2es(user_keywords)


def update_hashtag(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(load_timestamp())
    keywords_query_body = {
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
        "fields": ["hashtag", "uid"]
    }
    user_hashtag = {}
    for index_name in fb_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=facebook_flow_text_index_type, body=keywords_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_hashtag:
                    user_hashtag[uid] = {
                        'hashtag': {}
                    }
                if content['hashtag'][0]:
                    user_hashtag[uid]['hashtag'] = merge_dict(user_hashtag[uid]['hashtag'], json.loads(content['hashtag'][0]))
        except Exception,e:
            print e

    for uid, content in user_hashtag.items():
        user_hashtag[uid]['hashtag'] = json.dumps(content['hashtag'])
    return save_data2es(user_hashtag)

def update_influence(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    fb_bci_index_list = get_fb_bci_index_list(load_timestamp())
    fb_influence_query_body = {
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
        "fields": ["influence", "uid"]
    }
    user_influence = {}
    for index_name in fb_bci_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=fb_bci_index_type, body=fb_influence_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_influence:
                    user_influence[uid] = {
                        'influence_list': []
                    }
                influence = content.get('influence')[0]
                if influence:
                    user_influence[uid]['influence_list'].append(float(influence))
        except Exception,e:
            print e
    for uid, content in user_influence.items():
        if not sum(content['influence_list']):
            influence = 0.0
        else:
            influence = float(sum(content['influence_list']))/len(content['influence_list'])
        content['influence'] = influence
        content.pop('influence_list')
    return save_data2es(user_influence)

def update_sensitive(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(load_timestamp())
    sensitive_query_body = {
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
        "fields": ["sensitive_words_dict", "sensitive", "uid"]
    }
    user_sensitive = {}
    for index_name in fb_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=facebook_flow_text_index_type, body=sensitive_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_sensitive:
                    user_sensitive[uid] = {
                        'sensitive_dict': {},
                        'sensitive_list': []
                    }
                if content['sensitive_words_dict'][0]:
                    user_sensitive[uid]['sensitive_dict'] = merge_dict(user_sensitive[uid]['sensitive_dict'], json.loads(content['sensitive_words_dict'][0]))
                sensitive = content.get('sensitive')[0]
                if sensitive:
                    user_sensitive[uid]['sensitive_list'].append(float(sensitive))
        except Exception,e:
            print e
    for uid, content in user_sensitive.items():
        user_sensitive[uid]['sensitive_string'] = '&'.join(content['sensitive_dict'].keys())
        user_sensitive[uid]['sensitive_dict'] = json.dumps(content['sensitive_dict'])
        if not sum(content['sensitive_list']):
            sensitive = 0.0
        else:
            sensitive = float(sum(content['sensitive_list']))/len(content['sensitive_list'])
        content['sensitive'] = sensitive
        user_sensitive[uid]['sensitive'] = sensitive
        content.pop('sensitive_list')
    return save_data2es(user_sensitive)

def update_sentiment(uid_list=[]):
    '''
    SENTIMENT_DICT_NEW = {'0':u'中性', '1':u'积极', '2':u'生气', '3':'焦虑', \
         '4':u'悲伤', '5':u'厌恶', '6':u'消极其他', '7':u'消极'}
    '''
    if not uid_list:
        uid_list = load_uid_list()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(load_timestamp())
    sentiment_query_body = {
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
        "fields": ["sentiment", "uid"]
    }
    user_sentiment = {}
    for index_name in fb_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=facebook_flow_text_index_type, body=sentiment_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_sentiment:
                    user_sentiment[uid] = {
                        'sentiment_list': []
                    }
                sentiment = content.get('sentiment')[0]
                if sentiment:
                    user_sentiment[uid]['sentiment_list'].append(int(sentiment))        
        except Exception,e:
            print e
    for uid, content in user_sentiment.items():
        if content['sentiment_list']:
            sentiment = Counter(content['sentiment_list']).most_common(1)[0][0]
        else:
            sentiment = 0
        content['sentiment'] = sentiment
        content.pop('sentiment_list')
    return save_data2es(user_sentiment)


















#未完成
def update_domain(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(load_timestamp())
    user_domain_data = {}
    #load baseinfo
    fb_user_query_body = {
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
        "fields": ["bio", "about", "description", "quotes", "category", "uid"]
    }
    try:
        search_results = es.search(index=facebook_user_index_name, doc_type=facebook_user_index_type, body=fb_user_query_body)['hits']['hits']
        for item in search_results:
            content = item['fields']
            uid = content['uid'][0]
            if not uid in user_domain_data:
                user_domain_data[uid] = {
                    'bio_str': '',
                    'category': '',
                }
            category = content.get('category')[0]
            description = content.get('description')[0]
            quotes = content.get('quotes')[0]
            bio = content.get('bio')[0]
            about = content.get('about')[0]
            if not category:
                category = ''
            if not description:
                description = ''
            if not quotes:
                quotes = ''
            if not bio:
                bio = ''
            if not about:
                about = ''
            user_domain_data[uid] = {
                'bio_str': [quotes, bio, about, description],
                'category': category
            }
    except Exception,e:
        print e
    #load num of text
    textnum_query_body = {
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
        "fields": ["uid"],
    }
    for index_name in fb_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=facebook_flow_text_index_type, body=textnum_query_body)['hits']['hits']
            content = item['fields']
            uid = content['uid'][0]
            if not uid in user_domain_data:
                user_domain_data[uid] = {
                    'number_of_text': 0
                }
            user_domain_data[uid]['number_of_text'] += 1
        except Exception,e:
            print e
    return user_domain_data


def update_baseinfo(uid_list=[]):
    pass






def update_topic(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(load_timestamp())
    get_filter_keywords(fb_flow_text_index_list, uid_list)
    pass


if __name__ == '__main__':
    # print update_keywords(uid_list=['139819436047050'])
    # print update_hashtag(uid_list=['139819436047050'])
    # print update_influence(uid_list=['443835769306299'])
    # print update_sensitive(uid_list=['780790723'])
    # print update_sentiment(uid_list=['100013649473166'])
    print update_domain(uid_list=['139819436047050', '716502715155445'])