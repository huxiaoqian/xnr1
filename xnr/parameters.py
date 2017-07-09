#-*- coding:utf-8 -*-


MAX_DETECT_COUNT = 900
MAX_FLOW_TEXT_DAYS = 7 ## 最多查询最近多少天的流数据
TOP_KEYWORDS_NUM = 20  ## 最常用的关键词的数量
MAX_SEARCH_SIZE = 99999999 ## 从数据库中最大检索数量

SORT_FIELD = 'timestamp'
TOP_WEIBOS_LIMIT = 500

DOMAIN_ABS_PATH = '/home/ubuntu8/huxiaoqian/user_portrait_151220/user_portrait/user_portrait/cron/model_file/domain'

CH_ABS_PATH = '/home/ubuntu8/huxiaoqian/user_portrait_151220/user_portrait/user_portrait/cron/model_file/character'

MAX_VALUE = 99999999 



topic_en2ch_dict = {'art':u'文体类_娱乐','computer':u'科技类','economic':u'经济类', \
                    'education':u'教育类','environment':u'民生类_环保', 'medicine':u'民生类_健康',\
                    'military':u'军事类','politics':u'政治类_外交','sports':u'文体类_体育',\
                    'traffic':u'民生类_交通','life':u'其他类','anti-corruption':u'政治类_反腐',\
                    'employment':u'民生类_就业','fear-of-violence':u'政治类_暴恐',\
                    'house':u'民生类_住房','law':u'民生类_法律','peace':u'政治类_地区和平',\
                    'religion':u'政治类_宗教','social-security':u'民生类_社会保障'}