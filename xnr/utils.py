#-*-coding:utf-8-*-

from global_utils import es_user_profile,profile_index_name,profile_index_type
from parameter import MAX_SEARCH_SIZE

def nickname2uid(nickname_list):
	uids_list = set()
	query_body = {
		'query':{
			'filtered':{
				'filter':{
					'terms':{'nick_name':nickname_list}
				}
			}
		},
		'size':MAX_SEARCH_SIZE
	}

	es_results = es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,\
					body=query_body)['hits']['hits']
	print 'es_results:::',es_results
	if es_results:
		for result in es_results:
			result = result['_source']
			uid = result['uid']
			uids_list.add(uid)
	uids_list = list(uids_list)
	print 'uids_list::',uids_list
	return uids_list

def user_no2_id(user_no):
	task_id = 'WXNR'+str('%04d'%user_no)  #五位数 WXNR0001
	return task_id

def _id2user_no(task_id):
	user_no_string = filter(str.isdigit,task_id)
	print 'user_no_string::',user_no_string
	user_no = int(user_no_string)
	print 'user_no::',user_no
	return user_no