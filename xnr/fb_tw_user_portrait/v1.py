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

def load_fb_user_baseinfo(uid_list):
    fb_user = {}
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
        'size': MAX_SEARCH_SIZE
    }
    try:
        search_results = es.search(index=facebook_user_index_name, doc_type=facebook_user_index_type, body=fb_user_query_body)['hits']['hits']
        for item in search_results:
            user = item['_source']
            uname = user.get('username')
            category = user.get('category')
            description = user.get('description')
            quotes = user.get('quotes')
            bio = user.get('bio')
            about = user.get('about')
            if not uname:
                uname = ''
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
            fb_user[user['uid']] = {
                # 'location': user['location'],
                'uname': uname,
                'category': category,
                'description': description,
                'quotes': quotes,
                'bio': bio,
                'about': about
            }
    except Exception,e:
        print e
    #如果没有某个uid对应的记录值，则添上一条空的数据
    fb_user_uid_list = fb_user.keys() 
    for uid in uid_list:
        if not uid in fb_user_uid_list:
            fb_user[uid] = {
                'uname': '',
                'category': '',
                'description': '',
                'quotes': '',
                'bio': '',
                'about': ''
            }
    return fb_user

def load_fb_flow_text(fb_flow_text_index_list, uid_list):
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
                        'number_of_text': 0,
                        'sensitive': [],
                        'sensitive_words_dict': {},
                        'sentiment': [],
                    }
                fb_flow_text[uid]['keywords_dict'] = merge_dict(fb_flow_text[uid]['keywords_dict'], json.loads(content['keywords_dict']))
                fb_flow_text[uid]['number_of_text'] += 1
                fb_flow_text[uid]['sensitive'].append(int(content['sensitive']))
                fb_flow_text[uid]['sensitive_words_dict'] = merge_dict(fb_flow_text[uid]['sensitive_words_dict'], json.loads(content['sensitive_words_dict']))
                fb_flow_text[uid]['sentiment'].append(int(content['sentiment']))
        except Exception,e:
            print e
    #如果没有某个uid对应的记录值，则添上一条空的数据
    fb_flow_text_uid_list = fb_flow_text.keys() 
    for uid in uid_list:
        if not uid in fb_flow_text_uid_list:
            fb_flow_text[uid] = {
                'keywords_dict': {},
                'number_of_text': 0,
                'sensitive': [],
                'sensitive_words_dict': {},
                'sentiment': [],
            }
    return fb_flow_text

