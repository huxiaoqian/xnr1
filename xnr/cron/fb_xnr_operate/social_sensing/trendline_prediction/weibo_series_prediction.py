#-*-coding:utf-8-*-

import io
import matplotlib as plt
from pylab import *
import math
import getq
import numpy as np
import os
def getSingleBeauty(al):
    result = []
    idx1 = 0
    tempm = 0
    for i in range(0,len(al)):
        if tempm < al[i]:
            tempm = al[i]
            idx1 = i
    r = []
    b1 = 0
    b2 = 0
    idx0 = 0
    c0 = al[idx0]
    for i in range(0,idx1):
        if al[i]<al[idx1] and al[i]<c0:
            idx0 = i
            c0 = al[i]
    idxe = len(al)-1
    f1 = al[idx1]
    ce = al[idxe]
    if ce>=f1:
        ce = 0
    dmax1 = 0
    idxa1 = idx0
    for i in range(idx0,idx1+1):
        fenmu = 0
        if al[i]>1:
            fenmu = al[i]
        else:
            fenmu = 1
        if float(fenmu) == float(0):
            fenmu = 1
        #b1 += (1.0 * (f1 - c0) * i / (idx1 - idx0) + c0 - al[i])/ fenmu
        if float(idx1-idx0) == float(0):
            idx1 = idx0 +1
        dt = abs((f1 - c0) * (i - idx0) - (idx1 - idx0)* al[i] + (idx1 - idx0) * c0)/ math.sqrt(math.pow(f1 - c0, 2) + math.pow(idx1 - idx0, 2))
        y = (f1 - c0)*(i-idx0)/(idx1-idx0)+c0
        if dmax1 < dt and y>al[i]:
            idxa1 = i
            dmax1 = dt
    idxs1 = idx1
    smax1 = 0
    for i in range(idxe-1,idx1-1):
        dt = abs((f1 - ce) * (idxe - i) - (idxe - idx1)	* al[i] + (idxe - idx1) * ce)/math.sqrt(math.pow(f1 - ce, 2) + math.pow(idxe - idx1, 2))
        y = (f1 - ce)*(i-idxe)/(idx1-idxe)+ce
        if (smax1 < dt and y>al[i]):
            idxs1 = i
            smax1 = dt
    result.append(idxa1)
    result.append(idx1)
    m = 0
    for i in range(idxa1,idxs1):
        m+=al[i]
    result.append(m)
    if float(m) == float(0):
        m = 1
    p = 1.0*al[idxa1]/m
    if p ==0:
        p= 0.0001
    result.append(p)
    result.append(len(al))
    return result

