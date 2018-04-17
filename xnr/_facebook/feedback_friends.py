#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb

class Friend():
	def __init__(self):
		self.fb = Launcher('18538728360','zyxing,0513')
		self.driver = self.fb.login()
		self.driver.find_element_by_xpath('//a[@title="个人主页"]').click()
		time.sleep(1)
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

		self.list = []

	def get_friend(self):
		for each in driver.find_elements_by_xpath('//div[@class="_5h60 _30f"]//ul//li'):
			try:
				pic_url = each.find_element_by_xpath('./div/a/img').get_attribute('src')
				name = each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').text
				id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').get_attribute('data-hovercard')))
			except Exception as e:
				pass
			self.list.append({'pic_url':pic_url,'name':name,'id':id})
		return self.list

