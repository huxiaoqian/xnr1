# -*- coding: utf-8 -*-
'''
use to save table info in database
'''
import redis
from elasticsearch import Elasticsearch
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from global_config import ES_CLUSTER_HOST, ES_CLUSTER_PORT,ES_INTELLIGENT_HOST, ES_INTELLIGENT_PORT, \
                          ES_FLOW_TEXT_HOST, ES_FLOW_TEXT_PORT,\
                          ES_USER_PORTRAIT_HOST, ES_USER_PORTRAIT_PORT,USER_PROFILE_ES_HOST,\
                          REDIS_HOST, REDIS_PORT,REDIS_CLUSTER_HOST_FLOW3,REDIS_CLUSTER_PORT_FLOW3,\
                          REDIS_HOST_SENSITIVE,REDIS_PORT_SENSITIVE,REDIS_CLUSTER_HOST_FLOW2,REDIS_CLUSTER_PORT_FLOW2,\
                          REDIS_WX_HOST, REDIS_WX_PORT, \
                          qiniu_access_key, qiniu_secret_key, qiniu_bucket_name, qiniu_bucket_domain

#module1.1:init es
es_xnr = Elasticsearch(ES_CLUSTER_HOST, timeout=600)
es_intel = Elasticsearch(ES_INTELLIGENT_HOST, timeout=600)
#module1.2:config es table---index_name, doc_type

# week retweet/be_retweet relation es
retweet_index_name_pre = '1225_retweet_' # retweet: 'retweet_1' or 'retweet_2'
retweet_index_type = 'user'
be_retweet_index_name_pre = '1225_be_retweet_' #be_retweet: 'be_retweet_1'/'be_retweet_2'
be_retweet_index_type = 'user'

fb_be_retweet_index_name_pre = 'fb_be_retweet_' #be_retweet: 'fb_be_retweet_1'/'fb_be_retweet_2'
fb_be_retweet_index_type = 'user'

tw_be_retweet_index_name_pre = 'tw_be_retweet_' #be_retweet: 'tw_be_retweet_1'/'tw_be_retweet_2'
tw_be_retweet_index_type = 'user'
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
#use to save wx xnr info
wx_xnr_index_name = 'wx_xnr'
wx_xnr_index_type = 'user'

#use to save xnr_mapping info
xnr_map_index_name='xnr_mapping'
xnr_map_index_type='user'

## qq上报管理
qq_report_management_index_name = 'qq_report_management'
qq_report_management_index_name_pre = 'qq_report_management_'
qq_report_management_index_type = 'report'

#use to save xnr group message
group_message_index_name_pre = 'group_message_'        #group_message_2017-06-24
group_message_index_type = 'record'
sent_group_message_index_name_pre = 'sent_group_message_'

## wx上报管理
wx_report_management_index_name = 'wx_report_management'
wx_report_management_index_type = 'report'

#use to save wx xnr group message
wx_group_message_index_name_pre = 'wx_group_message_'        #wx_group_message_2017-06-24
wx_group_message_index_type = 'record'
wx_sent_group_message_index_name_pre = 'wx_sent_group_message_'

# use to search flow text and bci
es_flow_text = Elasticsearch(ES_FLOW_TEXT_HOST, timeout=600)
flow_text_index_name_pre = 'flow_text_' #flow_text_index_name: flow_text_2017-06-24
flow_text_index_type = 'text'

weibo_bci_index_name_pre = 'bci_'
weibo_bci_index_type = 'bci'

weibo_bci_history_index_name = 'bci_history'
weibo_bci_history_index_type = 'bci'

weibo_sensitive_history_index_name = 'sensitive_history'
weibo_sensitive_history_index_type = 'sensitive'

#use to identify the user portrait
es_user_profile = Elasticsearch(USER_PROFILE_ES_HOST, timeout = 600)
es_user_portrait = Elasticsearch(ES_USER_PORTRAIT_HOST, timeout=600)
portrait_index_name = 'user_portrait_1222'
portrait_index_type = 'user'

#fb user portrait
es_fb_user_profile = Elasticsearch(ES_CLUSTER_HOST, timeout = 600)
es_fb_user_portrait = Elasticsearch(ES_CLUSTER_HOST, timeout=600)
fb_portrait_index_name = 'fb_user_portrait'
fb_portrait_index_type = 'user'