def getTwoBeauties(al,idx1,idx2):
    result = []
    b2 = 0
    b1 = 0
    flag = 0
    idxmax = 0
    idx0 = 0
    c0 = al[idx0]
    for i in range(0,idx1):#(int i=0;i<idx1;i++){
        if(al[i]<al[idx1] and al[i]<c0):
            idx0 = i
            c0 = al[i]
        idxe = len(al)-1
        f2 = al[idx2]
        f1 = al[idx1]
        ce = al[idxe]
        for i in range(len(al)-1,idx2):#(int i=al.size()-1;i>idx2;i--){
            if(al[i]<ce and al[i]<f2):
                idxe = i
                ce = al[i]
        idxa2 = idx0
        dmax2 = 0
        dmax1 = 0
        idxa1 = idx0
        for i in range(idx0, idx2+1):# (int i = idx0; i <= idx2; i++) {
            fenmu = 0
            if al[i]>1:
                fenmu = al[i]
            else:
                fenmu = 1
            #b2 += (1.0 * (f2 - c0) * i / (idx2 - idx0) + c0 - al[i])/ fenmu
            if float(idx2-idx0) == float(0):
                idx2 = idx0+1
            dt = abs((f2 - c0) * (i - idx0) - (idx2 - idx0)	* al[i] + (idx2 - idx0) * c0) / math.sqrt(math.pow(f2 - c0, 2) + math.pow(idx2 - idx0, 2));
            y = 1.0 * (f2 - c0)*(i-idx0)/(idx2-idx0)+c0
            if (dmax2 < dt and y>al[i]):
                idxa2 = i
                dmax2 = dt
        for i in range(idx0,idx1+1):#(int i = idx0; i <= idx1; i++) {
            fenmu = 0
            if al[i]>1:
                fenmu = al[i]
            else:
                fenmu = 1
            b1 += (1.0 * (f1 - c0) * i / (idx1 - idx0) + c0 - al[i]) / fenmu;
            dt = abs((f1 - c0) * (i - idx0) - (idx1 - idx0) * al[i] + (idx1 - idx0) * c0) / math.sqrt(math.pow(f1 - c0, 2) + math.pow(idx1 - idx0, 2))
            y = (f1 - c0)*(i-idx0)/(idx1-idx0)+c0
            if (dmax1 < dt and y>al[i]):
                idxa1 = i
                dmax1 = dt
        idxs1 = idx1
        idxs2 = idx2
        smax2 = 0
        smax1 = 0
        for i in range(len(al)-1,idx2):#(int i = al.size() - 1; i > idx2; i--) {
            if float(f2-ce) == float(0):
                f2 = ce +1
            dt = abs((f2 - ce) * (idxe - i) - (idxe - idx2)	* al[i] + (idxe - idx2) * ce) / math.sqrt(math.pow(f2 - ce, 2) + math.pow(idxe - idx2, 2))
            y = (f2 - ce)*(i-idxe)/(idx2-idxe)+ce
            if (smax2 < dt and y>al[i]):
                idxs2 = i
                smax2 = dt
        ce = al[idxa2]
        idxe = idxa2
        for i in range(idxa2,idx1):#(int i = idxa2;i>idx1;i--){
            if(al[i]<f1 and al[i]<ce):
                idxe = i
                ce = al[i]
        for i in range(idxe-1,idx1):#(int i = idxe-1; i > idx1; i--) {
            if float(f1-ce) == float(0):
                f1 = ce + 1
            dt = abs((f1 - ce) * (idxe - i) - (idxe - idx1)	* al[i] + (idxe - idx1) * ce) / math.sqrt(math.pow(f1 - ce, 2) + math.pow(idxe - idx1, 2))
            if float(idx1-idxe) == float(0):
                idx1 = idxe+1
            y = (f1 - ce)*(i-idxe)/(idx1-idxe)+ce
            if smax1 < dt and y>al[i]:
                idxs1 = i
                smax1 = dt

    result.append(idxa1)
    result.append(idx1)
    m1 = 0
    for i in range(idxa1,idxs1):
        m1+=al[i]
    result.append(m1)
    if float(m1) == float(0):
        m1 = 1
    p1 = 1.0*al[idxa1]/m1
    if p1 ==0:
        p1= 0.0001
    result.append(p1)
    result.append(idxa2)
    result.append(idx2)
    m2 = 0
    for i in range(idxa2,idxs2):
        m2+=al[i]
    result.append(m2)
    if float(m2) == float(0):
        m2 = 1
    p2 = 1.0*al[idxa2]/m2
    if p2 ==0:
        p2= 0.0001
    result.append(p2)
    result.append(len(al))
    return result

def getS(al,idx,k):
    result = 0
    startidx = 0
    if idx < k:
        startidx = 0
    else:
        startidx = idx-k

    endidx = 0
    end = len(al)-1
    if end <idx+k:
        endidx = end
    else:
        endidx= idx+k

    max1 = 0
    max2 = 0
    for i in range(int(startidx),int(idx)):
        if (al[idx]-al[i])>max1:
            max1 = al[idx]-al[i]
    for i in range(int(k+1),int(endidx+1)):
        if (al[idx]-al[i])>max2:
            max2 = al[idx]-al[i]

    result = 1.0*(max1+max2)/2
    return result



def bassOnePeak(paras):
    idxa1 = paras[0]
    idx1 = paras[1]
    m1 = paras[2]
    p1 = paras[3]
    l = paras[4]
    c = 0
    q1 = getq.getpq(p1, idx1-idxa1)
    X = range(0, l, 1)
    Y = []
    for t in range(0,idxa1):
        Y.append(0)
    for t in range(idxa1, l):
        y = (m1*math.pow(p1+q1, 2))/p1*(math.exp(-1.0*(p1+q1)*float(t-idxa1))/math.pow((q1/p1*math.exp(-1.0*(p1+q1)*(t-idxa1))+1),2))
        Y.append(y)
    return Y

