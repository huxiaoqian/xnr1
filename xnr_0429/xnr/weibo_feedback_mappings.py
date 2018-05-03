#-*-coding:utf-8-*-
import os
import json
import time
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_feedback_comment_index_name_pre,weibo_feedback_comment_index_type,\
						weibo_feedback_retweet_index_name_pre,weibo_feedback_retweet_index_type,\
						weibo_feedback_private_index_name_pre,weibo_feedback_private_index_type,\
						weibo_feedback_at_index_name_pre,weibo_feedback_at_index_type,\
						weibo_feedback_like_index_name_pre,weibo_feedback_like_index_type,\
						weibo_feedback_fans_index_name,weibo_feedback_fans_index_type,\
						weibo_feedback_follow_index_name,weibo_feedback_follow_index_type,\
						weibo_feedback_group_index_name,weibo_feedback_group_index_type,\
						weibo_private_white_uid_index_name,weibo_private_white_uid_index_type
from time_utils import ts2datetime,datetime2ts

def weibo_feedback_retweet_mappings(datetime):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_retweet_index_type:{
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
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
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

	#current_time = time.time()
	weibo_feedback_retweet_index_name = weibo_feedback_retweet_index_name_pre + datetime
	if not es.indices.exists(index=weibo_feedback_retweet_index_name):
		es.indices.create(index=weibo_feedback_retweet_index_name,body=index_info,ignore=400)

def weibo_feedback_comment_mappings(datetime):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_comment_index_type:{
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
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
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

	#current_time = time.time()
	weibo_feedback_comment_index_name = weibo_feedback_comment_index_name_pre + datetime

	if not es.indices.exists(index=weibo_feedback_comment_index_name):
		es.indices.create(index=weibo_feedback_comment_index_name,body=index_info,ignore=400)


def weibo_feedback_at_mappings(datetime):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_at_index_type:{
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
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
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

	#current_time = time.time()
	weibo_feedback_at_index_name = weibo_feedback_at_index_name_pre + datetime

	if not es.indices.exists(index=weibo_feedback_at_index_name):
		es.indices.create(index=weibo_feedback_at_index_name,body=index_info,ignore=400)


def weibo_feedback_like_mappings(datetime):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_like_index_type:{
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
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
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

	#current_time = time.time()
	weibo_feedback_like_index_name = weibo_feedback_like_index_name_pre + datetime

	if not es.indices.exists(index=weibo_feedback_like_index_name):
		es.indices.create(index=weibo_feedback_like_index_name,body=index_info,ignore=400)

def weibo_feedback_private_mappings(datetime):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_private_index_type:{
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
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
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

	#current_time = time.time()
	weibo_feedback_private_index_name = weibo_feedback_private_index_name_pre + datetime

	if not es.indices.exists(index=weibo_feedback_private_index_name):
		es.indices.create(index=weibo_feedback_private_index_name,body=index_info,ignore=400)


def weibo_feedback_fans_mappings():  ## 粉丝提醒及回粉
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_fans_index_type:{
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
					'fans':{             
						'type':'long'
					},
					'weibos':{             
						'type':'long'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'fans_source':{
						'type':'string',
						'index':'not_analyzed'
					},
					'description':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
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
	#weibo_feedback_fans_index_name = weibo_feedback_fans_index_name_pre + ts2datetime(current_time)

	if not es.indices.exists(index=weibo_feedback_fans_index_name):
		es.indices.create(index=weibo_feedback_fans_index_name,body=index_info,ignore=400)

def weibo_feedback_follow_mappings():  ## 关注提醒及回粉
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_follow_index_type:{
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
					'fans':{             
						'type':'long'
					},
					'weibos':{             
						'type':'long'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'follow_source':{
						'type':'string',
						'index':'not_analyzed'
					},
					'description':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					},
					'sensitive_info':{
						'type':'long'
					},
					'sensitive_user':{
						'type':'long'
					},
					'group':{
						'type':'string',
						'index':'not_analyzed'
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
	#weibo_feedback_follow_index_name = weibo_feedback_follow_index_name_pre + ts2datetime(current_time)

	if not es.indices.exists(index=weibo_feedback_follow_index_name):
		es.indices.create(index=weibo_feedback_follow_index_name,body=index_info,ignore=400)

#uid、gid,gname,timestamp,members_uid

def weibo_create_group_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_feedback_group_index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'gid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'gname':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timestamp':{
						'type':'long'
					},
					'members':{
						'type':'string',
						'index':'not_analyzed'
					},
					'g_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'succ_uids':{
						'type':'string',
						'index':'not_analyzed'
					},
					'error_uids':{
						'type':'string',
						'index':'not_analyzed'
					},
					'member_count':{
						'type':'long'
					},
					'max_member':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_feedback_group_index_name):
		es.indices.create(index=weibo_feedback_group_index_name,body=index_info,ignore=400)

def weibo_private_white_uid_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			weibo_private_white_uid_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'white_uid_list':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_private_white_uid_index_name):
		es.indices.create(index=weibo_private_white_uid_index_name,body=index_info,ignore=400)


if __name__ == '__main__':
        
	current_time = int(time.time())
	datetime = ts2datetime(current_time)
        print 'datetime..',datetime	
	weibo_feedback_retweet_mappings(datetime)
	weibo_feedback_comment_mappings(datetime)
	weibo_feedback_at_mappings(datetime)
	weibo_feedback_like_mappings(datetime)
	weibo_feedback_private_mappings(datetime)

	weibo_feedback_follow_mappings()
	weibo_feedback_fans_mappings()
	weibo_create_group_mappings()
	weibo_private_white_uid_mappings()
        '''
	current_time = int(time.time())
	start_time = datetime2ts('2018-01-01')
	num_day = (current_time-start_time)/(24*3600)+1
	for i in range(num_day):
	    datetime = ts2datetime(start_time + i*24*3600)
            print 'datetime..',datetime	
	    weibo_feedback_retweet_mappings(datetime)
	    weibo_feedback_comment_mappings(datetime)
	    weibo_feedback_at_mappings(datetime)
	    weibo_feedback_like_mappings(datetime)
	    weibo_feedback_private_mappings(datetime)
        '''
