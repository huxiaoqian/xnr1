#-*- coding: utf-8 -*-
import time
import json
from collections import Counter
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from keyword_extraction import get_filter_keywords
import sys
sys.path.append('../')
from global_config import S_DATE_FB, S_DATE_TW
from global_utils import es_tw_user_portrait as es, \
                         tw_portrait_index_name, tw_portrait_index_type, \
                         twitter_user_index_name, twitter_user_index_type, \
                         twitter_flow_text_index_name_pre, twitter_flow_text_index_type, \
                         tw_bci_index_name_pre, tw_bci_index_type
from time_utils import get_twitter_flow_text_index_list, get_tw_bci_index_list, datetime2ts, ts2datetime
from parameter import MAX_SEARCH_SIZE, FB_TW_TOPIC_ABS_PATH, TW_DOMAIN_ABS_PATH, DAY, WEEK

sys.path.append('../cron/trans/')
from trans import trans

sys.path.append(FB_TW_TOPIC_ABS_PATH)
from test_topic import topic_classfiy
from config import name_list, zh_data

sys.path.append(TW_DOMAIN_ABS_PATH)
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
    try:
        search_results = es.search(index=twitter_user_index_name, doc_type=twitter_user_index_type, body=uid_list_query_body)['hits']['hits']
        for item in search_results:
            uid_list.append(item['_source']['uid'])
    except Exception,e:
        print e
    return uid_list

def load_timestamp(type='test'):
    if type == 'test':
        timestamp =  datetime2ts(S_DATE_TW)
    else:
        timestamp = time.time()
    return timestamp

def save_data2es(data):
    update_uid_list = []
    create_uid_list = []
    try:
        for uid, d in data.items():
            if es.exists(index=tw_portrait_index_name, doc_type=tw_portrait_index_type, id=uid):
                update_uid_list.append(uid)
            else:
                create_uid_list.append(uid)
        #bulk create
        bulk_create_action = []
        if create_uid_list:
            for uid in create_uid_list:
                create_action = {'index':{'_id': uid}}
                bulk_create_action.extend([create_action, data[uid]])
            result = es.bulk(bulk_create_action, index=tw_portrait_index_name, doc_type=tw_portrait_index_type)
            if result['errors'] :
                print result
                return False
        #bulk update
        if update_uid_list:
            bulk_update_action = []
            for uid in update_uid_list:
                update_action = {'update':{'_id': uid}}
                bulk_update_action.extend([update_action, {'doc': data[uid]}])
            result = es.bulk(bulk_update_action, index=tw_portrait_index_name, doc_type=tw_portrait_index_type)
            if result['errors'] :
                print result
                return False
    except Exception,e:
        print e
        return False
    return True

