# -*- coding: utf-8 -*-
import os
import json
import time
import sys

sys.path.append('../../')
from textrank4zh import TextRank4Keyword, TextRank4Sentence

from parameter import MIN_COMMUNITY_NUM,MAX_COMMUNITY_NUM,COMMUNITY_DENSITY_CLUSTER,\
                      MIN_MEAN_COMMUNITY_SENSITIVE,MIN_MEAN_COMMUNITY_INFLUENCE,\
                      MAX_SELECT_COMMUNITY_NUM,COMMUNITY_SIMILARITY

from parameter import DAY

from time_utils import ts2datetime,datetime2ts,get_flow_text_index_list

from global_config import S_TYPE,R_BEGIN_TIME,S_DATE,WEIBO_COMMUNITY_DATE

from global_utils import es_xnr,weibo_trace_community_index_name_pre,weibo_trace_community_index_type,\
                         weibo_community_index_name_pre,weibo_community_index_type,\
                         es_user_profile,profile_index_name,profile_index_type,\
                         es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                         es_retweet,retweet_index_name_pre,retweet_index_type,\
                         be_retweet_index_name_pre,be_retweet_index_type,\
                         es_comment,comment_index_name_pre,comment_index_type,\
                         be_comment_index_name_pre,be_comment_index_type

r_beigin_ts = datetime2ts(R_BEGIN_TIME)

sys.path.append('../../timed_python_files/community/')
from weibo_publicfunc import get_compelete_wbxnr

GROUP_ITER_COUNT = 100

#思路：
#step1:读取该周期生成的json文件，根据指标筛选社区<=20个
#step2:新旧社区对比，预警判断-预警次数计算（考虑生成预警文件或者在trace中记录），强制跟踪判断，特征更新，存储至detail_community

#读取虚拟人的社区
def get_xnr_community(xnr_user_no,date_time):
    file_name = './weibo_data/' + xnr_user_no + '_' + ts2datetime(date_time) + '_' +'save_com.json'
    file_community = open(file_name,'r')
    community_list = file_community.readlines()
    #print 'community:',type(community_list)
    return community_list


#根据社区指标对生成社区进行筛选：
def get_first_select_result(create_communitylist):
    first_select_community = []
    for community in create_communitylist:
        community = json.loads(community)

        #根据社区人数进行筛选
        if community['num'] > MIN_COMMUNITY_NUM and community['num'] < MAX_COMMUNITY_NUM:
            num_mark = True
            print 'num_community::',community['num']
        else:
            num_mark = False

        #根据社区紧密程度进行筛选
        if community['cluster'] > COMMUNITY_DENSITY_CLUSTER or community['density'] > COMMUNITY_DENSITY_CLUSTER:
            cluster_density_mark = True
            print 'cluster_density::',community['cluster'],community['density']
        else:
            cluster_density_mark = False

        #根据社区影响力和敏感度进行筛选
        if community['mean_sensitive'] > MIN_MEAN_COMMUNITY_SENSITIVE:
            mean_sensitive_mark = True
            print 'mean_sensitive::',community['mean_sensitive']
        else:
            mean_sensitive_mark = False

        if community['mean_influence'] > MIN_MEAN_COMMUNITY_INFLUENCE:
            mean_influence_mark = True
            print 'mean_influence::',community['mean_influence']
        else:
            mean_influence_mark = False

        if num_mark and cluster_density_mark and (mean_sensitive_mark or mean_influence_mark):
            first_select_community.append(community)
        else:
            pass

    return first_select_community


