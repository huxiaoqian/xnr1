# -*- coding: utf-8 -*-
import os
import json
import time
import sys


#读取虚拟人的社区
def get_xnr_community():
    file_name = 'save_com_json_all.json'
    file_community = open(file_name,'r')
    community = file_community.readlines()
    # print 'community:',type(community_list)
    # community_list = json.loads(community_list)
    # print 'community_list:',type(community_list),type(community_list[0]),community_list[0]
    community_list = []
    for community_item in community:
        community_item = json.loads(community_item)
        community_list.append(community_item)
        
    print 'community_list:',type(community_list),type(community_list[0]),len(community_list)
    
    mean_sensitive = 'mean_sensitive'
    community_list.sort(key=lambda k:(k.get(mean_sensitive,0)),reverse=True)
    max_mean_sensitive = community_list[0]['mean_sensitive']
    min_mean_sensitive = community_list[-1]['mean_sensitive']

    mean_influence = 'mean_influence'
    community_list.sort(key=lambda k:(k.get(mean_influence,0)),reverse=True)
    max_mean_influence = community_list[0]['mean_influence']
    min_mean_influence = community_list[-1]['mean_influence']

    num = 'num'
    community_list.sort(key=lambda k:(k.get(num,0)),reverse=True)
    max_num = community_list[0]['num']
    min_num = community_list[-1]['num']

    density = 'density'
    community_list.sort(key=lambda k:(k.get(density,0)),reverse=True)
    max_desity = community_list[0]['density']
    min_desity = community_list[-1]['density']

    cluster = 'cluster'
    community_list.sort(key=lambda k:(k.get(cluster,0)),reverse=True)
    max_cluster = community_list[0]['cluster']
    min_cluster = community_list[-1]['cluster']

    print 'max_mean_sensitive:',max_mean_sensitive,min_mean_sensitive
    print 'max_mean_influence:',max_mean_influence,min_mean_influence
    print 'num:',max_num,min_num
    print 'density:',max_desity,min_desity
    print 'cluster:',max_cluster,min_cluster
    
    new_community_list = []
    for i in range(0,len(community_list)):
        # print 'community_list_d:',type(community_list[i]),community_list[i]
        if community_list[i]['mean_sensitive'] < 0.00001:
            # community_list.remove(community_list[i])
            sensitive_mark = False
        else:
            sensitive_mark = True
            # new_community_list.append(community_list[i])

        if community_list[i]['mean_influence'] < 0.0975 and sensitive_mark:
            # community_list.remove(community_list[i])
            influence_mark = False
        else:
            influence_mark = True
            # new_community_list.append(community_list[i])


        if sensitive_mark and influence_mark and community_list[i]['num'] < 10 and community_list[i]['num'] > 1000:
            # community_list.remove(community_list[i])
            num_mark = False
        else:
            num_mark = True
            # new_community_list.append(community_list[i])

        if sensitive_mark and influence_mark and num_mark and community_list[i]['density'] < 0.5:
            # community_list.remove(community_list[i])
            density_mark = False
        else:
            density_mark = True
            # new_community_list.append(community_list[i])

        if sensitive_mark and influence_mark and num_mark and community_list[i]['cluster'] < 0.5:
            # community_list.remove(community_list[i])
            cluster_mark = False
        else:
            cluster_mark = True
                
        if sensitive_mark and influence_mark and num_mark and (cluster_mark or density_mark):
            new_community_list.append(community_list[i])



    print 'new_community_list_len',len(new_community_list)
    return community_list



if __name__ == '__main__':
    get_xnr_community()