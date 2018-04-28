#-*- coding: utf-8 -*-
'''
use to manage the system
'''
import os
import json
import sqlite
import sqlite3
import string
from xnr.global_utils import es_xnr as es
from xnr.global_utils import weibo_xnr_index_name,weibo_xnr_index_type,\
                        weibo_log_management_index_name,weibo_log_management_index_type,\
						weibo_authority_management_index_name,weibo_authority_management_index_type,\
						weibo_account_management_index_name,weibo_account_management_index_type,\
						qq_xnr_index_name,qq_xnr_index_type,\
						xnr_map_index_name,xnr_map_index_type,qq_xnr_index_name,qq_xnr_index_type,\
						weibo_feedback_group_index_name,weibo_feedback_group_index_type,\
                        wx_xnr_index_name,wx_xnr_index_type,\
                        fb_xnr_index_name,fb_xnr_index_type,\
                        tw_xnr_index_name,tw_xnr_index_type
from xnr.parameter import MAX_VALUE,USER_XNR_NUM

##############################################################
########	log management
##############################################################
#add log
#log_info=[user_id,user_name,login_time,login_ip,operate_time,operate_content]
def create_log_list(log_info):
	log_detail=dict()
	log_detail['user_id']=log_info[0]
	log_detail['user_name']=log_info[1]
	log_detail['login_time']=log_info[2].split('*')
	log_detail['login_ip']=log_info[3].split('*')
	log_detail['operate_time']=log_info[4]
	log_detail['operate_content']=log_info[5].split('*')
	log_detail['operate_date']=log_info[6]
	log_id=log_info[1]+'_'+log_info[6]

	#try:
	result=es.index(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,id=log_id,body=log_detail)
	#	result=True
	#except:
	#	result=False
	return result

#show log management
def show_log_list():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'operate_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,body=query_body)['hits']['hits']
	results=[]
	for item in result:
		item['_source']['log_id']=item['_id']
		#item['_source']['operate_content']=json.loads(item['_source']['operate_content'])
		results.append(item['_source'])
		#print results
	return results

#delete log list
def delete_log_list(log_id):
	try:
		es.delete(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,id=log_id)
		result=True
	except:
		result=False
	return result

##############################################################
########	authority management
##############################################################
#add authority description
def create_role_authority(role_name,description):
	authority_detail=dict()
	authority_detail['role_name']=role_name
	authority_detail['description']=description
	authority_id=role_name

	try:
		es.index(index=weibo_authority_management_index_name,doc_type=weibo_authority_management_index_type,id=authority_id,body=authority_detail)
		result=True
	except:
		result=False
	return result

#show authority description list
def show_authority_list():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE
	}
	result=es.search(index=weibo_authority_management_index_name,doc_type=weibo_authority_management_index_type,body=query_body)['hits']['hits']
	results=[]
	for item in result:
		results.append(item['_source'])
	return results

#change the authority description
def change_authority_list(role_name,description):
	try:
		es.update(index=weibo_authority_management_index_name,doc_type=weibo_authority_management_index_type,id=role_name,\
			body={'doc':{'role_name':role_name,'description':description}})
		result=True
	except:
		result=False
	return result

#delete the authority description
def delete_authority_list(role_name):
	try:
		es.delete(index=weibo_authority_management_index_name,doc_type=weibo_authority_management_index_type,id=role_name)
		result=True
	except:
		result=False
	return result


##############################################################
########	account management
##############################################################
#add account
#step 1: add user account
#user_account_info=[user_id,user_name,my_xnrs]
def create_user_account(user_account_info):
	account_detail=dict()
	account_detail['user_id']=user_account_info[0]
	account_detail['user_name']=user_account_info[1]
	account_detail['my_xnrs']=user_account_info[2]
	account_id=user_account_info[0]

	try:
		es.index(index=weibo_account_management_index_name,doc_type=weibo_account_management_index_type,id=account_id,body=account_detail)
		result=True
	except:
		result=False
	return result

