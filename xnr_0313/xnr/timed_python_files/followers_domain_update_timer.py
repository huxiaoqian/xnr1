# -*- coding:utf-8 -*-

import time
import os
import json
from collections import Counter

import sys
sys.path.append('../')

from global_utils import es_xnr,es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
					weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
					user_domain_index_name,user_domain_index_type
from global_config import S_TYPE, S_DATE
#from weibo_xnr_flow_text_mappings import daily_inerests_flow_text_mappings
from time_utils import ts2datetime,datetime2ts
from parameter import MAX_VALUE,domain_en2ch_dict
from time_utils import get_flow_text_index_list,datetime2ts
from timed_python_files.domain.test_domain_v2 import domain_classfiy

def followers_domain_update():

	if S_TYPE == 'test':
		current_time = datetime2ts(S_DATE)
		
	else:
		current_time = int(time.time())

	flow_text_index_name_list = get_flow_text_index_list(current_time)

	query_body = {
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE
	}

	search_results = es_xnr.search(index=weibo_xnr_fans_followers_index_name,\
		doc_type=weibo_xnr_fans_followers_index_type,body=query_body)['hits']['hits']
	followers_list_all = []
	for result in search_results:
		result = result['_source']
		followers_list = result['followers_list']
		followers_list_all.extend(followers_list)

	followers_list_all_set_list = list(set(followers_list_all))

	uid_weibo_keywords_dict,keywords_dict_all_users = uid_list_2_uid_keywords_dict(followers_list_all_set_list,flow_text_index_name_list)
	uids_avtive_list = uid_weibo_keywords_dict.keys()   # 防止关注列表中有无效uid，或者只有近期活跃的uid才有意义。
	
	## 领域分类
	r_domain = dict()
	print 'uids_avtive_list::',uids_avtive_list

	domain,r_domain = domain_classfiy(uids_avtive_list,uid_weibo_keywords_dict)
	print 'r_domain::',r_domain

	for uid, domain in r_domain.iteritems():
		domain_name = domain_en2ch_dict[domain]
		_id = uid
		try:
			print '_id:::',_id
			get_result = es_xnr.get(index=user_domain_index_name,doc_type=user_domain_index_type,\
				id=_id)['_source']

			get_result['domain_name'] = domain_name
			get_result['update_time'] = int(time.time())
			es_xnr.update(index=user_domain_index_name,doc_type=user_domain_index_type,\
				id=_id,body={'doc':get_result})

		except:
			item_dict = {}
			item_dict['uid'] = uid
			item_dict['domain_name'] = domain_name
			item_dict['update_time'] = int(time.time())

			es_xnr.index(index=user_domain_index_name,doc_type=user_domain_index_type,\
				id=_id,body=item_dict)
			#print '$$$$$$'
		

## 根据uids_list获取 分类器输入需要的字典，即 uid_keywords字典。
def uid_list_2_uid_keywords_dict(uids_list,flow_text_index_name_list,label='other'):
    uid_weibo_keywords_dict = dict()
    keywords_dict_all_users = dict()
    uid_weibo = [] # [[uid1,text1,ts1],[uid2,text2,ts2],...]
    #uid_list_active = []  # 防止关注列表中有无效uid，或者只有近期活跃的uid才有意义。
    
    for flow_text_index_name in flow_text_index_name_list:
        
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'terms':{
                            'uid':uids_list
                        }
                    }
                }
            },
            'size':MAX_VALUE
        }
        
        es_weibo_results = es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                                            body=query_body)['hits']['hits']
        print len(es_weibo_results)

        for i in range(len(es_weibo_results)):
            
            uid = es_weibo_results[i]['_source']['uid']
            keywords_dict = es_weibo_results[i]['_source']['keywords_dict']
            keywords_dict = json.loads(keywords_dict)
            #uid_list_active.append(uid)
            if i % 1000 == 0:
                print i
            if label == 'character':
                text = es_weibo_results[i]['_source']['text']
                timestamp = es_weibo_results[i]['_source']['timestamp']
                uid_weibo.append([uid,text,timestamp])
            
            '''
            ## 合并相同id的关键词字典
            
            if uid in uid_weibo_keywords_dict.keys():
                uid_weibo_keywords_dict[uid] = dict(Counter(uid_weibo_keywords_dict[uid])+Counter(keywords_dict))
            else:
                uid_weibo_keywords_dict[uid] = keywords_dict

            ## 合并所有用户的关键词字典
            keywords_dict_all_users = dict(Counter(keywords_dict_all_users)+Counter(keywords_dict))
            '''
            ## 统计用户所有词频
            
            if uid in uid_weibo_keywords_dict.keys():
                for keyword, count in keywords_dict.iteritems():
                    if keyword in uid_weibo_keywords_dict[uid].keys():
                        uid_weibo_keywords_dict[uid][keyword] += count
                    else:
                        uid_weibo_keywords_dict[uid][keyword] = count
            else:
                uid_weibo_keywords_dict[uid] = keywords_dict

            ## 合并所有用户的关键词字典

            for keyword, count in keywords_dict.iteritems():
                try:
                    keywords_dict_all_users[keyword] += count
                except:
                    keywords_dict_all_users[keyword] = count

    if label == 'character':
        return uid_weibo_keywords_dict,keywords_dict_all_users,uid_weibo
    else:
        return uid_weibo_keywords_dict,keywords_dict_all_users

if __name__ == '__main__':

	followers_domain_update()