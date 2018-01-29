#!/usr/bin/env python
# encoding: utf-8

import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from lxml import etree
import re
from pybloom import BloomFilter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from launcher import Launcher

class Operation():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()

	def publish(self, text):
		time.sleep(1)
		try:
			self.driver.find_element_by_xpath('//div[@class="_4bl9 _42n-"]').click()
		except:
			self.driver.find_element_by_xpath('//div[@class="_4bl9"]').click()
		time.sleep(2)
		try:
			self.driver.find_element_by_xpath('//textarea[@title="分享新鲜事"]').click()
			self.driver.find_element_by_xpath('//textarea[@title="分享新鲜事"]').send_keys(text)
		except:
			self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').click()
			self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').send_keys(text)
		try:
			self.driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()
		except:
			self.driver.find_element_by_xpath('//button[@class="_42ft _4jy0 _ej1 _4jy3 _4jy1 selected _51sy"]').click()

	def mention(self, username, text):
		try:
			self.driver.find_element_by_xpath('//div[@class="_4bl9 _42n-"]').click()
			time.sleep(3)
			self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').send_keys(text)
			time.sleep(1)
			self.driver.find_element_by_xpath('//table[@class="uiGrid _51mz _5f0n"]/tbody/tr[2]/td[2]/span/a/div').click()
			self.driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys(username)
			self.driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys(Keys.ENTER)
			time.sleep(1)
			self.driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()
		except Exception as e:
			print(e)

	def follow(self, uid):
		try:
			driver = self.launcher.target_page(uid)
			driver.find_element_by_xpath('//a[@class="_42ft _4jy0 _4jy4 _517h _51sy"]').click()
		except Exception as e:
			print(e)

	def not_follow(self, uid):
		try:
			driver = self.launcher.target_page(uid)
			chain = ActionChains(driver)
			implement = driver.find_element_by_xpath('//button[@class="_42ft _4jy0 _3oz- _52-0 _4jy4 _517h _51sy"]')
			chain.move_to_element(implement).perform()
			driver.find_element_by_xpath('//a[@ajaxify="/ajax/follow/unfollow_profile.php?profile_id=100022934584514&location=1"]').click()
		except Exception as e:
			print(e)

# 私信(未关注)
	def send_message(self, uid, text):
		#发送给未关注的用户
		try:
			driver = self.launcher.target_page(uid)
			message_url = 'https://www.facebook.com/messages/t/' + uid
			driver.get(message_url)
			time.sleep(5)
			driver.find_element_by_xpath('//div[@aria-label="输入消息..."]').send_keys(text)
			driver.find_element_by_xpath('//div[@aria-label="输入消息..."]').send_keys(Keys.ENTER)
		except Exception as e:
		    print(e) 

# 私信(已关注)
	def send_message2(self, uid, text):
		#发送给已关注的用户
		try:
			driver = self.launcher.target_page(uid)
			url = driver.find_element_by_xpath('//a[@class="_51xa _2yfv _3y89"]/a[1]').get_attribute('href')
			driver.get('https://www.facebook.com' + url)
			time.sleep(4)
			driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').click()
			driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(text)
			driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(Keys.ENTER)
		except Exception as e:
			print(e)

#########

# 点赞
	def like(self, uid, fid):
		post_url = 'https://www.facebook.com/' + uid + '/posts/' + fid
		video_url = 'https://www.facebook.com/' + uid + '/videos/' + fid
		self.driver.get(post_url)
		time.sleep(5)
		try:
			self.driver.find_element_by_xpath('//div[@aria-label="Facebook 照片剧场模式"]')
			self.driver.get(video_url)
			time.sleep(2)
			for each in self.driver.find_elements_by_xpath('//a[@data-testid="fb-ufi-likelink"]'):
				try:
					each.click()
				except:
					pass
		except:
			for each in self.driver.find_elements_by_xpath('//a[@data-testid="fb-ufi-likelink"]'):
				try:
					each.click()
				except:
					pass

# 评论
	def comment(self, uid, fid, text):
		post_url = 'https://www.facebook.com/' + uid + '/posts/' + fid
		video_url = 'https://www.facebook.com/' + uid + '/videos/' + fid
		self.driver.get(post_url)
		time.sleep(3)
		try:
			self.driver.find_element_by_xpath('//div[@aria-label="Facebook 照片剧场模式"]')
			self.driver.get(video_url)
			time.sleep(3)
			self.driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').click()
			time.sleep(1)
			self.driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').send_keys(text)
			self.driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').send_keys(Keys.ENTER)
		except:
			self.driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').click()
			time.sleep(1)
			self.driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').send_keys(text)
			self.driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').send_keys(Keys.ENTER)

# 分享
	def share(self, uid, fid, text):
		print 'uid, fid, text...',uid, fid, text
		post_url = 'https://www.facebook.com/' + uid + '/posts/' + fid
		video_url = 'https://www.facebook.com/' + uid + '/videos/' + fid
		self.driver.get(post_url)
		time.sleep(3)
		try:
			self.driver.find_element_by_xpath('//div[@aria-label="Facebook 照片剧场模式"]')
			self.driver.get(video_url)
			time.sleep(1)
			self.driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
			self.driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
			time.sleep(3)
			self.driver.find_element_by_xpath('//ul[@class="_54nf"]/li[2]').click()
			time.sleep(3)
			self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]').click()
			time.sleep(1)
			self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]').send_keys(text)
			time.sleep(1)
			self.driver.find_element_by_xpath('//button[@data-testid="react_share_dialog_post_button"]').click()
		except:
			self.driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
			self.driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
			time.sleep(5)
			self.driver.find_element_by_xpath('//ul[@class="_54nf"]/li[2]').click()
			time.sleep(5)
			try:
				self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]/div').click()
				time.sleep(1)
				self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]/div').send_keys(text)
				time.sleep(1)
			except:
				self.driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').click()
				time.sleep(1)
				self.driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').send_keys(text)
				time.sleep(1)
			self.driver.find_element_by_xpath('//button[@data-testid="react_share_dialog_post_button"]').click()

#添加好友
	def add_friend(self, uid):
		try:
			driver = self.launcher.target_page(uid)
			driver.find_element_by_xpath('//button[@class="_42ft _4jy0 FriendRequestAdd addButton _4jy4 _517h _9c6"]').click()
		except Exception as e:
			print(e)

#确认好友请求
	def confirm(self, uid):
		try:
			driver = self.launcher.target_page(uid)
			time.sleep(5)
			driver.find_element_by_xpath('//div[@class="incomingButton"]/button').click()
			time.sleep(1)
			driver.find_element_by_xpath('//li[@data-label="确认"]/a').click()
		except Exception,e:
			print e

#删除好友
	def delete_friend(self, uid):
		try:
			driver = self.launcher.target_page(uid)
			time.sleep(1)
			driver.find_element_by_xpath('//div[@id="pagelet_timeline_profile_actions"]/div/a').click()
			time.sleep(2)
			driver.find_element_by_xpath('//li[@data-label="删除好友"]/a').click()
		except Exception as e:
			print(e)

if __name__ == '__main__':
	operation = Operation('8618348831412','Z1290605918')
	time.sleep(1)
	#operation.confirm('100023782959440')
	#operation.like('100011257748826','475400189511902')
	#operation.comment('100011257748826','475400189511902','...')
	#operation.share('100011257748826','475400189511902','...')

