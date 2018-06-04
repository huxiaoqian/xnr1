# -*- coding: utf-8 -*-
import os
import json
import time
import sys

from datetime import datetime,date

sys.path.append('../../')
from parameter import DAY
from time_utils import ts2datetime,datetime2ts

from global_utils import R_WEIBO_COMMUNITY_CREATE as r_community
from global_utils import weibo_community_find_task_queue_name,weibo_community_select_task_queue_name,\
                         weibo_community_trace_task_queue_name
from global_utils import es_xnr,weibo_community_status_index_name,weibo_community_status_index_type

sys.path.append('../../timed_python_files/community/')
from weibo_publicfunc import get_compelete_wbxnr
from community_find_weibo import create_weibo_community
from weibo_select_community import get_final_community
from weibo_trace_community import trace_xnr_community,get_trace_community

sys.path.append('../../timed_python_files/community/mappings/')
from weibo_community_discovery_mappings import weibo_community_mappings
from weibo_trace_community_mappings import weibo_trace_community_mappings

#状态表状态查询,如果没有状态返回-1
#如果生成了状态是0
#如果选择了状态是1
def get_day_status(xnr_user_no,datetime):
    task_id = xnr_user_no + '_' + ts2datetime(datetime)
    try:
        result = es_xnr.get(index=weibo_community_status_index_name,doc_type=weibo_community_status_index_type,id=task_id)['_source']
        status = result['status']
    except:
        status = -1
    return status



#from datetime import datetime
#global datetime
#将生成社区加入队列
def push_create_community():
    #判断日期，等于0表示是周一
    from datetime import datetime
    dayOfWeek = datetime.today().weekday()

    #生成日期-周日
    datetime = int(time.time()) - DAY

    #虚拟人列表
    xnr_user_no_list = get_compelete_wbxnr()

    if dayOfWeek == 0:
        weibo_community_mappings(ts2datetime(datetime))
        for xnr_user_no in xnr_user_no_list:
            weibo_trace_community_mappings(xnr_user_no)
            #判断当天状态表情况
            status_mark = get_day_status(xnr_user_no,datetime)
            if status_mark < 0:
                task_dict = dict()
                task_dict['xnr_user_no'] = xnr_user_no
                task_dict['datetime'] = datetime
                #将计算任务加入队列
                r_community.lpush(weibo_community_find_task_queue_name,json.dumps(task_dict))
    print '已经把生成社区任务加入队列！！！'



#将选择社区加入队列
def push_select_community():
    #判断日期，等于0表示是周一
    from datetime import datetime
    dayOfWeek = datetime.today().weekday()

    #生成日期-周日
    datetime = int(time.time()) - DAY


    #虚拟人列表
    xnr_user_no_list = get_compelete_wbxnr()



    if dayOfWeek == 0:
        for xnr_user_no in xnr_user_no_list:
            #判断当天状态表情况
            status_mark = get_day_status(xnr_user_no,datetime)
            if status_mark == 0:
                task_dict = dict()
                task_dict['xnr_user_no'] = xnr_user_no
                task_dict['datetime'] = datetime
                #将计算任务加入队列
                r_community.lpush(weibo_community_select_task_queue_name,json.dumps(task_dict))
    print '已经把选择社区任务加入队列！！！'



#将跟踪社区加入队列
def push_trace_community():
    #判断日期，等于0表示是周一
    from datetime import datetime
    dayOfWeek = datetime.today().weekday()

    #生成日期-周日
    datetime = int(time.time()) - DAY

    #社区列表
    community_list = get_trace_community(datetime)

    #虚拟人列表
    xnr_user_no_list = get_compelete_wbxnr()

    if dayOfWeek != 0:
        for community in community_list:
            task_dict = dict()
            task_dict['community'] = community
            task_dict['datetime'] = datetime
            #将计算任务加入队列
            r_community.lpush(weibo_community_trace_task_queue_name,json.dumps(task_dict))
    else:
        num = 0
        for xnr_user_no in xnr_user_no_list:
            status_mark = get_day_status(xnr_user_no,datetime)
            num = num + status_mark
        if num == len(xnr_user_no_list):
            for community in community_list:
                task_dict = dict()
                task_dict['community'] = community
                task_dict['datetime'] = datetime
                #将计算任务加入队列
                r_community.lpush(weibo_community_trace_task_queue_name,json.dumps(task_dict))

    print '已经把跟踪社区任务加入队列！！！'



#pop生成社区任务
def rpop_create_community():

    while True:
        temp = r_community.rpop(weibo_community_find_task_queue_name)

        # print 'temp:::::',temp
        if not temp:
            print '当前没有生成社区任务'         
            break
        task_detail = json.loads(temp)
        xnr_user_no = task_detail['xnr_user_no']
        datetime = task_detail['datetime']
        task_id = xnr_user_no + '_' + ts2datetime(datetime)
        print 'task_detail::',task_detail

        print '把任务从队列中pop出来......'

        mark = create_weibo_community(xnr_user_no,datetime)

        task_detail['date'] = ts2datetime(datetime)

        task_detail['status'] = 0

        if mark:
            es_xnr.index(index=weibo_community_status_index_name,doc_type=weibo_community_status_index_type,\
                id=task_id, body=task_detail)


#pop选择社区任务
def rpop_select_community():

    while True:
        temp = r_community.rpop(weibo_community_select_task_queue_name)

        # print 'temp:::::',temp
        if not temp:
            print '当前没有选择社区任务'         
            break
        task_detail = json.loads(temp)
        xnr_user_no = task_detail['xnr_user_no']
        datetime = task_detail['datetime']
        task_id = xnr_user_no + '_' + ts2datetime(datetime)
        print 'task_detail::',task_detail

        print '把任务从队列中pop出来......'

        mark = get_final_community(xnr_user_no,datetime)

        if mark:
            es_xnr.update(index=weibo_community_status_index_name,doc_type=weibo_community_status_index_type,\
                id=task_id, body={'doc':{'status':1}})


#pop跟踪社区任务
def rpop_trace_community():

    while True:
        temp = r_community.rpop(weibo_community_trace_task_queue_name)

        # print 'temp:::::',temp
        if not temp:
            print '当前没有跟踪社区任务'         
            break
        task_detail = json.loads(temp)
        community = task_detail['community']
        datetime = task_detail['datetime']

        print 'task_detail::',task_detail

        print '把任务从队列中pop出来......'

        trace_xnr_community(community,datetime)

        print '完成'+community['community_name'] +'社区跟踪任务！'



if __name__ == '__main__':
#push
    push_create_community()
    rpop_create_community()

    push_select_community()
    rpop_select_community()

    push_trace_community()
    rpop_trace_community()
#pop
    #rpop_create_community()

    #rpop_select_community()

    #rpop_trace_community()
