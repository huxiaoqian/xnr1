# -*-coding: utf-8-*-
import json
import urllib2

import time

from tools.ElasticsearchJson import executeES
from tools.Launcher import SinaLauncher
from tools.Pattern import getMatchList, getMatch
from tools.URLTools import getUrlToPattern
from userinfo import SinaOperateAPI

class FeedbackFollow:
    def __init__(self, uid, current_ts):
        self.uid = uid
        self.update_time = current_ts

        self._headers = {
            "Headers": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;"
                       " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;"
                       " .NET4.0C; .NET4.0E; InfoPath.3)",
            "Referer": "http://weibo.com/u/%s/home?topnav=1&wvr=6" % self.uid
        }

    def follow(self):
        cr_url = 'http://weibo.com/p/100505%s/myfollow?t=1&pids=Pl_Official_RelationMyfollow__93' \
                 '&cfs=&Pl_Official_RelationMyfollow__93_page=1#Pl_Official_RelationMyfollow__93'
        json_list = []

        comment_url = cr_url % self.uid
        list_data = []
        while True:
            print comment_url
            try:
                request = urllib2.Request(comment_url, headers=self._headers)
                response = urllib2.urlopen(request, timeout=60)
                html = response.read().decode('string_escape').replace('\\/', '/')
            except Exception, e:
                print "Network Exception!!! ", e
            finally:
                datas = getMatchList(html, '<li class="member_li S_bg1".*?</li>')
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
                    #print 'data::',data
                    photo_url = getMatch(data, 'profile_image_url=(*)&')
                    uid = getMatch(data, 'usercard="id=(*)"')
                    nickname = getMatch(data, '<img.*?alt="(*)"')
                    timestamp = int(round(time.time()))
                    time.sleep(1)

                    sex = getMatch(data, '&sex=(*)"')
                    if not sex:
                        sex = ''
                    elif sex == 'f':
                        sex = 'female'
                    elif sex == 'm':
                        sex = 'male'

                    follow_source = getMatch(data, 'class="S_link2" >(*)</a>')
                    if not follow_source:
                        follow_source = ''

                    description = getMatch(data, 'W_autocut S_txt2">(*)</div>')
                    if not description:
                        description = ''

                    gid = getMatch(data, '&gid=(*)&')
                    if not gid:
                        gid = '0'
                    gname = getMatch(data, '&gname=(*)&')
                    if not gname:
                        gname = ''

                    r_uid = self.uid
                    _type = 'follow'

                    #获得关注人的详细信息
                    #user = SinaOperateAPI().getUserShow(uid=uid)

                    wb_item = {
                        'photo_url': photo_url,
                        'uid': uid,
                        'mid': uid,
                        'nick_name': nickname,
                        'timestamp': timestamp,
                        'sex': sex,
                        'description': description,
                        'follow_source': follow_source,
                        'gid': gid,
                        'gname': gname,
                        'root_uid': r_uid,
                        'weibo_type': _type,
                        'update_time': self.update_time
                    }

                    wb_json = json.dumps(wb_item)
                    # print wb_json
                    json_list.append(wb_json)

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
                request = urllib2.Request(comment_url, headers=self._headers)
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
                    'weibo_type': _type,
                    'update_time': self.update_time
                }

                wb_json = json.dumps(wb_item)
                # print wb_json
                json_list.append(wb_json)

        return json_list

    def groups(self):
        cr_url = 'http://weibo.com/p/100505%s/myfollow?pids=Pl_Official_RelationGroupList__96&relate=group' \
                 '&Pl_Official_RelationGroupList__96_page=1#Pl_Official_RelationGroupList__96'
        json_list = []

        comment_url = cr_url % self.uid
        list_data = []
        while True:
            print comment_url
            try:
                request = urllib2.Request(comment_url, headers=self._headers)
                response = urllib2.urlopen(request, timeout=60)
                html = response.read().decode('string_escape').replace('\\/', '/')
            except Exception, e:
                print "Network Exception!!! ", e
            finally:
                datas = getMatchList(html, '<div class="mod_info">.*?</p>')
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
                gid = getMatch(data, '/p/230491(*)"')
                gname = getMatch(data, 'relation_center">(*)</a></div>')
                timestamp = int(round(time.time()))
                time.sleep(1)

                wb_item = {
                    'uid': self.uid,
                    'mid': gid,
                    'gid': gid,
                    'gname': gname,
                    'timestamp': timestamp,
                    'update_time': self.update_time
                }

                wb_json = json.dumps(wb_item)
                # print wb_json
                json_list.append(wb_json)

        return json_list

    def execute(self):
        fans = self.fans()
        print 'fans:::',fans
        executeES('weibo_feedback_fans', 'text', fans)

        follow = self.follow()
        executeES('weibo_feedback_follow', 'text', follow)

        groups = self.groups()
        executeES('weibo_feedback_group', 'text', groups)

        return fans, follow, groups


if __name__ == '__main__':
    current_ts = int(time.time())
    xnr = SinaLauncher('13718641914', 'hua198912180')
    xnr.login()
    FeedbackFollow(xnr.uid, current_ts).execute()
