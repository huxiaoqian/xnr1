# -*-coding: utf-8-*-
import json
import urllib2

import time

from tools.ElasticsearchJson import executeES
from tools.Launcher import SinaLauncher
from tools.Pattern import getMatchList, getMatch
from tools.URLTools import getUrlToPattern


class FeedbackFollow:
    def __init__(self, uid):
        self.uid = uid

    def follow(self):
        cr_url = 'http://weibo.com/p/100505%s/myfollow?t=1&pids=Pl_Official_RelationMyfollow__93' \
                 '&cfs=&Pl_Official_RelationMyfollow__93_page=1#Pl_Official_RelationMyfollow__93'
        json_list = []

        comment_url = cr_url % self.uid
        while True:
            print comment_url
            try:
                request = urllib2.Request(comment_url)
                response = urllib2.urlopen(request, timeout=60)
                html = response.read().decode('string_escape').replace('\\/', '/')
            except Exception, e:
                print "Network Exception!!! ", e
            finally:
                datas = getMatchList(html, '<div class="member_wrap clearfix".*?<div class="markup_choose')
                # print len(datas)

                for data in datas:
                    photo_url = "http:" + getMatch(data, '<img.*?src="(*)"')
                    uid = getMatch(data, 'usercard="id=(*)"')
                    nickname = getMatch(data, '<img.*? title="(*)"')
                    r_uid = self.uid
                    _type = 'follow'

                    wb_item = {
                        'photo_url': photo_url,
                        'uid': uid,
                        'nickname': nickname,
                        'r_uid': r_uid,
                        'type': _type
                    }

                    wb_json = json.dumps(wb_item)
                    # print wb_json
                    json_list.append(wb_json)

                # 分页
                next_pageUrl = getUrlToPattern(html, comment_url, pattern='page', text_pattern='下一页')
                # print next_pageUrl
                if next_pageUrl:
                    comment_url = next_pageUrl[0]
                else:
                    break
        return json_list

    def fans(self):
        cr_url = 'http://weibo.com/p/100505%s/myfollow?pids=Pl_Official_RelationFans__88&cfs=600' \
                 '&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__88_page=1#Pl_Official_RelationFans__88'
        json_list = []

        comment_url = cr_url % self.uid
        list_data = []
        while True:
            print comment_url
            try:
                request = urllib2.Request(comment_url)
                response = urllib2.urlopen(request, timeout=60)
                html = response.read().decode('string_escape').replace('\\/', '/')
            except Exception, e:
                print "Network Exception!!! ", e
            finally:
                datas = getMatchList(html, '<dl class="clearfix">.*?</dl>')
                # print len(datas)
                # r_datas = datas.reverse()
                list_data.append(datas)

                # 分页
                next_pageUrl = getUrlToPattern(html, comment_url, pattern='page', text_pattern='下一页')
                # print next_pageUrl
                if next_pageUrl:
                    comment_url = next_pageUrl[0]
                else:
                    break

        r_list_data = reversed(list_data)
        for l_datas in r_list_data:
            r_datas = reversed(l_datas)
            for data in r_datas:
                photo_url = "http:" + getMatch(data, '<img.*?src="(*)"')
                uid = getMatch(data, 'usercard="id=(*)&')
                nickname = getMatch(data, '<img.*?alt="(*)"')
                timestamp = int(round(time.time()))
                time.sleep(1)

                sex = getMatch(data, '<i class="W_icon icon_(*)"')
                if not sex:
                    sex = ''
                follower = getMatch(data, 'follow" >(*)</a>')
                if follower and follower.isdigit():
                    follower = long(follower)
                else:
                    follower = 0
                geo = getMatch(data, '>地址</em>(*)</div>')
                if not geo:
                    geo = ''
                fan_source = getMatch(data, 'class="S_link2">(*)</a>')
                if not fan_source:
                    fan_source = ''
                fans = getMatch(data, 'current=fans" >(*)</a>')
                if fans and fans.isdigit():
                    fans = long(fans)
                else:
                    fans = 0
                description = getMatch(data, '<div class="info_intro"><span>(*)</span>')
                if not description:
                    description = ''
                weibos = getMatch(data, '/u/' + uid + '" >(*)</a>')
                if weibos and weibos.isdigit():
                    weibos = long(weibos)
                else:
                    weibos = 0

                r_uid = self.uid
                _type = 'followed'

                wb_item = {
                    'photo_url': photo_url,
                    'uid': uid,
                    'mid': uid,
                    'nick_name': nickname,
                    'timestamp': timestamp,
                    'sex': sex,
                    'follower': follower,
                    'geo': geo,
                    'fan_source': fan_source,
                    'fans': fans,
                    'description': description,
                    'weibos': weibos,
                    'root_uid': r_uid,
                    'weibo_type': _type
                }

                wb_json = json.dumps(wb_item)
                # print wb_json
                json_list.append(wb_json)

        return json_list


def execute():
    xnr = SinaLauncher('', '')
    xnr.login()
    mess = FeedbackFollow(xnr.uid)

    list = mess.fans()
    executeES('weibo_feedback_follow', 'text', list)


if __name__ == '__main__':
    execute()
