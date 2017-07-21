#-*- coding:utf-8 -*-
import os
import time
import json
import sys
from xnr.sina.weibo_operate import SinaOperateAPI
from xnr.tools.Launcher import SinaLauncher


## 发布微博
def publish_tweet_func(account_name,password,text,p_url,rank,rankid):

	xnr = SinaLauncher(account_name,password)
	xnr.login()
	user = SinaOperateAPI(xnr.uid)
	user.text = text
	user.rank = rank
	new_p_url = user.request_image_url(p_url)
	print 'new_p_url::',new_p_url
	user.pic_ids = ' '.join(new_p_url)
	user.rankid = rankid
	print 'user.pic_ids::',user.pic_ids
	mark = user.publish()

	return mark

## 转发微博
def retweet_tweet_func(account_name,password,text,r_mid):

	xnr = SinaLauncher(account_name,password)
	xnr.login()
	user = SinaOperateAPI(xnr.uid)
	user.text = text
	user.r_mid = r_mid
	mark = user.retweet()
	
	return mark


## 评论微博
def comment_tweet_func(account_name,password,text,r_mid):

	xnr = SinaLauncher(account_name,password)
	xnr.login()
	user = SinaOperateAPI(xnr.uid)
	user.text = text
	user.r_mid = r_mid
	mark = user.comment()

	return mark

## 私信
def private_tweet_func(account_name,password,text,r_mid):
	xnr = SinaLauncher(account_name,password)
	xnr.login()
	user = SinaOperateAPI(xnr.uid)
	user.text = text
	user.r_mid = r_mid
	mark = user.privmessage()

	return mark

## 点赞
def like_tweet_func(account_name,password,r_mid):

	xnr = SinaLauncher(account_name,password)
	xnr.login()
	user = SinaOperateAPI(xnr.uid)
	user.r_mid = r_mid
	mark = user.like()

	return mark

## 关注
def follow_tweet_func(account_name,password,uid):

	xnr = SinaLauncher(account_name,password)
	xnr.login()
	user = SinaOperateAPI(xnr.uid)
	user.r_mid = uid
	mark = user.followed()

	return mark

## 取消关注
def unfollow_tweet_func(account_name,password,uid):

	xnr = SinaLauncher(account_name,password)
	xnr.login()
	user = SinaOperateAPI(xnr.uid)
	user.r_mid = uid
	mark = user.unfollowed()

	return mark