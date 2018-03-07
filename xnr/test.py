#-*- coding:utf-8 -*-
import os
import time
import random
import json
import sys
import base64
from global_utils import es_xnr as es,r,es_flow_text
from global_utils import es_user_portrait,portrait_index_name,portrait_index_type
from global_utils import weibo_xnr_index_name,weibo_xnr_index_type,\
                        weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from weibo_xnr_flow_text_mappings import weibo_xnr_flow_text_mappings
# icon = open('./weibo_images/zhengyidang.png','rb')
# iconData = icon.read()
# iconData = base64.b64encode(iconData)
# print 'icondata:::',iconData

# imgData = base64.b64decode(iconData)
# time_name = time.strftime('%Y%m%d%H%M%S')
# random_name = time_name + '_%d' % random.randint(0,100)
# leniyimg = open('./'+random_name+'.jpg','wb')
# leniyimg.write(imgData)
# leniyimg.close()
#     

# query_body = {
#     'query':{
#         'match_all':{}
#     },
#     'size':20,
#     'sort':{'sensitive':{'order':'desc'}}
# }
# results = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,body=query_body)['hits']['hits']


# for result in results:
    
#     print result['_source']['sensitive']

# query_body= {
#     'query':{
#         'term':{'xnr_user_no':'WXNR0004'}
#     }
# }

# 导出
# query_body= {
#     'query':{
#         'match_all':{}
#     }
# }


# result = es.search(index='tweet_retweet_timing_list',doc_type='timing_list',\
#     body=query_body)['hits']['hits']

# result_json = {}

# for result_item in result:
#     _id = result_item['_id']
#     result_json[_id] = result_item
# #print 'result_json::',result_json

# with open("./retweet_tweet_timing.json","w") as dump_f:
#     # for item in result:
#     json.dump(result_json,dump_f)
#     print '@'


# 导入
# with open("./retweet_tweet_timing.json","r") as load_f:
#     #print 'load_f::',load_f
#     load_dict = json.load(load_f)
#     print load_dict
#     print type(load_dict)
#     for key,value in load_dict.iteritems():
        
#         _id = key
#         content = value['_source']

#         #weibo_xnr_flow_text_mappings('xnr_flow_text_2017-10-01')
#         es.index(index='tweet_retweet_timing_list',doc_type='timing_list',\
#             id=_id,body=content)


# follow_list = result[0]['_source']['followers_list']

# follow_list = list(set(follow_list))


# get_result = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
#     id='WXNR0004')['_source']
# follow_list = get_result['followers_list']

# follow_new_list = ['6051938764', '5099016176', '5713626060', '5927855538', '3684276561', '3769547063', '5876804193', '5625493137', '5720398851', '1926974981']
# follow_list.extend(follow_new_list)
# follow_list = list(set(follow_list))
# es.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
#     id='WXNR0004',body={'doc':{'followers_list':follow_list}})


# # query_body = {
# #     'query':{
# #         'term':{'xnr_user_no':['WXNR00004']}
# #     }
# # }

# results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']

# print 'results::',results

#es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043525244676524')
# es.delete(index='weibo_domain',doc_type='group',id='AV6396lYQIwrAS0usE0H')
# es.delete(index='weibo_domain',doc_type='group',id='AV64pqMhS8CBAF2ZGzdS')
# es.delete(index='tweet_timing_list',doc_type='timing_list',id='WXNR0004_1506426263_1506204755')
# es.delete(index='tweet_timing_list',doc_type='timing_list',id='WXNR0004_1506426265_1506136628')
# es.delete(index='tweet_timing_list',doc_type='timing_list',id='WXNR0004_1506426443_1506609382')
# es.delete(index='tweet_timing_list',doc_type='timing_list',id='WXNR0004_1505984970_1506008456')
# es.delete(index='tweet_timing_list',doc_type='timing_list',id='WXNR0004_1506426266_1506167318')

# es.update(index='qq_xnr',doc_type='user',id='QXNR0001', body={'doc':{'qq_groups':['576127356','586502775','5339432','513304542'],'qq_group_num':4}})

# for i in range(5,26):
#     no = str('%02d'%i)
#     es.delete(index='weibo_xnr',doc_type='user',id='WXNR00'+no)

#es.delete(index='weibo_xnr',doc_type='user',id='WXNR0014')
# print r.sadd('qq_group_set_01',['121567','5674567'])
# m = r.smembers('qq_group_set_01')
# if "123123123" in m:
#     print '1111'

# es.delete(index='weibo_example_model',doc_type='model',id='min_yun_ren_shi_grassroot')
# es.delete(index='weibo_example_model',doc_type='model',id='null_min_yun_ren_shi_grassroot')
# es.delete(index='weibo_example_model',doc_type='model',id='WXNR0004_min_yun_ren_shi_grassroot')
# es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043525622087918')
# es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043433776005723')
# es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043274014747152')
# es.delete(index='qq_xnr',doc_type='user',id='QXNR0003')
# es.delete(index='qq_xnr',doc_type='user',id='QXNR0005')
# es.delete(index='qq_xnr',doc_type='user',id='QXNR0006')

