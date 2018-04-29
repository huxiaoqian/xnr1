# -*- coding=utf-8 -*-

import re
import sys
import time
import json
import redis
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es,es_flow_text
from global_utils import flow_text_index_name_pre,flow_text_index_type
from global_config import R_BEGIN_TIME, S_TYPE
from parameter import DAY
from time_utils import ts2datetime, datetime2ts

def input_hashtag(index_pos):
	query_body = {
		'query':{
			'match_all':{}
		}
	}
	index_name = flow_text_index_name_pre + index_pos
	# results = es_flow_text.search(index=index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']

	# print 'results...',results
	es_scan = scan(es_flow_text,index=index_name,doc_type=flow_text_index_type,\
					query=query_body,size=500)

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
			RE = re.compile(u'#([0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
			hashtag_list = RE.findall(text)

			if hashtag_list:
				hashtag = '&'.join(hashtag_list)
			else:
				hashtag = ''

			bulk_action.extend([{'update':{'_id':_id}}, {'doc':{'hashtag':hashtag}}])

			if count % 500 == 0 and count != 0:
				es_flow_text.bulk(bulk_action, index=index_name,doc_type=flow_text_index_type,timeout=800)
				bulk_action = []
				print count


			count += 1
		except StopIteration:
			break


	if bulk_action:
		
		print es_flow_text.bulk(bulk_action, index=index_name,doc_type=flow_text_index_type,timeout=800)


date_st = '2016-11-08'
date_ed = '2016-11-27'

start_ts = datetime2ts(date_st)
end_ts = datetime2ts(date_ed)

days = (end_ts - start_ts)/DAY + 1

for i in range(days):
	timestamp = start_ts + i*DAY
	date_time = ts2datetime(timestamp)
	input_hashtag(date_time)
	print date_time


#input_hashtag()
#es_flow_text.indices.put_mapping(index='flow_text_*', doc_type=flow_text_index_type, body={"properties": {"hashtag" : {"type": "string", "index":"not_analyzed"}}})


