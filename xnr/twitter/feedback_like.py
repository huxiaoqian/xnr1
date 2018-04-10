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
		self.update_time = int(time.time())

	def get_like(self):
		try:
			for li in self.lis:
				type = li.get_attribute('data-component-context')
				if type == "favorite_activity":
					user_name = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/a/strong').text
					screen_name = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/a').get_attribute('href').replace('https:twitter.com/','')
					timestamp = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/div[1]/div/span').get_attribute('data-time')
					user_id = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/a').get_attribute('data-user-id')
					root_user_id = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div').get_attribute('data-user-id')
					root_content = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[2]').text
					mid = li.get_attribute('data-item-id')
					photo_url = li.find_element_by_xpath('./div/div/div/div[2]//img').get_attribute('src')

					item = {
						'uid':user_id,
						'photo_url':photo_url,
						'user_name':screen_name,
						'nick_name':user_name,
						'timestamp':int(timestamp),
						'text':root_content,
						'update_time':self.update_time,
						'root_text':root_content,
						'root_mid':mid
					}
					self.list.append(item)
		finally:
			self.driver.close()
		return self.list

	def save(self,indexName,typeName,list):
		self.es.executeES(indexName,typeName,list)

if __name__ == '__main__':
	like = Like('18538728360@163.com','zyxing,0513')
	list = like.get_like()
	print(list)
	#like.save('twitter_feedback_like','text',list)









