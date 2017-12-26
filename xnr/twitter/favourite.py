#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Favourite():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.api = self.launcher.api()
		self.list = []

	def target(self, screen_name):
		self.driver.find_element_by_xpath('//input[@id="search-query"]').send_keys(screen_name)
		self.driver.find_element_by_xpath('//input[@id="search-query"]').send_keys(Keys.ENTER)
		time.sleep(10)
		self.driver.find_element_by_xpath('//ul[@class="AdaptiveFiltersBar-nav"]/li[3]/a').click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//div[@class="Grid Grid--withGutter"]/div[1]/div/div/a').click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//a[@data-nav="tweets_with_replies_toggle"]').click()
		time.sleep(10)

	def id(slef,screen_name):
		for each in self.api.user_timeline(screen_name):
			id = each.id
			text = each.text
			self.list.append({'id':id,'text':text})
		return self.list

	def do_favourite(self, id):
		self.api.create_favorite(id)

if __name__ == '__main__':
	favourite = Favourite('18538728360@163.com','zyxing,0513')
	list = favourite.id('lvleilei1')
	print(list)
	favourite.do_favourite('923754480524517376')