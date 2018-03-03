# -*-coding:utf-8-*-
import sys
import json
sys.path.append('../')
from global_utils import es_xnr as es,twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
								twitter_count_index_name_pre,twitter_count_index_type,\
								twitter_user_index_name,twitter_user_index_type

def twitter_flow_text_mappings(index_name,index_type='text'):

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
					'tid':{
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
					'root_tid':{
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

	if not exist_indice:
		es.indices.create(index=index_name,body=index_info,ignore=400)


def twitter_count_mappings(index_name):

	index_info = {
		'settings':{	
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			twitter_count_index_type:{
				'tid':{	
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


def twitter_user_mappings():
	index_info = {
		'settings':{
			'number_of_replicas':0,
			'number_of_shards':5
		},
		'mappings':{
			'user':{
				'properties':{
					'uid':{
						'type':'string',
						'index':'not_analyzed'
					},
					'username':{
						'type':'string',
						'index':'not_analyzed'
					},
					'userscreenname':{
						'type':'string',
						'index':'not_analyzed'
					},
					'description':{
						'type':'string',
						'index':'not_analyzed'
					},
					'create_at':{
						'type':'long'
					},
					'url':{
						'type':'string',
						'index':'no'
					},
					'profile_image_url':{
						'type':'string',
						'index':'no'
					},
					'profile_background_image_url':{
						'type':'string',
						'index':'no'
					},
					'location':{
						'type':'string',
						'index':'not_analyzed'
					},
					'timezone':{
						'type':'string',
						'index':'no'
					},
					'access_level':{	
						'type':'long'
					},
					'status_count':{
						'type':'long'
					},
					'followers_count':{
						'type':'long'
					},
					'friends_count':{
						'type':'long'
					},
					'favourites_count':{
						'type':'long'
					},
					'listed_count':{
						'type':'long'
					},
					'is_protected':{
						'type':'short'
					},
					'is_geo_enabled':{
						'type':'short'
					},
					'is_show_all_inline_media':{
						'type':'short'
					},
					'is_contributors_enable':{
						'type':'short'
					},
					'is_follow_requestsent':{
						'type':'short'
					},
					'is_profile_background_tiled':{
						'type':'short'
					},
					'is_profile_use_background_image':{
						'type':'short'
					},
					'is_translator':{
						'type':'short'
					},
					'is_verified':{
						'type':'short'
					},
					'utcoffset':{
						'type':'long'
					},
					'lang':{
						'type':'string',
						'index':'not_analyzed'
					},
					'bigger_profile_image_url':{
						'type':'string',
						'index':'no'
					},
					'bigger_profile_image_url_https':{
						'type':'string',
						'index':'no'
					},
					'mini_profile_image_url':{
						'type':'string',
						'index':'no'
					},
					'mini_profile_image_url_https':{
						'type':'string',
						'index':'no'
					},
					'original_profile_image_url':{
						'type':'string',
						'index':'no'
					},
					'original_profile_image_url_https':{
						'type':'string',
						'index':'no'
					},
					'profile_background_image_url_https':{
						'type':'string',
						'index':'no'
					},
					'profile_banner_ipad_url':{
						'type':'string',
						'index':'no'
					},
					'profile_banner_ipad_retina_url':{
						'type':'string',
						'index':'no'
					},
					'profile_banner_mobile_url':{
						'type':'string',
						'index':'no'
					},
					'profile_banner_mobile_retina_url':{
						'type':'string',
						'index':'no'
					},
					'profile_banner_retina_url':{
						'type':'string',
						'index':'no'
					},
					'profile_banner_url':{
						'type':'string',
						'index':'no'
					},
					'profile_image_url_https':{
						'type':'string',
						'index':'no'
					},
					'update_time':{
						'type':'long'
					},
					'sensitivity':{
						'type':'float'
					},
					'sensitivity2':{
						'type':'float'
					}
				}
			}
		}
	}

	if not es.indices.exists(index='twitter_user'):
		es.indices.create(index='twitter_user',body=index_info,ignore=400)


if __name__ == '__main__':

	#twitter_flow_text_mappings(flow_text_index_name)
	#twitter_count_mappings(count_index_name)
	twitter_user_mappings()
