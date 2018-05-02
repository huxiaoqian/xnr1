# -*- coding=utf-8 -*-

import re
import sys
import time
import json
import redis
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es
from global_utils import flow_text_index_name_pre,flow_text_index_type,\
						twitter_flow_text_index_name_pre,facebook_flow_text_index_name_pre
from global_config import R_BEGIN_TIME, S_TYPE
from parameter import DAY
from time_utils import ts2datetime, datetime2ts

def input_hashtag(date_time,type_ft):
	query_body = {
		'query':{
			'match_all':{}
		}
	}
	if type_ft == 'fb':
		index_name_pre = facebook_flow_text_index_name_pre
	else:
		index_name_pre = twitter_flow_text_index_name_pre

	index_name = index_name_pre + date_time
	# results = es.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

	# print 'results...',results
	es_scan = scan(es,index=index_name,doc_type=flow_text_index_type,\
					query=query_body,size=1000)

	bulk_action = []
	
	count = 0

	while 1:
		try:
			data = es_scan.next()
			_id = data['_id']
			item = data['_source']
			text = item['text']

			action = {'update':{'_id':_id}}

			if isinstance(text, str):
			    text = text.decode('utf-8', 'ignore')
			#RE = re.compile(u'#([0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
			#hashtag_list = RE.findall(text)
			RE = re.compile(u'#([0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)[ ," =.。： :、]')
			hashtag_list = re.findall(RE,text)

			if hashtag_list:
				hashtag = '&'.join(hashtag_list)
			else:
				hashtag = ''

			bulk_action.extend([{'update':{'_id':_id}}, {'doc':{'hashtag':hashtag}}])

			if count % 1000 == 0 and count != 0:
				es.bulk(bulk_action, index=index_name,doc_type=flow_text_index_type,timeout=600)
				bulk_action = []
				print count


			count += 1
		except StopIteration:
			break


	if bulk_action:
		
		print es.bulk(bulk_action, index=index_name,doc_type=flow_text_index_type,timeout=600)



date_st = '2017-10-16'
date_ed = '2017-10-25'

start_ts = datetime2ts(date_st)
end_ts = datetime2ts(date_ed)

days = (end_ts - start_ts)/DAY + 1

# for i in range(days):
# 	timestamp = start_ts + i*DAY
# 	date_time = ts2datetime(timestamp)
# 	input_hashtag(date_time,'fb')
# 	#input_hashtag(date_time,'tw')
# 	print date_time

for i in range(days):
	timestamp = start_ts + i*DAY
	date_time = ts2datetime(timestamp)
	#input_hashtag(date_time,'fb')
	input_hashtag(date_time,'tw')
	print date_time

#input_hashtag()
#es.indices.put_mapping(index='facebook_flow_text_*', doc_type=flow_text_index_type, body={"properties": {"hashtag" : {"type": "string", "index":"not_analyzed"}}})
#es.indices.put_mapping(index='twitter_flow_text_*', doc_type=flow_text_index_type, body={"properties": {"hashtag" : {"type": "string", "index":"not_analyzed"}}})
