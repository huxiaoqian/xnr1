# -*- coding: utf-8 -*-

import time
from global_utils import flow_text_index_name_pre,group_message_index_name_pre,xnr_flow_text_index_name_pre,\
                        xnr_flow_text_index_type,facebook_flow_text_index_name_pre,\
                        facebook_count_index_name_pre,twitter_flow_text_index_name_pre,\
                        twitter_count_index_name_pre,\
                        xnr_flow_text_index_type, wx_group_message_index_name_pre, \
                        fb_bci_index_name_pre, tw_bci_index_name_pre, facebook_flow_text_index_name_pre,\
                        twitter_flow_text_index_name_pre
from global_config import R_BEGIN_TIME,S_TYPE
from parameter import MAX_FLOW_TEXT_DAYS,DAY,FLOW_TEXT_START_DATE

def unix2hadoop_date(ts):
    return time.strftime('%Y_%m_%d', time.localtime(ts))

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def ts2yeartime(ts):
    return time.strftime('%Y', time.localtime(ts))

def ts2date(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def ts2date_min(ts):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))

def date2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

def window2time(window, size=24*60*60):
    return window*size

def datetimestr2ts(date):
    return time.mktime(time.strptime(date, '%Y%m%d'))

def ts2datetimestr(ts):
    return time.strftime('%Y%m%d', time.localtime(ts))

def ts2HourlyTime(ts, interval):
    # interval 取 Minite、Hour
    ts = ts - ts % interval
    return ts

def ts2datetime_full(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ts))

def ts2datehour(ts):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))

def datehour2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M')))




#use to get retweet/be_retweet/comment/be_comment db_number
#input: timestamp
#output: db_number
r_beigin_ts = datetime2ts(R_BEGIN_TIME)
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) % 2 + 1
    if S_TYPE == 'test':
        db_number = 1
    return db_number

def get_flow_text_index_list(date_range_end_ts):
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = flow_text_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)

    return index_name_list

def fb_get_flow_text_index_list(date_range_end_ts):
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = facebook_flow_text_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)

    return index_name_list

def tw_get_flow_text_index_list(date_range_end_ts):
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = twitter_flow_text_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)

    return index_name_list

def get_day_flow_text_index_list(date_ts):
    day_date=ts2datetime(date_ts)
    index_name = flow_text_index_name_pre + day_date

    return index_name


def get_xnr_flow_text_index_list(date_range_end_ts):
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = xnr_flow_text_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    
    return index_name_list

def get_xnr_feedback_index_listname(index_name_pre,date_range_end_ts):
    index_name_list=[]
    date_range_start_ts=FLOW_TEXT_START_DATE
    if ts2datetime(date_range_start_ts) != ts2datetime(date_range_end_ts):
        iter_date_ts=date_range_end_ts
        while iter_date_ts >= date_range_start_ts:
            date_range_start_date=ts2datetime(iter_date_ts)
            index_name=index_name_pre+date_range_start_date
            index_name_list.append(index_name)
            iter_date_ts=iter_date_ts-DAY
    else:
        date_range_start_date=ts2datetime(date_range_start_ts)
        index_name=index_name_pre+date_range_start_date
        index_name_list.append(index_name)
    return index_name_list


def get_xnr_flow_text_index_listname(index_name_pre,date_range_start_ts,date_range_end_ts):
    index_name_list=[]
    #date_range_start_ts=FLOW_TEXT_START_DATE
    if ts2datetime(date_range_start_ts) != ts2datetime(date_range_end_ts):
        iter_date_ts=date_range_end_ts
        while iter_date_ts >= date_range_start_ts:
            date_range_start_date=ts2datetime(iter_date_ts)
            #print date_range_start_date,ts2datetime(date_range_start_ts),ts2datetime(date_range_end_ts)
            index_name=index_name_pre+date_range_start_date
            index_name_list.append(index_name)
            iter_date_ts=iter_date_ts-DAY
            #print ts2datetime(iter_date_ts),iter_date_ts,date_range_start_ts
    else:
        date_range_start_date=ts2datetime(date_range_start_ts)
        index_name=index_name_pre+date_range_start_date
        index_name_list.append(index_name)
    return index_name_list

# use to search certain period of group message without the upper bound of days limit

def get_groupmessage_index_list(startdate,enddate):

    index_name_list = []
    days_num = (datetime2ts(enddate)-datetime2ts(startdate))/DAY

    for i in range(0,(days_num+1)):
        date_range_start_ts = datetime2ts(startdate) + i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = group_message_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)

    return index_name_list


def get_timeset_indexset_list(index_name_pre,startdate,enddate):

    index_name_list = []
    days_num = (datetime2ts(enddate)-datetime2ts(startdate))/DAY

    for i in range(0,(days_num+1)):
        date_range_start_ts = datetime2ts(startdate) + i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)

    return index_name_list

def get_timets_set_indexset_list(index_name_pre,start_ts,endts_):

    index_name_list = []
    days_num = (datetime2ts(ts2datetime(start_ts))-datetime2ts(ts2datetime(start_ts)))/DAY

    for i in range(0,(days_num+1)):
        date_range_start_ts = datetime2ts(ts2datetime(start_ts)) + i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)

    return index_name_list

def get_facebook_flow_text_index_list(date_range_end_ts):
    ## 不包括 date_range_end_ts 这天
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = facebook_flow_text_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    
    return index_name_list

def get_facebook_count_index_list(date_range_end_ts):
    ## 不包括 date_range_end_ts 这天
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = facebook_count_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    
    return index_name_list

def get_fb_bci_index_list(date_range_end_ts):
    ## 不包括 date_range_end_ts 这天
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = fb_bci_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    
    return index_name_list

def get_twitter_flow_text_index_list(date_range_end_ts):
    ## 不包括 date_range_end_ts 这天
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = twitter_flow_text_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    
    return index_name_list

def get_tw_bci_index_list(date_range_end_ts):
    ## 不包括 date_range_end_ts 这天
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = tw_bci_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    
    return index_name_list

def get_twitter_count_index_list(date_range_end_ts):
    ## 不包括 date_range_end_ts 这天
    index_name_list = []
    days_num = MAX_FLOW_TEXT_DAYS
    for i in range(1,(days_num+1)):
        date_range_start_ts = date_range_end_ts - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = twitter_count_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    
# use to search certain period of group message without the upper bound of days limit
def get_wx_groupmessage_index_list(startdate,enddate):
    index_name_list = []
    days_num = (datetime2ts(enddate)-datetime2ts(startdate))/DAY
    for i in range(0,(days_num+1)):
        date_range_start_ts = datetime2ts(startdate) + i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        index_name = wx_group_message_index_name_pre + date_range_start_datetime
        index_name_list.append(index_name)
    return index_name_list
