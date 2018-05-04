#encoding:UTF-8
import sys
import redis
import json
from time import time
# reload(sys)
# sys.path.append('../../')
# from global_utils import R_ADMIN as r
'''
@author: ahuaxuan 
@date: 2009-02-20
'''

wordTree = [None for x in range(256)]
wordTree.append(0)
nodeTree = [wordTree, 0]
def readInputText():
    txt = ''
    for line in open('/home/xnr1/xnr_0429/xnr/cron/qq_group_message/sensitive_words.txt', 'rb'):
    # for line in open('sensitive_words.txt', 'rb'):
        txt = txt + line
    return txt

def createWordTree():
    wordTree = [None for x in range(256)]
    wordTree.append(0)
    nodeTree = [wordTree, 0]
    awords = []
    for b in open('/home/xnr1/xnr_0429/xnr/cron/qq_group_message/sensitive_words.txt', 'rb'):
       awords.append(b.strip())
    # awords = r.hkeys('sensitive_words')    
    # print awords
    for word in awords:
        temp = wordTree
        for a in range(0,len(word)):
            index = ord(word[a])
            if a < (len(word) - 1):
                if temp[index] == None:
                    node = [[None for x in range(256)],0]
                    temp[index] = node
                elif temp[index] == 1:
                    node = [[None for x in range(256)],1]
                    temp[index] = node
                
                temp = temp[index][0]
            else:
                temp[index] = 1

    return nodeTree 

def searchWord(str, nodeTree):
    temp = nodeTree
    words = []
    word = []
    a = 0
    while a < len(str):
        index = ord(str[a])
        temp = temp[0][index]
        if temp == None:
            temp = nodeTree
            a = a - len(word)
            word = []
        elif temp == 1 or temp[1] == 1:         #该字为某个关键词的底部
            word.append(index)
            words.append(word)
            a = a - len(word) + 1 
            word = []
            temp = nodeTree
        else:
            word.append(index)
        a = a + 1
    
    map_words = {}
    for w in words:
        iter_word = "".join([chr(x) for x in w])
        if not map_words.__contains__(iter_word):
            map_words[iter_word] = 1
        else:
            map_words[iter_word] = map_words[iter_word] + 1
    
    return map_words

if __name__ == '__main__':
    # reload(sys)  
    # sys.setdefaultencoding('GBK')  
    node = createWordTree();

    list2 = searchWord("知道64和达赖太阳花北京军区", node)
    print list2
    for key in list2.keys():
        key.decode('utf-8')
        print key
