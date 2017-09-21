# -*-coding:utf-8-*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import get_create_sensitive_words,show_sensitive_words_default,show_sensitive_words_condition,delete_sensitive_words,change_sensitive_words,\
                  get_create_date_remind,show_date_remind,show_date_remind_condition,show_select_date_remind,change_date_remind,delete_date_remind,\
                  get_create_hidden_expression,show_hidden_expression,show_hidden_expression_condition,show_select_hidden_expression,change_hidden_expression,delete_hidden_expression,\
                  create_corpus,show_corpus,show_corpus_class,show_select_corpus,change_select_corpus,delete_corpus,\
                  get_create_type_content,domain_create_task,get_show_domain_group_summary,\
                  get_show_domain_group_detail_portrait,get_show_domain_description,\
                  get_show_domain_role_info,get_delete_domain,get_export_example_model,\
                  get_generate_example_model,get_show_example_model

mod = Blueprint('weibo_xnr_knowledge_base_management', __name__, url_prefix='/weibo_xnr_knowledge_base_management')

## 生成实例模板
@mod.route('/generate_example_model/')
def ajax_generate_example_model():
    xnr_user_no = request.args.get('xnr_user_no','')
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    results = get_generate_example_model(xnr_user_no,domain_name,role_name)

    return json.dumps(results)

## 导出实例模板

@mod.route('/show_example_model/')
def ajax_show_example_model():
    xnr_user_no = request.args.get('xnr_user_no','')
    results = get_show_example_model(xnr_user_no)

    return json.dumps(results)

@mod.route('/export_example_model/')
def ajax_export_example_model():
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    results = get_export_example_model(domain_name,role_name)

    return json.dumps(results)

## 创建领域
@mod.route('/create_domain/')
def ajax_create_domain():
    xnr_user_no = request.args.get('xnr_user_no','')
    domain_name = request.args.get('domain_name','')
    create_type = request.args.get('create_type','')  # 按关键词--by_keywords  按种子用户--by_seed_users  按所有用户--by_all_users 
    keywords_string = request.args.get('keywords_string','')  # 按关键词方式，以中文逗号“，”分割。若是不是按关键词，则不传递此参数
    seed_users = request.args.get('seed_users','')  # 按种子用户方式，不同uid之间以中文逗号“，”分隔
    all_users = request.args.get('all_users','')  #按所有用户方式，传递所有uid
    create_type_new = get_create_type_content(create_type,keywords_string,seed_users,all_users)
    create_time = int(time.time())
    submitter = request.args.get('submitter','admin@qq.com')
    description = request.args.get('description','')
    remark = request.args.get('remark','')

    mark = domain_create_task(xnr_user_no,domain_name,create_type_new,create_time,submitter,description,remark)

    return json.dumps(mark)  # True False

## 展示群体摘要信息
@mod.route('/show_domain_group_summary/')
def ajax_show_domain_group_summary():
    xnr_user_no = request.args.get('xnr_user_no','')

    results = get_show_domain_group_summary(xnr_user_no)

    return json.dumps(results)

## 展示群体详细画像信息
@mod.route('/show_domain_group_detail_portrait/')
def ajax_show_domain_group_detail_portrait():
    xnr_user_no = request.args.get('xnr_user_no','')
    domain_name = request.args.get('domain_name','')
    results = get_show_domain_group_detail_portrait(xnr_user_no,domain_name)

    return json.dumps(results)

## 展示群体描述
@mod.route('/show_domain_description/')
def ajax_show_domain_description():
    xnr_user_no = request.args.get('xnr_user_no','')
    domain_name = request.args.get('domain_name','')
    results = get_show_domain_description(xnr_user_no,domain_name)

    return json.dumps(results)

## 展示角色
@mod.route('/show_domain_role_info/')
def ajax_show_domain_role_info():
    domain_name = request.args.get('domain_name','')
    role_name = request.args.get('role_name','')
    results = get_show_domain_role_info(domain_name,role_name)

    return json.dumps(results)

