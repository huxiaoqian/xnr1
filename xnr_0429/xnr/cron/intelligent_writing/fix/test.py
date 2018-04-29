# -*- coding: utf-8 -*-
import os
import sys
import json 
sys.path.append('../../../../')
from global_config import db,weibo_es,weibo_index_name,weibo_index_type,MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO,\
                            topics_river_index_name,topics_river_index_type,subopinion_index_name,subopinion_index_type

index_body={'name':'aoyunhui','start_ts':1468944000,'end_ts':1468944000,'features':'3','keys':'4','cluster_dump_dict':'5'}
        
print weibo_es
print weibo_es.delete(index=topics_river_index_name,doc_type=topics_river_index_type,id='aoyunhui_1468944000_1471622400')


   # index_body={'name':task[0],'start_ts':task[1],'end_ts':task[2],'features':json.dumps(features),'cluster_dump_dict':json.dumps(cluster_dump_dict)}
    # weibo_es.index(index=topics_river_index_name,doc_type=topics_river_index_type,id=taskid,body=index_body)
