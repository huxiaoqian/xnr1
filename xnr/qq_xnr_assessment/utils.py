# -*-coding:utf-8-*-

from xnr.global_config import S_TYPE,QQ_S_DATE
from xnr.global_utils import es_xnr,group_message_index_name_pre,group_message_index_type,\
					qq_xnr_index_name,qq_xnr_index_type
from xnr.time_utils import datetime2ts,ts2datetime

def get_influence_mark(xnr_user_no):

	get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']
	qq_number = get_result['qq_number']

	if S_TYPE == 'test':
		current_time = datetime2ts(QQ_S_DATE)
	else:
		current_time = int(time.time())

	#current_date = ts2datetime(current_time)
	#results = 

	return True
