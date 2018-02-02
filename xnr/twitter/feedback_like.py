#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from Elasticsearch_tw import Es_twitter
import time

class Like():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)	
		self.driver = self.launcher.login()
		self.es = Es_twitter()
		self.api = self.launcher.api()
		self.driver.get('https://twitter.com/i/notifications')
		time.sleep(2)
		self.lis = self.driver.find_elements_by_xpath('//li[@data-item-type="activity"]')
		self.list = []

	def get_like(self):
		for li in self.lis:
			type = li.get_attribute('data-component-context')
			if type == "favorite_activity":
				user_name = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/a/strong').text
				timestamp = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/div[1]/div/span').get_attribute('data-time')
				user_id = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/a').get_attribute('data-user-id')
				root_user_name = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[1]/b').text
				root_user_screen_name = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[1]/span[3]/b').text
				root_user_id = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div').get_attribute('data-user-id')
				root_content = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[2]').text

				item = {
					'nick_name':user_name,
					'timestamp':int(timestamp),
					'uid':user_id,
					'root_user_name':root_user_name,
					'root_nick_name':root_user_screen_name,
					'root_uid':root_user_id,
					'root_text':root_content
				}
				self.list.append(item)

		return self.list

	def save(self,indexName,typeName,list):
		self.es.executeES(indexName,typeName,list)

if __name__ == '__main__':
	like = Like('8617078448226','xnr123456')
	list = like.get_like()
	like.save('twitter_feedback_like','text',list)