#跟踪社区在跟踪周期内的指标阈值范围信息，若没有跟踪社区则适当提高指标阈值
def get_xnr_trace_community_detail(xnr_user_no,date_time):
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'xnr_user_no':xnr_user_no}},
                        {'terms':{'community_status':[0,1,-2]}},
                        {'range':{'trace_time':{'lt':date_time}}}
                        ]
                    }
                }
            }
        },
        'size':7,
        'sort':{'trace_time':{'order':'desc'}}
    }

    trace_index_name = weibo_trace_community_index_name_pre + xnr_user_no.lower()
    trace_community_detail = dict()

    if es_xnr.indices.exists(index = trace_index_name):
        trace_result = es_xnr.search(index = trace_index_name, doc_type = weibo_trace_community_index_type,body = query_body)['hits']['hits']
        len_num = len(trace_result)
        total_num = 0
        cluster_sum = 0
        density_sum = 0
        mean_influence_sum = 0
        mean_sensitive_sum = 0
        if len_num > 0:
            for item in trace_result:
                total_num = total_num + item['_source']['num']
                cluster_sum = cluster_sum + item['_source']['cluster']
                density_sum = density_sum + item['_source']['density']
                mean_influence_sum = mean_influence_sum + item['_source']['mean_influence']
                mean_sensitive_sum = mean_sensitive_sum + item['_source']['mean_sensitive']

            trace_community_detail['min_num'] = (total_num / len_num) * 0.5
            trace_community_detail['max_num'] = (total_num / len_num) * 1.5
            trace_community_detail['cluster'] = (cluster_sum / len_num) * 0.75
            trace_community_detail['density'] = (density_sum / len_num) * 0.75
            trace_community_detail['mean_influence'] = (mean_influence_sum / len_num) * 0.5
            trace_community_detail['mean_sensitive'] = (mean_sensitive_sum / len_num) * 0.5
        else:
            trace_community_detail['min_num'] = MIN_COMMUNITY_NUM
            trace_community_detail['max_num'] = MAX_COMMUNITY_NUM
            trace_community_detail['cluster'] = COMMUNITY_DENSITY_CLUSTER
            trace_community_detail['density'] = COMMUNITY_DENSITY_CLUSTER
            trace_community_detail['mean_influence'] = MIN_MEAN_COMMUNITY_INFLUENCE
            trace_community_detail['mean_sensitive'] = MIN_MEAN_COMMUNITY_SENSITIVE
    else:
        trace_community_detail['min_num'] = MIN_COMMUNITY_NUM
        trace_community_detail['max_num'] = MAX_COMMUNITY_NUM
        trace_community_detail['cluster'] = COMMUNITY_DENSITY_CLUSTER
        trace_community_detail['density'] = COMMUNITY_DENSITY_CLUSTER
        trace_community_detail['mean_influence'] = MIN_MEAN_COMMUNITY_INFLUENCE
        trace_community_detail['mean_sensitive'] = MIN_MEAN_COMMUNITY_SENSITIVE

    return trace_community_detail

#基于跟踪社区指标或指定阈值进行二次筛选
def get_second_select_result(first_select_community,trace_community):
    community_list = []
    for community in first_select_community:
        if community['num'] > trace_community['min_num'] and community['num'] < trace_community['max_num']:
            num_mark = True
        else:
            num_mark = False

        if community['cluster'] > trace_community['cluster'] or community['density'] > trace_community['density']:
            cluster_density_mark = True
        else:
            cluster_density_mark = False

        if community['mean_influence'] > trace_community['mean_influence']:
            mean_influence_mark = True
        else:
            mean_influence_mark = False

        if community['mean_sensitive'] > trace_community['mean_sensitive']:
            mean_sensitive_mark = True
        else:
            mean_sensitive_mark = False

        if num_mark and cluster_density_mark and mean_influence_mark and mean_sensitive_mark:
            community_list.append(community)
        else:
        	pass
    
    return community_list


######社区特征细节补充函数
# 新社区预警判断
def get_newcommunity_warning(community,trace_community_detail):
    cluster_e = trace_community_detail['cluster']/0.75
    density_e = trace_community_detail['density']/0.75
    mean_influence_e = trace_community_detail['mean_influence']/0.5
    mean_sensitive_e = trace_community_detail['mean_sensitive']/0.5
    max_num_e = trace_community_detail['max_num']/1.5

    warning_remind = 0
    warning_rank = 0
    warning_type = []
    if community['cluster'] > cluster_e or community['density'] > density_e: 
        warning_rank = warning_rank + 1
        cluster_type = '社区聚集预警'
        warning_type.append(cluster_type)
    if community['mean_influence'] > mean_influence_e:
        warning_rank = warning_rank + 1
        influenc_type = '影响力剧增预警'
        warning_type.append(influenc_type)
    if community['mean_sensitive'] > mean_sensitive_e:
        warning_rank = warning_rank + 1
        sensitive_type = '敏感度剧增预警'
        warning_type.append(sensitive_type)
    if community['num'] > max_num_e:
        warning_rank = warning_rank + 1
        num_mark = True
        num_type = '人物突增预警'
        warning_type.append(num_type)

    if warning_rank >0:
        warning_remind = 1
    else:
        pass

    return warning_remind,warning_rank,warning_type



