1、文件结构

   public是为观点计算封装的代码库，各方法输入输出详情参考各方法定义部分，目录结构如下

   folder: public
       file: comment_module - 评论计算主模块
          func: comments_calculation
              输入为comments list
              输出为经过垃圾过滤、聚类、情绪计算的结果

          func: comments_calculation_v2 - 评论计算
              输入为comments_list
              subfunc: comments_rubbish_clustering_calculation - 垃圾过滤 + 聚类
              subfunc: comments_sentiment_rubbish_calculation - 垃圾过滤 + 情绪
              输出为经过垃圾过滤、聚类、情绪计算的结果

       file: settings.py - 参数配置文件

       file: default_settings.py - 默认参数配置文件

       file: utils - 基础工具模块
          func: ts2date ... - 时间转化方法
          func: _default_mongo - 初始化数据库对象
          func: cut_words - 分词, 加入黑名单过滤单个词，保留名词、动词、形容词
          func: cut_words_noun - 分词, 加入黑名单过滤单个词，保留名词

       file: Database - 数据库操作模块
          class: EventManager - 话题管理
          class: CommentsManager - 评论表管理
          class: EventComments - 话题评论管理
          class: News - 新闻管理
          class: Comment - 评论单条信息操作

       file: ad_filter - 简单规则垃圾过滤
          func: ad_filter - 按照简单规则过滤评论方法：market_words + 分词后词的长度

       file: classify_mid_weibo - 中性情感分类
          func: mid_sentiment_classify - 中性情感分类：情感词表 + 标点符号
              subfunc: label_adjust - 根据标点符号调整类别标签
              subfunc: label_classify - 根据情感词表对中性文本分类

       file: comment_clustering_tfidf_v7 - 最新版本的评论聚类方法
          func: tfidf_v2 - 计算每条文本中每个词的tfidf
          func: text_classify - 对每条评论分别计算属于每个类的权重
          func: cluster_evaluation - 聚类效果评价 
          func: choose_cluster - 选取聚类个数2~15个中聚类效果最好的保留

