#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
#import os
import time
base_path = '/home/xnr1/xnr_0429/xnr/timed_python_files'

def test(index_pre, user_index, redis_task):
    base_str = 'python /home/xnr1/xnr_0429/xnr/timed_python_files/fb_tw_trans_base.py -t ' + index_pre + ' -u ' + user_index + ' -r ' + redis_task

    p_str1 = base_str
 
    command_str = base_str
    p_str2 = 'pgrep -f ' + '"' + command_str + '"'
    process_ids = subprocess.Popen(p_str2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_id_list = process_ids.stdout.readlines()
    for process_id in process_id_list:
        process_id = process_id.strip()
        kill_str = 'kill -9 ' + process_id
        p2 = subprocess.Popen(kill_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    print p_str1
    p2 = subprocess.Popen(p_str1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 

    for line in p2.stdout.readlines():
        print 'line: ', line

if __name__ == '__main__':
    print 'start'
    print time.time() 
    print 'twitter flow text'
    test(index_pre='twitter_flow_text_', user_index='twitter_user', redis_task='twitter_flow_text_trans_task')
    print 'facebook flow text'
    test(index_pre='facebook_flow_text_', user_index='facebook_user', redis_task='facebook_flow_text_trans_task')
    print 'facebook user'
    test(index_pre='facebook_user', user_index='facebook_user', redis_task='facebook_user_trans_task')
    print 'twitter user'
    test(index_pre='twitter_user', user_index='twitter_user', redis_task='twitter_user_trans_task')
