#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from Elasticsearch_tw import Es_twitter
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

	def get_follower(self):
		try:
			for each in self.api.followers(self.uid):
				name = each.name
				screen_name = each.screen_name
				id = each.id
				root_uid = self.api.me().id
				item = {
					'user_name':name,
					'nick_name':screen_name,
					'uid':id,
					'update_time':self.update_time,
					'root_uid':root_uid
				}
				self.list.append(item)
		except Exception as e:
			for each in self.api.followers():
				name = each.name
				screen_name = each.screen_name
				id = each.id
				root_uid = self.api.me().id
				item = {
					'user_name':name,
					'nick_name':screen_name,
					'uid':id,
					'update_time':self.update_time,
					'root_uid':root_uid
				}
				self.list.append(item)
		return self.list


	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)


if __name__ == '__main__':
	current_ts = int(time.time())
	follower = Follower('18538728360@163.com','zyxing,0513',current_ts,"902921493155217409") #传uid
	
	list = follower.get_follower()
	follower.save('twitter_feedback_fans', 'text', list)


