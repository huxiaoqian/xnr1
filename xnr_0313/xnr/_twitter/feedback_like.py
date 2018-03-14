#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Like():
	def __init__(self):		
		self.driver = Launcher('18538728360@163.com','zyxing,0513').login()
		self.driver.get('https://twitter.com/i/notifications')
		self.lis = self.driver.find_elements_by_xpath('//li[@data-item-type="activity"]')


	def get_like(self):
		for li in self.lis:
			type = li.get_attribute('data-component-context')
			if type == "favorite_activity":
				user_name = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/a/strong').text
				time = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/div[1]/div/span').get_attribute('data-time')
				user_id = li.find_element_by_xpath('./div/div/div/div[2]/div[1]/a').get_attribute('data-user-id')
				root_user_name = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[1]/b').text
				root_user_screen_name = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[1]/span[3]/b').text
				root_user_id = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div').get_attribute('data-user-id')
				root_content = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[2]').text

				item = {
					'user_name':user_name,
					'time':time,
					'user_id':user_id,
					'root_user_name':root_user_name,
					'root_user_screen_name':root_user_screen_name,
					'root_user_id':root_user_id,
					'root_content':root_content
				}

		return item

	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	es = Es_twitter()
	like = Like()
	item = like.get_like()
	like.save('twitter_feedback_like_2017-11-13','text',item)









