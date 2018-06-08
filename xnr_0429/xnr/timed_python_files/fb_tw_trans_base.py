# -*- coding: utf-8 -*-
import redis
from elasticsearch import Elasticsearch
from multiprocessing import Pool, Manager
import os, time, random
import math
import getopt
import sys
from googletrans import Translator
sys.path.append('../cron/trans')
sys.path.append('../')
from global_utils import es_xnr_2 as es, r_37 as r
from facebook_mappings import facebook_flow_text_mappings,facebook_count_mappings,facebook_user_mappings
from twitter_mappings import twitter_flow_text_mappings,twitter_count_mappings,twitter_user_mappings
from global_utils import twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
                    twitter_count_index_name_pre,twitter_count_index_type,\
                    twitter_user_index_name,twitter_user_index_type,\
                    facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
                    facebook_count_index_name_pre,facebook_count_index_type,\
                    facebook_user_index_name,facebook_user_index_type,\
                    twitter_flow_text_trans_task_name,facebook_flow_text_trans_task_name,\
                    twitter_user_trans_task_name,facebook_user_trans_task_name

gap = 10 #指定一个翻译批次的数目
batch = 3000  #指定一个temp处理的批次

def load_batch_data(redis_task):
    redis_task_temp = redis_task + '_temp'
    length = r.llen(redis_task)
    temp = r.lrange(redis_task, length-batch, length-1)
    if temp:
        for t in temp:
            r.rpush(redis_task_temp, eval(t))
        return redis_task_temp
    return False

def remove_batch_data(redis_task, length):
    redis_task_temp = redis_task + '_temp'
    for i in range(length):
        r.rpop(redis_task)
    r.delete(redis_task_temp)

# No JSON object could be decoded。表情真烦。。。翻译通不过，显示No JSON object could be decoded，直接返回原文得了。
def asdjalkfs_trans(qi, target_language='zh-cn'):
    res = []
    for q in qi:
        try:
            translator = Translator()
            text = translator.translate(q,'zh-cn').text
            res.append(text)
        except Exception,e:
            res.append(q)
    return res

# from trans_v2 import trans
def trans(q, target_language='zh-cn'):
    res = []
    try:
        translator = Translator()
        results = translator.translate(q, target_language)
        for result in results:
            res.append(result.text)
    except Exception,e:
        if 'decode' in str(e):
            res = asdjalkfs_trans(q)
        else:
            print 'trans Exception: ', str(e)
    return res

# No JSON object could be decoded。表情真烦。。。翻译通不过，显示No JSON object could be decoded，直接返回原文得了。
def asdjalkfs_trans_with_detail(qi, target_language='zh-cn'):
    res = []
    for q in qi:
        try:
            translator = Translator()
            r = translator.translate(q,'zh-cn')
            res.append((r.text, r.src))
        except Exception,e:
            res.append((q,'en'))
    return res

# 同时返回text,src字段,分别是翻译后的文本和原文本的语言类型
# [(text, src), (text, src), ...]
def trans_with_detail(q, target_language='zh-cn'):
    res = []
    try:
        translator = Translator()
        results = translator.translate(q, target_language)
        for result in results:
            res.append((result.text, result.src))
    except Exception,e:
        if 'decode' in str(e):
            res = asdjalkfs_trans_with_detail(q)
        else:
            print 'trans_with_detail Exception: ', str(e)
    return res

def my_bulk_func(bulk_action, index_name, doc_type):
    # bulk_action: [action,source_item,action,source_item,...]
    try:
        es.bulk(bulk_action,index=index_name,doc_type=doc_type,timeout=600)
    except Exception,e: #如果出现错误，就减小存储的批次，再次出现问题的批次直接放弃
        # print 'my_bulk_func Exception: ', str(e)
        for i in range(len(bulk_action)/2):
            temp_bulk_action = bulk_action[2*i : 2*i+2]
            try:
                es.bulk(temp_bulk_action,index=index_name,doc_type=doc_type,timeout=600)
            except:
                pass

def subprocess_task(li, queue, redis_task, target_language='zh-cn'):
    text_list = []
    id_list = []
    for l in li:
        id_list.append(l[0])
        text_list.append(l[1])
    results = trans_with_detail(text_list, target_language)
    if results:
        for i in range(len(li)):
            if results[i][1] == 'zh-CN':
                flag_ch = 1
            else:
                flag_ch = 0
            #[id, text_ch, flag_ch, date]
            queue.put([li[i][0], results[i][0], flag_ch, li[i][2]])
        return True
    else:   #翻译失败,如果任务出错，则重新加入队列中
        for l in li:
            r.lpush(redis_task, l)
        time.sleep(10)
        return False

def subprocess_task_facebook_user(li, queue, redis_task, target_language='zh-cn'):
    text_list = []
    for l in li:
        text_list.extend(l[1:])
    results = trans(text_list, target_language)
    if results:
        for i in range(len(li)):
            bio_list = results[4*i : 4*i + 4]
            bio_str = '_'.join(bio_list)
            queue.put([li[i][0], bio_str])
        return True
    else:   #翻译失败,如果任务出错，则重新加入队列中
        for l in li:
            r.lpush(redis_task, l)
        time.sleep(10)
        return False

def subprocess_task_twitter_user(li, queue, redis_task, target_language='zh-cn'):
    #[[uid, description, location], ...]
    text_list = []
    for l in li:
        text_list.extend(l[1:])
    results = trans(text_list, target_language)
    if results:
        for i in range(len(li)):
            description, location = results[2*i :  2*i + 2] 
            queue.put([li[i][0], description, location])
        return True
    else:   #翻译失败,如果任务出错，则重新加入队列中
        for l in li:
            r.lpush(redis_task, l)
        time.sleep(10)
        return False


