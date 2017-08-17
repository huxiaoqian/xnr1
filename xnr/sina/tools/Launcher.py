# -*-coding: utf-8-*-
import base64
import binascii
import cookielib
import json
import re
import sys
import urllib
import urllib2

import rsa

sys.path.append("..")


# 用于模拟登陆新浪微博
class SinaLauncher():
    def __init__(self, username, password):
        self.password = password
        self.username = username
        print 'username::',username
        print 'password::',password

    def get_prelogin_args(self):
        """
        该函数用于模拟预登录过程,并获取服务器返回的 nonce , servertime , pub_key 等信息
        """
        json_pattern = re.compile('\((.*)\)')
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&' \
              + self.get_encrypted_name() + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            raw_data = response.read().decode('utf-8')
            json_data = json_pattern.search(raw_data).group(1)
            data = json.loads(json_data)
            # print data
            return data
        except urllib2.URLError, e:
            print "%s" % e.reason
            return None

    def get_encrypted_pw(self, data):
        rsa_e = 65537  # 0x10001
        pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
        pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''  # 清空password
        passwd = binascii.b2a_hex(pw_encypted)
        # print passwd
        return passwd

    def get_encrypted_name(self):
        username_urllike = urllib2.quote(self.username)
        username_encrypted = base64.b64encode(bytes(username_urllike))
        return username_encrypted.decode('utf-8')

    def enableCookies(self):
        # 建立一个cookies 容器
        cookie_container = cookielib.CookieJar()
        # 将一个cookies容器和一个HTTP的cookie的处理器绑定
        cookie_support = urllib2.HTTPCookieProcessor(cookie_container)
        # 创建一个opener,设置一个handler用于处理http的url打开
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        # 安装opener，此后调用urlopen()时会使用安装过的opener对象
        urllib2.install_opener(opener)

    def build_post_data(self, raw):
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "useticket": "1",
            "pagerefer": "http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter"
                         "&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.14",
            "vsnf": "1",
            "su": self.get_encrypted_name(),
            "service": "miniblog",
            "servertime": raw['servertime'],
            "nonce": raw['nonce'],
            "pwencode": "rsa2",
            "rsakv": raw['rsakv'],
            "sp": self.get_encrypted_pw(raw),
            "sr": "1280*800",
            "encoding": "UTF-8",
            "prelt": "77",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META"
        }
        data = urllib.urlencode(post_data).encode('utf-8')
        return data

    def login(self):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        self.enableCookies()
        data = self.get_prelogin_args()
        post_data = self.build_post_data(data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
        }
        try:
            request = urllib2.Request(url=url, data=post_data, headers=headers)
            response = urllib2.urlopen(request)
            html = response.read().decode('GBK')
            # print html
        except urllib2.URLError as e:
            print e.reason

        p = re.compile('location\.replace\(\'(.*?)\'\)')
        p2 = re.compile(r'"userdomain":"(.*?)"')

        try:
            login_url = p.search(html).group(1)
            # print login_url
            request = urllib2.Request(login_url)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            # print page
            self.uid = re.findall('uniqueid":"(\d+)"', page)[0]

            #print self.uid
            # login_url = 'http://weibo.com/' + p2.search(page).group(1)
            # login_url = 'http://weibo.com/comment/inbox?spam=0&role=0&pids=Pl_Content_Commentlist&wvr=6'
            # print login_url
            # request = urllib2.Request(login_url)
            # response = urllib2.urlopen(request)
            # final = response.read().decode('utf-8')
            # print final
            print "Login success!"
        except:
            print 'Login error!'
            return


if __name__ == '__main__':
    test = SinaLauncher('', '')
    test.login()
    print test.uid
