#-*- coding: utf-8 -*-
import socket
import threading
import json

LOCALHOST_IP = '127.0.0.1'
wxbot_port = 6661
server = None
opt = None


def tcplink(conn, addr):
    print 'Accept new connection from %s:%s...'  % addr
    data = conn.recv(8192)
    result = None
    if data:
        data = json.loads(data)
        global opt
        opt = data['opt']
        print opt
    conn.close()  
    print 'Connection from %s:%s closed.' % addr

def listen():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCALHOST_IP, wxbot_port))
    server.listen(5)    #等待连接的最大数量为5
    while True:
        if opt == 'close':
            try:
                server.close()
                print '1111'
            except Exception,e:
                print e
            finally:
                print '2222'
                break
        conn, addr = server.accept()
        t = threading.Thread(target=tcplink, args=(conn, addr))
        t.start()

listen()