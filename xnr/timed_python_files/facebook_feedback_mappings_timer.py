#-*-coding:utf-8-*-
import os
import json
import time
from elasticsearch import Elasticsearch
import sys
sys.path.append('../')
from global_utils import es_xnr as es
from global_utils import facebook_feedback_comment_index_name_pre,facebook_feedback_comment_index_type,\
						facebook_feedback_retweet_index_name_pre,facebook_feedback_retweet_index_type,\
						facebook_feedback_private_index_name_pre,facebook_feedback_private_index_type,\
						facebook_feedback_at_index_name_pre,facebook_feedback_at_index_type,\
						facebook_feedback_like_index_name_pre,facebook_feedback_like_index_type,\
						facebook_feedback_friends_index_name_pre,facebook_feedback_friends_index_type

from time_utils import ts2datetime

# 点赞
def facebook_feedback_like_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_feedback_like_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{               ## 设为空
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'text':{             ## 设为空
						'type':'string',
						'index':'not_analyzed'
					},
					'root_mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_info':{
						'type':'long'
					},
					'sensitive_user':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					}
				}
			}
		}
	}

	current_time = time.time()
	facebook_feedback_like_index_name = facebook_feedback_like_index_name_pre + ts2datetime(current_time)

	if not es.indices.exists(index=facebook_feedback_like_index_name):
		es.indices.create(index=facebook_feedback_like_index_name,body=index_info,ignore=400)

# 分享
def facebook_feedback_retweet_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_feedback_retweet_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'retweet':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'like':{
						'type':'long'
					},
					'root_mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_info':{
						'type':'long'
					},
					'sensitive_user':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					}
				}
			}
		}
	}

	current_time = time.time()
	facebook_feedback_retweet_index_name = facebook_feedback_retweet_index_name_pre + ts2datetime(current_time)
	if not es.indices.exists(index=facebook_feedback_retweet_index_name):
		es.indices.create(index=facebook_feedback_retweet_index_name,body=index_info,ignore=400)

# 标记
def facebook_feedback_at_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_feedback_at_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_info':{
						'type':'long'
					},
					'sensitive_user':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					}
				}
			}
		}
	}

	current_time = time.time()
	facebook_feedback_at_index_name = facebook_feedback_at_index_name_pre + ts2datetime(current_time)

	if not es.indices.exists(index=facebook_feedback_at_index_name):
		es.indices.create(index=facebook_feedback_at_index_name,body=index_info,ignore=400)


# 评论
def facebook_feedback_comment_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_feedback_comment_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'comment_type':{  ## make 发出的评论   receive 收到的评论
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_info':{
						'type':'long'
					},
					'sensitive_user':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					}
				}
			}
		}
	}

	current_time = time.time()
	facebook_feedback_comment_index_name = facebook_feedback_comment_index_name_pre + ts2datetime(current_time)

	if not es.indices.exists(index=facebook_feedback_comment_index_name):
		es.indices.create(index=facebook_feedback_comment_index_name,body=index_info,ignore=400)


# 私信
def facebook_feedback_private_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_feedback_private_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{               
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'text':{             
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'w_new_count':{  # 0表示均已读 1,2,....表示未读信息个数
						'type':'long'
					},
					'private_type':{ # make 表示发出的私信   receive表示收到的私信
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_info':{
						'type':'long'
					},
					'sensitive_user':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					}
				}
			}
		}
	}

	current_time = time.time()
	facebook_feedback_private_index_name = facebook_feedback_private_index_name_pre + ts2datetime(current_time)

	if not es.indices.exists(index=facebook_feedback_private_index_name):
		es.indices.create(index=facebook_feedback_private_index_name,body=index_info,ignore=400)

# 好友列表
def facebook_feedback_friends_mappings():  ## 粉丝提醒及回粉
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_feedback_friends_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'sex':{
						'type':'string',
						'index':'not_analyzed'
					},
					'geo':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'followers':{             
						'type':'long'
					},
					'friends':{             
						'type':'long'
					},
					'facebooks':{             
						'type':'long'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'friends_source':{
						'type':'string',
						'index':'not_analyzed'
					},
					'description':{
						'type':'string',
						'index':'not_analyzed'
					},
					'facebook_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_info':{
						'type':'long'
					},
					'sensitive_user':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					},
					'sensor_mark':{
						'type':'string',
						'index':'not_analyzed'
					},
					'trace_follow_mark':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	#current_time = time.time()
	#facebook_feedback_friends_index_name = facebook_feedback_friends_index_name_pre + ts2datetime(current_time)
	facebook_feedback_friends_index_name = 'facebook_feedback_friends'
	if not es.indices.exists(index=facebook_feedback_friends_index_name):
		es.indices.create(index=facebook_feedback_friends_index_name,body=index_info,ignore=400)


if __name__ == '__main__':
	
	#facebook_feedback_like_mappings()
	#facebook_feedback_retweet_mappings()
	#facebook_feedback_at_mappings()
	#facebook_feedback_comment_mappings()
	#facebook_feedback_private_mappings()
	facebook_feedback_friends_mappings()