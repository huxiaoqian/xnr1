#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from Elasticsearch_tw import Es_twitter
import datetime
import time

class Message():
	def __init__(self,username, password):
		self.launcher = Launcher(username, password)
		self.api = self.launcher.api()
		self.es = Es_twitter()
		self.list = []
		self.root_uid = self.api.me()

	def get_message(self):
		for each in self.api.direct_messages():
			content = each.text
			sender_screen_name = each.sender._json['screen_name']
			sender_id = each.sender._json['id']
			timestamp = int(time.mktime(each.created_at.timetuple()))
			mid = each.id

			item = {
				'nick_name':sender_screen_name,
				'uid':sender_id,
				'text':content,
				'timestamp':timestamp,
				'root_uid':self.root_uid,
				'mid':mid
			}
			self.list.append(item)

		return self.list

	def save(self,indexName,typeName,list):
		self.es.executeES(indexName,typeName,list)

if __name__ == '__main__':
	message = Message('8617078448226','xnr123456')
	list = message.get_message()
	message.save('twitter_feedback_private','text',list)