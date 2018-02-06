#-*-coding=utf-8-*-

import copy
import uuid
import logging
from duplicate import duplicate
from ad_filter import ad_filter
from rubbish_classifier import rubbish_classifier
from weibo_subob_classifier import subob_classifier
from classify_mid_weibo import mid_sentiment_classify
from triple_sentiment_classifier import triple_classifier
from neutral_classifier import triple_classifier as neutral_classifier
from weibo_subob_rub_neu_classifier import weibo_subob_rub_neu_classifier
from comment_clustering_tfidf_v7 import tfidf_v2, text_classify, \
        cluster_evaluation, choose_cluster, comment_news, filter_comment, \
        global_weight_cal_tfidf
from load_settings import load_settings

settings = load_settings()
COMMENT_WORDS_CLUSTER_NUM = settings.get("COMMENT_WORDS_CLUSTER_NUM")
CLUSTER_EVA_MIN_SIZE = settings.get("CLUSTER_EVA_MIN_SIZE")
COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION = settings.get("COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION")
LOG_FILE = settings.get("LOG_FILE")


def comments_calculation_v2(comments, logfile=LOG_FILE, cluster_num=COMMENT_WORDS_CLUSTER_NUM, \
        cluster_eva_min_size=CLUSTER_EVA_MIN_SIZE, \
        version=COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION):
    """评论计算
       将sentiment和clustering的结果进行合并，取并集
       cluster_infos: 聚簇信息
       item_infos:  单条信息列表
                    情绪数据字段：sentiment、same_from、duplicate
                    聚类数据字段：clusterid、weight、same_from、duplicate
                    合并后：sentiment、same_from_sentiment、duplicate_sentiment、
                            clusterid、weight、same_from、duplicate
    """
    # setup logger
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    logger.info('-------------------------------')
    logger.info('start comments calculation v2')

    # backup copy
    comments_copy = copy.deepcopy(comments)

    # 情绪计算
    logger.info('start comments sentiment calculation')
    sentiment_results = comments_sentiment_rubbish_calculation(comments, logger)
    logger.info('end comments sentiment calculation')

    # 观点计算
    logger.info('start comments clustering calculation')
    clustering_results = comments_rubbish_clustering_calculation(comments_copy, logger, \
            cluster_num=cluster_num, \
            cluster_eva_min_size=cluster_eva_min_size, \
            version=version)
    logger.info('end comments clustering calculation')

    sentiment_dict = {r['id']: r for r in sentiment_results['item_infos']}
    clustering_dict = {r['id']: r for r in clustering_results['item_infos']}

    # 以clustering_dict为模板，将sentiment和clustering的item_infos合并，用并集
    merge_results = []
    for _id, r in clustering_dict.iteritems():
        if _id in sentiment_dict:
            cr = sentiment_dict[_id]

            added_info = {'sentiment': cr['sentiment'], 'same_from_sentiment': cr['same_from'], \
                    'duplicate_sentiment': cr['duplicate']}

            r.update(added_info)

        merge_results.append(r)

    logger.info('end comments calculation v2')

    return {'cluster_infos': clustering_results['cluster_infos'], 'item_infos': merge_results}


def comments_rubbish_clustering_calculation(comments, logger, cluster_num=COMMENT_WORDS_CLUSTER_NUM, \
        cluster_eva_min_size=CLUSTER_EVA_MIN_SIZE, \
        version=COMMENT_CLUSTERING_PROCESS_FOR_CLUTO_VERSION):
    """评论垃圾过滤、聚类
       input: comments
           comment中包含news_id, news_content
       cluster_infos: 聚簇信息
       item_infos:单条信息列表, 数据字段：clusterid、weight、same_from、duplicate
    """
    # 无意义信息的clusterid，包括ad_filter分出来的广告，svm分出的垃圾，主客观分类器分出的新闻
    NON_CLUSTER_ID = 'nonsense'

    # 其他类的clusterid
    OTHER_CLUSTER_ID = 'other'

    # 最小聚类输入信息条数，少于则不聚类
    MIN_CLUSTERING_INPUT = 30

    # 簇信息，主要是簇的特征词信息
    clusters_infos = {'features': dict()}

    # 去除sentiment label clusterid ad_label subob_label rub_label
    clear_keys = ['label', 'ad_label', 'subob_label', 'rub_label', 'weight']
    inputs = []
    for r in comments:
        for key in clear_keys:
            if key in r:
                del r[key]

        inputs.append(r)
    comments = inputs

    # 单条信息list，每条信息存储 clusterid weight sentiment字段
    items_infos = []

    # 数据字段预处理
    inputs = []
    for r in comments:
        r['title'] = ''
        r['content168'] = r['content168'].encode('utf-8')
        r['content'] = r['content168']
        r['text'] = r['content168']
        if 'news_content' in r and r['news_content']:
            r['news_content'] = r['news_content'].encode('utf-8')
        else:
            r['news_content'] = ''

        # 简单规则过滤广告
        item = ad_filter(r)
        if item['ad_label'] == 0:
            inputs.append(item)
        else:
            item['clusterid'] = NON_CLUSTER_ID + '_rub'
            items_infos.append(item)

    # svm去除垃圾
    items = rubbish_classifier(inputs)
    inputs = []
    for item in items:
        if item['rub_label'] == 1:
            item['clusterid'] = NON_CLUSTER_ID + '_rub'
            items_infos.append(item)
        else:
            inputs.append(item)

    # 按新闻对评论归类
    results = comment_news(inputs)

    final_inputs = []
    for news_id, _inputs in results.iteritems():
        # 结合新闻，过滤评论
        _inputs = filter_comment(_inputs)
        inputs = [r for r in _inputs if r['rub_label'] == 0]
        print 'inputs:',len(inputs)
        inputs_rubbish = [r for r in _inputs if r['rub_label'] == 1]
        for r in inputs_rubbish:
            r['clusterid'] =  NON_CLUSTER_ID + '_rub'
            items_infos.append(r)

        if len(inputs) >= MIN_CLUSTERING_INPUT:
            tfidf_word, input_dict = tfidf_v2(inputs)
            results = choose_cluster(tfidf_word, inputs, \
                    cluster_num=cluster_num, version=version)

            #评论文本聚类
            cluster_text = text_classify(inputs, results, tfidf_word)

            evaluation_inputs = []

            for k, v in enumerate(cluster_text):
                inputs[k]['label'] = v['label']
                inputs[k]['weight'] = v['weight']
                evaluation_inputs.append(inputs[k])

            #簇评价, 权重及簇标签
            recommend_text = cluster_evaluation(evaluation_inputs, min_size=cluster_eva_min_size)
            for label, items in recommend_text.iteritems():
                if label != OTHER_CLUSTER_ID:
                    clusters_infos['features'][label] = results[label]
                    print '11111',results[label]
                    for item in items:
                        item['clusterid'] = label
                        item['weight'] = item['weight']

                    final_inputs.extend(items)
                else:
                    for item in items:
                        item['clusterid'] = OTHER_CLUSTER_ID
                    items_infos.extend(items)
        else:
            # 如果信息条数小于,则直接展示信息列表
            tfidf_word, input_dict = tfidf_v2(inputs)
            uuid_label = str(uuid.uuid4())
            clusters_infos['features'][uuid_label] = [kw for kw, count in tfidf_word]
            print '22222222',clusters_infos['features'][uuid_label]
            for r in inputs:
                r['clusterid'] = uuid_label
                r['weight'] = global_weight_cal_tfidf(tfidf_word, r)

            final_inputs.extend(inputs)

    # 去重，根据子观点类别去重
    cluster_items = dict()
    for r in final_inputs:
        clusterid = r['clusterid']
        try:
            cluster_items[clusterid].append(r)
        except KeyError:
            cluster_items[clusterid] = [r]

    for clusterid, items in cluster_items.iteritems():
        results = duplicate(items)
        items_infos.extend(results)

    return {'cluster_infos': clusters_infos, 'item_infos': items_infos}