#tw user portrait
es_tw_user_profile = Elasticsearch(ES_CLUSTER_HOST, timeout = 600)
es_tw_user_portrait = Elasticsearch(ES_CLUSTER_HOST, timeout=600)
tw_portrait_index_name = 'tw_user_portrait'
tw_portrait_index_type = 'user'

#es: translations
es_translation = Elasticsearch(ES_CLUSTER_HOST, timeout=600)
translation_index_name = 'translation'
translation_index_type = 'record'

#use to identify the qq document task redis list
qq_document_task_name = 'qq_document'


#use to identify the weibo xnr update queue list
update_userinfo_queue_name = 'update_userinfo'

#use to identify the qq login png save file
#QRCODE_PATH = '/root/.qqbot-tmp/'
QRCODE_PATH = '/home/ubuntu8/yumingming/xnr1/xnr/static/images/QQ/'
ABS_LOGIN_PATH = '/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/qq/receiveQQGroupMessage.py'

#wxxnr的一些数据的存放地址
wx_xnr_data_path = 'xnr/wx/data'
wx_xnr_qrcode_path = 'xnr/static/WX'
WX_LOGIN_PATH = 'xnr/wx/run_bot.py' #使用命令行开启run_bot()的subprocess的程序地址
sensitive_words_path = 'xnr/wx/sensitive_words.txt'

'''
公共mappings
'''

writing_task_index_name = 'intel_writing_task'
writing_task_index_type = 'task'

#weibo_topic_index_name = 'task_id'
weibo_topic_type = 'weibo'
facebook_topic_type = 'facebook' 
twitter_topic_type = 'twitter' 

intel_opinion_results_index_name = 'intel_opinion_results'
intel_type_all = 'all'
intel_type_follow = 'follow'
intel_type_influence = 'influence'
intel_type_sensitive = 'sensitive'

topics_river_index_name = 'topic_river_results'
topics_river_index_type = 'river'

timeline_index_name = 'timeline_results'
timeline_index_type = 'timeline'

intel_models_text_index_name = 'models_text'
intel_models_text_index_type = 'text'


opinion_corpus_index_name = 'opinion_corpus'
opinion_corpus_index_type = 'text'

opinion_corpus_results_index_name = 'opinion_corpus_results'
opinion_corpus_results_index_type = 'text'

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

fb_domain_index_name = 'facebook_domain'
fb_domain_index_type = 'group'

tw_domain_index_name = 'twitter_domain'
tw_domain_index_type = 'group'

#use to save role info
weibo_role_index_name = 'weibo_role'
weibo_role_index_type = 'role'

fb_role_index_name = 'fb_role'
fb_role_index_type = 'role'

tw_role_index_name = 'tw_role'
tw_role_index_type = 'role'
# use to save example model
weibo_example_model_index_name = 'weibo_example_model'
weibo_example_model_index_type = 'model'

##facebook
fb_example_model_index_name = 'facebook_example_model'
fb_example_model_index_type = 'model'

##twitter
tw_example_model_index_name = 'twitter_example_model'
tw_example_model_index_type = 'model'

# use to publish tweet at future time
weibo_xnr_timing_list_index_name = 'tweet_timing_list'
weibo_xnr_timing_list_index_type = 'timing_list'

# use to retweet tweet at future time
weibo_xnr_retweet_timing_list_index_name = 'tweet_retweet_timing_list'
weibo_xnr_retweet_timing_list_index_type = 'timing_list'


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

#use to save weibo xnr like operate
weibo_xnr_save_like_index_name='weibo_xnr_save_like'
weibo_xnr_save_like_index_type='text'

#use to save weibo xnr count info
weibo_xnr_count_info_index_name='weibo_xnr_count'
weibo_xnr_count_info_index_type='text'

#use to save weibo xnr keywords value count info
weibo_keyword_count_index_name='weibo_keyword_count'
weibo_keyword_count_index_type='text'

#community discovery
#use to save weibo community target user info
weibo_community_target_user_index_name_pre = 'weibo_community_target_user_'
weibo_community_target_user_index_type = 'user'

