#-*- coding: utf-8 -*-
import time
import sys
import getopt

def test(name, pwd):
    print 'aaaa'
    while True:
        print name
        print pwd
        time.sleep(20)

if __name__ == '__main__':
    try:
        print 'bbbb'
        opts, args = getopt.getopt(sys.argv[1:], 'hn:p:')
        for op, value in opts:
            if op == '-n':
                name = value
            elif op == '-p':
                pwd = value
        test(name, pwd)
    except Exception,e:
        print e