def update_keywords(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    tw_flow_text_index_list = get_twitter_flow_text_index_list(load_timestamp())
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
    for index_name in tw_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=twitter_flow_text_index_type, body=keywords_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_keywords:
                    user_keywords[uid] = {
                        'keywords': {}
                    }
                if content.has_key('keywords_dict'):
                    user_keywords[uid]['keywords'] = merge_dict(user_keywords[uid]['keywords'], json.loads(content['keywords_dict'][0]))
        except Exception,e:
            print e
    for uid in uid_list:
        if uid in user_keywords:
            content = user_keywords[uid]
            temp_keywords = {}
            if len(content['keywords']) >= 50:
                for item in sorted(content['keywords'].items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[:50]:
                    temp_keywords[item[0]] = item[1]
            else:
                temp_keywords = content['keywords']
            user_keywords[uid]['keywords'] = json.dumps(temp_keywords)
            user_keywords[uid]['keywords_string'] = '&'.join(temp_keywords.keys())
        else:
            user_keywords[uid] = {
                'keywords': json.dumps({}),
                'keywords_string': ''   
            }
    return save_data2es(user_keywords)

def update_hashtag(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    tw_flow_text_index_list = get_twitter_flow_text_index_list(load_timestamp())
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
    for index_name in tw_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=twitter_flow_text_index_type, body=keywords_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_hashtag:
                    user_hashtag[uid] = {
                        'hashtag_list': []
                    }
                if content.has_key('hashtag'):
                    hashtag = content['hashtag'][0]
                    if hashtag:
                        hashtag_list = hashtag.split('&') 
                        user_hashtag[uid]['hashtag_list'].extend(hashtag_list)
        except Exception,e:
            print e
    for uid in uid_list:
        if uid in user_hashtag:
            content = user_hashtag[uid]
            hashtag_list = user_hashtag[uid]['hashtag_list']
            user_hashtag[uid] = {
                'hashtag': '&'.join(list(set(hashtag_list)))
            }
        else:
            user_hashtag[uid] = {
                'hashtag': ''
            }
    return save_data2es(user_hashtag)


def update_sentiment(uid_list=[]):
    '''
    SENTIMENT_DICT_NEW = {'0':u'中性', '1':u'积极', '2':u'生气', '3':'焦虑', \
         '4':u'悲伤', '5':u'厌恶', '6':u'消极其他', '7':u'消极'}
    '''
    if not uid_list:
        uid_list = load_uid_list()
    tw_flow_text_index_list = get_twitter_flow_text_index_list(load_timestamp())
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
    for index_name in tw_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=twitter_flow_text_index_type, body=sentiment_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_sentiment:
                    user_sentiment[uid] = {
                        'sentiment_list': []
                    }
                if content.has_key('sentiment'):
                    user_sentiment[uid]['sentiment_list'].append(int(content.get('sentiment')[0]))        
        except Exception,e:
            print e
    for uid in uid_list:
        if uid in user_sentiment:
            content = user_sentiment[uid]
            if content['sentiment_list']:
                sentiment = Counter(content['sentiment_list']).most_common(1)[0][0]
            else:
                sentiment = 0
            content['sentiment'] = sentiment
            content.pop('sentiment_list')
        else:
            user_sentiment[uid] = {
                'sentiment': 0
            }
    return save_data2es(user_sentiment)

def update_influence(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    tw_bci_index_list = get_tw_bci_index_list(load_timestamp())
    tw_influence_query_body = {
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
    for index_name in tw_bci_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=tw_bci_index_type, body=tw_influence_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_influence:
                    user_influence[uid] = {
                        'influence_list': []
                    }
                if content.has_key('influence'):
                    user_influence[uid]['influence_list'].append(float(content.get('influence')[0]))
        except Exception,e:
            print e
    for uid in uid_list:
        if uid in user_influence:
            content = user_influence[uid]
            if not sum(content['influence_list']):
                influence = 0.0
            else:
                influence = float(sum(content['influence_list']))/len(content['influence_list'])
            content['influence'] = influence
            content.pop('influence_list')
        else:
            user_influence[uid] = {
                'influence': 0.0
            } 
    return save_data2es(user_influence)

def update_sensitive(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    tw_flow_text_index_list = get_twitter_flow_text_index_list(load_timestamp())
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
    for index_name in tw_flow_text_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=twitter_flow_text_index_type, body=sensitive_query_body)['hits']['hits']
            for item in search_results:
                content = item['fields']
                uid = content['uid'][0]
                if not uid in user_sensitive:
                    user_sensitive[uid] = {
                        'sensitive_dict': {},
                        'sensitive_list': []
                    }
                if content.has_key('sensitive_words_dict'):
                    user_sensitive[uid]['sensitive_dict'] = merge_dict(user_sensitive[uid]['sensitive_dict'], json.loads(content['sensitive_words_dict'][0]))
                if content.has_key('sensitive'):
                    user_sensitive[uid]['sensitive_list'].append(float(content.get('sensitive')[0]))
        except Exception,e:
            print e
    for uid in uid_list:
        if uid in user_sensitive:
            content = user_sensitive[uid]
            user_sensitive[uid]['sensitive_string'] = '&'.join(content['sensitive_dict'].keys())
            user_sensitive[uid]['sensitive_dict'] = json.dumps(content['sensitive_dict'])
            if not sum(content['sensitive_list']):
                sensitive = 0.0
            else:
                sensitive = float(sum(content['sensitive_list']))/len(content['sensitive_list'])
            content['sensitive'] = sensitive
            user_sensitive[uid]['sensitive'] = sensitive
            content.pop('sensitive_list')
        else:
            user_sensitive[uid] = {
                'sensitive': 0,
                'sensitive_string': '',
                'sensitive_dict': json.dumps({})

            }
    return save_data2es(user_sensitive)

def count_text_num(uid_list, tw_flow_text_index_list):
    count_result = {}
    #QQ那边好像就是按照用户来count的    https://github.com/huxiaoqian/xnr1/blob/82ff9704792c84dddc3e2e0f265c46f3233a786f/xnr/qq_xnr_manage/qq_history_count_timer.py
    for uid in uid_list:
        textnum_query_body = {
            'query':{
                "filtered":{
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"uid": uid}},
                            ]
                         }
                    }
                }
            }
        }
        text_num = 0
        for index_name in tw_flow_text_index_list:
            result = es.count(index=index_name, doc_type=twitter_flow_text_index_type, body=textnum_query_body)
            if result['_shards']['successful'] != 0:
                text_num += result['count']
        count_result[uid] = text_num
    return count_result