#根据新一轮的结果，更新user表中chinese_user相关信息
def update_chinese_user():
    pass

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ht:u:r:')
        for op, value in opts:
            if op == '-t':
                index_pre = value
            elif op == '-u':
                user_index = value
            elif op == '-r':
                redis_task = value
        print 'translate task details: ', index_pre, user_index, redis_task
        queue = Manager().Queue()

        #判断时text类型的翻译任务还是user类型的翻译任务，分而治之
        if index_pre in ['twitter_flow_text_', 'facebook_flow_text_']:
            bulk_action_all = {}
            count_dict = {}
            count_i = 0
            text_index_pre = index_pre
            redis_task_temp = load_batch_data(redis_task)
            length = r.llen(redis_task_temp)
            while r.llen(redis_task_temp):
                print 'trans start'
                p = Pool()
                while r.llen(redis_task_temp):
                    li = []
                    for i in range(gap):
                        l = r.rpop(redis_task_temp)
                        if l:
                            li.append(eval(l))
                    if li:
                        p.apply_async(subprocess_task, args=(li,queue,redis_task_temp,))
                p.close()
                p.join()
                print 'trans end'
            while not queue.empty():
                item = queue.get(True)
                _id = item[0]
                text_ch = item[1]
                flag_ch = item[2]
                date_time = item[3]
                action = {'update':{'_id': _id}}
                source_item = {'text_ch': text_ch, 'flag_ch': flag_ch}

                #存储
                try:
                    bulk_action_all[date_time].extend([action,{'doc': source_item}])
                    count_dict[date_time] += 1
                    count_i += 1
                except:
                    bulk_action_all[date_time] = [action,{'doc': source_item}]
                    count_dict[date_time] = 1 
                    count_i += 1

                for date, count in count_dict.iteritems():
                    if count % 1000 == 0 :
                        index_name = text_index_pre + date
                        if text_index_pre == 'twitter_flow_text_':
                            twitter_flow_text_mappings(index_name)
                        else:
                            facebook_flow_text_mappings(index_name)
                        if bulk_action_all[date]:
                            # es.bulk(bulk_action_all[date],index=index_name,doc_type='text',timeout=600)
                            my_bulk_func(bulk_action_all[date], index_name, 'text')
                            bulk_action_all[date] = []
            for date, bulk_action in bulk_action_all.iteritems():
                if bulk_action:
                    index_name = text_index_pre + date
                    if text_index_pre == 'twitter_flow_text_':
                        twitter_flow_text_mappings(index_name)
                    else:
                        facebook_flow_text_mappings(index_name)
                    # es.bulk(bulk_action_all[date],index=index_name,doc_type='text',timeout=600)
                    my_bulk_func(bulk_action_all[date], index_name, 'text')
            remove_batch_data(redis_task, length)
            print 'Done.'
        elif index_pre in ['facebook_user', 'twitter_user']:
            if index_pre == 'facebook_user':
                facebook_user_mappings()
                count = 0
                bulk_action = []
                redis_task_temp = load_batch_data(redis_task)
                length = r.llen(redis_task_temp)
                while r.llen(redis_task_temp):
                    print 'trans start'
                    p = Pool()
                    while r.llen(redis_task_temp):
                        li = []
                        for i in range(gap):
                            l = r.rpop(redis_task_temp)
                            if l:
                                li.append(eval(l))
                        if li:
                            p.apply_async(subprocess_task_facebook_user, args=(li,queue,redis_task_temp,))
                    p.close()
                    p.join()
                    print 'trans end'
                while not queue.empty():
                    item = queue.get(True)
                    uid = item[0]
                    bio_str = item[1]
                    action = {'update':{'_id': uid}}
                    source_item = {'bio_str': bio_str}
                    count += 1
                    bulk_action.extend([action,{'doc': source_item}])
                    if count % 1000 == 0:
                        # es.bulk(bulk_action, index=index_pre, doc_type='user')
                        my_bulk_func(bulk_action, index_pre, 'user')
                        bulk_action = []
                if bulk_action:
                    # es.bulk(bulk_action, index=index_pre, doc_type='user')
                    my_bulk_func(bulk_action, index_pre, 'user')
                remove_batch_data(redis_task, length)
                print 'Done.'
            else:   #twitter_user
                twitter_user_mappings()
                count = 0
                bulk_action = []
                redis_task_temp = load_batch_data(redis_task)
                length = r.llen(redis_task_temp)
                #[[uid, description, location], ...]
                while r.llen(redis_task_temp):
                    print 'trans start'
                    p = Pool()
                    while r.llen(redis_task_temp):
                        li = []
                        for i in range(gap):
                            l = r.rpop(redis_task_temp)
                            if l:
                                li.append(eval(l))
                        if li:
                            p.apply_async(subprocess_task_twitter_user, args=(li,queue,redis_task_temp,))
                    p.close()
                    p.join()
                    print 'trans end'
                while not queue.empty():
                    item = queue.get(True)
                    uid = item[0]
                    description = item[1]
                    location = item[2]
                    action = {'update':{'_id': uid}}
                    source_item = {'description_ch': description, 'location_ch': location}
                    count += 1
                    bulk_action.extend([action,{'doc': source_item}])
                    if count % 1000 == 0:
                        # es.bulk(bulk_action, index=index_pre, doc_type='user')
                        my_bulk_func(bulk_action, index_pre, 'user')
                        bulk_action = []
                if bulk_action:
                    # es.bulk(bulk_action, index=index_pre, doc_type='user')
                    my_bulk_func(bulk_action, index_pre, 'user')
                remove_batch_data(redis_task, length)
                print 'Done.'
    except Exception,e:
        print 'Translate Task Exception:', str(e)