# xnr_flow_text
xnr_flow_text_index_name_pre = 'xnr_flow_text_'
xnr_flow_text_index_type = 'text'
new_xnr_flow_text_index_name_pre = 'new_xnr_flow_text_'
new_xnr_flow_text_index_type = 'text'
# 日常发帖
daily_interest_index_name_pre = 'daily_inerest_flow_text_'
daily_interest_index_type = 'text'

# 安全性评估 发帖内容
topic_distribute_tweets_index_name_pre = 'topic_distribute_tweets_'
topic_distribute_tweets_index_type = 'topic'

domain_distribute_tweets_index_name_pre = 'domain_distribute_tweets_'
domain_distribute_tweets_index_type = 'domain'

user_domain_index_name = 'user_domain'
user_domain_index_type = 'domain'

# social sensing
index_sensing = "manage_sensing_task"
type_sensing = "task"
id_sensing = "social_sensing_task"
social_sensing_index_name = 'social_sensing_text'
social_sensing_index_name_pre = 'social_sensing_text_'
social_sensing_index_type = 'text'

weibo_private_white_uid_index_name = 'weibo_private_white_uid'
weibo_private_white_uid_index_type = 'white_uid'


# content recommendation & sub opinion

weibo_hot_keyword_task_index_name = 'recommend_subopinion_keywords_task'
weibo_hot_keyword_task_index_type = 'keywords_task'

weibo_hot_content_recommend_results_index_name = 'content_recommend_results'
weibo_hot_content_recommend_results_index_type = 'content_recommend'

weibo_hot_subopinion_results_index_name = 'subopinion_results'
weibo_hot_subopinion_results_index_type = 'subopinion'

# 行为评估分值
weibo_xnr_assessment_index_name= 'weibo_xnr_assessment'
weibo_xnr_assessment_index_type = 'score'

# 业务知识库
weibo_date_remind_index_name_test = 'weibo_date_remind_test'
weibo_date_remind_index_name = 'weibo_date_remind'
weibo_date_remind_index_type = 'remind'

weibo_sensitive_words_index_name = 'weibo_sensitive_words'
weibo_sensitive_words_index_type = 'sensitive_words'

weibo_hidden_expression_index_name_test = 'weibo_hidden_expression_test'
weibo_hidden_expression_index_name = 'weibo_hidden_expression'
weibo_hidden_expression_index_type = 'hidden_expression'

## 预警
weibo_user_warning_index_name = 'weibo_user_warning'
weibo_user_warning_index_name_pre = 'weibo_user_warning_'
weibo_user_warning_index_type = 'text'

weibo_event_warning_index_name = 'weibo_event_warning'
weibo_event_warning_index_name_pre = 'weibo_event_warning_'
weibo_event_warning_index_type = 'text'

weibo_speech_warning_index_name = 'weibo_speech_warning'
weibo_speech_warning_index_name_pre = 'weibo_speech_warning_'
weibo_speech_warning_index_type = 'text'

weibo_timing_warning_index_name_pre = 'weibo_time_warning_'
weibo_timing_warning_index_type = 'text'

weibo_warning_corpus_index_name = 'weibo_warning_corpus'
weibo_warning_corpus_index_type = 'text'

# 语料库 -- 主题和日常
weibo_xnr_corpus_index_name = 'weibo_corpus'
weibo_xnr_corpus_index_type = 'text'

## 上报管理
weibo_report_management_index_name_pre = 'weibo_report_management_'
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


## qq发言统计 
qq_xnr_history_count_index_name_pre = 'qq_history_count_'
qq_xnr_history_count_index_type = 'count'  # - 活跃
qq_xnr_history_be_at_index_type = 'be_at'   # - 影响力
qq_xnr_history_sensitive_index_type = 'sensitive'   # - 渗透

## wx发言统计 
wx_xnr_history_count_index_name = 'wx_history_count'
wx_xnr_history_count_index_type = 'count'  # - 活跃
wx_xnr_history_be_at_index_type = 'be_at'   # - 影响力
wx_xnr_history_sensitive_index_type = 'sensitive'   # - 渗透

# facebook

