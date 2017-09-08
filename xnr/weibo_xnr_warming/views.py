#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from utils import show_personnal_warming,\
				  show_event_warming,\
				  show_speech_warming,addto_speech_warming,\
				  show_date_warming,report_warming_content,get_hashtag


mod = Blueprint('weibo_xnr_warming', __name__, url_prefix='/weibo_xnr_warming')

###人物行为预警
#显示预警内容
#http://219.224.134.213:9209/weibo_xnr_warming/show_personnal_warming/?xnr_user_no=WXNR0002&day_time=1480176000
@mod.route('/show_personnal_warming/')
def ajax_show_personnal_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	day_time=request.args.get('day_time','')
	#day_time=time.time()
	results=show_personnal_warming(xnr_user_no,day_time)
	return json.dumps(results)

#一键上报、转发、评论、点赞、导出至excel见公共操作模块


###言论内容预警
#显示预警内容，默认显示已关注用户，未关注用户传值0
#http://219.224.134.213:9209/weibo_xnr_warming/show_speech_warming/?xnr_user_no=WXNR0003&day_time=1480176000&show_type=0
@mod.route('/show_speech_warming/')
def ajax_show_speech_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	show_type=request.args.get('show_type','')
	day_time=request.args.get('day_time','') 
	#day_time=time.time()     
	results=show_speech_warming(xnr_user_no,show_type,day_time)
	return json.dumps(results)

#一键上报、转发、评论、点赞、导出至excel见公共操作模块

#加入预警库
#http://219.224.134.213:9209/weibo_xnr_warming/addto_speech_warming/?xnr_user_no=WXNR0001&content_type=unfollow&uid=1701350272&text=杨振宁95岁生日恢复中国国籍&mid=4044828436797896&timestamp=1503450000&retweeted=1071&comment=250&like=55&uid_list=1701350272,2659684317
@mod.route('/addto_speech_warming/')
def ajax_addto_speech_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	# content_type=request.args.get('content_type','')
	uid=request.args.get('uid','')
	text=request.args.get('text','')
	mid=request.args.get('mid','')
	timestamp=request.args.get('timestamp','')
	retweeted=request.args.get('retweeted','')
	comment=request.args.get('comment','')
	like=request.args.get('like','')
	# uid_list=request.args.get('uid_list','')
	speech_info=[content_type,uid,text,mid,timestamp,retweeted,comment,like,uid_list]
	results=addto_speech_warming(xnr_user_no,speech_info)
	return json.dumps(results)


###事件涌现预警
#显示预警内容
#http://219.224.134.213:9209/weibo_xnr_warming/show_event_warming/?xnr_user_no=WXNR0004
@mod.route('/show_event_warming/')
def ajax_show_event_warming():
	xnr_user_no=request.args.get('xnr_user_no','')
	results=show_event_warming(xnr_user_no)
	return json.dumps(results)

#一键上报、转发、评论、点赞、导出至excel见公共操作模块

#查看详情——见操作统计的公共模块


###时间预警
#显示预警内容
#http://219.224.134.213:9209/weibo_xnr_warming/show_date_warming
@mod.route('/show_date_warming/')
def ajax_show_date_warming():
	today_time=int(time.time())
	results=show_date_warming(today_time)
	return json.dumps(results)

############公共操作部分#####################
#一键上报
#user_dict=[uid,nick_name,fansnum,friendsnum]
#weibo_dict=[mid,text,timestamp,retweeted,like,comment]
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
@mod.route('/report_warming_content/')
def ajax_report_warming_content():
	report_type=request.args.get('report_type','')
	report_time=int(time.time())
	xnr_user_no=request.args.get('xnr_user_no','')
	event_name=request.args.get('event_name','')
	uid=request.args.get('uid','')

	#获取主要参与用户信息
	user_info=request.args.get('user_info','')    #userinfo中各用户之间以*隔开，每个用户的用户信息以,隔开
	
	#获取典型微博信息
	weibo_info=request.args.get('weibo_info','')  #格式同user_info

	report_info=[report_type,report_time,xnr_user_no,event_name,uid]
	results=report_warming_content(report_info,user_info,weibo_info)
	return json.dumps(results)

#见操作统计的公共模块

#转发

#评论

#点赞

#导出到excel