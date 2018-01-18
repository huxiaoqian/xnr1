# -*- coding: utf-8 -*-
import time
import os
import sys
trans_path = os.path.join(os.path.abspath(os.getcwd()), 'xnr/cron/trans/')
sys.path.append(trans_path)
from trans import trans as text_trans

def utils_text_trans(q):
    return text_trans(q)

def utils_voice_trans(res):
    pass