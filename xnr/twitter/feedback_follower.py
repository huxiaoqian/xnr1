#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Follower():
	def __init__(self, username, password, *args):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.api = self.launcher.api()
		self.es = Es_twitter()
		self.list = []
		try:
			self.uid = uid
		except Exception as e:
			pass

	def get_follower(self):
		try:
			for each in self.api.followers(self.uid):
				name = each.name
				screen_name = each.screen_name
				id = each.id
				item = {
					'user_name':name,
					'nick_name':screen_name,
					'uid':id
				}
				self.list.append(item)
		except Exception as e:
			for each in self.api.followers():
				name = each.name
				screen_name = each.screen_name
				id = each.id
				item = {
					'user_name':name,
					'nick_name':screen_name,
					'uid':id
				}
				self.list.append(item)

		return self.list

	def save(self,indexName,typeName,list):
		for item in list:
			self.es.executeES(indexName,typeName,item)


if __name__ == '__main__':
	follower = Follower('18538728360@163.com','zyxing,0513') #传uid
	list = follower.get_follower()
	print(list)
	follower.save('twitter_feedback_fans_2017-11-13','text',list)


