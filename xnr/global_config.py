# -*- coding: utf-8 -*-
'''
use to save database information
'''
import os

#use to mark type:  run or test
S_TYPE = 'test'   #test/run
S_DATE = '2016-11-20' #when type=test, now_date=S_DATE

#config es
#config xnr user info
ES_CLUSTER_HOST = ['219.224.134.213:9205', '219.224.134.214:9205',\
                   '219.224.134.215:9205']
ES_CLUSTER_PORT = '9205'
#config flow text info
ES_FLOW_TEXT_HOST = ['219.224.134.216:9201', '219.224.134.217:9201',\
                          '219.224.134.218:9201']
ES_FLOW_TEXT_PORT = '9201'

# need three ES identification 
USER_PROFILE_ES_HOST = ['10.128.55.81','10.128.55.82','10.128.55.83']
USER_PROFILE_ES_PORT = 9200

#config user portrat
ES_USER_PORTRAIT_HOST = ['219.224.134.216:9201', '219.224.134.217:9201',\
                     '219.224.134.218:9201']
ES_USER_PORTRAIT_PORT = '9201'

#es_path
ES_PATH = '/home/ubuntu8/huxiaoqian/elasticsearch-1.6.0/'

#config redis
REDIS_HOST = '219.224.134.212'
REDIS_PORT = '7392'

#redis_path
REDIS_PATH = '/home/ubuntu7/huxiaoqian/redis-3.0.5/7392/'

# use to identify the db number of redis-97
R_BEGIN_TIME = '2016-03-21'