#补全社区人员信息，注意标记核心人物
def get_community_userinfo(uid_list,core_uidlist,outer_uidlist):
    user_list = []
    # print 'es_user_profile::',es_user_profile
    user_result = es_user_profile.mget(index = profile_index_name,doc_type = profile_index_type,body = {'ids':uid_list})['docs']
    
    core_user = []
    for item in user_result:
        user_dict = dict()
        user_dict['uid'] = item['_id']

        if item['found']:
            user_dict['photo_url']=item['_source']['photo_url']            
            user_dict['nick_name']=item['_source']['nick_name']
            user_dict['sex']=item['_source']['sex']
            user_dict['friendsnum']=item['_source']['friendsnum']
            user_dict['fansnum']=item['_source']['fansnum']
            user_dict['user_location']=item['_source']['user_location']
        else:
            user_dict['photo_url']=''            
            user_dict['nick_name']=''
            user_dict['sex']=''
            user_dict['friendsnum']=''
            user_dict['fansnum']=''
            user_dict['user_location']=''

        #核心人物判断
        
        core_mark = len(list(set(item['_id'].split())&set(core_uidlist)))
        if core_mark > 0:
            user_dict['core_user'] = 1
            core_user.append(user_dict)
        else:
            user_dict['core_user'] = 0

        user_list.append(user_dict)


    #社区外人物信息
    outer_userlist = []
    outeruser_result = es_user_profile.mget(index = profile_index_name,doc_type = profile_index_type,body = {'ids':outer_uidlist})['docs']
    for item in outeruser_result:
        user_dict = dict()
        user_dict['uid'] = item['_id']

        if item['found']:
            user_dict['photo_url']=item['_source']['photo_url']            
            user_dict['nick_name']=item['_source']['nick_name']
            user_dict['sex']=item['_source']['sex']
            user_dict['friendsnum']=item['_source']['friendsnum']
            user_dict['fansnum']=item['_source']['fansnum']
            user_dict['user_location']=item['_source']['user_location']
        else:
            user_dict['photo_url']=''            
            user_dict['nick_name']=''
            user_dict['sex']=''
            user_dict['friendsnum']=''
            user_dict['fansnum']=''
            user_dict['user_location']=''
        outer_userlist.append(user_dict)
    return json.dumps(user_list),json.dumps(core_user),json.dumps(outer_userlist)


# 确定社区网络图 

#use to merge dict list
#input: dict_list
#ouput: merge_dict
def union_dict_list(objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])

    return _total

#use to merge dict list and filter by uid_list
#input: dict_list
#output: meige_dict
def filter_union_dict(objs, filter_uid_list, mark):
    _keys = set(sum([obj.keys() for obj in objs], []))
    if mark == 'in&out':
        _in_total = {}
        _in_keys = _keys & set(filter_uid_list)
        for _key in _in_keys:
            _in_total[_key] = sum([int(obj.get(_key,0)) for obj in objs])
        _out_total = {} 
        _out_keys = _keys - set(filter_uid_list)
        for _key in _out_keys:
            _out_total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])       
        return _in_total, _out_total
    elif mark == 'out':
        _out_total = {}
        _out_keys = _keys - set(filter_uid_list)
        for _key in _out_keys:
            _out_total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
        return _out_total

#use to get db number for retweet/be_retweet/comment/be_comment
#input: timestamp
#output: db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) % 2 + 1
    #run_type
    if S_TYPE == 'test':
        db_number = 1
    return db_number

#查询用户昵称
def get_user_name(uid_list):
    try:
        portrait_exist_result = es_user_profile.mget(index=profile_index_name,\
            doc_type=profile_index_type,body={'ids':uid_list})['docs']
    except:
        portrait_exist_result = []
    uid2uname_dict = {}
    print portrait_exist_result
    for portrait_item in portrait_exist_result:
        uid = portrait_item['_id']
        if portrait_item['found'] == True:
            source = portrait_item['_source']
            uname = source['nick_name']
        else:
            uname = uid
        uid2uname_dict[uid] = uname
    return uid2uname_dict

#查询用户昵称
def get_user_nickname(uid):
    # try:
    print 'nick_name!!!!'
    user_result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
    user_name=user_result['nick_name']
    # except:
        # user_name=uid
    print 'nick_name final'
    return user_name

