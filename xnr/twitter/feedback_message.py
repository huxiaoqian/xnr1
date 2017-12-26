#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter


class Message():
	def __init__(self,username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.api = self.launcher.api()
		self.es = Es_twitter()
		self.list = []

	def get_message(self):
		for each in self.api.direct_messages():
			content = each.text
			sender_screen_name = each.sender._json['screen_name']
			sender_id = each.sender._json['id']
			time = each.created_at

			item = {
				'nick_name':sender_screen_name,
				'uid':sender_id,
				'text':content,
				'timestamp':time
			}
			self.list.append(item)

		return self.list

	def save(self,indexName,typeName,list):
		for item in list:
			self.es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	message = Message('18538728360@163.com','zyxing,0513')
	list = message.get_message()
	print(list)
	message.save('twitter_feedback_private_2017-11-13','text',list)