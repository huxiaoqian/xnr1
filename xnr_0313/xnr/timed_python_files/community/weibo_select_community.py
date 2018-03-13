# -*- coding: utf-8 -*-
import os
import json
import time
import sys

sys.path.append('../../')
from parameter import MIN_COMMUNITY_NUM,MAX_COMMUNITY_NUM,COMMUNITY_DENSITY_CLUSTER,\
                      MIN_MEAN_COMMUNITY_SENSITIVE,MIN_MEAN_COMMUNITY_INFLUENCE
from global_utils import es_xnr


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


#根据指标筛选推荐社区
def get_select_community(xnr_user_no,date_time):
    #获取生成社区列表
    create_communitylist = get_xnr_community(xnr_user_no,date_time)

    #根据社区指标对生成社区进行筛选
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

    #第一次筛选后的社区人数
    first_community_num = len(first_select_community)
    print 'first_select_community::',first_community_num,first_select_community

    #计算xnr当前跟踪社区指标平均值信息
    # trace_community_detail = get_xnr_trace_community_detail(xnr_user_no)
    return True


#新旧社区对比

if __name__ == '__main__':
    xnr_user_no = 'WXNR0004'
    date_time = '2018-03-11'
    get_select_community(xnr_user_no,date_time)