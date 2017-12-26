# -*-coding:utf-8-*-

from facebook.fb_operate import Operation

def save_to_xnr_flow_text(tweet_type,xnr_user_no,text):
    current_time = int(time.time())
    current_date = ts2datetime(current_time)
    xnr_flow_text_index_name = xnr_flow_text_index_name_pre + current_date

    item_detail = {}
    item_detail['uid'] = xnr_user_no2uid(xnr_user_no)
    item_detail['xnr_user_no'] = xnr_user_no
    item_detail['text'] = text
    item_detail['task_source'] = tweet_type
    #item_detail['topic_field'] = ''
    item_detail['mid'] = ''
    task_id = xnr_user_no + '_' + str(current_time)
    
    #classify_results = topic_classfiy(classify_mid_list, classify_text_dict)

    try:
        print 'xnr_flow_text_index_name:::',xnr_flow_text_index_name
        result = fb_xnr_flow_text_mappings(xnr_flow_text_index_name)
        print 'result::',result
        index_result = es.index(index=xnr_flow_text_index_name,doc_type=xnr_flow_text_index_type,\
                id=task_id,body=item_detail)
        print 'index_result:::',index_result
        mark = True

    except:
        mark = False

    return mark


# 发帖
def fb_publish(account_name,password,text):

	operation = Operation(account_name,password)
	operation.publish(text)

	





'''
operation = Operation('8617078448226','xnr123456')
#operation.publish('12.24 test')
#operation.mention('xerxes','12.24 test')
operation.follow('100022568024116')
#operation.not_follow('100022568024116')
#operation.like('tl_unit_-8182132709408758851','100022568024116')
#operation.comment('tl_unit_-8182132709408758851','100022568024116','12.26 test')
#operation.share('tl_unit_-8182132709408758851','100022568024116','12.26 test')
'''


