# -*-coding:utf-8-*-
import time
import os
import json

import sys
sys.path.append('../')

from global_utils import es_xnr,group_message_index_name_pre,group_message_index_type,\
					flow_text_index_name_pre
from global_config import S_TYPE, S_DATE
#from weibo_xnr_flow_text_mappings import daily_inerests_flow_text_mappings
from time_utils import ts2datetime,datetime2ts
from parameter import MAX_VALUE,domain_en2ch_dict
from qq_xnr_groupmessage_mappings import group_message_mappings
from weibo_xnr_flow_text_mappings import weibo_xnr_flow_text_mappings

def create_mappings():
	timestamp = int(time.time())
	current_date = ts2datetime(timestamp)
	qq_number = 123  # 无效
	group_message_mappings(qq_number, current_date)
	index_name = flow_text_index_name_pre + current_date
	weibo_xnr_flow_text_mappings(index_name)

if __name__ == '__main__':
	create_mappings()

