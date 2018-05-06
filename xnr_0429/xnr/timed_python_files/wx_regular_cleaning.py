# -*- coding:utf-8 -*-
import time
import os
import sys
sys.path.append('../')
from time_utils import ts2datetime, datetime2ts
from global_config import WX_IMAGE_ABS_PATH, WX_VOICE_ABS_PATH
from parameter import DAY
import shutil 

#清理wx群组消息保存下来的图片、语音文件
def clean_wx_group_media_files():
    remove_wx_media_old_files(WX_IMAGE_ABS_PATH)
    remove_wx_media_old_files(WX_VOICE_ABS_PATH)
    #imageslim(WX_IMAGE_ABS_PATH)

def load_legal_filepath_suf_list(period):
    legal_filepath_suf_list = []
    for i in range(0, period):
        date_range_start_ts = time.time() - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        legal_filepath_suf_list.append(date_range_start_datetime)
    return legal_filepath_suf_list

def remove_wx_media_old_files(filepath_pre, period=30):
    #遍历filepath_pre下的文件夹，如果不在最近30天内，则删除
    #1、得到合法的（在period内）文件夹名
    legal_filepath_suf_list = load_legal_filepath_suf_list(period)
    filepath_suf_list = os.listdir(filepath_pre) #得到文件夹下的所有文件名称 
    for filepath_suf in filepath_suf_list: #遍历文件夹  
        filepath = os.path.join(filepath_pre, filepath_suf)
        if os.path.isdir(filepath):
            if not filepath_suf in legal_filepath_suf_list:
                shutil.rmtree(filepath)
    print 'remove ok'

if __name__ == '__main__':
    clean_wx_group_media_files()
