#-*- coding:utf-8 -*-
import time
import json
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
path = '/home/ubuntu8/huxiaoqian/xnr2_data_v2'

# import sys
# sys.path.append('../')
from time_utils import date2ts,datetime2ts,ts2datetime
from global_utils import es_xnr as es,facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
							facebook_count_index_name_pre,facebook_count_index_type,\
							facebook_user_index_name,facebook_user_index_type,\
							twitter_flow_text_index_name_pre,twitter_flow_text_index_type,\
							twitter_count_index_name_pre,twitter_count_index_type,\
							twitter_user_index_name,twitter_user_index_type
from timed_python_files.facebook_mappings import facebook_flow_text_mappings,facebook_count_mappings
from timed_python_files.twitter_mappings import twitter_flow_text_mappings,twitter_count_mappings


def Twitter_user_mappings(rows):

	# db = MySQLdb.connect(host="localhost",user="root",passwd="",db="db_F",charset='utf8')
	# cursor = db.cursor()
	# cursor.execute("SELECT * from TIDscouting")
	# rows = cursor.fetchall()

	bulk_action = [] 
	count = 0
	for row in rows:
		# print '!!!!',row
		#print 'create___at....',row[5]
		action = {'index':{'_id':row[1]}}
		source_item = {}
		source_item['uid'] = str(row[1])
		source_item['username'] = row[2].decode("utf-8", "replace")
		source_item['userscreenname'] = row[3].decode("utf-8", "replace")
		source_item['description'] = row[4].decode("utf-8", "replace")
		source_item['create_at'] = int(time.mktime(row[5].timetuple()))
		source_item['url'] = row[6]
		source_item['profile_image_url'] = row[7]
		source_item['profile_background_image_url'] = row[8]
		source_item['location'] = row[9].decode("utf-8", "replace")
		source_item['timezone'] = row[10]
		source_item['access_level'] = row[11]
		source_item['status_count'] = row[12]
		source_item['followers_count'] = row[13]
		source_item['friends_count'] = row[14]
		source_item['favourites_count'] = row[15]
		source_item['listed_count'] = row[16]
		source_item['is_protected'] = row[17]
		source_item['is_geo_enabled'] = row[18]
		source_item['is_show_all_inline_media'] = row[19]
		source_item['is_contributors_enable'] = row[20]
		source_item['is_follow_requestsent'] = row[21]
		source_item['is_profile_background_tiled'] = row[22]
		source_item['is_profile_use_background_image'] = row[23]
		source_item['is_translator'] = row[24]
		source_item['is_verified'] = row[25]
		source_item['utcoffset'] = row[26]
		source_item['lang'] = row[27]
		source_item['bigger_profile_image_url'] = row[28]
		source_item['bigger_profile_image_url_https'] = row[29]
		source_item['mini_profile_image_url'] = row[30]
		source_item['mini_profile_image_url_https'] = row[31]
		source_item['original_profile_image_url'] = row[32]
		source_item['original_profile_image_url_https'] = row[33]
		source_item['profile_background_image_url_https'] = row[34]
		source_item['profile_banner_ipad_url'] = row[35]
		source_item['profile_banner_ipad_retina_url'] = row[36]
		source_item['profile_banner_mobile_url'] = row[37]
		source_item['profile_banner_mobile_retina_url'] = row[38]
		source_item['profile_banner_retina_url'] = row[39]
		source_item['profile_banner_url'] = row[40]
		source_item['profile_image_url_https'] = row[41]
		source_item['update_time'] = int(time.mktime(row[42].timetuple()))
		source_item['sensitivity'] = row[43]
		source_item['sensitivity2'] = row[44]

		bulk_action.extend([action,source_item])
		#print 'bulk_action...',bulk_action
		count += 1
		if count % 1000 == 0:
			es.bulk(bulk_action,index='twitter_user',doc_type='user',timeout=600)
			bulk_action = []
			print count

	if bulk_action:
		print '@@',es.bulk(bulk_action,index='twitter_user',doc_type='user',timeout=600)

