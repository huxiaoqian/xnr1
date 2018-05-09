# -*- coding: utf-8 -*-
import os
import json
import time
import sys

from weibo_publicfunc import get_compelete_wbxnr
from community_find_weibo import create_weibo_community
sys.path.append('../')
from global_utils import es_xnr,opinion_corpus_index_name,opinion_corpus_index_type
from global_utils import R_OPINION as r_r
from global_utils import opinion_expand_task_queue_name

