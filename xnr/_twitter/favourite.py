#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Retweet():
	def __init__(self):
		self.driver = Launcher('18538728360@163.com','zyxing,0513').login()
		self.driver.find_element_by_xpath('//input[@id="search-query"]').send_keys('lvleilei1')
		self.driver.find_element_by_xpath('//input[@id="search-query"]').send_keys(Keys.ENTER)
		time.sleep(10)
		self.driver.find_element_by_xpath('//ul[@class="AdaptiveFiltersBar-nav"]/li[3]/a').click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//div[@class="Grid Grid--withGutter"]/div[1]/div/div/a').click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//a[@data-nav="tweets_with_replies_toggle"]').click()
		time.sleep(10)
		self.api = Launcher('18538728360@163.com','zyxing,0513').api()

		self.id_list = []

	def id(slef,screen_name):
		for each in self.api.user_timeline(screen_name):
			id = each.id
			text = each.text
			self.id_list.append({'id':id,'text':text})
		return self.id_list

	def do_retweet(id):
		self.api.create_favorite(id)

if __name__ == '__main__':
	retweet = Retweet()
	retweet.do_retweet()