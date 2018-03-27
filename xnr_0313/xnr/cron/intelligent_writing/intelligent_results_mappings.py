# -*-coding:utf-8-*-

import os
import sys
import json

reload(sys)
sys.path.append('../../')

from global_utils import es_intel as es
from global_utils import intel_opinion_results_index_name,intel_type_all, intel_type_follow, \
                intel_type_influence, intel_type_sensitive, \
                topics_river_index_name, topics_river_index_type, \
                timeline_index_name, timeline_index_type,\
                intel_models_text_index_name, intel_models_text_index_type

def intel_opinion_results_mappings(index_type):

    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            index_type:{
                'properties':{
                    'task_id':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'content':{
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=intel_opinion_results_index_name)
    if not exist_indice:
        es.indices.create(index=intel_opinion_results_index_name, body=index_info, ignore=400)

def topic_river_results_mappings():

    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            topics_river_index_type:{
                'properties':{
                    'task_id':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'content':{
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=topics_river_index_name)
    if not exist_indice:
        es.indices.create(index=topics_river_index_name, body=index_info, ignore=400)

def timeline_results_mappings():

    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            timeline_index_type:{
                'properties':{
                    'task_id':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'content':{
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=timeline_index_name)
    if not exist_indice:
        es.indices.create(index=timeline_index_name, body=index_info, ignore=400)


def models_text_mappings():

    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            intel_models_text_index_type:{
                'properties':{
                    'task_id':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'model_text_pos':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'model_text_neg':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'model_text_news':{
                        'type':'string',
                        'index':'not_analyzed'
                    }
                }
            }
        }
    }


    exist_indice = es.indices.exists(index=intel_models_text_index_name)
    if not exist_indice:
        es.indices.create(index=intel_models_text_index_name, body=index_info, ignore=400)


if __name__ == '__main__':

    #topic_river_results_mappings()
    #timeline_results_mappings()
    es.indices.delete(index=intel_models_text_index_name)
    models_text_mappings()