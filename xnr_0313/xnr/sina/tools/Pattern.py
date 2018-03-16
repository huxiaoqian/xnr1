# -*-coding: utf-8-*-
import os.path
import re

SP_MARK = r"(*)"
SP_MARKS = r"(.*?)"


# /**
#  * 处理正则表达式
#  *
#  * @param sp_regex
#  * @param case_insensitive
#  * @return
#  */
def createPattern(sp_regex, case_insensitive):
    # patterns = []
    pos = -1
    pos = sp_regex.find(SP_MARK)

    if pos > -1:
        patterns = ['', '', '']
        subRegex_0 = sp_regex[0: pos]
        subRegex_1 = sp_regex[(pos + len(SP_MARK)): len(sp_regex)]
        if case_insensitive:
            patterns[0] = re.compile(subRegex_0 + ".*?" + subRegex_1, re.I | re.S).pattern
            patterns[1] = re.compile(subRegex_0, re.I | re.S).pattern
            patterns[2] = re.compile(subRegex_1, re.I | re.S).pattern
        else:
            patterns[0] = re.compile(subRegex_0 + '.*?' + subRegex_1, re.S).pattern
            patterns[1] = re.compile(subRegex_0, re.S).pattern
            patterns[2] = re.compile(subRegex_1, re.S).pattern
        return patterns
    else:
        patterns = ['']
        if case_insensitive:
            patterns[0] = re.compile(sp_regex, re.I | re.S).pattern
        else:
            patterns[0] = re.compile(sp_regex, re.S).pattern
        return patterns


# /**
#  * 新增仅匹配一次的方法
#  *
#  * @param content
#  * @param sp_regex
#  * @return
#  */
def getMatch(content, sp_regex):
    return __getMatch(content, sp_regex, False)


# /**
#  * 新增仅匹配一次的方法
#  *
#  * @param content
#  * @param sp_regex
#  * @param case_insensitive
#  * @return
#  */
def __getMatch(content, sp_regex, case_insensitive):
    try:
        patterns = createPattern(sp_regex, case_insensitive)
        if SP_MARK in sp_regex:
            patterns[0] = patterns[0].replace("(*)", "(.*?)")
        if SP_MARKS in sp_regex:
            patterns[0] = patterns[0].replace("(.*?)", ".*?")

        _content = content.replace('\n', '\\n')  # 去除隐式回车换行
        m = re.search(patterns[0], _content)
        # print _content, patterns[0]
        if m:
            _match = m.group()
            if len(patterns) > 1:
                result = re.search(patterns[1], _match)
                _match = _match.replace(result.group(), '', 1)

                result = re.search(patterns[2], _match)
                _match = _match.replace(result.group(), '', 1)
            return _match.replace('\\n', '\n')
    except Exception, e:
        print 'pattern Exception', e
    return None


# /**
#  * @param content
#  *            用于匹配的正文
#  * @param sp_regex
#  *            用于匹配的（特殊）正则表达式
#  * @return 匹配结果列表
#  */
def getMatchList(content, sp_regex):
    return __getMatchList(content, sp_regex, False, 65536)


# /**
#  * @param content
#  *            用于匹配的正文
#  * @param sp_regex
#  *            用于匹配的（特殊）正则表达式
#  * @param case_insensitive
#  *            是否忽略大小写
#  * @param match_num
#  *            最多匹配的结果数
#  * @return 匹配结果列表
#  */
def __getMatchList(content, sp_regex, case_insensitive, match_num):
    match = []
    try:
        patterns = createPattern(sp_regex, case_insensitive)
        if SP_MARK in sp_regex:
            patterns[0] = patterns[0].replace("(*)", "(.*?)")
        if SP_MARKS in sp_regex:
            patterns[0] = patterns[0].replace("(.*?)", ".*?")

        _content = content.replace('\n', '\\n')  # 去除隐式回车换行
        m = re.finditer(patterns[0], _content)

        for me in m:
            _match = me.group()
            if len(patterns) > 1:
                result = re.search(patterns[1], _match)
                _match = _match.replace(result.group(), '', 1)

                result = re.search(patterns[2], _match)
                _match = _match.replace(result.group(), '', 1)
            match.append(_match.replace('\\n', '\n'))
            if len(match) >= match_num:
                break
    except Exception, e:
        print 'Exception', str(e)
    return match


# string类型如果不是汉字，decode
# 汉字正则前加u
if __name__ == '__main__':
    # str1 = "hello like you  ,xxxx like you " \
    #       "\\r\\n\\t\\u2019this" \
    #       " is hello 33 lli 3 kkkkou"
    # str = getMatch(str1, "he.*?lo(*)you")
    # print str
    if os.path.exists('d:\\test.htm'):
        f = open('d:\\test.htm', 'r')
        data = f.read()
        # print type(data), chardet.detect(data)

        # print data.decode("gbk")
        data = data.decode("gbk")
        if data.find('\n') > -1:
            # strs = data.replace('\n', '\\r\\n')
            strs = getMatch(data, u'id="(ajaxlist|countOld)">.*?成立时间(*)jumpPage')
            print 'iiii---- ', strs
