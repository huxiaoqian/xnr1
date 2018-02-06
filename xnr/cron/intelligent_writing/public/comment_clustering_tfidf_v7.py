# -*- coding: utf-8 -*-

import os
import time
import math
import uuid
import csv
import re
import heapq
import numpy as np
from gensim import corpora
from collections import Counter
from utils_public import cut_words, cut_words_noun
from ad_filter import market_words
from load_settings import load_settings

settings = load_settings()
CLUTO_FOLDER = settings.get("CLUSTERING_CLUTO_FOLDER")
CLUTO_EXECUTE_PATH = settings.get("CLUSTERING_CLUTO_EXECUTE_PATH")
PROCESS_FOR_CLUTO_VERSION = settings.get("COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION")
PROCESS_GRAM = settings.get("COMMENT_CLUSTERING_PROCESS_GRAM")
CLUSTERING_KMEANS_CLUSTERING_NUM = settings.get("CLUSTERING_KMEANS_CLUSTERING_NUM")
CLUSTERING_CLUTO_EXECUTE_PATH = settings.get("CLUSTERING_CLUTO_EXECUTE_PATH")
COMMENT_CLUSTERING_CLUSTER_EVA_MIN_SIZE = settings.get("COMMENT_CLUSTERING_CLUSTER_EVA_MIN_SIZE")
WORD_LIST_TOP_PERCENT = settings.get("WORD_LIST_TOP_PERCENT")
MIN_CLUSTER_NUM = settings.get("MIN_CLUSTER_NUM")
MAX_CLUSTER_NUM = settings.get("MAX_CLUSTER_NUM")
COMMENT_WORDS_CLUSTER_NUM = settings.get("COMMENT_WORDS_CLUSTER_NUM")

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')

def freq_word_comment(items):
    '''
    统计一条评论中的名词
    输入数据：
        items:新闻组成的列表:字典, 数据示例：[{'item的下标':评论id,'news_id':新闻id,'content':新闻内容}]
    输出数据：
        top_word:词和词频构成的列表，{词：词频率}
        word_comment:每条评论的名词，{"_id":[名词1，名词2，...]}
    '''
    words_list = []
    word_comment = {} # 记录每条评论的名词
    for item in items:
        text = item['content']
        words = cut_words_noun(text)
        word_item = []
        for w in words:
            words_list.append(w)
            word_item.append(w)
        word_comment[items.index(item)]=word_item

    counter = Counter(words_list)
    total = sum(counter.values())#总词频数
    topk_words = counter.most_common()
    top_word = {k:float(v)/float(total) for k,v in topk_words}

    return top_word,word_comment

def freq_word_news(item):
    '''
    统计新闻的名词
    输入数据:新闻，字符串
    输出数据:新闻的词及词频率字典，{词：词频率}
    '''
    words_list = []
    words = cut_words_noun(item)
    word_item = []
    for w in words:
        words_list.append(w)

    counter = Counter(words_list)
    total = sum(counter.values())#总词频数
    topk_words = counter.most_common()
    top_word = {k:float(v)/float(total) for k,v in topk_words}

    return top_word

def word_list(comment_word, news_word, top_percent=WORD_LIST_TOP_PERCENT):
    '''
    统计在评论和新闻中出现频率都高的词
    输入数据:
        comment_word:评论中的词及词频，字典格式
        news_word:新闻中的词及词频，字典格式
    输出数据:
        评论和新闻中出现频率排在前20%的词，[(词，词频)]
    '''
    word_all = {}
    for k,v in comment_word.iteritems():
        if news_word.has_key(k):
            word_all[k] = comment_word[k]+news_word[k]
        else:
            word_all[k] = comment_word[k]

    for k,v in news_word.iteritems():
        if word_all.has_key(k)==False:
            word_all[k] = news_word[k]

    sorted_word = sorted(word_all.iteritems(),key=lambda(k,v):v,reverse=True)
    result_word = [(k,v)for k,v in sorted_word]

    return result_word[:int(len(result_word)*top_percent)]

