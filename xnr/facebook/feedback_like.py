#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb
import re

class Like():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.like_list = self.launcher.get_like_list()
		self.es = Es_fb()
		self.list = []

	def get_like(self):
		for url in self.like_list:
			self.driver.get(url)
			root_name = self.driver.find_element_by_xpath('//span[@class="fwb"]').text
			print(root_name)
			id = ''.join(re.findall(re.compile('id=(\d+)'),self.driver.find_element_by_xpath('//span[@class="fwb"]/a').get_attribute('data-hovercard')))
			print(id)
			try:
				root_content = self.driver.find_element_by_xpath('//div[@class="_58jw"]/p').text
			except Exception as e:
				root_content = 'None'
			print(root_content)
			self.driver.get(self.driver.find_element_by_xpath('//a[@class="_2x4v"]').get_attribute('href'))
			time.sleep(10)
			for each in self.driver.find_elements_by_xpath('//li[@class="_5i_q"]'):
				author_name = each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').text
				print(author_name)
				author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').get_attribute('data-hovercard')))
				print(author_id)
				pic_url = each.find_element_by_xpath('./div/a/div/img').get_attribute('src')
				print(pic_url)
				try:
					relationship = each.find_element_by_xpath('./div/div/div/div[2]/div[2]/span/div/a/span[2]/span').text
				except:
					relationship = "None"
				print(relationship)
				item = {'nick_name':author_name,'uid':author_id,'photo_url':pic_url,'facebook_type':relationship}
				self.list.append(item)
		return self.list

	def save(self,indexName,typeName,list):
		for item in list:
			self.es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	like = Like('8617078448226','xnr123456')
	list = like.get_like()
	like.save('facebook_feedback_like_2017-11-13','text',list)

	