def Twitters_mappings():
	import time
	db = MySQLdb.connect(host="localhost",user="root",passwd="",db="db_F",charset='utf8')
	cursor = db.cursor()
	cursor.execute("SELECT * from TIDscouting")
	rows = cursor.fetchall()

	bulk_action_all = {}
	count_dict = {}
 	count_i = 0

	for row in rows:
		# print 'row[4].....',row[4]
		# print 'row[4].....',type(row[4])
		# print '###########',int(time.mktime(row[4].timetuple()))
		action = {'index':{'_id':row[2]}}
		source_item = {}
		source_item['uid'] = str(row[1])
		source_item['tid'] = str(row[2])
		source_item['text'] = row[3].decode("utf-8", "replace")
		source_item['timestamp'] = int(time.mktime(row[4].timetuple()))
		source_item['update_time'] = int(time.mktime(row[5].timetuple()))

		date_time = ts2datetime(int(time.mktime(row[4].timetuple())))

		try:
			bulk_action_all[date_time].extend([action,source_item])
			count_dict[date_time] += 1
			count_i += 1
		except:
			bulk_action_all[date_time] = [action,source_item]
			count_dict[date_time] = 1
			count_i += 1

		for date, count in count_dict.iteritems():
			if count % 1000 == 0 :
				index_name = twitter_flow_text_index_name_pre + date
				
				#if not es.indices.exists(index=index_name):
				twitter_flow_text_mappings(index_name)  # 内含判断

				if bulk_action_all[date]:
					es.bulk(bulk_action_all[date],index=index_name,doc_type=twitter_flow_text_index_type,timeout=600)
					bulk_action_all[date] = []
				
		if count_i % 1000 == 0:
			print count_i

	for date, bulk_action in bulk_action_all.iteritems():

		if bulk_action:

			index_name = twitter_flow_text_index_name_pre + date

			#if not es.indices.exists(index=index_name):
			twitter_flow_text_mappings(index_name) # 内含判断
			
			es.bulk(bulk_action_all[date],index=index_name,doc_type=twitter_flow_text_index_type,timeout=600)
			
def Twitter_count_mappings():
	import time
	db = MySQLdb.connect(host="localhost",user="root",passwd="",db="db_F",charset='utf8')
	cursor = db.cursor()
	cursor.execute("SELECT * from Tscouting")
	rows = cursor.fetchall()

	bulk_action_all = {}
	count_dict = {}
 	count_i = 0

	for row in rows:
		timestamp = int(time.mktime(row[5].timetuple()))
		_id = str(row[1]) + '_' + str(timestamp)
		action = {'index':{'_id':_id}}
		source_item = {}
		#source_item['uid'] = row[1].split('_')[0]
		source_item['tid'] = str(row[1])
		source_item['share'] = row[2]
		source_item['comment'] = row[3]
		source_item['favorite'] = row[4]
		source_item['update_time'] = timestamp

		date_time = ts2datetime(timestamp)

		try:
			bulk_action_all[date_time].extend([action,source_item])
			count_dict[date_time] += 1
			count_i += 1
		except:
			bulk_action_all[date_time] = [action,source_item]
			count_dict[date_time] = 1
			count_i += 1

		for date, count in count_dict.iteritems():
			if count % 1000 == 0:
				index_name = twitter_count_index_name_pre + date
				
				#if not es.indices.exists(index=index_name):
				twitter_count_mappings(index_name)
				if bulk_action_all[date]:
					es.bulk(bulk_action_all[date],index=index_name,doc_type=twitter_count_index_type,\
							timeout=600)
					bulk_action_all[date] = []
				
		if count_i % 1000 == 0:
			print count_i

	for date, bulk_action in bulk_action_all.iteritems():

		if bulk_action:

			index_name = twitter_count_index_name_pre + date

			#if not es.indices.exists(index=index_name):
			twitter_count_mappings(index_name)
			
			es.bulk(bulk_action_all[date],index=index_name,doc_type=twitter_count_index_type,timeout=600)

