#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Share():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.driver.get('https://twitter.com/i/notifications')
		self.es = Es_twitter()
		self.lis = self.driver.find_elements_by_xpath('//li[@data-item-type="activity"]')
		self.list = []


	def get_share(self):
		for li in self.lis:
			type = li.get_attribute('data-component-context')
			if type == "quote_activity":
				user_name = li.find_element_by_xpath('./div/div[2]/div[1]/a/span[1]').text
				user_screen_name = li.find_element_by_xpath('./div/div[2]/div[1]/a/span[2]').text
				user_id = li.find_element_by_xpath('./div/div[2]/div[1]/a').get_attribute('data-user-id')
				time = li.find_element_by_xpath('./div/div[2]/div[1]/small/a/span').get_attribute('data-time')
				content = li.find_element_by_xpath('./div/div[2]/div[2]/p').text
				root_user_name = li.find_element_by_xpath('./div/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/b').text
				root_user_screen_name = li.find_element_by_xpath('./div/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/span[3]/b').text
				root_user_id = li.find_element_by_xpath('./div/div[2]/div[3]/div/div').get_attribute('data-user-id')
				root_content = li.find_element_by_xpath('./div/div[2]/div[3]/div/div[1]/div[1]/div[1]/div[2]').text

				item = {
					'user_name':user_name,
					'nick_name':user_screen_name,
					'uid':user_id,
					'update_time':time,
					'text':content,
					'root_user_name':root_user_name,
					'root_nick_name':root_user_screen_name,
					'root_uid':root_user_id,
					'root_text':root_content
				}
				self.list.append(item)

		return self.list

	def save(self,indexName,typeName,list):
		for item in list:
			self.es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	share = Share('18538728360@163.com','zyxing,0513')
	list = share.get_share()
	share.save('twitter_feedback_retweet_2017-11-13','text',list)



