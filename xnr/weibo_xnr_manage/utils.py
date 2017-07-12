#-*- coding: utf-8 -*-
'''
use to save function about database
'''
import os
from xnr.global_utils import es_xnr,weibo_xnr_index_name,weibo_xnr_index_type


#create a weibo_xnr
#def create_weibo_xnr(weiboxnr_info):
	


#delete_weibo_xnr
def delete_weibo_xnr(user_no):
	try:
		es_xnr.delete(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=user_no)
		result='sucessful deleted'
	except:
		result='Not successful'
	return result

