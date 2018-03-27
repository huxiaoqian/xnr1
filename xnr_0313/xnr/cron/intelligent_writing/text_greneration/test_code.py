# -*- coding=utf-8 -*-

import re
import sys
import time
import json
import csv
from text_generation import text_generation_main

def main(file_name):

	text_list = []
	reader = csv.reader(file('./text_data/%s.csv' % file_name, 'rb'))
	for line in reader:
		text = line[1]
		text_list.append(text)
	print 'text_list..',text_list
	print  ''
	keywords = ['父亲','拒绝']
	summary = text_generation_main(text_list,keywords)
	print 'summary...',summary
	with open('./result/%s.csv' % file_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow([summary])
	f.close()

if __name__ == '__main__':
	main('text_fudan')