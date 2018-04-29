# -*-coding:utf-8-*-
import sys
import json
sys.path.append('../')
from global_utils import es_xnr as es,facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
								facebook_count_index_name_pre,facebook_count_index_type,\
							facebook_user_index_name,facebook_user_index_type

def facebook_flow_text_mappings(index_name,index_type='text'):

	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5,
			'analysis':{
				'analyzer':{
					'my_analyzer':{
						'type':'pattern',
						'pattern':'&'
					}
				}
			}
		},
		'mappings':{
			index_type:{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'fid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'text':{
						'type':'string',
						'index':'not_analyzed'
					},
					'text_ch':{
						'type':'string',
						'index':'not_analyzed'
					},
					'flag_ch':{	# text是否为中文   0 - 否  1 - 是
						'type':'short'
					},
					'picture_url':{
						'type':'string',
						'index':'not_analyzed'
					},
					'geo':{
						'type': 'string',
						'analyzer': 'my_analyzer'
					},
					'ip':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'keywords_dict':{
						'type':'string',
						'index':'no'
					},
					'keywords_string':{
						'type':'string',
						'analyzer':'my_analyzer'
					},
					'sensitive_words_dict':{
						'type':'string',
						'index':'no'
					},
					'sensitive_words_string':{
						'type':'string',
						'analyzer':'my_analyzer'
					},
					'sensitive':{
						'type':'long'
					},
					'sentiment':{
						'type':'long'
					},
					'message_type':{
						'type':'long'
					},
					'directed_uid':{
						'type':'long',
					},
					'directed_uname':{
						'type': 'string',
						'index': 'not_analyzed'
					},
					'root_uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'root_fid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'share':{
						'type':'long'
					},
					'comment':{
						'type':'long'
					},
					'favorite':{
						'type':'long'
					},
					'timestamp':{
						'type':'long'
					},
					'update_time':{
						'type':'long'
					},
                    'fansnum':{
                        'type':'long'
                    },
                    'followersnum':{
                        'type':'long'
                    },
                    'tweets_num':{
                        'type':'long'
                    }
				}
			}
		}
	}

	exist_indice = es.indices.exists(index=index_name)
	print 'index_name...',index_name
	if not exist_indice:
		#print 'create...',index_name
		print es.indices.create(index=index_name,body=index_info,ignore=400)


def facebook_count_mappings(index_name):

	index_info = {
		'settings':{	
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_count_index_type:{
				'uid':{
					'type':'string',
					'index':'not_analyzed'
				},
				'fid':{	
					'type':'string',
					'index':'not_analyzed'
				},
				'share':{
					'type':'long'
				},
				'comment':{
					'type':'long'
				},
				'favorite':{
					'type':'long'
				},
				'update_time':{
					'type':'long'
				}
			}
		}
	}

	if not es.indices.exists(index=index_name):
		es.indices.create(index=index_name,body=index_info,ignore=400)


def facebook_user_mappings(index_name):
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			facebook_user_index_type:{
				'properties':{
					'uid':{  # 对应txt中id
						'type':'string',
						'index':'not_analyzed'
					},
					'work':{
						'type':'string',
						'index':'not_analyzed'
					},
					'website':{
						'type':'string',
						'index':'no'
					},
					'location':{
						'type':'string',
						'index':'not_analyzed'
					},
					'link':{
						'type':'string',
						'index':'not_analyzed'
					},
					'locale':{
						'type':'string',
						'index':'not_analyzed'
					},
					'education':{
						'type':'string',
						'index':'not_analyzed'
					},
					'update_time':{    # 原数据 updated_time
						'type':'long'
					},
					'relationship_status':{
						'type':'string',
						'index':'not_analyzed'
					},
					'first_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'languages':{	
						'type':'string',
						'index':'not_analyzed'
					},
					'username':{
						'type':'string',
						'index':'not_analyzed'
					},
					'quotes':{
						'type':'string',
						'index':'not_analyzed'
					},
					'bio':{
						'type':'string',
						'index':'not_analyzed'
					},
					'name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'last_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'gender':{
						'type':'string',
						'index':'not_analyzed'
					},
					'favorite_athletes':{
						'type':'string',
						'index':'not_analyzed'
					},
					'parking':{
						'type':'string',
						'index':'not_analyzed'
					},
					'checkins':{
						'type':'long'
					},
					'about':{
						'type':'string',
						'index':'not_analyzed'
					},
					'is_community_page':{
						'type':'boolean'
					},
					'founded':{     # 建立时间
						'type':'long'
					},
					'category':{
						'type':'string',
						'index':'not_analyzed'
					},
					'cover':{
						'type':'string',
						'index':'not_analyzed'
					},
					'has_added_app':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mission':{
						'type':'string',
						'index':'not_analyzed'
					},
					'description':{
						'type':'string',
						'index':'not_analyzed'
					},
					'likes':{
						'type':'long'
					},
					'were_here_count':{
						'type':'long'
					},
					'can_post':{
						'type':'boolean'
					},
					'talking_about_count':{
						'type':'long'
					},
					'is_published':{
						'type':'boolean'
					},
					'favorite_teams':{
						'type':'string',
						'index':'not_analyzed'
					},
					'birthday':{
						'type':'string',
						'index':'not_analyzed'
					},
					'birthyear':{    # 额外添加  默认为0
						'type':'long'
					},
					'phone':{
						'type':'string',
						'index':'not_analyzed'
					},
					'company_overview':{
						'type':'string',
						'index':'not_analyzed'
					},
					'products':{
						'type':'string',
						'index':'not_analyzed'
					},
					'category_list':{
						'type':'string'
					},
					'hometown':{
						'type':'string',
						'index':'not_analyzed'
					},
					'interested_in':{
						'type':'string',
						'index':'not_analyzed'
					},
					'mobile_phone':{
						'type':'string',
						'index':'not_analyzed'
					},
					'email':{
						'type':'string',
						'index':'not_analyzed'
					},
					'icon':{
						'type':'string',
						'index':'not_analyzed'
					},
					'privacy':{
						'type':'string',
						'index':'not_analyzed'
					},
					'version':{
						'type':'long'
					},
					'personal_info':{
						'type':'string',
						'index':'not_analyzed'
					},
					'affiliation':{
						'type':'string',
						'index':'not_analyzed'
					},
					'inspirational_people':{
						'type':'string',
						'index':'not_analyzed'
					},
					'political':{
						'type':'string',
						'index':'not_analyzed'
					},
					'religion':{
						'type':'string',
						'index':'not_analyzed'
					},
					'awards':{
						'type':'string',
						'index':'not_analyzed'
					},
					'middle_name':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}
		}
	}

	if not es.indices.exists(index_name):
		es.indices.create(index=index_name,body=index_info,ignore=400)


if __name__ == '__main__':

	#facebook_flow_text_mappings(flow_text_index_name)
	#facebook_count_mappings(count_index_name)
	facebook_user_mappings(facebook_user_index_name)