## 删除领域
@mod.route('/delete_domain/')
def ajax_delete_domain():
    domain_name = request.args.get('domain_name','')
    mark = get_delete_domain(domain_name)

    return json.dumps(mark)

#根据
@mod.route('/create_weibo_xnr/')
def ajax_create_weibo_xnr():
    
    domain_name =  request.args.get('domain_name','')
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    domain_info = get_domain_info(domain_pinyin)
    
    return json.dumps(domain_info)

@mod.route('/show_role_info/')
def ajax_show_role_info():
    domain_name = request.args.get('domain_name','')
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_name = request.args.get('role_name','')
    role_info = get_role_info(domain_pinyin,role_name)

    return json.dumps(role_info)

########################################################
'''
业务知识库管理
'''
## 敏感词管理
#添加敏感词
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/create_sensitive_words/?rank=1&sensitive_words=左倾&create_type=all_xnrs
@mod.route('/create_sensitive_words/')
def ajax_create_sensitive_words():
    rank = request.args.get('rank','')
    sensitive_words = request.args.get('sensitive_words','')
    create_type = request.args.get('create_type','')
    create_time = int(time.time())
    mark = get_create_sensitive_words(rank,sensitive_words,create_type,create_time)

    return json.dumps(mark)

#批量添加敏感词
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/create_sensitive_words_batch/?rank=2&sensitive_words_string=恐怖，暴力，袭击，暴乱&create_type=my_xnrs
@mod.route('/create_sensitive_words_batch/')
def ajax_create_sensitive_words_batch():
    rank = request.args.get('rank','')
    sensitive_words_string = request.args.get('sensitive_words_string','')
    sensitive_words=sensitive_words_string.encode('utf-8').split('，')
    create_type = request.args.get('create_type','')
    create_time = int(time.time())
    mark_result=[]
    for item in sensitive_words:
        mark=get_create_sensitive_words(rank,item,create_type,create_time)
        mark_result.append(mark)
    return json.dumps(mark_result)

#默认显示敏感词列表
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_sensitive_words_default
@mod.route('/show_sensitive_words_default/')
def ajax_show_sensitive_words_default():
    results=show_sensitive_words_default()
    return json.dumps(results)

#按等级or类别显示敏感词列表
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_sensitive_words_condition/
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_sensitive_words_condition/?rank=3
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_sensitive_words_condition/?create_type=all_xnrs&rank=1
@mod.route('/show_sensitive_words_condition/')
def ajax_show_sensitive_words_condition():
    create_type=request.args.get('create_type','')
    rank=request.args.get('rank','')
    results=show_sensitive_words_condition(create_type,rank)
    return json.dumps(results)

#删除指定敏感词
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/delete_sensitive_words/?words_id='左倾'
@mod.route('/delete_sensitive_words/')
def ajax_delete_sensitive_words():
    words_id=request.args.get('words_id','')
    results=delete_sensitive_words(words_id)
    return json.dumps(results)


#修改指定敏感词
#对指定敏感词进行修改
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/change_sensitive_words/?words_id='左倾'&rank=2&sensitive_words='左倾*'&create_type=all_xnr
@mod.route('/change_sensitive_words/')
def ajax_change_sensitive_words():
    words_id=request.args.get('words_id','')
    rank=request.args.get('rank','')
    sensitive_words=request.args.get('sensitive_words','')
    create_type=request.args.get('create_type','')
    create_time=int(time.time())
    change_info=[rank,sensitive_words,create_type,create_time]
    results=change_sensitive_words(words_id,change_info)
    return json.dumps(results)

## 时间节点预警
#添加时间节点预警
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/create_date_remind/?timestamp=2001-09-11&keywords=911事件&create_type=all_xnrs&content_recommend=“9·11事件”（September 11 attacks），又称“911‘、“9·11恐怖袭击事件”[1]  ，是2001年9月11日发生在美国纽约世界贸易中心的一起系列恐怖袭击事件.
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/create_date_remind/?timestamp=1931-09-18&keywords=918事变&create_type=my_xnrs&content_recommend=九一八事变（又称奉天事变、柳条湖事件）是日本在中国东北蓄意制造并发动的一场侵华战争，是日本帝国主义侵华的开端。
@mod.route('/create_date_remind/')
def ajax_create_date_remind():
    timestamp = request.args.get('timestamp','')
    keywords = request.args.get('keywords','')
    #keywords_string = '&'.join(keywords.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())
    content_recommend = request.args.get('content_recommend','')
    
    mark = get_create_date_remind(timestamp,keywords,create_type,create_time,content_recommend)

    return json.dumps(mark)

