# -*- coding: utf-8 -*-
import time

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


if __name__ == '__main__':
    print time.time()
    print ts2datetime(time.time())
    print datetime2ts(ts2datetime(time.time()))
    print ts2datetime(datetime2ts(ts2datetime(time.time())))
