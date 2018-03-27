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
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from launcher import Launcher

#fb = Launcher('18538728360','zyxing,0513')


#280312322476555/feed?message="test"&access_token=
class Operation():
	def __init__(self):
		self.launcher = Launcher('18538728360','zyxing,0513')
		self.driver = self.launcher.login()

	def publish(self):
		self.driver.find_element_by_xpath('//div[@class="_4bl9 _42n-"]').click()
		time.sleep(2)
		self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').send_keys('测试消息3')
		self.driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()

	def mention(self):
		self.driver.find_element_by_xpath('//div[@class="_4bl9 _42n-"]').click()
		time.sleep(3)
		self.driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').send_keys('测试消息4')
		time.sleep(1)
		self.driver.find_element_by_xpath('//table[@class="uiGrid _51mz _5f0n"]/tbody/tr[2]/td[2]/span/a/div').click()
		self.driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys('xerxes zhang')
		self.driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys(Keys.ENTER)
		time.sleep(1)
		self.driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()

	def follow(self):
		driver = self.launcher.target_page()
		driver.find_element_by_xpath('//a[@class="_42ft _4jy0 _4jy4 _517h _51sy"]').click()

	def not_follow(self):
		driver = self.launcher.target_page()
		chain = ActionChains(driver)
		implement = driver.find_element_by_xpath('//button[@class="_42ft _4jy0 _3oz- _52-0 _4jy4 _517h _51sy"]')
		chain.move_to_element(implement).perform()
		driver.find_element_by_xpath('//a[@ajaxify="/ajax/follow/unfollow_profile.php?profile_id=100022568024116&location=1"]').click()

# 私信(未关注)
	def send_message(self):
		#发送给未关注的用户
		driver = self.launcher.target_page()
		url = driver.find_element_by_xpath('//a[@class="_51xa _2yfv _3y89"]/a[2]').get_attribute('href')
		driver.get('https://www.facebook.com' + url)
		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys('test')
		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(Keys.ENTER)
# 私信(已关注)
	def send_message2(self):
		#发送给已关注的用户
		driver = self.launcher.target_page()
		url = driver.find_element_by_xpath('//a[@class="_51xa _2yfv _3y89"]/a[1]').get_attribute('href')
		driver.get('https://www.facebook.com' + url)
		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys('test')
		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(Keys.ENTER)

# 测试id
#id = 'tl_unit_-8182132709408758851'

	def like(self, id):
		driver = self.launcher.target_page()
		driver.find_element_by_xpath('//div[@id="%s"]/div/div[2]/div[2]/form/div[1]/div[1]/div/div[1]/div/div/div/span[1]/div/a'%id).click()


	def comment(self, id):
		driver = self.launcher.target_page()
		driver.find_element_by_xpath('//div[@id="%s"]/div/div[2]/div[2]/form/div[2]/div/div[2]/div/div[2]/div/div/div/div/div'%id).click()
		driver.find_element_by_xpath('//div[@id="%s"]/div/div[2]/div[2]/form/div[2]/div/div[2]/div/div[2]/div/div/div/div/div'%id).send_keys('test comment')
		driver.find_element_by_xpath('//div[@id="%s"]/div/div[2]/div[2]/form/div[2]/div/div[2]/div/div[2]/div/div/div/div/div'%id).send_keys(Keys.ENTER)

# 分享
	def share(self):
		driver = self.launcher.target_page()
		#action_chains = ActionChains(driver)
		driver.find_element_by_xpath('//div[@id="%s"]/div/div[2]/div[2]/form/div[1]/div[1]/div/div[1]/div/div/div/span[3]//span'%id).click()
		time.sleep(3)
		driver.find_element_by_xpath('//div[@id="%s"]/div/div[2]/div[2]/form/div[1]/div[1]/div/div[1]/div/div/div/span[3]/div/span'%id).click()
		#action_chains.key_down(Keys.CONTROL).click(el)
		#driver.find_element_by_xpath('//div[@id="%s"]/div/div[2]/div[2]/form/div[1]/div[1]/div/div[1]/div/div/div/span[3]/div/span'%id).click()
		time.sleep(3)
		driver.find_element_by_xpath('//ul[@class="_54nf"]/li[2]').click()
		time.sleep(8)
		driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]').click()
		driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]/div/div/div').send_keys('test')
		time.sleep(3)
		driver.find_element_by_xpath('//button[@data-testid="react_share_dialog_post_button"]').click()


# 好友
	def friends(self,uid):
		uid = '100022568024116'
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
				id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').get_attribute('data-hovercard')))
			except Exception as e:
				pass





