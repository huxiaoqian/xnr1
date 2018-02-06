#-*-coding=utf-8-*-
"""默认参数配置文件, 不要修改，可以修改settings.py，以覆盖default_settings
   default_settings.py
"""

# Database.py
MONGOD_PORT = 27017
MONGOD_HOST = 'localhost'

MONGO_DB_NAME = 'news'

EVENTS_COLLECTION = 'news_topic'
SUB_EVENTS_COLLECTION = 'news_subevent'
SUB_EVENTS_FEATURE_COLLECTION = 'news_subevent_feature'
EVENTS_NEWS_COLLECTION_PREFIX = 'post_'
EVENTS_COMMENTS_COLLECTION_PREFIX = 'comment_'
COMMENTS_CLUSTER_COLLECTION = 'comment_cluster'

# ad_filter.py
MARKET_WORDS = 'market_words.txt'

# classify_mid_weibo.py
HAPPY_WORDS = './words/happy.txt'
ANGRY_WORDS = './words/angry.txt'
SAD_WORDS = './words/sad.txt'

# clustering.py
CLUSTERING_CLUTO_FOLDER = 'cluto'
CLUSTERING_CLUTO_EXECUTE_PATH = './cluto-2.1.2/Linux-i686/vcluster'
CLUSTERING_KMEANS_CLUSTERING_NUM = 10
CLUSTERING_TOPK_FREQ_WORD = 20 # 计算每类tfidf词前，选取的高频词的数量
CLUSTERING_CLUSTER_EVA_TOP_NUM = 5 # 聚类评价时保留的聚类数
CLUSTERING_CLUSTER_EVA_LEAST_FREQ = 10 # 
CLUSTERING_CLUSTER_EVA_LEAST_SIZE = 8 #

# comment_clustering_tfidf_v7
MIN_CLUSTER_NUM = 2
MAX_CLUSTER_NUM = 15
COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION = 'v1'
COMMENT_CLUSTERING_PROCESS_GRAM = 3
COMMENT_CLUSTERING_CLUSTER_EVA_MIN_SIZE = 5
WORD_LIST_TOP_PERCENT = 0.2

# feature.py
FEATURE_TFIDF_TOPK = 100 #
FEATURE_TITLE_TERM_WEIGHT = 5 #
FEATURE_CONTENT_TERM_WEIGHT = 1 #

# rubbish_classifier.py
RUBBISH_BATCH_COUNT = 1000

# utils.py
CUT_BLACK_WORDS = 'black.txt'

# comment_module.py
CLUSTER_EVA_MIN_SIZE = 5
COMMENT_WORDS_CLUSTER_NUM = 10
LOG_FILE = 'log.txt'

