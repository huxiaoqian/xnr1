# -*-coding:utf-8-*-
from zhtools.langconv import *

fo = open('sensitive_words_fanjian.txt','wb')

for b in open('sensitive_words.txt', 'rb'):
    #print b.strip().split('={MOD}')[0]
    word = b.strip().split('={MOD}')[0]
    print type(word)
    line = Converter('zh-hant').convert(word.decode('utf-8'))
    line = line.encode('utf-8')
    print 'line_type..',type(line)
    fo.write(word)
    if line != word:
    	fo.write('\n')
        fo.write(line)
        fo.write('\n')