def Facebooks_mappings():
	import time
	db = MySQLdb.connect(host="localhost",user="root",passwd="",db="db_F",charset='utf8')
	cursor = db.cursor()
	cursor.execute("SELECT * from FIDscouting")
	rows = cursor.fetchall()

	bulk_action_all = {}
	count_dict = {}
 	count_i = 0

	for row in rows:
		# print 'row[4].....',row[4]
		# print 'row[4].....',type(row[4])
		# print '###########',int(time.mktime(row[4].timetuple()))
		#print 'row[3]......',row[3]
		action = {'index':{'_id':row[2].split('_')[1]}}
		source_item = {}
		source_item['uid'] = str(row[1])
		source_item['fid'] = row[2].split('_')[1]
		source_item['text'] = row[3].decode("utf-8", "replace")
		source_item['timestamp'] = int(time.mktime(row[4].timetuple()))
		source_item['update_time'] = int(time.mktime(row[5].timetuple()))

		date_time = ts2datetime(int(time.mktime(row[4].timetuple())))

		try:
			bulk_action_all[date_time].extend([action,source_item])
			count_dict[date_time] += 1
			count_i += 1
		except:
			bulk_action_all[date_time] = [action,source_item]
			count_dict[date_time] = 1
			count_i += 1

		for date, count in count_dict.iteritems():
			if count % 1000 == 0:
				index_name = facebook_flow_text_index_name_pre + date
				
				if not es.indices.exists(index=index_name):
					facebook_flow_text_mappings(index_name)
				
				if bulk_action_all[date]:
					es.bulk(bulk_action_all[date],index=index_name,doc_type=facebook_flow_text_index_type,\
							timeout=600)
					bulk_action_all[date] = []
				
		if count_i % 1000 == 0:
			print count_i

	for date, bulk_action in bulk_action_all.iteritems():

		if bulk_action:

			index_name = facebook_flow_text_index_name_pre + date

			if not es.indices.exists(index=index_name):
				facebook_flow_text_mappings(index_name)
			
			es.bulk(bulk_action_all[date],index=index_name,doc_type=facebook_flow_text_index_type,timeout=600)
			
def Facebook_count_mappings():
	import time
	db = MySQLdb.connect(host="localhost",user="root",passwd="",db="db_F",charset='utf8')
	cursor = db.cursor()
	cursor.execute("SELECT * from Fscouting")
	rows = cursor.fetchall()

	bulk_action_all = {}
	count_dict = {}
 	count_i = 0

	for row in rows:
		timestamp = int(time.mktime(row[5].timetuple()))
		_id = row[1] + '_' + str(timestamp)
		action = {'index':{'_id':_id}}
		source_item = {}
		source_item['uid'] = row[1].split('_')[0]
		source_item['fid'] = row[1].split('_')[1]
		source_item['share'] = row[2]
		source_item['comment'] = row[3]
		source_item['favorite'] = row[4]
		source_item['update_time'] = timestamp

		date_time = ts2datetime(timestamp)

		try:
			bulk_action_all[date_time].extend([action,source_item])
			count_dict[date_time] += 1
			count_i += 1
		except:
			bulk_action_all[date_time] = [action,source_item]
			count_dict[date_time] = 1
			count_i += 1

		for date, count in count_dict.iteritems():
			if count % 1000 == 0:
				index_name = facebook_count_index_name_pre + date
				
				#if not es.indices.exists(index=index_name):
				facebook_count_mappings(index_name)
				
				if bulk_action_all[date]:
					es.bulk(bulk_action_all[date],index=index_name,doc_type=facebook_flow_text_index_type,\
							timeout=600)
					bulk_action_all[date] = []
				
		if count_i % 1000 == 0:
			print count_i

	for date, bulk_action in bulk_action_all.iteritems():

		if bulk_action:

			index_name = facebook_count_index_name_pre + date

			#if not es.indices.exists(index=index_name):
			facebook_count_mappings(index_name)
			
			es.bulk(bulk_action_all[date],index=index_name,doc_type=facebook_flow_text_index_type,timeout=600)
			