def comment_word_in_news(word_comment, word_news, inputs):
    '''
    判断一条评论中的名词是否在新闻中出现过
    输入数据：
        word_comment:每条评论的名词，{"过滤后评论的下标":[名词1，名词2，...]}
        word_news:相应新闻的词及词频列表，[(词，词频)]
        inputs:过滤后的评论文本的集合,[{'_id':评论id,'news_id':新闻id,'content':新闻内容}]
    输出数据：
        list: rub_label, 每条评论中的名词是否在新闻中出现过，0表示出现过, 1表示没有出现
    '''
    results = []
    news_word = [item[0] for item in word_news]
    for k, v in word_comment.iteritems():
        count = 0#每条评论中包含的新闻词数
        for w in v:
            if w in news_word:
                count += 1

        if count >= 2:
             comment_news_label = 0
        else:
             comment_news_label = 1

        item = inputs[k]
        item['rub_label'] = comment_news_label

        results.append(item)

    return results


def filter_comment(inputs):
    """
    针对一条新闻下的一组评论进行过滤
    过滤评论函数：将评论中@及后面用户名、表情符号去掉，只保留名词、动词、形容词次数大于3的评论;如果评论中的名词在高频（新闻+评论）词中出现过则保留该条评论，否则删除掉
    输入数据:
        inputs:评论数据，示例：[{'_id':评论id,'news_id':新闻id,'content':评论内容}]
        news:新闻数据，"新闻"
    输出数据:
        过滤后的评论数据
    """
    for r in inputs:
        news_content = r['news_content']

    item_reserved = []
    item_rubbish = []

    at_pattern = r'@(.+?)\s'
    emotion_pattern = r'\[(\S+?)\]'

    for input in inputs:
        rub_label = 0 # 表示不是垃圾
        text = re.sub(at_pattern, '',input['content']+' ')#在每个input后加一个空格，以去掉@在末尾的情况
        text = text.strip(' ')
        text = re.sub(emotion_pattern,'',text)
        words = cut_words(text)
        if len(words) >= 3 and len(words)<=20:
            for word in words:
                if word in market_words:
                    rub_label = 1 # 表示命中广告词，是垃圾
                    input['rub_label'] = rub_label
                    item_rubbish.append(input)
                    break

            if rub_label == 0:
                input['content'] = text
                item_reserved.append(input)
        else:
            rub_label = 1
            input['rub_label'] = rub_label
            item_rubbish.append(input)

    # 如果评论中的名词出现在过新闻中，则保留该评论
    comment_top, comment_noun = freq_word_comment(item_reserved) # 评论中的词及词频
    news_word = freq_word_news(news_content) # 新闻中的词及词频
    imp_word = word_list(comment_top,news_word) # 评论和新闻中的词及词频结合
    results = comment_word_in_news(comment_noun, imp_word, item_reserved)

    return results + item_rubbish


def comment_news(inputs):
    '''
    将新闻评论按新闻id归类
    输入数据：评论数组组成的列表，示例：[{"_id":评论编号，"news_id":新闻编号，"content":评论内容}]
    输出数据：按新闻id归类的新闻评论，示例：{新闻编号：[{"_id":评论编号，"news_id":新闻编号，"content":评论内容}]}
    '''
    results = dict()

    for input in inputs:
        news_id = input["news_id"]

        try:
            results[news_id].append(input)
        except KeyError:
            results[news_id] = [input]

    return results


def freq_word(items):
    '''
    统计一条文本的词频
    输入数据：
        items: 新闻组成的列表:字典, 数据示例：{'_id':评论id,'news_id':新闻id,'content':新闻内容}
    输出数据：
        top_word: 词和词频构成的字典, 数据示例：{词：词频，词：词频，...}
    '''
    words_list = []
    text = items['content']
    words = cut_words_noun(text)
    for w in words:
        words_list.append(w)

    counter = Counter(words_list)
    total = sum(counter.values())#总词频数
    topk_words = counter.most_common()
    top_word = {k:(float(v)/float(total)) for k,v in topk_words}

    return top_word

