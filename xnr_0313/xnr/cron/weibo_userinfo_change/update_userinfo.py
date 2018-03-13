#-*- coding:utf-8 -*-
import sys
import json
reload(sys)
sys.path.append('../../')
from global_utils import r, update_userinfo_queue_name

def update_userinfo():
    results = dict()
    while True:
        task = r.rpop(update_userinfo_queue_name)
        if not task:
            break
        else:
            task_dict = json.loads(task)
            task_id = task_dict['task_id']
            weibo_mail_account = task_dict['weibo_mail_account']
            weibo_phone_account = task_dict['weibo_phone_account']
            pwd = task_dict['password']
            if weibo_mail_account:
                uname = weibo_mail_account
            elif weibo_phone_account:
                uname = weibo_phone_account
            else:
                break
            new_userinfo_dict = get_userinfo(uname, pwd)
            if new_userinfo_dict:
                update_dict = {'age': new_userinfo_dict['birth'],\
                        'job':new_userinfo_dict['job']}
                es.update(index=weibo_xnr_index_name,\
                    doc_type=weibo_xnr_index_type,id=task_id,body={'doc':item_exist})



if __name__=='__main__':
    update_userinfo()
