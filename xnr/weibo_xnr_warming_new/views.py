#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_personnal_warming,show_speech_warming,show_date_warming,show_event_warming,addto_warning_corpus	           
				   
				  #,report_warming_content,get_hashtag


mod = Blueprint('weibo_xnr_warming_new', __name__, url_prefix='/weibo_xnr_warming_new')

#人物行为预警
#http://219.224.134.213:9209/weibo_xnr_warming_new/show_personnal_warming/?xnr_user_no=WXNR0004&start_time=1511755200&end_time=1511857583
@mod.route('/show_personnal_warming/')
def ajax_show_personnal_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))
	results=show_personnal_warming(xnr_user_no,start_time,end_time)
	return json.dumps(results)


#言论内容预警
#show_type=0,全部用户；1，关注用户；2，未关注用户
#http://219.224.134.213:9209/weibo_xnr_warming_new/show_speech_warming/?xnr_user_no=WXNR0004&show_type=0&start_time=1511755200&end_time=1511857583
@mod.route('/show_speech_warming/')
def ajax_show_speech_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	show_type=int(request.args.get('show_type',''))
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))   
	results=show_speech_warming(xnr_user_no,show_type,start_time,end_time)
	return json.dumps(results)

#时间预警
#http://219.224.134.213:9209/weibo_xnr_warming_new/show_date_warming/?account_name=admin@qq.com&start_time=1511668800&end_time=1512389253
@mod.route('/show_date_warming/')
def ajax_show_date_warming():
	account_name=request.args.get('account_name','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_date_warming(account_name,start_time,end_time)
	return json.dumps(results)


###事件涌现预警
#http://219.224.134.213:9209/weibo_xnr_warming_new/show_event_warming/?xnr_user_no=WXNR0004&start_time=1511668800&end_time=1512389253
@mod.route('/show_event_warming/')
def ajax_show_event_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	start_time=int(request.args.get('start_time',''))
	end_time=int(request.args.get('end_time',''))  
	results=show_event_warming(xnr_user_no,start_time,end_time)
	return json.dumps(results)


#加入预警库
@mod.route('/addto_warning_corpus/')
def ajax_addto_warning_corpus():
	task_detail=dict()
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['warning_source']=request.args.get('warning_source','')
	task_detail['uid']=request.args.get('uid','')
	task_detail['mid']=request.args.get('mid','')
	task_detail['timestamp']=int(request.args.get('timestamp',''))
	task_detail['create_time']=int(time.time())
	results=addto_warning_corpus(task_detail)
	return json.dumps(results)


#上报
#一键上报
#user_info=[uid,nick_name,fansnum,friendsnum]
#weibo_info=[mid,text,timestamp,retweeted,like,comment,sensitive,sensitive_words_string]
#人物行为预警上报report_content=[weibo_list]
#test:http://219.224.134.213:9209/weibo_xnr_warming/report_warming_content/?report_type=人物&xnr_user_no=WXNR0003&uid=2659684317&weibo_info=4044828436797896,'//@掌管颖的后宫: #赵丽颖# 本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:#赵丽颖# #赵丽颖楚乔传# 总裁夫人集合完毕@赵丽颖 [心][心][心]#特工皇妃楚乔传# #赵丽颖乘风破浪#',1479845711,0,0,0*4044828486221158,'//@掌管颖的后宫: #赵丽颖# 本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:#赵丽颖# #赵丽颖楚乔传# 总裁夫人集合完毕@赵丽颖 [心][心][心]#特工皇妃楚乔传# #赵丽颖乘风破浪#',1479845723,0,0,0*4044828503513100,'//@掌管颖的后宫: #赵丽颖# 本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:#赵丽颖# #赵丽颖楚乔传# 总裁夫人集合完毕@赵丽颖 [心][心][心]#特工皇妃楚乔传# #赵丽颖乘风破浪# n',1479845727,0,0,0	
#http://219.224.134.213:9209/weibo_xnr_warming/report_warming_content/?report_type=人物&xnr_user_no=WXNR0003&uid=2659684317&weibo_info=4044828436797896,'//@掌管颖的后宫本夫人在此',1479845711,0,0,0*4044828486221158,'//@掌管颖的后宫赵丽颖',1479845723,0,0,0*4044828503513100,'//@掌管颖的后宫本夫人在此n',1479845727,0,0,0	
#http://219.224.134.213:9209/weibo_xnr_warming/report_warming_content/?report_type=人物&xnr_user_no=WXNR0003&uid=2659684317&weibo_info=4044828436797896,'//@掌管颖的后宫赵丽颖本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:赵丽颖赵丽颖楚乔传总裁夫人集合完毕@赵丽颖 [心][心][心]特工皇妃楚乔传赵丽颖乘风破浪',1479845711,0,0,0*4044828486221158,'//@掌管颖的后宫: 赵丽颖本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:赵丽颖赵丽颖楚乔传总裁夫人集合完毕@赵丽颖 [心][心][心]特工皇妃楚乔传赵丽颖乘风破浪',1479845723,0,0,0*4044828503513100,'//@掌管颖的后宫:赵丽颖本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:赵丽颖赵丽颖楚乔传总裁夫人集合完毕@赵丽颖 [心][心][心]特工皇妃楚乔传赵丽颖乘风破浪n',1479845727,0,0,0	
#http://219.224.134.213:9209/weibo_xnr_warming/report_warming_content/?report_type=人物&xnr_user_no=WXNR0003&uid=2659684317&weibo_info=4044828436797896,'//@掌管颖的后宫: %23赵丽颖%23 本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:%23赵丽颖%23 %23赵丽颖楚乔传%23 总裁夫人集合完毕@赵丽颖 [心][心][心]%23特工皇妃楚乔传%23 %23赵丽颖乘风破浪%23',1479845711,0,0,0*4044828486221158,'//@掌管颖的后宫: %23赵丽颖%23 本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:%23赵丽颖%23 %23赵丽颖楚乔传%23 总裁夫人集合完毕@赵丽颖 [心][心][心]%23特工皇妃楚乔传%23 %23赵丽颖乘风破浪%23',1479845723,0,0,0*4044828503513100,'//@掌管颖的后宫: %23赵丽颖%23 本夫人在此[哈哈][哈哈]@赵丽颖 //@赵丽颖数据小分队:%23赵丽颖%23 %23赵丽颖楚乔传%23 总裁夫人集合完毕@赵丽颖 [心][心][心]%23特工皇妃楚乔传%23 %23赵丽颖乘风破浪%23 n',1479845727,0,0,0	
#言论内容预警上报report_content=[weibo_dict]
#test:http://219.224.134.213:9209/weibo_xnr_warming/report_warming_content/?report_type=言论&xnr_user_no=WXNR0002&uid=1701350272&weibo_info=4046350159548465,【洪秀柱痛批蔡当局流氓、强盗：难道要逼我们革命？】　　中国台湾网11月27日讯  据台湾《联合报》报道，台当局“不当党产处理委员会”25日认定“中投”、欣裕台公司属于国民党不当党产，宣布将收归公有。http://t.cn/RfO3TK,1480208518,0,1,0
#事件涌现预警上报report_content=[user_list,weibo_list]
#test:http://219.224.134.213:9209/weibo_xnr_warming/report_warming_content/?report_type=事件&xnr_user_no=WXNR0002&event_name=杨振宁95岁生日恢复中国国籍&user_info=5537979196,兰德科特,100,200*3969238480,后会无期25799,88,179*3302557313,东南老曹,600,50&weibo_info=4044828436797896,'欢迎杨振宁先生恢复中国国籍',1503450000,1071,250,55*4044828486221158,'欢迎杨振宁先生恢复中国国籍，转为中科院资深',1503450000,1071,250,55*4044828503513100,'欢迎杨振宁先生恢复中国国籍，转为中科院资深',1503450000,1071,250,55
#备注：text中的'#'字符用'%23'代替
@mod.route('/report_warming_content/', methods=['POST'])
def ajax_report_warming_content():
	task_detail=dict()
	task_detail['report_type']=request.args.get('report_type','') #预警类型
	task_detail['report_time']=int(time.time())
	task_detail['xnr_user_no']=request.args.get('xnr_user_no','')
	task_detail['event_name']=request.args.get('event_name','')    #事件名称
	task_detail['uid']=request.args.get('uid','')                  #人物预警uid

	task_detail['report_id']=request.args.get('report_id','')    #上报内容的id

	#获取主要参与用户信息
	task_detail['user_info']=request.args.get('user_info','')   #user_info=[uid,uid,……]	
	#获取典型微博信息
	task_detail['weibo_info']=request.args.get('weibo_info','')   #weibo_info=[{'mid':*,'timestamp':*},{'mid':*,'timestamp':*},……]

	results=report_warming_content(task_detail)
	return json.dumps(results)

