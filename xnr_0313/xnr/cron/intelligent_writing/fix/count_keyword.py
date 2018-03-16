# -*- coding: utf-8 -*-
import os
import sys
import json 
sys.path.append('../../../../')
# sys.path.append('../')
AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../public/')
sys.path.append(AB_PATH)
#print sys.path
#sys.path.append('../public/')
#from global_utils import getTopicByNameStEt,getWeiboByNameStEt
from time_utils import datetime2ts, ts2HourlyTime,ts2datetime_full
#from global_config import db,weibo_es,weibo_index_name,weibo_index_type,MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO,NEWS_LIMIT,\
from global_config import weibo_es,weibo_index_name,weibo_index_type,MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO,NEWS_LIMIT,\
                            index_event_analysis_results,type_event_analysis_results,\
                            topics_river_index_name,topics_river_index_type,subopinion_index_name,subopinion_index_type
import re
#from ad_filter import ad_filter
#sys.path.append('/home/cron/language/public')
#print sys.path
from comment_module import comments_calculation_v2
from weibo_module import weibo_calculation
from fix_config import default_task_id, \
        default_cluster_num, default_cluster_eva_min_size, \
        default_vsm, ALLOWED_EXTENSIONS, UPLOAD_FOLDER, \
        RESULT_FOLDER, emotions_vk_v1, LOG_FOLDER,RESULT_WEIBO_FOLDER,LOG_WEIBO_FOLDER,\
        UPLOAD_WEIBO_FOLDER

Minute = 60
Fifteenminutes = 15 * 60
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24


def count_fre(topic,start_ts,over_ts,news_limit,weibo_limit,during=Fifteenminutes):   #高频词
    # query_body = {
    #     'query':{
    #         'filtered':{
    #             'filter':{
    #                 'range':{
    #                     'timestamp':{'gte': start_ts, 'lt':over_ts} 
    #                 }
    #             }
    #         }
    #     },
    #     'size':weibo_limit  #
    # }
    # keywords_dict = {}
    # keyword_weibo = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)['hits']['hits']   
    # news_list = []#新闻类微博
    # normal_list = []#主观微博
    # print len(keyword_weibo)
    # for key_weibo in keyword_weibo:
    	#keywords_dict_list = json.loads(key_weibo['_source']['keywords_dict'])  #
        # for k,v in keywords_dict_list.iteritems():
        #     try:
        #         keywords_dict[k] += v
        #     except:
        #         keywords_dict[k] = v
    #     text_weibo = key_weibo['_source']['text']
    #     mid_weibo = key_weibo['_source']['mid']
    #     timestamp = key_weibo['_source']['timestamp']
    #     comment = key_weibo['_source']['comment']
    #     retweeted = key_weibo['_source']['retweeted']
    #     uid = key_weibo['_source']['uid']
    #     pattern = re.compile(r'【.*】')
    #     find_news = pattern.findall(text_weibo.encode('utf8'))

    #     if find_news:
    #         news_list.append({'news_id':'news','content168':text_weibo,'id':mid_weibo,'datetime':ts2datetime_full(timestamp),'comment':comment,'retweeted':retweeted})
    #     else:
    #         normal_list.append({'news_id':'weibo','content':text_weibo,'id':mid_weibo,'datetime':ts2datetime_full(timestamp),'comment':comment,'retweeted':retweeted,'uid':uid})

    # #词频
    # word_results = sorted(keywords_dict.iteritems(),key=lambda x:x[1],reverse=True)[:w_limit]   

    #新闻类微博：词云、主题河、鱼骨图   主题河：拿到主题后，按时间段查相关微博的数量；鱼骨图：每个主题的一个微博及所有微博
    #    return json.dumps({"features":features, "cluster_dump_dict":cluster_dump_dict})
    #taskid = topic+'_'+str(start_ts)+'_'+str(over_ts)
    #子观点微博
    language_results = {}

    normal_list = subopinion_content(topic,start_ts,over_ts,weibo_limit) #读主观微博
    weibo_classify = json.loads(weibo_comments_list(topic,start_ts,over_ts,weibo_list=normal_list))  #

    subopinion_results = weibo_classify['features']
    subopinion_weibo_results = weibo_classify['cluster_dump_dict']

    #主题河
    news_list = news_content(topic,start_ts,over_ts,news_limit)   #读新闻微博
    print '85',len(news_list)
    news_classify = json.loads(news_comments_list(topic,start_ts,over_ts,weibo_list=news_list))  #聚类后存到es里

    news_topics = news_classify['features']
    fish_topics = news_classify['cluster_dump_dict']

    

    #print news_classify,type(news_classify)
    # news_topics = news_classify['features']
    # fish_topics = news_classify['cluster_dump_dict']


    #按类分时间段对应的微博数
    zhutihe_results = cul_key_weibo_time_count(topic,news_topics,start_ts,over_ts,during)


    #print key_weibo_time_count  #{u'9b2de1b6-ce42-405f-a5b4-661ebe10a5b4': {1469030400: 0, 1469089800: 12, 1469149200: 10, 1468948500: 0, 1469208600: 0}
      
    #主观微博：子观点排序
    #return json.dumps({"features":features,"ratio": ratio_results,"cluster_dump_dict":cluster_dump_dict})


    #聚类后存到es里
    #print weibo_classify,type(weibo_classify)
    # subopinion_results = weibo_classify['features']
    # subopinion_weibo_results = weibo_classify['cluster_dump_dict']
        

    #return json.dumps({'zhutihe_results':zhutihe_results,'subopinion_results':subopinion_results})
    # for i in w_results:
    #     results.append({i[0]:i[1]})
    # print results

    language_results['subopinion_results'] = subopinion_results
    language_results['subopinion_weibo_results'] = subopinion_weibo_results
    language_results['news_topics'] = news_topics
    language_results['fish_topics'] = fish_topics
    language_results['event_river'] = zhutihe_results

    language_results = json.dumps(language_results)
    save_results_es(topic, language_results)
    return language_results


