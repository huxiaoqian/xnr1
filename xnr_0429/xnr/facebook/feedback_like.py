#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from Elasticsearch_fb import Es_fb
import re

class Like():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.like_list,self.driver,self.display = self.launcher.get_like_list()
		self.es = Es_fb()
		self.list = []
		self.update_time = int(time.time())

	def get_like(self):
		try:
			for url in self.like_list:
				self.driver.get(url)
				time.sleep(1)
				# 退出通知弹窗进入页面
				try:
					self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass

				try:
					text = self.driver.find_element_by_xpath('//div[@class="_5pbx userContent _22jv _3576"]').text
				except Exception as e:
					text = 'None'
				try:
					try:
						timestamp = int(self.driver.find_element_by_xpath('//abbr[@class="_5ptz"]').get_attribute('data-utime'))
					except:
						timestamp = int(self.driver.find_element_by_xpath('//abbr[@class="_5ptz timestamp livetimestamp"]').get_attribute('data-utime'))
				except:
					timestamp = 0
				try:
					mid = ''.join(re.findall(re.compile('/(\d+)'),self.driver.find_element_by_xpath('//a[@class="_5pcq"]').get_attribute('href')))
				except:
					mid = 0
				# 进入点赞列表页
				self.driver.get(self.driver.find_element_by_xpath('//a[@class="_2x4v"]').get_attribute('href'))
				time.sleep(5)
				# 退出通知弹窗进入页面
				try:
					self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				for each in self.driver.find_elements_by_xpath('//li[@class="_5i_q"]'):
					try:
						author_name = each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').text
					except:
						author_name = 'None'
					try:
						author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').get_attribute('data-hovercard')))
					except:
						author_id = 'None'
					try:
						pic_url = each.find_element_by_xpath('./div/a/div/img').get_attribute('src')
					except:
						pic_url = 'None'

					item = {'uid':author_id, 'photo_url':pic_url, 'nick_name':author_name, 'timestamp':timestamp, 'text':text, 'update_time':self.update_time, 'root_text':text, 'root_mid':mid}
					self.list.append(item)
		finally:
			self.driver.quit()
			self.display.popen.kill()
		return self.list

	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	like = Like('8618538728360','zyxing,0513')
	list = like.get_like()
	print list

	










