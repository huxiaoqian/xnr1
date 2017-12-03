#-*- coding: utf-8 -*-
import subprocess
import sys
import getopt
from xnr.wx.MyBot import MyBot

def run_bot(wxbot_id, wxbot_port, groups_list):
    try :
        bot = MyBot(wxbot_id=wxbot_id, wxbot_port=wxbot_port, init_groups_list=groups_list)
        bot.listen()
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
        print e