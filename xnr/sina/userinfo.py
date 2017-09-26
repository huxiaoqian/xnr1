#-*-coding: utf-8-*-
import base64
import json
import os.path
import time
import urllib
import urllib2

import re

from tools.Launcher import SinaLauncher


class SinaOperateAPI:
    def getUserShow(self, uid=None, screen_name=None):
        """
        字段说明见userinfo.txt
        :return:
        """
        u_url = 'https://api.weibo.com/2/users/show.json?access_token=2.009t4mFGWp4peBbb59564f4e5n6k6B'
        if uid:
            u_url += "&uid=" + uid
        if screen_name:
            u_url += "&screen_name=" + urllib.quote(screen_name)
        print 'u_url:', u_url
        #try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url= u_url, headers=headers)
        response = urllib2.urlopen(request, timeout=600)
        
        content = json.loads(response.read())
        return content
        #except Exception, e:
        #    print "download page error!!! ", e
        #    return ''

    def getCoutry(self, key=None):
        u_url = 'https://api.weibo.com/2/common/get_country.json?access_token=2.009t4mFGWp4peBbb59564f4e5n6k6B'

        try:
            request = urllib2.Request(u_url)
            response = urllib2.urlopen(request, timeout=60)

            content = json.loads(response.read())
            if key:
                for country in content:
                    for k, v in country.items():
                        if k == key:
                            return v
            else:
                return content
        except Exception, e:
            print e
            return ''

    def getProvince(self, key=None):
        u_url = 'https://api.weibo.com/2/common/get_province.json' \
                '?access_token=2.009t4mFGWp4peBbb59564f4e5n6k6B&country=001'
        code = '0010'

        if key == '400':
            return '海外'
        if key == '100':
            return '其他'

        try:
            request = urllib2.Request(u_url)
            response = urllib2.urlopen(request, timeout=60)

            content = json.loads(response.read())
            if key:
                code_key = code + key
                for country in content:
                    for k, v in country.items():
                        if k == code_key:
                            return v
            else:
                return content
        except Exception, e:
            print e
            return ''

    def getCity(self, province, key=None):
        u_url = 'https://api.weibo.com/2/common/get_city.json' \
                '?access_token=2.009t4mFGWp4peBbb59564f4e5n6k6B&province=%s'
        code = '0010'

        if province == '400':
            if os.path.exists('400.json'):
                rfile = open('400.json', 'r')
                data = rfile.read()
                rfile.close()
                content = json.loads(data)
                print content
                for country in content:
                    for k, v in country.items():
                        if k == key:
                            return v
            else:
                print '400.json missing'
            return ''
        if province == '100':
            return ''

        try:
            provinceCode = code + province
            u_url = u_url % provinceCode
            request = urllib2.Request(u_url)
            response = urllib2.urlopen(request, timeout=60)

            content = json.loads(response.read())
            if key:
                if len(key) == 1:
                    code_key = provinceCode + '00' + key
                if len(key) == 2:
                    code_key = provinceCode + '0' + key
                for country in content:
                    for k, v in country.items():
                        if k == code_key:
                            return v
            else:
                return content
        except Exception, e:
            print e
        return ''


def execute():
    """
    输入用户名、密码登录
    输入发布内容（和rank）
    :return:
    """
    xnr = SinaLauncher('weiboxnr05@126.com', 'Bh123456')
    xnr.login()

    #user = SinaOperateAPI()

    #user = SinaOperateAPI().getUserShow(screen_name='巨星大大')
    print xnr.uid

if __name__ == '__main__':
    #execute()
    # user = SinaOperateAPI().getUserShow(screen_name='巨星大大')
    # print user
    # execute()
    user = SinaOperateAPI().getUserShow(screen_name='巨星大大')

    print user