# social sensing
fb_index_sensing = "fb_manage_sensing_task"
fb_type_sensing = "task"
fb_id_sensing = "fb_social_sensing_task"
#fb_social_sensing_index_name = 'fb_social_sensing_text'
fb_social_sensing_index_name_pre = 'fb_social_sensing_text_'
fb_social_sensing_index_type = 'text'

#use to save fb xnr personal information
fb_xnr_index_name='fb_xnr'
fb_xnr_index_type='user'

#use to save fb xnr information which should be count
fb_xnr_fans_followers_index_name='fb_xnr_fans_followers'
fb_xnr_fans_followers_index_type='uids'

#use to save facebook xnr count info
facebook_xnr_count_info_index_name='facebook_xnr_count'
facebook_xnr_count_info_index_type='text'

# 行为评估分值
facebook_xnr_assessment_index_name= 'facebook_xnr_assessment'
facebook_xnr_assessment_index_type = 'score'

#use to save feedback info
facebook_feedback_comment_index_name_pre = 'facebook_feedback_comment_'
facebook_feedback_comment_index_name = 'facebook_feedback_comment'
facebook_feedback_comment_index_type = 'text'

facebook_feedback_retweet_index_name_pre = 'facebook_feedback_retweet_'
facebook_feedback_retweet_index_name = 'facebook_feedback_retweet'
facebook_feedback_retweet_index_type = 'text'

facebook_feedback_private_index_name_pre = 'facebook_feedback_private_'
facebook_feedback_private_index_name = 'facebook_feedback_private'
facebook_feedback_private_index_type = 'text'

facebook_feedback_at_index_name_pre = 'facebook_feedback_at_'
facebook_feedback_at_index_name = 'facebook_feedback_at'
facebook_feedback_at_index_type = 'text'

facebook_feedback_like_index_name_pre = 'facebook_feedback_like_'
facebook_feedback_like_index_name = 'facebook_feedback_like'
facebook_feedback_like_index_type = 'text'

facebook_feedback_fans_index_name_pre = 'facebook_feedback_fans_'
facebook_feedback_fans_index_name = 'facebook_feedback_fans'
facebook_feedback_fans_index_type = 'text'

facebook_feedback_friends_index_name_pre = 'facebook_feedback_friends_'
facebook_feedback_friends_index_name = 'facebook_feedback_friends'
facebook_feedback_friends_index_type = 'text'

# use to save flow text 
facebook_flow_text_index_name_pre = 'facebook_flow_text_'
facebook_flow_text_index_type = 'text'

facebook_count_index_name_pre = 'facebook_count_'
facebook_count_index_type = 'text'

facebook_user_index_name = 'facebook_user'
facebook_user_index_type = 'user'

fb_xnr_flow_text_index_name_pre = 'fb_xnr_flow_text_'
fb_xnr_flow_text_index_type = 'text'


# use to publish tweet at future time
fb_xnr_timing_list_index_name = 'fb_tweet_timing_list'
fb_xnr_timing_list_index_type = 'timing_list'

# use to retweet tweet at future time
fb_xnr_retweet_timing_list_index_name = 'fb_tweet_retweet_timing_list'
fb_xnr_retweet_timing_list_index_type = 'timing_list'


# use to save influence
fb_bci_index_name_pre = 'fb_bci_'
fb_bci_index_type = 'bci'

fb_hot_keyword_task_index_name = 'fb_recommend_subopinion_keywords_task'
fb_hot_keyword_task_index_type = 'keywords_task'

fb_hot_content_recommend_results_index_name = 'fb_content_recommend_results'
fb_hot_content_recommend_results_index_type = 'content_recommend'

fb_hot_subopinion_results_index_name = 'fb_subopinion_results'
fb_hot_subopinion_results_index_type = 'subopinion'


# 日常兴趣
fb_daily_interest_index_name_pre = 'fb_daily_inerest_flow_text_'
fb_daily_interest_index_type = 'text'

#预警
facebook_user_warning_index_name_pre = 'facebook_user_warning_'
facebook_user_warning_index_type = 'text'

facebook_event_warning_index_name_pre = 'facebook_event_warning_'
facebook_event_warning_index_type = 'text'

facebook_speech_warning_index_name_pre = 'facebook_speech_warning_'
facebook_speech_warning_index_type = 'text'