def save_results_es(topic, language_results):

    #mappings_event_analysis_results(topic)
    index_name = index_event_analysis_results
    index_type = type_event_analysis_results

    id = topic

    try:
        item_exist = weibo_es.get(index=index_name,doc_type=index_type,id=id)['_source']
        weibo_es.update(index=index_name,doc_type=index_type,id=id,body={'doc':{'language_results':language_results}})
    except Exception,e:
        weibo_es.index(index=index_name,doc_type=index_type,id=id,body={'language_results':language_results})





def news_content(topic,start_ts,end_ts,news_limit = NEWS_LIMIT):
    query_body ={'query':{
                    'bool':{
                        'must':[
                            {'wildcard':{'text':'*【*】*'}},
                            {'range':{'timestamp':{'lt':end_ts,'gte':start_ts}}
                        }]
                    }
                },
                'size':news_limit  
                }
    news_results = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)['hits']['hits']#['_source']
    # print topic,weibo_index_type,start_ts,end_ts,query_body
    # print news_results
    news_list = []
    for key_weibo in news_results:
        text_weibo = key_weibo['_source']['text']
        mid_weibo = key_weibo['_source']['mid']
        timestamp = key_weibo['_source']['timestamp']
        comment = key_weibo['_source']['comment']
        retweeted = key_weibo['_source']['retweeted']
        uid = key_weibo['_source']['uid']
        news_list.append({'news_id':'news','content168':text_weibo,'id':mid_weibo,'datetime':ts2datetime_full(timestamp),'comment':comment,'retweeted':retweeted})
    return news_list

