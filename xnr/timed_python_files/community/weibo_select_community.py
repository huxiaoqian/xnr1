# -*- coding: utf-8 -*-
import os
import json
import time
import sys

sys.path.append('../../')
from parameter import MIN_COMMUNITY_NUM,MAX_COMMUNITY_NUM,COMMUNITY_DENSITY_CLUSTER,\
                      MIN_MEAN_COMMUNITY_SENSITIVE,MIN_MEAN_COMMUNITY_INFLUENCE,\
                      MAX_SELECT_COMMUNITY_NUM
from global_utils import es_xnr,weibo_trace_community_index_name_pre,weibo_trace_community_index_type


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
                        {'terms':{'trace_status':[0,1,2]}},
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
                total_num = total_num + item['num']
                cluster_sum = cluster_sum + item['cluster']
                density_sum = density_sum + item['density']
                mean_influence_sum = mean_influence_sum + item['mean_influence']
                mean_sensitive_sum = mean_sensitive_sum + item['mean_sensitive']

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
    if first_community_num > MAX_SELECT_COMMUNITY_NUM:
        #计算xnr当前跟踪社区指标平均值信息
        trace_community_detail = get_xnr_trace_community_detail(xnr_user_no,date_time)

        #基于跟踪社区指标信息进行二次筛选
        second_select_community = get_second_select_result(first_select_community,trace_community_detail)
    else:
        second_select_community = first_select_community


    return second_select_community


#新旧社区的比较与信息更新


if __name__ == '__main__':
    xnr_user_no = 'WXNR0004'
    date_time = '2018-03-13'
    get_select_community(xnr_user_no,date_time)