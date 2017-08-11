# coding=utf-8
import sys
import re
import os.path
from bs4 import BeautifulSoup, Comment

reload(sys)
sys.setdefaultencoding('utf-8')

p1 = re.compile("\\s+").pattern

p2 = re.compile("(&nbsp;)+").pattern

# xA0
p3 = re.compile("[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\\xA0]").pattern

p4 = re.compile("<!DOCTYPE\\s+.*?>", re.S).pattern

p5 = re.compile("<!--.*?-->", re.S).pattern

p6 = re.compile("<script\\s*>.*?<\\/script\\s*>", re.I | re.S).pattern

p7 = re.compile("<script\\s+.*?<\\/script\\s*>", re.I | re.S).pattern

p8 = re.compile("<style\\s*>.*?<\\/style\\s*>", re.I | re.S).pattern

p9 = re.compile("<style\\s+.*?<\\/style\\s*>", re.I | re.S).pattern

p10 = re.compile("</[a-zA-Z]+\\s*>", re.I | re.S).pattern

p11 = re.compile("<[a-zA-Z]+[/]?>", re.I | re.S).pattern

# "<[a-zA-Z]+\\s+([^>]*?('.*?'|\\\".*?\\\")[^>]*?)*?[/]?>",
p12 = re.compile("<\\[a-zA-Z]+(\\s*\\[a-zA-Z]+\\s*([=]\\s*('.*?'|\\\".*?\\\"|\\[a-zA-Z]+))?)*?[/]?>",
                 re.I | re.S).pattern

p13 = re.compile("<.*?>", re.I | re.S).pattern

# 保留img的特殊处理...
p_img = re.compile("<img", re.I).pattern

p_img_1 = re.compile("\\[img_begin\\]").pattern

p_img_2 = re.compile("\\[img_end\\]").pattern

# 保留strong的特殊处理, 不再保留
# p_strong_1 = re.compile("<strong>", re.I).pattern

# p_strong_2 = re.compile("</strong>", re.I).pattern

# p_strong_1_ = re.compile("\\[strong_begin\\]").pattern

# p_strong_2_ = re.compile("\\[strong_end\\]").pattern

# 把连续换行（中间有空格）替成一个
p_empty_newline = re.compile(u"[\r\n][\\s　]*[\r\n]").pattern

# 把连续空格替成一个
p_space = re.compile(u"[ 　]+").pattern

# 把换行之后的空格（段落缩进）替空
p_newline_space = re.compile(u"\r\n[ 　]+").pattern


def extractForHTML(rawHtmlCode):
    return extractForHTML1(rawHtmlCode, " ")


def extractForTags(rawHtmlCode):
    rawHtmlCode = tagExtract(rawHtmlCode, 'script')
    rawHtmlCode = tagExtract(rawHtmlCode, 'noscript')
    rawHtmlCode = tagExtract(rawHtmlCode, 'style')
    rawHtmlCode = tagExtract(rawHtmlCode, 'img')
    rawHtmlCode = tagExtract(rawHtmlCode, 'iframe')

    rawHtmlCode = commentExtract(rawHtmlCode)
    return extractForHTML1(rawHtmlCode, " ")


