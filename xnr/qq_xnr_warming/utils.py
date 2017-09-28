#-*- coding: utf-8 -*-
'''
qq_xnr warming function
'''
import os
import json
import time
#from xnr.global_utils import es_flow_text,flow_text_index_type
from xnr.time_utils import ts2yeartime,ts2datetime,datetime2ts
from xnr.parameter import USER_NUM
from xnr.global_config import S_TYPE

#QQ一键上报
#report_dict={'report_type':{},'report_time':{},'xnr_user_no':{},'qq_number':{}}
#report_content=[sensitive_content,user_info]
#人物行为预警,sensitive_content和user_info不为空
#言论内容预警sensitive_content不为空
#sensitive_content={}
#user_info={}

#def qq_

#一键上报
#report_info=[report_type,report_time,xnr_user_no,event_name,uid]
###report_content=[user_list,weibo_list]
#人物行为预警上报report_content=[weibo_list]
#言论内容预警上报report_content=[weibo_dict]
#事件涌现预警上报report_content=[user_list,weibo_list]
#user_dict=[uid,nick_name,fansnum,friendsnum]
#weibo_dict=[mid,text,timestamp,retweeted,like,comment]
#user_list=[user_dict,user_dict,....]
#weibo_list=[weibo_dict,weibo_dict,....]
def report_warming_content(report_info,user_info,weibo_info):
    report_dict=dict()
    report_dict['report_type']=report_info[0]
    report_dict['report_time']=int(report_info[1])
    report_dict['xnr_user_no']=report_info[2]
    report_dict['event_name']=report_info[3]
    report_dict['uid']=report_info[4]
    report_id=report_info[2]+'_'+str(report_info[1])

    #对用户信息进行
    user_list=[]
    if user_info:
        #print 'aaaaaa'
        user_info_item=user_info.encode('utf-8').split('*')
        for user_item in user_info_item:
            user_detail=user_item.split(',')
            user_dict=dict()
            user_dict['uid']=user_detail[0]
            user_dict['nick_name']=user_detail[1]
            user_dict['fansnum']=user_detail[2]
            user_dict['friendsnum']=user_detail[3]
            user_list.append(user_dict)

    #对微博信息进行处理
    weibo_list=[]
    if weibo_info:
        #print 'bbbbbb'
        #print 'weibo_info:::',weibo_info
        weibo_info_item=weibo_info.split('*')
        print weibo_info_item
        for weibo_item in weibo_info_item:
            #print 'weibo_item：：：',weibo_item
            weibo_detail=weibo_item.split(',')
            weibo_dict=dict()
            weibo_dict['mid']=weibo_detail[0]
            weibo_dict['text']=weibo_detail[1]
            weibo_dict['timestamp']=weibo_detail[2]
            weibo_dict['retweeted']=weibo_detail[3]
            weibo_dict['like']=weibo_detail[4]
            weibo_dict['comment']=weibo_detail[5]
            weibo_list.append(weibo_dict)

    report_content=dict()
    report_content['user_list']=user_list
    report_content['weibo_list']=weibo_list

    report_dict['report_content']=json.dumps(report_content)

    try:
        es_xnr.index(index=weibo_report_management_index_name,doc_type=weibo_report_management_index_type,id=report_id,body=report_dict)
        mark=True
    except:
        mark=False
    return mark