#use to get group social attribute
#write in version: 16-01-23
#input: uid_list
#output: group social attribute
def get_community_coreuser_socail(uid_list,timestamp):
    uid2uname = get_user_name(uid_list)
    result = {}
    #step1: get db number
    # timestamp = int(time.time())
    db_num = get_db_num(timestamp)
    retweet_index_name = retweet_index_name_pre + str(db_num)
    be_retweet_index_name = be_retweet_index_name_pre + str(db_num)
    comment_index_name = comment_index_name_pre + str(db_num)
    be_comment_index_name = be_comment_index_name_pre + str(db_num)
    #step2: split uid list to iter mget
    iter_count = 0
    all_user_count = len(uid_list)
    in_stat_results = dict()
    out_stat_result = dict()
    all_in_record = []
    all_out_record = []
    all_out_user_count = 0
    all_out_in_usr_count = 0
    while iter_count < all_user_count:
        # iter_uid_list = uid_list
        iter_uid_list = uid_list[iter_count:iter_count+GROUP_ITER_COUNT]
        #step3:mget retweet
        try:
            retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type, \
                                             body={'ids':iter_uid_list})['docs']
        except:
            retweet_result = []
        retweet_dict = {} #{uid1: {ruid1:count1, ruid2:count2}, uid2:{},...}
        for item in retweet_result:
            uid = item['_id']
            #tesit for error es
            try:
                if item['found'] == True:
                    retweet_dict[uid] = json.loads(item['_source']['uid_retweet'])
            except:
                pass

        #step4:mget comment
        try:
            comment_result = es_comment.mget(index=comment_index_name, doc_type=comment_index_type, \
                                             body={'ids':iter_uid_list})['docs']
        except:
            comment_result = []
        comment_dict = {} #{uid1:{ruid1:count1, ruid2:count2},...}
        # print 'comment_result:',comment_result
        for item in comment_result:
            uid = item['_id']
            try:
                if item['found'] == True:
                    comment_dict[uid] = json.loads(item['_source']['uid_comment'])
            except:
            	pass
        #step5:mget be_retweet
        try:
            be_retweet_result = es_retweet.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type, \
                                                body={'ids':iter_uid_list})['docs']
        except:
            be_retweet_result = []
        be_retweet_dict = dict() #{uid1: {uid_be_retweet dict}, uid2:{},...}
        for item in be_retweet_result:
            uid = item['_id']
            #test for error es
            try:
                if item['found'] == True:
                    be_retweet_dict[uid] = json.loads(item['_source']['uid_be_retweet'])
            except:
                pass
        #step6:mget be_comment
        try:
            be_comment_result = es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type,\
                                                body={'ids':iter_uid_list})['docs']
        except:
            be_comment_result = []
        be_comment_dict = dict() #{uid1:{uid_be_comment dict}, uid2:{},...}
        for item in be_comment_result:
            uid = item['_id']
            #test for error es
            try:
                if item['found'] == True:
                    be_comment_dict[uid] = json.loads(item['_source']['uid_be_comment'])
            except:
                pass
        #step7:union retweet&comment, be_retweet&be_comment
        for iter_uid in iter_uid_list:
            try:
                user_retweet_result = retweet_dict[iter_uid]
            except:
                user_retweet_result = {}
            try:
                user_comment_result = comment_dict[iter_uid]
            except:
                user_comment_result = {}
            filter_in_dict, filter_out_dict = filter_union_dict([user_retweet_result, user_comment_result], uid_list, 'in&out')
            
            #step8: record the retweet/coment relaton in group uid 
            
            # 
            # uid_in_record = [[iter_uid, ruid, filter_in_dict[ruid], uid2uname[iter_uid], uid2uname[ruid]] for ruid in filter_in_dict if iter_uid != ruid]
            # 
            # print 'filter_in_dict:',filter_in_dict
            # print 'filter_out_dict:',filter_out_dict
            # uid_in_record = [[iter_uid,uid2uname[iter_uid],ruid,uid2uname[ruid],filter_in_dict[ruid]] for ruid in filter_in_dict if iter_uid != ruid]
            uid_in_record = []
            for ruid in filter_in_dict:
                # print 'ruid:',ruid
                item_list = []
                if iter_uid != ruid:
                    # print 'aaaa'
                    item_list.append(iter_uid)

                    if uid2uname.has_key(iter_uid):
                        iter_name = uid2uname[iter_uid]
                    else:
                        iter_name = iter_uid
                    item_list.append(iter_name)

                    item_list.append(ruid)

                    if uid2uname.has_key(ruid):
                        ruid_name = uid2uname[ruid]
                    else:
                        ruid_name = ruid
                    item_list.append(ruid_name)
                    item_list.append(filter_in_dict[ruid])
                    
                    if item_list:
                        uid_in_record.append(item_list)
                    else:
                        pass
                else:
                    pass
                # print 'item_list:',item_list
            # print 'uid_in_record:',uid_in_record
            # in_record = [uid_in_record]
            all_in_record.extend(uid_in_record)  # [[uid1, ruid1, count1],[uid1,ruid2,count2],[uid2,ruid2,count3],...]
            #step9: record the retweet/comment/be_retweet/be_comment relation out group uid
            try:
                user_be_retweet_result = be_retweet_dict[iter_uid]
            except:
                user_be_retweet_result = {}
            try:
                user_be_comment_result = be_comment_dict[iter_uid]
            except:
                user_be_comment_result = {}
            filter_out_dict = filter_union_dict([filter_out_dict, user_be_retweet_result, user_be_comment_result], uid_list, 'out')
            #step10: filter out user who is in user_portrait
            
            # uid_out_record = [[iter_uid,get_user_nickname(iter_uid),ruid,get_user_nickname(ruid),filter_out_dict[ruid]] for ruid in filter_out_dict if iter_uid != ruid]
            uid_out_record = []
            for ruid in filter_out_dict:
                item_list = []
                if iter_uid != ruid:
                    item_list.append(iter_uid)
                    if uid2uname.has_key(iter_uid):
                        iter_name = uid2uname[iter_uid]
                    else:
                        iter_name = iter_uid
                    item_list.append(iter_name)

                    item_list.append(ruid)

                    if uid2uname.has_key(ruid):
                        ruid_name = uid2uname[ruid]
                    else:
                        ruid_name = ruid
                    item_list.append(ruid_name)
                    item_list.append(filter_out_dict[ruid])
                    
                    if item_list:
                        uid_out_record.append(item_list)
                    else:
                        pass
                else:
                    pass
            # out_record = [uid_out_record]
            all_out_record.extend(uid_out_record) #[[uid1, ruid1,count1],[uid1,ruid2,count2],[uid2,ruid2,count3],...]
        iter_count += GROUP_ITER_COUNT

    #step11 sort interaction in group by retweet&comment count
    sort_in_record = sorted(all_in_record, key=lambda x:x[4], reverse=True)
    # print 'all_out_record::',all_out_record
    sort_out_record = sorted(all_out_record,key=lambda x:x[4], reverse=True)

    # print 'sort_in_record::',len(sort_in_record)
    # print 'sort_out_record::',len(sort_out_record)
    #core_uidlist,outer_uidlist,community_dict['core_user_socail'],community_dict['core_outer_socail']
    core_user_socail = [item for item in sort_in_record if item[4] > 2]
    core_uidlist = list(set([item[0] for item in core_user_socail]))
    # print 'core_uidlist:',core_uidlist
    # print 'core_user_socail:',core_user_socail
    core_outer_socail_temp = [item for item in sort_out_record if (len(list(set(item[2].split())&set(core_uidlist)))>0 or len(list(set(item[0].split())&set(core_uidlist)))>0) and item[4] > 10]
    # core_outer_socail = [item for item in sort_out_record if (len(list(set(item[2])&set(core_uidlist)))>0  or len(list(set(item[0].split())&set(core_uidlist)))>0)]
    core_outer_socail = sorted(core_outer_socail_temp,key=lambda x:x[4],reverse=True)[0:30]
    # print 'core_outer_socail::',core_outer_socail
    outer_uidlist = [item[0] for item in core_outer_socail]

    # print 'core_user_socail:',type(core_user_socail)
    # print 'core_outer_socail:',type(core_outer_socail)
    # print 'core_uidlist::',type(core_uidlist)
    # print 'outer_uidlist::',type(outer_uidlist)
    # return json.loads(core_uidlist),json.loads(outer_uidlist),json.loads(core_user_socail),json.loads(core_outer_socail)
    return core_uidlist,outer_uidlist,core_user_socail,core_outer_socail

