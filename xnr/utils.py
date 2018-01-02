#-*-coding:utf-8-*-

from global_utils import es_flow_text,es_user_profile,profile_index_name,profile_index_type,\
                        es_xnr,weibo_xnr_index_name,weibo_xnr_index_type,\
                        weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                        index_sensing,type_sensing,weibo_bci_index_name_pre,weibo_bci_index_type,\
                        tw_xnr_index_name,tw_xnr_index_type,fb_xnr_index_name,fb_xnr_index_type,\
                        tw_xnr_fans_followers_index_name,tw_xnr_fans_followers_index_type,\
                        fb_xnr_fans_followers_index_name,fb_xnr_fans_followers_index_type,\
                        facebook_user_index_name,facebook_user_index_type,\
                        twitter_user_index_name, twitter_user_index_type
from parameter import MAX_SEARCH_SIZE,DAY
from global_config import S_TYPE,S_DATE_BCI
from time_utils import ts2datetime

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
    #print 'es_results:::',es_results
    if es_results:
        for result in es_results:
            result = result['_source']
            uid = result['uid']
            uids_list.add(uid)
    uids_list = list(uids_list)
    #print 'uids_list::',uids_list
    return uids_list

def uid2nick_name_photo(uid):
    uname_photo_dict = {}
    try:
        user = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
        nick_name = user['nick_name']
        photo_url = user['photo_url']
    except:
        nick_name = uid
        photo_url = ''
        
    return nick_name,photo_url

def fb_uid2nick_name_photo(uid):
    uname_photo_dict = {}
    try:
        user = es_flow_text.get(index=facebook_user_index_name,doc_type=facebook_user_index_type,id=uid)['_source']
        nick_name = user['name']
        photo_url = ''#user['photo_url']
    except:
        nick_name = uid
        photo_url = ''
        
    return nick_name,photo_url

def tw_uid2nick_name_photo(uid):
    uname_photo_dict = {}
    try:
        user = es_flow_text.get(index=twitter_user_index_name,doc_type=twitter_user_index_type,id=uid)['_source']
        nick_name = user['username']
        photo_url = user['profile_image_url_https']
    except:
        nick_name = uid
        photo_url = ''
        
    return nick_name,photo_url

def user_no2qq_id(user_no):
    task_id = 'QXNR'+str('%04d'%user_no)  #五位数 QXNR0001
    return task_id

def user_no2_id(user_no):
    task_id = 'WXNR'+str('%04d'%user_no)  #五位数 WXNR0001
    return task_id

def user_no2wxbot_id(user_no):
    task_id = 'WXXNR'+str('%04d'%user_no)  #X位数 WXXNR0001
    return task_id

def wxbot_id2user_no(task_id):
    user_no_string = filter(str.isdigit,task_id)
    user_no = int(user_no_string)
    return user_no

def _id2user_no(task_id):
    user_no_string = filter(str.isdigit,task_id)
    #print 'user_no_string::',user_no_string
    user_no = int(user_no_string)
    #print 'user_no::',user_no
    return user_no

def xnr_user_no2uid(xnr_user_no):
    try:
        result = es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
        uid = result['uid']
    except:
        uid = ''

    return uid

def fb_xnr_user_no2uid(xnr_user_no):
    try:
        result = es_xnr.get(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=xnr_user_no)['_source']
        uid = result['uid']
    except:
        uid = ''

    return uid    

def tw_xnr_user_no2uid(xnr_user_no):
    try:
        result = es_xnr.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']
        uid = result['uid']
    except:
        uid = ''

    return uid 

def uid2xnr_user_no(uid):
    try:
        query_body = {
            'query':{
                'term':{'uid':uid}
            }
        }
        result = es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no = result[0]['_source']['xnr_user_no']

    except:
        xnr_user_no = ''

    return xnr_user_no

# 保存至粉丝关注表