def subopinion_content(topic,start_ts,end_ts,weibo_limit):
    query_body ={'query':{
                    'bool':{
                        'must_not':[
                            {'wildcard':{'text':'*【*】*'}}],
                        'must':[
                            {'range':{'timestamp':{'lt':end_ts,'gte':start_ts}}
                        }]
                    }
                },
                'size':weibo_limit  
                }
    subopinion_results = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)['hits']['hits']#['_source']
    normal_list = []
    for key_weibo in subopinion_results:
        text_weibo = key_weibo['_source']['text']
        mid_weibo = key_weibo['_source']['mid']
        timestamp = key_weibo['_source']['timestamp']
        try:
            comment = key_weibo['_source']['comment']
        except:
            comment = 0
        try:
            retweeted = key_weibo['_source']['retweeted']
        except:
            retweeted = 0
        uid = key_weibo['_source']['uid']
        normal_list.append({'news_id':'weibo','content':text_weibo,'id':mid_weibo,'datetime':ts2datetime_full(timestamp),'comment':comment,'retweeted':retweeted,'uid':uid})
    return normal_list    

def cul_key_weibo_time_count(topic,news_topics,start_ts,over_ts,during):
    key_weibo_time_count = {}
    time_dict = {}
    for clusterid,keywords in news_topics.iteritems(): #{u'd2e97cf7-fc43-4982-8405-2d215b3e1fea': [u'\u77e5\u8bc6', u'\u5e7f\u5dde', u'\u9009\u624b']}
        start_ts = int(start_ts)
        over_ts = int(over_ts)

        over_ts = ts2HourlyTime(over_ts, during)
        interval = (over_ts - start_ts) / during


        for i in range(interval, 0, -1):    #时间段取每900秒的

            begin_ts = over_ts - during * i
            end_ts = begin_ts + during
            must_list=[]
            must_list.append({'range':{'timestamp':{'gte':begin_ts,'lt':end_ts}}})
            temp = []
            for word in keywords:
                sentence =  {"wildcard":{"keywords_string":"*"+word+"*"}}
                temp.append(sentence)
            must_list.append({'bool':{'should':temp}})

            query_body = {"query":{
                            "bool":{
                                "must":must_list
                            }
                        }
                    }
            key_weibo = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)
            key_weibo_count = key_weibo['hits']['total']  #分时间段的类的数量
            time_dict[end_ts] = key_weibo_count
        key_weibo_time_count[clusterid] = time_dict
        return key_weibo_time_count

 

