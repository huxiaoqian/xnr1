# -*- coding: UTF-8 -*-
import sys
import json
from elasticsearch.helpers import scan

sys.path.append('../')
from global_utils import es_user_portrait

index_name = 'manage_sensing_task'
index_type = 'task'

def main():
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}, 'size':1}, index=index_name, doc_type=index_type)
    count = 0
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            task_name = scan_re['task_name']
            history_status = json.loads(scan_re['history_status'])
            #iter history status
            new_history_status = []
            for history_item in history_status:
                history_item_last = history_item[-1]
                if history_item_last == u'':
                    new_history_item = history_item[:-1]
                    new_history_item.append("0")
                    new_history_status.append(new_history_item)
                else:
                    new_history_status.append(history_item)
                    new_history_item = history_item
            print 'new_history_status:', new_history_status
            es_user_portrait.update(index=index_name, doc_type=index_type, \
                    id=task_name, body={'doc':{'history_status': json.dumps(new_history_status)}})
        except StopIteration:
            print 'all done'
            break
        except Exception as e:
            raise e
    print 'count:', count


if __name__=='__main__':
    main()
