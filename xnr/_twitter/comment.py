#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Comment():
	def __init__(self):
		self.driver = Launcher('18538728360@163.com','zyxing,0513').login()
		time.sleep(10)
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

	def id(slef,screen_name):
		for each in self.api.user_timeline(screen_name):
			id = each.id
			text = each.text

	def do_comment(id):
		self.driver.find_element_by_xpath('//li[@data-item-id="%s"]/div/div[2]/div[4]/div[2]/div[1]/button/div'%id).click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//div[@class="tweet-box rich-editor is-showPlaceholder"]').send_keys('11.22 test')
		time.sleep(10)
		self.driver.find_element_by_xpath('//div[@class="TweetBoxToolbar-tweetButton tweet-button"]/button[1]').click()


if __name__ == '__main__':
	comment = Comment()
	comment.do_comment('923754480524517376')