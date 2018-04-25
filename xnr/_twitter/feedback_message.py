#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter


class Message():
	def get_message(self):
		for each in api.direct_messages():
			content = each.text
			sender_screen_name = each.sender._json['screen_name']
			sender_id = each.sender._json['id']
			time = each.created_at

			item = {
				'screen_name':screen_name,
				'id':id,
				'content':content,
				'time':time
			}

		return item

	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	api = Launcher('18538728360@163.com','zyxing,0513').api()
	es = Es_twitter()
	message = Message()
	item = message.get_message()
	message.save('twitter_feedback_private_2017-11-13','text',item)