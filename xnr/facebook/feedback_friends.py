#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb
import re

class Friend():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		time.sleep(2)
		self.driver.find_element_by_xpath('//a[@title="个人主页"]').click()
		time.sleep(3)
		self.driver.find_element_by_xpath('//ul[@id="u_jsonp_2_8"]/li[3]/a').click()
		time.sleep(1)
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
		self.es = Es_fb()
		self.list = []

	def get_friend(self):
		for each in self.driver.find_elements_by_xpath('//div[@class="_5h60 _30f"]//ul//li'):
			try:
				pic_url = each.find_element_by_xpath('./div/a/img').get_attribute('src')
				print(pic_url)
				name = each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').text
				print(name)
				user_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').get_attribute('data-hovercard')))
				print(user_id)
			except Exception as e:
				pass
			self.list.append({'photo_url':pic_url,'nick_name':name,'uid':user_id})
		return self.list

	def save(self, indexName, typeName, list):
		for item in list:
			self.es.executeES(indexName, typeName, item)

if __name__ == '__main__':
	friend = Friend('8617078448226','xnr123456')
	list = friend.get_friend()
	friend.save('facebook_feedback_friends','text',list)

