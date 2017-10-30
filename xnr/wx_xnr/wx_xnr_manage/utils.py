# -*- coding: utf-8 -*-
import time
import socket
import json
from multiprocessing import Process
from xnr.wx_xnr.global_utils import es_xnr, wx_xnr_index_name, wx_xnr_index_type, wx_xnr_history_count_index_name, \
                        wx_xnr_history_count_index_type, wx_group_message_index_name_pre, wx_group_message_index_type
from xnr.wx_xnr.parameter import MAX_VALUE, LOCALHOST_IP
from xnr.wx_xnr.xnr_utils import user_no2wxbot_id
from xnr.wx_xnr.wx.MyBot import MyBot
from xnr.wx_xnr.wx.control_bot import create_wx_xnr, load_all_groups, set_groups, check_status, xnr_logout, login_wx_xnr, show_wx_xnr, delete_wx_xnr

def utils_create_xnr(xnr_info):
	return create_wx_xnr(xnr_info)

def utils_load_all_groups(wxbot_id):
	return load_all_groups(wxbot_id)

def utils_set_groups(wxbot_id, group_list):
	return set_groups(wxbot_id, group_list)

def utils_logout(wxbot_id):
	return xnr_logout(wxbot_id)

def utils_login(wxbot_id):
	return login_wx_xnr(wxbot_id)

def utils_check_status(wxbot_id):
	return check_status(wxbot_id)

def utils_show_wxxnr():
	return show_wx_xnr()

def utils_delete(wxbot_id):
	return delete_wx_xnr(wxbot_id)