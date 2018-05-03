#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class At():
	def get_mention():
		for each in api.mentions_timeline():
			user_screen_name = each.author.screen_name
			user_name = each.author.name
			user_id = each.author.id
			text = each.text
			user_mention_screen_name = each.entities['user_mentions'][0]['screen_name']
			user_mention_name = each.entities['user_mentions'][0]['name']
			user_mention_id = each.entities['user_mentions'][0]['id']
			time = each.created_at

			item = {
				'user_screen_name': user_screen_name,
				'user_name': user_name,
				'user_id': user_id,
				'text': text,
				'user_mention_screen_name': user_mention_screen_name,
				'user_mention_name': user_mention_name,
				'user_mention_id': user_mention_id,
				'time': time
			}

		return item
			

	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	api = Launcher('18538728360@163.com','zyxing,0513').api()
	es = Es_twitter()
	at = At()
	item = at.get_mention()
	at.save('twitter_feedback_at_2017-11-13','text',item)





