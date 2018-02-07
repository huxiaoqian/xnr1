# -*- coding: utf-8 -*-
# User: linhaobuaa
# Date: 2015-01-04 16:00:00
# Version: 0.4.0


import os
import time
import math
import uuid
from gensim import corpora
from utils import cut_words
from collections import Counter
from load_settings import load_settings

settings = load_settings()
CLUTO_FOLDER = settings.get('CLUSTERING_CLUTO_FOLDER')
KMEANS_CLUSTERING_NUM = settings.get('CLUSTERING_KMEANS_CLUSTERING_NUM')
CLUTO_EXECUTE_PATH = settings.get('CLUSTERING_CLUTO_EXECUTE_PATH')
TOPK_FREQ_WORD_NUM = settings.get('CLUSTERING_TOPK_FREQ_WORD')
CLUSTER_EVA_TOP_NUM = settings.get('CLUSTERING_CLUSTER_EVA_TOP_NUM')
CLUSTER_EVA_LEAST_FREQ = settings.get('CLUSTERING_CLUSTER_EVA_LEAST_FREQ')
CLUSTER_EVA_LEAST_SIZE = settings.get('CLUSTERING_CLUSTER_EVA_LEAST_SIZE')
AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')


def process_for_cluto(inputs, cluto_input_folder=None):
    """
    数据预处理函数
    input：
        inputs: 新闻数据, 示例：[{'_id':新闻id,'source_from_name':新闻来源,'title':新闻标题,'content':新闻内容,'timestamp':时间戳}]
    output:
        cluto输入文件路径
    """
    # handle default
    if not cluto_input_folder:
        cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)

    feature_set = set() # 不重复的词集合
    words_list = [] # 所有新闻分词结果集合
    for input in inputs:
        text = input['title'] + input['content']
        words = cut_words(text)
        words_list.append(words)

    # 特征词字典
    dictionary = corpora.Dictionary(words_list)

    # 将feature中的词转换成列表
    feature_set = set(dictionary.keys())

    row_count = len(inputs) # documents count
    column_count = len(feature_set) # feature count
    nonzero_count = 0 # nonzero elements count

    # 文件名以PID命名
    if not os.path.exists(cluto_input_folder):
        os.makedirs(cluto_input_folder)
    file_name = os.path.join(cluto_input_folder, '%s.txt' % os.getpid())

    with open(file_name, 'w') as fw:
        lines = []

        for words in words_list:
            bow = dictionary.doc2bow(words)
            nonzero_count += len(bow)
            line = ' '.join(['%s %s' % (w + 1, c) for w, c in bow]) + '\n'
            lines.append(line)

        fw.write('%s %s %s\n' % (row_count, column_count, nonzero_count))
        fw.writelines(lines)

    return file_name


def cluto_kmeans_vcluster(k=KMEANS_CLUSTERING_NUM, input_file=None, vcluster=None):
    '''
    cluto kmeans聚类
    input：
        k: 聚簇数，默认取10
        input_file: cluto输入文件路径，如果不指定，以cluto_input_folder + pid.txt方式命名
        vcluster: cluto vcluster可执行文件路径
    output：
        cluto聚类结果, list
    '''
    # handle default
    # 聚类结果文件, result_file
    if not input_file:
        cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)
        input_file = os.path.join(cluto_input_folder, '%s.txt' % os.getpid())
        result_file = os.path.join(cluto_input_folder, '%s.txt.clustering.%s' % (os.getpid(), k))
    else:
        result_file = '%s.clustering.%s' % (input_file, k)

    if not vcluster:
        vcluster = os.path.join(AB_PATH, CLUTO_EXECUTE_PATH)

    command = "%s -niter=20 %s %s" % (vcluster, input_file, k)
    os.popen(command)

    results = [line.strip() for line in open(result_file)]

    if os.path.isfile(result_file):
        os.remove(result_file)

    if os.path.isfile(input_file):
        os.remove(input_file)

    return results


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


def kmeans(items, k=KMEANS_CLUSTERING_NUM):
    """kmeans聚类
       input:
           cluto要求至少输入两条文本
           items: [{"title": "新闻标题", "content": "新闻内容"}], 以utf-8编码
       output:
           items: [{"title": "新闻标题", "content": "新闻内容", "label": "簇标签"}]
    """
    if len(items) < 2:
        raise ValueError("length of input items must be larger than 2")

    input_file = process_for_cluto(items)
    labels = cluto_kmeans_vcluster(k=k, input_file=input_file) # cluto聚类，生成文件，每行为一条记录的簇标签
    label2id = label2uniqueid(labels)

    for idx, item in enumerate(items):
        label = labels[idx]
        if int(label) != -1:
            item['label'] = label2id[label]
        else:
            # 将-1类归为其它
            item['label'] = 'other'

    return items

def freq_word(items, topk=TOPK_FREQ_WORD_NUM):
    '''
    统计一批文本的topk高频词
    input：
        items:
            新闻组成的列表:字典的序列, 数据示例：[{'_id':新闻id,'source_from_name':新闻来源,'title':新闻标题,'content':新闻内容,'timestamp':时间戳,'lable':类别标签},...]
        topk:
            按照词频的前多少个词, 默认取20
    output：
        topk_words: 词、词频组成的列表, 数据示例：[(词，词频)，(词，词频)...]
    '''
    words_list = []
    for item in items:
        text = item['title'] + item['content']
        words = cut_words(text)
        words_list.extend(words)

    counter = Counter(words_list)
    total_weight = sum(dict(counter.most_common()).values())
    topk_words = counter.most_common(topk)
    keywords_dict = {k: v for k, v in topk_words}

    return keywords_dict, total_weight