def tfidf_v2(inputs):
    '''
    计算每条文本中每个词的tfidf，对每个词在各个文本中tfidf加和除以出现的文本次数作为该词的权值。
    输入数据：
        评论数据，示例：[{'_id':评论id,'news_id':新闻id,'content':评论内容}]
    输出数据：
        result_tfidf[:topk]:前20%tfidf词及tfidf值的列表,示例：[(词,tfidf)]
        input_word_dict:每一条记录的词及tfidf,示例：{"_id":{词：tfidf,词：tfidf,...}}
    '''
    total_document_count = len(inputs)
    tfidf_dict = {}#词在各个文本中的tfidf之和
    count_dict = {}#词出现的文本数
    count = 0#记录每类下词频总数
    input_word_dict = {}#每条记录每个词的tfidf,{"_id":{词：tfidf，词：tfidf}}
    for input in inputs:
        word_count = freq_word(input)
        count += sum(word_count.values())
        word_tfidf_row = {}#每一行中词的tfidf
        for k,v in word_count.iteritems():
            tf = v
            document_count = sum([1 for input_item in inputs if k in input_item['content']])
            idf = math.log(float(total_document_count)/(float(document_count+1)))
            tfidf = tf*idf
            word_tfidf_row[k] = tfidf
            try:
                tfidf_dict[k] += tfidf
            except KeyError:
                tfidf_dict[k] = 1
        input_word_dict[input["id"]] = word_tfidf_row

    for k,v in tfidf_dict.iteritems():
        tfidf_dict[k] =  float(tfidf_dict[k])/float(len(inputs))

    sorted_tfidf = sorted(tfidf_dict.iteritems(), key = lambda asd:asd[1],reverse = True)
    result_tfidf = [(k,v)for k,v in sorted_tfidf]

    topk = int(math.ceil(float(len(result_tfidf))*0.2))#取前20%的tfidf词
    return result_tfidf[:topk],input_word_dict


def word_bag(word, inputs, gram):
    '''
    取出一个词前三个词和后三个词，包括动词、名词、形容词
    输入数据：
    word:选取出的特征词
    inputs:过滤后的评论文本
    gram:取特征词前面gram个词和后面gram个词
    输出数据：
    counter_dict:{特征词：counter(在每个维度上特征值)}
    '''
    #一个词与前后三个词构成词袋
    words_bag = []
    counter_dict = {}
    for w in word:
        for input in inputs:
            if w[0] in input['content']:
                text = input['content']
                words = cut_words(text)
                if w[0] in words:
                    index = words.index(w[0])
                    if index-gram<0:
                        bag = words[:index]
                    else:
                        bag = words[index-gram:index]
                    bag.extend(words[index:index+gram])
                    words_bag.extend(bag)
            counter = Counter(words_bag)
            top_words = counter.most_common()
            counter_dict[w] = {k:v for k,v in top_words}

    #特征词列表
    feature_list = list(set(words_bag))

    return counter_dict,feature_list


def process_for_cluto(word, inputs, version=PROCESS_FOR_CLUTO_VERSION, gram=PROCESS_GRAM):
    '''
    处理成cluto的输入格式，词-文本聚类
    输入数据：
        word:特征词,[(词，tfidf)]
        input_dict:每条文本中包含的词及tfidf,{"_id":{词:tfidf,词：tfidf}}
        inputs:过滤后的评论数据
    输出数据：
        cluto输入文件的位置
    '''
    if version == 'v1':
        #生成cluto输入文件
        row = len(word)#词数
        column = len(inputs)#特征列数
        nonzero_count = 0#非0特征数

        cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)
        if not os.path.exists(cluto_input_folder):
            os.makedirs(cluto_input_folder)
        file_name = os.path.join(cluto_input_folder, '%s.txt' % os.getpid())

        with open(file_name, 'w') as fw:
            lines = []    
            #词频聚类
            for w in word:
                row_record = []#记录每行特征
                for i in range(len(inputs)):
                    n = str(inputs[i]['content']).count(str(w[0]))
                    if n!= 0:
                        nonzero_count += 1
                        row_record.append('%s %s'%(str(i+1),n))
                line = ' '.join(row_record) + '\r\n'
                lines.append(line)
            fw.write('%s %s %s\r\n'%(row, column, nonzero_count))
            fw.writelines(lines)

    elif version == 'v2':
        words_feature, feature_list = word_bag(word,inputs,gram)
        #生成cluto输入文件
        row = len(word)#词数
        column = len(feature_list)#特征列数
        nonzero_count = 0#非0特征数

        cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)
        if not os.path.exists(cluto_input_folder):
            os.makedirs(cluto_input_folder)
        file_name = os.path.join(cluto_input_folder, '%s.txt' % os.getpid())

        with open(file_name, 'w') as fw:
            lines = []    
            #词频聚类
            for k,v in words_feature.iteritems():
                row_record = []
                feature_line = v
                for f in feature_list:
                    if f in feature_line:
                        nonzero_count += 1
                        row_record.append('%s %s'%(int(feature_list.index(f))+1,feature_line[f]))
                line = ' '.join(row_record)+'\r\n'
                lines.append(line)
            fw.write('%s %s %s\r\n'%(row, column, nonzero_count))
            fw.writelines(lines)
    print file_name
    return file_name

