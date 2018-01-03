# -*-coding:utf-8-*-

from global_utils import es_xnr,fb_xnr_retweet_timing_list_index_name,fb_xnr_retweet_timing_list_index_type

def retweet_timing_list_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			fb_xnr_retweet_timing_list_index_type:{
				'properties':{
					'xnr_user_no':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'nick_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'photo_url':{
						'type':'string',
						'index':'no'
					},
					'timestamp':{         # 该微博发布时间
						'type':'long'
					},
					'timestamp_set':{      # 计划发送时间
						'type':'long'
					},
					'timestamp_post':{      # 实际发送时间
						'type':'long'
					},
					'compute_status':{     # 发送状态  0- 未发送   1- 已发送
						'type':'long'
					}
				}
			}
		}
	}

	if not es_xnr.indices.exists(index=fb_xnr_retweet_timing_list_index_name):

		es_xnr.indices.create(index=fb_xnr_retweet_timing_list_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	retweet_timing_list_mappings()