# 社区得分的评分
# def get_newcommunity_score(community):

# 统计社区发布的高频词,参考监测关键词生成
def extract_keywords(w_text):

    tr4w = TextRank4Keyword()
    tr4w.analyze(text=w_text, lower=True, window=4)
    k_dict = tr4w.get_keywords(100, word_min_len=2)

    return k_dict

def get_community_keyword(uid_list,date_time):
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms':{'uid':uid_list}}
                        ]
                    }
                }
            }
        },
        'aggs':{
                'keywords':{
                    'terms':{
                        'field':'keywords_string',
                        'size': 1000
                    }
                }
        }
    }
    flow_text_index_name_list = get_flow_text_index_list(date_time)
    flow_text_exist = es_flow_text.search(index = flow_text_index_name_list,doc_type = flow_text_index_type,\
               body = query_body)['aggregations']['keywords']['buckets']

    word_dict = dict()

    word_dict_new = dict()

    keywords_string = ''
    for item in flow_text_exist:
        word = item['key']
        count = item['doc_count']
        word_dict[word] = count

        keywords_string += '&'
        keywords_string += item['key']

    k_dict = extract_keywords(keywords_string)

    for item_item in k_dict:
        keyword = item_item.word
        # print 'keyword::',keyword,type(keyword)
        if word_dict.has_key(keyword):
            word_dict_new[keyword] = word_dict[keyword]
        else:
            word_dict_new[keyword] = 1

    keyword_dict = sorted(word_dict_new.items(),key = lambda d:d[1],reverse = True)
    #print 'keyword_dict',keyword_dict,keyword_dict[0],type(keyword_dict[0])
    keyword_name = keyword_dict[0][0] + '_' + keyword_dict[1][0]
    return json.dumps(keyword_dict),keyword_name


