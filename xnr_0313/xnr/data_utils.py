# -*- coding: utf-8 -*-

#用于生成ID，补全4位数，把1变成0001
def num2str(num):
	num_str="%04d"%num
	return num_str