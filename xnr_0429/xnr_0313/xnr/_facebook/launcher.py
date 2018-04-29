#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver

class Launcher():
	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.driver = webdriver.Firefox()
		self.driver.get('https://www.facebook.com')
		self.driver.find_element_by_xpath('//input[@id="email"]').send_keys(username)
		self.driver.find_element_by_xpath('//input[@id="pass"]').send_keys(password)
		self.driver.find_element_by_xpath('//input[@data-testid="royal_login_button"]').click()
	def login():
		# 点掉进入主页之后的提醒
		time.sleep(1)
		try:
			self.driver.find_element_by_xpath('//a[@action="cancel"]').click()
		except Exception as e:
			pass

		# 将cookie保存在req中
		req = requests.Session()
		cookies = self.driver.get_cookies()
		for cookie in cookies:
			req.cookies.set(cookie['name'],cookie['value'])
		headers = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'
		}
		return self.driver

	def get_like_list(self):
		#self.driver = self.login()
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
		return like_list

	def get_share_list(self):
		#self.driver = self.login()
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
		#self.driver = self.login()
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
		#self.driver = self.login()
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



	def target_page(self,uid):
		#uid = '100022568024116'
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
			if "scroll-done" in driver.title:
				break
			else:
				time.sleep(3)

		return self.driver


	def target_post(self):
		driver = self.target_page(uid)
		id_list = []
		content_list = []
		for each in driver.find_elements_by_xpath('//div[@class="_4-u2 mbm _4mrt _5jmm _5pat _5v3q _4-u8"]/div/div[2]/div[1]/div[2]/div[2]'):
			if not len(each.text) == 0:
				content = each.text
				content_list.append(content)
			else:
				content = 'None'
				content_list.append(content)
		for each in driver.find_elements_by_xpath('//div[@class="_4-u2 mbm _4mrt _5jmm _5pat _5v3q _4-u8"]'):
			id = each.get_attribute('id')
			id_list.append(id)
		z = zip(id_list,content_list)
		dict = dict({id,content} for id,content in z)
		return dict


