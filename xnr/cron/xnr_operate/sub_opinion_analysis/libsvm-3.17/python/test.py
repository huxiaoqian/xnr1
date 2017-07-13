# -*- coding: utf-8 -*-

import os
import csv
from svmutil import *
from opinion_produce import *

def main():
    
    reader = csv.reader(file('./test/weibo0521.csv', 'rb'))
    weibo_data = []
    count = 0
    for line in reader:
        weibo_data.append(line[1])
        count = count + 1
        if count >= 1000:
            break

    opinion_name,word_result,text_list = opinion_main(weibo_data,5)

    with open('./test/opinion_name.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in opinion_name.iteritems():
            writer.writerow((k,v))
    f.close()

    with open('./test/word_result.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in word_result.iteritems():
            for i in v:
                writer.writerow((k,i))
    f.close()

    with open('./test/text_list.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in text_list.iteritems():
            for i in v:
                writer.writerow((k,i))
    f.close()
    
if __name__ == '__main__':
    main()
