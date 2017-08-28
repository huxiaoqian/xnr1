# -*-coding: utf-8-*-
import os
import sys
import time
import subprocess

reload(sys)
sys.path.append('../')
from global_utils import QRCODE_PATH

#QRCODE_PATH = '/root/.qqbot-tmp/'

def getQRCode():
    filenames = os.listdir(QRCODE_PATH)
    filenames.sort(compare)

    for filename in filenames:
        if '.png' in filename:
            print QRCODE_PATH + filename

            # mtime = time.ctime(os.path.getmtime(QRCODE_PATH + filename))  # modify time
            # ctime = time.ctime(os.path.getctime(QRCODE_PATH + filename))  # create time
            # print mtime, ctime
            return QRCODE_PATH + filename
    return QRCODE_PATH


def compare(x, y):
    stat_x = os.stat(QRCODE_PATH + x)
    stat_y = os.stat(QRCODE_PATH + y)
    if stat_x.st_ctime > stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime < stat_y.st_ctime:
        return 1
    else:
        return 0

def getQRCode_v2(qq_xnr):
    #read qq_xnr es to get qqbot_port
    '''
    try:
        qq_xnr_es_result = es.get(index_name=qq_xnr_index_name, doc_type=qq❯
                    id=qq_xnr,_source=True)['_source']
        qqbot_port = qq_xnr_es_result['qqbot_port']
    except:
        print 'qq_xnr is not exist'
        qqbot_port = ''
        return 'qqbot_port is not exist'
    '''
    #mkdir for save qq_xnr png
    #test
    qqbot_port = '8189'
    
    p_str0 = 'mkdir '+ QRCODE_PATH + qqbot_port
    os.system(p_str0)
    #p1 = subprocess.Popen(p_str0, \
    #    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #login QQbot
    p_str1 = 'python receiveQQGroupMessage.py -i '+qqbot_port + ' >> login'+qqbot_port+'.txt'
    print 'p_str1:', p_str1
    p2 = subprocess.Popen(p_str1, \
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #get login png filename
    print 'curdir:', os.getcwd()
    filenames1 = os.listdir(os.getcwd())
    print 'filename1:', filenames1
    port_dir = QRCODE_PATH+qqbot_port
    print 'port_dir:', port_dir
    os.system('chmod 777 '+port_dir)
    filenames = os.listdir(port_dir)
    print 'filenames:', filenames
    fileitem = [[filename, os.stat(port_dir+filename).st_mtime] for filename in filenames]
    print 'fileitem:', fileitem
    new_fileitem = sorted(fileitem, key=lambda x:x[1], reverse=True)[0]
    new_filepath = new_fileitem[0]
    return new_filepath
    

if __name__ == '__main__':
    #getQRCode()
    qq_xnr = '841319111'
    new_filepath = getQRCode_v2(qq_xnr)
    print 'new_filepath:', new_filepath