def Facebook_user_mappings():
	import format
	#from format import load_json_text
	path_file = path + '/' + 'user.json'

	bulk_action = []
	count = 0
	#keys_dif = ['uid','update_time',]
	# 'id' 'updated_time'  
	dict_key_list = ['hometown','location','education','category_list',\
					'favorite_athletes','interested_in','work','parking',
					'inspirational_people','languages','cover','favorite_teams']

	with open(path_file,'r') as f:
		for line in f:
			line = json.loads(line)
			del line['_id']
			keys_list = line.keys()

			action = {'index':{'_id':line['id']}}

			source_item = {}
			
			source_item['uid'] = line['id']
			del line['id']

			if 'founded' in keys_list:

				try:
					date_time = int(line['founded'])
					time_string = str(date_time) + '-01-01 00:00:00'
					timestamp = int(time.mktime(time.strptime(time_string,"%Y-%m-%d %H:%M:%S")))
					source_item['founded'] = timestamp
				except:
					try:
						if u'年' in line['founded']:
							import re
							time_list = re.split(r'[^\u4e00-\u9fa5]',line['founded'])
							year = str(time_list[0])
							month = str(time_list[1]).zfill(2)
							day = str(time_list[2]).zfill(2)
							date = '-'.join([year,month,day])
							time_string = date+ ' 00:00:00'
							timestamp = int(time.mktime(time.strptime(time_string,"%Y-%m-%d %H:%M:%S")))
							source_item['founded'] = timestamp
						else:
							import re
							time_list = re.split(r'[^\u4e00-\u9fa5]',line['founded'])
							month = str(time_list[0]).zfill(2)
							day = str(time_list[1]).zfill(2)
							year = str(time_list[2])
							date = '-'.join([year,month,day])
							time_string = date+ ' 00:00:00'

							timestamp = int(time.mktime(time.strptime(time_string,"%Y-%m-%d %H:%M:%S")))
							source_item['founded'] = timestamp
					except:
						source_item['founded'] = 0

				del line['founded']

			for dict_key in dict_key_list:

				if dict_key in keys_list:
					source_item[dict_key] = json.dumps(line[dict_key])
					del line[dict_key]
			
			if 'updated_time' in keys_list:
				time_string = line['updated_time'][:10] + ' '+line['updated_time'][11:19]
				source_item['update_time'] = int(time.mktime(time.strptime(time_string,"%Y-%m-%d %H:%M:%S")))
				del line['updated_time']
				
			if 'birthday' in keys_list:
				birthday_list = line['birthday'].split('/')
				try:
					source_item['birthday'] = '-'.join(birthday_list[:2])
				except:
					source_item['birthday'] = ' '

				if len(birthday_list) == 3:
					source_item['birthyear'] = int(birthday_list[2])
				else:
					source_item['birthyear'] = 0

				del line['birthday']

			keys_list_new = line.keys()

			for key_item in keys_list_new:
				source_item[key_item] = line[key_item]

			bulk_action.extend([action,source_item])

			count += 1
			if count % 1000 == 0:
				es.bulk(bulk_action,index='facebook_user',doc_type='user',timeout=600)
				bulk_action = []
				print count

	if bulk_action:
		es.bulk(bulk_action,index='facebook_user',doc_type='user',timeout=600)

if __name__ == '__main__':

	# #db = MySQLdb.connect(host="localhost",user="root",passwd="",db="db_F",charset='utf8')
	# db = MySQLdb.connect(host="localhost",user="root",passwd="",db="twitter_chinese_326",charset='utf8')
	# # #db = MySQLdb.connect("localhost","root","","twitter_chinese_326" )

	# cursor = db.cursor()
	# cursor.execute("SELECT * from chinese_info_sc")
	# rows = cursor.fetchall()
	# Twitter_user_mappings(rows)


	# print rows[877]
	# print rows[871]
	# print rows[873]
	# print rows[875]
	# print rows[878]
	# print rows[879]
	
	#Twitter_user_mappings()
	Twitters_mappings()
	#Twitter_count_mappings()
	Facebooks_mappings()
	#Facebooks_mappings_test()
	#Facebook_count_mappings()

	#Facebook_user_mappings()



#print 'data...',data


# import xlrd
# import pandas as pd

# def printSheet(oXls, sheetName):  
#     sheetIsEmpty = True  
#     tmpSheet = oXls.sheet_by_name(sheetName)  
#     tmpLine = ""  
  
#     for row in range(tmpSheet.nrows):  
#         for col in range(tmpSheet.ncols):  
#             if tmpSheet.cell(row, col).value != None:  
#                 sheetIsEmpty = False  
#                 try:  
#                     tmpLine += str(tmpSheet.cell(row, col).value) + "\t"  
#                 except:  
#                     tmpLine += tmpSheet.cell(row, col).value + "\t"  
#         tmpLine += "\n"  
  
#     if sheetIsEmpty == False:  
#         print "sheet name:%s" % sheetName  
#         print tmpLine   

# xlsFile = xlrd.open_workbook("/home/ubuntu8/huxiaoqian/xnr2_data_v2/scoutFuser.xls")  
# sheet = xlsFile.sheets()[0]  
# print 'sheet...',sheet
# print "xls has %d sheets" % xlsFile.nsheets  
# df_list = []
# for i in range(50):
# 	row_info = sheet.row_values(i)
# 	row_info_new = [item.encode('utf-8') for item in row_info]
# 	df_list.append(row_info_new)

# df_list_new = pd.DataFrame(df_list)
# df_list_new.to_csv('f_test.csv')

# for sheetName in sheets:  
#     printSheet(xlsFile, sheetName) 

