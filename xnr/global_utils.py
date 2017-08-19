# -*- coding: utf-8 -*-
'''
use to save table info in database
'''
import redis
from elasticsearch import Elasticsearch
from global_config import ES_CLUSTER_HOST, ES_CLUSTER_PORT, \
                          ES_FLOW_TEXT_HOST, ES_FLOW_TEXT_PORT, \
                          ES_USER_PORTRAIT_HOST, ES_USER_PORTRAIT_PORT,\
                          REDIS_HOST, REDIS_PORT,REDIS_CLUSTER_HOST_FLOW3,REDIS_CLUSTER_PORT_FLOW3,\
                          REDIS_HOST_SENSITIVE,REDIS_PORT_SENSITIVE
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

profile_index_name = 'weibo_user'  # user profile es
profile_index_type = 'user'

#use to save xnr info
xnr_index_name = 'xnr'
xnr_index_type = 'user'
#use to save qq xnr info
qq_xnr_index_name = 'qq_xnr'
qq_xnr_index_type = 'user'
#use to save xnr group message
group_message_index_name_pre = 'group_message_'        #group_message_2017-06-24
group_message_index_type = 'record'
es_flow_text = Elasticsearch(ES_FLOW_TEXT_HOST, timeout=600)
flow_text_index_name_pre = 'flow_text_' #flow_text_index_name: flow_text_2017-06-24
flow_text_index_type = 'text'
#use to identify the user portrait
es_user_profile = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout = 600)
es_user_portrait = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout=600)
portrait_index_name = 'user_portrait_1222'
portrait_index_type = 'user'

'''
以下为微博相关定义

'''
#use to save weibo xnr personal information
weibo_xnr_index_name='weibo_xnr'
weibo_xnr_index_type='user'

#use to save weibo xnr information which should be count
weibo_xnr_fans_followers_index_name='weibo_xnr_fans_followers'
weibo_xnr_fans_followers_index_type='uids'

es_retweet = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout = 600)
es_comment = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout = 600)

#use to save domain info
weibo_domain_index_name = 'weibo_domain'
weibo_domain_index_type = 'group'

#use to save role info
weibo_role_index_name = 'weibo_role'
weibo_role_index_type = 'role'

# use to publish tweet at future time
weibo_xnr_timing_list_index_name = 'tweet_timing_list'			
weibo_xnr_timing_list_index_type = 'timing_list'

#use to test lookup weibocontent,can be deleted after test

#use to save feedback info
weibo_feedback_comment_index_name_pre = 'weibo_feedback_comment_'
weibo_feedback_comment_index_name = 'weibo_feedback_comment'
weibo_feedback_comment_index_type = 'text'

weibo_feedback_retweet_index_name_pre = 'weibo_feedback_retweet_'
weibo_feedback_retweet_index_name = 'weibo_feedback_retweet'
weibo_feedback_retweet_index_type = 'text'

weibo_feedback_private_index_name_pre = 'weibo_feedback_private_'
weibo_feedback_private_index_name = 'weibo_feedback_private'
weibo_feedback_private_index_type = 'text'

weibo_feedback_at_index_name_pre = 'weibo_feedback_at_'
weibo_feedback_at_index_name = 'weibo_feedback_at'
weibo_feedback_at_index_type = 'text'

weibo_feedback_like_index_name_pre = 'weibo_feedback_like_'
weibo_feedback_like_index_name = 'weibo_feedback_like'
weibo_feedback_like_index_type = 'text'

weibo_feedback_fans_index_name_pre = 'weibo_feedback_fans_'
weibo_feedback_fans_index_name = 'weibo_feedback_fans'
weibo_feedback_fans_index_type = 'text'

weibo_feedback_follow_index_name_pre = 'weibo_feedback_follow_'
weibo_feedback_follow_index_name = 'weibo_feedback_follow'
weibo_feedback_follow_index_type = 'text'

weibo_feedback_group_index_name = 'weibo_feedback_group'
weibo_feedback_group_index_type = 'text'

# xnr_flow_text
xnr_flow_text_index_name_pre = 'xnr_flow_text_'
xnr_flow_text_index_type = 'text'
# social sensing
index_sensing = "manage_sensing_task"
type_sensing = "task"
id_sensing = "social_sensing_task"
social_sensing_index_name = 'social_sensing_text'
social_sensing_index_type = 'text'

# content recommendation & sub opinion 

weibo_hot_keyword_task_index_name = 'recommend_subopinion_keywords_task'
weibo_hot_keyword_task_index_type = 'keywords_task'

weibo_hot_content_recommend_results_index_name = 'content_recommend_results'
weibo_hot_content_recommend_results_index_type = 'content_recommend'

weibo_hot_subopinion_results_index_name = 'subopinion_results'
weibo_hot_subopinion_results_index_type = 'subopinion'

weibo_bci_index_name_pre = 'bci_'
weibo_bci_index_type = 'bci'

# 业务知识库
weibo_date_remind_index_name = 'weibo_date_remind'
weibo_date_remind_index_type = 'remind'

weibo_sensitive_words_index_name = 'weibo_sensitive_words'
weibo_sensitive_words_index_type = 'sensitive_words'

weibo_hidden_expression_index_name = 'weibo_hidden_expression'
weibo_hidden_expression_index_type = 'hidden_expression'

## 预警
weibo_user_warning_index_name = 'weibo_user_warning'
weibo_user_warning_index_type = 'text'

weibo_event_warning_index_name = 'weibo_event_warning'
weibo_event_warning_index_type = 'text'

weibo_speech_warning_index_name = 'weibo_speech_warning'
weibo_speech_warning_index_type = 'text'


# 语料库 -- 主题和日常
weibo_xnr_corpus_index_name = 'weibo_corpus'
weibo_xnr_corpus_index_type = 'text'

## 上报管理
weibo_report_management_index_name = 'weibo_report_management'
weibo_report_management_index_type = 'report'

## 日志管理
weibo_log_management_index_name = 'weibo_log'
weibo_log_management_index_type = 'log'

## 权限管理
weibo_authority_management_index_name = 'weibo_authority_management'
weibo_authority_management_index_type = 'authority'

## 账户管理
weibo_account_management_index_name = 'weibo_account_management'
weibo_account_management_index_type = 'account'


#module2.1: init redis
def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0):
    return redis.StrictRedis(host, port)

r = _default_redis(host=REDIS_HOST, port=REDIS_PORT)
weibo_target_domain_detect_queue_name = 'weibo_target_domain_detect_task'
weibo_target_domain_analysis_queue_name = 'weibo_target_domain_analysis_task'

# social sensing redis
R_SOCIAL_SENSING = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
weibo_social_sensing_task_queue_name = 'weibo_social_sensing_task'

# content recommendation sub opinion TASK
R_RECOMMEND_SUBOPINION_KEYWORD_TASK = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
weibo_recommend_subopinion_keywords_task_queue_name = 'recommend_subopnion_keywords_task_queue'

#use to save xnr info

# sensitive user
R_CLUSTER_FLOW3 = redis.StrictRedis(host=REDIS_CLUSTER_HOST_FLOW3, port=REDIS_CLUSTER_PORT_FLOW3)
R_ADMIN = _default_redis(host=REDIS_HOST_SENSITIVE, port=REDIS_PORT_SENSITIVE, db=15)