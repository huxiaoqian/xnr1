#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter


class Follower():
	def __init__(self,*args):
		try:
			self.uid = uid
		except Exception as e:
			pass

	def get_follower(self):
		try:
			for each in api.followers(uid):
				name = each.name
				screen_name = each.screen_name
				id = each.id
		except Exception as e:
			for each in api.followers():
				name = each.name
				screen_name = each.screen_name
				id = each.id
				
		item = {
			'name':name,
			'screen_name':screen_name,
			'id':id
		}

		return item

	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)


if __name__ == '__main__':
	api = Launcher('18538728360@163.com','zyxing,0513').api()
	es = Es_twitter()
	follower = Follower() #传uid
	item = follower.get_follower()
	follower.save('twitter_feedback_fans_2017-11-13','text',item)