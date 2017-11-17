#-*- coding: utf-8 -*-
from wxpy import *
import uuid

bot = Bot(console_qr=True)
group = bot.groups().search(u'紫荆山管城')[0]

for member in group.members:
	member.set_remark_name(str(uuid.uuid1()))

embed()