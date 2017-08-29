# -*- coding: utf-8 -*-

from global_utils import es_xnr,weibo_xnr_save_like_index_name,weibo_xnr_save_like_index_type


#保存点赞操作-虚拟人点赞别人
#input:like_info=[uid,photo_url,nick_name,mid,timestamp,text,root_mid,root_uid,weibo_type,update_time]
#output:mark=True/False
def save_xnr_like(like_info):
	like_detail=dict()
	like_detail['uid']=like_info[0]
	like_detail['photo_url']=like_info[1]
	like_detail['nick_name']=like_info[2]
	like_detail['mid']=like_info[3]
	like_detail['timestamp']=like_info[4]
	like_detail['text']=like_info[5]
	like_detail['root_mid']=like_info[6]
	like_detail['root_uid']=like_info[7]
	like_detail['weibo_type']=like_info[8]
	like_detail['update_time']=like_info[9]

	like_id=like_info[3]

	try:
		es_xnr.index(index=weibo_xnr_save_like_index_name,doc_type=weibo_xnr_save_like_index_type,id=like_id,body=like_detail)
		mark=True
	except:
		mark=False
	return mark

