#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb
import re

class Comment():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.es = Es_fb()
		self.comment_list = self.launcher.get_comment_list()
		self.list = []

	def get_comment(self):
		for url in self.comment_list:
			self.driver.get(url)
			time.sleep(1)
			try:
				root_content = self.driver.find_element_by_xpath('//div[@role="feed"]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]').text
			except:
				root_content = self.driver.find_element_by_xpath('//div[@role="feed"]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]').text
			try:
				root_time = self.driver.find_element_by_xpath('//abbr[@class="_5ptz"]').get_attribute('data-utime')
			except:
				root_time = self.driver.find_element_by_xpath('//abbr[@class="_5ptz timestamp livetimestamp"]').get_attribute('data-utime')
			for each in self.driver.find_elements_by_xpath('//div[@aria-label="评论"]'):
				try:
					author_name = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[1]/a').text
				except:
					author_name = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[1]/a').text					
				try:
					author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[1]/a').get_attribute('data-hovercard')))
				except:
					author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[1]/a').get_attribute('data-hovercard')))					
				pic_url = each.find_element_by_xpath('./div/div/div/div[1]/a/img').get_attribute('src')
				try:
					content = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[2]/span/span/span/span').text
				except:
					content = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[2]/span/span/span/span').text					
				ti = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div[2]/span[4]/a/abbr').get_attribute('data-utime')
				self.list.append({'nick_name':author_name,'uid':author_id,'photo_url':pic_url,'text':content,'timestamp':ti})
		return self.list

	def save(self,indexName,typeName,list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	comment = Comment('8617078448226','xnr123456')
	list = comment.get_comment()
	comment.save('facebook_feedback_comment','text',list)
