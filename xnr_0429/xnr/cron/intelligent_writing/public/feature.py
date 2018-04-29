#-*-coding=utf-8-*-

import math
from utils import cut_words
from load_settings import load_settings

settings = load_settings()
TFIDF_TOPK = settings.get("FEATURE_TFIDF_TOPK")
TITLE_TERM_WEIGHT = settings.get("FEATURE_TITLE_TERM_WEIGHT")
CONTENT_TERM_WEIGHT = settings.get("FEATURE_CONTENT_TERM_WEIGHT")


def tfidf_cal(keywords_dict_list, topk=TFIDF_TOPK):
    '''计算tfidf
       input
           keywords_dict_list: 不同簇的关键词, list
       output
           不同簇的top tfidf词
    '''
    results = []
    for keywords_dict in keywords_dict_list:
        tf_idf_dict = dict()

        total_freq = sum(keywords_dict.values()) # 该类所有词的词频总和
        total_document_count = len(keywords_dict_list) # 类别总数
        for keyword, count in keywords_dict.iteritems():
            tf = float(count) / float(total_freq)
            document_count = sum([1 for kd in keywords_dict_list if keyword in kd.keys()])
            idf = math.log(float(total_document_count) / float(document_count + 1))
            tf_idf = tf * idf
            tf_idf_dict[keyword] = tf_idf

        tf_idf_results = sorted(tf_idf_dict.iteritems(), key=lambda(k, v): v, reverse=False)
        tf_idf_results = tf_idf_results[len(tf_idf_results)-topk:]
        tf_idf_results.reverse()
        tf_idf_results = {w: c for w, c in tf_idf_results}

        results.append(tf_idf_results)

    return results


def extract_feature(items, title_term_weight=TITLE_TERM_WEIGHT, content_term_weight=CONTENT_TERM_WEIGHT):
    '''
    提取特征词函数: Tf-idf, 名词/动词/形容词, TOP100, 标题与内容权重区分 5:1
    input：
        items: 新闻数据, 不考虑时间段, 字典的序列, 输入数据示例：[{'title': 新闻标题, 'content': 新闻内容, 'label': 类别标签}]
        title_term_weight: title中出现词的权重
        content_term_weight: content中出现词的权重
    output:
        每类特征词及权重, 数据格式：字典 {'类1': {'我们': 32, '他们': 43}}
    '''
    def extract_keyword(items):
        keywords_weight = dict()
        for item in items:
            title = item['title']
            content = item['content']

            title_terms = cut_words(title)
            content_terms = cut_words(content)

            for term in title_terms:
                try:
                    keywords_weight[term] += title_term_weight
                except KeyError:
                    keywords_weight[term] = title_term_weight

            for term in content_terms:
                try:
                    keywords_weight[term] += content_term_weight
                except KeyError:
                    keywords_weight[term] = content_term_weight

        # 筛掉频率大于或等于0.8, 频数小于或等于3的词
        keywords_count = dict()
        total_weight = sum(keywords_weight.values())
        for keyword, weight in keywords_weight.iteritems():
            ratio = float(weight) / float(total_weight)
            if ratio >= 0.8 or weight <= 3:
                continue

            keywords_count[keyword] = weight

        return keywords_count

    items_dict = {}
    for item in items:
        try:
            items_dict[item['label']].append(item)
        except:
            items_dict[item['label']] = [item]

    keywords_count_list = []
    for label, one_items in items_dict.iteritems():
        keywords_count = extract_keyword(one_items)
        keywords_count_list.append(keywords_count)

    results = tfidf_cal(keywords_count_list)

    return dict(zip(items_dict.keys(), results))