def trans_bio_data(bio_data):
    count = 1.0
    while True:
        translated_bio_data = trans(bio_data)
        if len(translated_bio_data) == len(bio_data):
            break
        else:
            print 'sleep start ...'
            time.sleep(count)
            count = count*1.1
            print 'sleep over ...'
    return translated_bio_data
    
def update_domain(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    tw_flow_text_index_list = get_twitter_flow_text_index_list(load_timestamp())
    user_domain_data = {}
    #load num of text
    count_result = count_text_num(uid_list, tw_flow_text_index_list)
    #load baseinfo
    tw_user_query_body = {
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
        "fields": ["location", "username", "description", "uid"]
    }
    try:
        search_results = es.search(index=twitter_user_index_name, doc_type=twitter_user_index_type, body=tw_user_query_body)['hits']['hits']
        for item in search_results:
            content = item['fields']
            uid = content['uid'][0]
            if not uid in user_domain_data:
                text_num = count_result[uid]
                user_domain_data[uid] = {
                    'location': '',
                    'username': '',
                    'description': '',
                    'number_of_text': text_num
                }
            if content.has_key('location'):
                location = content.get('location')[0]
            else:
                location = ''
            if content.has_key('description'):
                description = content.get('description')[0][:1000]
            else:
                description = ''
            if content.has_key('username'):
                username = content.get('username')[0]
            else:
                username = '' 
            user_domain_data[uid]['location'] = location
            user_domain_data[uid]['username'] = username
            user_domain_data[uid]['description'] = description
    except Exception,e:
        print e
    #由于一个用户请求一次翻译太耗时，所以统一批量翻译
    trans_uid_list = []
    untrans_bio_data = []
    cut = 100
    n = len(user_domain_data)/cut
    for uid, content in user_domain_data.items():
        trans_uid_list.append(uid)
        untrans_bio_data.extend([content['location'] ,content['description']])
        if n:
            if len(trans_uid_list)%cut == 0:
                temp_trans_bio_data = trans_bio_data(untrans_bio_data)
                for i in range(len(trans_uid_list)):
                    uid = trans_uid_list[i]
                    user_domain_data[uid]['location'] = '_'.join(temp_trans_bio_data[2*i])
                    user_domain_data[uid]['description'] = '_'.join(temp_trans_bio_data[2*i+1])
                trans_uid_list = []
                untrans_bio_data = []
                n = n - 1
        else:
            if len(trans_uid_list) == (len(user_domain_data)%cut):
                temp_trans_bio_data = trans_bio_data(untrans_bio_data)
                for i in range(len(trans_uid_list)):
                    uid = trans_uid_list[i]
                    user_domain_data[uid]['location'] = '_'.join(temp_trans_bio_data[2*i])
                    user_domain_data[uid]['description'] = '_'.join(temp_trans_bio_data[2*i+1])
                trans_uid_list = []
                untrans_bio_data = []
    #domian计算         
    user_domain_temp = domain_main(user_domain_data)    
    user_domain = {}
    for uid in uid_list:
        if uid in user_domain_temp:
            user_domain[uid] = {
                'domain': user_domain_temp[uid]
            }
        else:
            user_domain[uid] = {'domain': 'other'}
    return save_data2es(user_domain)

def update_topic(uid_list=[]):
    if not uid_list:
        uid_list = load_uid_list()
    tw_flow_text_index_list = get_twitter_flow_text_index_list(load_timestamp())
    user_topic_data = get_filter_keywords(tw_flow_text_index_list, uid_list)
    user_topic_dict, user_topic_list = topic_classfiy(uid_list, user_topic_data)

    user_topic_string = {}
    for uid, topic_list in user_topic_list.items():
        li = []
        for t in topic_list:
            li.append(zh_data[name_list.index(t)].decode('utf8'))
        user_topic_string[uid] = '&'.join(li)
    user_topic = {}
    for uid in uid_list:
        if uid in user_topic_dict:
            user_topic[uid] = {
                'filter_keywords': json.dumps(user_topic_data[uid]),
                'topic': json.dumps(user_topic_dict[uid]),
                'topic_string': user_topic_string[uid]
            }
        else:
            user_topic[uid] = {
                'filter_keywords': json.dumps({}),
                'topic': json.dumps({}),
                'topic_string': ''
            }
    return save_data2es(user_topic)

def update_baseinfo(uid_list=[]):
    user_baseinfo = {}
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
        "fields": ["location", "original_profile_image_url", "followers_count", "status_count", "followers_count", "friends_count", "is_verified", "username", "uid"]
    }
    search_results = es.search(index=twitter_user_index_name, doc_type=twitter_user_index_type, body=fb_user_query_body)['hits']['hits']
    for item in search_results:
        content = item['fields']
        uid = content['uid'][0]
        if not uid in user_baseinfo:
            user_baseinfo[uid] = {
                'uid': str(uid),
                'uname': '',
                'location': '',
                'verified':'',
                'statusnum': 0,
                'friendsnum': 0,
                'fansnum': 0,
                'photo_url': '',
            }
        location = ''
        if content.has_key('location'):
            location = content.get('location')[0]
        uname = ''
        if content.has_key('username'):
            uname = content.get('username')[0]
        photo_url = ''
        if content.has_key('original_profile_image_url'):
            photo_url = content.get('original_profile_image_url')[0]
        verified = ''
        if content.has_key('is_verified'):
            verified = str(content.get('is_verified')[0])
        statusnum = ''
        if content.has_key('status_count'):
            statusnum = content.get('status_count')[0]
        friendsnum = ''
        if content.has_key('friends_count'):
            friendsnum = content.get('friends_count')[0]
        fansnum = ''
        if content.has_key('followers_count'):
            fansnum = content.get('followers_count')[0]

        user_baseinfo[uid]['location'] = location
        user_baseinfo[uid]['uname'] = uname
        user_baseinfo[uid]['photo_url'] = photo_url
        user_baseinfo[uid]['verified'] = verified
        user_baseinfo[uid]['statusnum'] = statusnum
        user_baseinfo[uid]['friendsnum'] = friendsnum
        user_baseinfo[uid]['fansnum'] = fansnum
    for uid in uid_list:
        if not uid in user_baseinfo:
            user_baseinfo[uid] = {
                'uid': str(uid),
                'uname': '',
                'location': '',
                'verified':'',
                'statusnum': 0,
                'friendsnum': 0,
                'fansnum': 0,
                'photo_url': '',
            }
    return save_data2es(user_baseinfo)