#step 2: add the user's xnr account =>chang the user account,add
def add_user_xnraccount(account_id,xnr_accountid):
	user_account_info=es.get(index=weibo_account_management_index_name,doc_type=weibo_account_management_index_type,id=account_id)
	origin_xnr_account=user_account_info['_source']['my_xnrs']
	if origin_xnr_account:
		origin_xnr_account.extend(xnr_accountid)
	else:
		origin_xnr_account=xnr_accountid
	new_xnr_account=[]
	[new_xnr_account.append(i) for i in origin_xnr_account if not i in new_xnr_account]
	try:
		es.update(index=weibo_account_management_index_name,doc_type=weibo_account_management_index_type,id=account_id,\
			body={'doc':{'my_xnrs':new_xnr_account}})
		result=True
	except:
		result=False
	return result


#show all users account
#连接数据库,获取账户列表
def get_user_account_list():
    # cx = sqlite3.connect("/home/xnr1/xnr_0313/xnr/flask-admin.db") 
    cx = sqlite3.connect("/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/flask-admin.db")
    cu=cx.cursor()
    cu.execute("select email from user") 
    user_info = cu.fetchall()
    cx.close()
    return user_info

#根据账户名称查询所管理的虚拟人
#微博虚拟人
def get_user_xnr_list(user_account,status_start,status_end):
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'bool':{
        			    'must':[
        			    	{'term':{'submitter':user_account}},
        			    	{'range':{'create_status':{'gte':status_start,'lt':status_end}}}
        			    ]
        			}
        		}
        	}
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list

#QQ虚拟人
def get_qq_xnr_list(account_name):
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'bool':{
        			    'must':[
        			    	{'term':{'submitter':account_name}}
        			    ]
        			}
        		}
        	}
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list

#整合账户管理

def show_all_users_account():
    account_list=get_user_account_list()
    print account_list
    account_info=[]
    for account_name in account_list:
        account_dict=dict()
        account_name=list(account_name)[0]
        account_dict['user_name']=account_name
        #未完成虚拟人
        status_zero=0
        status_second=2
        status_three=3        
        weibo_uncomplete_xnr_list=get_user_xnr_list(account_name,status_zero,status_second)
        account_dict['uncomplete_xnr_weibo']=weibo_uncomplete_xnr_list
        account_dict['uncomplete_xnr_qq']=[]
        account_dict['uncomplete_xnr_weixin']=[]
        account_dict['uncomplete_xnr_facebook']=[]
        account_dict['uncomplete_xnr_twitter']=[]
        #已完成虚拟人
        weibo_complete_xnr_list=get_user_xnr_list(account_name,status_second,status_three)
        account_dict['complete_xnr_weibo']=weibo_complete_xnr_list
        qq_complete_xnr_list=get_qq_xnr_list(account_name)
        account_dict['complete_xnr_qq']=qq_complete_xnr_list
        account_dict['complete_xnr_weixin']=[]
        account_dict['complete_xnr_facebook']=[]
        account_dict['complete_xnr_twitter']=[]
        account_info.append(account_dict)
    return account_info


def show_users_account(main_user):
    account_list=[]
    #微博
    weibo_dict=dict()
    weibo_dict['platform_name']='微博'
    status_zero=0
    status_second=2
    status_three=3
    weibo_dict['complete_xnr_list']=get_user_xnr_list(main_user,status_second,status_three)
    weibo_dict['uncomplete_xnr_list']=get_user_xnr_list(main_user,status_zero,status_second)
    account_list.append(weibo_dict)

    #qq
    qq_dict=dict()
    qq_dict['platform_name']='QQ'
    qq_dict['complete_xnr_list']=get_qq_xnr_list(main_user)
    qq_dict['uncomplete_xnr_list']=[]
    account_list.append(qq_dict)

    #weixin
    weixin_dict=dict()
    weixin_dict['platform_name']='微信'
    weixin_dict['complete_xnr_list']=[]
    weixin_dict['uncomplete_xnr_list']=[]
    account_list.append(weixin_dict)

    #facebook
    facebook_dict=dict()
    facebook_dict['platform_name']='facebook'
    facebook_dict['complete_xnr_list']=[]
    facebook_dict['uncomplete_xnr_list']=[]
    account_list.append(facebook_dict)

    #twitter
    twitter_dict=dict()
    twitter_dict['platform_name']='twitter'
    twitter_dict['complete_xnr_list']=[]
    twitter_dict['uncomplete_xnr_list']=[]
    account_list.append(twitter_dict)
    return account_list


