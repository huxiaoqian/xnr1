# -*- coding: utf-8 -*-
import time
import datetime
from xnr.global_utils import es_xnr,wx_xnr_index_name,wx_xnr_index_type,\
                             wx_group_message_index_name_pre, wx_group_message_index_type,\
                             wx_report_management_index_name, wx_report_management_index_type
from xnr.parameter import MAX_VALUE, DAY
from xnr.time_utils import get_wx_groupmessage_index_list, ts2datetime, datetime2ts
from xnr.wx.control_bot import load_wxxnr_redis_data
import sys
sys.path.append('../cron/trans')
from trans import trans as text_trans


def utils_text_trans(q):
    return text_trans(q)

def utils_voice_trans(res):
    pass
