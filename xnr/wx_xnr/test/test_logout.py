#-*- coding: utf-8 -*-
from wxpy import *
import time
# bot = Bot(console_qr=True, logout_callback=)
# 

def test():
    start_time = time.time()
    while True:
        end_time = time.time()
        # print start_time, end_time
        t = int(end_time - start_time)
        print t
        if t > 10:
            return 1
            break


print test()