def save_to_fans_follow_ES(xnr_user_no,uid,save_type,follow_type,trace_type='ordinary_follow'):

    if save_type == 'followers':

        try:
            results = es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no)

            results = results["_source"]
            if follow_type == 'follow':
                if trace_type == 'trace_follow':
                    # 添加追随关注
                    try:
                        trace_follow_uids = results['trace_follow_list']
                        trace_follow_uids_set = set(trace_follow_uids)
                        trace_follow_uids_set.add(uid)
                        trace_follow_uids = list(trace_follow_uids_set)
                    except:
                        trace_follow_uids = [uid]

                    # 添加普通关注
                    try:
                        followers_uids = results['followers_list']
                        followers_uids_set = set(followers_uids)
                        followers_uids_set.add(uid)
                        followers_uids = list(followers_uids_set)
                    except:
                        followers_uids = [uid]
                    
                    results['followers_list'] = followers_uids
                    results['trace_follow_list'] = trace_follow_uids
                    es_xnr.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no,body={'doc':results})

                else:

                    try:
                        followers_uids = results['followers_list']
                        followers_uids_set = set(followers_uids)
                        followers_uids_set.add(uid)
                        followers_uids = list(followers_uids_set)
                    except:
                        followers_uids = [uid]

                    results['followers_list'] = followers_uids

                    es_xnr.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no,body={'doc':results})

            elif follow_type == 'unfollow':
                try:
                    followers_uids = results['followers_list']
                    followers_uids = list(set(followers_uids).difference(set([uid])))
                    results['followers_list'] = followers_uids

                    es_xnr.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                                id=xnr_user_no,body={'doc':results})
                except:
                    return False

        except:
            #if follow_type == 'follow':
            body_info = {}
            body_info['followers_list'] = [uid]
            body_info['xnr_use_no'] = xnr_user_no

            es_xnr.index(index=weibo_xnr_fans_followers_index_name, doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no, body=body_info)
            #elif follow_type == 'unfollow':

    elif save_type == 'fans':
        try:
            results = es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no)

            results = results["_source"]

            
            try:
                fans_uids = results['fans_list']
                fans_uids_set = set(fans_uids)
                fans_uids_set.add(uid)
                fans_uids = list(fans_uids_set)
                results['fans_list'] = fans_uids
            except:
                results['fans_list'] = [uid]

            es_xnr.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                        id=xnr_user_no,body={'doc':results})

        except:
            body_info = {}
            body_info['fans_list'] = [uid]
            body_info['xnr_use_no'] = xnr_user_no
            es_xnr.index(index=weibo_xnr_fans_followers_index_name, doc_type=weibo_xnr_fans_followers_index_type,\
                    id=xnr_user_no, body=body_info)

    return True

## 判断是否为敏感人物传感器
def judge_sensing_sensor(xnr_user_no,uid):
    
    exist_item = es_xnr.exists(index=index_sensing,doc_type=type_sensing,id=xnr_user_no)

    if not exist_item:
        return False 
    else:
        get_result = es_xnr.get(index=index_sensing,doc_type=type_sensing,id=xnr_user_no)['_source']
        
        social_sensors = get_result['social_sensors']
    
        if uid in social_sensors:
            return True
        else:
            return False

## 判断是否为重点关注人物
def judge_trace_follow(xnr_user_no,uid):

    exist_item = es_xnr.exists(index=weibo_xnr_fans_followers_index_name,\
        doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)

    if not exist_item:
        return False 
    else:
        get_result = es_xnr.get(index=weibo_xnr_fans_followers_index_name,\
            doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
        
        trace_follow_list = get_result['trace_follow_list']
    
        if uid in trace_follow_list:
            return True
        else:
            return False

## 判断关注类型
def judge_follow_type(xnr_user_no,uid):

    exist_item = es_xnr.exists(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                id=xnr_user_no)

    if not exist_item:
        weibo_type = 'stranger'
    else:
        es_get = es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
                id=xnr_user_no)['_source']

        fans_list = es_get['fans_list']
        followers_list = es_get['followers_list']

        if uid in fans_list:
            if uid in followers_list:
                weibo_type = 'friends'
            else:
                weibo_type = 'followed'
        elif uid in followers_list:
            weibo_type = 'follow'
        else:
            weibo_type = 'stranger'

    return weibo_type