facebook_timing_warning_index_name_pre = 'facebook_time_warning_'
facebook_timing_warning_index_type = 'text'

#监测
facebook_keyword_count_index_name = 'facebook_keyword_count'
facebook_keyword_count_index_type = 'text'

## 上报管理
facebook_report_management_index_name_pre = 'facebook_report_management_'
facebook_report_management_index_name = 'facebook_report_management'
facebook_report_management_index_type = 'report'

# 语料库 -- 主题和日常
facebook_xnr_corpus_index_name = 'facebook_corpus'
facebook_xnr_corpus_index_type = 'text'

#预警库
facebook_warning_corpus_index_name = 'facebook_warning_corpus'
facebook_warning_corpus_index_type = 'text'

#社区预警
facebook_community_target_user_index_name_pre = 'facebook_community_target_user_'
facebook_community_target_user_index_type = 'user'

facebook_select_community_index_name_pre = 'facebook_select_community_'
facebook_select_community_index_type = 'community'

facebook_detail_community_index_name_pre = 'facebook_detail_community_'
facebook_detail_community_index_type = 'community'

facebook_trace_community_index_name_pre = 'facebook_trace_community_'
facebook_trace_community_index_type = 'text'

# twitter

# social sensing
tw_index_sensing = "tw_manage_sensing_task"
tw_type_sensing = "task"
tw_id_sensing = "tw_social_sensing_task"
tw_social_sensing_index_name = 'tw_social_sensing_text'
tw_social_sensing_index_name_pre = 'tw_social_sensing_text_'
tw_social_sensing_index_type = 'text'

#use to save tw xnr personal information
tw_xnr_index_name='tw_xnr'
tw_xnr_index_type='user'

#use to save tw xnr information which should be count
tw_xnr_fans_followers_index_name='tw_xnr_fans_followers'
tw_xnr_fans_followers_index_type='uids'


# 行为评估分值
twitter_xnr_assessment_index_name= 'twitter_xnr_assessment'
twitter_xnr_assessment_index_type = 'score'

#use to save twitter xnr count info
twitter_xnr_count_info_index_name='twitter_xnr_count'
twitter_xnr_count_info_index_type='text'

#use to save feedback info
twitter_feedback_comment_index_name_pre = 'twitter_feedback_comment_'
twitter_feedback_comment_index_name = 'twitter_feedback_comment'
twitter_feedback_comment_index_type = 'text'

twitter_feedback_retweet_index_name_pre = 'twitter_feedback_retweet_'
twitter_feedback_retweet_index_name = 'twitter_feedback_retweet'
twitter_feedback_retweet_index_type = 'text'

twitter_feedback_private_index_name_pre = 'twitter_feedback_private_'
twitter_feedback_private_index_name = 'twitter_feedback_private'
twitter_feedback_private_index_type = 'text'

twitter_feedback_at_index_name_pre = 'twitter_feedback_at_'
twitter_feedback_at_index_name = 'twitter_feedback_at'
twitter_feedback_at_index_type = 'text'

twitter_feedback_like_index_name_pre = 'twitter_feedback_like_'
twitter_feedback_like_index_name = 'twitter_feedback_like'
twitter_feedback_like_index_type = 'text'

twitter_feedback_fans_index_name_pre = 'twitter_feedback_fans_'
twitter_feedback_fans_index_name = 'twitter_feedback_fans'
twitter_feedback_fans_index_type = 'text'

twitter_feedback_follow_index_name_pre = 'twitter_feedback_follow_'
twitter_feedback_follow_index_name = 'twitter_feedback_follow'
twitter_feedback_follow_index_type = 'text'

# use to save twitter flow text
twitter_flow_text_index_name_pre = 'twitter_flow_text_'
twitter_flow_text_index_type = 'text'


twitter_count_index_name_pre = 'twitter_count_'
twitter_count_index_type = 'text'


twitter_user_index_name = 'twitter_user'
twitter_user_index_type = 'user'

tw_xnr_flow_text_index_name_pre = 'tw_xnr_flow_text_'
tw_xnr_flow_text_index_type = 'text'

tw_xnr_index_name='tw_xnr'
tw_xnr_index_type='user'


# 日常兴趣
tw_daily_interest_index_name_pre = 'tw_daily_inerest_flow_text_'
tw_daily_interest_index_type = 'text'


