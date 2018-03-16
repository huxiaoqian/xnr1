# -*- coding: utf-8 -*-

import os
import sys
from fix_utils import  mkdir_p   #_default_mongo_db,
PRESENT_AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

IS_PROD = 0

if IS_PROD == 1:
    pass
else:
    # 219.224.135.47
    default_topic_name = u'APEC2014'
    default_weibo_topic_name = u'APEC2014-微博'
    default_topic_id = '54916b0d955230e752f2a94e'
    default_news_id = '1-1-30963839'
    default_weibo_news_id = 'weibo'
    default_news_url = 'http://news.sina.com.cn/c/2014-10-09/145630963839.shtml'
    default_subevent_id = '7325a077-76b8-4b03-bbed-d8f0faaf28fd'
    # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    ALLOWED_EXTENSIONS = set(['jl'])
    UPLOAD_FOLDER = '/tmp/upload/'
    RESULT_FOLDER = os.path.join(PRESENT_AB_PATH, './download/comment/')
    LOG_FOLDER = os.path.join(PRESENT_AB_PATH, './log/comment/')
    UPLOAD_WEIBO_FOLDER = '/tmp/upload_weibo/'
    RESULT_WEIBO_FOLDER = os.path.join(PRESENT_AB_PATH, './download/weibo/')
    LOG_WEIBO_FOLDER = os.path.join(PRESENT_AB_PATH, './log/weibo/')
    mkdir_p(UPLOAD_FOLDER)
    mkdir_p(RESULT_FOLDER)
    mkdir_p(UPLOAD_WEIBO_FOLDER)
    mkdir_p(RESULT_WEIBO_FOLDER)
    mkdir_p(LOG_FOLDER)
    mkdir_p(LOG_WEIBO_FOLDER)
    default_task_id = default_topic_id
    default_cluster_num = ''
    CLUSTER_EVA_MIN_SIZE = 5
    COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION = 'v1'
    default_cluster_eva_min_size = CLUSTER_EVA_MIN_SIZE
    default_vsm = COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION


# def get_db_names():
#     results = _default_mongo_db().database_names()
#     return [r for r in results if r.startswith('news')]

# db_names = get_db_names()
# MONGO_DB_NAME = db_names[0]
# EVENTS_COLLECTION = "news_topic"
# SUB_EVENTS_COLLECTION = "news_subevent"
# SUB_EVENTS_FEATURE_COLLECTION = "news_subevent_feature"
# EVENTS_NEWS_COLLECTION_PREFIX = "post_"
# EVENTS_COMMENTS_COLLECTION_PREFIX = "comment_"
# COMMENTS_CLUSTER_COLLECTION = 'comment_cluster'

emotions_vk = {0: '无倾向', 1: '高兴', 2: '愤怒', 3: '悲伤', 4: '新闻'}
emotions_vk_v1 = {0:'中性', 1:'积极', 2:'愤怒', 3:'悲伤'}
emotions_kv = {'happy': 1, 'angry': 2, 'sad': 3, 'news': 4}
emotions_zh_kv = {'happy': '高兴', 'angry': '愤怒', 'sad': '悲伤', 'news': '新闻'}
