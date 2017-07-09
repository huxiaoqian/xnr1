# -*- coding:utf-8 -*-

'''
weibo information monitor function about database task
'''

import sys
import time,datetime
from xnr.global_utils import es_flow_text,flow_text_index_name_pre,flow_text_index_type
from xnr.parameter import MAX_VALUE
from xnr.time_utils import ts2datetime
from elasticsearch import Elasticsearch

#from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
#from scipy.misc import imread
#import matplotlib.pyplot as plt

#S_FLOW_TEXT_HOST=['219.224.134.216:9201','219.224.134.217:9201','219.224.134.218:9201']
#s_flow_text=Elasticsearch(ES_FLOW_TEXT_HOST,timeout=600)
#low_text_index_name_pre='flow_text_'
#low_text_index_type='text'
#ef ts2datetime(ts):
#   return time.strftime('%Y-%m-%d',time.localtime(ts))

#lookup weiboxnr_content example test,can be delete
def show_weiboxnr_content():
    results=[]
    query_body={
            "query":{
                "match_all":{}
            }
            }
    results= es_flow_text.search(index="flow_text_2016-11-11",doc_type="text",body=query_body)
    return results


#lookup keywordslist test,can be delete
def lookup_weiboxnr_keywordslist():
    results=[]
    query_body={
            'query':{
                'match_all':{}
                },
            }
    results=es_flow_text.search(index="flow_text_2016-11-18",doc_type=flow_text_index_type,body=query_body)
   # keywords_list=[]
   # if results:
   #     for item in results:
   #         keywords_list.append(item["_source"]["uid"])
   # return keywords_list
    return results


#lookup all users
def lookup_weibo_users():
    query_body={
            'query':{
                'match_all':{}
                },
            }
    results=es_flow_text.search(index='weibo_user',doc_type=user,body=query_body)
    weibo_users=[]
    for item in results:
        weibo_users.append(item['_source']['uid'])
    return weibo_users


#lookup weibo_xnr concerned users
#def lookup_weiboxnr_concernedusers(weiboxnr_id):



#lookup weibo_xnr unattended users
#def lookup_weiboxnr_unattendedusers(weiboxnr_id):

#lookup weibo info based on userlist and time
def lookup_weibo_info(ts_first,ts_second,userlist):
    time1=time.mktime(ts_first.timetuple())
    time2=time.mktime(ts_second.timetuple())
    query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'terms':{'uid':userlist}},
                                {'range':{
                                    'timestamp':{
                                        'gte':time1,
                                        'lte':time2
                                        }
                                    }}
                                ]
                            }
                        }
                    }
                },
           #'size':999999
            'size':MAX_VALUE
            }

    datetime_1=ts2datetime(time1)
    datetime_2=ts2datetime(time2)
    index_name_1=flow_text_index_name_pre+datetime_1
    print index_name_1
    exist_es_1=es_flow_text.indices.exists(index_name_1)
    index_name_2=flow_text_index_name_pre+datetime_2
    exist_es_2=es_flow_text.indices.exists(index_name_2)


    if datetime_1 == datetime_2 and exist_es_1:
        search_results=es_flow_text.search(index=index_name_1,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    elif datetime_1 !=datetime_2 and exist_es_2:
        search_results=es_flow_text.search(index=index_name_2,doc_tyoe=flow_text_index_type,body=query_body)['hits']['hits']
    else:
        search_results=[]
   # search_results=es_flow_text.search(index=index_name_1,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
   # print search_results
    keyword_list=[]
    if search_results:
        for item in search_results:
            keyword_list.append(item['_source']['keywords_string'])

   # return search_results
    return keyword_list


#count the keyword 
def count_weiboxnr_keyword(keyword_list):
    word_list=[]
    for item in keyword_list:
        words=item.split('&')
        word_list.extend(words)
    keyword_dict={}
    for word in word_list:
        keyword_dict[word]=word_list.count(word)
    return keyword_dict


#create wordcloud based on keywords
#def create_weiboxnr_keywordcloud(keyword_dict):
#    abel_mask=plt.imread('../static/img/weibo_monitor/keyword_mask.jpg')
#    key_wordcloud=WordCloud(
#            background_color='white',
#            mask=abel_mask,
#            max_words=500,
#            stopwords=STOPWORDS,
            #font_oath='C:/Uers/Windows/fonts/simkai.ttf',
#            max_font_size=400,
#            random_state=50,
#            scale=.5
#            ).generate_from_frequencies(keyword_dict)

#    image_colors=ImageColorGenerator(abel_mask)
#    key_wordcloud.recolor(color_func=image_colors)
#    key_wordcloud.to_file('../static/img/weibo_monitor/keywordcloud.jpg')

#lookup hot posts
'''
def lookup_hot_posts(classify_id):
    #classify choice
    if classify_id==0:
        userlist=lookup_weibo_users()
    elif classify_id==1:
        userlist=lookup_weiboxnr_concernedusers(weiboxnr_id)
    elif classify_id==2:
        userlist=lookup_weoboxnr_unattendedusers(weiboxnr_id)
    else:
        userlist=lookup_weibo_users()

    query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'terms':{'uid':userlist}},
                                {'match':{
                                    'text':{
                                        'query':search_content
                                        }
                                    }
                                    },
                                {'range':{
                                    'timestamp':{
                                        'gle':,
                                        'lte':
                                        }
                                    }
                                    }
                                ]
                            }
                        }
                    }
                },
            'size':MAX_VALUE,
            'sort':{'timestamp':{'order':'desc'}}
            }
            
'''

#test and debug
#if __name__ == "__main__":
#    ts_first='2016/11/15 10:27:12'
#    ts_second='2016/11/15 10:27:14'
#    firsttime=datetime.datetime.strptime(ts_first,'%Y/%m/%d %H:%M:%S')
#    secondtime=datetime.datetime.strptime(ts_second,'%Y/%m/%d %H:%M:%S')
#    userlist=[3033874187,2604977652,3936969641,3964892488]
#    lookup_weibo_info(firsttime,secondtime,userlist)

