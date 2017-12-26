#!/usr/bin/env python
# encoding: utf-8

from launcher import Launcher
from es import Es_twitter
from feedback_at import At
from feedback_follower import Follower
from feedback_like import Like
from feedback_message import Message
from feedback_share import Share

def execute(username, password):
	launcher = Launcher(username, password)
	driver = launcher.login()

	at = At(username, password)
	list = at.get_mention()
	at.save('twitter_feedback_at_2017-11-13','text',list)

	follower = Follower(username, password) #传uid
	list = follower.get_follower()
	follower.save('twitter_feedback_fans_2017-11-13','text',list)

	like = Like(username, password)
	list = like.get_like()
	like.save('twitter_feedback_like_2017-11-13','text',list)

	message = Message(username, password)
	list = message.get_message()
	message.save('twitter_feedback_private_2017-11-13','text',list)

	share = Share(username, password)
	list = share.get_share()
	share.save('twitter_feedback_retweet_2017-11-13','text',list)

if __name__ == '__main__':
	execute('18538728360@163.com','zyxing,0513')