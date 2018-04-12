#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver
import tweepy
from tweepy import OAuthHandler
import requests
import time
from pyvirtualdisplay import Display
from launcher import Launcher

la = Launcher('8617078448226','xnr123456')
api = la.api()

id_list = []
for num in range(1,10):
	for ecah in api.user_timeline(page=num):
		id_list.append(each.id)