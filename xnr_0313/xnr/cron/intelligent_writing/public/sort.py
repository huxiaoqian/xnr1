#-*-coding=utf-8-*-
# User: linhaobuaa
# Date: 2014-12-22 10:00:00
# Version: 0.1.0

def text_weight_cal(item, feature_words):
    """根据类的特征词计算单条文本的权重
       input:
           item: 单条信息, {"title": "标题", "content": "内容"}, utf-8编码
           feature_words: 某一类的特征词, 字典
       output:
           单条文本的权重
    """
    text = item["title"] + item["content"]
    return sum([text.count(word) for word, count in feature_words.iteritems()])

