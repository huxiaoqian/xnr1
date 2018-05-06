#-*- coding: utf-8 -*-
import subprocess
import sys
import os
import getopt
sys.path.append(os.getcwd())
path1 = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
sys.path.append(path1)
sys.path.append(os.path.join(path1, 'wx'))
print sys.path
print os.path.join(path1, 'wx')
print 'path1: ', path1
from MyWXBot import remove_wx_media_old_files
print remove_wx_media_old_files
sys.path.append('..')
from wx import MyWXBot
print MyWXBot.__file__
#MyWXBot.Mybot
#from MyWXBot import Mybot
sys.path.append('../../../')
from xnr.wx.MyWXBot import MyBot

def run_bot(wxbot_id, wxbot_port, groups_list):
    try :
        bot = MyBot(wxbot_id=wxbot_id, wxbot_port=wxbot_port, init_groups_list=groups_list)
        print 'run_bot bot'
        bot.listen()
        print 'run_bot listen'
    except Exception,e:
        print e

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:p:g:')
        groups_list = ''
        for op, value in opts:
            if op == '-i':
                wxbot_id = value
            elif op == '-p':
                wxbot_port = int(value)
            elif op == '-g':
                groups_list = value
        print 'start_bot: ', wxbot_id, wxbot_port, groups_list
        run_bot(wxbot_id, wxbot_port, groups_list)
    except Exception,e:
        print 'run_bot.py Exception:', str(e)
