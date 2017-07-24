# -*-coding: utf-8-*-
import base64
import json
import os.path
import time
import urllib
import urllib2

import re

import sys
reload(sys)
sys.path.append('./xnr')

from tools.Launcher import SinaLauncher

class SinaOperateAPI:
    def __init__(self, uid):
        self.uid = uid
        self.text = ''
        self.pic_ids = ''
        self.rank = 0
        self.rankid = ''
        self.r_mid = ''

        self._headers = {
            "Headers": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;"
                       " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;"
                       " .NET4.0C; .NET4.0E; InfoPath.3)",
            "Referer": "http://weibo.com/u/%s/home?topnav=1&wvr=6" % self.uid
        }

    def publish(self):
        """
        发布原创微博
        :param text:
        :param pic_ids:
        :param rank: 0 公开， 6好友圈， 1 自己， 7 群(需加 rankid)
        :param rankid 
        :return:
        """
        if not self.text and not self.pic_ids:
            return False

        pub_url = 'http://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print pub_url
        post_data = self.getPostData(post_type='publish') 
        try:
            request = urllib2.Request(url=pub_url, data=post_data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            # print content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'publish success...'
                return True
            else:
                return False
        except:
            return False

    def retweet(self):
        """
        转发微博
        :param text:
        :param pic_ids:
        :param rank: 0 公开， 6好友圈， 1 自己， 7 群(需加 rankid)
        :param r_mid:mid=4131527589733848
        :return:
        """
        re_url = 'http://weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=%s&__rnd=%d' \
                % (self.uid, int(time.time() * 1000))
        print re_url
        post_data = self.getPostData(post_type='retweet')

        try:
            request = urllib2.Request(url=re_url, data=post_data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            print 'content:::',content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'retweet success...'
                return True
            else:
                return False
        except:
            return False

    def comment(self):
        """
        评论微博
        :param text:
        :param r_mid:
        :return:
        """
        com_url = 'http://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print com_url
        post_data = self.getPostData(post_type='comment')

        try:
            request = urllib2.Request(url=com_url, data=post_data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            print 'content:::',content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'comment success...'
                return True
            else:
                return False
        except:
            return False

    def privmessage(self):
        """
        发布私信
        :param text:
        :param r_mid:
        :return:
        """
        pr_url = 'http://weibo.com/aj/message/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print pr_url
        post_data = self.getPostData(post_type='private')

        try:
            request = urllib2.Request(url=pr_url, data=post_data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            # print content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'private message success...'
                return True
            else:
                return False
        except:
            return False

    def like(self):
        """
        点赞微博
        :param r_mid:
        :return:
        """
        l_url = 'http://weibo.com/aj/v6/like/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print l_url
        post_data = self.getPostData(post_type='like')
        try:
            request = urllib2.Request(url=l_url, data=post_data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            print 'content:::',content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'like success...'
                return True
            else:
                return False
        except:
            return False

    def followed(self):
        """
        关注用户
        :param r_uid:
        :return:
        """
        f_url = 'http://weibo.com/aj/f/followed?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print f_url
        post_data = self.getPostData(post_type='followed')

        try:
            request = urllib2.Request(url=f_url, data=post_data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            # print content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'followed success...'
                return True
            else:
                return False
        except:
            return False

    def unfollowed(self):
        """
        取关用户
        :param r_uid:
        :return:
        """
        un_url = 'http://weibo.com/aj/f/unfollow?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print un_url
        post_data = self.getPostData(post_type='unfollowed')
        try:
            request = urllib2.Request(url=un_url, data=post_data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            # print content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'unfollowed success...'
                return True
            else:
                return False
        except:
            return False

    def getPostData(self, post_type=None):
        if post_type == 'publish':
            post_data = {
                "_t": "0",
                "appkey": "",
                "location": "v6_content_home",
                "pdetail": "",
                "module": "stissue",
                "pic_id": self.pic_ids,
                'pubToTxt': "",
                "pub_source": "main_",
                "pub_type": "dialog",
                "rank": self.rank,
                "rankid": self.rankid,
                "style_type": "1",
                "text": self.text,
                "tid": ""
            }

        if post_type == 'retweet':
            post_data = {
                "_t": "0",
                "appkey": "",
                "group_source": "group_all",
                "location": "v6_content_home",
                "mark": "",
                "mid": self.r_mid,
                "module": "",
                "page_module_id": "",
                "pdetail": "",
                "pic_id": self.pic_ids,
                "pic_src": "",
                "rank": self.rank,
                "rankid": self.rankid,
                "reason": self.text,
                "refer_sort": "",
                "r_id": "",
                "style_type": "1"
            }

        if post_type == 'comment':
            post_data = {
                "_t": "0",
                "act": "post",
                "content": self.text,
                "forward": "0",
                "group_source": "group_all",
                "isroot": "0",
                "location": "v6_content_home",
                "mid": self.r_mid,
                "module": "scommlist",
                "pdetail": "",
                "rid": "",
                "uid": self.uid
            }

        if post_type == 'private':
            post_data = {
                "_t": "0",
                "el": "[object]",
                "fids": "",
                "location": "msgdialog",
                "module": "msgissue",
                "style_id": "1",
                "text": self.text,
                "tovfids": "",
                "uid": self.r_mid
            }

        if post_type == 'like':
            post_data = {
                "_t": "0",
                "group_source": "group_all",
                "loc": "profile",
                "location": "page_100505_home",
                "mid": self.r_mid,  # 4126115536531932
                "qid": "heart",
                "version": "mini"
            }

        if post_type == 'followed':
            post_data = {
                "_t": "0",
                "extra": "",
                "f": "1",
                "location": "myfans_v6",
                "nogroup": "false",
                "objectid": "",
                "oid": self.uid,
                "refer_flag": "1005050005_",
                "refer_sort": "followed",
                "template": "1",
                "uid": self.r_mid,
                "wforce": "1"
            }

        if post_type == 'unfollowed':
            post_data = {
                "_t": "0",
                "location": "page_100505_myfollow",
                "oid": self.uid,
                "refer_flag": "",
                "refer_sort": "",
                "uid": self.r_mid
            }
        print 'post_data::',post_data
        data = urllib.urlencode(post_data).encode('utf-8')
        print 'data::',data
        return data

    def request_image_url(self, image_path):
        image_url = 'http://picupload.service.weibo.com/interface/pic_upload.php?&mime=image%2Fjpeg' \
                    '&data=base64&url=0&markpos=1&logo=&nick=0&marks=1&app=miniblog'

        image_ids = []
        _path = re.sub("[\[\]'\" ]", "", image_path)
        img_path = _path.split(',')
        print 'img_path[0]::',img_path[0]
        print 'img_path::',img_path

        for img in img_path:
            if os.path.exists(img):

                print 'img123:',img
            try:
                print '11:',open(img, 'rb')
                print '\n'
                b = base64.b64encode(open(img, 'rb').read())
                data = urllib.urlencode({'b64_data': b})
                print 'data::::',data
                request = urllib2.Request(url=image_url, data=data, headers=self._headers)
                response = urllib2.urlopen(request, timeout=60).read()
                print response

                m = re.search('{"code".*?}}}}', response)
                if m:
                    result = m.group()
                    image_result = json.loads(result)
                    image_id = image_result.get('data').get('pics').get('pic_1').get('pid')
                    print image_id
                    image_ids.append(image_id)
            except:
                image_ids.append('')
                print '123'
                continue
        print 'image_ids::',image_ids
        return image_ids


def execute(username,password,text):
    """
    输入用户名、密码登录
    输入发布内容（和rank）
    :return:
    """
    print '123'
    #xnr = SinaLauncher('', '')
    xnr = SinaLauncher(username,password)
    xnr.login()
    print '345'

    user = SinaOperateAPI(xnr.uid)
    # pics = user.request_image_url(['e:/tes33.gif'])
    # user.pic_ids = ' '.join(pics).strip()
    # print user.pic_ids
    #user.text = 'comment weibo 434 3'
    user.text = text
    #user.r_mid = '2429014690'
    # user.rank = 0
    # if user.rank == 7:
    #     user.rankid = ''
    #user.unfollowed(r_uid)
    print '567'
    print 'text::',text
    user.publish()
    print '789'

if __name__ == '__main__':
    execute(username,password,text)
