#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class At():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.api = self.launcher.api()
		self.es = Es_twitter()
		self.list = []

	def get_mention(self):
		for each in self.api.mentions_timeline():
			user_screen_name = each.author.screen_name
			user_name = each.author.name
			user_id = each.author.id
			text = each.text
			user_mention_screen_name = each.entities['user_mentions'][0]['screen_name']
			user_mention_name = each.entities['user_mentions'][0]['name']
			user_mention_id = each.entities['user_mentions'][0]['id']
			time = each.created_at
			item = {
				'user_name': user_screen_name,
				'nick_name': user_name,
				'uid': user_id,
				'text': text,
				'user_mention_screen_name': user_mention_screen_name,
				'user_mention_name': user_mention_name,
				'user_mention_id': user_mention_id,
				'timestamp': time
			}
			self.list.append(item)
		return self.list

	def save(self, indexName, typeName, list):
		for item in list:
			self.es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	at = At('18538728360@163.com','zyxing,0513')
	list = at.get_mention()
	print(list)
	at.save('twitter_feedback_at_2017-11-13','text',list)





