# -*-coding: utf-8-*-
import os
import time

QRCODE_PATH = '/root/.qqbot-tmp/'

# QRCODE_PATH = 'C:\Users\herry\.qqbot-tmp/'


def getQRCode():
    filenames = os.listdir(QRCODE_PATH)
    filenames.sort(compare)

    for filename in filenames:
        if '.png' in filename:
            print QRCODE_PATH + filename

            # mtime = time.ctime(os.path.getmtime(QRCODE_PATH + filename))  # modify time
            # ctime = time.ctime(os.path.getctime(QRCODE_PATH + filename))  # create time
            # print mtime, ctime
            return QRCODE_PATH + filename
    return QRCODE_PATH


def compare(x, y):
    stat_x = os.stat(QRCODE_PATH + x)
    stat_y = os.stat(QRCODE_PATH + y)
    if stat_x.st_ctime > stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime < stat_y.st_ctime:
        return 1
    else:
        return 0


if __name__ == '__main__':
    getQRCode()
