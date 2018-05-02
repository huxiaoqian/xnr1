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
                        facebook_feedback_friends_index_name_pre,facebook_feedback_friends_index_type,\
                        facebook_feedback_friends_index_name

from time_utils import ts2datetime

'''
#字段说明
uid（对方uid）
photo_url（对方头像）
nick_name（对方昵称）
mid（对方互动帖子id）
timestamp（对方互动时间戳）
text（对方互动内容）
sex（对方性别）
geo（对方地理位置）
friends（对方好友数）
profile_url（对方个人资料页链接）
update_time（爬取时间戳）
root_text（原贴内容）
root_mid（原贴id）
root_uid（虚拟人uid）
root_nick_name（虚拟人昵称）
facebook_type（对方类别）
sensitive_info（敏感信息）
sensitive_user（敏感用户）
comment_type（"make"或者"receive"，分别表示虚拟人发出的或者收到的）
private_type（"make"或者"receive"，分别表示虚拟人发出的或者收到的。如不能区分则为：“unknown”，此时将文本仅保存在text字段中即可。）
retweet（互动帖子转发数）
comment（互动帖子评论数）
like（互动帖子点赞数）
'''
# 点赞
def facebook_feedback_like_mappings(facebook_feedback_like_index_name):
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
                    'timestamp':{
                        'type':'long'
                    },
                    'text':{        #xxx点赞了
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'update_time':{
                        'type':'long'
                    },
                    'root_text':{        
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
                    'root_nick_name':{   
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'facebook_type':{   
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_info':{
                        'type':'long'
                    },
                    'sensitive_user':{
                        'type':'long'
                    },

                }
            }
        }
    }

    #current_time = time.time()
    #facebook_feedback_like_index_name = facebook_feedback_like_index_name_pre + ts2datetime(current_time)

    if not es.indices.exists(index=facebook_feedback_like_index_name):
        es.indices.create(index=facebook_feedback_like_index_name,body=index_info,ignore=400)

# 分享
def facebook_feedback_retweet_mappings(facebook_feedback_retweet_index_name):
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
                    'text':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'update_time':{
                        'type':'long'
                        }
                    },
                    'root_text':{
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
                    'root_nick_name':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'facebook_type':{  
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_info':{
                        'type':'long'
                    },
                    'sensitive_user':{
                        'type':'long'
                    },
                    'retweet':{
                        'type':'long'
                    },
                    'comment':{
                        'type':'long'
                    },
                    'like':{
                        'type':'long'
                    },
            }
        }
    }

    #current_time = time.time()
    #facebook_feedback_retweet_index_name = facebook_feedback_retweet_index_name_pre + ts2datetime(current_time)
    
    if not es.indices.exists(index=facebook_feedback_retweet_index_name):
        es.indices.create(index=facebook_feedback_retweet_index_name,body=index_info,ignore=400)

# 标记
def facebook_feedback_at_mappings(facebook_feedback_at_index_name):
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
                    'text':{    #xxx提到了你
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'update_time':{
                        'type':'long'
                    },
                    'root_uid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'root_nick_name':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'facebook_type':{ 
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_info':{
                        'type':'long'
                    },
                    'sensitive_user':{
                        'type':'long'
                    },

                }
            }
        }
    }

    #current_time = time.time()
    #facebook_feedback_at_index_name = facebook_feedback_at_index_name_pre + ts2datetime(current_time)

    if not es.indices.exists(index=facebook_feedback_at_index_name):
        es.indices.create(index=facebook_feedback_at_index_name,body=index_info,ignore=400)


# 评论
def facebook_feedback_comment_mappings(facebook_feedback_comment_index_name):
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
                    'update_time':{
                        'type':'long'
                    },
                    'root_text':{
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
                    'root_nick_name':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'facebook_type':{ 
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_info':{
                        'type':'long'
                    },
                    'sensitive_user':{
                        'type':'long'
                    },
                    'comment_type':{  ## make 发出的评论   receive 收到的评论
                        'type':'string',
                        'index':'not_analyzed'
                    },

                }
            }
        }
    }

    #current_time = time.time()
    #facebook_feedback_comment_index_name = facebook_feedback_comment_index_name_pre + ts2datetime(current_time)

    if not es.indices.exists(index=facebook_feedback_comment_index_name):
        es.indices.create(index=facebook_feedback_comment_index_name,body=index_info,ignore=400)


# 私信
def facebook_feedback_private_mappings(facebook_feedback_private_index_name):
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
                    'timestamp':{
                        'type':'long'
                    },
                    'text':{             
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'update_time':{
                        'type':'long'
                    },
                    'root_text':{             
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'root_uid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'root_nick_name':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'facebook_type':{   
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'private_type':{ #  private_type（"make"或者"receive"，分别表示虚拟人发出的或者收到的。如不能区分则为：“unknown”，此时将文本仅保存在text字段中即可。）
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_info':{
                        'type':'long'
                    },
                    'sensitive_user':{
                        'type':'long'
                    },

                }
            }
        }
    }

    #current_time = time.time()
    #facebook_feedback_private_index_name = facebook_feedback_private_index_name_pre + ts2datetime(current_time)

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
                    'friends':{             
                        'type':'long'
                    },
                    'profile_url':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'update_time':{
                        'type':'long'
                    },
                    'root_uid':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'root_nick_name':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'facebook_type':{ 
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_info':{
                        'type':'long'
                    },
                    'sensitive_user':{
                        'type':'long'
                    },
                }
            }
        }
    }

    #current_time = time.time()
    #facebook_feedback_friends_index_name = facebook_feedback_friends_index_name_pre + ts2datetime(current_time)

    if not es.indices.exists(index=facebook_feedback_friends_index_name):
        es.indices.create(index=facebook_feedback_friends_index_name,body=index_info,ignore=400)


if __name__ == '__main__':

    #current_time = time.time()
    #index_name = index_name_pre + ts2datetime(current_time)

    #index_name = ''
    # facebook_feedback_like_mappings(index_name)
    # facebook_feedback_retweet_mappings(index_name)
    # facebook_feedback_at_mappings(index_name)
    # facebook_feedback_comment_mappings(index_name)
    # facebook_feedback_private_mappings(index_name)
    facebook_feedback_friends_mappings()