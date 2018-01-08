#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter
import time
from selenium.webdriver.common.keys import Keys

class Comment():
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

	def id(self, screen_name):
		for each in self.api.user_timeline(screen_name):
			id = each.id
			text = each.text
			self.list.append({'id':id,'text':text})
		return self.list

	def do_comment(self, id, text):
		self.driver.find_element_by_xpath('//li[@data-item-id="%s"]/div/div[2]/div[4]/div[2]/div[1]/button/div'%id).click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//div[@class="tweet-box rich-editor is-showPlaceholder"]').click()
		self.driver.find_element_by_xpath('//div[@class="tweet-box rich-editor is-showPlaceholder"]').send_keys(text)
		time.sleep(10)
		self.driver.find_element_by_xpath('//button[@class="tweet-action EdgeButton EdgeButton--primary js-tweet-btn"]').click()


if __name__ == '__main__':
	comment = Comment('8617078448226','xnr123456')
	comment.target('墙裂热推')
	comment.do_comment('921048620971053056')