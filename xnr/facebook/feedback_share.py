#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb
import re

class Share():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.es = Es_fb()
		self.list = []
		self.share_list = self.launcher.get_share_list()
	def get_share(self):
		self.driver.get(self.share_list[0])
		for ea in self.driver.find_elements_by_xpath('//div[@id="repost_view_permalink"]/div/div[1]/div'):
			for each in ea.find_elements_by_xpath('./div'):
				author_name = each.find_element_by_xpath('./div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').text
				author_id = re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').get_attribute('data-hovercard'))
				pic_url = each.find_element_by_xpath('./div/div[2]/div/div[2]/div/div/a/div/img').get_attribute('src')
				try:
					content = each.find_element_by_xpath('./div/div[2]/div/div[2]/div[2]//p').text
				except Exception as e:
					content = 'None'
				timestamp = int(each.find_element_by_xpath('./div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/a/abbr').get_attribute('data-utime'))
				item = {'nick_name':author_name,'uid':author_id,'photo_url':pic_url,'text':content,'timestamp':timestamp}
				self.list.append(item)
		return self.list
		
	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	share = Share('8618348831412','Z1290605918')
	list = share.get_share()
	share.save('facebook_feedback_retweet','text',list)
