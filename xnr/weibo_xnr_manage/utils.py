#-*- coding: utf-8 -*-
'''
use to save function about database
'''
import os
from xnr.global_utils import es_xnr,weibo_xnr_index_name,weibo_xnr_index_type


#create_weibo_xnr:create_wxnr_first
#wxnr_goal_info=[active_field,role_define,political_tendency,psychological_characteristics,business_goal]
#def create_wxnr_first(wxnr_goal_info):


#create a weibo_xnr
#input:wxnr_goal_info,wxnr_role_info,wxnr_account_info
#output:wxnr
#def create_weibo_xnr(wxnr_goal_info,wxnr_role_info,wxnr_account_info):
	#step 1: goal set
	#通过目标定制信息创建虚拟人，用flag_first标识第一步创建状态
	#if wxnr_goal_info:
		#user_id=create_wxnr_first(wxnr_goal_info)
		#flag_first=True
	#else:
		#flag_first=False

	#step 2: role create

	#step 3: attach to social account
	



#delete_weibo_xnr
def delete_weibo_xnr(user_no):
	try:
		es_xnr.delete(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=user_no)
		result='sucessful deleted'
	except:
		result='Not successful'
	return result

