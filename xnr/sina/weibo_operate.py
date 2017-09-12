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
        self.uid = uid  # 当前用户id
        self.text = ''  # 内容
        self.pic_ids = ''  # 图片上传后的名字
        self.rank = 0  # 范围（公开、自己、好友圈、群）
        self.rankid = ''  # 范围群的id
        self.r_mid = ''  # 微博的id
        self.r_uid = ''  # 其他用户id
        self.cid = ''  # 回复评论中内容的id
        self.forward = '0'  # 0不转发，1转发
        self.isroot = '0'  # 0不评论，1评论
        self.group = ''  # 群名字
        self.members = ''  # 群成员id，多个用','分开

        self._headers = {
            "Headers": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;"
                       " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;"
                       " .NET4.0C; .NET4.0E; InfoPath.3)",
            "Referer": "http://weibo.com/u/%s/home?topnav=1&wvr=6" % self.uid
        }

    def __getPostURL(self, url, post_data):
        #print 'post_data:::',post_data
        #print 'url:::',url
        try:

            data = urllib.urlencode(post_data).encode('utf-8')
            #print 'data::::',data
            request = urllib2.Request(url=url, data=data, headers=self._headers)
            response = urllib2.urlopen(request, timeout=90)

            content = response.read()
            #print content
            succ = json.loads(content)
            if succ['code'] == '100000':
                print 'publish success...', succ['msg']
                return True, '成功'
            else:
                 print 'publish fail...', succ['msg']
                 return False, succ['msg']
        except:
            return False, '失败'

    def request_image_url(self, image_path):
        image_url = 'http://picupload.service.weibo.com/interface/pic_upload.php?&mime=image%2Fjpeg' \
                    '&data=base64&url=0&markpos=1&logo=&nick=0&marks=1&app=miniblog'
        print 'image_path:::',image_path
        _path = re.sub("[\[\]'\" ]", "", image_path)
        print '_path::::',_path
        img_path = _path.split(',')

        image_ids = []
        for img in img_path:
            print 'img:::',img
            try:
                b = base64.b64encode(open(img, 'rb').read())
                data = urllib.urlencode({'b64_data': b})
                # print data
                request = urllib2.Request(url=image_url, data=data, headers=self._headers)
                response = urllib2.urlopen(request, timeout=60).read()
                # print response

                m = re.search('{"code".*?}}}}', response)
                if m:
                    result = m.group()
                    image_result = json.loads(result)
                    image_id = image_result.get('data').get('pics').get('pic_1').get('pid')
                    image_ids.append(image_id)
            except:
                image_ids.append('')
                continue
        return image_ids

    def publish(self):
        """
        发布原创微博
        :param text:
        :param pic_ids:
        :param rank: 0 公开， 6好友圈， 1 自己， 7 群(需加 rankid)
        :return:
        """
        if not self.text and not self.pic_ids:
            return False

        w_url = 'http://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

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
        return self.__getPostURL(w_url, post_data)

    def retweet(self):
        """
        转发微博
        :param text:
        :param pic_ids:
        :param rank: 0 公开， 6好友圈， 1 自己， 7 群(需加 rankid)
        :param r_mid:mid=4131527589733848
        :return:
        """
        w_url = 'http://weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=%s&__rnd=%d' % (self.uid, int(time.time() * 1000))
        print w_url

        post_data = {
            "_t": "0",
            "appkey": "",
            "group_source": "group_all",
            "is_comment_base": self.forward,
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
        return self.__getPostURL(w_url, post_data)

    def comment(self):
        """
        评论微博
        :param text:
        :param r_mid:
        :return:
        """
        w_url = 'http://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

        post_data = {
            "_t": "0",
            "act": "post",
            "content": self.text,
            "forward": self.forward,
            "group_source": "group_all",
            "isroot": self.isroot,
            "location": "v6_content_home",
            "mid": self.r_mid,
            "module": "scommlist",
            "pdetail": "",
            "rid": "",
            "uid": self.uid
        }
        return self.__getPostURL(w_url, post_data)

    def receive(self):
        """
        回复微博
        :param text:
        :param cid:
        :param text:
        :param r_mid:
        :param r_uid:
        :param uid:
        :return:
        """
        w_url = 'http://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

        post_data = {
            "_t": "0",
            "act": "reply",
            "canUploadImage": "0",
            "cid": self.cid,
            "content": self.text,
            "forward": self.forward,
            "ispower": "1",
            "isroot": "0",
            "location": "",
            "mid": self.r_mid,
            "ouid": self.r_uid,
            "pdetail": "",
            "root_comment_id": "0",
            "uid": self.uid
        }
        return self.__getPostURL(w_url, post_data)

    def privmessage(self):
        """
        发布私信
        :param text:
        :param r_mid:
        :return:
        """
        w_url = 'http://weibo.com/aj/message/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

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
        return self.__getPostURL(w_url, post_data)

    def like(self):
        """
        点赞微博
        :param r_mid:
        :return:
        """
        w_url = 'http://weibo.com/aj/v6/like/add?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

        post_data = {
            "_t": "0",
            "group_source": "group_all",
            "loc": "profile",
            "location": "page_100505_home",
            "mid": self.r_mid,  # 4126115536531932
            "qid": "heart",
            "version": "mini"
        }
        return self.__getPostURL(w_url, post_data)

    def followed(self):
        """
        关注用户
        :param r_uid:
        :return:
        """
        w_url = 'http://weibo.com/aj/f/followed?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

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
        return self.__getPostURL(w_url, post_data)

    def unfollowed(self):
        """
        取关用户
        :param r_uid:
        :return:
        """
        w_url = 'http://weibo.com/aj/f/unfollow?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

        post_data = {
            "_t": "0",
            "location": "page_100505_myfollow",
            "oid": self.uid,
            "refer_flag": "",
            "refer_sort": "",
            "uid": self.r_mid
        }
        return self.__getPostURL(w_url, post_data)

    def createGroup(self):
        """
        建群（好友圈就是一个群）
        :param group:
        :param members:
        :return:
        """
        w_url = 'http://weibo.com/aj/groupchat/create?ajwvr=6&__rnd=%d' % int(time.time() * 1000)
        print w_url

        post_data = {
            "_t": "0",
            "members": self.members,
            "name": self.group
        }
        print 'members::',self.members
        print 'name::',self.group
        return self.__getPostURL(w_url, post_data)


def execute():
    """
    输入用户名、密码登录
    输入发布内容（和rank）
    :return:
    """
    xnr = SinaLauncher('', '')
    xnr.login()

    user = SinaOperateAPI(xnr.uid)
    # pics = user.request_image_url("['e:/tes33.gif', 'e:/ttest.jpg']")
    # user.pic_ids = ' '.join(pics).strip()
    # print user.pic_ids
    user.text = 'comment wei撒打算bo 434 3'
    user.r_mid = '4131527589733848'
    # user.rank = 0
    # if user.rank == 7:
    #     user.rankid = ''
    user.publish()


if __name__ == '__main__':
    execute()