def news_comments_list(taskid,start_ts,over_ts,weibo_list,cluster_num=-1,cluster_eva_min_size=default_cluster_eva_min_size,vsm=default_vsm,calculation_label=1):#weibo_list把微博读进来
    """计算饼图数据，并将饼图数据和去重后的推荐文本写到文件
    taskid = request.args.get('taskid', default_task_id)
    cluster_num = request.args.get('cluster_num', default_cluster_num) #若无此参数，取-1；否则取用户设定值
    if cluster_num == default_cluster_num:
        cluster_num = -1
    cluster_eva_min_size = request.args.get('cluster_eva_min_size', default_cluster_eva_min_size)
    vsm = request.args.get('vsm', default_vsm)
    calculation_label = int(request.args.get('calcu', 1)) # 默认进行重新计算, 0表示从从已有结果数据文件加载数据
    """
    params = {"taskid": taskid, "cluster_num": cluster_num, "cluster_eva_min_size": cluster_eva_min_size, \
            "vsm": vsm, "calculation_label": calculation_label}

    comments = weibo_list
    logfile = os.path.join(LOG_FOLDER, taskid + '.log')

    cal_results = comments_calculation_v2(comments, logfile=logfile, cluster_num=cluster_num, \
            cluster_eva_min_size=int(cluster_eva_min_size), version=vsm)
    #print cal_results
    features = cal_results['cluster_infos']['features']
    item_infos = cal_results['item_infos']
    cluster_ratio = dict()
    senti_ratio = dict()
    sentiment_results = dict()
    cluster_results = dict()
    rub_results = []

    # 过滤前文本数
    before_filter_count = len(item_infos)
    # 过滤后文本数
    after_filter_count = 0

    download_items = []
    for comment in item_infos:
        # print comment
        download_item = {}
        download_item["id"] = comment["id"]
        download_item["title"] = comment["title"]
        download_item["text"] = comment["text"]
        # download_item["timestamp"] = comment["timestamp"]
        download_item["datetime"] = comment["datetime"]
        download_item["clusterid"] = comment["clusterid"]
        download_item["sentiment"] = comment["sentiment"]
        download_item["ad_label"] = comment["ad_label"]
        if (comment["clusterid"][:8] != 'nonsense') and (comment["clusterid"] != 'other'):
            download_item["duplicate"] = comment["duplicate"]
            download_item["same_from"] = comment["same_from"]
        download_items.append(download_item)
        if ('clusterid' in comment) and (comment['clusterid'][:8] != 'nonsense') : 
            clusterid = comment['clusterid']

            try:
                cluster_ratio[clusterid] += 1
            except KeyError:
                cluster_ratio[clusterid] = 1
            try:
                cluster_results[clusterid].append(comment)
            except KeyError:
                cluster_results[clusterid] = [comment]

        if ('sentiment' in comment) and (comment['sentiment'] in emotions_vk_v1) and ('clusterid' in comment) \
                and (comment['clusterid'][:8] != 'nonsense'):
            sentiment = comment['sentiment']

            try:
                senti_ratio[sentiment] += 1
            except KeyError:
                senti_ratio[sentiment] = 1
            try:
                sentiment_results[sentiment].append(comment)
            except KeyError:
                sentiment_results[sentiment] = [comment]

            after_filter_count += 1

        if comment['clusterid'][:8] == 'nonsense':
            rub_results.append(comment)

    ratio_results = dict()
    ratio_total_count = sum(cluster_ratio.values())
    for clusterid, ratio in cluster_ratio.iteritems():
        if clusterid in features:
            feature = features[clusterid]
            if feature and len(feature):
                ratio_results[','.join(feature[:3])] = float(ratio) / float(ratio_total_count)

    sentiratio_results = dict()
    sentiratio_total_count = sum(senti_ratio.values())
    for sentiment, ratio in senti_ratio.iteritems():
        if sentiment in emotions_vk_v1:
            label = emotions_vk_v1[sentiment]
            if label and len(label):
                sentiratio_results[label] = float(ratio) / float(sentiratio_total_count)

    # 情感分类去重
    sentiment_dump_dict = dict()
    for sentiment, contents in sentiment_results.iteritems():
        dump_dict = dict()
        for comment in contents:
            same_from_sentiment = comment["same_from_sentiment"]
            try:
                dump_dict[same_from_sentiment].append(comment)
            except KeyError:
                dump_dict[same_from_sentiment] = [comment]
        sentiment_dump_dict[sentiment] = dump_dict

    # 子观点分类去重
    cluster_dump_dict = dict()
    for clusterid, contents in cluster_results.iteritems():
        if clusterid in features:
            feature = features[clusterid]
            if feature and len(feature):
                dump_dict = dict()
                for comment in contents:
                    same_from_cluster = comment["same_from"]
                    try:
                        dump_dict[same_from_cluster].append(comment)
                    except KeyError:
                        dump_dict[same_from_cluster] = [comment]
                    for k,v in dump_dict.iteritems():
                        sort_dump_dict = sorted(v,key=lambda x:x['weight'],reverse=True)
                    cluster_dump_dict[clusterid] = sort_dump_dict

    # dump_file = open(task_result_file+'_news', 'w')
    # dump_file.write(json.dumps({"params": params, "features":features, "senti_dump_dict":sentiment_dump_dict, \
    #         "cluster_dump_dict":cluster_dump_dict, "ratio":ratio_results, "sentiratio": sentiratio_results, \
    #         "before_filter_count": before_filter_count, "after_filter_count": after_filter_count}))
    # dump_file.close()
    # new_file = open(task_result_file+'_news_2','w')
    # print task_result_file+'2'  #所有的微博
    # for i in xrange(0,len(download_items)):
    #     new_file.write(json.dumps(download_items[i])+'\n')
    # new_file.close
    #task = taskid.split('_')
    #index_body={'name':task[0],'start_ts':task[1],'end_ts':task[2],'features':json.dumps(features),'cluster_dump_dict':json.dumps(cluster_dump_dict)}
    
    index_body={'name':taskid,'start_ts':start_ts,'end_ts':over_ts,'features':json.dumps(features),'cluster_dump_dict':json.dumps(cluster_dump_dict)}
    weibo_es.index(index=topics_river_index_name,doc_type=topics_river_index_type,id=taskid,body=index_body)

    return json.dumps({"features":features, "cluster_dump_dict":cluster_dump_dict})
    # return json.dumps(download_items)


