#-*-coding:utf-8-*-

from global_utils import es_user_profile,profile_index_name,profile_index_type,\
                        es_xnr,weibo_xnr_index_name,weibo_xnr_index_type,\
                        weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type
from parameter import MAX_SEARCH_SIZE

# 保存至粉丝和关注者列表
# input: xnr_user_no--对应的虚拟人,fan_follow_uid-- 要保存的粉丝或关注者uid,
#        save_type-- 保存类型，粉丝为 'fans',关注者为 'followers'
# output: 保存是否成功
def save_to_fans_follow_ES(xnr_user_no,fan_follow_uid,save_type):
	try:
		es_results = es.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
							id=xnr_user_no)['_source']
		if save_type == 'fans':
			fans_uid_list = json.loads(es_results['fans_list'])
			if fan_follow_uid in fans_uid_list:
				mark = True
			else:
				fans_uid_list.append(fan_follow_uid)
		else:
			followers_uid_list = json.loads(es_results['followers_list'])
			if fan_follow_uid in followers_uid_list:
				mark = True
			else:
				followers_uid_list.append(fan_follow_uid)
	except:
		item = dict()
		if save_type == 'fans':
			item['fans_list'] = [fan_follow_uid]
		else:
			item['followers_list'] = [fan_follow_uid]
		try:
			es.index(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
				id=xnr_user_no,body=item)

			mark = True
		except:
			mark = False 

	return mark