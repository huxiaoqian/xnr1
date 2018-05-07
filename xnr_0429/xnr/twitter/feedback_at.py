#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from Elasticsearch_tw import Es_twitter
import datetime
import time

class At():
	def __init__(self, username, password, consumer_key, consumer_secret, access_token, access_secret):
		self.launcher = Launcher(username, password, consumer_key, consumer_secret, access_token, access_secret)
		self.api = self.launcher.api()
		self.es = Es_twitter()
		self.list = []
		self.update_time = int(time.time())

	def get_mention(self):
		for each in self.api.mentions_timeline():
			try:
				user_screen_name = each.author.screen_name
				user_name = each.author.name
				user_id = each.author.id
				text = each.text
				user_mention_screen_name = each.entities['user_mentions'][0]['screen_name']
				user_mention_name = each.entities['user_mentions'][0]['name']
				user_mention_id = each.entities['user_mentions'][0]['id']
				timestamp = int(time.mktime(each.created_at.timetuple()))
				mid = each.id
				photo_url = each.author.profile_image_url_https

				item = {
					'uid': user_id,
					'photo_url': photo_url,
					'user_name': user_screen_name,
					'nick_name': user_name,
					'mid': mid,
					'timestamp': timestamp,
					'text': text,
					'update_time': self.update_time
				}
				self.list.append(item)
			except:
				pass
		self.launcher.display.popen.kill()
		return self.list

	def save(self, indexName, typeName, list):
		self.es.executeES(indexName,typeName, list)

if __name__ == '__main__':
	at = At('8617078448226','xnr123456', 'N1Z4pYYHqwcy9JI0N8quoxIc1', 'VKzMcdUEq74K7nugSSuZBHMWt8dzQqSLNcmDmpGXGdkH6rt7j2', '943290911039029250-yWtATgV0BLE6E42PknyCH5lQLB7i4lr', 'KqNwtbK79hK95l4X37z9tIswNZSr6HKMSchEsPZ8eMxA9')
	list = at.get_mention()
	print(list)
	#at.save('twitter_feedback_at','text',list)





