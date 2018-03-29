# -*- coding:utf-8 -*-

'''
weibo community function 
'''
import sys
import json
import time,datetime
from xnr.time_utils import ts2datetime,datetime2ts,ts2date
from xnr.global_utils import es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                             es_user_profile,profile_index_name,profile_index_type,\
                             es_xnr
                             

from xnr.parameter import DAY,MAX_SEARCH_SIZE
from xnr.global_config import S_TYPE,S_DATE




################主功能函数
#跟踪社区
def show_trace_community(xnr_user_no,now_time):
	return True


#新社区
def show_new_community(xnr_user_no,now_time):
	return True



#社区预警
def get_community_warning(xnr_user_no,community_id):
	return True


# 社区详情
def get_community_detail(now_time,community_id):
	return True
