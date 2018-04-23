#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Share():
	def __init__(self):		
		self.driver = Launcher('18538728360@163.com','zyxing,0513').login()
		self.driver.get('https://twitter.com/i/notifications')
		self.lis = self.driver.find_elements_by_xpath('//li[@data-item-type="activity"]')


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
					'user_screen_name':user_screen_name,
					'user_id':user_id,
					'time':time,
					'content':content,
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
	share = Share()
	item = share.get_share()
	share.save('twitter_feedback_retweet_2017-11-13','text',item)



