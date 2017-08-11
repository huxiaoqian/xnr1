# -*-coding: utf-8-*-
import sys
import time
import datetime
import re

sys.path.append('..')

from tools.Pattern import getMatch

def getTimeStamp(timestamp):
    if isinstance(timestamp, unicode):
        timestamp = timestamp.encode('utf-8', 'ignore')

    year = re.search('\d{4}-\d+-\d+', timestamp)
    if year:
        timeformat = time.mktime(time.strptime(timestamp, '%Y-%m-%d %H:%M'))
        timestamp = str(timeformat)[:-2]
    elif re.search('月', timestamp):
        cur = datetime.datetime.now().year
        dateString = str(cur) + '年' + timestamp
        timeformat = time.mktime(time.strptime(dateString, '%Y年%m月%d日 %H:%M'))
        timestamp = str(timeformat)[:-2]
    elif re.search('今天', timestamp):
        timeformat = time.strftime('%Y-%m-%d', time.localtime())
        dateString = str(timeformat) + timestamp.replace('今天', '')
        timeformat = time.mktime(time.strptime(dateString, '%Y-%m-%d %H:%M'))
        timestamp = str(timeformat)[:-2]
    elif re.search('前', timestamp):
        dateString = getDatetime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), timestamp)
        if dateString:
            date_str = str(dateString)[:-3]
            timeformat = time.mktime(time.strptime(date_str, '%Y-%m-%d %H:%M'))
            timestamp = str(timeformat)[:-2]

    return timestamp

def getDatetime(curtime, timeString):
    dateString = None
    curtime = datetime.datetime.strptime(curtime, "%Y-%m-%d %H:%M:%S")
    if timeString.find(u'秒前') > -1:
        temp_time = getMatch(timeString, '^\d+')
        dateString = curtime - datetime.timedelta(seconds=long(temp_time))
    if timeString.find(u'分钟前') > -1:
        temp_time = getMatch(timeString, '\d+')
        dateString = curtime - datetime.timedelta(minutes=long(temp_time))
    if timeString.find(u'小时前') > -1:
        temp_time = getMatch(timeString, '\d+')
        dateString = curtime - datetime.timedelta(hours=long(temp_time))
    if timeString.find(u'天前') > -1:
        temp_time = getMatch(timeString, '\d+')
        dateString = curtime - datetime.timedelta(days=long(temp_time))
    return dateString