#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
from xnr.global_utils import es_xnr,facebook_xnr_corpus_index_name,facebook_xnr_corpus_index_type



#step 2: show corpus
def show_corpus_facebook(corpus_type):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'corpus_type':corpus_type}
                }
            }

        },
        'size':MAX_VALUE
    }
    result=es.search(index=facebook_xnr_corpus_index_name,doc_type=facebook_xnr_corpus_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results


def show_corpus_class_facebook(create_type,corpus_type):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'term':{'corpus_type':corpus_type},
                    'term':{'create_type':create_type}
                }
            }

        },
        'size':MAX_VALUE
    }
    result=es.search(index=facebook_xnr_corpus_index_name,doc_type=facebook_xnr_corpus_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results

def show_condition_corpus_facebook(corpus_condition):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':corpus_condition
                    }
                }
            }

        },
        'size':MAX_VALUE
    }    
    result=es.search(index=facebook_xnr_corpus_index_name,doc_type=facebook_xnr_corpus_index_type,body=query_body)['hits']['hits']
    results=[]
    for item in result:
        item['_source']['id']=item['_id']
        results.append(item['_source'])
    return results


def show_facebook_corpus(task_detail):
    result = dict()
    theme_corpus = '主题语料'
    daily_corpus = '日常语料' 
    opinion_corpus = '观点语料'
    if task_detail['corpus_status'] == 0:        
        result['theme_corpus'] = show_corpus_facebook(theme_corpus)
        
        result['daily_corpus'] = show_corpus_facebook(daily_corpus)
        
        result['opinion_corpus'] = ''
    else:
        if task_detail['request_type'] == 'all':
            if task_detail['create_type']:
                result['theme_corpus'] = show_corpus_class_facebook(task_detail['create_type'],theme_corpus)
                
                result['daily_corpus'] = show_corpus_class_facebook(task_detail['create_type'],daily_corpus)
            else:
                pass
        else:
            corpus_condition = []
            if task_detail['create_type']:
                corpus_condition.append({'term':{'create_type':task_detail['create_type']}})
            else:
                pass

            theme_corpus_condition = corpus_condition
            if task_detail['theme_type_1']:
                theme_corpus_condition.append({'terms':{'theme_daily_name':task_detail['theme_type_1']}})
                theme_corpus_condition.append({'term':{'corpus_type':theme_corpus}})

                result['theme_corpus'] = show_condition_corpus_facebook(theme_corpus_condition)
            else:
                if task_detail['create_type']:
                    result['theme_corpus'] = show_corpus_class_facebook(task_detail['create_type'],theme_corpus)
                else:
                    result['theme_corpus'] = show_corpus_facebook(theme_corpus)

            daily_corpus_condition = corpus_condition
            if task_detail['theme_type_2']:
                daily_corpus_condition.append({'terms':{'theme_daily_name':task_detail['theme_type_2']}})
                daily_corpus_condition.append({'term':{'corpus_type':daily_corpus}})
                
                result['daily_corpus'] = show_condition_corpus_facebook(daily_corpus_condition)
            else:
                if task_detail['create_type']:
                    result['daily_corpus'] = show_corpus_class_facebook(task_detail['create_type'],daily_corpus)
                else:
                    result['daily_corpus'] = show_corpus_facebook(daily_corpus)

        result['opinion_corpus'] = ''

    return result
 