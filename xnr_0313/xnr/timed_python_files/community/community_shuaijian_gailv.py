# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 16:55:54 2016

@author: NaNa
"""

from numpy import *
import time
import copy
import numpy as np
import pandas as pd
import math
import os,json
import networkx


def Propagate(x,old, new, neighbours,v,uid_index,asynchronous,degree_dict):
    x_index=uid_index[x]    
    new[x_index] = {}
    #洗牌保证随机性（都相等的情况）  现在是按权重排序的
    #random.shuffle(neighbours)
    #print 'neighbours',neighbours
    #依据邻结点标签集更新该节点
    for eachpoint in neighbours:   #对于节点的每个邻居
        eachpoint_index=uid_index[eachpoint[0]]
        for eachlable in old[eachpoint_index]:   #这个邻居在之前表里有的点
            b = old[eachpoint_index][eachlable]      #53 23 55  代表标签
            #print 'b',b
            try:
                degree_dict[eachlable]
            except:
                degree_dict[eachlable] = 0

            if b[1]>0:

                if eachlable in new[x_index]:
                    new[x_index][eachlable] += (new[x_index][eachlable][0] + b[0]*eachpoint[1]*degree_dict[eachlable], b[1]-0.2)   #b*nei_weights[eachpoint_index]  12/19 #标签
                else:
                    new[x_index].update({eachlable:(b[0]*eachpoint[1]*degree_dict[eachlable],b[1]-0.2)})   #b*nei_weights[eachpoint_index]
            if asynchronous:
                old[x_index] = copy.deepcopy(new[x])
    Normalize(new[x_index])
    #print new[x]
    maxb = 0.0
    maxc = 0
    t = []
    #去除小于1/v的候选项，若均小于则''选b最大的赋值''，否则规范化
    for each in new[x_index]:
        if new[x_index][each][0] < 1/float(v):
            t.append(each)
            if new[x_index][each][0] >= maxb:#取最后一个
            #if new[x][each] > maxb:#取第一个
                maxb = new[x_index][each][0]
                maxc = each
    for i in range(len(t)):
        del new[x_index][t[i]]
    if len(new[x_index]) == 0:
        #new[x][maxc] = 1   #应该是x
        new[x_index][x] = (1,1)
    else:
        Normalize(new[x_index])



def Normalize(x):
    sums = 0.0
    for each in x:
        sums += x[each][0]
    for each in x:
        if sums != 0:
            # x[each][0] = x[each][0]/sums
            x[each] = (x[each][0]/sums,x[each][1])

def id_l(l):
    ids = []
    for each in l:
        ids.append(id_x(each))
    return ids

def id_x(x):
    ids = []
    for each in x:
        ids.append(each)
    return ids

def pd_count(l):
    counts = {}
    for eachpoint in l:
        for eachlable in eachpoint:
            if eachlable in counts:
                n = counts[eachlable]
                counts.update({eachlable: n+1})
            else:
                counts.update({eachlable: 1})
    return counts

def mc(cs1, cs2):
    #print cs1,cs2
    cs = {}
    for each in cs1:
        if each in cs2:
            cs[each] = min(cs1[each], cs2[each])
    return cs

def Modulartiy(A, coms, sums,vertices):
    Q = 0.0
    for eachc in coms:
        li = 0
        for eachp in coms[eachc]:
            for eachq in coms[eachc]:
                try:
                    li += A[eachp][eachq]
                except:
                    pass
        li /= 2
        di = 0
        for eachp in coms[eachc]:
            for eachq in range(vertices):
                try:
                    di += A[eachp][eachq]
                except:
                    pass
        Q = Q + (li - (di * di) /(sums*4))
    Q = Q / float(sums)
    return Q
    
#input:邻接矩阵、每类的点的索引
def cal_modularity(m,clusters):
    #print type(clusters),len(clusters)
    #print 'clusters:',clusters
    Q = 0
    m = np.array(m)
    degree = np.sum(m,axis=1)
    total_degree = float(m.sum())
    #print clusters
    for node_list in clusters:#0,2
        #print len(node_list),type(node_list)
        tot = 0
        in_degree = 0
        for i in range(len(node_list)):#0
            for j in range(len(node_list)):#2
                if i == j:
                    continue
                in_degree += m[node_list[i]][node_list[j]]
            tot += degree[node_list[i]]    
        Q += in_degree/total_degree - (tot/total_degree)**2
    #print Q
    return Q    
    

def ExtendQ(A,coms,sums,o,uid_index,r):
    #k-每个节点的度数 o-每个节点属于的社区数
    s = sums
    #k = sorted(k, key=lambda x: x[0], reverse=False)

    EQ = 0.0
    # r = np.sum(A['final'],axis=1)
    # r = A.groupby('idA')['final'].sum()
    print 'coms.values():',len(coms.values())
    count = 0
    for com in coms.values():
        print len(com)
        for i in com:
            for j in com:
                if i ==j :
                    continue
                # print '1111:',A['final'][(A['idA']==i)&(A['idB']==j)]

                try:
                    value = A[i][j]
                except:
                    try:
                        value = A[j][i]
                    except:
                        continue
                count += 1
                EQ += (value-(r[i]*r[j])/s)/float(o[uid_index[i]]*o[uid_index[j]])
                # print EQ
    print 'eq counts:',count
    EQ = EQ/s
    
    return EQ


def deal_c(circle,mix,sort_rel,vers):
    c_set = set()    
    for c_v in circle.values():
        for c_j in c_v:
            c_set.add(c_j)
    c_list = list(c_set)
    circle_new = {}
    for k,v in circle.iteritems():
        circle_new[k]=[c_list.index(j) for j in v]
    
    mix_new=mix[c_list][:,c_list]
    mask = np.argsort(-mix_new,axis=1)[:,vers:]
    for i in range(len(mix_new)):
        mix_new[i][mask[i]]=0
    new_rel = [c_list.index(i) for i in sort_rel if i in c_list]    
    return circle_new,mix_new,len(c_list),new_rel


def split_deal_c(circle,fri,mix,sort_rel,vers):
    c_set = set()    
    for c_v in circle.values():
        c_set=c_set| set(c_v)

    c_list = list(c_set)
#    circle_new = {}
#    for k,v in circle.iteritems():
#        circle_new[k]=[c_list.index(j) for j in v]
    
    fri_new=fri.loc[c_list,c_list]
    mix_new=mix.loc[c_list,c_list]
#    mask = np.argsort(-mix_new,axis=1)[:,vers:]
#    for i in range(len(mix_new)):
#        mix_new[i][mask[i]]=0
    new_rel = [i for i in sort_rel if i in c_list]    
    return circle,fri_new,mix_new,len(c_list),new_rel


def na_nmi(a,b,vertics):
    info = 0.0
    for i in a.keys():
        for j in b.keys():
            inter = len(set(a[i])&set(b[j]))
            if inter != 0:
                a1 = (float(inter)*vertics)/(len(a[i])*len(b[j]))
                b1 = math.log(a1,2)*(float(inter)/vertics)
                info += b1
    h = 0.0
    for dicts in [a,b]:
        for k in dicts.keys():
            if len(dicts[k]) != 0:
                p = float(len(dicts[k]))/vertics
                h += - p*(math.log(p,2))
    nmi = info*2/h
    return round(nmi,3)


def split_matrix(data,v,sort_rel,s,data_df,degree_dict):
    #real_c,fri,mix,vertices,sort_rel = split_deal_c(real_c,fri,mix,sort_rel,v)
    #print '?'
    #vertices = len(A)    
    range_list = list(set(data_df['idA'].unique())|(set(data_df['idB'].unique())))
    label_new = [{} for i in range_list]
    label_old = [{i: (1,1)} for i in range_list]
    minl = {}
    oldmin = {}
    flag = False# asynchronous
    itera = 0# 迭代次数
    start = time.clock()# 计时
    
    uid_index={}
    for i,j in enumerate(range_list):
        uid_index[j]=i    
        
    #同异步迭代过程
    while True:   
        '''
        if flag:
            flag = False
        else:
            flag = True
        '''
        itera += 1
        #vers = copy.deepcopy(range_list)
        print 'iter:',itera
        count = 0
        for i in sort_rel:
            #i = random.choice(vers)
            if count % 1000 == 0:
                print itera,count
            count += 1
            # neighbours = data[data['idA'] == i]
            # neighbours.index = neighbours['idB']
            # neighbours = neighbours['final'].to_dict()
            neighbours = sorted(data[i].iteritems(),key=lambda x:x[1],reverse=True)
            Propagate(i,label_old, label_new, neighbours, v, uid_index,flag,degree_dict)
            #vers.remove(i)

        if id_l(label_old) == id_l(label_new):
            minl = mc(minl, pd_count(label_new)) #统计每个标签出现的次数
        else:
            minl = pd_count(label_new)
        if minl != oldmin:
            label_old = label_new
            oldmin = minl
        else:
            break
        #test
        # if itera > 10:
        #     break
    print 'iter:',itera
    coms = {}
    sub = {}
    for each in range_list:      #点数
        ids = id_x(label_old[uid_index[each]])
        for eachc in ids:
            if eachc in coms and eachc in sub:
                coms[eachc].append(each)
            #elif :
                sub.update({eachc: set(sub[eachc]) & set(ids)})  #标签的交集
            else:
                coms.update({eachc:[each]})  #each——这个点 eachc——有的某个标签   ids所有标签
                sub.update({eachc:ids})
    #sub最后得到的就是里面的点都一样的 可以去掉的社区
    #coms=real_c
    #获取每个节点属于的标签数
    o = [0 for i in range_list]
    for i in coms.values():
        for j in i:
            o[uid_index[j]] += 1     

    # print 'sub:',sub
    for each in sub:
        if len(sub[each]):
            for eachc in sub[each]:  #这个标签社区each下的点有的别的标签eachc
                if eachc != each:    #别的标签不等于这个标签的话
                    coms[eachc] = list(set(coms[eachc]) - set(coms[each]))   #别的标签的成员减去这个社区的成员    
    j = 0
    counts = 0
    for i in coms.values():
        j += len(i)
        if len(i)>0:
            counts+=1
    print 'total counts:',j
    elapsed = (time.clock() - start)
    #nmi = na_nmi(coms,real_c,len(range_list))    
    #print ExtendQ(fri,coms,fri.sum().sum()
    r = data_df.groupby('idA')['final'].sum()
    #EQ_mix':ExtendQ(data,coms,s,o,uid_index,r)
    return {'total counts':j,'t':elapsed,'counts':counts,'coms':coms,'m':v,'iter':itera}



def read_data_dict(path,name):
    data = {}
    data_df = []
    lines = open(path+name,'r').readlines()
    for i in lines:
        i = i.strip().split(' ')
        tmp_dict = {'idA':i[0],'idB':i[1],'final':float(i[2])}
        data_df.append(tmp_dict)
        try:
            data[tmp_dict['idA']][tmp_dict['idB']] = tmp_dict['final']
        except:
            data[tmp_dict['idA']] = {tmp_dict['idB']:tmp_dict['final']}
        try:
            data[tmp_dict['idB']][tmp_dict['idA']] = tmp_dict['final']
        except:
            data[tmp_dict['idB']] = {tmp_dict['idA']:tmp_dict['final']}

        data_df.append({'idA':i[1],'idB':i[0],'final':float(i[2])})

    df = pd.DataFrame(data_df)       
    df = df.drop_duplicates()      
    return data,df

def read_data_dict_from_g(G):
    print type(G)
    print networkx.__version__
    data = {}
    data_df = []
    for i,j in G.edges():
        tmp_dict = {'idA':i,'idB':j,'final':G[i][j]['weight']}
        data_df.append(tmp_dict)
        try:
            data[tmp_dict['idA']][tmp_dict['idB']] = tmp_dict['final']
        except:
            data[tmp_dict['idA']] = {tmp_dict['idB']:tmp_dict['final']}
        try:
            data[tmp_dict['idB']][tmp_dict['idA']] = tmp_dict['final']
        except:
            data[tmp_dict['idB']] = {tmp_dict['idA']:tmp_dict['final']}

        data_df.append({'idA':j,'idB':i,'final':G[j][i]['weight']})
    df = pd.DataFrame(data_df)       
    print df.head()
    df = df.drop_duplicates()      
    return data,df


def find_community(degree_dict,G,output_name):
    t1 = time.time()
    # data,data_df = read_data_dict(path,name)
    data,data_df = read_data_dict_from_g(G)
    print data_df.head()
    print data_df.columns

    sort_rel = sorted(degree_dict.iteritems(),key=lambda x:x[1],reverse=True)
    sort_rel = [i[0] for i in sort_rel]

    s = data_df['final'].sum()
    print s
    data_dict = {}
    result = split_matrix(data,6,sort_rel,s,data_df,degree_dict)
    # print result
    print 'copra find community time:',time.time() - t1
    df = pd.DataFrame([result])
    df.to_csv(output_name+'.csv')
    return result['coms'].values()

if __name__ == '__main__':
    #节点个数,V
    #vertices = [34,115,105,62]
    #txtlist = ['karate.txt','football.txt','books.txt','dolphins.txt']
    data,data_df = read_data_dict()
    print data_df.head()
    print data_df.columns

    sort_rel = sorted(degree_dict.iteritems(),key=lambda x:x[1],reverse=True)
    sort_rel = [i[0] for i in sort_rel]

    s = data_df['final'].sum()
    print s
    data_dict = {}
    result = split_matrix(data,6,sort_rel,s,data_df,degree_dict)
    # print result
    df = pd.DataFrame([result])
    df.to_csv('weibo_coms_20171212_6.csv')