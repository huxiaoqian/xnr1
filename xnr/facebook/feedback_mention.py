#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from Elasticsearch_fb import Es_fb
import re

class Mention():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.mention_list = self.launcher.get_mention_list()
		self.es = Es_fb()
		self.list = []
		self.update_time = int(time.time())

	def get_mention(self):
		for url in self.mention_list:
			self.driver.get(url)
			time.sleep(1)
			# 退出通知弹窗进入页面
			try:
				self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass

			for each in self.driver.find_elements_by_xpath('//div[@id="contentArea"]'):
				try:
					try:
						author_name = each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').text
					except:
						author_name = each.find_element_by_xpath('./div/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').text					
				except:
					author_name = 'None'
				try:
					try:
						author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').get_attribute('data-hovercard')))
					except:
						author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').get_attribute('data-hovercard')))					
				except:
					author_id = 'None'
				try:
					try:
						pic_url = each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/a/div/img').get_attribute('src')
					except:
						pic_url = each.find_element_by_xpath('./div/div/div/div/div/div/div[2]/div/div[2]/div/div/a/div/img').get_attribute('src')					
				except:
					pic_url = 'None'
				try:
					try:
						ti = int(each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/span/a/abbr').get_attribute('data-utime'))
					except:
						ti = int(each.find_element_by_xpath('./div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/a/abbr').get_attribute('data-utime'))					
				except:
					ti = 'None'
				try:
					content = each.find_element_by_xpath('./div/div/div/div/div/div/div[2]/div/div[2]/div[2]/p').text
				except:
					content = 'None'
				try:
					try:
						mid = ''.join(re.findall(re.compile('/(\d+)'),each.find_element_by_xpath('./div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/span/a').get_attribute('href')))
					except:
						mid = ''.join(re.findall(re.compile('/(\d+)'),each.find_element_by_xpath('./div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/a').get_attribute('href')))		
				except:
					mid = 'None'
				item = {'uid':author_id, 'photo_url':pic_url, 'nick_name':author_name, 'mid':mid, 'timestamp':ti, 'text':content, 'update_time':self.update_time}
				self.list.append(item)
		return self.list

	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	mention = Mention('8618348831412','Z1290605918')
	list = mention.get_mention()
	print(list)