# -*-coding:utf-8-*-

import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_xnr as es
from global_utils import fb_xnr_index_name,fb_xnr_index_type,\
                        fb_xnr_fans_followers_index_name,fb_xnr_fans_followers_index_type

def fb_xnr_mappings():
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            fb_xnr_index_type:{
                'properties':{
                    'submitter':{           # 当前管理用户
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'user_no':{                    #虚拟人编号数字
                        'type':'long'
                    },
                    'xnr_user_no':{               # 虚拟人编号
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'uid':{                     # uid
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'fb_mail_account':{        #所绑定的微博邮箱账号
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'fb_phone_account':{        #所绑定的微博手机账号
                        'type':'string',
                        'index':'not_analyzed'
                    },        
                    'nick_name':{                #昵称
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'password':{                #密码
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'create_time':{              #创建时间
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'domain_name':{              #渗透领域
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'role_name':{                 #角色定位
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'political_side':{         #政治倾向
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'psy_feature':{  #心理特征
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'business_goal':{            #业务目标
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'daily_interests':{   # 日常兴趣，字符串，以&连接
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'monitor_keywords':{   # 检测关键词，字符串，以&连接
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'age':{            #年龄
                        'type':'long'
                    },
                    'sex':{            #性别
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'location':{        #所在地
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'career':{            #职业
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'description':{        #个人描述
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'active_time':{              #活跃时间 
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'day_post_average':{            #日发帖量设置：从不，1-2，3-5……
                        'type':'string',
                        'index':'not_analyzed'
                    },            
                    'create_status':{        #虚拟人创建状态
                        'type':'long'           #0表示第一步完成，1表示第二步完成 2表示第三步完成，即最终完成创建。
                    }
                }
            }
        }
    }
    exist_indice=es.indices.exists(index=fb_xnr_index_name)
    if not exist_indice:
      
        #create
        es.indices.create(index=fb_xnr_index_name,body=index_info,ignore=400)


def fb_xnr_fans_followers_mappings():
    index_info={
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            fb_xnr_fans_followers_index_type:{
                'properties':{
                    'user_no':{                    #虚拟人编号，即用户ID
                        'type':'long'
                    },
                    'uid':{                     # uid
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'fans_list':{                #粉丝列表
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'followers_list':{                #关注列表
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'xnr_user_no':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'trace_follow_list':{
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }
    exist_indice=es.indices.exists(index=fb_xnr_fans_followers_index_name)
    if not exist_indice:
        
        #create
        es.indices.create(index=fb_xnr_fans_followers_index_name,body=index_info,ignore=400)

if __name__=='__main__':
  
    fb_xnr_mappings()
    fb_xnr_fans_followers_mappings()