#补充社区特征
def update_newcommunity_character(xnr_user_no,date_time,community,trace_community_detail):
    community_dict = dict()
    community_dict['xnr_user_no'] = xnr_user_no
    print 'date_time:',date_time
    community_dict['create_time'] = date_time

    community_dict['num'] = community['num']
    community_dict['nodes'] = community['nodes']
    community_dict['density'] = community['density']
    community_dict['cluster'] = community['cluster']
    community_dict['max_influence'] = community['max_influence']
    community_dict['mean_influence'] = community['mean_influence']
    community_dict['max_sensitive'] = community['max_sensitive']
    community_dict['mean_sensitive'] = community['mean_sensitive']

    community_dict['update_time'] = date_time #更新时间
    community_dict['community_status'] = 0     # 0表示是新社区，新旧社区对比时可能更新

    community_uidlist = community['nodes']
    #新社区预警判断
    community_dict['warning_remind'],community_dict['warning_rank'],\
    community_dict['warning_type'] = get_newcommunity_warning(community,trace_community_detail) 

    #核心人物社交网络信息
    core_uidlist,outer_uidlist,core_user_socail,core_outer_socail = get_community_coreuser_socail(community['nodes'],date_time) 
    community_dict['core_user_socail'] = json.dumps(core_user_socail)
    community_dict['core_outer_socail'] = json.dumps(core_outer_socail)
    #社区人员信息列表（标记核心人员），核心人员列表
    community_dict['community_user_list'],community_dict['core_user'],\
    community_dict['outer_user'] = get_community_userinfo(community['nodes'],core_uidlist,outer_uidlist) 
    community_dict['core_user_change'] = '' #核心社区人员变化信息，在新旧社区对比时更新
    community_dict['community_user_change'] = ''  #社区人员变化信息，在新旧社区对比时更新


    #社区推荐跟踪得分,总分5分，与预警级别暂时保持一致
    community_dict['total_score'] = community_dict['warning_rank']

    #社区高频关键词
    community_dict['socail_keyword'],community_dict['community_name'] = get_community_keyword(community['nodes'],date_time)
    
    community_dict['community_id'] = xnr_user_no + '_' + ts2datetime(date_time) + community_dict['community_name']
    
    return community_dict

