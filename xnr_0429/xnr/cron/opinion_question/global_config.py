# -*-coding:utf-8-*-

import re
import time
from elasticsearch import Elasticsearch

user_profile_host = ["219.224.134.216:9201"]
user_portrait_host = ["219.224.134.216:9201"]
flow_text_host = ["219.224.134.216:9201"]

profile_index_name = "weibo_user"
profile_index_type = "user"
portrait_name = "user_portrait_ys"#知识图谱 user protrait
flow_text_index_name_pre = "flow_text_"
portrait_type = "user"
flow_text_index_type = "text"

# retweet&comment for test
retweet_comment_es_host = ['219.224.134.216:9201']
retweet_comment_port = "9201"
# week retweet/be_retweet relation es
retweet_index_name_pre = '1225_retweet_' # retweet: 'retweet_1' or 'retweet_2'
retweet_index_type = 'user'
be_retweet_index_name_pre = '1225_be_retweet_' #be_retweet: 'be_retweet_1'/'be_retweet_2'
be_retweet_index_type = 'user'
# week comment/be_comment relation es
comment_index_name_pre = '1225_comment_'
comment_index_type = 'user'
be_comment_index_name_pre = '1225_be_comment_'
be_comment_index_type = 'user'


domain_list = [u'高校', u'境内机构', u'境外机构', u'媒体', u'境外媒体', u'民间组织', u'法律机构及人士', \
        u'政府机构及人士', u'媒体人士', u'活跃人士', u'草根', u'其他', u'商业人士']
topic_list = [u'文体类_娱乐', u'科技类', u'经济类', u'教育类', u'民生类_环保', \
        u'民生类_健康', u'军事类', u'政治类_外交', u'文体类_体育', u'民生类_交通', \
        u'其他类', u'政治类_反腐', u'民生类_就业', u'政治类_暴恐', u'民生类_住房', \
        u'民生类_法律', u'政治类_地区和平', u'政治类_宗教', u'民生类_社会保障']

text_data_list = ['2016-11-11','2016-11-12','2016-11-13','2016-11-14','2016-11-15','2016-11-16',\
             '2016-11-17','2016-11-18','2016-11-19','2016-11-20','2016-11-21','2016-11-22','2016-11-23','2016-11-24','2016-11-25','2016-11-26',\
             '2016-11-27']

#topic en2ch dict
topic_en2ch_dict = {'art':u'文体类_娱乐','computer':u'科技类','economic':u'经济类', \
           'education':u'教育类','environment':u'民生类_环保', 'medicine':u'民生类_健康',\
           'military':u'军事类','politics':u'政治类_外交','sports':u'文体类_体育',\
           'traffic':u'民生类_交通','life':u'其他类','anti-corruption':u'政治类_反腐',\
           'employment':u'民生类_就业','fear-of-violence':u'政治类_暴恐',\
           'house':u'民生类_住房','law':u'民生类_法律','peace':u'政治类_地区和平',\
           'religion':u'政治类_宗教','social-security':u'民生类_社会保障'}

#domain en2ch dict
domain_en2ch_dict = {'university':u'高校', 'homeadmin':u'境内机构', 'abroadadmin':u'境外机构', \
                     'homemedia':u'媒体', 'abroadmedia':u'境外媒体', 'folkorg':u'民间组织',\
                     'lawyer':u'法律机构及人士', 'politician':u'政府机构及人士', 'mediaworker':u'媒体人士',\
                     'activer':u'活跃人士', 'grassroot':u'草根', 'other':u'其他', 'business':u'商业人士'}

es_user_portrait = Elasticsearch(user_portrait_host, timeout=600)
es_flow_text = Elasticsearch(flow_text_host, timeout=600)
es_user_profile = Elasticsearch(user_profile_host, timeout=600)
es_retweet = Elasticsearch(retweet_comment_es_host, timeout=600)
es_comment = Elasticsearch(retweet_comment_es_host, timeout = 600)
be_es_retweet = Elasticsearch(retweet_comment_es_host, timeout=600)
be_es_comment = Elasticsearch(retweet_comment_es_host, timeout = 600)

ES_INTELLIGENT_HOST = ['192.168.169.45:9205','192.168.169.46:9205','192.168.169.47:9205']
#['219.224.134.213:9205', '219.224.134.214:9205',\
#                   '219.224.134.215:9205']
ES_INTELLIGENT_PORT = '9205'

ES_CLUSTER_HOST = ['192.168.169.45:9205','192.168.169.46:9205','192.168.169.47:9205']
#['219.224.134.213:9205', '219.224.134.214:9205',\
#                   '219.224.134.215:9205']
ES_CLUSTER_PORT = '9205'
#config flow text info
ES_FLOW_TEXT_HOST = ['10.128.55.75:9200','10.128.55.76:9200']
#['219.224.134.216:9201', \
#                          '219.224.134.214:9201']
ES_FLOW_TEXT_PORT = '9200' #'9201'