def load_fb_bci_data(fb_bci_index_list, uid_list):
    fb_bci_query_body = {
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
    fb_bci_data = {}
    for index_name in fb_bci_index_list:
        try:
            search_results = es.search(index=index_name, doc_type=fb_bci_index_type, body=fb_bci_query_body)['hits']['hits']
            for item in search_results:
                content = item['_source']
                uid = content['uid']
                if not uid in fb_bci_data:
                    fb_bci_data[uid] = {
                        'influence': []
                    }
                influence = content.get('influence')
                if not influence:
                    influence = 0.0
                fb_bci_data[uid]['influence'].append(float(influence))
        except Exception,e:
            print e
    #如果没有某个uid对应的记录值，则添上一条空的数据
    fb_bci_uid_list = fb_bci_data.keys() 
    for uid in uid_list:
        if not uid in fb_bci_uid_list:
            fb_bci_data[uid] = {
                'influence': []
            }
    return fb_bci_data

def load_fb_user_data(fb_flow_text_index_list, fb_bci_index_list):
    #加载数据
    uid_list = load_uid_list()  #[uid1,uid2,uid3,...]
    fb_user_baseinfo = load_fb_user_baseinfo(uid_list)
    fb_flow_text = load_fb_flow_text(fb_flow_text_index_list, uid_list)
    fb_bci_data = load_fb_bci_data(fb_bci_index_list, uid_list)

    #对获取的数据进行初步整合处理，以达到计算方法要求的输入数据类型
    user_keywords_data = {}     #{uid1:{'key1':f1,'key2':f2...}...}
    user_topic_data = {}        #{uid1:{'key1':f1,'key2':f2...}...}
    user_domain_data = {}       #{'uid':{'bio_str':bio_string,'category':category,'number_of_text':number of text}...}    
    user_influence_data = {}    #{'uid':[influence1, influence2, ...], ...}
    user_sentiment_data = {}    #{'uid':[sentiment1, sentiment2, ...], ...}
    user_sensitive_data = {}    #{'uid':{'sensitive': [sensitive1,...], 'sensitive_words_dict': {...}, 'sensitive_words_string': '...'}}

    for uid in uid_list:
        baseinfo = fb_user_baseinfo[uid]
        user_keywords_data[uid] = fb_flow_text[uid]['keywords_dict']
        # bio_str:Facebook用户背景信息中的quotes、bio、about、description，用'_'链接
        #不在这里进行翻译了，所以给bio_str传一个list而非str回去，更容易后续操作
        
        '''
        #繁体
        baseinfo['quotes'] = u''
        baseinfo['bio'] = u''
        baseinfo['about'] = u'新聞、時事、中國內幕、香港台灣新聞、世界新聞、財經、名家點評、生活、教育、時尚、幽默、奇聞異事、娛樂、健康養生 正體：http://b5.secretchina.com/ 簡體：http://www.secretchina.com/'
        baseinfo['description'] = u'全球都在看中國 全球都愛《看中國》'
        #0 1 0 0
        #处理前： 
        #politician
        #0 2 3 0
        #转换后： 
        #mediaworker
        #0 2 3 0
        #翻译后： 
        #mediaworker
        '''

        '''
        #英文
        baseinfo['quotes'] = u''
        baseinfo['bio'] = u''
        baseinfo['about'] = u"中国Advocating for the advancement of democracy and human rights since 2003."
        baseinfo['description'] = u"Asia's first national democracy assistance foundation committed to advancing human rights and democracy in Asia and worldwide."
        #0 0 0 0
        #处理前： 
        #other
        #0 0 0 0
        #转换后： 
        #other
        #0 0 0 1
        #翻译后： 
        #business
        '''

        user_domain_data[uid] = {
            'bio_str': [baseinfo['quotes'], baseinfo['bio'], baseinfo['about'], baseinfo['description']],
            'category': baseinfo['category'],
            'number_of_text': fb_flow_text[uid]['number_of_text']
        }
    for uid, flow_text in fb_flow_text.items():
        user_sentiment_data[uid] = flow_text['sentiment']
        if uid not in user_sensitive_data:
            user_sensitive_data[uid] = {
                'sensitive': flow_text['sensitive'],
                'sensitive_words_dict': flow_text['sensitive_words_dict'],
                'sensitive_words_string': '&'.join(flow_text['sensitive_words_dict'].keys())
            }
    for uid, bci_data in fb_bci_data.items():
        user_influence_data[uid] = bci_data['influence']

    






    user_topic_data = user_keywords_data
    #新建一个filter_keywords在flow_text中？这样效率高吗，毕竟单条的处理不如多条一起处理的快
    #把这块功能单独写到一个文件里？
    #这样的话原始的keywords还要吗？









    return uid_list, user_keywords_data, user_topic_data, user_domain_data, user_influence_data, user_sentiment_data, user_sensitive_data

def compute_domain(users_base_data):
    '''
    ###输入数据：
    user_data用户数据字典：{'uid':{'bio_str':bio_string,'category':category,'number_of_text':number of text}...}
    其中：
    bio_str:Facebook用户背景信息中的quotes、bio、about、description，用'_'链接。注意：有部分内容是英文，需要转换成中文
    category:Facebook用户背景信息中的category
    number_of_text:用户最近7天发帖数量
    ###输出数据：
    user_label用户身份字典:{'uid':label,'uid':label...}
    '''
    user_label = domain_main(users_base_data)

    return user_label

def compute_topic(uid_list, user_filter_keywords):
    '''
    ###输入数据示例：
    uidlist:uid列表（[uid1,uid2,uid3,...]）
    uid_weibo:分词之后的词频字典（{uid1:{'key1':f1,'key2':f2...}...}）
    ###输出数据示例：字典
    1、用户18个话题的分布：
    {uid1:{'art':0.1,'social':0.2...}...}
    2、用户关注较多的话题（最多有3个）：
    {uid1:['art','social','media']...}
    '''

    #转换编码格式
    user_filter_keywords_encode = {}
    for key, val in user_filter_keywords.items():
        key = key.encode('utf8')
        user_filter_keywords_encode[key] = {}
        for k, v in val.items():
            k = k.encode('utf8')
            user_filter_keywords_encode[key][k] = v


    # print 'users_fb_text_encode'
    # print users_fb_text_encode
    user_topic_dict, user_topic_list = topic_classfiy(uid_list, user_filter_keywords_encode)
    # print 'user_topic_dict'
    # print user_topic_dict
    user_topic_string = {}
    for uid, topic_list in user_topic_list.items():
        li = []
        for t in topic_list:
            li.append(zh_data[name_list.index(t)].decode('utf8'))
        user_topic_string[uid] = '&'.join(li)
    print user_topic_string 
    print user_topic_dict
    return user_topic_dict, user_topic_string

def compute_influence(influence_list):
    '''
    计算影响力
    '''
    if influence_list:
        return sum(influence_list)/float(len(influence_list))
    else:
        return 0.0

def compute_sensitive(sensitive_list):
    '''
    计算敏感值以及敏感词
    '''
    if sensitive_list:
        return sum(sensitive_list)/float(len(sensitive_list))
    else:
        return 0.0

def compute_sentiment(sentiment_list):
    '''
    计算情绪值
    '''
    if sentiment_list:
        return Counter(sentiment_list).most_common(1)[0][0]
    else:
        return 0

def compute_attribute(uid_list, user_filter_keywords, user_keywords_data, user_topic_data, user_domain_data, user_influence_data, user_sentiment_data, user_sensitive_data): 
    user_domain = compute_domain(user_domain_data)
    # user_topic_dict, user_topic_string = compute_topic(uid_list, user_topic_data)
    user_topic_dict, user_topic_string = compute_topic(uid_list, user_filter_keywords)

    user_data = {}
    for uid in uid_list:
        user_data[uid] = {
            'domain': user_domain[uid],
            'topic': json.dumps(user_topic_dict[uid]),
            'topic_string': user_topic_string[uid].decode('utf8'),
            'filter_keywords': json.dumps(user_filter_keywords[uid]),  #等flow_text中的filter_keywords计算好以后再说
            # 'keywords': json.dumps(user_keywords_data[uid]),
            'influence': compute_influence(user_influence_data[uid]),
            'sensitive': compute_sensitive(user_sensitive_data[uid]['sensitive']),
            'sentiment': compute_sentiment(user_sentiment_data[uid]),
            # 'keywords_string': '&'.join(user_keywords_data[uid].keys()),
            'sensitive_dict': json.dumps(user_sensitive_data[uid]['sensitive_words_dict']),
            'sensitive_string': user_sensitive_data[uid]['sensitive_words_string'],
        }
    return user_data

def save_compute_result(user_data):
    bulk_action = []
    try:
        for uid, u_data in user_data.items():
            action = {'index':{'_id': uid}}
            bulk_action.extend([action, {'doc': u_data}])
        result = es.bulk(bulk_action, index=fb_portrait_index_name, doc_type=fb_portrait_index_type)
        if result['errors'] :
            print result
            return False
    except Exception,e:
        print e
        return False
    return True

def main(type='RT'):
    if type == 'test':
        timestamp =  datetime2ts(S_DATE_FB)
    else:
        timestamp = time.time()

    
    fb_flow_text_index_list = get_facebook_flow_text_index_list(timestamp)    #获取不包括今天在内的最近7天的表的index_name
    fb_bci_index_list = get_fb_bci_index_list(timestamp)
    
    uid_list, user_keywords_data, user_topic_data, user_domain_data, user_influence_data, user_sentiment_data, user_sensitive_data = load_fb_user_data(fb_flow_text_index_list, fb_bci_index_list)
    


    user_filter_keywords = get_filter_keywords(fb_flow_text_index_list, uid_list)

    user_data = compute_attribute(uid_list, user_filter_keywords, user_keywords_data, user_topic_data, user_domain_data, user_influence_data, user_sentiment_data, user_sensitive_data)
    print save_compute_result(user_data)
    print uid_list
    
if __name__ == '__main__':
    main('test')

