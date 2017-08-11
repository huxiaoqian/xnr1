# -*-coding: utf-8-*-
import os.path
import re
from urlparse import urljoin, urlsplit


# /**
#  * 直接拼出完整的URL
#  *
#  * @param p_url
#  * @param n_url
#  * @return
#  */
def urlToParse(p_url, n_url):
    url = urljoin(p_url, n_url)
    return url


p_1 = re.compile("\\\\").pattern

p_2 = re.compile("http(s)*://", re.I).pattern

p_3 = re.compile("\\./").pattern


# p_sp = re.compile("/+").pattern;

# /**
#  * 利用正则匹配到完整URL
#  *
#  * @param url（子）
#  * @param currentUrl（父）
#  * @return
#  */
def changeUrl(url, currentUrl):
    str = ''
    if url.startswith("http://") or url.startswith("https://"):
        return url

    if url[0] == '?':
        pos = currentUrl.find("?")
        if pos > -1:
            str = currentUrl[0, pos] + url
        else:
            str = currentUrl + url
        return str

    try:
        str = urljoin(currentUrl, url)
        url = urlsplit(str)
        path = url.path
        # print path, url.path
        if path.find("/../") > -1:
            path = path.replace("/../", "/")
        elif str.find("/./") > -1:
            path = path.replace("/./", "/")
        if path != url.path:
            # print "here"
            str = str.replace(url.path, path)
    except Exception, e:
        str = ""

    return str


# /**
#  * ['\\\"]
#  */
p_html_1 = re.compile("['\\\"]").pattern

# /**
#  * <
#  */
p_html_2 = re.compile("<").pattern

# /**
#  * href=
#  */
p_html_3 = re.compile("href=", re.I).pattern

# /**
#  * [\">]
#  */
p_html_4 = re.compile("[\">]").pattern

# /**
#  * src=
#  */
p_html_6 = re.compile("src=", re.I).pattern

# <h2>(?:(?!<h2>).)*?</h2>
# <a(?:(?!<a).)*?</a
p_html_a = re.compile("<a (?:(?!<a ).)*?(?=(</a|<a))", re.I | re.S).pattern

p_html_area = re.compile("<area.*?>", re.I | re.S).pattern

p_html_url = re.compile("href=[ ]*[^ ]+?[ >]", re.I).pattern

p_html_text = re.compile(">.*?$", re.I | re.S).pattern

p_html_script = re.compile("<script.*?</script", re.I | re.S).pattern

p_html_script_2 = re.compile("<script.*?</script>", re.I | re.S).pattern

p_html_src = re.compile("src=[ ]*[^ ]+?[ >]", re.I).pattern

p_html_sp = re.compile("[a-zA-Z0-9_]+\\.jsp\\?[a-zA-Z0-9_=&]+", re.I).pattern

p_html_iframe = re.compile("<iframe.*?</iframe", re.I | re.S).pattern

p_base = re.compile("(?<![\"'])<base.*?>", re.I | re.S).pattern


def getUrlToPattern(s, thisurl, pattern=None, text_pattern=None):
    urlLists = getUrls(s, False, False, True, thisurl)
    url_list = []
    for lists in urlLists:
        # print lists[0]
        if pattern and text_pattern:
            # print pattern, text_pattern
            if lists[0].find(pattern) > -1 and lists[1].find(text_pattern) > -1:
                url_list.append(lists[0])
        elif pattern:
            if lists[0].find(pattern) > -1:
                url_list.append(lists[0])
        elif text_pattern:
            if lists[1].find(text_pattern) > -1:
                url_list.append(lists[0])
    return url_list


def getUrl(s, thisurl):
    return getUrls(s, False, False, True, thisurl)


def getUrl1(s, considerScript, considerIframe, thisurl):
    return getUrls(s, considerScript, considerIframe, True, thisurl)


p_space = re.compile(r'\s+').pattern