#预警
twitter_user_warning_index_name_pre = 'twitter_user_warning_'
twitter_user_warning_index_type = 'text'

twitter_event_warning_index_name_pre = 'twitter_event_warning_'
twitter_event_warning_index_type = 'text'

twitter_speech_warning_index_name_pre = 'twitter_speech_warning_'
twitter_speech_warning_index_type = 'text'

twitter_timing_warning_index_name_pre = 'twitter_time_warning_'
twitter_timing_warning_index_type = 'text'

#监测
twitter_keyword_count_index_name = 'twitter_keyword_count'
twitter_keyword_count_index_type = 'text'

## 上报管理
twitter_report_management_index_name_pre = 'twitter_report_management_'
twitter_report_management_index_name= 'twitter_report_management'
twitter_report_management_index_type = 'report'

# 语料库 -- 主题和日常
twitter_xnr_corpus_index_name = 'twitter_corpus'
twitter_xnr_corpus_index_type = 'text'

#预警库
twitter_warning_corpus_index_name = 'twitter_warning_corpus'
twitter_warning_corpus_index_type = 'text'

# use to save influence
tw_bci_index_name_pre = 'tw_bci_'
tw_bci_index_type = 'bci'


# use to publish tweet at future time
tw_xnr_timing_list_index_name = 'tw_tweet_timing_list'
tw_xnr_timing_list_index_type = 'timing_list'

# use to retweet tweet at future time
tw_xnr_retweet_timing_list_index_name = 'tw_tweet_retweet_timing_list'
tw_xnr_retweet_timing_list_index_type = 'timing_list'


tw_hot_keyword_task_index_name = 'tw_recommend_subopinion_keywords_task'
tw_hot_keyword_task_index_type = 'keywords_task'

tw_hot_content_recommend_results_index_name = 'tw_content_recommend_results'
tw_hot_content_recommend_results_index_type = 'content_recommend'

tw_hot_subopinion_results_index_name = 'tw_subopinion_results'
tw_hot_subopinion_results_index_type = 'subopinion'


#module2.1: init redis
def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0):
    return redis.StrictRedis(host, port)

R_WRITING = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
writing_task_queue_name = 'intelligent_writing_task'

r = _default_redis(host=REDIS_HOST, port=REDIS_PORT)
weibo_target_domain_detect_queue_name = 'weibo_target_domain_detect_task'
weibo_target_domain_analysis_queue_name = 'weibo_target_domain_analysis_task'

fb_target_domain_detect_queue_name = 'facebook_target_domain_detect_task'
fb_target_domain_analysis_queue_name = 'facebook_target_domain_analysis_task'

tw_target_domain_detect_queue_name = 'twitter_target_domain_detect_task'
tw_target_domain_analysis_queue_name = 'twitter_target_domain_analysis_task'

# social sensing redis
R_SOCIAL_SENSING = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
weibo_social_sensing_task_queue_name = 'weibo_social_sensing_task'

# content recommendation sub opinion TASK
R_RECOMMEND_SUBOPINION_KEYWORD_TASK = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
weibo_recommend_subopinion_keywords_task_queue_name = 'recommend_subopnion_keywords_task_queue'
fb_recommend_subopinion_keywords_task_queue_name = 'fb_recommend_subopnion_keywords_task_queue'
tw_recommend_subopinion_keywords_task_queue_name = 'tw_recommend_subopnion_keywords_task_queue'

# use to save follower every day
R_WEIBO_XNR_FANS_FOLLOWERS = _default_redis(host=REDIS_HOST,port=REDIS_PORT,db=1)
r_fans_uid_list_datetime_pre = 'fans_uid_list_'  # fans_uid_list_2017-08-30
r_fans_count_datetime_xnr_pre = 'fans_count_'    # fans_count_2017-08-30_6337917209
r_fans_search_xnr_pre = 'fans_search_'    # fans_search_6337917209

r_followers_uid_list_datetime_pre = 'followers_uid_list_'  # followers_uid_list_2017-08-30
r_followers_count_datetime_xnr_pre = 'followers_count_'    # followers_count_2017-08-30_6337917209
r_followers_search_xnr_pre = 'followers_search_'    # followers_search_6337917209



