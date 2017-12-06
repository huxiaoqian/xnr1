#-*- coding: utf-8 -*-
import time
import json
import sys
sys.path.append('../')
from global_config import S_DATE_FB, S_DATE_TW
from global_utils import es_fb_user_portrait as es, \
                         fb_portrait_index_name, fb_portrait_index_type, \
                         facebook_user_index_name, facebook_user_index_type, \
                         facebook_flow_text_index_name_pre, facebook_flow_text_index_type
from time_utils import get_facebook_flow_text_index_list, datetime2ts, ts2datetime
from parameter import MAX_SEARCH_SIZE, FB_TW_TOPIC_ABS_PATH, FB_DOMAIN_ABS_PATH
from trans.trans import trans

sys.path.append(FB_TW_TOPIC_ABS_PATH)
from test_topic import topic_classfiy

sys.path.append(FB_DOMAIN_ABS_PATH)
from domain_classify import domain_main


def load_fb_user_baseinfo():
    fb_user = {}
    # fb_user_query_body = {'size': MAX_SEARCH_SIZE}
    fb_user_query_body = {'size': 3}
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
                        'number_of_text': 0
                    }
                fb_flow_text[uid]['keywords_dict'] = merge_dict(fb_flow_text[uid]['keywords_dict'], json.loads(content['keywords_dict']))
                fb_flow_text[uid]['number_of_text'] += 1
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

def load_fb_user_data(fb_user_baseinfo, fb_flow_text):
    uid_list = []          #[uid1,uid2,uid3,...]
    users_fb_text = {}  #{uid1:{'key1':f1,'key2':f2...}...}
    users_data = {}     #{'uid':{'bio_str':bio_string,'category':category,'number_of_text':number of text}...}
    for uid, baseinfo in fb_user_baseinfo.items():
        uid_list.append(uid)
        users_fb_text[uid] = fb_flow_text[uid]['keywords_dict']
        # bio_str:Facebook用户背景信息中的quotes、bio、about、description，用'_'链接
        bio_str = '_'.join(trans([baseinfo['quotes'], baseinfo['bio'], baseinfo['about'], baseinfo['description']]))
        if not bio_str:
            print 'translate error', uid
            bio_str = u'\u9519\u8bef_\u9519\u8bef_\u9519\u8bef_\u9519\u8bef'
        users_data[uid] = {
            'bio_str': bio_str,
            'category': baseinfo['category'],
            'number_of_text': fb_flow_text[uid]['number_of_text']
        }
    return uid_list, users_fb_text, users_data

def compute_domain(users_data):
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
    user_label = domain_main(users_data)
    return user_label

def compute_topic(users_fb_text, users_data):
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
    users_fb_text_encode = {}
    for key, val in users_fb_text.items():
        key = key.encode('utf8')
        users_fb_text_encode[key] = {}
        for k, v in val.items():
            k = k.encode('utf8')
            users_fb_text_encode[key][k] = v
    topic_result_data, uid_topic = topic_classfiy(uid_list, users_fb_text_encode)
    return topic_result_data, uid_topic

def compute_attribute(uid_list, users_fb_text, users_data):
    user_label = compute_domain(users_data)
    topic_result_data, uid_topic = compute_topic(users_fb_text, users_data)
    

    return topic_result_data, uid_topic, user_label

def save_compute_result(result_data, uid_topic, user_label):
    print 'result_data: '
    print result_data
    print 'uid_topic'
    print uid_topic
    print 'user_label'
    print user_label
    '''
    注意重复用户
    记录id用uid
    '''



def main(type='RT'):
    if type == 'test':
        timestamp =  datetime2ts(S_DATE_FB)
    else:
        timestamp = time.time()

    fb_user_baseinfo = load_fb_user_baseinfo()
    fb_flow_text_index_list = get_facebook_flow_text_index_list(timestamp)    #获取不包括今天在内的最近7天的表的index_name
    fb_flow_text = load_fb_flow_text(fb_flow_text_index_list, fb_user_baseinfo.keys())
    uid_list, users_fb_text, users_data = load_fb_user_data(fb_user_baseinfo, fb_flow_text)
    result_data, uid_topic, user_label = compute_attribute(uid_list, users_fb_text, users_data)
    save_compute_result(result_data, uid_topic, user_label)

if __name__ == '__main__':
    main('test')

