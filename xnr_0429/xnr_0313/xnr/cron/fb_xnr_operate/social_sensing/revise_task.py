# -*- coding:utf-8 -*-
import json
import sys
reload(sys)
sys.path.append('../../')
from global_utils import R_SOCIAL_SENSING as r
from global_utils import es_user_portrait as es
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_name
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from time_utils import ts2datetime, datetime2ts, ts2date


task_name = "两会".decode('utf-8')
task_detail = es.get(index="manage_sensing_task", doc_type="task", id=task_name)['_source']
#task_detail['create_at'] = 1456934400
#task_detail['keywords'] = json.dumps(["两会", "人大", "政协"])
#task_detail['sensitive_words'] = json.dumps([])
#task_detail['task_type'] = "2"
task_detail['stop_time'] = '1457020800'
task_detail['finish'] = '1'
task_detail['processing_status'] = "0"
es.index(index="manage_sensing_task", doc_type="task", id=task_name, body=task_detail)
print task_detail
