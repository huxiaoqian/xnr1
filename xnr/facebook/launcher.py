#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver
import time
import requests
import json
from pyvirtualdisplay import Display

class Launcher():
	def __init__(self, username, password):
		self.username = username
		self.password = password
		#模拟窗口
		self.display = Display(visible=0,size=(1024,768))
		self.display.start()
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.Chrome()
		self.req = requests.Session()

	def login(self):
		self.driver.get('https://www.facebook.com')
		self.driver.find_element_by_xpath('//input[@id="email"]').send_keys(self.username)
		self.driver.find_element_by_xpath('//input[@id="pass"]').send_keys(self.password)
		self.driver.find_element_by_xpath('//input[@data-testid="royal_login_button"]').click()
		# 点掉进入主页之后的提醒
		time.sleep(1)
		try:
			self.driver.find_element_by_xpath('//a[@action="cancel"]').click()
		except Exception as e:
			pass
		time.sleep(2)
		self.driver.find_element_by_xpath('//div[@data-click="home_icon"]/a').click()

		# 将cookie保存在req中
		cookies = self.driver.get_cookies()
		for cookie in cookies:
			self.req.cookies.set(cookie['name'],cookie['value'])
		headers = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'
		}
		return self.driver

	def get_like_list(self):
		self.driver.get('https://www.facebook.com/notifications')
		time.sleep(3)
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
			if "scroll-done" in self.driver.title:
				break
			else:
				time.sleep(3)
		lis = self.driver.find_elements_by_xpath('//ul[@data-testid="see_all_list"]/li')
		like_list = []
		share_list = []
		mention_list = []
		comment_list = []
		for li in lis:
			data_gt = json.loads(li.get_attribute('data-gt'))
			type = data_gt['notif_type']
			if type == "like" or type == "like_tagged" or type == "feedback_reaction_generic":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				like_list.append(url)
			if type == "story_reshare":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				share_list.append(url)
			if type == "mention" or type == "tagged_with_story":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				mention_list.append(url)
			if type == "feed_comment":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				comment_list.append(url)
		return like_list

	def get_share_list(self):
		self.driver.get('https://www.facebook.com/notifications')
		time.sleep(3)
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
			if "scroll-done" in self.driver.title:
				break
			else:
				time.sleep(3)
		lis = self.driver.find_elements_by_xpath('//ul[@data-testid="see_all_list"]/li')
		like_list = []
		share_list = []
		mention_list = []
		comment_list = []
		for li in lis:
			data_gt = json.loads(li.get_attribute('data-gt'))
			type = data_gt['notif_type']
			if type == "like" or type == "like_tagged":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				like_list.append(url)
			if type == "story_reshare":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				share_list.append(url)
			if type == "mention" or type == "tagged_with_story":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				mention_list.append(url)
			if type == "feed_comment":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				comment_list.append(url)
		return share_list


	def get_mention_list(self):
		self.driver.get('https://www.facebook.com/notifications')
		time.sleep(3)
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
			if "scroll-done" in self.driver.title:
				break
			else:
				time.sleep(3)
		lis = self.driver.find_elements_by_xpath('//ul[@data-testid="see_all_list"]/li')
		like_list = []
		share_list = []
		mention_list = []
		comment_list = []
		for li in lis:
			data_gt = json.loads(li.get_attribute('data-gt'))
			type = data_gt['notif_type']
			if type == "like" or type == "like_tagged":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				like_list.append(url)
			if type == "story_reshare":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				share_list.append(url)
			if type == "mention" or type == "tagged_with_story":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				mention_list.append(url)
			if type == "feed_comment":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				comment_list.append(url)
		return mention_list

	def get_comment_list(self):
		self.driver.get('https://www.facebook.com/notifications')
		time.sleep(3)
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
			if "scroll-done" in self.driver.title:
				break
			else:
				time.sleep(3)
		lis = self.driver.find_elements_by_xpath('//ul[@data-testid="see_all_list"]/li')
		like_list = []
		share_list = []
		mention_list = []
		comment_list = []
		for li in lis:
			data_gt = json.loads(li.get_attribute('data-gt'))
			type = data_gt['notif_type']
			if type == "like" or type == "like_tagged":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				like_list.append(url)
			if type == "story_reshare":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				share_list.append(url)
			if type == "mention" or type == "tagged_with_story":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				mention_list.append(url)
			if type == "feed_comment":
				url = li.find_element_by_xpath('./div/div/a').get_attribute('href')
				comment_list.append(url)
		return comment_list


	def target_page(self, uid):
		self.driver.get('https://www.facebook.com/'+uid)
		return self.driver

	def target_post(self, uid, fid):
		self.driver.get('https://www.facebook.com/'+uid)		
		time.sleep(3)
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
			if "scroll-done" in self.driver.title:
				break
			else:
				time.sleep(3)



if __name__ == '__main__':
	launcher = Launcher('8618348831412','Z1290605918')
	#print("login start")
	launcher.login()
	#launcher.target_page("100011257748826")
	launcher.target_post('100022568024116')