#  /**
# 	 * 抽取页面源码中的标准URL
# 	 *
# 	 * @param s
# 	 * @param considerScript
# 	 * @param considerIframe
# 	 * @param thisurl
# 	 * @return
# 	 */
def getUrls(s, considerScript, considerIframe, considerArea, thisurl):
    html = s

    m_base = re.search(p_base, html)
    if m_base:
        base = m_base.group()
        m = re.search(p_html_url, base)
        if m:
            base_url = m.group()
            result = re.search(p_html_3, base_url)
            base_url = base_url.replace(result.group(), '')

            result = re.search(p_html_4, base_url)
            base_url = base_url.replace(result.group(), '').strip()
            thisurl = base_url

    html_re = re.search(p_html_1, html)
    if html_re:
        html = html.replace(html_re.group(), '')

    html_re = re.search(p_html_2, html)
    if html_re:
        html = html.replace(html_re.group(), ' <')

    al = []
    _match = re.search(p_html_script_2, html)
    if _match:
        html = html.replace(_match.group(), '')
    matcher = re.finditer(p_html_a, html)

    for m_match in matcher:
        strurl = m_match.group()

        murl = re.search(p_html_url, strurl)
        mtext = re.search(p_html_text, strurl)

        tempurl = ""
        temptext = ""
        if murl:
            tempurl = murl.group()
        else:
            continue

        if mtext:
            temptext = mtext.group()
        else:
            continue
        _temp = re.search(p_html_3, tempurl)
        tempurl = tempurl.replace(_temp.group(), '')

        _temp = re.search(p_html_4, tempurl)
        if _temp:
            tempurl = tempurl.replace(_temp.group(), '').strip()

        temptext = temptext[1: len(temptext) - 1]
        if len(tempurl) < 1:
            continue

        # print matcher.__init__()
        ss = ['', '', '']
        ss[0] = changeUrl(tempurl, thisurl).strip()

        tt = re.search(p_space, temptext.strip())
        if tt:
            ss[1] = temptext.strip().replace(tt.group(), '')
        else:
            ss[1] = temptext.strip()

        ss[2] = html.index(strurl)  # not sure, the postion of url in html

        al.append(ss)

    if considerScript:
        matcher = re.finditer(p_html_script, html)
        for m_match in matcher:
            strurl = m_match.group()
            murl = re.search(p_html_src, strurl)

            tempurl = ""
            if murl:
                tempurl = murl.group()
            else:
                continue
            if tempurl == "":
                murl = re.search(p_html_sp, strurl)
                if murl:
                    tempurl = murl.group()

            _temp = re.search(p_html_6, tempurl)
            tempurl = tempurl.replace(_temp.group(), '')

            _temp = re.search(p_html_4, tempurl)
            tempurl = tempurl.replace(_temp.group(), '').strip()
            if len(tempurl) < 1:
                continue

            ss = ['', '', '']
            ss[0] = changeUrl(tempurl, thisurl).strip()
            ss[1] = ""
            ss[2] = html.index(strurl)

            al.append(ss)

    if considerIframe:
        matcher = re.finditer(p_html_iframe, html)
        for m_match in matcher:
            strurl = m_match.group()
            murl = re.search(p_html_src, strurl)

            tempurl = ""
            if murl:
                tempurl = murl.group()
            else:
                continue

            _temp = re.search(p_html_6, tempurl)
            tempurl = tempurl.replace(_temp.group(), '')

            _temp = re.search(p_html_4, tempurl)
            tempurl = tempurl.replace(_temp.group(), '').strip()
            if len(tempurl) < 1:
                continue

            ss = ['', '', '']
            ss[0] = changeUrl(tempurl, thisurl).strip()
            ss[1] = ""
            ss[2] = html.index(strurl)

            al.append(ss)

    if considerArea:
        matcher = re.finditer(p_html_area, html)
        for m_match in matcher:
            strurl = m_match.group()
            murl = re.search(p_html_url, strurl)

            tempurl = ""
            temptext = ""
            if murl:
                tempurl = murl.group()
            else:
                continue

            _temp = re.search(p_html_3, tempurl)
            tempurl = tempurl.replace(_temp.group(), '')

            _temp = re.search(p_html_4, tempurl)
            tempurl = tempurl.replace(_temp.group(), '').strip()

            if len(tempurl) < 1:
                continue

            ss = ['', '', '']
            ss[0] = changeUrl(tempurl, thisurl).strip()
            ss[1] = temptext.strip()
            ss[2] = html.index(strurl)

            al.append(ss)
    # print al
    return al


p_img = re.compile("<img.*?src\\s*=\\s*.*?[ >]", re.I | re.S).pattern

p_img_1 = re.compile("<img.*?src\\s*=\\s*", re.I | re.S).pattern

p_img_2 = re.compile("[ >]", re.I | re.S).pattern


# /* *
# 	 * 抽取页面源码中图片的标准URL
# 	 *
# 	 * @param s
# 	 * @param thisurl
# 	 * @return
# 	 */
def getImages(s, thisurl):
    als = []

    matcher = re.finditer(p_img, s)
    for m_match in matcher:
        src_segment = m_match.group()

        _temp = re.search(p_img_1, src_segment)
        url = src_segment.replace(_temp.group(), '')

        _temp = re.search(p_img_2, url)
        url = url.replace(_temp.group(), '')
        if url.startswith("'") or url.startswith("\""):
            url = url[1: len(url) - 1]
        if url.endswith("/"):
            url = url[0: len(url) - 1]
        if url.endswith("'") or url.endswith("\""):
            url = url[0: len(url) - 1]
        if len(url.strip()) < 1:
            continue
        absolute_url = changeUrl(url, thisurl)

        al = [absolute_url, ""]
        als.append(al)
    return als


if __name__ == '__main__':
    # test = changeUrl(".././..//1/2010-07/15/001/20100715001_pdf.pdf",
    #                  "http://www.wccdaily.com.cn/epaper/hxdsb/html/2010-07/15/node_52.htm")
    # print "test: ", test


    rootdir = "d:\\test.htm"
    if os.path.exists(rootdir):
        print "dir---", rootdir
        with open(rootdir) as json_file:
            data = json_file.read()
            # list = getUrl(data, "http://www.globalsecurity.org/military/world/centralasia/index.html")
            # print list
            list = getImages(data, "http://www.globalsecurity.org/military/world/centralasia/index.html")
            for li in list:
                print li[0], li[1]
