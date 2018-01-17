#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter
import time

class Follower():
	def __init__(self, username, password, current_ts, *args):
		self.launcher = Launcher(username, password)
		self.api = self.launcher.api()
		self.es = Es_twitter()
		self.update_time = current_ts
		self.list = []
		try:
			self.uid = args[0]
		except Exception as e:
			print "no uid"

	def get_follow(self):
		try:
			for each in self.api.friends_ids(self.uid):
				id = each
				name = self.api.get_user(each).name
				screen_name = self.api.get_user(each).screen_name
				item = {
					'user_name':name,
					'nick_name':screen_name,
					'uid':id,
					'update_time':self.update_time
				}
				self.list.append(item)
		except Exception as e:
			for each in self.api.friends_ids():
				id = each
				name = self.api.get_user(each).name
				screen_name = self.api.get_user(each).screen_name
				item = {
					'user_name':name,
					'nick_name':screen_name,
					'uid':id,
					'update_time':self.update_time
				}
				self.list.append(item)
		return self.list

	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)


if __name__ == '__main__':
	current_ts = int(time.time())
	follower = Follower('8617078448226','xnr123456',current_ts,"902921493155217409") #传uid
	
	list = follower.get_follow()
	follower.save('twitter_feedback_follow', 'text', list)

