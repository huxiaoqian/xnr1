#-*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.getcwd())
sys.path.append('../')
from global_utils import es_xnr, r_wx, wx_xnr_index_name, wx_xnr_index_type
sys.path.append('../wx/')
from control_bot import check_status, login_wx_xnr, send_qrcode2mail


def load_wx_xnr():
    wxbot_id_list = []
    query_body = {}
    try:
        res = es_xnr.search(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, body=query_body)['hits']['hits']
        for r in res:
	    wxbot_id = r['_source']['xnr_user_no']
	    status = check_status(wxbot_id)
	    if not status == 'listening':
	        wxbot_id_list.append(wxbot_id)
    except Exception,e:
	print 'load_wx_xnr Exception: ', str(e)
    return wxbot_id_list


def auto_start():
    wxbot_id_list = load_wx_xnr()
    print wxbot_id_list
    for wxbot_id in wxbot_id_list:
	print wxbot_id
	qr_path = login_wx_xnr(wxbot_id)
	print wxbot_id, ' auto_start result: ', qr_path

if __name__ == '__main__':
    auto_start()
  

