# -*- coding:utf-8 -*-
import sys
import json
sys.path.append('../')
from global_utils import es_xnr as es, new_tw_xnr_flow_text_index_name_pre, \
                new_tw_xnr_flow_text_index_type


def new_tw_xnr_flow_text_mappings(index_name):
    index_info = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'my_analyzer':{
                            'type': 'pattern',
                            'pattern': '&'
                        }
                    }
                }
            },
            'mappings':{
                'text':{
                    'properties':{
                        'task_source':{  # 日常发帖，热点跟随，业务发帖，此处空着
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'xnr_user_no':{ #虚拟人编号
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'uid':{ #虚拟人uid
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'text':{ #文本内容
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'picture_url':{ #图片url
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'vedio_url':{ #视频url
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'user_fansnum':{ #粉丝数
                            'type':'long'
                        },
                        'user_followersum':{ #关注者数
                            'type':'long'
                        },
                        'weibos_sum':{ #发帖总数
                            'type':'long'
                        },
                        'tid':{ #帖子id
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'ip':{ #IP地址
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'directed_uid':{#直接转发帖子的源uid
                            'type':'long',
                            },
                        'directed_uname':{#直接转发帖子的源用户昵称
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'timestamp':{#时间戳
                            'type': 'long'
                            },
                        'sentiment': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'geo':{#地理位置
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'keywords_dict':{#关键词dict
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'keywords_string':{ #关键词string
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'sensitive_words_dict':{#敏感词dict
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'sensitive_words_string':{#敏感词string
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'message_type':{#数据类型，、原创——1、转发——2、评论——3
                            'type': 'long'
                            },
                        'root_uid':{#源头帖子的uid
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'root_tid':{#源头帖子的tid
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                         # uncut weibo text
                        'origin_text':{#源头帖子的文本
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'origin_keywords_dict':{#源头帖子的dict
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'origin_keywords_string':{#源头帖子的string
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'comment':{#评论数
                            'type':'long'
                            },
                        'sensitive':{#敏感度
                            'type':'long'
                            },
                        'retweeted':{#转发数
                            'type':'long'
                            },
                        'like':{ #点赞数
                            'type':'long'
                        },
                        'topic_field_first': {
                            'index': 'not_analyzed',
                            'type': 'string'
                        },
                        'topic_field':{
                            'type':'string',
                            'index':'not_analyzed'
                        }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)

def tw_daily_inerests_flow_text_mappings(index_name):

    index_info = {
        'settings':{
            'number_of_replicas':0,
            'bumber_of_shards':5
        },
        'mappings':{
            'text':{
                'properties':{
                    'timestamp':{
                        'type':'long'
                    },
                    'content':{
                        'type':'string',
                        'index':'no'
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=index_name)

    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)

# if __name__ == '__main__':

#     new_tw_xnr_flow_text_mappings(index_name)
# if __name__=='__main__':
#     new_xnr_flow_text_index_list = ['new_tw_xnr_flow_text__2017-10-16','new_tw_xnr_flow_text__2017-10-17','new_tw_xnr_flow_text__2017-10-18',\
# 'new_tw_xnr_flow_text__2017-10-19','new_tw_xnr_flow_text__2017-10-20','new_tw_xnr_flow_text__2017-10-21',\
# 'new_tw_xnr_flow_text__2017-10-22','new_tw_xnr_flow_text__2017-10-23','new_tw_xnr_flow_text__2017-10-24',\
# 'new_tw_xnr_flow_text__2017-10-25','new_tw_xnr_flow_text__2017-12-04','new_tw_xnr_flow_text__2018-01-05',\
# 'new_tw_xnr_flow_text__2018-01-06','new_tw_xnr_flow_text__2018-01-07','new_tw_xnr_flow_text__2018-01-08',\
# 'new_tw_xnr_flow_text__2018-01-10','new_tw_xnr_flow_text__2018-01-15','new_tw_xnr_flow_text__2018-01-18',\
# 'new_tw_xnr_flow_text__2018-01-19','new_tw_xnr_flow_text__2018-01-23','new_tw_xnr_flow_text__2018-01-24',\
# 'new_tw_xnr_flow_text__2018-01-26','new_tw_xnr_flow_text__2018-01-30','new_tw_xnr_flow_text__2018-04-01',\
# 'new_tw_xnr_flow_text__2018-04-03','new_tw_xnr_flow_text__2018-04-09','new_tw_xnr_flow_text__2018-04-12']
#     es.indices.put_mapping(index=new_xnr_flow_text_index_list, doc_type=new_tw_xnr_flow_text_index_type, \
#             body={'properties':{'topic_field': {'index': 'not_analyzed','type': 'string'},\
#             }}, ignore=400)