## use to save follower every day    facebook
R_FACEBOOK_XNR_FANS_FOLLOWERS = _default_redis(host=REDIS_HOST,port=REDIS_PORT,db=1)
r_fb_fans_uid_list_datetime_pre = 'fb_fans_uid_list_'  # fb_fans_uid_list_2017-08-30
r_fb_fans_count_datetime_xnr_pre = 'fb_fans_count_'    # fb_fans_count_2017-08-30_6337917209
r_fb_fans_search_xnr_pre = 'fb_fans_search_'    # fb_fans_search_6337917209

r_fb_followers_uid_list_datetime_pre = 'fb_followers_uid_list_'  # fb_followers_uid_list_2017-08-30
r_fb_followers_count_datetime_xnr_pre = 'fb_followers_count_'    # fb_followers_count_2017-08-30_6337917209
r_fb_followers_search_xnr_pre = 'fb_followers_search_'    # fb_followers_search_6337917209




## use to save follower every day    twitter
R_TWITTER_XNR_FANS_FOLLOWERS = _default_redis(host=REDIS_HOST,port=REDIS_PORT,db=1)
r_tw_fans_uid_list_datetime_pre = 'tw_fans_uid_list_'  # fb_fans_uid_list_2017-08-30
r_tw_fans_count_datetime_xnr_pre = 'tw_fans_count_'    # fb_fans_count_2017-08-30_6337917209
r_tw_fans_search_xnr_pre = 'tw_fans_search_'    # fb_fans_search_6337917209

r_tw_followers_uid_list_datetime_pre = 'tw_followers_uid_list_'  # fb_followers_uid_list_2017-08-30
r_tw_followers_count_datetime_xnr_pre = 'tw_followers_count_'    # fb_followers_count_2017-08-30_6337917209
r_tw_followers_search_xnr_pre = 'tw_followers_search_'    # fb_followers_search_6337917209



# use to save action assessment every day
# R_WEIBO_XNR_ASSESSMENT = _default_redis(host=REDIS_HOST,port=REDIS_PORT,db=1)
# r_weibo_xnr_assessment_pre = 'weibo_xnr_assessment_'

#use to save xnr info

## hashtag
R_CLUSTER_FLOW2 = redis.StrictRedis(host=REDIS_CLUSTER_HOST_FLOW2, port=REDIS_CLUSTER_PORT_FLOW2)

# sensitive user
R_CLUSTER_FLOW3 = redis.StrictRedis(host=REDIS_CLUSTER_HOST_FLOW3, port=REDIS_CLUSTER_PORT_FLOW3)
R_ADMIN = _default_redis(host=REDIS_HOST_SENSITIVE, port=REDIS_PORT_SENSITIVE, db=15)

# 存储qq监测群
r_qq_group_set_pre = 'qq_group_set_'

# facebook&twitter uname_id
R_UNAME2ID_FT = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
fb_uname2id = 'fb_user'
tw_uname2id = 'tw_user'

# r_retweet 转发网络
redis_host_list = [1,2]
R_retweet = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=2)

fb_retweet_1 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=3)
fb_retweet_2 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=4)

tw_retweet_1 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
tw_retweet_2 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=6)

fb_retweet_dict = {'1':fb_retweet_1,'2':fb_retweet_2}
tw_retweet_dict = {'1':tw_retweet_1,'2':tw_retweet_2}



#微信虚拟人相关
r_wx = _default_redis(host=REDIS_WX_HOST, port=REDIS_WX_PORT)
qiniu = Auth(qiniu_access_key, qiniu_secret_key)

R_OPERATE_QUEUE = redis.StrictRedis(host=REDIS_CLUSTER_HOST_FLOW2, port=REDIS_CLUSTER_PORT_FLOW2, db=3)
operate_queue_name = 'operate'


#各类虚拟人从redis中获取编号时所对应的key
fb_xnr_max_no = 'fb_xnr_max_no'
tw_xnr_max_no = 'tw_xnr_max_no'
wx_xnr_max_no = 'wx_xnr_max_no'
wb_xnr_max_no = 'wb_xnr_max_no'
qq_xnr_max_no = 'qq_xnr_max_no'
