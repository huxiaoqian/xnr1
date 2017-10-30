#-*- coding: utf-8 -*-
from wxpy import *

cache_path = 'bot.pkl'
qr_path = 'botqr.png'
def my_qr_callback(**kwargs):
    with open(qr_path, 'wb') as fp:
        fp.write(kwargs['qrcode'])


bot = Bot(cache_path=cache_path, qr_path=qr_path, qr_callback=my_qr_callback)

embed()