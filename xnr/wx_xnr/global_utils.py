#-*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from redis import Redis
from global_config import ES_CLUSTER_HOST, Redis_WX_TEST_PORT
from global_config import qiniu_access_key, qiniu_secret_key, qiniu_bucket_name, qiniu_bucket_domain

es_xnr = Elasticsearch(ES_CLUSTER_HOST, timeout=600)
r = Redis(port=Redis_WX_TEST_PORT)
qiniu = Auth(qiniu_access_key, qiniu_secret_key)

#use to save wx xnr info
wx_xnr_index_name = 'wx_xnr'
wx_xnr_index_type = 'user'

## wx上报管理
wx_report_management_index_name = 'wx_report_management'
wx_report_management_index_type = 'report'

#use to save xnr group message
wx_group_message_index_name_pre = 'wx_group_message_'        #wx_group_message_2017-06-24
wx_group_message_index_type = 'record'
wx_sent_group_message_index_name_pre = 'wx_sent_group_message_'

## wx发言统计 
wx_xnr_history_count_index_name = 'qq_history_count'
wx_xnr_history_count_index_type = 'count'  # - 活跃
wx_xnr_history_be_at_index_type = 'be_at'   # - 影响力
wx_xnr_history_sensitive_index_type = 'sensitive'   # - 渗透

#wxxnr的一些数据的存放地址
wx_xnr_data_path = 'xnr/wx_xnr/wx/data'
wx_xnr_qrcode_path = 'xnr/static/images/WX'
WX_LOGIN_PATH = 'xnr/wx_xnr/wx/run_bot.py'	#使用命令行开启run_bot()的subprocess的程序地址
sensitive_words_path = 'xnr/wx_xnr/wx/sensitive_words.txt'