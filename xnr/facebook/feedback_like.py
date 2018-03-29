#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from Elasticsearch_fb import Es_fb
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
			time.sleep(1)
			# 退出通知弹窗进入页面
			try:
				self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass

			try:
				root_name = self.driver.find_element_by_xpath('//span[@class="fwb"]').text
			except:
				root_name = self.driver.find_element_by_xpath('//span[@class="fwb fcg"]').text		
			try:
				id = ''.join(re.findall(re.compile('id=(\d+)'),self.driver.find_element_by_xpath('//span[@class="fwb"]/a').get_attribute('data-hovercard')))
			except:
				id = ''.join(re.findall(re.compile('id=(\d+)'),self.driver.find_element_by_xpath('//span[@class="fwb fcg"]/a').get_attribute('data-hovercard')))
			try:
				root_content = self.driver.find_element_by_xpath('//div[@class="_5pbx userContent _22jv _3576"]/p').text
			except Exception as e:
				root_content = 'None'
			try:
				timestamp = int(self.driver.find_element_by_xpath('//abbr[@class="_5ptz"]').get_attribute('data-utime'))
			except:
				timestamp = int(self.driver.find_element_by_xpath('//abbr[@class="_5ptz timestamp livetimestamp"]').get_attribute('data-utime'))
			self.driver.get(self.driver.find_element_by_xpath('//a[@class="_2x4v"]').get_attribute('href'))
			time.sleep(5)
			# 退出通知弹窗进入页面
			try:
				self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass
			for each in self.driver.find_elements_by_xpath('//li[@class="_5i_q"]'):
				author_name = each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').text
				author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').get_attribute('data-hovercard')))
				pic_url = each.find_element_by_xpath('./div/a/div/img').get_attribute('src')
				try:
					relationship = each.find_element_by_xpath('./div/div/div/div[2]/div[2]/span/div/a/span[2]/span').text
				except:
					relationship = "None"
				item = {'nick_name':author_name,'uid':author_id,'photo_url':pic_url,'facebook_type':relationship,'root_name':root_name,'id':id,'root_content':root_content,'timestamp':timestamp}
				self.list.append(item)
		return self.list

	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	# like = Like('8618348831412','Z1290605918')
	like = Like('13041233988','han8528520258')
	list = like.get_like()
	print list
	# like.save('facebook_feedback_like','text',list)

	










