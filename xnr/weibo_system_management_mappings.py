#-*-coding:utf-8-*-
import os
import json
from global_utils import es_xnr as es
from global_utils import weibo_log_management_index_name,weibo_log_management_index_type,\
						weibo_authority_management_index_name,weibo_authority_management_index_type,\
						weibo_account_management_index_name,weibo_account_management_index_type

# 日志管理
def weibo_log_management_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_log_management_index_type:{
				'properties':{
					'user_id':{
						'type':'string',
						'index':'not_analyzed'
					},
					'user_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'login_time':{ #登录时间list[15....,15.....]
						'type':'string',
						'index':'no'
					},
					'login_ip':{#登录ip list
						'type':'string',
						'index':'no'
					},
					'operate_time':{  #操作日期时间戳
						'type':'long'
					},
					'operate_content':{  #操作内容dict
						'type':'string',
						'index':'no'
					},
					'operate_date':{      #操作日期
					     'type':'string',
					     'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_log_management_index_name):
		es.indices.create(index=weibo_log_management_index_name,body=index_info,ignore=400)


# 权限管理
def weibo_authority_management_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_authority_management_index_type:{
				'properties':{
					'role_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'description':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_authority_management_index_name):
		es.indices.create(index=weibo_authority_management_index_name,body=index_info,ignore=400)


# 账户管理
def weibo_account_management_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_account_management_index_type:{
				'properties':{
					'user_id':{
						'type':'string',
						'index':'not_analyzed'
					},
					'user_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'my_xnrs':{  # list: [xnr001,xnr002,...]
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_account_management_index_name):
		es.indices.create(index=weibo_account_management_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	weibo_log_management_mappings()
	weibo_authority_management_mappings()
	weibo_account_management_mappings()
