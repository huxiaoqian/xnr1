#-*- coding:utf-8 -*-
import os
import time
import json
import sys
from xnr.global_utils import es_xnr as es
from xnr.global_utils import xnr_flow_text_index_name_pre,xnr_flow_text_index_type
from xnr.time_utils import ts2datetime

def save_to_xnr_flow_text(tweet_type,xnr_user_no,text):
	current_time = int(time.time())
	current_date = ts2datetime(current_time)
	xnr_flow_text_index_name = xnr_flow_text_index_name_pre + current_date

	item_detail = {}
	item_detail['xnr_user_no'] = xnr_user_no
	item_detail['text'] = text
	item_detail['tweet_type'] = tweet_type
	task_id = xnr_user_no + '_' + str(current_time)
	try:
		es.index(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,\
				id=task_id,body=item_detail)
		mark = True

	except:
		mark = False

	return mark
