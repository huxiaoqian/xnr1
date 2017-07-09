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

#use to save xnr info
xnr_index_name = 'xnr'
xnr_index_type = 'user'
#use to save xnr
qq_xnr_index_name = 'qq_xnr'
qq_xnr_index_type = 'user'
#use to save qq xnr
group_message_index_name = 'group_message_'        #group_message_xnr_qqnumber_2017-06-24
group_message_index_type = 'record'
es_flow_text = Elasticsearch(ES_FLOW_TEXT_HOST, timeout=600)
flow_text_index_name_pre = 'flow_text_' #flow_text_index_name: flow_text_2017-06-24
flow_text_index_type = 'text'
#use to identify the user portrait

es_user_portrait = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout=600)
portrait_index_name = 'user_portrait_1222'
portrait_index_type = 'user'

es_retweet = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout = 600)
es_comment = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout = 600)

#use to save domain info
weibo_domain_index_name = 'weibo_domain'
weibo_domain_index_type = 'group'

#use to save role info
weibo_role_index_name = 'weibo_role'
weibo_role_index_type = 'role'

#use to save feedback info
weibo_feedback_comment_index_name = 'weibo_feedback_comment'
weibo_feedback_comment_index_type = 'text'

weibo_feedback_retweet_index_name = 'weibo_feedback_retweet'
weibo_feedback_retweet_index_type = 'text'

weibo_feedback_private_index_name = 'weibo_feedback_private'
weibo_feedback_private_index_type = 'text'

weibo_feedback_at_index_name = 'weibo_feedback_at'
weibo_feedback_at_index_type = 'text'

weibo_feedback_like_index_name = 'weibo_feedback_like'
weibo_feedback_like_index_type = 'text'

weibo_feedback_follow_index_name = 'weibo_feedback_follow'
weibo_feedback_follow_index_type = 'text'


#module2.1: init redis
def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0):
    return redis.StrictRedis(host, port)

r = _default_redis(host=REDIS_HOST, port=REDIS_PORT)
#use to save xnr info

weibo_target_domain_detect_queue_name = 'weibo_target_domain_detect_task'
weibo_target_domain_analysis_queue_name = 'weibo_target_domain_analysis_task'





