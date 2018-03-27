#-*-coding=utf-8-*-

import time
from sta_ad import start_ad

weibos = [{'_id': 1, 'text': 'Python的标准库中的os模块包含普遍的操作系统功能。如果你希望你的程序能够与平台无关的话,这个模块是尤为重要的。'}]

start_ts = time.time()
results = []
count = 0
while 1:
    results.extend(weibos)
    count += 1
    if count == 100:
        break

start_ad(results)
print time.time() - start_ts