def bassTwoPeaks(paras):
    idxa1 = paras[0]
    idx1 = paras[1]
    m1 = paras[2]
    p1 = paras[3]
    idxa2 = paras[4]
    idx2 = paras[5]
    m2 = paras[6]
    p2 = paras[7]
    l = paras[8]
    c = 0
    q1 = getq.getpq(p1, idx1-idxa1)
    X = range(0, l, 1)
    Y = []
    for t in range(0,idxa1):
        Y.append(0)
    for t in range(idxa1, idxa2):
        y = (m1*math.pow(p1+q1, 2))/p1*(math.exp(-1.0*(p1+q1)*float(t-idxa1))/math.pow((q1/p1*math.exp(-1.0*(p1+q1)*(t-idxa1))+1),2))
        Y.append(y)
    q2 = getq.getpq(p2, idx2-idxa2)
    for t in range(idxa2, l):
        y = (m2*math.pow(p2+q2, 2))/p2*(math.exp(-1.0*(p2+q2)*float(t-idxa2))/math.pow((q2/p2*math.exp(-1.0*(p2+q2)*(t-idxa2))+1), 2))+(m1*math.pow(p1+q1, 2))/p1*(math.exp(-1.0*(p1+q1)*float(t-idxa1))/math.pow((q1/p1*math.exp(-1.0*(p1+q1)*(t-idxa1))+1), 2))
        Y.append(y)
    return Y

def spd(al, h, k):
    oo = []
    result = []
    n = len(al)
    al_t = []
    for i in range(0,len(al)):
        al_t.append(getS(al,i,k))
    N =len(al_t)
    sum1=0.0
    sum2=0.0
    for i in range(N):
        sum1+= al_t[i]
        sum2+= al_t[i]**2
    mean=sum1/N
    var=math.sqrt(sum2/N-mean**2)
    for i in range(0,len(al)):
        if al_t[i]>0 and (al_t[i]-mean)>h*var:
            oo.append(i)
            result.append(i)
    temp = 0
    for ni in range(0,len(oo)-1):
        a = oo[ni+1]
        b = oo[ni]
        if (a-b)<=k:
            min = ni
            if al[a]>al[b]:
                min = ni
            else:
                min = ni+1
            if temp != min:
                result.remove(oo[min])
            temp = min
    return result

def judge(oo,al):
    result = []
    max1 = 0
    max2 = 0
    idx1 = 0
    idx2 = 0
    flag = False
    if (len(oo) >= 2):
        temp = 0;
        for j in range(0,len(oo)):
            if (max2 < al[oo[j]]):
                max2 = al[oo[j]]
                idx2 = oo[j]
                temp = j
        for i in range(0,temp):#int i = 0; i < temp; i++) {
            if (max1 < al[oo[i]]):
                max1 = al[oo[i]]
                idx1 = oo[i]
        idxbreak = 0
        maxbreak = max2
        if (max1 > 5 and idx1 > 0 and idx2 > idx1 and max2 > max1):
            for i in range(idx1+1,idx2):
                if (al[i] < 0.1 * max2):
                    flag = True
    if flag:
        result.append(idx1)
        result.append(idx2)
    return result

if __name__=='__main__':
    path = os.getcwd()
    file = io.open(path+'/series_data/event_data.txt',mode='r',encoding="utf-8")
    c = 0
    map = {}
    temp = ''
    for line in file.readlines():
        if c%2 ==0:
            temp = line.strip()
        else:
            list = []
            for si in line.strip()[1:-1].split(','):
                list.append(int(si))
            map[temp] = list
        c+=1
    k = 5
    h =0.5
    all_dict = dict()
    for key,value in map.items():
        lenth = len(value)
        print key, value.index(max(value))
        true_index = value.index(max(value))
        #value = value[:30]
        peak = spd(value,h,k)
        flag = judge(peak,value)
        if len(flag) == 2:
            paras = getTwoBeauties(value,flag[0],flag[1])
            paras[-1] = lenth
            series = bassTwoPeaks(paras)
        else:
            paras = getSingleBeauty(value)
            paras[-1] = lenth
            series = bassOnePeak(paras)
        print series.index(max(series))
        prediction_index = series.index(max(series))

        diff = abs(prediction_index-true_index)
        try:
            all_dict[diff] += 1
        except:
            all_dict[diff] = 1
    print all_dict
    print sorted(all_dict.iteritems(), key=lambda x:x[0], reverse=False)
    print sum(all_dict.values())