#显示时间节点预警列表
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_date_remind
@mod.route('/show_date_remind/')
def ajax_show_date_remind():
    results=show_date_remind()
    return json.dumps(results)

#按类别显示时间节点预警列表
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_date_remind_condition/?create_type=all_xnrs
@mod.route('/show_date_remind_condition/')
def ajax_show_date_remind_condition():
    create_type=request.args.get('create_type','')
    results=show_date_remind_condition(create_type)
    return json.dumps(results)

#显示指定的时间节点内容，用于修改
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_select_date_remind/?task_id=1503135422
@mod.route('/show_select_date_remind/')
def ajax_show_select_date_remind():
    task_id=request.args.get('task_id','')
    results=show_select_date_remind(task_id)
    return json.dumps(results)

#修改指定的时间节点预警内容
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/change_date_remind/?task_id=1503135422&keywords=美国911事件&create_type=all_xnrs
@mod.route('/change_date_remind/')
def ajax_change_date_remind():
    task_id=request.args.get('task_id','')
    keywords=request.args.get('keywords','')
    create_type = request.args.get('create_type','')
    create_time=int(time.time())
    results=change_date_remind(task_id,keywords,create_type,create_time)
    return json.dumps(results)


#删除指定的时间节点预警内容
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/delete_date_remind/?task_id=1503135316
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/delete_date_remind/?task_id=1503409186
@mod.route('/delete_date_remind/')
def ajax_delete_date_remind():
    task_id=request.args.get('task_id','')
    results=delete_date_remind(task_id)
    return json.dumps(results)



## 隐喻式表达
#添加隐喻式表达
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/create_hidden_expression/?origin_word=习大大&evolution_words=习主席，习大大&create_type=all_xnrs
@mod.route('/create_hidden_expression/')
def ajax_create_hidden_expression():
    origin_word = request.args.get('origin_word','')
    evolution_words = request.args.get('evolution_words','')
    evolution_words_string = '&'.join(evolution_words.encode('utf-8').split('，'))  # 字符串，以 '&'连接
    create_type = request.args.get('create_type','')
    create_time = int(time.time())

    mark = get_create_hidden_expression(origin_word,evolution_words_string,create_type,create_time)

    return json.dumps(mark)

#显示隐喻式表达列表
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_hidden_expression
@mod.route('/show_hidden_expression/')
def ajax_show_hidden_expression():
    results=show_hidden_expression()
    return json.dumps(results)

#按类别显示隐喻式表达
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_hidden_expression_condition/?create_type=all_xnrs
@mod.route('/show_hidden_expression_condition/')
def ajax_show_hidden_expression_condition():
    create_type=request.args.get('create_type','')
    results=show_hidden_expression_condition(create_type)
    return json.dumps(results)
#显示指定的隐喻式表达，用于修改
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_select_hidden_expression/?express_id=习大大
@mod.route('/show_select_hidden_expression/')
def ajax_show_select_hidden_expression():
    express_id=request.args.get('express_id','')
    results=show_select_hidden_expression(express_id)
    return json.dumps(results)

#修改指定的隐喻式表达内容
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/change_hidden_expression/?express_id=习大大&origin_word=习大大&evolution_words=习主席，习大大，习总书记&create_type=all_xnrs
@mod.route('/change_hidden_expression/')
def ajax_change_hidden_expression():
    express_id=request.args.get('express_id','')
    origin_word=request.args.get('origin_word','')
    evolution_words=request.args.get('evolution_words','')
    evolution_words_string='&'.join(evolution_words.encode('utf-8').split('，'))
    create_type=request.args.get('create_type','')
    create_time=int(time.time())
    change_info=[origin_word,evolution_words_string,create_type,create_time]
    results=change_hidden_expression(express_id,change_info)
    return json.dumps(results)

