# -*-utf-8-*-

from xnr.global_utils import es_xnr as es
from xnr.global_utils import weibo_date_remind_index_name,weibo_date_remind_index_type,\
							weibo_sensitive_words_index_name,weibo_sensitive_words_index_type,\
							weibo_hidden_expression_index_name,weibo_hidden_expression_index_type
from xnr.time_utils import ts2datetime

def get_create_sensitive_words(rank,sensitive_words_string,create_type,create_time):
	task_detail = dict()
	task_detail['rank'] = rank
	task_detail['sensitive_words_string'] = sensitive_words_string
	task_detail['create_type'] = create_type
	task_detail['create_time'] = create_time
	task_id = sensitive_words_string
	try:
		es.index(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=task_id,body=task_detail)
		mark = True
	except:
		mark = False

	return mark

def get_create_date_remind(timestamp,keywords_string,create_type,create_time):
	task_detail = dict()
	task_detail['date_time'] = ts2datetime(int(timestamp))[5:10]
	task_detail['keywords'] = keywords_string
	task_detail['create_type'] = create_type
	task_detail['create_time'] = create_time

	task_id = ts2datetime(int(timestamp))[5:10]
	try:
		es.index(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id,body=task_detail)
		mark = True
	except:
		mark = False

	return mark

def get_create_hidden_expression(origin_word,evolution_words_string,create_type,create_time):
	task_detail = dict()
	task_detail['origin_word'] = origin_word
	task_detail['evolution_words_string'] = evolution_words_string
	task_detail['create_type'] = create_type
	task_detail['create_time'] = create_time
	task_id = origin_word
	try:
		es.index(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=task_id,body=task_detail)
		mark = True
	except:
		mark = False

	return mark