def cluto_kmeans_vcluster(k=CLUSTERING_KMEANS_CLUSTERING_NUM, input_file=None, vcluster=None):
    '''
    cluto kmeans聚类
    输入数据：
        k: 聚簇数
        input_file: cluto输入文件路径，如果不指定，以cluto_input_folder + pid.txt方式命名
        vcluster: cluto vcluster可执行文件路径

    输出数据：
        cluto聚类结果, list
        聚类结果评价文件位置及名称
    '''
    # 聚类结果文件, result_file

    cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)

    if not input_file:
        input_file = os.path.join(cluto_input_folder, '%s.txt' % os.getpid())
        result_file = os.path.join(cluto_input_folder, '%s.txt.clustering.%s' % (os.getpid(), k))
        evaluation_file = os.path.join(cluto_input_folder,'%s_%s.txt'%(os.getpid(),k))
    else:
        result_file = os.path.join(cluto_input_folder,'%s.clustering.%s' % (input_file, k))
        evaluation_file = os.path.join(cluto_input_folder,'%s_%s.txt'%(os.getpid(),k))

    if not vcluster:
        vcluster = os.path.join(AB_PATH, CLUSTERING_CLUTO_EXECUTE_PATH)

    command = "%s -niter=20 %s %s > %s" % (vcluster, input_file, k, evaluation_file)
    os.popen(command)

    # 提取聚类结果
    print result_file
    results = [line.strip() for line in open(result_file)]

    #提取每类聚类效果
    with open(evaluation_file) as f:
        s = f.read()
        pattern = re.compile(r'\[I2=(\S+?)\]')
        res = pattern.search(s).groups()
        evaluation_results = res[0]

    if os.path.isfile(result_file):
        os.remove(result_file)

    if os.path.isfile(input_file):
        os.remove(input_file)

    if os.path.isfile(evaluation_file):
        os.remove(evaluation_file)

    return results, evaluation_results

def label2uniqueid(labels):
    '''
        为聚类结果不为其他类的生成唯一的类标号
        input：
            labels: 一批类标号，可重复
        output：
            label2id: 各类标号到全局唯一ID的映射
    '''
    label2id = dict()
    for label in set(labels):
        label2id[label] = str(uuid.uuid4())

    return label2id

def kmeans(word, inputs, k=CLUSTERING_KMEANS_CLUSTERING_NUM, \
        version=PROCESS_FOR_CLUTO_VERSION, gram=PROCESS_GRAM):
    '''
    kmeans聚类函数
    输入数据：
        word:前20%tfidf词及tfidf值的列表,示例：[(词,tfidf)]
        input_dict:每条文本中包含的词及tfidf,{"_id":{词:tfidf,词：tfidf}}
        inputs:[{'_id':评论id,'news_id':新闻id,'content':评论内容}]
        k:聚类个数
    输出数据：
        每类词构成的字典，{类标签：[词1，词2，...]}
        聚类效果评价文件路径
    '''
    if len(inputs) < 2:
        raise ValueError("length of input items must be larger than 2")

    input_file = process_for_cluto(word, inputs, version=version, gram=gram)
    labels, evaluation_results = cluto_kmeans_vcluster(k=k, input_file=input_file)
    label2id = label2uniqueid(labels)

    #将词对归类，{类标签：[词1，词2，...]}
    word_label = {}
    for i in range(len(word)):
        l = labels[i]
        if int(l) != -1:
            l = label2id[l]
        else:
            l = 'other'

        if word_label.has_key(l):
            item = word_label[l]
            item.append(word[i][0])
        else:
            item = []
            item.append(word[i][0])
            word_label[l] = item

    return word_label, evaluation_results


