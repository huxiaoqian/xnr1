#-*- coding: utf-8 -*-
'''
log management function
'''
import os
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
sys.path.append('../')
# import sqlite
import sqlite3
from parameter import USER_XNR_NUM,DAY,MAX_VALUE
from time_utils import ts2datetime,datetime2ts
from global_utils import es_flow_text,flow_text_index_name_pre,flow_text_index_type
from global_utils import es_xnr,weibo_xnr_index_name,weibo_xnr_index_type,\
                         xnr_flow_text_index_name_pre,xnr_flow_text_index_type,\
                         weibo_xnr_retweet_timing_list_index_name,weibo_xnr_retweet_timing_list_index_type,\
                         weibo_xnr_save_like_index_name,weibo_xnr_save_like_index_type,\
                         weibo_feedback_private_index_name_pre,weibo_feedback_private_index_type,\
                         weibo_xnr_corpus_index_name,weibo_xnr_corpus_index_type,\
                         weibo_speech_warning_index_name,weibo_speech_warning_index_type,\
                         weibo_xnr_timing_list_index_name,weibo_xnr_timing_list_index_type,\
                         weibo_domain_index_name,weibo_domain_index_type,\
                         weibo_sensitive_words_index_name,weibo_sensitive_words_index_type,\
                         weibo_date_remind_index_name,weibo_date_remind_index_type,\
                         weibo_hidden_expression_index_name,weibo_hidden_expression_index_type,\
                         weibo_log_management_index_name,weibo_log_management_index_type,\
                         qq_xnr_index_name,qq_xnr_index_type,\
                         qq_xnr_history_count_index_name_pre,qq_xnr_history_count_index_type,\
                         qq_report_management_index_name,qq_report_management_index_type,\
                         wx_xnr_index_name,wx_xnr_index_type,\
                         wx_xnr_history_count_index_name,wx_xnr_history_count_index_type,\
                         wx_report_management_index_name,wx_report_management_index_type,\
                         weibo_report_management_index_name_pre,weibo_report_management_index_type,\
                         weibo_warning_corpus_index_name,weibo_warning_corpus_index_type


#境外通道
from global_utils import es_xnr_2,tw_xnr_index_name,tw_xnr_index_type,\
                         tw_xnr_flow_text_index_name_pre,tw_xnr_flow_text_index_type,\
                         tw_xnr_retweet_timing_list_index_name,tw_xnr_retweet_timing_list_index_type,\
                         twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
                         twitter_xnr_save_like_index_name,twitter_xnr_save_like_index_type,\
                         twitter_feedback_private_index_name_pre,twitter_feedback_private_index_type,\
                         twitter_xnr_corpus_index_name,twitter_xnr_corpus_index_type,\
                         twitter_report_management_index_name_pre,twitter_report_management_index_type,\
                         twitter_warning_corpus_index_name,twitter_warning_corpus_index_type,\
                         tw_xnr_timing_list_index_name,tw_xnr_timing_list_index_type,\
                         fb_xnr_index_name,fb_xnr_index_type,\
                         fb_xnr_flow_text_index_name_pre,fb_xnr_flow_text_index_type,\
                         fb_xnr_retweet_timing_list_index_name,fb_xnr_retweet_timing_list_index_type,\
                         facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
                         facebook_xnr_save_like_index_name,facebook_xnr_save_like_index_type,\
                         facebook_feedback_private_index_name_pre,facebook_feedback_private_index_type,\
                         facebook_xnr_corpus_index_name,facebook_xnr_corpus_index_type,\
                         facebook_report_management_index_name_pre,facebook_report_management_index_type,\
                         facebook_warning_corpus_index_name,facebook_warning_corpus_index_type,\
                         fb_xnr_timing_list_index_name,fb_xnr_timing_list_index_type





#连接数据库,获取账户列表
def get_user_account_list():     
    #cx = sqlite3.connect("/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/flask-admin.db")
    cx = sqlite3.connect("/home/xnr1/xnr_0429/xnr/flask-admin.db") 
    cu=cx.cursor()
    cu.execute("select email from user") 
    user_info = cu.fetchall()
    cx.close()
    return user_info


#根据账户名称查询所管理的微博虚拟人
def get_user_xnr_list(user_account):
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'term':{'submitter':user_account}
        		}
        	}
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list