#es.update(index='weibo_xnr',doc_type='user',id='WXNR0004',body={'doc':{'monitor_keywords':'民运,民运人士,民主运动'}})

# es.indices.delete(index='user_bought')
# es.indices.delete(index='weibo_feedback_comment_2017*')
# es.indices.delete(index='weibo_feedback_at_2017*')
# es.indices.delete(index='weibo_feedback_private_2017*')
# es.indices.delete(index='weibo_feedback_like_2017*')

# query_body={
#     'query':{
#         'range':{'sensitive':{'gt':0}}
#     },
    
#     'sort':{'sensitive':{'order':'desc'}},
#     'size':30
    
# }
# flow_text_index_name = ['flow_text_2016-11-27']
# # flow_text_index_name = ['flow_text_2016-11-20','flow_text_2016-11-19','flow_text_2016-11-18',\
# # 'flow_text_2016-11-17','flow_text_2016-11-16','flow_text_2016-11-15']
# #es_result = es_flow_text.search(index=flow_text_index_name,doc_type='text',body=query_body)['aggregations']['followers_sensitive_num']['buckets']
# es_result = es_flow_text.search(index=flow_text_index_name,doc_type='text',body=query_body)['hits']['hits']

# uid_list = []
# for result in es_result:
#     result = result['_source']
#     uid_list.append(result['uid'])

# print 'uid_list::',uid_list

# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-01')['_source']
# item_dict = {}
# item_dict = {'influence':0.50,'safe':18.01,'penetration':20.05}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-01',body   ={'doc':item_dict})

# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-02')['_source']
# item_dict = {}
# item_dict = {'influence':0.50,'safe':18.04,'penetration':14.28}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-02',body   ={'doc':item_dict})

# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-03')['_source']
# item_dict = {}
# item_dict = {'influence':0.50,'safe':0,'penetration':16.33}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-03',body   ={'doc':item_dict})

# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-04')['_source']
# item_dict = {}
# item_dict = {'influence':0.50,'safe':0,'penetration':17.24}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-04',body   ={'doc':item_dict})

# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-05')['_source']
# item_dict = {}
# item_dict = {'influence':1.43,'safe':19.21,'penetration':10.03}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-05',body   ={'doc':item_dict})

# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-06')['_source']
# item_dict = {}
# item_dict = {'influence':3.58,'safe':30.54,'penetration':25.48}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-06',body   ={'doc':item_dict})

# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-07')['_source']
# item_dict = {}
# item_dict = {'influence':0,'safe':0,'penetration':24.56}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-07',body   ={'doc':item_dict})


# get_reuslt = es.get(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-15')['_source']
# item_dict = {}
# item_dict = {'influence':0,'penetration':0,'safe':0}
# es.update(index='weibo_xnr_count',doc_type='text',id='WXNR0004_2017-10-15',body   ={'doc':item_dict})


# with open('./uid_sensitive.txt','w') as f:
#     for item in es_result:
#         uid = item['key']
#         f.write(uid+'\n')
#     f.close()

# query_body = {
#     'query':{
#         'filtered':{
#             'filter':{
#                 'terms':{'xnr_user_no':['WXNR0001','WXNR0002','WXNR0004']}
#             }
#         }
#     },
#     'size':10
# }

# es_results = es.search(index='weibo_xnr',doc_type='user',body=query_body)['hits']['hits']

# for result in es_results:
#     print result

# item = {}
# item['text'] = '想问下各位 银行已经面签完了不过的情况多吗？'
# item['speaker_qq_number'] = '1355581192'
# item['sensitive_flag'] = 0
# item['sensitive_words_string'] = ''
# item['qq_group_nickname'] = '房屋买卖违约维权律师'
# item['sensitive_value'] = 0
# item['xnr_qq_number'] = '1965056593'
# item['xnr_nickname'] = '袁慧茹'
# item['speaker_nickname'] = '[wū] · [ ]'
# item['timestamp'] = 1506860121
# item['qq_group_number'] = '513304542'

# id = '1965056593_513304542_1506860121_7536c341631345922d86632b28863e'
# es.index(index='group_message_2017-10-01',doc_type='record',id=id,body=item)

#es.delete(index='group_message_2017-10-01',doc_type='record',id='AV7cBiJA82y9EzvV4MqU')



# def processinfo(x):

#     process_list = psutil.get_process_list() #获取进程列表
#     for r in process_list:
#         aa = str(r)
#         f = re.compile(x,re.I)
#         print 'aa::',aa
#         print 'f::',f
#         if f.search(aa):
#             print aa.split('pid=')[1].split(',')[0]  
#             print aa.split('pid=')

# processinfo(sys.argv[1])

#es.update(index='weibo_xnr_fans_followers',doc_type='uids',id='WXNR0004',body={'doc':{'trace_follow_list':[1264080891,1715330060,1082347151]}})




