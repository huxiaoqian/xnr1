#-*-coding=utf-8-*-

import re
#from xapian_case.utils import cut_filter
from global_utils_do import cut_filter

def remove_rub(text):
    """remove http、分享自
    """
    pattern_list = [r'\（分享自 .*\）', r'http://\w*']
    for i in pattern_list:
        p = re.compile(i)
        text = p.sub('', text)
    return text


def cut_mid_weibo(text):
    """在中性情感中根据规则再提取新闻微博
    """
    text = cut_filter(text) # 去掉文本中的网页链接和分享自
    n1 = text.find('发表')
    n2 = text.find('【')

    if '//' in text:
        return -1

    if n1 == 0:
        return 0

    if n2 == -1:
        return -1

    sub_str = text[0:n2]    
    if '#' in sub_str and '//' not in sub_str and '@' not in sub_str:
        return 0

    return -1


def subob_classifier(item):
    """主客观文本分类, 区分新闻微博和评论微博的主函数, 根据规则将新闻和评论分开,返回标签
    输入数据：data(list元素)，示例：[{'text',...},{'text',...}...], text以utf-8编码
    输出数据:label_data(list元素)，示例：[类别标签1,类别标签2...]
            1表示新闻，0表示非新闻
    """
    text = item['content168']

    if '【' not in text and '】' not in text: # 评论
        label = 0

    elif '【评】' in text:
        label = 0

    elif text.find('【') == 0:
        n = text.find('】')
        comment = remove_rub(text[n: len(text)])
        if len(comment):
            label = 1 # 客观
        else:
            label = 0

    else:
        label = 0

    item['subob_label'] = label

    return item

