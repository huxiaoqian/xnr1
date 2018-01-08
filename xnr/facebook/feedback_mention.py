#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb
import re

class Mention():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.mention_list = self.launcher.get_mention_list()
		self.es = Es_fb()
		self.list = []

	def get_mention(self):
		for url in self.mention_list:
			print(url)
			self.driver.get(url)
			for each in self.driver.find_elements_by_xpath('//div[@id="contentArea"]'):
				author_name = each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').text
				author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').get_attribute('data-hovercard')))
				pic_url = each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/a/div/img').get_attribute('src')
				time = each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/span/a/abbr').get_attribute('data-utime')
				try:
					content = each.find_element_by_xpath('./div/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div/div/p').text
				except Exception as e:
					content = 'None'
				item = {'nick_name':author_name,'uid':author_id,'photo_url':pic_url,'timestamp':time,'text':content}
				self.list.append(item)
		return self.list

	def save(self,indexName,typeName,list):
		for item in list:
			es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	mention = Mention('8617078448226','xnr123456')
	list = mention.get_mention()
	mention.save('facebook_feedback_at_2017-11-13','text',list)