#delete account
#step 1:delete the user account
def delete_user_account(account_id):
	try:
		es.delete(index=weibo_account_management_index_name,doc_type=weibo_account_management_index_type,id=account_id)
		result=True
	except:
		result=False
	return result

#step 2:delete the user's xnr account =>chang the user account,delete
def delete_user_xnraccount(account_id,xnr_accountid):
	user_account_info=es.get(index=weibo_account_management_index_name,doc_type=weibo_account_management_index_type,id=account_id)
	origin_xnr_account=user_account_info['_source']['my_xnrs']

	if origin_xnr_account:
		origin_xnr_account.remove(xnr_accountid)
	else:
		origin_xnr_account=xnr_accountid

	try:
		es.update(index=weibo_account_management_index_name,doc_type=weibo_account_management_index_type,id=account_id,\
			body={'doc':{'my_xnrs':origin_xnr_account}})
		result=True
	except:
		result=False
	return result

#change user account info
#user_account_info=[user_id,user_name,my_xnrs]
def change_user_account(change_detail):
	user_id=change_detail['user_id']
	user_name=change_detail['user_name']
	my_xnrs=change_detail['my_xnrs']
	try:
		es.update(index=weibo_account_management_index_name,doc_type=weibo_account_management_index_type,id=user_id,\
			body={'doc':{'user_id':user_id,'user_name':user_name,'my_xnrs':my_xnrs}})
		result=True
	except:
		result=False
	return result





##############################################################
########	xnr_map
##############################################################

#add xnr_map_relationship
def add_xnr_map_relationship(xnr_map_detail):
    xnr_map_id=xnr_map_detail['main_user']+'_'+str(xnr_map_detail['timestamp'])
    try:
        es.index(index=xnr_map_index_name,doc_type=xnr_map_index_type,body=xnr_map_detail,id=xnr_map_id)
        result=True
    except:
        result=False
    return result    	

#control add xnr_map_relationship
def select_all_xnr(main_user,index_name,index_type):
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'bool':{
        			    'must':[
        			    	{'term':{'submitter':main_user}}
        			    ]
        			}
        		}
        	}
        },
        'size':MAX_VALUE
    }
    try:
        user_result=es.search(index=index_name,doc_type=index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_dict=dict()
            xnr_user_dict['xnr_user_no']=item['_source']['xnr_user_no']
            xnr_user_dict['xnr_name']=item['_source']['nickname']
            xnr_user_no_list.append(xnr_user_dict)
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list

def select_all_weibo_xnr(main_user,index_name,index_type):
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'bool':{
        			    'must':[
        			    	{'term':{'submitter':main_user}},
        			    	{'term':{'create_status':2}}
        			    ]
        			}
        		}
        	}
        },
        'size':MAX_VALUE
    }
    try:
        user_result=es.search(index=index_name,doc_type=index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_dict=dict()
            xnr_user_dict['xnr_user_no']=item['_source']['xnr_user_no']
            xnr_user_dict['xnr_name']=item['_source']['nick_name']
            xnr_user_no_list.append(xnr_user_dict)
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list

def select_xnr_map_relationship(main_user,platform_no,platform_name):
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'bool':{
        			    'must':[
        			    	{'term':{'main_user':main_user}}
        			    ]
        			}
        		}
        	}
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es.search(index=xnr_map_index_name,doc_type=xnr_map_index_type,body=query_body)['hits']['hits']
        result=[]
        for item in es_result:
            xnr_user_dict=dict()
            xnr_user_dict['xnr_user_no']=item['_source'][platform_no]
            xnr_user_dict['xnr_name']=item['_source'][platform_name]
            result.append(xnr_user_dict)
    except:
        result=''
    return result  

#比较两个集合
def compare_list(all_xnr_list,maped_xnr_list):
    for item in maped_xnr_list:
        if item in all_xnr_list:
            all_xnr_list.remove(item)
        else:
            pass
    return all_xnr_list

