#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb

class Comment():
	def __init__(self):
		self.list = []

	def get_comment(self):
		for url in comment_list:
			driver.get(url)
			root_content = driver.find_element_by_xpath('//div[@class="_58jw"]/p').text
			root_time = driver.find_element_by_xpath('//abbr[@class="_5ptz"]').get_attribute('data-utime')
			for each in driver.find_elements_by_xpath('//div[@aria-label="评论"]'):
				author_name = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[1]/a').text
				author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[1]/a').get_attribute('data-hovercard')))
				pic_url = each.find_element_by_xpath('./div/div/div/div[1]/a/img').get_attribute('src')
				content = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div/span/span[2]/span/span/span/span').text
				time = each.find_element_by_xpath('./div/div/div/div[2]/div/div/div[2]/span[4]/a/abbr').get_attribute('data-utime')
				self.list.append({'author_name':author_name,'author_id':author_id,'pic_url':pic_url,'content':content,'time':time})
		return self.list

	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	
	fb = Launcher('18538728360','zyxing,0513')
	es = es_twitter()
	comment_list = fb.get_comment_list()
	comment = Comment()
	list = comment.get_comment()
	comment.save(list)