def choose_cluster(tfidf_word, inputs, cluster_min=MIN_CLUSTER_NUM, \
        cluster_max=MAX_CLUSTER_NUM, cluster_num=COMMENT_WORDS_CLUSTER_NUM, \
        version=PROCESS_FOR_CLUTO_VERSION):
    '''
    选取聚类个数cluster_min(2)~cluster_max(5)个中聚类效果最好的保留
    输入数据：
        tfidf_word:tfidf topk词及权值，[(词，权值)]
        inputs:过滤后的评论
        cluster_min:尝试的最小聚类个数
        cluster_max:尝试的最大聚类个数
    输出数据：
        聚类效果最好的聚类个数下的词聚类结果
    '''
    if cluster_num == -1:
        # 自动聚类
        evaluation_result = {} # 每类的聚类评价效果
        cluster_result = {} # 记录每个聚类个数下，kmeans词聚类结果，{聚类个数：{类标签：[词1，词2，...]}}
        for i in range(cluster_min, cluster_max, 1):
            results, evaluation = kmeans(tfidf_word, inputs, k=i, version=version)
            cluster_result[i] = results
            evaluation_result[i] = evaluation

        sorted_evaluation = sorted(evaluation_result.iteritems(), key=lambda(k,v):k, reverse=False)

        #计算各个点的斜率
        slope = {}#每点斜率
        slope_average = 0 # 斜率的平均值
        for i in range(1, len(sorted_evaluation)):
            slope[i]=(float(sorted_evaluation[i][1])-float(sorted_evaluation[i-1][1]))/float(sorted_evaluation[i][1])
            slope_average += slope[i]
        slope_average = slope_average/float(len(sorted_evaluation)-1)

        #计算各个点与斜率均值的差值，找到差值最小点
        slope_difference = {}#斜率与均值的差值
        for k,v in slope.iteritems():
            slope_difference[k] = abs(float(slope[k])-slope_average)
        sorted_slope_difference = sorted(slope_difference.iteritems(),key=lambda(k,v):v, reverse=False)

        results = cluster_result[sorted_slope_difference[0][0]]
    else:
        results, evaluation = kmeans(tfidf_word, inputs, k=cluster_num, version=version)

    return results


def text_classify(inputs, word_label, tfidf_word):
    '''
    对每条评论分别计算属于每个类的权重，将其归入权重最大的类
    输入数据：
        inputs:评论字典的列表，[{'_id':评论id,'news_id':新闻id,'content':评论内容}]
        word_cluster:词聚类结果,{'类标签'：[词1，词2，...]}
        tfidf_word:tfidf topk词及权值，[(词，权值)]

    输出数据：
        每条文本的归类，字典，{'_id':[类，属于该类的权重]}
    '''
    #将词及权值整理为字典格式
    word_weight = {}
    for idx,w in enumerate(tfidf_word):
        word_weight[w[0]] = w[1]

    #计算每条评论属于各个类的权值
    for input in inputs:
        text_weight = {}
        text = input['content']
        text_word = cut_words_noun(text)#每句话分词结果，用于text_weight中

        for l,w_list in word_label.iteritems():
            weight = 0
            for w in w_list:
                weight += text.count(w)*word_weight[w]
            text_weight[l] = float(weight)/(float(len(text_word)) + 1.0)
        sorted_weight = sorted(text_weight.iteritems(), key = lambda asd:asd[1], reverse = True)
        if sorted_weight[0][1]!=0:#只有一条文本属于任何一个类的权值都不为0时才归类
            clusterid, weight = sorted_weight[0]
        else:
            clusterid = 'other'
            weight = 0

        input['label'] = clusterid
        input['weight'] = weight

    return inputs

def cluster_evaluation(items, min_size=COMMENT_CLUSTERING_CLUSTER_EVA_MIN_SIZE):
    '''
    只保留文本数大于num的类
    输入数据:
        items: 新闻数据, 字典的序列, 输入数据示例：[{'news_id': 新闻编号, 'content': 评论内容, 'label': 类别标签}]
        num:类文本最小值
    输出数据:
        各簇的文本, dict
    '''
    # 将文本按照其类标签进行归类
    items_dict = {}
    for item in items:
        try:
            items_dict[item['label']].append(item)
        except:
            items_dict[item['label']] = [item]

    other_items = []
    for label in items_dict.keys():
        items = items_dict[label]
        if len(items) < min_size:
            for item in items:
                item['label'] = 'other'
                other_items.append(item)

            items_dict.pop(label)

    try:
        items_dict['other'].extend(other_items)
    except KeyError:
        items_dict['other'] = other_items

    return items_dict

def global_weight_cal_tfidf(tfidf_word, item):
    """根据tfidf词计算全局文本权重
    """
    #将词及权值整理为字典格式
    word_weight = {}
    for idx, w in enumerate(tfidf_word):
        word_weight[w[0]] = w[1]

    text = item["title"] + item["content"]
    text_word = cut_words_noun(text)#每句话分词结果，用于text_weight中

    weight = 0
    for w, c in tfidf_word:
        weight += text.count(w) * word_weight[w]
    text_weight = float(weight)/(float(len(text_word)) + 1.0)

    return text_weight