def control_add_xnr_map_relationship(main_user):
    xnr_dict=dict()
    #weibo
    weibo_all_xnr_list=select_all_weibo_xnr(main_user,weibo_xnr_index_name,weibo_xnr_index_type)
    weibo_platform_no='weibo_xnr_user_no'
    weibo_platform_name='weibo_xnr_name'
    weibo_maped_xnr_list=select_xnr_map_relationship(main_user,weibo_platform_no,weibo_platform_name)
    xnr_dict['weibo_xnr_list']=compare_list(weibo_all_xnr_list,weibo_maped_xnr_list)
    #print weibo_all_xnr_list

    #qq
    qq_all_xnr_list=select_all_xnr(main_user,qq_xnr_index_name,qq_xnr_index_type)
    qq_platform_no='qq_xnr_user_no'
    qq_platform_name='qq_xnr_name'
    qq_maped_xnr_list=select_xnr_map_relationship(main_user,qq_platform_no,qq_platform_name)
    xnr_dict['qq_xnr_list']=compare_list(qq_all_xnr_list,qq_maped_xnr_list)

    #weixin
    weixin_all_xnr_list=select_all_xnr(main_user,wx_xnr_index_name,wx_xnr_index_type)
    weixin_platform_no='weixin_xnr_user_no'
    weixin_platform_name='weixin_xnr_name'
    weixin_maped_xnr_list=select_xnr_map_relationship(main_user,weixin_platform_no,weixin_platform_name)
    xnr_dict['weixin_xnr_list']=compare_list(weixin_all_xnr_list,weixin_maped_xnr_list)

    #facebook
    facebook_all_xnr_list=select_all_weibo_xnr(main_user,fb_xnr_index_name,fb_xnr_index_type)
    facebook_platform_no='facebook_xnr_user_no'
    facebook_platform_name='facebook_xnr_name'
    facebook_maped_xnr_list=select_xnr_map_relationship(main_user,facebook_platform_no,facebook_platform_name)
    xnr_dict['facebook_xnr_list']=compare_list(facebook_all_xnr_list,facebook_maped_xnr_list)
    

    #twitter
    twitter_all_xnr_list=select_all_weibo_xnr(main_user,tw_xnr_index_name,tw_xnr_index_type)
    twitter_platform_no='twitter_xnr_user_no'
    twitter_platform_name='twitter_xnr_name'
    twitter_maped_xnr_list=select_xnr_map_relationship(main_user,twitter_platform_no,twitter_platform_name)
    xnr_dict['twitter_xnr_list']=compare_list(twitter_all_xnr_list,twitter_maped_xnr_list)

    return xnr_dict



    


#show xnr_map_relationship
def show_xnr_map_relationship(main_user):
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'bool':{
        			    'must':[
        			    	{'term':{'main_user':main_user}}
        			    ]
        			}
        		}
        	}
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es.search(index=xnr_map_index_name,doc_type=xnr_map_index_type,body=query_body)['hits']['hits']
        result=[]
        for item in es_result:
            item['_source']['id']=item['_id']
            result.append(item['_source'])
    except:
        result=''
    return result  