####################################################################
#组织函数
#根据指标筛选推荐社区
def get_select_community(xnr_user_no,date_time):
    #获取生成社区列表
    create_communitylist = get_xnr_community(xnr_user_no,date_time)

    #根据社区指标对生成社区进行筛选
    first_select_community = get_first_select_result(create_communitylist)

    #第一次筛选后的社区人数
    first_community_num = len(first_select_community)
    print 'first_select_community::',first_community_num,first_select_community

    second_select_community = []

    #计算xnr当前跟踪社区指标平均值信息
    trace_community_detail = get_xnr_trace_community_detail(xnr_user_no,date_time)
    if first_community_num > MAX_SELECT_COMMUNITY_NUM:
        #基于跟踪社区指标信息进行二次筛选
        second_select_community = get_second_select_result(first_select_community,trace_community_detail)
    else:
        second_select_community = first_select_community

    #补充社区特征
    community_list = []
    for community in second_select_community:
    	community_detail = update_newcommunity_character(xnr_user_no,date_time,community,trace_community_detail)
    	community_list.append(community_detail)

    return community_list

#旧社区上一周期预警判断
def get_community_warning_traceresult(community,date_time):
    # print 'community::::',community,type(community)
    weibo_trace_community_index_name = weibo_trace_community_index_name_pre + community["xnr_user_no"].lower()
    start_time = date_time - 7*DAY
    query_body = {
	    'query':{
	        'filtered':{
	            'filter':{
	                'bool':{
	                    'must':[
	                        {'term':{'community_id':community['community_id']}},
	                        {'range':{'trace_time':{'gte':start_time,'lte':date_time}}}
	                    ]
	                }
	            }
	        }
	    }
	}
    trace_result = es_xnr.search(index=weibo_trace_community_index_name,\
        doc_type=weibo_trace_community_index_type,body=query_body)['hits']['hits']
    warning_mark = 0
    for item in trace_result:
        if item['_source']['warning_rank'] > 0:
            warning_mark = warning_mark + 1
        else:
            pass
    return warning_mark


#获取已有的社区信息
def get_old_community(xnr_user_no,date_time):
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'xnr_user_no':xnr_user_no}},
                        {'terms':{'community_status':[1,-2]}}                        
                        ]
                    }
                }
            }
        }
    }
    weibo_community_index_name = weibo_community_index_name_pre + ts2datetime(date_time - 7*DAY)
    print 'old_community:::',weibo_community_index_name
    community_list = []

    if es_xnr.indices.exists(weibo_community_index_name):
        community_result = es_xnr.search(index = weibo_community_index_name,doc_type = weibo_community_index_type,body = query_body)['hits']['hits']
        for community in community_result:
            #获取社区预警情况，在上一周期内是否出现预警
            warning_mark = get_community_warning_traceresult(community['_source'],date_time)
            if warning_mark > 0:
                pass
            else:
            	community['_source']['warning_remind'] = community['_source']['warning_remind'] + 1

            if community['_source']['warning_remind'] > 4 and community['_source']['community_status'] != -2:
            	pass
            else:
                community_list.append(community['_source'])
    else:
        pass

    return community_list


#存储社区至数据库
def save_community_detail(community_detail,date_time):
    try:
        es_community = es_xnr.index(index=weibo_community_index_name_pre+ts2datetime(date_time),\
            doc_type=weibo_community_index_type,body=community_detail,id=community_detail['community_id'])
        mark = True
    except:
        mark = False
    return mark


#用户变化函数
def get_user_change(new_users,old_users):
    new_userid_list = [item['uid'] for item in json.loads(new_users)]
    old_userid_list = [item['uid'] for item in json.loads(old_users)]

    common_uidlist = set(new_userid_list)&set(old_userid_list)
    add_uidlist = set(new_userid_list) - common_uidlist
    dec_uidlist = set(old_userid_list) - common_uidlist

    user_change_list = []
    for new_user in json.loads(new_users):
        if len(set(new_user['uid'].split())&add_uidlist)>0:
            new_user['change'] = 1
        elif len(set(new_user['uid'].split())&common_uidlist)>0:
        	new_user['change'] = 0
        user_change_list.append(new_user)

    for old_user in json.loads(old_users):
    	if len(set(old_user['uid'].split())&dec_uidlist)>0:
    		old_user['change'] = -1
    	user_change_list.append(old_user)

    return json.dumps(user_change_list)

