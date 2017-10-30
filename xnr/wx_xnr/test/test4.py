#-*- coding: utf-8 -*-
import subprocess

ABS_LOGIN_PATH = '/home/ubuntu8/hanmc/git/repo/xnr1/xnr/wx_xnr/test/test5.py'
def test():
    name = 'hanmc'
    pwd = '123456'
    p_str1 = 'python '+ ABS_LOGIN_PATH + ' -n '+ name + ' -p ' + pwd + ' >> test5.txt'
    print p_str1
    command_str = 'python '+ ABS_LOGIN_PATH + ' -n '+ name + ' -p ' + pwd
    p_str2 = 'pgrep -f ' + '"' + command_str + '"'

    process_ids = subprocess.Popen(p_str2, \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_id_list = process_ids.stdout.readlines()
    
    for process_id in process_id_list:
        process_id = process_id.strip()
        kill_str = 'kill -9 ' + process_id
        print 'kill_str::',kill_str
        p2 = subprocess.Popen(kill_str, \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    p2 = subprocess.Popen(p_str1, \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p2.pid
    

print test()