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
sys.setdefaultencoding('utf-8')
from launcher import Launcher

class Operation():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()

	def publish(self, text):
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[@class="_4bl9 _42n-"]').click()
		time.sleep(4)
		#self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').click()
		self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]/div/div/div[2]/div').send_keys(text)
		self.driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()

	def mention(self, username, text):
		self.driver.find_element_by_xpath('//div[@class="_4bl9 _42n-"]').click()
		time.sleep(3)
		self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').send_keys(text)
		time.sleep(1)
		self.driver.find_element_by_xpath('//table[@class="uiGrid _51mz _5f0n"]/tbody/tr[2]/td[2]/span/a/div').click()
		self.driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys(username)
		self.driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys(Keys.ENTER)
		time.sleep(1)
		self.driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()

	def follow(self, uid):
		driver = self.launcher.target_page(uid)
		driver.find_element_by_xpath('//a[@class="_42ft _4jy0 _4jy4 _517h _51sy"]').click()

	def not_follow(self, uid):
		driver = self.launcher.target_page(uid)
		chain = ActionChains(driver)
		implement = driver.find_element_by_xpath('//button[@class="_42ft _4jy0 _3oz- _52-0 _4jy4 _517h _51sy"]')
		chain.move_to_element(implement).perform()
		driver.find_element_by_xpath('//a[@ajaxify="/ajax/follow/unfollow_profile.php?profile_id=100022934584514&location=1"]').click()

# 私信(未关注)
	def send_message(self, uid, text):
		#发送给未关注的用户
		driver = self.launcher.target_page(uid)
		try:
			url = driver.find_element_by_xpath('//div[@class="_51xa _2yfv _3y89"]/a[2]').get_attribute('href')
			#print 'message1'
		except:
			url = driver.find_element_by_xpath('//div[@class="_51xa _2yfv _3y89"]/a[1]').get_attribute('href')			
			#print 'message2'
		driver.get(url)
		time.sleep(5)
		driver.find_element_by_xpath('//div[@aria-label="输入消息..."]').send_keys(text)
		driver.find_element_by_xpath('//div[@aria-label="输入消息..."]').send_keys(Keys.ENTER)
# 私信(已关注)
	def send_message2(self, uid, text):
		#发送给已关注的用户
		driver = self.launcher.target_page(uid)
		url = driver.find_element_by_xpath('//a[@class="_51xa _2yfv _3y89"]/a[1]').get_attribute('href')
		driver.get('https://www.facebook.com' + url)
		time.sleep(4)
		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').click()
		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(text)
		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(Keys.ENTER)

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
			self.driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]/div').send_keys(text)
			self.driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]/div').send_keys(Keys.ENTER)
		except:
			self.driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').click()
			time.sleep(1)
			self.driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]/div').send_keys(text)
			self.driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]/div').send_keys(Keys.ENTER)

# 分享
	def share(self, uid, fid, text):
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
			time.sleep(3)
			self.driver.find_element_by_xpath('//ul[@class="_54nf"]/li[2]').click()
			time.sleep(3)
			self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]').click()
			time.sleep(1)
			self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]').send_keys(text)
			time.sleep(1)
			self.driver.find_element_by_xpath('//button[@data-testid="react_share_dialog_post_button"]').click()
	

# 好友
	'''
	def friends(self,uid):
		self.driver.get('https://www.facebook.com/'+ uid +'/friends')
		self.driver.execute_script("""
			(function () {
			var y = 0;
			var step = 100;
			window.scroll(0, 0);
			function f() {
			if (y < document.body.scrollHeight) {
			y += step;
			window.scroll(0, y);
			setTimeout(f, 150);
			} else {
			window.scroll(0, 0);
			document.title += "scroll-done";
			}
			}
			setTimeout(f, 1500);
			})();
			""")
		time.sleep(3)
		while True:
			if "scroll-done" in driver.title:
				break
			else:
				time.sleep(3)
		for each in driver.find_elements_by_xpath('//div[@id="contentArea"]/div/div[2]/div/div/div/div[2]/div//ul//li'):
			try:
				pic_url = each.find_element_by_xpath('./div/a/img').get_attribute('src')
				name = each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').text
				print(name)
				id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').get_attribute('data-hovercard')))
			except Exception as e:
				pass
	'''


#添加好友
	def add_friend(self, uid):
		driver = self.launcher.target_page(uid)
		driver.find_element_by_xpath('//button[@class="_42ft _4jy0 FriendRequestAdd addButton _4jy4 _517h _9c6"]').click()

#确认好友请求
	def confirm(self, uid):
		driver = self.launcher.target_page(uid)
		time.sleep(1)
		driver.find_element_by_xpath('//div[@class="incomingButton"]/button').click()
		time.sleep(1)
		driver.find_element_by_xpath('//li[@data-label="确认"]/a').click()

#删除好友
	def delete_friend(self, uid):
		driver = self.launcher.target_page(uid)
		time.sleep(1)
		driver.find_element_by_xpath('//div[@id="pagelet_timeline_profile_actions"]/div/a').click()
		time.sleep(2)
		driver.find_element_by_xpath('//li[@data-label="删除好友"]/a').click()

if __name__ == '__main__':
	operation = Operation('8618348831412','Z1290605918')
	time.sleep(1)
	#operation.confirm('100023782959440')
	#operation.like('100011257748826','475400189511902')
	#operation.comment('100011257748826','475400189511902','...')
	#operation.share('100011257748826','475400189511902','...')