def update_all():
    time_list = []
    time_list.append(time.time())

    uid_list = load_uid_list()
    print 'total num: ', len(uid_list)
    time_list.append(time.time())
    print 'time used: ', time_list[-1] - time_list[-2]

    #日更新
    print 'update_influence: ', update_influence(uid_list)
    time_list.append(time.time())
    print 'time used: ', time_list[-1] - time_list[-2]

    print 'update_hashtag: ', update_hashtag(uid_list)
    time_list.append(time.time())
    print 'time used: ', time_list[-1] - time_list[-2]

    print 'update_sensitive: ', update_sensitive(uid_list)
    time_list.append(time.time())
    print 'time used: ', time_list[-1] - time_list[-2]



    print 'update_sentiment: ', update_sentiment(uid_list)
    time_list.append(time.time())
    print 'time used: ', time_list[-1] - time_list[-2]


    #周更新
    if not ((datetime2ts(ts2datetime(time.time())) - datetime2ts(S_DATE_TW)) % (WEEK*DAY)):
        print 'update_domain: ', update_domain(uid_list)
        time_list.append(time.time())
        print 'time used: ', time_list[-1] - time_list[-2]

        print 'update_sentiment: ', update_sentiment(uid_list)
        time_list.append(time.time())
        print 'time used: ', time_list[-1] - time_list[-2]

        print 'update_topic: ', update_topic(uid_list)
        time_list.append(time.time())
        print 'time used: ', time_list[-1] - time_list[-2]

        print 'update_keywords:', update_keywords(uid_list)
        time_list.append(time.time())
        print 'time used: ', time_list[-1] - time_list[-2]

if __name__ == '__main__':
    # update_all()
    update_baseinfo(load_uid_list())
    