def cluster_tfidf(keywords_count_list, total_weight_list, least_freq=CLUSTER_EVA_LEAST_FREQ):
    '''计算tfidf
       input
           keywords_count_list: 不同簇的关键词, 词及词频字典的list
           least_freq: 计算tf-idf时，词在类中出现次数超过least_freq时，才被认为出现
       output
           不同簇的tfidf, list
    '''
    cluster_tf_idf = [] # 各类的tf-idf
    for idx, keywords_dict in enumerate(keywords_count_list):
        tf_idf_list = [] # 该类下词的tf-idf list
        total_freq = total_weight_list[idx] # 该类所有词的词频总和
        total_document_count = len(keywords_count_list) # 类别总数
        for keyword, count in keywords_dict.iteritems():
            tf = float(count) / float(total_freq) # 每个词的词频 / 该类所有词词频的总和
            document_count = sum([1 if keyword in kd.keys() and kd[keyword] > least_freq else 0 for kd in keywords_count_list])
            idf = math.log(float(total_document_count) / float(document_count + 1))
            tf_idf = tf * idf
            tf_idf_list.append(tf_idf)

        cluster_tf_idf.append(sum(tf_idf_list))

    return cluster_tf_idf


def cluster_evaluation(items, top_num=CLUSTER_EVA_TOP_NUM, topk_freq=TOPK_FREQ_WORD_NUM, least_freq=CLUSTER_EVA_LEAST_FREQ, min_tfidf=None, \
        least_size=CLUSTER_EVA_LEAST_SIZE):
    '''
    聚类评价，计算每一类的tf-idf: 计算每一类top词的tfidf，目前top词选取该类下前20个高频词，一个词在一个类中出现次数大于10算作在该类中出现
    input:
        items: 新闻数据, 字典的序列, 输入数据示例：[{'title': 新闻标题, 'content': 新闻内容, 'label': 类别标签}]
        top_num: 保留top_num的tfidf类
        topk_freq: 选取的高频词的前多少
        least_freq: 计算tf-idf时，词在类中出现次数超过least_freq时，才被认为出现
        min_tfidf: tfidf大于min_tfidf的类才保留
        least_size: 小于least_size的簇被归为其他簇
    output:
        各簇的文本, dict
    '''

    # 将文本按照其类标签进行归类
    items_dict = {}
    for item in items:
        try:
            items_dict[item['label']].append(item)
        except:
            items_dict[item['label']] = [item]

    # 对每类文本提取topk_freq高频词
    labels_list = []
    keywords_count_list = []
    total_weight_list = []
    for label, one_items in items_dict.iteritems():
        if label != 'other':
            labels_list.append(label)
            keywords_count, weight = freq_word(one_items, topk=topk_freq)
            total_weight_list.append(weight)
            keywords_count_list.append(keywords_count)

    # 计算每类的tfidf
    tfidf_list = cluster_tfidf(keywords_count_list, total_weight_list, least_freq=least_freq)
    tfidf_dict = dict(zip(labels_list, tfidf_list))
    keywords_dict = dict(zip(labels_list, keywords_count_list))

    def choose_by_tfidf():
        """ 根据tfidf对簇进行选择, 保留前5类, 并与min_tfidf作比，保留不小与min_tfidf的簇
            input:
                top_num: 保留top_num的tfidf类
            output:
                更新后的items_dict
        """
        cluster_num = len(tfidf_list)

        sorted_tfidf = sorted(tfidf_dict.iteritems(), key=lambda(k, v): v, reverse=True)

        # 筛掉tfidf小于min_tfidf的类
        if min_tfidf:
            delete_labels = []
            candidate_tfidf = []
            for label, tfidf in sorted_tfidf:
                if tfidf < min_tfidf:
                    delete_labels.append(label)
                else:
                    candidate_tfidf.append((label, tfidf))
            delete_labels.extend([l[0] for l in candidate_tfidf[-(len(candidate_tfidf)-top_num):]])
        else:
            delete_labels = [l[0] for l in sorted_tfidf[-(len(sorted_tfidf)-top_num):]]

        other_items = []
        for label in items_dict.keys():
            if label != 'other':
                items = items_dict[label]
                if label in delete_labels:
                    for item in items:
                        item['label'] = 'other'
                        other_items.append(item)

                    items_dict.pop(label)

        try:
            items_dict['other'].extend(other_items)
        except KeyError:
            items_dict['other'] = other_items

    # 根据簇的tfidf评价选择
    choose_by_tfidf()

    def choose_by_size():
        """小于least_size的簇被归为其他簇
        """
        other_items = []
        for label in items_dict.keys():
            if label != 'other':
                items = items_dict[label]
                if len(items) < least_size:
                    for item in items:
                        item['label'] = 'other'
                        other_items.append(item)

                    items_dict.pop(label)

        try:
            items_dict['other'].extend(other_items)
        except KeyError:
            items_dict['other'] = other_items

    # 根据簇的大小进行评价选择
    choose_by_size()

    return items_dict, tfidf_dict

