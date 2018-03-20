# -*- coding: utf-8 -*-
import os
import json
import time
import sys

sys.path.append('../../')
from parameter import MIN_COMMUNITY_NUM,MAX_COMMUNITY_NUM,COMMUNITY_DENSITY_CLUSTER,\
                      MIN_MEAN_COMMUNITY_SENSITIVE,MIN_MEAN_COMMUNITY_INFLUENCE,\
                      MAX_SELECT_COMMUNITY_NUM,COMMUNITY_SIMILARITY

from parameter import DAY

from time_utils import ts2datetime

from global_utils import es_xnr,weibo_trace_community_index_name_pre,weibo_trace_community_index_type,\
                         weibo_community_index_name_pre,weibo_community_index_type,\
                         es_user_profile,profile_index_name,profile_index_type


sys.path.append('../../timed_python_files/community/')
from weibo_publicfunc import get_compelete_wbxnr

#思路：
#step1:读取该周期生成的json文件，根据指标筛选社区<=20个
#step2:新旧社区对比，预警判断-预警次数计算（考虑生成预警文件或者在trace中记录），强制跟踪判断，特征更新，存储至detail_community

#读取虚拟人的社区
def get_xnr_community(xnr_user_no,date_time):
    file_name = './weibo_data/' + xnr_user_no + '_' + date_time + '_' +'save_com.json'
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

        if num_mark and cluster_density_mark and mean_sensitive_mark and mean_influence_mark:
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
        }
    }

    trace_index_name = weibo_trace_community_index_name_pre + xnr_user_no
    trace_index_detail = dict()

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
    if community['cluster'] > cluster_e:
        warning_rank = warning_rank + 1
    if community['density'] > density_e:
    	warning_rank = warning_rank + 1
    if community['mean_influence'] > mean_influence_e:
    	warning_rank = warning_rank + 1
    if community['mean_sensitive'] > mean_sensitive_e:
    	warning_rank = warning_rank + 1
    if community['num'] > max_num_e:
    	warning_rank = warning_rank + 1
    	num_mark = True

    if warning_rank >0:
    	if num_mark and warning_rank == 1:
    		pass
    	else:
    		warning_remind = 1
    else:
    	pass

    return warning_remind,warning_rank



#补全社区人员信息，注意标记核心人物
def get_community_userinfo(uid_list,core_uidlist):
    user_list = []
    user_result = es_user_profile.mget(index = profile_index_name,doc_type = profile_index_type,body = {'ids':uid_list})['docs']
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
        core_list = []
        core_mark = len(list(set(core_list.append(item['_id']),core_uidlist)))
        if core_mark > 0:
            user_dict['core_user'] = 1
        else:
            user_dict['core_user'] = 0

        user_list.append(user_dict)

    return user_list

# 
# def get_community_coreuser_socail(uid_list):

#
# def get_newcommunity_score(community):

# 
# def get_community_keyword(uid_list):

#补充社区特征
def update_newcommunity_character(xnr_user_no,date_time,community,trace_community_detail):
    community_dict = dict()
    community_dict['xnr_user_no'] = xnr_user_no
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
    community_dict['community_status'] = 0 # 0表示是新社区，新旧社区对比时可能更新

    community_uidlist = community['nodes']
    #新社区预警判断
    community_dict['warning_remind'],community_dict['warning_rank'] = get_newcommunity_warning(community,trace_community_detail) 
    
    #核心人物社交网络信息
    core_uidlist,community_dict['core_user'],community_dict['core_user_socail'],\
    community_dict['core_outer_socail'],community_dict['outer_user'] = get_community_coreuser_socail(community['nodes']) 

    #社区人员信息列表（标记核心人员），核心人员列表
    community_dict['community_user_list'] = get_community_userinfo(community['nodes'],core_uidlist) 
    community_dict['core_user_change'] = '' #核心社区人员变化信息，在新旧社区对比时更新
    community_dict['community_user_change'] = ''  #社区人员变化信息，在新旧社区对比时更新


    #社区推荐跟踪得分,总分5分
    community_dict['total_score'] = get_newcommunity_score(community)

    #社区高频关键词
    community_dict['socail_keyword'],community_dict['community_name'] = get_community_keyword(community['nodes'])
    
    community_dict['community_id'] = xnr_user_no + '_' + ts2datetime(date_time) + community_dict['community_name']
    
    return community_dict


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


#获取已有的社区信息
def get_old_community(xnr_user_no,date_time):
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'xnr_user_no':xnr_user_no}},
                        {'terms':{'community_status':[0,1,-2]}}                        
                        ]
                    }
                }
            }
        }
    }
    weibo_community_index_name = weibo_community_index_name_pre + ts2datetime(date_time - 7*DAY)
    community_list = []

    if es_xnr.indices.exists(weibo_community_index_name):
        community_result = es_xnr.search(index = weibo_community_index_name,doc_type = weibo_community_index_type,body = query_body)['hits']['hits']
        for community in community_result:
        	community_list.append(item['_source'])
    else:
        pass

    return community_list


def get_final_community(xnr_user_no,date_time):
    #新生成的社区list
    create_communitylist = get_select_community(xnr_user_no,date_time)
    #已有社区列表
    old_communitylist = get_old_community(xnr_user_no,date_time)
   
    #新旧社区对比
    #step.1 若旧社区为空，则直接保留新社区,存储至es；
    # 若旧社区不为空，则对新旧社区进行对比
    # 若对比不相似则存储旧社区，对旧社区进行一些判断与更新；
    # 若对比相似，则要进行新旧社区融合处理

    # final_community_list = []
    # if old_communitylist:
    #     for new_community in create_communitylist:
    #         for old_community in old_communitylist:
    #             similarity_uidlen = len(list(set(new_community['nodes'],old_community['nodes'])))
    #             similarity = similarity_uidlen / old_community['num']
    #             if similarity > COMMUNITY_SIMILARITY:

    #             else:
    #                 new_community['community_status'] = 0
    # else:
    #     final_community_list


#step2:
# 新旧社区对比
# 预警判断-预警次数计算（考虑生成预警文件或者在trace中记录），强制跟踪判断，
# 特征更新，存储至detail_community

if __name__ == '__main__':
    xnr_user_no = 'WXNR0004'
    date_time = '2018-03-13'
    get_select_community(xnr_user_no,date_time)