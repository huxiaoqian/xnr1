#!/usr/bin/python
#-*- coding:utf-8 -*-
from xnr.global_utils import es_xnr as es
from xnr.global_utils import weibo_date_remind_index_name,weibo_date_remind_index_type,\
							weibo_sensitive_words_index_name,weibo_sensitive_words_index_type,\
							weibo_hidden_expression_index_name,weibo_hidden_expression_index_type,\
							weibo_xnr_corpus_index_name,weibo_xnr_corpus_index_type
from xnr.time_utils import ts2datetime
from xnr.parameter import MAX_VALUE,MAX_SEARCH_SIZE




###################################################################
###################   Business Knowledge base    ##################
###################################################################

###########functional module 1: sensitive words manage  ###########

#step 1:	create sensitive words
def get_create_sensitive_words(rank,sensitive_words,create_type,create_time):
	task_detail = dict()
	task_detail['rank'] = rank
	task_detail['sensitive_words'] = sensitive_words
	task_detail['create_type'] = create_type
	task_detail['create_time'] = create_time
	task_id = sensitive_words
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
		'size':MAX_SEARCH_SIZE,
		'sort':{'create_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,body=query_body)['hits']['hits']
	results=[]
	for item in result:
		results.append(item['_source'])
	return results

#step 2.2:  show the list of sensitive words according to the condition
def show_sensitive_words_condition(create_type,rank):
    show_condition_list=[]
    if create_type and rank:
       show_condition_list.append({'term':{'create_type':create_type}})	
       show_condition_list.append({'term':{'rank':rank}})
    elif create_type:
    	show_condition_list.append({'term':{'create_type':create_type}})	
    elif rank:
    	show_condition_list.append({'term':{'rank':rank}})

    query_body={
		'query':{
			'filtered':{
				'filter':{
				    'bool':{
				        'must':show_condition_list
				        }
				    }
				
			}

		},
		'size':MAX_SEARCH_SIZE,
		'sort':{'create_time':{'order':'desc'}}
	}
	#print query_	
    if create_type or rank:
        results=es.search(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,body=query_body)['hits']['hits']
        result=[]
        for item in results:
            result.append(item['_source'])
    else:
        result=show_sensitive_words_default()
    return result


#step 3:	delete the sensitive word
def delete_sensitive_words(words_id):
	try:
		es.delete(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=words_id)
		result=True
	except:
		result=False
	return result

#step 4:	change the sensitive word

#step 4.2: change the selected sensitive word
def change_sensitive_words(words_id,change_info):
	rank=change_info[0]
	sensitive_words=change_info[1]
	create_type=change_info[2]
	create_time=change_info[3]

	try:
		es.update(index=weibo_sensitive_words_index_name,doc_type=weibo_sensitive_words_index_type,id=words_id,\
			body={"doc":{'rank':rank,'sensitive_words':sensitive_words,'create_type':create_type,'create_time':create_time}})
		result=True
	except:
		result=False
	return result


###########  functional module 2: time alert node manage #########

#step 1:	add time alert node 
def get_create_date_remind(timestamp,keywords,create_type,create_time,content_recommend):
	task_detail = dict()
	#task_detail['date_time'] = ts2datetime(int(timestamp))[5:10]
	task_detail['date_time']=timestamp[5:10]
	task_detail['keywords'] = keywords
	task_detail['create_type'] = create_type
	task_detail['create_time'] = create_time
	task_detail['content_recommend']=content_recommend

	task_id = create_time
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
	results=[]
	for item in result:
		results.append(item['_source'])
	return results

def show_date_remind_condition(create_type):
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'create_type':create_type}
				}
			}
		},
		'size':MAX_VALUE,
		'sort':{'create_time':{'order':'desc'}}
	}
	result=es.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
	results=[]
	for item in result:
		results.append(item['_source'])
	return results

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
	content_recommend=change_info[4]
	try:
		es.update(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id,\
			body={"doc":{'date_time':date_time,'keywords':keywords,'create_type':create_type,\
			'create_time':create_time,'content_recommend':content_recommend}})
		result=True
	except:
		result=False
	return result


#step 4:	delete the time alert node
def delete_date_remind(task_id):
	try:
		es.delete(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,id=task_id)
		result=True
	except:
		result=False
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
	results=[]
	for item in result:
		results.append(item['_source'])
	return results

def show_hidden_expression_condition(create_type):
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'create_type':create_type}
				}
			}
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
		result=True
	except:
		result=False
	return result

#step 4:	delete the metaphorical expression
def delete_hidden_expression(express_id):
	try:
		es.delete(index=weibo_hidden_expression_index_name,doc_type=weibo_hidden_expression_index_type,id=express_id)
		result=True
	except:
		result=False
	return result




###################################################################
###################   weibo_corpus Knowledge base    ##################
###################################################################

#step 1:create corpus
#corpus_info=[corpus_type,theme_daily_name,text,uid,mid,timestamp,retweeted,comment,like,create_type]
#subject corpus:corpus_type='主题语料'
#daily corpus:corpus_type='日常语料'
def create_corpus(corpus_info):
	corpus_detail=dict()
	corpus_detail['corpus_type']=corpus_info[0]
	corpus_detail['theme_daily_name']=corpus_info[1]
	corpus_detail['text']=corpus_info[2]
	corpus_detail['uid']=corpus_info[3]
	corpus_detail['mid']=corpus_info[4]
	corpus_detail['timestamp']=corpus_info[5]
	corpus_detail['retweeted']=corpus_info[6]
	corpus_detail['comment']=corpus_info[7]
	corpus_detail['like']=corpus_info[8]
	corpus_detail['create_type']=corpus_info[9]
	corpus_id=corpus_info[4]  #mid
	print corpus_info
	try:
		es.index(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id,body=corpus_detail)
		mark=True
	except:
		mark=False

	return mark


#step 2: show corpus
def show_corpus(corpus_type):
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'corpus_type':corpus_type}
				}
			}

		},
		'size':MAX_VALUE
	}
	result=es.search(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,body=query_body)['hits']['hits']
	return result


def show_corpus_class(create_type,corpus_type):
	query_body={
		'query':{
			'filtered':{
				'filter':{
					'term':{'corpus_type':corpus_type},
					'term':{'create_type':create_type}
				}
			}

		},
		'size':MAX_VALUE
	}
	result=es.search(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,body=query_body)['hits']['hits']
	return result

	
#step 3: change the corpus
#explain:carry out show_select_corpus before change,carry out step 3.1 & 3.2
#step 3.1: show the selected corpus
def show_select_corpus(corpus_id):
	result=es.get(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id)
	return result

#step 3.2: change the selected corpus
def change_select_corpus(corpus_id,corpus_info):
	corpus_type=corpus_info[0]
	theme_daily_name=corpus_info[1]
	text=corpus_info[2]
	uid=corpus_info[3]
	mid=corpus_info[4]
	timestamp=corpus_info[5]
	retweeted=corpus_info[6]
	comment=corpus_info[7]
	like=corpus_info[8]
	create_type=corpus_info[9]

	try:
		es.update(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id,\
			body={"doc":{'corpus_type':corpus_type,'theme_daily_name':theme_daily_name,'text':text,\
			'uid':uid,'mid':mid,'timestamp':timestamp,'retweeted':retweeted,'comment':comment,'like':like,'create_type':create_type}})
		result=True
	except:
		result=False
	return result


#step 4: delete the corpus
def delete_corpus(corpus_id):
	try:
		es.delete(index=weibo_xnr_corpus_index_name,doc_type=weibo_xnr_corpus_index_type,id=corpus_id)
		result=True
	except:
		result=False
	return result