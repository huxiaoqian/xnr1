#-*-coding=utf-8-*-

from neutral_classifier import triple_classifier
from rubbish_classifier import rubbish_classifier
from weibo_subob_classifier import subob_classifier, cut_mid_weibo
from load_settings import load_settings

settings = load_settings()
RUBBISH_BATCH_COUNT = settings.get("RUBBISH_BATCH_COUNT")

def weibo_subob_rub_neu_classifier(items, batch=RUBBISH_BATCH_COUNT):
    '''
    分类主函数:
    输入数据:weibo(list元素)，示例：[[mid,text,...],[mid,text,...]...]
            batch: rubbish filter的参数
    输出数据:label_data(字典元素)，示例：{{'mid':类别标签},{'mid':类别标签}...}
            1表示垃圾文本，0表示新闻文本，[2表示中性文本, 已去除]，-1表示有极性的文本
    '''
    results = []
    items = rubbish_classifier(items, batch=batch)

    for item in items:
        label = 1
        if item['rub_label'] == 1:
            label = 1 # 垃圾

        else:
            item = subob_classifier(item)
            if item['subob_label'] == 1:
                label = 0 # 客观
            else:
                sentiment = triple_classifier(item)
                if sentiment == 0:
                    # label = 2 # 中性
                    label = cut_mid_weibo(item['content168'])
                else:
                    label = -1 # 有极性

        item['subob_rub_neu_label'] = label
        results.append(item)

    return results

