#-*-coding:utf-8-*-
import os
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import weibo_feedback_comment_index_name,weibo_feedback_comment_index_type,\
						weibo_feedback_retweet_index_name,weibo_feedback_retweet_index_type,\
						weibo_feedback_private_index_name,weibo_feedback_private_index_type,\
						weibo_feedback_at_index_name,weibo_feedback_at_index_type,\
						weibo_feedback_like_index_name,weibo_feedback_like_index_type,\
						weibo_feedback_follow_index_name,weibo_feedback_follow_index_type


def weibo_feedback_retweet_mappings():
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
						'type':'long'
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
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_feedback_retweet_index_name):
		es.indices.create(index=weibo_feedback_retweet_index_name,body=index_info,ignore=400)


def weibo_feedback_comment_mappings():
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
					'comment_type':{  ## make 发出的评论   receive 收到的评论
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_feedback_comment_index_name):
		es.indices.create(index=weibo_feedback_comment_index_name,body=index_info,ignore=400)


def weibo_feedback_at_mappings():
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
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_feedback_at_index_name):
		es.indices.create(index=weibo_feedback_at_index_name,body=index_info,ignore=400)


def weibo_feedback_like_mappings():
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
						'type':'long'
					},
					'root_mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_feedback_like_index_name):
		es.indices.create(index=weibo_feedback_like_index_name,body=index_info,ignore=400)



def weibo_feedback_private_mappings():
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
						'type':'long'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo_type':{   ## follow(关注人的)  粉丝  好友  陌生人
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_feedback_private_index_name):
		es.indices.create(index=weibo_feedback_private_index_name,body=index_info,ignore=400)


def weibo_feedback_follow_mappings():  ## 关注回粉
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
					'mid':{               
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
					}
				}
			}
		}
	}

	if not es.indices.exists(index=weibo_feedback_follow_index_name):
		es.indices.create(index=weibo_feedback_follow_index_name,body=index_info,ignore=400)



if __name__ == '__main__':
	weibo_feedback_retweet_mappings()
	weibo_feedback_comment_mappings()
	weibo_feedback_at_mappings()
	weibo_feedback_like_mappings()
	weibo_feedback_private_mappings()
	weibo_feedback_follow_mappings()