def get_final_community(xnr_user_no,date_time):
    #新生成的社区list
    create_communitylist = get_select_community(xnr_user_no,date_time)
    #已有社区列表
    old_communitylist = get_old_community(xnr_user_no,date_time)
    print 'old_communitylist::',len(old_communitylist)
    print 'new_community::',len(create_communitylist)
    #新旧社区对比
    #step.1 若旧社区为空，则直接保留新社区,存储至es；
    # 若旧社区不为空，则对新旧社区进行对比
    # 若对比不相似则存储旧社区，对旧社区进行一些判断与更新；
    # 若对比相似，则要进行新旧社区融合处理
    result_mark_list = []    
    if old_communitylist:
        newid_list = []
        for new_community in create_communitylist:
            similarity_oldid = old_communitylist[0]['community_id']
            similarity_firstlen = len(list(set(new_community['nodes'])&set(old_communitylist[0]['nodes'])))
            similarity_first = similarity_firstlen / old_communitylist[0]['num']       	
            for old_community in old_communitylist[1:]:
                similarity_uidlen = len(list(set(new_community['nodes'])&set(old_community['nodes'])))
                similarity = similarity_uidlen / old_community['num']
                if similarity > similarity_first:
                    similarity_first = similarity
                    similarity_oldid = old_community['community_id']
                    print 'similarity_oldid::',similarity_oldid
            if similarity_first > COMMUNITY_SIMILARITY:
            	print 'similarity:::',similarity_first
                newid_list.append(similarity_oldid)
            else:
            	similarity_oldid = 'a'
            	newid_list.append(similarity_oldid)
            	
           # print 'similarity_oldid::',similarity_oldid
        for idx,new_community in enumerate(create_communitylist):
            old_community_list = [c for c in old_communitylist if c['community_id'] == newid_list[idx]]
            if len(old_community_list) > 0:
            	old_community = old_communitylist[0]
            	new_community['community_id'] = old_community['community_id']
            	new_community['create_time'] = old_community['create_time']
            	new_community['community_name'] = old_community['community_name']
            	new_community['community_status'] = old_community['community_status']
            	new_community['core_user_change'] = get_user_change(new_community['core_user'],old_community['core_user'])
                new_community['community_user_change'] = get_user_change(new_community['community_user_list'],old_community['community_user_list'])
                result_mark = save_community_detail(new_community,date_time)
            else:
            	print 'new_community:::',new_community['community_name']
            	result_mark = save_community_detail(new_community,date_time)

        for old_community in old_communitylist:
            if old_community['community_id'] in newid_list:
                print 'old_community::::',old_community['community_name']
            else:
                result_mark = save_community_detail(old_community,date_time)
                result_mark_list.append(result_mark)

    else:
    	print 'newnew!!!'
        for new_community in create_communitylist:
            new_community['community_status'] = 1
            result_mark = save_community_detail(new_community,date_time)
            result_mark_list.append(result_mark)  

    result_final = True      
    # return result_mark_list
    return result_final


if __name__ == '__main__':
    # start_time = int(time.time())
    # xnr_user_no = 'WXNR0004'
    # date_time = datetime2ts('2018-03-13')
    # # get_select_community(xnr_user_no,date_time)
    # uid_list = ["3623353053", "5269743490", "3847403453", "5461392052", "5935891935", "2684793101", "5889425309", "2947335715", "5677806677", "5857120687", "2141246805", "1646029765", "1710173801", "5897716478", "5796731205", "5080620052", "5843802987", "5874487882", "5337758780", "6052732011", "1836308272", "2520614617", "5237810007", "3200673035", "5305142622", "5113031562", "2782682084", "2482242324", "5889618968", "5754076274"]
    # # get_community_coreuser_socail(uid_list,datetime2ts(date_time))
    # # end_time = int(time.time())
    # # print 'time_cost:',end_time - start_time
    # core_uidlist = ["3623353053", "5269743490", "3847403453"]
    # outer_uidlist = [ "5586779165", "1236103277"]
    # get_community_userinfo(uid_list,core_uidlist,outer_uidlist)
    if S_TYPE == 'test':
    	datetime = datetime2ts(WEIBO_COMMUNITY_DATE)
    	xnr_user_no_list = ['WXNR0004']
    else:
    	datetime = int(time.time())-8*DAY
    	xnr_user_no_list = get_compelete_wbxnr()
    start_time = int(time.time())
    for xnr_user_no in xnr_user_no_list:
        print 'xnr_user_no::',xnr_user_no
        get_final_community(xnr_user_no,datetime)
    end_time = int(time.time())
    print 'cost_time::',end_time - start_time
