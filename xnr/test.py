#-*- coding:utf-8 -*-
import os
import time
import random
import json
import sys
import base64
from global_utils import es_xnr as es
from global_utils import weibo_xnr_index_name,weibo_xnr_index_type

icon = open('./weibo_images/minzudang.png','rb')
iconData = icon.read()
iconData = base64.b64encode(iconData)
print 'icondata:::',iconData

imgData = base64.b64decode(iconData)
time_name = time.strftime('%Y%m%d%H%M%S')
random_name = time_name + '_%d' % random.randint(0,100)
leniyimg = open('./'+random_name+'.jpg','wb')
leniyimg.write(imgData)
leniyimg.close()
	