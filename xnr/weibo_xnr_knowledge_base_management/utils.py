# -*-utf-8-*-

from xnr.global_utils import es_xnr as es
from xnr.global_utils import weibo_date_remind_index_name,weibo_date_remind_index_type,\
							weibo_sensitive_words_index_name,weibo_sensitive_words_index_type,\
							weibo_hidden_expression_index_name,weibo_hidden_expression_index_type
from xnr.time_utils import ts2datetime
from xnr.parameter import MAX_VALUE




###################################################################
###################   Business Knowledge base    ##################
###################################################################

###########functional module 1: sensitive words manage  ###########

#step 1:	create sensitive words
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

#step 2:	show the list of sensitive words
#step 2.1:  show the list of sensitive words default
def show_sensitive_words_default():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'create_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,body=query_body)['hits']['hits']
	return result

#step 2.2:  show the list of sensitive words according to the rank
def show_sensitive_words_rank(rank_value):
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'rank':rank_value}
				}
			}

		},
		'size':MAX_VALUE,
		'sort':{'create_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,body=query_body)['hits']['hits']
	return result

#step 3:	delete the sensitive word
def delete_sensitive_words(words_id):
	try:
		es.delete(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=words_id)
		result='delete success!'
	except:
		result='delete failed!'
	return result

#step 4:	change the sensitive word
#step 4.1: show the selected sensitive word
def show_select_sensitive_words(words_id):
	result=es.get(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=words_id)
	return result

#step 3.2: change the selected sensitive word
def change_sensitive_words(words_id,change_info):
	rank=change_info[0]
	sensitive_words=change_info[1]
	create_type=change_info[2]
	create_time=change_info[3]

	try:
		es.update(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=words_id,\
			body={"doc":{'rank':rank,'sensitive_words':sensitive_words,'create_type':create_type,'create_time':create_time}})
		result='change success'
	except:
		result='change failed'
	return result


###########  functional module 2: time alert node manage #########

#step 1:	add time alert node 
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

#step 2:	show the time alert node list
def show_date_remind():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'create_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
	return result

#step 3:	change the time alert node
#explain: Carry out show_select_date_remind before change,carry out step 3.1 & 3.2
#step 3.1: show the selected time alert node
def show_select_date_remind(task_id):
	result=es.get(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)
	return result

#step 3.2: change the selected time alert node
def change_date_remind(task_id,change_info):
	date_time=change_info[0]
	keywords=change_info[1]
	create_type=change_info[2]
	create_time=change_info[3]

	try:
		es.update(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id,\
			body={"doc":{'date_time':date_time,'keywords':keywords,'create_type':create_type,'create_time':create_time}})
		result='change success'
	except:
		result='change failed'
	return result


#step 4:	delete the time alert node
def delete_date_remind(task_id):
	try:
		es.delete(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)
		result='delete success!'
	except:
		result='delete failed!'
	return result

###########		functional module 3: metaphorical expression 	###########

#step 1:	add metaphorical expression 
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

#step 2:	show the metaphorical expression list
def show_hidden_expression():
	query_body={
		'query':{
			'match_all':{}
		},
		'size':MAX_VALUE,
		'sort':{'create_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,body=query_body)['hits']['hits']
	return result

#step 3:	change the metaphorical expression
#step 3.1: show the selected hidden expression
def show_select_hidden_expression(express_id):
	result=es.get(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=express_id)
	return result

#step 3.2: change the selected hidden expression
def change_hidden_expression(express_id,change_info):
	origin_word=change_info[0]
	evolution_words_string=change_info[1]
	create_type=change_info[2]
	create_time=change_info[3]

	try:
		es.update(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=express_id,\
			body={"doc":{'origin_word':origin_word,'evolution_words_string':evolution_words_string,'create_type':create_type,'create_time':create_time}})
		result='change success'
	except:
		result='change failed'
	return result

#step 4:	delete the metaphorical expression
def delete_hidden_expression(express_id):
	try:
		es.delete(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=express_id)
		result='delete success!'
	except:
		result='delete failed!'
	return result