# -*- coding: utf-8 -*-
import sys
import redis
import subprocess
sys.path.append('../')


from global_utils import r, qq_document_task_name

def main():
    while True:
        task_result = r.rpop(qq_document_task_name)
        if task_result:
            task_info_dict =json.loads(task_result)
            qq_xnr = task_info_dict['qq_xnr']
            qqbot_port = task_info_dict['qqbot_port']
            p_str = 'python receiveQQGroupMessage.py -i '+port+' >> login'+port+'.txt'
            p = subprocess.Popen(p_str, \
                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            break



if __name__=='__main__':
    #main()
    #test
    
    port_list = ['8193', '8192']
    for port in port_list:
        p_str1 = 'mkdir /root/.qqbot-tmp/'+port
        p = subprocess.Popen(p_str1, \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p_str = 'python receiveQQGroupMessage.py -i '+port+ '-b /root/.qqbot-tmp/'+ port + ' >> login'+port+'.txt'
        p = subprocess.Popen(p_str, \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
