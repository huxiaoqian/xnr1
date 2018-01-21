# -*- coding: utf-8 -*-
import time
import os
import sys
trans_path = os.path.join(os.path.abspath(os.getcwd()), 'xnr/cron/trans/')
sys.path.append(trans_path)
from trans import trans as text_trans

def utils_text_trans(q):
    q_list = [q]
    result_list = text_trans(q_list)
    try:
        return result_list[0]
    except:
        return ''

def utils_voice_trans(res):
    pass