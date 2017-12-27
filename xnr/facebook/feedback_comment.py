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
			print(url)
			self.driver.get(url)
			try:
				root_content = self.driver.find_element_by_xpath('//div[@class="_58jw"]/p').text
			except:
				root_content = self.driver.find_element_by_xpath('//div[@class="_5_jv _58jw"]/p').text
			root_time = self.driver.find_element_by_xpath('//abbr[@class="_5ptz"]').get_attribute('data-utime')
			for each in self.driver.find_elements_by_xpath('//div[@aria-label="评论"]'):
				author_name = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[1]/a').text
				author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[1]/a').get_attribute('data-hovercard')))
				pic_url = each.find_element_by_xpath('./div/div/div/div[1]/a/img').get_attribute('src')
				content = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[2]/span/span/span/span').text
				time = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div[2]/span[4]/a/abbr').get_attribute('data-utime')
				self.list.append({'nick_name':author_name,'uid':author_id,'photo_url':pic_url,'text':content,'timestamp':time})
		return self.list

	def save(self,indexName,typeName,list):
		for item in list:
			self.es.executeES(indexName, typeName, item)

if __name__ == '__main__':
	comment = Comment('18538728360@163.com','zyxing,0513')
	list = comment.get_comment()
	comment.save('facebook_feedback_comment_2017-11-13','text',list)
