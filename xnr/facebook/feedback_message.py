#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb

class Message():
	def __init__(self,username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.es = Es_fb()
		self.list = []

	def get_list(self):
		self.driver.get('https://www.facebook.com/messages/t/')
		sx_list = []
		for each in self.driver.find_elements_by_xpath('//ul[@aria-label="对话列表"]/li'):
			author_name = each.find_element_by_xpath('./div/a/div[2]/div[1]/span').text
			pic_url = each.find_element_by_xpath('./div/a/div[1]/div/div/div/img').get_attribute('src')
			message_url = each.find_element_by_xpath('./div/a').get_attribute('data-href')
			sx_list.append({'name':author_name,'pic':pic_url,'message_url':message_url})
		return sx_list

	def get_message(self):
		sx_list = self.get_list()
		for sx in sx_list:
			#print(sx['name'])
			self.driver.get(sx['message_url'])
			time.sleep(1)
			for message in self.driver.find_elements_by_xpath('//div[@class="_41ud"]'):
				try:
					mes = message.find_element_by_xpath('./div/div/div/span').text
				except Exception as e:
					mes = 'None'
			self.list.append({'nick_name':sx['name'],'text':mes})
		return self.list

	def save(self,indexName,typeName,item):
		self.es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	message = Message('18538728360','zyxing,0513')
	list = message.get_message()
	message.save('facebook_feedback_private_2017-11-13','text',list)




