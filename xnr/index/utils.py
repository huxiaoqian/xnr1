# -*- coding: utf-8 -*-
import time
import os
import sys
trans_path = os.path.join(os.path.abspath(os.getcwd()), 'xnr/cron/trans/')
sys.path.append(trans_path)
from trans import trans as text_trans
from trans import voice2text

def utils_text_trans(q):
    q_list = [q]
    result_list = text_trans(q_list)
    try:
        return result_list[0]
    except:
        return ''

def utils_voice_trans(voice_path):
    if os.path.isfile(voice_path):
        r = voice2text(voice_path)
        if r:
            return r
    return False