def weibo_comments_list(taskid,start_ts,over_ts,weibo_list,cluster_num=-1,cluster_eva_min_size=default_cluster_eva_min_size,vsm=default_vsm,calculation_label=1):#weibo_list把微博读进来

    params = {"taskid": taskid, "cluster_num": cluster_num, "cluster_eva_min_size": cluster_eva_min_size, \
            "vsm": vsm, "calculation_label": calculation_label}

    task_result_file = os.path.join(RESULT_WEIBO_FOLDER, taskid)
    if os.path.exists(task_result_file) and calculation_label == 0:
        # 从已有数据文件加载结果集
        with open(task_result_file) as dump_file:
            dump_dict = json.loads(dump_file.read())
            ratio_results = dump_dict["ratio"]
            sentiratio_results = dump_dict["sentiratio"]
            before_filter_count = dump_dict["before_filter_count"]
            after_filter_count = dump_dict["after_filter_count"]

        return json.dumps({"ratio": ratio_results, "sentiratio": sentiratio_results, \
                "before_filter_count": before_filter_count, "after_filter_count": after_filter_count})

    comments = weibo_list
    print 'weibo_list:',len(comments)
    logfile = os.path.join(LOG_WEIBO_FOLDER, taskid + '.log')
    cal_results = weibo_calculation(comments, logfile=logfile, cluster_num=cluster_num, \
            cluster_eva_min_size=int(cluster_eva_min_size), version=vsm)
    features = cal_results['cluster_infos']['features']
    item_infos = cal_results['item_infos']
  
    cluster_ratio = dict()
    senti_ratio = dict()
    sentiment_results = dict()
    cluster_results = dict()
    rub_results = []

    # 过滤前文本数
    before_filter_count = len(item_infos)
    # 过滤后文本数
    after_filter_count = 0

    download_items = []
    for comment in item_infos:  
        #print comment["clusterid"]
        download_item = {}
        #comment = item_infos[comment]
        download_item["id"] = comment["id"]
        download_item["text"] = comment["text"]
        download_item["clusterid"] = comment["clusterid"]
        download_item["ad_label"] = comment["ad_label"]
        download_item["comment"] = comment["comment"]
        download_item["datetime"] = comment["datetime"]
        download_item["retweeted"] = comment["retweeted"]
        download_item["uid"] = comment["uid"]
        # download_item["same_from"] = comment["same_from"]
        download_items.append(download_item)
        if ('clusterid' in comment) and (comment['clusterid'][:8] != 'nonsense') : 
            clusterid = comment['clusterid']

            try:
                cluster_ratio[clusterid] += 1
            except KeyError:
                cluster_ratio[clusterid] = 1
            try:
                cluster_results[clusterid].append(comment)
            except KeyError:
                cluster_results[clusterid] = [comment]

        # if ('sentiment' in comment) and (comment['sentiment'] in emotions_vk_v1) and ('clusterid' in comment) \
        #         and (comment['clusterid'][:8] != 'nonsense'):
        #     sentiment = comment['sentiment']

        #     try:
        #         senti_ratio[sentiment] += 1
        #     except KeyError:
        #         senti_ratio[sentiment] = 1
        #     try:
        #         sentiment_results[sentiment].append(comment)
        #     except KeyError:
        #         sentiment_results[sentiment] = [comment]

        #     after_filter_count += 1

        if comment['clusterid'][:8] == 'nonsense':
            rub_results.append(comment)

    ratio_results = dict()
    ratio_total_count = sum(cluster_ratio.values())
    for clusterid, ratio in cluster_ratio.iteritems():
        if clusterid in features:
            feature = features[clusterid]
            if feature and len(feature):
                ratio_results[','.join(feature[:3])] = float(ratio) / float(ratio_total_count)

    #jln0825 没有情感的东西 不要了
    # sentiratio_results = dict()
    # sentiratio_total_count = sum(senti_ratio.values())
    # for sentiment, ratio in senti_ratio.iteritems():
    #     if sentiment in emotions_vk_v1:
    #         label = emotions_vk_v1[sentiment]
    #         if label and len(label):
    #             sentiratio_results[label] = float(ratio) / float(sentiratio_total_count)

    # # 情感分类去重
    # sentiment_dump_dict = dict()
    # for sentiment, contents in sentiment_results.iteritems():
    #     dump_dict = dict()
    #     for comment in contents:
    #         same_from_sentiment = comment["same_from_sentiment"]
    #         try:
    #             dump_dict[same_from_sentiment].append(comment)
    #         except KeyError:
    #             dump_dict[same_from_sentiment] = [comment]
    #     sentiment_dump_dict[sentiment] = dump_dict

    # 子观点分类去重
    cluster_dump_dict = dict()
    for clusterid, contents in cluster_results.iteritems():
        #print clusterid
        if clusterid in features:
            feature = features[clusterid]
            if feature and len(feature):
                dump_dict = dict()
                for comment in contents:
                    same_from_cluster = comment["same_from"]
                    try:
                        dump_dict[same_from_cluster].append(comment)
                    except KeyError:
                        dump_dict[same_from_cluster] = [comment]
                    cluster_dump_dict[clusterid] = dump_dict

    #task = taskid.split('_')
    for key in features.keys():
        print features[key],type(features[key])
        keys = ('_').join(features[key])
        #index_body={'name':task[0],'start_ts':task[1],'end_ts':task[2],'ratio':json.dumps(ratio_results),'cluster':json.dumps(key),'features':json.dumps(features),'keys':keys,'cluster_dump_dict':json.dumps(cluster_dump_dict[key])}
        index_body={'name':taskid,'start_ts':start_ts,'end_ts':over_ts,'ratio':json.dumps(ratio_results),'cluster':json.dumps(key),'features':json.dumps(features),'keys':keys,'cluster_dump_dict':json.dumps(cluster_dump_dict[key])}
        #print index_body
        #print subopinion_index_type,subopinion_index_name
        #jln  0907
        weibo_es.index(index=subopinion_index_name,doc_type=subopinion_index_type,id=key,body=index_body)


    return json.dumps({"features":features,"ratio": ratio_results,"cluster_dump_dict":cluster_dump_dict})#features关键词和类的对应