#获取微博虚拟人的uidlist
def get_xnr_uid_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'term':{'create_status':2}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
        xnr_uid_list=[]
        for item in user_result:
            xnr_uid_list.append(item['_source']['uid'])
    except:
        xnr_uid_list=[]
    return xnr_uid_list


##微博日志文件操作内容模块
#创建虚拟人
def create_xnr_number(user_account,start_time,end_time):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    number=len(xnr_user_no_list)
    return number

#发帖统计
def count_type_posting(task_source,operate_date,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'term':{'task_source':task_source}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    xnr_flow_text_index_name=xnr_flow_text_index_name_pre+operate_date
    try:
        es_result=es_xnr.search(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#跟踪转发
def count_tweet_retweet(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'timestamp_set':{'gte':start_time,'lt':end_time}}},
                            {'term':{'compute_status':1}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=weibo_xnr_retweet_timing_list_index_name,doc_type=weibo_xnr_retweet_timing_list_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number

#上报预警记录
def count_report_type(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'report_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        weibo_report_management_index_name = weibo_report_management_index_name_pre + ts2datetime(end_time)
        es_result=es_xnr.search(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number

#转发、评论
def count_retweet_comment_operate(operate_type,operate_date,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'uid':uid_list}},
                            {'term':{'message_type':operate_type}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    flow_text_index_name=flow_text_index_name_pre+operate_date
    if es_flow_text.indices.exists(index=flow_text_index_name):
        es_result=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    else:
        number=0
    return number


#点赞
def count_like_operate(start_time,end_time,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'root_uid':uid_list}},
                            {'range':{'update_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=weibo_xnr_save_like_index_name,doc_type=weibo_xnr_save_like_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#私信
def count_private_message(start_time,end_time,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'root_uid':uid_list}},
                            {'term':{'private_type':'make'}},
                            {'range':{'timestamp':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        weibo_feedback_private_index_name = weibo_feedback_private_index_name_pre + ts2datetime(end_time)
        es_result=es_xnr.search(index=weibo_feedback_private_index_name,doc_type=weibo_feedback_private_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number

#加入语料库
def count_add_corpus(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#加入预警库
def count_add_warming_speech(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=weibo_warning_corpus_index_name,doc_type=weibo_warning_corpus_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#添加定时任务
def count_add_timing_task(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=weibo_xnr_timing_list_index_name,doc_type=weibo_xnr_timing_list_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#领域创建
def count_create_domain(user_account,start_time,end_time):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#业务知识库
def count_create_business(user_account,start_time,end_time,index_name,index_type):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=index_name,doc_type=index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number

##QQ
#根据账户名称查询所管理的微博虚拟人
def get_user_qqxnr_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'submitter':user_account}
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list


##QQ创建虚拟人
def create_qqxnr_number(user_account,start_time,end_time):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'range':{'create_ts':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    number=len(xnr_user_no_list)
    return number


##QQ操作统计-今日发言量
def count_qqxnr_daily_post(date_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no_list}},
                            {'term':{'date_time':date_time}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    qq_xnr_history_count_index_name = qq_xnr_history_count_index_name_pre + date_time
    try:
        user_result=es_xnr.search(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,body=query_body)['hits']['hits']
        number=0
        for item in user_result:
            number=number+item['_source']['daily_post_num']
    except:
        number=0
    return number 

#QQ上报
def count_qq_report_number(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'report_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=qq_report_management_index_name,doc_type=qq_report_management_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#微信虚拟人创建
def create_weixinxnr_number(user_account,start_time,end_time):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'range':{'create_ts':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=wx_xnr_index_name,doc_type=wx_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    number=len(xnr_user_no_list)
    return number	


#微信虚拟人列表
def get_user_weixinxnr_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'submitter':user_account}
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=wx_xnr_index_name,doc_type=wx_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list


#微信发言量
def count_weixinxnr_daily_post(date_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'xnr_user_no':xnr_user_no_list}},
                            {'term':{'date_time':date_time}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    # qq_xnr_history_count_index_name = qq_xnr_history_count_index_name_pre + date_time
    try:
        user_result=es_xnr.search(index=wx_xnr_history_count_index_name,doc_type=wx_xnr_history_count_index_type,body=query_body)['hits']['hits']
        number=0
        for item in user_result:
            number=number+item['_source']['daily_post_num']
    except:
        number=0
    return number 

#微信上报
def count_weixin_report_number(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'report_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr.search(index=wx_report_management_index_name,doc_type=wx_report_management_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#根据账户名称查询所管理的twitter虚拟人
def get_user_twxnr_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'submitter':user_account}
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr_2.search(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list


#获取tw虚拟人的uidlist
def get_twxnr_uid_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'term':{'create_status':2}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr_2.search(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,body=query_body)['hits']['hits']
        xnr_uid_list=[]
        for item in user_result:
            xnr_uid_list.append(item['_source']['uid'])
    except:
        xnr_uid_list=[]
    return xnr_uid_list


##tw日志文件操作内容模块
#创建虚拟人
def create_twxnr_number(user_account,start_time,end_time):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr_2.search(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    number=len(xnr_user_no_list)
    return number


#tw发帖统计
def count_type_twposting(task_source,operate_date,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'term':{'task_source':task_source}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    xnr_flow_text_index_name=tw_xnr_flow_text_index_name_pre+operate_date
    try:
        es_result=es_xnr_2.search(index=xnr_flow_text_index_name,doc_type=tw_xnr_flow_text_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#tw跟踪转发
def count_tw_tweet_retweet(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'timestamp_set':{'gte':start_time,'lt':end_time}}},
                            {'term':{'compute_status':1}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=tw_xnr_retweet_timing_list_index_name,doc_type=tw_xnr_retweet_timing_list_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#tw转发、评论
def count_tw_retweet_comment_operate(operate_type,operate_date,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'uid':uid_list}},
                            {'term':{'message_type':operate_type}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    flow_text_index_name=twitter_flow_text_index_name_pre+operate_date
    if es_xnr_2.indices.exists(index=flow_text_index_name):
        es_result=es_xnr_2.search(index=flow_text_index_name,doc_type=twitter_flow_text_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    else:
        number=0
    return number


#tw点赞
def count_tw_like_operate(start_time,end_time,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'root_uid':uid_list}},
                            {'range':{'update_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=twitter_xnr_save_like_index_name,doc_type=twitter_xnr_save_like_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#tw私信
def count_tw_private_message(start_time,end_time,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'root_uid':uid_list}},
                            {'term':{'private_type':'make'}},
                            {'range':{'timestamp':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        twitter_feedback_private_index_name = twitter_feedback_private_index_name_pre + ts2datetime(end_time)
        es_result=es_xnr_2.search(index=twitter_feedback_private_index_name,doc_type=twitter_feedback_private_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#tw加入语料库
def count_tw_add_corpus(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=twitter_xnr_corpus_index_name,doc_type=twitter_xnr_corpus_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#tw上报预警记录
def count_tw_report_type(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'report_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        twitter_report_management_index_name = twitter_report_management_index_name_pre + ts2datetime(end_time)
        es_result=es_xnr_2.search(index=twitter_report_management_index_name,doc_type=twitter_report_management_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#tw加入预警库
def count_tw_add_warming_speech(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=twitter_warning_corpus_index_name,doc_type=twitter_warning_corpus_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#tw添加定时任务
def count_tw_add_timing_task(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=tw_xnr_timing_list_index_name,doc_type=tw_xnr_timing_list_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number



##fb日志文件操作内容模块
#创建虚拟人
def create_fbxnr_number(user_account,start_time,end_time):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr_2.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    number=len(xnr_user_no_list)
    return number


#根据账户名称查询所管理的fb虚拟人
def get_user_fbxnr_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'submitter':user_account}
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr_2.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list



#获取fb虚拟人的uidlist
def get_fbxnr_uid_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{'submitter':user_account}},
                            {'term':{'create_status':2}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr_2.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
        xnr_uid_list=[]
        for item in user_result:
            xnr_uid_list.append(item['_source']['uid'])
    except:
        xnr_uid_list=[]
    return xnr_uid_list


#fb发帖统计
def count_type_fbposting(task_source,operate_date,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'term':{'task_source':task_source}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    xnr_flow_text_index_name=fb_xnr_flow_text_index_name_pre+operate_date
    try:
        es_result=es_xnr_2.search(index=xnr_flow_text_index_name,doc_type=fb_xnr_flow_text_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#fb跟踪转发
def count_fb_tweet_retweet(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'timestamp_set':{'gte':start_time,'lt':end_time}}},
                            {'term':{'compute_status':1}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=fb_xnr_retweet_timing_list_index_name,doc_type=fb_xnr_retweet_timing_list_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number



#fb转发、评论
def count_fb_retweet_comment_operate(operate_type,operate_date,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'uid':uid_list}},
                            {'term':{'message_type':operate_type}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    flow_text_index_name=facebook_flow_text_index_name_pre+operate_date
    if es_xnr_2.indices.exists(index=flow_text_index_name):
        es_result=es_xnr_2.search(index=flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    else:
        number=0
    return number


#fb点赞
def count_fb_like_operate(start_time,end_time,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'root_uid':uid_list}},
                            {'range':{'update_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=facebook_xnr_save_like_index_name,doc_type=facebook_xnr_save_like_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#fb私信
def count_fb_private_message(start_time,end_time,uid_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'root_uid':uid_list}},
                            {'term':{'private_type':'make'}},
                            {'range':{'timestamp':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        facebook_feedback_private_index_name = facebook_feedback_private_index_name_pre + ts2datetime(end_time)
        es_result=es_xnr_2.search(index=facebook_feedback_private_index_name,doc_type=facebook_feedback_private_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#fb加入语料库
def count_fb_add_corpus(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=facebook_xnr_corpus_index_name,doc_type=facebook_xnr_corpus_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#fb上报预警记录
def count_fb_report_type(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'report_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        facebook_report_management_index_name = facebook_report_management_index_name_pre + ts2datetime(end_time)
        es_result=es_xnr_2.search(index=facebook_report_management_index_name,doc_type=facebook_report_management_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#fb加入预警库
def count_fb_add_warming_speech(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=facebook_warning_corpus_index_name,doc_type=facebook_warning_corpus_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number


#fb添加定时任务
def count_fb_add_timing_task(start_time,end_time,xnr_user_no_list):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'xnr_user_no':xnr_user_no_list}},
                            {'range':{'create_time':{'gte':start_time,'lt':end_time}}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es_xnr_2.search(index=fb_xnr_timing_list_index_name,doc_type=fb_xnr_timing_list_index_type,body=query_body)['hits']['hits']
        number=len(es_result)
    except:
        number=0
    return number



#日志生成文件组织
def create_user_log():
    now_time=int(time.time())
    today_datetime=datetime2ts(ts2datetime(now_time))
    start_time=today_datetime-DAY    #前一天0点
    end_time=today_datetime          #定时文件启动的0点
    operate_date=ts2datetime(start_time)

    #查询账户列表
    user_name_list=get_user_account_list()

    mark_list=[]
    #查询账户所管理的虚拟人
    for user_account in user_name_list:
        #对应账户的日志ID
        #print 'user_account',user_account,type(user_account)
        #print 'operate_date',operate_date,type(operate_date)
        user_account=list(user_account)[0]
        log_id=str(user_account)+'_'+operate_date
        print log_id
        log_content_dict=dict()

###########################################################################
#微博部分日志
###########################################################################

        #账户是否创建虚拟人
        xnr_number=create_xnr_number(user_account,start_time,end_time)
        if xnr_number > 0:
            log_content_dict[u'创建微博虚拟人']=xnr_number
        else:
            pass

        xnr_user_no_list=get_user_xnr_list(user_account)
        xnr_uid_list=get_xnr_uid_list(user_account)
        
        #遍历各个模块，验证所管理虚拟人是否进行操作
        ##################发帖操作#################
        #日常发帖
        daily_post_type='daily_post'
        daily_post_num=count_type_posting(daily_post_type,operate_date,xnr_user_no_list)
        if daily_post_num > 0:
            log_content_dict[u'微博-日常发帖']=daily_post_num
        else:
            pass

        #业务发帖
        business_post_type='business_post'
        business_post_num=count_type_posting(business_post_type,operate_date,xnr_user_no_list)
        if business_post_num > 0:
            log_content_dict[u'微博-业务发帖']=business_post_num
        else:
            pass

        #热点跟随
        hot_post_type='hot_post'
        hot_post_num=count_type_posting(hot_post_type,operate_date,xnr_user_no_list)
        if hot_post_num > 0:
            log_content_dict[u'微博-热点跟随']=hot_post_num
        else:
            pass

        #跟踪转发
        retweet_timing_num=count_tweet_retweet(start_time,end_time,xnr_user_no_list)
        if retweet_timing_num > 0:
            log_content_dict[u'微博-跟踪转发']=retweet_timing_num
        else:
            pass

        ##################社交操作：转发、评论、点赞#################
        #转发
        retweet_type='3'
        retweet_num=count_retweet_comment_operate(retweet_type,operate_date,xnr_uid_list)
        if retweet_num > 0:
            log_content_dict[u'微博-转发']=retweet_num
        else:
            pass

        #评论
        comment_type='2'
        comment_num=count_retweet_comment_operate(comment_type,operate_date,xnr_uid_list)
        if comment_num > 0:
            log_content_dict[u'微博-评论']=comment_num
        else:
            pass

        #点赞
        like_num=count_like_operate(start_time,end_time,xnr_uid_list)
        if like_num > 0:
            log_content_dict[u'微博-点赞']=like_num
        else:
            pass

        #私信
        private_message_num=count_private_message(start_time,end_time,xnr_uid_list)
        if private_message_num > 0:
            log_content_dict[u'微博-私信']=private_message_num
        else:
            pass

        ##################加入语料#################
        add_corpus_num=count_add_corpus(start_time,end_time,xnr_user_no_list)
        if add_corpus_num > 0:
            log_content_dict[u'微博-加入语料']=add_corpus_num
        else:
            pass

        ##################上报操作#################
        report_num=count_report_type(start_time,end_time,xnr_user_no_list)
        if report_num > 0:
            log_content_dict[u'微博-上报']=report_num
        else:
            pass

        ##################加入预警库#################
        add_warming_num=count_add_warming_speech(start_time,end_time,xnr_user_no_list)
        if add_warming_num > 0:
            log_content_dict[u'微博-加入预警库']=add_warming_num
        else:
            pass

        ##################定时任务#################
        timing_task_num=count_add_timing_task(start_time,end_time,xnr_user_no_list)
        if timing_task_num > 0:
            log_content_dict[u'微博-创建定时任务']=timing_task_num
        else:
            pass

###########################################################################
###########################################################################

        ##################领域创建#################
        create_domain_num=count_create_domain(user_account,start_time,end_time)
        if create_domain_num > 0:
            log_content_dict[u'领域创建']=create_domain_num
        else:
            pass

        ##################业务知识库#################
        #敏感词创建
        create_sensitive_words_num=count_create_business(user_account,start_time,end_time,weibo_sensitive_words_index_name,weibo_sensitive_words_index_type)
        if create_sensitive_words_num > 0:
            log_content_dict[u'创建敏感词']=create_sensitive_words_num
        else:
            pass

        #时间节点创建
        create_date_remind_num=count_create_business(user_account,start_time,end_time,weibo_date_remind_index_name,weibo_date_remind_index_type)
        if create_date_remind_num > 0:
            log_content_dict[u'创建时间节点']=create_date_remind_num
        else:
            pass

        #隐喻式表达创建
        create_hidden_expression_num=count_create_business(user_account,start_time,end_time,weibo_hidden_expression_index_name,weibo_hidden_expression_index_type)
        if create_hidden_expression_num > 0:
            log_content_dict[u'创建隐喻式表达']=create_hidden_expression_num
        else:
            pass


###########################################################################
#QQ部分日志
###########################################################################
        #账户是否创建QQ虚拟人
        qq_xnr_number=create_qqxnr_number(user_account,start_time,end_time)
        if qq_xnr_number > 0:
            log_content_dict[u'创建QQ虚拟人']=qq_xnr_number
        else:
            pass

        qq_xnr_user_no_list=get_user_qqxnr_list(user_account)

        #今日发帖量
        qqxnr_daily_post = count_qqxnr_daily_post(operate_date,qq_xnr_user_no_list)
        if qqxnr_daily_post > 0:
            log_content_dict[u'QQ-发言']=qqxnr_daily_post
        else:
            pass

        #上报数量
        qq_report_number=count_qq_report_number(start_time,end_time,qq_xnr_user_no_list)
        if qq_report_number > 0:
            log_content_dict[u'QQ-上报']=qq_report_number
        else:
            pass
      

###########################################################################
#微信部分日志
###########################################################################
        #账户是否创建QQ虚拟人
        weixin_xnr_number=create_weixinxnr_number(user_account,start_time,end_time)
        if weixin_xnr_number > 0:
            log_content_dict[u'创建微信虚拟人']=weixin_xnr_number
        else:
            pass

        weixin_xnr_user_no_list=get_user_weixinxnr_list(user_account)

        #今日发帖量
        weixinxnr_daily_post = count_weixinxnr_daily_post(operate_date,weixin_xnr_user_no_list) 
        if weixinxnr_daily_post > 0:
            log_content_dict[u'微信-发言']=weixinxnr_daily_post
        else:
            pass

        #上报数量
        weixin_report_number=count_weixin_report_number(start_time,end_time,weixin_xnr_user_no_list)
        if weixin_report_number > 0:
            log_content_dict[u'微信-上报']=weixin_report_number
        else:
            pass

        log_content=json.dumps(log_content_dict)


###########################################################################
#twitter部分日志
###########################################################################

        #账户是否创建虚拟人
        tw_xnr_number=create_twxnr_number(user_account,start_time,end_time)
        if tw_xnr_number > 0:
            log_content_dict[u'创建twitter虚拟人']=tw_xnr_number
        else:
            pass

        tw_xnr_user_no_list=get_user_twxnr_list(user_account)
        tw_xnr_uid_list=get_twxnr_uid_list(user_account)
        
        #遍历各个模块，验证所管理虚拟人是否进行操作
        ##################发帖操作#################
        #日常发帖
        tw_daily_post_type='daily_post'
        tw_daily_post_num=count_type_twposting(tw_daily_post_type,operate_date,tw_xnr_user_no_list)
        if tw_daily_post_num > 0:
            log_content_dict[u'twitter-日常发帖']=tw_daily_post_num
        else:
            pass

        #业务发帖
        tw_business_post_type='business_post'
        tw_business_post_num=count_type_twposting(tw_business_post_type,operate_date,tw_xnr_user_no_list)
        if tw_business_post_num > 0:
            log_content_dict[u'twitter-业务发帖']=tw_business_post_num
        else:
            pass

        #热点跟随
        tw_hot_post_type='hot_post'
        tw_hot_post_num=count_type_twposting(tw_hot_post_type,operate_date,tw_xnr_user_no_list)
        if tw_hot_post_num > 0:
            log_content_dict[u'twitter-热点跟随']=tw_hot_post_num
        else:
            pass

        #跟踪转发
        tw_retweet_timing_num=count_tw_tweet_retweet(start_time,end_time,tw_xnr_user_no_list)
        if tw_retweet_timing_num > 0:
            log_content_dict[u'twitter-跟踪转发']=tw_retweet_timing_num
        else:
            pass

        

        ##################社交操作：转发、评论、点赞#################
        #转发
        tw_retweet_type='3'
        tw_retweet_num=count_tw_retweet_comment_operate(tw_retweet_type,operate_date,tw_xnr_uid_list)
        if tw_retweet_num > 0:
            log_content_dict[u'twitter-转发']=tw_retweet_num
        else:
            pass

        #评论
        tw_comment_type='2'
        tw_comment_num=count_tw_retweet_comment_operate(tw_comment_type,operate_date,tw_xnr_uid_list)
        if tw_comment_num > 0:
            log_content_dict[u'twitter-评论']=tw_comment_num
        else:
            pass

        #点赞
        tw_like_num=count_tw_like_operate(start_time,end_time,tw_xnr_uid_list)
        if tw_like_num > 0:
            log_content_dict[u'twitter-点赞']=tw_like_num
        else:
            pass

        #私信
        tw_private_message_num=count_tw_private_message(start_time,end_time,tw_xnr_uid_list)
        if tw_private_message_num > 0:
            log_content_dict[u'twitter-私信']=tw_private_message_num
        else:
            pass

        ##################加入语料#################
        tw_add_corpus_num=count_tw_add_corpus(start_time,end_time,tw_xnr_user_no_list)
        if tw_add_corpus_num > 0:
            log_content_dict[u'twitter-加入语料']=tw_add_corpus_num
        else:
            pass

        ##################上报操作#################
        tw_report_num=count_tw_report_type(start_time,end_time,tw_xnr_user_no_list)
        if tw_report_num > 0:
            log_content_dict[u'twitter-上报']=tw_report_num
        else:
            pass

        ##################加入预警库#################
        tw_add_warming_num=count_tw_add_warming_speech(start_time,end_time,tw_xnr_user_no_list)
        if tw_add_warming_num > 0:
            log_content_dict[u'twitter-加入预警库']=tw_add_warming_num
        else:
            pass

        ##################定时任务#################
        tw_timing_task_num=count_tw_add_timing_task(start_time,end_time,tw_xnr_user_no_list)
        if tw_timing_task_num > 0:
            log_content_dict[u'twitter-创建定时任务']=tw_timing_task_num
        else:
            pass

        

     
###########################################################################
#facebook部分日志
###########################################################################

        #账户是否创建虚拟人
        fb_xnr_number=create_fbxnr_number(user_account,start_time,end_time)
        if fb_xnr_number > 0:
            log_content_dict[u'创建facebook虚拟人']=fb_xnr_number
        else:
            pass

        fb_xnr_user_no_list=get_user_fbxnr_list(user_account)
        fb_xnr_uid_list=get_fbxnr_uid_list(user_account)
        
        #遍历各个模块，验证所管理虚拟人是否进行操作
        ##################发帖操作#################
        #日常发帖
        fb_daily_post_type='daily_post'
        fb_daily_post_num=count_type_fbposting(fb_daily_post_type,operate_date,fb_xnr_user_no_list)
        if fb_daily_post_num > 0:
            log_content_dict[u'facebook-日常发帖']=fb_daily_post_num
        else:
            pass

        #业务发帖
        fb_business_post_type='business_post'
        fb_business_post_num=count_type_fbposting(fb_business_post_type,operate_date,fb_xnr_user_no_list)
        if fb_business_post_num > 0:
            log_content_dict[u'facebook-业务发帖']=fb_business_post_num
        else:
            pass

        #热点跟随
        fb_hot_post_type='hot_post'
        fb_hot_post_num=count_type_fbposting(fb_hot_post_type,operate_date,fb_xnr_user_no_list)
        if fb_hot_post_num > 0:
            log_content_dict[u'facebook-热点跟随']=fb_hot_post_num
        else:
            pass

        #跟踪转发
        fb_retweet_timing_num=count_fb_tweet_retweet(start_time,end_time,fb_xnr_user_no_list)
        if fb_retweet_timing_num > 0:
            log_content_dict[u'facebook-跟踪转发']=fb_retweet_timing_num
        else:
            pass

        

        ##################社交操作：转发、评论、点赞#################
        #转发
        fb_retweet_type='3'
        fb_retweet_num=count_fb_retweet_comment_operate(fb_retweet_type,operate_date,fb_xnr_uid_list)
        if fb_retweet_num > 0:
            log_content_dict[u'facebook-转发']=fb_retweet_num
        else:
            pass

        #评论
        fb_comment_type='2'
        fb_comment_num=count_fb_retweet_comment_operate(fb_comment_type,operate_date,fb_xnr_uid_list)
        if fb_comment_num > 0:
            log_content_dict[u'facebook-评论']=fb_comment_num
        else:
            pass

        #点赞
        fb_like_num=count_fb_like_operate(start_time,end_time,fb_xnr_uid_list)
        if fb_like_num > 0:
            log_content_dict[u'facebook-点赞']=fb_like_num
        else:
            pass

        #私信
        fb_private_message_num=count_fb_private_message(start_time,end_time,fb_xnr_uid_list)
        if fb_private_message_num > 0:
            log_content_dict[u'facebook-私信']=fb_private_message_num
        else:
            pass

        ##################加入语料#################
        fb_add_corpus_num=count_fb_add_corpus(start_time,end_time,fb_xnr_user_no_list)
        if fb_add_corpus_num > 0:
            log_content_dict[u'facebook-加入语料']=fb_add_corpus_num
        else:
            pass

        ##################上报操作#################
        fb_report_num=count_fb_report_type(start_time,end_time,fb_xnr_user_no_list)
        if fb_report_num > 0:
            log_content_dict[u'facebook-上报']=fb_report_num
        else:
            pass

        ##################加入预警库#################
        fb_add_warming_num=count_fb_add_warming_speech(start_time,end_time,fb_xnr_user_no_list)
        if fb_add_warming_num > 0:
            log_content_dict[u'facebook-加入预警库']=fb_add_warming_num
        else:
            pass

        ##################定时任务#################
        fb_timing_task_num=count_fb_add_timing_task(start_time,end_time,fb_xnr_user_no_list)
        if fb_timing_task_num > 0:
            log_content_dict[u'facebook-创建定时任务']=fb_timing_task_num
        else:
            pass




       #写入日志
       #日志ID存在判断
        try:
            es_xnr.update(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,id=log_id,body={'doc':{'operate_content':log_content}})
            mark=True
        except:
            mark=False
        mark_list.append(mark)
    return mark_list


if __name__ == '__main__':
    create_user_log()








