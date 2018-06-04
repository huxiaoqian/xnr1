# -*- coding: utf-8 -*-
import time
import sys
import os,datetime
from wx_regular_cleaning import clean_wx_group_media_files

sys.path.append('../')
from time_utils import ts2datetime,datetime2ts
from parameter import DAY
from global_utils import es_xnr,es_xnr_2

#weibo_feedback
from global_utils import weibo_feedback_comment_index_name_pre,\
                         weibo_feedback_retweet_index_name_pre,\
                         weibo_feedback_private_index_name_pre,\
                         weibo_feedback_at_index_name_pre,\
                         weibo_feedback_like_index_name_pre

#new_xnr_flow_text
from global_utils import new_xnr_flow_text_index_name_pre

#group_message
from global_utils import group_message_index_name_pre

#twitter_flow_text_
from global_utils import twitter_flow_text_index_name_pre

#facebook_flow_text
from global_utils import facebook_flow_text_index_name_pre

#twitter_count
from global_utils import twitter_count_index_name_pre

#facebook_count
from global_utils import facebook_count_index_name_pre

#tw_bci
from global_utils import tw_bci_index_name_pre

#fb_bci
from global_utils import fb_bci_index_name_pre

#wx_group_message
from global_utils import wx_group_message_index_name_pre,wx_sent_group_message_index_name_pre

#facebook_feedback
from global_utils import facebook_feedback_comment_index_name_pre,\
                         facebook_feedback_retweet_index_name_pre,\
                         facebook_feedback_private_index_name_pre,\
                         facebook_feedback_at_index_name_pre,\
                         facebook_feedback_like_index_name_pre

#new_fb_xnr_flow_text_
from global_utils import new_fb_xnr_flow_text_index_name_pre

#twitter_feedback
from global_utils import twitter_feedback_comment_index_name_pre,\
                         twitter_feedback_retweet_index_name_pre,\
                         twitter_feedback_private_index_name_pre,\
                         twitter_feedback_at_index_name_pre,\
                         twitter_feedback_like_index_name_pre
# new_tw_xnr_flow_text
from global_utils import new_tw_xnr_flow_text_index_name_pre

#community
from global_utils import weibo_community_index_name_pre

#waring
from global_utils import weibo_user_warning_index_name_pre,facebook_user_warning_index_name_pre,twitter_user_warning_index_name_pre,\
                         weibo_event_warning_index_name_pre,facebook_event_warning_index_name_pre,twitter_event_warning_index_name_pre,\
                         weibo_speech_warning_index_name_pre,facebook_speech_warning_index_name_pre,twitter_speech_warning_index_name_pre,\
                         weibo_timing_warning_index_name_pre,facebook_timing_warning_index_name_pre,twitter_timing_warning_index_name_pre

#writing_task
from global_utils import writing_task_index_name,writing_task_index_type


def public_delete_func(index_pre,datetime,day_num):
    date = ts2datetime(datetime - day_num*DAY)
    index_name = index_pre + date
    index_exist = es_xnr.indices.exists(index=index_name)
    if index_exist:
        es_xnr.indices.delete(index=index_name)

    return True


def outpublic_delete_func(index_pre,datetime,day_num):
    date = ts2datetime(datetime - day_num*DAY)
    index_name = index_pre + date
    index_exist = es_xnr_2.indices.exists(index=index_name)
    if index_exist:
        es_xnr_2.indices.delete(index=index_name)

    return True


def delete_weibo_feedback(datetime,day_num):
    public_delete_func(weibo_feedback_comment_index_name_pre,datetime,day_num)
    public_delete_func(weibo_feedback_retweet_index_name_pre,datetime,day_num)
    public_delete_func(weibo_feedback_private_index_name_pre,datetime,day_num)
    public_delete_func(weibo_feedback_at_index_name_pre,datetime,day_num)
    public_delete_func(weibo_feedback_like_index_name_pre,datetime,day_num)

    return True



def delete_new_xnr_flow_text(datetime,day_num):

    public_delete_func(new_xnr_flow_text_index_name_pre,datetime,day_num)
 
    return True 



def delete_group_message(datetime,day_num):

    public_delete_func(group_message_index_name_pre,datetime,day_num)

    return True     



def delete_twitter_flow_text(datetime,day_num):

    public_delete_func(twitter_flow_text_index_name_pre,datetime,day_num)

    return True



def delete_facebook_flow_text(datetime,day_num):

    public_delete_func(facebook_flow_text_index_name_pre,datetime,day_num)

    return True



def delete_twitter_count(datetime,day_num):

    public_delete_func(twitter_count_index_name_pre,datetime,day_num)

    return True


def delete_facebook_count(datetime,day_num):

    public_delete_func(facebook_count_index_name_pre,datetime,day_num)

    return True



def delete_tw_bci(datetime,day_num):

    public_delete_func(tw_bci_index_name_pre,datetime,day_num)

    return True


