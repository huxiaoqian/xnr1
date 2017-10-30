# -*- coding: utf-8 -*-
import time
from global_utils import wx_group_message_index_name_pre
from parameter import DAY

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
