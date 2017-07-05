# -*- coding: utf-8 -*-
'''
use to save table info in database
'''
import redis
from elasticsearch import Elasticsearch
from global_config import ES_CLUSTER_HOST, ES_CLUSTER_PORT, \
                          ES_FLOW_TEXT_HOST, ES_FLOW_TEXT_PORT, \
                          ES_USER_PORTRAIT_HOST, ES_USER_PORTRAIT_PORT,\
                          REDIS_HOST, REDIS_PORT
#module1.1:init es
es_xnr = Elasticsearch(ES_CLUSTER_HOST, timeout=600)
#module1.2:config es table---index_name, doc_type
#use to save xnr info
xnr_index_name = 'xnr'
xnr_index_type = 'user'
#use to save xnr
qq_xnr_index_name = 'qq_xnr'
qq_xnr_index_type = 'user'
#use to save qq xnr
es_flow_text = Elasticsearch(ES_FLOW_TEXT_HOST, timeout=600)
flow_text_index_name_pre = 'flow_text_' #flow_text_index_name: flow_text_2017-06-24
flow_text_index_type = 'text'
#use to identify the user portrait
es_user_portrait = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout=600)
portrait_index_name = 'user_portrait_1222'
portrait_index_type = 'user'

#use to save domain info
weibo_domain_index_name = 'weibo_domain'
weibo_domain_index_type = 'group'

#use to save role info
weibo_role_index_name = 'weibo_role'
weibo_role_index_type = 'role'

#module2.1: init redis
def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0):
    return redis.StrictRedis(host, port)

r = _default_redis(host=REDIS_HOST, port=REDIS_PORT)
#use to save xnr info

weibo_target_domain_detect_queue_name = 'weibo_target_domain_detect_task'
weibo_target_domain_analysis_queue_name = 'weibo_target_domain_analysis_task'





