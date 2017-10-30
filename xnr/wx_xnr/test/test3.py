#-*- coding: utf-8 -*-
from wxpy import *

bot = Bot(console_qr=True)

hmc = ensure_one(bot.friends().search(u'韩梦成'))
group = ensure_one(bot.groups().search(u'微信虚拟人状况监管群'))

@bot.register(hmc)
def reg_hmc(msg):
	print msg.text

embed()