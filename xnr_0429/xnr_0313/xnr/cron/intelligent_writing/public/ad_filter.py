# -*- coding: utf-8 -*-

import os
import re
import sys
sys.path.append('/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/intelligent_writing/public/')

from utils_public import cut_words
from load_settings import load_settings

# 加载配置参数
settings = load_settings()
MARKET_WORDS = settings.get('MARKET_WORDS')
EXTRA_MARKET_LIST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), MARKET_WORDS)

def load_market_words():
    one_words = set([line.strip('\r\n') for line in file(EXTRA_MARKET_LIST_PATH)])
    return one_words

market_words = load_market_words()

def remove_at(text):
    """text去除@
       text: utf-8
    """
    at_pattern = r'@(.+?)\s'
    text = text + ' ' # 在每个input后加一个空格，以去掉@在末尾的情况
    text = re.sub(at_pattern, '', text)
    text = text.strip()

    return text


def remove_emoticon(text):
    """text去除emoticon
       text: utf-8
    """
    emotion_pattern = r'\[(\S+?)\]'
    text = re.sub(emotion_pattern, '', text)

    return text


def ad_filter(item, market_words=market_words):
    """
        按照简单规则过滤评论函数：将评论中@及后面用户名、表情符号去掉，只保留名词、动词、形容词词数大于3的评论
        input:
            item:评论数据，示例：{'_id':评论id,'content':评论内容}
        output:
            过滤后的评论数据, 增加了ad_label，0表示非垃圾; 增加了text_filter_ad，表示去除无用东西的文本
    """
    text = item['content']
    text = remove_at(text)
    text = remove_emoticon(text)
    words = cut_words(text)

    ad_label = 0 # 默认每条记录都不是垃圾
    if len(words) >= 3 and len(words)<=20:
        if len(set(words) & set(market_words)):
            ad_label = 1
    else:
        ad_label = 1

    item['ad_label'] = ad_label
    item['text_filter_ad'] = text

    return item