# es.delete(index='weibo_example_model',doc_type='model',id='wei_quan_qun_ti_lawyer')

# query_body = {
#     'query':{
#         'match_all':{}
#     },
#     'size':'1000'
# }

# results = es.search(index='facebook_user',doc_type='user',body=query_body)['hits']['hits']

# _id_list = []

# for result in results:

#     result = result['_source']

#     _id = result['uid']

#     _id_list.append(_id)

# print '_id_list...',_id_list


# # agg 
# def count_statis():

#     query_body = {
#         'query':{    
#             'bool':{
#                 'must':[
#                     {'range':{'update_time':{'gt':1507774875,'lte':1507812886}}}
#                 ]
#             }
#         },
#         'aggs':{
#             'all_fids':{
#                 'terms':{
#                     'field':'fid',
#                     'order':{'stats_share.max':'desc'},
#                     'size':100
#                 },
#                 'aggs':{
#                     'stats_share':{
#                         'stats':{
#                             'field':'share'
#                         }
#                     }
#                 }

#             }
#         }
#     }

#     results = es.search(index='facebook_count_2017-10-12',doc_type='text',\
#         body=query_body)['aggregations']['all_fids']['buckets']

#     import copy
#     results_origin = copy.deepcopy(results)

#     fid_share_dict = {}
#     results.sort(key=lambda x:(x['stats_share']['max']-x['stats_share']['min']),reverse=True)
    
#     fid_list = [item['key'] for item in results if (item['stats_share']['max']-item['stats_share']['min']) > 10]

#     TOP_HOT_FB = 100

#     if len(fid_list) < TOP_HOT_FB:

#         fid_list_2 = [item['key'] for item in results_origin[:TOP_HOT_FB - len(fid_list)]]

#         fid_list.extend(fid_list_2)


#count_statis()
# results =  es.search(index='twitter_flow_text_2017-10-25',doc_type='text',body={'query':{'match_all':{}},'size':100})['hits']['hits']
# tid_list = [item['_source']['tid'] for item in results]
# print 'tid_list',tid_list

# def search():
    
#     white_uid_list = ['123']
#     query_item = 'keywords_string'
    
#     nest_query_list = []
#     keyword_list = [u'载人飞船',u'领袖',u'黄金',u'原油']
#     for keyword in keyword_list:
#         #nest_query_list.append({'match':{query_item:keyword}})
#         nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})

#     SHOULD_PERCENT = 3

#     query_body = {
#         'query':{
#             'bool':{
#                 'should':nest_query_list,
#                 "minimum_should_match": SHOULD_PERCENT,
#                 'must_not':{'terms':{'uid':white_uid_list}}
#             }
#         },
#         'size':20,
#         'sort':[{'user_fansnum':{'order':'desc'}}]
#     }
    
#     es_results = es_flow_text.search(index='flow_text_2016-11-19',doc_type='text',\
#                 body=query_body)['hits']['hits']

#     print 'results...',es_results

#search()       

# item = {'fid':'6679197029855974713','uid':'100018797745111','timestamp':1508934020,'text':u'周五！'}
# es.index(index='facebook_flow_text_2017-10-25',doc_type='text',body=item,id='6679197029855974713')

# item_dict = {'tid':'956863562332475392','uid':'935416088380153856','timestamp':1508934030,'text':'hahaha'}
# es.index(index='twitter_flow_text_2017-10-25',doc_type='text',body=item_dict,id='956863562332475392')

# es.delete(index='tw_xnr_fans_followers',doc_type='uids',id='FXNR0003')

#es.delete(index='facebook_flow_text_2017-10-25',doc_type='text',id='6679197029855974713')

# query_sensitive = {
#                     'query':{
#                         'match_all':{}
#                     },
#                     "aggs" : {
#                         "uids" : {
#                             "terms" : {
#                               "field" : "uid",
#                               "order": {
#                                 "avg_sensitive" : "desc" 
#                               }
#                             },
#                             "aggs": {
#                                 "avg_sensitive": {
#                                     "avg": {"field": "sensitive"} 
#                                 }
#                             }
#                         }
#                     },
#                     'size':5
#                 }

# q = es.search(index='facebook_flow_text_2017-10-25',doc_type='text',body=query_sensitive)['aggregations']                

# print 'q..',q

# query_body = {
# 	'query':{
# 		'bool':{
# 			'must':[
# 				{'term':{'uid':'183774741715570'}},
# 				{'term':{'text':'明镜新闻网 shared a link.'}}
# 			]
# 		}
# 	}
# }


# r = es.search(index='facebook_flow_text_2017-10-15',doc_type='text',body=query_body)['hits']['hits']
# print 'r..',r

es.delete(index='qq_xnr',doc_type='user',id='QXNR0008')
#es.indices.put_mapping(index='qq_xnr', doc_type='user', body={"properties": {"group_info" : {"type": "string", "index":"not_analyzed"}}})
# print es.update(index='weibo_xnr',doc_type='user',id='WXNR0004',body={'doc':{'password':'xnr1234567'}})
