#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from Elasticsearch_fb import Es_fb
import re

class Comment():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.es = Es_fb()
		self.comment_list = self.launcher.get_comment_list()
		self.list = []
		self.update_time = int(time.time())

	def get_comment(self):
		for url in self.comment_list:
			print(url)
			self.driver.get(url)
			time.sleep(1)
			# 退出通知弹窗进入页面
			try:
				self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass

			try:
				try:
					root_text = self.driver.find_element_by_xpath('//div[@role="feed"]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]').text
				except:
					root_text = self.driver.find_element_by_xpath('//div[@role="feed"]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]').text
			except:
				root_text = 'None'
			try:
				try:
					root_mid = ''.join(re.findall(re.compile('story_fbid=(\d+)'),self.driver.find_element_by_xpath('//div[@role="feed"]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/span[3]/span/a').get_attribute('href')))
				except:
					root_mid = ''.join(re.findall(re.compile('story_fbid=(\d+)'),self.driver.find_element_by_xpath('//div[@role="feed"]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/span[3]/span/a').get_attribute('href')))
			except:
				root_mid = 'None'
			for each in self.driver.find_elements_by_xpath('//div[@aria-label="评论"]'):
				try:
					try:
						author_name = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[1]/a').text
					except:
						author_name = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[1]/a').text					
				except:
					author_name = 'None'
				try:
					try:
						author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[1]/a').get_attribute('data-hovercard')))
					except:
						author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[1]/a').get_attribute('data-hovercard')))					
				except:	
					author_id = 'None'
				try:
					pic_url = each.find_element_by_xpath('./div/div/div/div[1]/a/img').get_attribute('src')
				except:
					pic_url = 'None'
				try:
					content = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/div/div/span/span[2]/span/span/span/span').text
				except:
					content = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[2]/span/span/span/span').text					
				try:
					ti = int(each.find_element_by_xpath('./div/div/div/div[2]/div/div/div[2]/span[4]/a/abbr').get_attribute('data-utime'))
				except:
					ti = int(each.find_element_by_xpath('./div/div/div/div[2]/div/div/div[2]/span[5]/a/abbr').get_attribute('data-utime'))					
				self.list.append({'uid':author_id, 'photo_url':pic_url, 'nick_name':author_name, 'mid':root_mid, 'timestamp':ti, 'text':content,\
									 'update_time':self.update_time, 'root_text':root_text, 'root_mid':root_mid})
		return self.list

	def save(self,indexName,typeName,list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	comment = Comment('8618348831412','Z1290605918')
	list = comment.get_comment()
	print list
	# comment.save('facebook_feedback_comment','text',list)