# /**
#   * 去掉字符串中的HTML字符
#   * @ param rawHtmlCode
#   * @ param substitution
#   * @ return
#   * /
def extractForHTML1(rawHtmlCode, substitution):
    if rawHtmlCode == None:
        return ""

    # 避免全角＆替换为半角&产生的问题
    if isinstance(rawHtmlCode, unicode):
        text = toDBCcaseUnicode(rawHtmlCode)
    elif isinstance(rawHtmlCode, str):
        text = toDBCcase(rawHtmlCode)
    else:
        text = toDBCcase(str(rawHtmlCode))  # .replaceAll("\n", "")
    # text = text.replaceAll("\r", "");

    # m = re.finditer(p1, text)
    # if m:
    #     text = text.replace(m.group(), " ")

    m = re.finditer(p2, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    # 去掉
    # m = re.finditer(p3, text)
    # for _m in m:
    #     text = text.replace(_m.group(), "")

    m = re.finditer(p4, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    m = re.finditer(p5, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    m = re.finditer(p6, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    m = re.finditer(p7, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    m = re.finditer(p8, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    m = re.finditer(p9, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    # text = p_strong_1.matcher(text).replaceAll("[strong_begin]");
    # text = p_strong_2.matcher(text).replaceAll("[strong_end]");

    # END TAG: should [a-zA-Z:] or [a-zA-Z]
    # p = re.compile("</[a-zA-Z]+\\s*>", re.I);
    m = re.finditer(p10, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    # START TAG (without blank space)
    # p = re.compile("<[a-zA-Z]+[/]?>", re.I);
    m = re.finditer(p11, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    pos1 = text.find("<img")
    pos2 = -1
    while pos1 > -1:
        pos2 = text.find(">", pos1)
        if pos2 < 0:
            pos2 = text.find("<", pos1)
        text = text[0: pos2] + "[img_end]" + text[pos2 + 1: len(text)]
        pos1 = text.find("<img", pos2)
        # print pos1

    m = re.finditer(p_img, text)
    for _m in m:
        text = text.replace(_m.group(), "[img_begin]")

    m = re.finditer(p12, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    m = re.finditer(p13, text)
    for _m in m:
        text = text.replace(_m.group(), substitution)

    # p = re.compile("\\s+");
    # m = p1.matcher(text);
    # text = m.replaceAll(" ");

    # text = text.replaceAll("&amp;", "&");
    # text = text.replaceAll("&", "&amp;");
    # text = text.replaceAll("'", "&apos;");
    # text = text.replaceAll("\"", "&quot;");
    # text = text.replaceAll("<", "&lt;");
    # text = text.replaceAll(">", "&gt;");

    m = re.finditer(p_img_1, text)
    for _m in m:
        text = text.replace(_m.group(), "<img")

    m = re.finditer(p_img_2, text)
    for _m in m:
        text = text.replace(_m.group(), ">")

    # text = p_strong_1_.matcher(text).replaceAll("<strong>");
    # text = p_strong_2_.matcher(text).replaceAll("</strong>");

    m = re.finditer(p_empty_newline, text)
    for _m in m:
        text = text.replace(_m.group(), "\r\n")

    m = re.finditer(p_space, text)
    for _m in m:
        text = text.replace(_m.group(), " ")

    m = re.finditer(p_newline_space, text)
    for _m in m:
        text = text.replace(_m.group(), "\r\n")

    return text.strip()


# /**
#  * 完成全角字符到半角字符的转换
#  *
#  * /
def toDBCcase(src):
    ch = ''
    for i in range(len(src)):
        c = ord(src[i])
        if c >= 65281 and c <= 65374:
            ch = ch + chr(c - 65248)
        else:
            ch = ch + chr(c)
    return ch


def toDBCcaseUnicode(src):
    ch = ''
    for i in range(len(src)):
        c = ord(src[i])
        if c >= 65281 and c <= 65374:
            ch = ch + unichr(c - 65248)
        else:
            ch = ch + unichr(c)
    return ch


# /**
#  * 去除注释
#  *
#  * /
def commentExtract(data):
    soup = BeautifulSoup(data, 'html.parser')
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()

    return soup.prettify()


# /**
#  * 去处单个标签
#  * 例：<div.*?</div>
#  * /
def tagExtract(data, tagType):
    soup = BeautifulSoup(data, 'html.parser')
    [s.extract() for s in soup(tagType)]

    return soup.prettify()


if __name__ == '__main__':
    # test = "<div style=&apos;float:left; width:259px;&apos;><img>待定</div><div class=&apos;jsq&apos;><a href=&apos;http://house.fdc.com.cn/jsq/index.htm&apos; target=&apos;_blank&apos;>贷款计算器</a></div>"
    if os.path.exists('d:\\test.htm'):
        with open('d:\\test.htm') as json_file:
            test = json_file.read()
            print extractForTags(test)
            # print tagExtract(test, 'div')
            # print htmlExtract(test)
