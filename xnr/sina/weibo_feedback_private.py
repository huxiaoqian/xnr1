# -*-coding: utf-8-*-

import json
import time
import urllib2
#from bs4 import BeautifulSoup
from sina.weibo_feedback_follow import FeedbackFollow
from tools.ElasticsearchJson import executeES
from tools.TimeChange import getTimeStamp

from tools.Launcher import SinaLauncher
from tools.HtmlExtractor import extractForHTML, commentExtract
from tools.Pattern import getMatchList, getMatch
from tools.URLTools import getUrlToPattern


class FeedbackPrivate:
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

    def messages(self):
        cr_url = 'http://weibo.com/messages?pids=Pl_Content_MessageList&page=1'
        de_url = 'http://weibo.com/aj/message/getbyid?ajwvr=6&count=50&uid=%s&_t=0&__rnd=%d'
        json_list = []
        tags = False

        comment_url = cr_url
        while True:
            print comment_url
            try:
                request = urllib2.Request(comment_url, headers=self._headers)
                response = urllib2.urlopen(request, timeout=60)
                html = response.read().decode('string_escape').replace('\\/', '/')
            except Exception, e:
                print "Network Exception!!! ", e
                #print 'html:', html
            
            finally:
                datas = getMatchList(html, '<div class="private_list SW_fun_bg S_line2 clearfix".*?<!-- 下拉列表 -->')

                for data in datas:
                    photo_url = "http:" + getMatch(data, '<img.*?src="(*)"')
                    uid = getMatch(data, 'usercard="id=(*)"')
                    nickname = getMatch(data, '<img.*?alt="(*)"')
                    r_uid = self.uid
                    
                    counts = getMatch(data, '<em class="W_new_count S_spetxt_bg">(*)</em>')
                    if counts and counts.isdigit():
                        counts = long(counts)
                    else:
                        counts = 0
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

                    try:
                        detailUrl = de_url % (uid, int(time.time() * 1000))
                        print 'detail_url:', detailUrl
                        request = urllib2.Request(detailUrl)
                        response = urllib2.urlopen(request, timeout=60)

                        ms_content = json.loads(response.read())
                        
                    except Exception, e:
                        print "Network Exception!!! ", e
                    else:
                        html = ms_content["data"]["html"]
                        ms_datas = getMatchList(html, u'(<!-- 单行文字-->|<div class="space">).*?<!--／附件信息-->')
                        # print datas[0]
                        last_time = 0
                        for ms_data in ms_datas:
                            mid_uid = getMatch(ms_data, 'usercard="id=(*)"')
                            mid = getMatch(ms_data, 'mid="(*)"')
                            timestamp = getMatch(ms_data, 'prompt_font S_txt2 S_bg1">(*)</legend>')
                            #soup = BeautifulSoup(ms_data)
                            #timestamp_bs4 = soup.find_all('legend', class_=["prompt_font", "S_txt2", "S_bg1"])
                            if timestamp:
                                timestamp = long(getTimeStamp(timestamp))
                                last_time = timestamp
                            else:
                                timestamp = last_time
                            
                            if timestamp < self.lasttime:
                                tags = True
                                print 'timestamp<lasttime, timestamp, lasttime:', timestamp, self.lasttime
                                #break
                                next

                            text = getMatch(ms_data, u'<div class="cont">.*?<!--／附件信息-->')
                            if text:
                                text = extractForHTML(text)
                                text = commentExtract(text)

                            if mid_uid == uid:
                                private_type = 'receive'
                            elif mid_uid == r_uid:
                                private_type = 'make'
                            else:
                                private_type = ''

                            wb_item = {
                                'photo_url': photo_url,
                                'uid': uid,
                                'nick_name': nickname,
                                'mid': mid,
                                'timestamp': timestamp,
                                'text': text,
                                'root_uid': r_uid,
                                'weibo_type': _type,
                                'private_type': private_type,
                                'w_new_count': counts,
                                'update_time': self.update_time
                            }

                            wb_json = json.dumps(wb_item)
                            print wb_json
                            json_list.append(wb_json)
            
                # 分页
                next_pageUrl = getUrlToPattern(html, comment_url, pattern='page', text_pattern='下一页')
                # print next_pageUrl
                if next_pageUrl:
                    comment_url = next_pageUrl[0]
                elif not next_pageUrl or tags:
                    break
            
        json_list = []
        return json_list

    def execute(self):
        mess = self.messages()
        executeES('weibo_feedback_private', 'text', mess)


if __name__ == '__main__':
    user = 'weiboxnr04@126.com'
    pwd = 'xnr123456'
    xnr = SinaLauncher(user, pwd)
    xnr.login()
    FeedbackPrivate(xnr.uid).execute()