#删除指定的隐喻式表达内容
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/delete_hidden_expression/?express_id=习近平
@mod.route('/delete_hidden_expression/')
def ajax_delete_hidden_expression():
    express_id=request.args.get('express_id','')
    results=delete_hidden_expression(express_id)
    return json.dumps(results)

'''
言论知识库管理
'''
#添加语料
#注：添加主题语料和日常语料均调用该函数，只是默认的corpus_type取值不同
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/add_corpus/?corpus_type=主题语料&theme_daily_name=影视&text=我参与了@新浪江西 发起的投票 【电影《建军大业》，你最期待谁的表演？】，我投给了“李易峰 饰 何长工”这个选项。你也快来表态吧~&uid=2306260070&mid=4046347889808989&retweeted=0&comment=0&like=0&create_type=all_xnrs
@mod.route('/add_corpus/')
def ajax_add_corpus():
    corpus_type=request.args.get('corpus_type','')             #corpus_type可取值：主题语料，日常语料
    theme_daily_name=request.args.get('theme_daily_name','')
    text=request.args.get('text','')
    uid=request.args.get('uid','')
    mid=request.args.get('mid','')
    timestamp=int(time.time())
    retweeted=request.args.get('retweeted','')
    comment=request.args.get('comment','')
    like=request.args.get('like','')
    create_type=request.args.get('create_type','')
    corpus_info=[corpus_type,theme_daily_name,text,uid,mid,timestamp,retweeted,comment,like,create_type]
    results=create_corpus(corpus_info)
    return json.dumps(results)

#默认显示语料
#日常语料和主题语料部分分别传入不同的corpus_type
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_corpus/?corpus_type=主题语料
@mod.route('/show_corpus/')
def ajax_show_corpus():
    corpus_type=request.args.get('corpus_type','')
    results=show_corpus(corpus_type)
    return json.dumps(results)

#按类别显示主题语料库
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_corpus_class/?corpus_type=主题语料&create_type=my_xnrs
@mod.route('/show_corpus_class/')
def ajax_show_corpus_class():
    create_type=request.args.get('create_type','')
    corpus_type=request.args.get('corpus_type','')
    results=show_corpus_class(create_type,corpus_type)
    return json.dumps(results)

#修改语料
#注：主题语料和日常语料都调用该函数模块
#step 1:显示指定修改的内容
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/show_select_corpus/?corpus_id=4046347889808989
@mod.route('/show_select_corpus/')
def ajax_show_select_corpus():
    corpus_id=request.args.get('corpus_id','')
    results=show_select_corpus(corpus_id)
    return json.dumps(results)

#step 2:修改指定语料
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/change_select_corpus/?corpus_id=4046347889808989&corpus_type=主题语料&theme_daily_name=影视&text=我参与了@新浪江西 发起的投票 【电影《建军大业》，你最期待谁的表演？】，我投给了“李易峰 饰 何长工”这个选项。你也快来表态吧~&uid=2306260070&mid=4046347889808989&retweeted=0&comment=0&like=0&create_type=my_xnrs
@mod.route('/change_select_corpus/')
def ajax_change_select_corpus():
    corpus_id=request.args.get('corpus_id','')
    corpus_type=request.args.get('corpus_type','')             #corpus_type可取值：主题语料，日常语料
    theme_daily_name=request.args.get('theme_daily_name','').split(',')
    create_type=request.args.get('create_type','')
    results=change_select_corpus(corpus_id,corpus_type,theme_daily_name,create_type)
    return json.dumps(results)

#删除语料
#http://219.224.134.213:9209/weibo_xnr_knowledge_base_management/delete_corpus/?corpus_id=4046347889808989
@mod.route('/delete_corpus/')
def ajax_delete_corpus():
    corpus_id=request.args.get('corpus_id','')
    results=delete_corpus(corpus_id)
    return json.dumps(results)