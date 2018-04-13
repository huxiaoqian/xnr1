#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from Elasticsearch_tw import Es_twitter
import time

class Share():
	def __init__(self, username, password, consumer_key, consumer_secret, access_token, access_secret):
		self.launcher = Launcher(username, password, consumer_key, consumer_secret, access_token, access_secret)
		self.api = self.launcher.api()
		self.driver = self.launcher.login()
		self.driver.get('https://twitter.com/i/notifications')
		self.es = Es_twitter()
		self.lis = self.driver.find_elements_by_xpath('//li[@data-item-type="activity"]')
		self.list = []
		self.update_time = int(time.time())

	def get_share(self):
		try:
			root_uid = self.api.me().id
			for li in self.lis:
				try:
					type = li.get_attribute('data-component-context')
					if type == "quote_activity" or type == "retweet_activity":
						try:
							mid = li.get_attribute('data-item-id')
							user_name = li.find_element_by_xpath('./div/div[2]/div[1]/a/span[1]').text
							screen_name = li.find_element_by_xpath('./div/div[2]/div[1]/a').get_attribute('href').replace('https:twitter.com/','')
							photo_url = li.find_element_by_xpath('./div/div[2]//img').get_attribute('src')
							user_id = li.find_element_by_xpath('./div/div[2]/div[1]/a').get_attribute('data-user-id')
							timestamp = int(li.find_element_by_xpath('./div/div[2]/div[1]/small/a/span').get_attribute('data-time'))
							content = li.find_element_by_xpath('./div/div[2]/div[2]/p').text
							root_user_screen_name = li.find_element_by_xpath('./div/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/span[3]/b').text
							root_content = li.find_element_by_xpath('./div/div[2]/div[3]/div/div[1]/div[1]/div[1]/div[2]').text
						except:
							mid = li.get_attribute('data-item-id')
							user_name = li.find_element_by_xpath('./div/div/div/div[2]/div/a').text
							screen_name = li.find_element_by_xpath('./div/div/div/div[2]/div/a').get_attribute('href').replace('https:twitter.com/','')
							photo_url = li.find_element_by_xpath('./div/div/div/div[2]//img').get_attribute('src')
							user_id = li.find_element_by_xpath('./div/div/div/div[2]/div/a').get_attribute('data-user-id')
							timestamp = int(li.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span').get_attribute('data-time'))
							content = 'None'
							root_uid = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div').get_attribute('data-user-id')
							root_user_screen_name = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div').get_attribute('data-screen-name')
							root_content = li.find_element_by_xpath('./div/div/div/div[2]/div[2]/div/div/div/div/div/div[2]').text

						item = {
							'uid':user_id,
							'photo_url':photo_url,
							'user_name':screen_name,
							'nick_name':user_name,
							'mid':mid,
							'timestamp':timestamp,
							'text':content,
							'update_time':self.update_time,
							'root_text':root_content,
							'root_mid':mid
						}
						self.list.append(item)
				except:
					pass
		finally:
			self.driver.close()
		return self.list

	def save(self,indexName,typeName,list):
		self.es.executeES(indexName,typeName,list)

if __name__ == '__main__':
	share = Share('8617078448226', 'xnr123456', 'N1Z4pYYHqwcy9JI0N8quoxIc1', 'VKzMcdUEq74K7nugSSuZBHMWt8dzQqSLNcmDmpGXGdkH6rt7j2', '943290911039029250-yWtATgV0BLE6E42PknyCH5lQLB7i4lr', 'KqNwtbK79hK95l4X37z9tIswNZSr6HKMSchEsPZ8eMxA9')
	list = share.get_share()
	print(list)
	#share.save('twitter_feedback_retweet','text',list)