# need three ES identification
USER_PROFILE_ES_HOST = ['10.128.55.81:9200','10.128.55.82:9200','10.128.55.83:9200']
#['219.224.134.216:9201', \
#                          '219.224.134.214:9201']
USER_PROFILE_ES_PORT = '9200' #'9201'

#config user portrat
ES_USER_PORTRAIT_HOST = ['10.128.55.69:9200','10.128.55.70:9200','10.128.55.71:9200']
#['219.224.134.216:9201', \
#                     '219.224.134.214:9201']
ES_USER_PORTRAIT_PORT = '9200' #'9201'


#es_path
ES_PATH = '/home/pkgs/elasticsearch-1.6.0/' #'/home/ubuntu8/huxiaoqian/elasticsearch-1.6.0/'

#config redis

REDIS_HOST_45 = '192.168.169.45'
REDIS_PORT_45 = '6666'

REDIS_HOST_46 = '192.168.169.46' #'219.224.134.212'
REDIS_PORT_46 = '6666' #'7392'

REDIS_HOST_47 = '192.168.169.47'
REDIS_PORT_47 = ''

REDIS_HOST_NEW = ''
REDIS_PORT_NEW = ''

REDIS_CLUSTER_HOST_FLOW2 = '10.128.55.68' #'219.224.134.213'
REDIS_CLUSTER_PORT_FLOW2 = '6666'

#redis_path
REDIS_PATH = '/home/pkgs/redis-3.0.5/6666' #'/home/ubuntu7/huxiaoqian/redis-3.0.5/7392/'



# use to identify the db number of redis-97
R_BEGIN_TIME = '2016-03-21'

##　 weibo敏感词redis
REDIS_CLUSTER_HOST_FLOW3 = '219.224.134.214' #'10.128.55.71'
REDIS_CLUSTER_PORT_FLOW3 = '6379'

REDIS_HOST_SENSITIVE = '10.128.55.68'
REDIS_PORT_SENSITIVE = '6379'

#wx redis
REDIS_WX_PORT = '6667'
REDIS_WX_HOST = '192.168.169.45'#'219.224.134.213'

#flow3:retweet/be_retweet redis
RETWEET_REDIS_HOST = '10.128.55.69'
RETWEET_REDIS_PORT = '6379'
#flow3:comment/be_comment redis
COMMENT_REDIS_HOST = '10.128.55.70'
COMMENT_REDIS_PORT = '6379'


#使用七牛来存储捕获到的图片
#2018-1-2 放弃使用七牛，改为存储到本地
qiniu_access_key = "2QHQTgGYH8Ow3dy1jpuSKLAlTo-ZkRav1ty2Nok8"
qiniu_secret_key = "Q91z6hnj5H0LaRkbAN8IPdc8dypdAQ_n21S8tEcu"
qiniu_bucket_name = "publicbucket"
qiniu_bucket_domain = "ovorc2c4c.bkt.clouddn.com"

#微信多媒体数据存放地址
WX_IMAGE_ABS_PATH = '/home/xnr1/xnr_0429/xnr/static/WX/image'
WX_VOICE_ABS_PATH = '/home/xnr1/xnr_0429/xnr/static/WX/voice'

#wx
WX_S_DATE = '2017-10-25'
WX_S_DATE_NEW = '2017-10-25'
WX_S_DATE_ASSESSMENT = '2017-10-25'
WX_GROUP_MESSAGE_START_DATE = '2017-10-25'
WX_GROUP_MESSAGE_START_DATE_ASSESSMENT = '2017-10-25'
WX_GROUP_MESSAGE_START_DATE_ASSESSMENT = '2017-10-25'


def get_evaluate_max():
    max_result = {}
    evaluate_index = ['importance', 'influence', 'activeness', 'sensitive']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size': 1,
            'sort': [{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es_user_portrait.search(index=portrait_name, doc_type=portrait_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result

def normal_index(index, max_index):
    try:
        normal_value = math.log((index / max_index) * 9 + 1, 10) * 100
        return normal_value
    except:
        return index

##test for time
def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

R_BEGIN_TIME = '2016-11-21'
DAY = 24*3600
RUN_TYPE = 0

def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    r_begin_ts = datetime2ts(R_BEGIN_TIME)
    db_number = ((date_ts - r_begin_ts) / (DAY * 7)) % 2 + 1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number

def cut_filter(w_text):
    pattern_list = [r'\（分享自 .*\）', r'http://t.cn/\w*']
    for i in pattern_list:
        p = re.compile(i)
        w_text = p.sub('', w_text)
    #w_text = re.sub(r'[a-zA-z]','',w_text)
    a1 = re.compile(r'\[.*?\]')
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'回复\@' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'.*?\:')
    w_text = a1.sub('',w_text)
##    a1 = re.compile(r'\@.*?\s')
##    w_text = a1.sub('',w_text)
##    a1 = re.compile(r'\w',re.L)
##    w_text = a1.sub('',w_text)
    if w_text == '转发微博' or w_text == '转发':
        w_text = ''

    return w_text
