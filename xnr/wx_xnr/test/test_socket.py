#-*- coding: utf-8 -*-
import socket
import json


opt = 'close'
# opt = 'test'


sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.settimeout(1)
try:
    sk.connect(('127.0.0.1', 6661))
    sk.send(json.dumps({'opt':opt}))
    print 'Server port 6661 OK!'
except Exception,e:
    print e
    print 'Server port 6661 not connect!'
sk.close()