#change platform
def change_xnr_platform(origin_platform,origin_xnr_user_no,new_platform):
    search_field=origin_platform + '_xnr_user_no'
    new_search_field_no=new_platform + '_xnr_user_no'
    #new_search_field_name=new_platform + '_xnr_name'
    query_body={
        '_source':{
        'include':new_search_field_no
        },
        'query':{
        	'filtered':{
        		'filter':{
        			'bool':{
        			    'must':[
        			    	{'term':{search_field:origin_xnr_user_no}}
        			    ]
        			}
        		}
        	}
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es.search(index=xnr_map_index_name,doc_type=xnr_map_index_type,body=query_body)['hits']['hits']
        result=[]
        for item in es_result:
            result.append(item['_source'])
    except:
        result=''
    return result 


def delete_xnr_map_relationship(xnr_map_id):
	try:
		es.delete(index=xnr_map_index_name,doc_type=xnr_map_index_type,id=xnr_map_id)
		result=True
	except:
		result=False
	return result


#update
def update_xnr_map_relationship(xnr_map_detail,xnr_map_id):    
    try:
        es.delete(index=xnr_map_index_name,doc_type=xnr_map_index_type,id=xnr_map_id)
        es.index(index=xnr_map_index_name,doc_type=xnr_map_index_type,body=xnr_map_detail,id=xnr_map_id)
        # es.update(index=xnr_map_index_name,doc_type=xnr_map_index_type,body=xnr_map_detail,id=xnr_map_id)
        result=True
    except:
        result=False
    return result  



#change platform
def lookup_xnr_relation(origin_platform,origin_xnr_user_no):
    search_field=origin_platform + '_xnr_user_no'
    #new_search_field_no=new_platform + '_xnr_user_no'
    #new_search_field_name=new_platform + '_xnr_name'
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'term':{search_field:origin_xnr_user_no}}
                        ]
                    }
                }
            }
        },
        'size':MAX_VALUE
    }
    try:
        es_result=es.search(index=xnr_map_index_name,doc_type=xnr_map_index_type,body=query_body)['hits']['hits']
        result=[]
        for item in es_result:
            #qq群组
            #item['_source']['qq_groups']=lookup_qqxnr_group(item['_source']['qq_xnr_user_no'])
            #微信群组
            #item['_source']['weixin_groups']=lookup_weixinxnr_group(item['_source']['weixin_xnr_user_no'])
            #微博群组
            item['_source']['weibo_groups']=lookup_weiboxnr_group(item['_source']['weibo_xnr_user_no'])
            #facebook群组
            item['_source']['facebook_groups']=[]
            #item['_source']['facebook_groups']=lookup_facebookxnr_group(item['_source']['facebook_xnr_user_no'])
            #twitter群组
            item['_source']['twitter_groups']=[]
            #item['_source']['twitter_groups']=lookup_twitterxnr_group(item['_source']['twitter_xnr_user_no'])
            result.append(item['_source'])
    except:
        result=''
    return result 

#qq群编号
def lookup_qqxnr_group(xnr_user_no):
    try:
        qq_xnr_result=es.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
        qq_groups=[]
        for item in qq_xnr_result['qq_groups']:
            qq_groups_dict=dict()
            qq_groups_dict['gid']=item
            qq_groups_dict['gname']=''  
            qq_groups.append(qq_groups_dict)
    except:
        qq_groups=[]
    return qq_groups


#微信群编号
def lookup_weixinxnr_group(xnr_user_no):
    grou_info=show_listening_groups(xnr_user_no)
    idx = grou_info['wx_groups_id'] 
    names = grou_info['wx_groups_nickname']
    id_name = []
    for i, _id in enumerate(idx):
        id_name_dict = {}
        id_name_dict['gid'] = idx[i]
        id_name_dict['gname'] = names[i]
        id_name.append(id_name_dict)
    return id_name


#查询微博虚拟人uid
def lookup_weiboxnr_uid(xnr_user_no):
	try:
		xnr_result=es.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
		xnr_uid=xnr_result['uid']
	except:
		xnr_uid=''
	return xnr_uid


#微博群组信息
def lookup_weiboxnr_group(xnr_user_no):
    #查询虚拟人uid
    xnr_uid=lookup_weiboxnr_uid(xnr_user_no)
    query_body={
        'query':{
        	'filtered':{
        		'filter':{
        			'term':{'uid':xnr_uid}
        		}
        	}
        },
        'size':MAX_VALUE
    }
    
    try:
        group_result=es.search(index=weibo_feedback_group_index_name,doc_type=weibo_feedback_group_index_type,body=query_body)['hits']['hits']
    #print 'group_result:',group_result
        group_list=[]
        for item in group_result:
            group_dict=dict()
            group_dict['gid']=item['_source']['gid']
            group_dict['gname']=item['_source']['gname']
            group_list.append(group_dict)
    except:
        group_list=[]
    return group_list