if __name__ == '__main__':
    #topic = sys.argv[1] # u'香港自由行' u'张灵甫遗骨疑似被埋羊圈' u'高校思想宣传' u'高校宣传思想工作' u'外滩踩踏' 'APEC' u'全军政治工作会议'
    #start_date = sys.argv[2] # '2015-02-23'
    #end_date = sys.argv[3] # '2015-03-02'


    # topic = u'奥运会'
    # topic_id = getTopicByNameStEt(topic,START_TS,END_TS) #通过中文名得到英文名
    # topic = topic_id[0]['_source']['index_name']
    #print weibo_es.delete(index='subopinion',doc_type='text',id='direct')

    topic = 'aoyunhui'
    start_date = '2016-07-20'
    end_date = '2016-08-20'

    #topic = topic.decode('utf-8')
    start_ts = datetime2ts(start_date)
    end_ts = datetime2ts(end_date)

    # start_ts = 1469680510
    # end_ts = 1469680515
    print 'topic: ', topic, 'from %s to %s' % (start_ts, end_ts)    
    count_fre(topic, start_ts=start_ts, over_ts=end_ts,news_limit=NEWS_LIMIT,weibo_limit=2000)#w_limit=MAX_FREQUENT_WORDS,weibo_limit=MAX_LANGUAGE_WEIBO
