#encoding:UTF-8
import sys
import redis
import json
from time import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import R_ADMIN as r
from global_utils import es_xnr as es 
'''
@author: ahuaxuan 
@date: 2009-02-20
'''

wordTree = [None for x in range(256)]
wordTree.append(0)
nodeTree = [wordTree, 0]
def readInputText():
    txt = ''
    for line in open('text.txt', 'rb'):
        txt = txt + line
    return txt

def createWordTree():
    wordTree = [None for x in range(256)]
    wordTree.append(0)
    nodeTree = [wordTree, 0]
    awords = []
    for b in open('sensitive_words.txt', 'rb'):
        #print b.strip().split('={MOD}')[0]
        awords.append(b.strip().split('={MOD}')[0])
    #awords = r.hkeys('sensitive_words')    
    #print 'awords:::',awords
    #print 'awords...........',type(awords[0])
    # 从 es 中读取隐喻式
    query_body = {
        'query':{
            'match_all':{}
        }
    }

    es_scan_results = scan(es,query=query_body,size=1000,index='weibo_hidden_expression',\
        doc_type='hidden_expression')

    while 1:
        try:
            
            scan_data = es_scan_results.next()
            item = scan_data['_source']
            origin_word = item['origin_word']
            evolution_words_list = item['evolution_words_string'].split('&')
            # awords.append(origin_word.encode('utf-8')+"={MOD}")
            awords.append(origin_word.encode('utf-8'))
            for evolution_words in evolution_words_list:
                # awords.append(evolution_words.encode('utf-8')+"={MOD}")
                awords.append(evolution_words.encode('utf-8'))

        except StopIteration:
                print 'over!!!!'
                break

    #temp = wordTree
    for word in awords:
        temp = wordTree

        for a in range(0,len(word)):
            
            index = ord(word[a])
            #print 'index....',index
            if a < (len(word) - 1):
                if temp[index] == None:
                    node = [[None for x in range(256)],0]
                    temp[index] = node
                    #print 'node.....',node
                elif temp[index] == 1:
                    node = [[None for x in range(256)],1]
                    temp[index] = node
                
                temp = temp[index][0]
            else:
                temp[index] = 1

    return nodeTree 

def searchWord(str, nodeTree):
    #print 'str...',str
    temp = nodeTree
    words = []
    word = []
    a = 0
    while a < len(str):
        index = ord(str[a])
        try:
            temp = temp[0][index]
        except:
            temp = None
        if temp == None:
            temp = nodeTree
            a = a - len(word)
            word = []
        elif temp == 1 or temp[1] == 1:
            word.append(index)
            words.append(word)
            a = a - len(word) + 1 
            word = []
            temp = nodeTree
        else:
            word.append(index)
        a = a + 1
    
    map_words = {}
    #print 'words...',words
    for w in words:
        iter_word = "".join([chr(x) for x in w])
        #print 'iter_word....',iter_word
        if not map_words.__contains__(iter_word):
            map_words[iter_word] = 1
        else:
            map_words[iter_word] = map_words[iter_word] + 1
    
    return map_words

if __name__ == '__main__':
    #reload(sys)  
    #sys.setdefaultencoding('GBK')  
    #input2 = readInputText()
    DFA = createWordTree()
    #text = u'@LiuGang8964 @winstonywu @liuxiaodong2017 @zhangjian8964 @FengCongde 李录是不是六四后马上跑到美国?不像刘刚王丹等人被抓?'
    #text = u'王丹'
    #print 'DFA..',DFA
    #text = "RT @zhu0588: 打朋友斗父母 要想参加红卫兵造反派组织的大串联,还要经受种种的考验,过了关才有资格.比如他们会叫你打你最好的朋友俩嘴巴,或是给某个他们不喜欢的老师的脑门上写上一条标语,如果你的父母被揪出来了,他们甚至会让你押着他们到最热闹的地方游街.https://t…"
    text = '中办发'
    # sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
    sensitive_words_dict = searchWord(text, DFA)
    

    print 'sensitive_words_dict...',sensitive_words_dict
    # createWordTree();
    # beign=time()
    # list2 = searchWord(input2)
    # print "cost time : ",time()-beign
    # print list2
    # strLst = []
    # print 'I have find some words as ', len(list2)
    # map = {}
    # for w in list2:
    #     word = "".join([chr(x) for x in w])
    #     if not map.__contains__(word):
    #         map[word] = 1
    #     else:
    #         map[word] = map[word] + 1
    
    # for key, value in map.items():
    #     print key, value