def delete_fb_bci(datetime,day_num):

    public_delete_func(fb_bci_index_name_pre,datetime,day_num)

    return True


def delete_wx_group_message(datetime,day_num):

    public_delete_func(wx_group_message_index_name_pre,datetime,day_num)

    public_delete_func(wx_sent_group_message_index_name_pre,datetime,day_num)

    return True


def delete_facebook_feedback(datetime,day_num):
    outpublic_delete_func(facebook_feedback_comment_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_feedback_retweet_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_feedback_private_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_feedback_at_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_feedback_like_index_name_pre,datetime,day_num)

    return True


def delete_fbnew_xnr_flow_text(datetime,day_num):

    outpublic_delete_func(new_fb_xnr_flow_text_index_name_pre,datetime,day_num)
 
    return True 


def delete_twitter_feedback(datetime,day_num):
    outpublic_delete_func(twitter_feedback_comment_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_feedback_retweet_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_feedback_private_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_feedback_at_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_feedback_like_index_name_pre,datetime,day_num)

    return True


def delete_twnew_xnr_flow_text(datetime,day_num):

    outpublic_delete_func(new_tw_xnr_flow_text_index_name_pre,datetime,day_num)
 
    return True 



def delete_community(datetime,day_num):

    public_delete_func(weibo_community_index_name_pre,datetime,day_num)

    delete_wbcommunity_temp_files(datetime)

    return True


def delete_wbcommunity_temp_files(datetime):
    dirToBeEmptied = './timed_python_files/community/weibo_data' #需要清空的文件夹

    ds = list(os.walk(dirToBeEmptied)) #获得所有文件夹的信息列表
    delta = datetime.timedelta(days=30) #设定30天前的文件为过期
    now = datetime #获取当前时间

    for d in ds: #遍历该列表
        os.chdir(d[0]) #进入本级路径，防止找不到文件而报错
        if d[2] != []: #如果该路径下有文件
            for x in d[2]: #遍历这些文件
            ctime = datetime.datetime.fromtimestamp(os.path.getctime(x)) #获取文件创建时间
            if ctime < (now-delta): #若创建于delta天前
                os.remove(x) #则删掉

    return True


def delete_user_warning(datetime,day_num):
    public_delete_func(weibo_user_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_user_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_user_warning_index_name_pre,datetime,day_num)

    return True


def delete_event_warning(datetime,day_num):
    public_delete_func(weibo_event_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_event_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_event_warning_index_name_pre,datetime,day_num)

    return True


def delete_speech_warning(datetime,day_num):
    public_delete_func(weibo_speech_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_speech_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_speech_warning_index_name_pre,datetime,day_num)

    return True


def delete_timing_warning(datetime,day_num):
    public_delete_func(weibo_timing_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(facebook_timing_warning_index_name_pre,datetime,day_num)
    outpublic_delete_func(twitter_timing_warning_index_name_pre,datetime,day_num)

    return True

def delete_writing_task():
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'compute_status':4}
                }
            }

        },
        'size':100
    }
    try:
        temp_result = es_xnr.search(index=writing_task_index_name,doc_type=writing_task_index_type,body=query_body)['hits']['hits']
        if temp_result:
            for item in temp_result:
                task_id = item['_id']
                try:
                    es_xnr.delete(index=writing_task_index_name,doc_type=writing_task_index_type,id=task_id)
                    result=True
                except:
                    result=False

    except:
        result = False

    return result


def delete_main_func(datetime):

    delete_weibo_feedback(datetime,feedback_day_num=30)

    delete_new_xnr_flow_text(datetime,new_xnr_flow_text_num=1000)

    delete_group_message(datetime,group_message_num=30)

    delete_twitter_flow_text(datetime,twitter_flow_text_num=8)

    delete_facebook_flow_text(datetime,facebook_flow_text_num=8)

    delete_twitter_count(datetime,twitter_count_num=2)

    delete_facebook_count(datetime,facebook_count_num=2)

    delete_tw_bci(datetime,tw_bci_num=8)

    delete_fb_bci(datetime,fb_bci_num=8)

    delete_writing_task()

    #hmc
    clean_wx_group_media_files()

    delete_wx_group_message(datetime,wx_group_message_num=30)

    delete_facebook_feedback(datetime,day_num=30)

    delete_fbnew_xnr_flow_text(datetime,day_num=1000)

    delete_twitter_feedback(datetime,day_num=30)

    delete_twnew_xnr_flow_text(datetime,day_num=1000)

    #qxk
    delete_community(datetime,day_num=180)

    delete_user_warning(datetime,day_num=1000)

    delete_event_warning(datetime,day_num=1000)

    delete_speech_warning(datetime,day_num=365)

    delete_timing_warning(datetime,day_num=2000)
    

if __name__ == '__main__':
    datetime = int(time.time())
    delete_main_func(datetime)