def comments_sentiment_rubbish_calculation(comments, logger):
    """输入为一堆comments, 字段包括title、content168
       输出：
           item_infos:单条信息列表, 数据字段：sentiment、same_from、duplicate
    """
    # 无意义信息的clusterid，包括ad_filter分出来的广告，svm分出的垃圾，主客观分类器分出的新闻
    NON_CLUSTER_ID = 'nonsense'

    # 有意义的信息clusterid
    MEAN_CLUSTER_ID = 'sentiment'

    # 单条信息list，每条信息存储 clusterid weight sentiment字段
    items_infos = []

    # 去除sentiment label clusterid ad_label subob_label rub_label
    clear_keys = ['sentiment', 'label', 'clusterid', 'ad_label', 'subob_label', 'rub_label', 'weight']
    inputs = []
    for r in comments:
        for key in clear_keys:
            if key in r:
                del r[key]

        inputs.append(r)
    comments = inputs

    # 数据字段预处理
    inputs = []
    for r in comments:
        r['title'] = ''
        r['content168'] = r['content168'].encode('utf-8')
        r['content'] = r['content168']
        r['text'] = r['content168']

        inputs.append(r)

    # 先分中性及3类分类器
    svm_inputs = []
    for r in inputs:
        sentiment = neutral_classifier(r)

        if sentiment != 0:
            sentiment = triple_classifier(r)
            if sentiment == 0:
                svm_inputs.append(r)
            else:
                r['sentiment'] = sentiment
                items_infos.append(r)
        else:
            svm_inputs.append(r)

    # 情绪调整
    senti_modify_inputs = []
    for r in svm_inputs:
        sentiment = mid_sentiment_classify(r['text'])
        if sentiment == -1:
            sentiment = 0 # 中性

        if sentiment != 0:
            r['sentiment'] = sentiment
            items_infos.append(r)
        else:
            r['sentiment'] = sentiment
            senti_modify_inputs.append(r)

    # 新闻分类
    inputs = []
    for r in senti_modify_inputs:
        r = subob_classifier(r)
        if r['subob_label'] == 1:
            # 主客观文本分类
            r['sentiment'] = NON_CLUSTER_ID + '_news' # 新闻
            items_infos.append(r)
        else:
            inputs.append(r)

    # 去垃圾
    items = rubbish_classifier(inputs)
    for item in items:
        if item['rub_label'] == 1:
            # svm去垃圾
            item['sentiment'] = NON_CLUSTER_ID + '_rub'
        else:
            # 简单规则过滤广告
            item = ad_filter(item)
            if item['ad_label'] == 1:
                item['sentiment'] = NON_CLUSTER_ID + '_rub'

        items_infos.append(item)

    # 去重，在一个情绪类别下将文本去重
    sentiment_dict = dict()
    for item in items_infos:
        if 'sentiment' in item:
            sentiment = item['sentiment']
            try:
                sentiment_dict[sentiment].append(item)
            except KeyError:
                sentiment_dict[sentiment] = [item]

    items_infos = []
    for sentiment, items in sentiment_dict.iteritems():
        items_list = duplicate(items)
        items_infos.extend(items_list)

    return {'item_infos': items_infos}