def show_all_xnr(main_user,task_id):
    xnr_dict=dict()
    #weibo
    weibo_all_xnr_list=select_all_weibo_xnr(main_user,weibo_xnr_index_name,weibo_xnr_index_type)
    weibo_platform_no='weibo_xnr_user_no'
    weibo_platform_name='weibo_xnr_name'
    weibo_maped_xnr_list=select_xnr_map_relationship(main_user,weibo_platform_no,weibo_platform_name)
    xnr_dict['weibo_xnr_list']=compare_list(weibo_all_xnr_list,weibo_maped_xnr_list)
    #print weibo_all_xnr_list

    #qq
    qq_all_xnr_list=select_all_xnr(main_user,qq_xnr_index_name,qq_xnr_index_type)
    qq_platform_no='qq_xnr_user_no'
    qq_platform_name='qq_xnr_name'
    qq_maped_xnr_list=select_xnr_map_relationship(main_user,qq_platform_no,qq_platform_name)
    xnr_dict['qq_xnr_list']=compare_list(qq_all_xnr_list,qq_maped_xnr_list)

    #weixin
    weixin_all_xnr_list=select_all_xnr(main_user,wx_xnr_index_name,wx_xnr_index_type)
    weixin_platform_no='weixin_xnr_user_no'
    weixin_platform_name='weixin_xnr_name'
    weixin_maped_xnr_list=select_xnr_map_relationship(main_user,weixin_platform_no,weixin_platform_name)
    xnr_dict['weixin_xnr_list']=compare_list(weixin_all_xnr_list,weixin_maped_xnr_list)

    #facebook
    facebook_all_xnr_list=select_all_weibo_xnr(main_user,fb_xnr_index_name,fb_xnr_index_type)
    facebook_platform_no='facebook_xnr_user_no'
    facebook_platform_name='facebook_xnr_name'
    facebook_maped_xnr_list=select_xnr_map_relationship(main_user,facebook_platform_no,facebook_platform_name)
    xnr_dict['facebook_xnr_list']=compare_list(facebook_all_xnr_list,facebook_maped_xnr_list)
    

    #twitter
    twitter_all_xnr_list=select_all_weibo_xnr(main_user,tw_xnr_index_name,tw_xnr_index_type)
    twitter_platform_no='twitter_xnr_user_no'
    twitter_platform_name='twitter_xnr_name'
    twitter_maped_xnr_list=select_xnr_map_relationship(main_user,twitter_platform_no,twitter_platform_name)
    xnr_dict['twitter_xnr_list']=compare_list(twitter_all_xnr_list,twitter_maped_xnr_list)


    #当前映射的内容添加上
    try:
        result_es = es.get(index=xnr_map_index_name,doc_type=xnr_map_index_type,id=task_id)['_source']
        if result_es['weibo_xnr_user_no']:
            weibo_user_dict = dict()
            weibo_user_dict['xnr_user_no'] = result_es['weibo_xnr_user_no']
            weibo_user_dict['xnr_name'] = result_es['weibo_xnr_name']
            weibo_user_dict['mark'] = 1
            xnr_dict['weibo_xnr_list'].append(weibo_user_dict)
        if result_es['qq_xnr_user_no']:
            qq_user_dict = dict()
            qq_user_dict['xnr_user_no'] = result_es['qq_xnr_user_no']
            qq_user_dict['xnr_name'] = result_es['qq_xnr_name']
            qq_user_dict['mark'] = 1
            xnr_dict['qq_xnr_list'].append(qq_user_dict)
        if result_es['weixin_xnr_user_no']:
            weixin_user_dict = dict()
            weixin_user_dict['xnr_user_no'] = result_es['weixin_xnr_user_no']
            weixin_user_dict['xnr_name'] = result_es['weixin_xnr_name']
            weixin_user_dict['mark'] = 1
            xnr_dict['weixin_xnr_list'].append(weixin_user_dict)
        if result_es['facebook_xnr_user_no']:
            facebook_user_dict = dict()
            facebook_user_dict['xnr_user_no'] = result_es['facebook_xnr_user_no']
            facebook_user_dict['xnr_name'] = result_es['facebook_xnr_name']
            facebook_user_dict['mark'] = 1
            xnr_dict['facebook_xnr_list'].append(facebook_user_dict)
        if result_es['twitter_xnr_user_no']:
            twitter_user_dict = dict()
            twitter_user_dict['xnr_user_no'] = result_es['twitter_xnr_user_no']
            twitter_user_dict['xnr_name'] = result_es['twitter_xnr_name']
            twitter_user_dict['mark'] = 1
            xnr_dict['twitter_xnr_list'].append(twitter_user_dict)
    except:
        pass

    return xnr_dict