## 得到影响力相对值
def get_influence_relative(uid,influence):
    if S_TYPE == 'test':
        datetime = S_DATE_BCI
    else:
        datetime = ts2datetime(time.time()-DAY)
    new_datetime = datetime[0:4]+datetime[5:7]+datetime[8:10]
    weibo_bci_index_name = weibo_bci_index_name_pre + new_datetime
    
    query_body = {
        'query':{
            'match_all':{}
        },
        'sort':{'user_index':{'order':'desc'}}
    }
    results = es_flow_text.search(index=weibo_bci_index_name,doc_type=weibo_bci_index_type,body=query_body)['hits']['hits']

    user_index_max = results[0]['_source']['user_index']

    influence_relative = influence/user_index_max

    return influence_relative

def fb_save_to_fans_follow_ES(xnr_user_no,uid,follow_type,trace_type):

 
    results = es_xnr.get(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
            id=xnr_user_no)

    results = results["_source"]
    if follow_type == 'follow':
        if trace_type == 'trace_follow':
            # 添加追随关注
            try:
                trace_follow_uids = results['trace_follow_pre_list']
                trace_follow_uids_set = set(trace_follow_uids)
                trace_follow_uids_set.add(uid)
                trace_follow_uids = list(trace_follow_uids_set)
            except:
                trace_follow_uids = [uid]

            # # 添加普通关注
            # try:
            #     followers_uids = results['followers_list']
            #     followers_uids_set = set(followers_uids)
            #     followers_uids_set.add(uid)
            #     followers_uids = list(followers_uids_set)
            # except:
            #     followers_uids = [uid]
            
            # results['followers_list'] = followers_uids
            results['trace_follow_list'] = trace_follow_uids
            es_xnr.update(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
                        id=xnr_user_no,body={'doc':results})


    elif follow_type == 'unfollow':

        try:
            followers_uids = results['trace_follow_pre_list']
            followers_uids = list(set(followers_uids).difference(set([uid])))
            results['trace_follow_pre_list'] = followers_uids

            es_xnr.update(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
                        id=xnr_user_no,body={'doc':results})
        except:
            return False

    return True


def tw_save_to_fans_follow_ES(xnr_user_no,uid,follow_type,trace_type):

 
    results = es_xnr.get(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
            id=xnr_user_no)

    results = results["_source"]
    if follow_type == 'follow':
        if trace_type == 'trace_follow':
            try:
                # 添加追随关注
                try:
                    trace_follow_uids = results['trace_follow_list']
                    trace_follow_uids_set = set(trace_follow_uids)
                    trace_follow_uids_set.add(uid)
                    trace_follow_uids = list(trace_follow_uids_set)
                except:
                    trace_follow_uids = [uid]

                # # 添加普通关注
                # try:
                #     followers_uids = results['followers_list']
                #     followers_uids_set = set(followers_uids)
                #     followers_uids_set.add(uid)
                #     followers_uids = list(followers_uids_set)
                # except:
                #     followers_uids = [uid]
                
                # results['followers_list'] = followers_uids
            
                results['trace_follow_list'] = trace_follow_uids
                es_xnr.update(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,\
                            id=xnr_user_no,body={'doc':results})
            except:
                return False


    elif follow_type == 'unfollow':

        try:
            followers_uids = results['trace_follow_pre_list']
            followers_uids = list(set(followers_uids).difference(set([uid])))
            results['trace_follow_pre_list'] = followers_uids

            es_xnr.update(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,\
                        id=xnr_user_no,body={'doc':results})
        except:
            return False

    return True


if __name__ == '__main__':

    save_to_fans_follow_ES('WXNR0004','1496814565','followers')
    #es_xnr.delete(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
    #    id='AV4Zi0NasTFJ_K1Z2dDy')