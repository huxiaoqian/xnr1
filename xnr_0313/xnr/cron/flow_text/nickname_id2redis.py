# -*-coding:utf-8-*-

import os
import sys
import json
import redis
from elasticsearch.helpers import scan

sys.path.append('../../')
from global_utils import es_xnr as es,R_UNAME2ID_FT, fb_uname2id, tw_uname2id, facebook_user_index_name, \
					facebook_user_index_type, twitter_user_index_name, twitter_user_index_type

def tw2redis():
	query_body = {
		'query':{
			'match_all':{}
		}
	}

	es_scan = scan(es,index=twitter_user_index_name,doc_type=twitter_user_index_type,\
					query=query_body,size=1000)

	while 1:
		try:
			data = es_scan.next()
			item = data['_source']
			uname = item['userscreenname']
			uid = item['uid']
			R_UNAME2ID_FT.hset(tw_uname2id,uname,uid)

		except StopIteration:
			break


def fb2redis():
	query_body = {
		'query':{
			'match_all':{}
		}
	}

	es_scan = scan(es,index=facebook_user_index_name,doc_type=facebook_user_index_type,\
					query=query_body,size=1000)

	while 1:
		try:
			data = es_scan.next()
			item = data['_source']
			uid = item['uid']

			try:
				uname_1 = item['username']
				uname_2 = item['name']

			except:
				uname_1 = item['name']
				uname_2 = item['name']

			
			R_UNAME2ID_FT.hset(fb_uname2id,uname_1,uid)
			R_UNAME2ID_FT.hset(fb_uname2id,uname_2,uid)

		except StopIteration:
			break


if __name__ == '__main__':

	#tw2redis()
	#print R_UNAME2ID_FT.hget(tw_uname2id,'ArchiveDaily')
	print R_UNAME2ID_FT.hget(fb_uname2id,'xulinfree')
	#fb2redis()