#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from Elasticsearch_fb import Es_fb
import re

class Message():
	def __init__(self,username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.es = Es_fb()
		self.list = []
		self.update_time = int(time.time())

	def get_list(self):
		self.driver.get('https://www.facebook.com/messages/t/')
		# 退出通知弹窗进入页面
		try:
			self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
		except:
			pass

		sx_list = []
		for each in self.driver.find_elements_by_xpath('//ul[@aria-label="对话列表"]/li'):
			try:
				author_name = each.find_element_by_xpath('./div/a/div[2]/div[1]/span').text
			except:
				author_name = 'None'
			try:
				author_id = ''.join(re.findall(re.compile('row_header_id_user:(\d+)'),each.find_element_by_xpath('./div').get_attribute('id')))
			except:
				author_id = 'None'
			try:
				pic_url = each.find_element_by_xpath('./div/a/div[1]/div/div/div//img').get_attribute('src')
			except:
				pic_url = 'None'
			try:
				message_url = each.find_element_by_xpath('./div/a').get_attribute('data-href')
			except:
				message_url = False
			if message_url:
				sx_list.append({'name':author_name, 'pic':pic_url, 'message_url':message_url, 'author_id':author_id})
		return sx_list

	def get_message(self):
		try:
			sx_list = self.get_list()
			for sx in sx_list:
				self.driver.get(sx['message_url'])
				time.sleep(1)
				# 退出通知弹窗进入页面
				try:
					self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass

				for message in self.driver.find_elements_by_xpath('//div[@class="_41ud"]'):
					try:
						ymd = '-'.join([t for t in re.findall(re.compile('(\d+)年(\d+)月(\d+)日'),message.find_element_by_xpath('./div/div').get_attribute('data-tooltip-content'))[0]])
						hm = ':'.join([q for q in re.findall(re.compile('(\d+):(\d+)'),message.find_element_by_xpath('./div/div').get_attribute('data-tooltip-content'))[0]])
						messagetime = ymd + ' ' + hm + ':00'
						messageTime = int(time.mktime(time.strptime(messagetime,'%Y-%m-%d %H:%M:%S')))
					except:
						messageTime = 0

					try:
						messageId = re.findall(re.compile('"fbid:(\d+)"'),message.find_element_by_xpath('./div/div').get_attribute('participants'))[-1]
						if messageId == sx['author_id']:
							private_type = 'receive'
							text = message.text
							root_text = 'None'
						else:
							private_type = 'make'
							text = 'None'
							root_text = message.text
					except:
							private_type = 'unknown'
							text = 'None'
							root_text = 'None'
				self.list.append({'uid':sx['author_id'], 'photo_url':sx['pic'], 'nick_name':sx['name'], 'timestamp':messageTime, 'update_time':self.update_time, 'text':text, 'root_text':root_text, 'private_type':private_type})
		finally:
			self.driver.quit()
		return self.list

	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	message = Message('8618348831412','Z1290605918')
	list = message.get_message()
	print list
	# message.save('facebook_feedback_private','text',list)




