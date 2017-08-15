# -*-coding: utf-8-*-
import json
import urllib2

import time
import json

from tools.ElasticsearchJson import executeES
from tools.Launcher import SinaLauncher
from tools.Pattern import getMatchList, getMatch
from tools.URLTools import getUrlToPattern
#from xnr.weio_publish_func import getUserShow,getCoutry,getProvince,getCity

#import sys
#sys.path.append('../')
from userinfo import SinaOperateAPI

class FeedbackFollow:
    def __init__(self, uid, current_ts):
        self.uid = uid
        self.update_time = current_ts

    def follow(self):
        cr_url = 'http://weibo.com/p/100505%s/myfollow?t=1&pids=Pl_Official_RelationMyfollow__93' \
                 '&cfs=&Pl_Official_RelationMyfollow__93_page=1#Pl_Official_RelationMyfollow__93'
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

                    operate = SinaOperateAPI()
                    user_info = operate.getUserShow(uid=uid)
                    #print user_info
                    #location = user_info['location']
                    #province = operate.getProvince(user_info['province'])
                    #city = operate.getCity(user_info['province'], user_info['city'])
                    #print location, '==', province, '--', city


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
                        'weibo_type': _type,#,
                        'update_time':self.update_time,
                        'fans':user_info['followers_count'],
                        'follower':user_info['friends_count'],
                        'weibos':user_info['statuses_count'],
                        'geo': user_info['location']
                        #'update_time': int(round(time.time()))
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
                print 'next_pageUrl', next_pageUrl
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
                    'weibo_type': _type,#,
                    'update_time':self.update_time#,
                    #'update_time': int(round(time.time()))
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
                request = urllib2.Request(comment_url)
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
                    'timestamp': timestamp,#,
                    'update_time':self.update_time#,
                    #'update_time': int(round(time.time()))
                }

                wb_json = json.dumps(wb_item)
                # print wb_json
                json_list.append(wb_json)

        return json_list

    def execute(self):
        # fans = self.fans()
        #executeES('weibo_feedback_follow', 'text', fans)
        # executeES('weibo_feedback_fans', 'text', fans)

        follow = self.follow()
        #executeES('weibo_feedback_followed', 'text', follow)
        executeES('weibo_feedback_follow', 'text', follow)

        # groups = self.groups()
        # executeES('weibo_feedback_group', 'text', groups)

        return fans, follow, groups


if __name__ == '__main__':
    xnr = SinaLauncher('weiboxnr02@126.com','xnr123456')
    xnr.login()
    FeedbackFollow(xnr.uid, time.time()).execute()
