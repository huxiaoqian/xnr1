# -*-coding: utf-8-*-

import json
import urllib2

import time

from sina.weibo_feedback_follow import FeedbackFollow
from tools.ElasticsearchJson import executeES

from tools.Launcher import SinaLauncher
from tools.HtmlExtractor import extractForHTML
from tools.Pattern import getMatchList, getMatch


class FeedbackRetweet:
    def __init__(self, uid, current_ts, fans, follow, groups, lastTime):
        self.uid = uid
        self.follow = follow
        self.fans = fans
        self.groups = groups
        self.update_time = current_ts
        self.lasttime = lastTime

        self._headers = {
            "Headers": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;"
                       " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;"
                       " .NET4.0C; .NET4.0E; InfoPath.3)",
            "Referer": "http://weibo.com/u/%s/home?topnav=1&wvr=6" % self.uid
        }

    def atMeMicroBlog(self):
        pre_page = 0
        page = 1
        pagebar = 0
        # max_page = 100
        at_MBurl = 'http://weibo.com/aj/at/mblog/list?ajwvr=6&pre_page=%s&page=%s' \
                   '&filter_by_author=0&filter_by_type=0&is_adv=0&pagebar=%s'
        json_list = []
        tags = False

        while True:
            wbUrl = at_MBurl % (pre_page, page, pagebar)
            print "current url: ", wbUrl
            try:
                request = urllib2.Request(wbUrl, headers=self._headers)
                response = urllib2.urlopen(request, timeout=60)

                mb_content = json.loads(response.read())
            except Exception, e:
                print "Network Exception!!! ", e
            finally:
                html = mb_content["data"]

                # 分页
                if html.replace('\n', '') == '' or tags:
                    break
                # if page > max_page:
                #     break
                elif pre_page < page:
                    pre_page += 1
                elif pre_page == page and pagebar == 0:
                    pagebar = 1
                elif pagebar == 1:
                    pre_page = page
                    page += 1
                    pagebar = 0

                datas = getMatchList(html, '<div class="WB_face W_fl">(*)<div node-type="feed_list_repeat')

                for data in datas:
                    photo_url = "http:" + getMatch(data, '<img.*?src="(*)"')
                    uid = getMatch(data, 'usercard="id=(*)&')
                    nickname = getMatch(data, 'nick-name="(*)"')
                    mid = getMatch(data, 'pubuser_nick:(*)"')
                    timestamp = getMatch(data, '<div class="WB_from S_txt2">.*?date="(*)"')[0:-3]
                    if timestamp and timestamp.isdigit():
                        timestamp = long(timestamp)
                    else:
                        timestamp = 0
                    print '6666666'
                    if timestamp <= self.lasttime:
                        tags = True
                        break

                    text = getMatch(data, 'feed_list_content" >(*)</div>').strip()
                    if text:
                        text = extractForHTML(text.strip())
                    else:
                        text = ''

                    retweet = getMatch(data, 'forward_btn_text">.*?<em>(*)</em>').replace('转发', '')
                    if retweet and retweet.isdigit():
                        retweet = long(retweet)
                    else:
                        retweet = 0

                    comment = getMatch(data, 'comment_btn_text">.*?<em>(*)</em>').replace('评论', '')
                    if comment and comment.isdigit():
                        comment = long(comment)
                    else:
                        comment = 0

                    like = getMatch(data, 'UI_ani_praised".*?<em>(*)</em>')
                    if like and like.isdigit():
                        like = long(like)
                    else:
                        like = 0
                    r_mid = getMatch(data, 'rootmid=(*)&')
                    r_uid = self.uid

                    _type = 'stranger'
                    type1 = ''
                    type2 = ''
                    for fljson in self.follow:
                        fjson = json.loads(fljson)
                        if fjson['uid'] == uid:
                            type1 = 'follow'
                            break
                    for fljson in self.fans:
                        fjson = json.loads(fljson)
                        if fjson['uid'] == uid:
                            type2 = 'followed'
                            break
                    if type1 and type2:
                        _type = 'friend'
                    elif type1:
                        _type = type1
                    elif type2:
                        _type = type2
                    if uid == r_uid:
                        _type = 'self'

                    wb_item = {
                        'photo_url': photo_url,
                        'uid': uid,
                        'nick_name': nickname,
                        'mid': mid,
                        'timestamp': timestamp,
                        'text': text,
                        'retweet': retweet,
                        'comment': comment,
                        'like': like,
                        'root_mid': r_mid,
                        'root_uid': r_uid,
                        'weibo_type': _type,
                        'update_time': self.update_time
                    }

                    wb_json = json.dumps(wb_item)
                    json_list.append(wb_json)
        return json_list

    def execute(self):
        retweet = self.atMeMicroBlog()
        executeES('weibo_feedback_retweet', 'text', retweet)


if __name__ == '__main__':
    xnr = SinaLauncher('', '')
    xnr.login()
    FeedbackRetweet(xnr.uid).execute()
