# -*- coding: utf-8 -*-
import os
import json
import time
import sys

from elasticsearch import Elasticsearch
import networkx as nx
from community_shuaijian_gailv import find_community
import json,os,time,community

sys.path.append('../../')
from global_utils import es_user_portrait,es_user_profile,retweet_index_name_pre,retweet_index_type,\
                         comment_index_name_pre,comment_index_type,\
                         weibo_bci_history_index_name,weibo_bci_history_index_type,\
                         weibo_sensitive_history_index_name,weibo_sensitive_history_index_type


from global_config import S_TYPE,R_BEGIN_TIME,S_DATE,WEIBO_COMMUNITY_DATE

from time_utils import ts2datetime,datetime2ts
from parameter import DAY

sys.path.append('../../timed_python_files/community/')
from weibo_publicfunc import get_compelete_wbxnr
from weibo_create_target_user import create_xnr_targetuser

r_beigin_ts = datetime2ts(R_BEGIN_TIME)


##########定义公共变量
PATH = ''
FILE_NAME = 'graph_edges1.txt'


user_es = es_user_portrait

def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) % 2 + 1
    #run_type
    if S_TYPE == 'test':
        db_number = 1
    return db_number

now_ts = time.time()
db_number = get_db_num(now_ts)
retweet_index = retweet_index_name_pre + str(db_number)
retweet_type = retweet_index_type
comment_index = comment_index_name_pre + str(db_number)
comment_type = comment_index_type
influence_index = weibo_bci_history_index_name
influence_type = weibo_bci_history_index_type  #bci_week_ave
sensitive_index = weibo_sensitive_history_index_name
sensitive_type = weibo_sensitive_history_index_type #sensitive_week_ave 




def get_users(xnr_user_no,nodes=None):
    print 'xnr_user_no:::',xnr_user_no
    if not nodes:
        print 'get xnr es...'
        # result = xnr_es.search(index=save_index,doc_type=save_type,body={'query':{'match_all':{}},'size':999999})
        # result = result['hits']['hits']
        # uids = [i['_source']['uid'] for i in result]
        uids = create_xnr_targetuser(xnr_user_no)
    else:
        print 'have input nodes...'
        uids = nodes
    retweet_result = user_es.mget(index=retweet_index, doc_type=retweet_type,body={'ids':uids}, _source=True)['docs']
   # comment_result = user_es.mget(index=comment_index, doc_type=comment_type,body={'ids':uids}, _source=True)['docs']
   # print 'retweet_index::',retweet_index
   # print 'retweet_result:::',retweet_result
   # print 'comment_result:::',comment_result	
    G = nx.Graph()
   # retweet_result.sort(key=lambda k:(json.loads(k['_source']['uid_retweet']).getvalues()),reverse=True)
    for i in retweet_result:
       # print 'i:',i
        if not i['found']:
            continue
        uid_retweet = json.loads(i['_source']['uid_retweet'])
        max_count = max([int(n) for n in uid_retweet.values()])
        G.add_weighted_edges_from([(i['_source']['uid'],j,float(uid_retweet[j])/max_count) for j in uid_retweet.keys() if j != i['_source']['uid'] and j and i['_source']['uid']])

    # for i in comment_result:
    #     print 'comment_i:',i
        # if not i['found']:
        #     continue
        # uid_comment = json.loads(i['_source']['uid_comment'])
        # max_count = max([int(n) for n in uid_comment.values()])
        # G.add_weighted_edges_from([(i['_source']['uid'],j,float(uid_comment[j])/max_count) for j in uid_comment.keys() if j != i['_source']['uid'] and j and i['_source']['uid']])
       

    print 'GGG:::',G.number_of_nodes(),G.number_of_edges()
   # print 'G_nodes::',G.neighbors(2)
    print 'G has compelete!'    

    return G 


def find_from_uid_list(xnr_user_no,nodes=None,path=PATH,file_name=FILE_NAME,com_type='copra',G=None):
    #得到用户集
    print 'get users...',type(G)
    if not G:
        G = get_users(xnr_user_no,nodes)
    else:
        G = G.subgraph(nodes)
    print 'G::::',G
    print 'start to part community!!'
    node_clus = nx.clustering(G) #50w
    print 'number of users:',len(node_clus)
    nodes = [i for i in node_clus if node_clus[i]>0]#7w
    print 'node clustering > 0:',len(nodes)	
    allG = G
    print 'allg',allG.number_of_nodes()

    #根据聚集系数大于0筛选用户
    G = G.subgraph(nodes)
    try:
        G.remove_node('')
    except:
        pass
    # G.remove_nodes_from(list(set(node_clus)-set(nodes))) #80w边
    # G.remove_node('')
    print 'number of edges:',G.number_of_edges(),' number of nodes:',G.number_of_nodes()
    degree_dict = nx.degree_centrality(G)

    print 'find coms using ',com_type
    start = time.time()
    #选择采用的划分方法
    if com_type in ['oslom','slpa']:
        #存到文件里，调包用
        f = open(path+file_name,'w')
        count = 0
        for s,r in G.edges():
            if s and r:
                f.write(s+' '+r+' '+str(G[s][r]['weight'])+'\n')
                count += 1
                if count % 100 == 0:
                    print count 
        f.close()
        print('total nodes count:',len(nodes),' total edges count:',count)
        if com_type == 'oslom':
            coms = oslom_coms(path,file_name)
        else:
            coms = slpa_coms(path,file_name)
        coms_list = coms.values()
    else:
        #传边
        file_path = './weibo_data/' + ts2datetime(int(time.time())) + '_' + str(int(time.time()))
        coms_list = find_community(degree_dict,G,file_path)
    print 'find community time:',time.time()-start
    print 'post process...'
    coms_list = post_process(allG,coms_list)


    return G,allG,coms_list



def post_process(G,coms_list):
    #处理社区 过滤少于3的社区；对大于10000的社区再次划分
    new_coms = []
    count = 0
    for v in coms_list:
        if len(v) < 3:
            continue 
        elif len(v) > 10000:
            sub_g,sub_coms = find_from_uid_list(v,G=G)
            for sub_v in sub_coms:
                if len(sub_v)>=3:
                    new_coms.append(sub_v)
        else:
            new_coms.append(v)
    print 'len coms:',len(new_coms)
    return new_coms

def group_evaluate(xnr_user_no,nodes,all_influence,all_sensitive,G=None):
    result = {}
    result['xnr_user_no'] = xnr_user_no
    result['nodes'] = nodes
    result['num'] = len(nodes)
    if G:
        sub_g = G.subgraph(nodes)
    else:
        sub_g = get_users(xnr_user_no,nodes)
    result['density'] = round(nx.density(sub_g),4)
    result['cluster'] = round(nx.average_clustering(sub_g),4)
    result['transitivity'] = round(nx.transitivity(sub_g),4)

	# for i in user_es.mget(index=sensitive_index, doc_type=sensitive_type,body={'ids':nodes}, fields=['sensitive_week_ave'],_source=False)['docs']:
		# print i#['fields']['sensitive_week_ave']
	
    influence_result = [float(i['fields']['bci_week_ave'][0]) if i['found'] else 0  for i in es_user_profile.mget(index=influence_index, doc_type=influence_type,body={'ids':nodes}, fields=['bci_week_ave'],_source=False)['docs']]
    sensitive_result = [float(i['fields']['sensitive_week_ave'][0]) if i['found'] else 0 for i in es_user_profile.mget(index=sensitive_index, doc_type=sensitive_type,body={'ids':nodes}, fields=['sensitive_week_ave'],_source=False)['docs']]


    result['max_influence'] = round((max(influence_result)/float(all_influence))*100,4)
    result['mean_influence'] = round(((sum(influence_result)/len(influence_result))/float(all_influence))*100,4)

    result['max_sensitive'] = round((max(sensitive_result)/float(all_sensitive))*100,4)
    result['mean_sensitive'] = round(((sum(sensitive_result)/len(sensitive_result))/float(all_sensitive))*100,4)
    
    # result['mean_sensitive'] = 0.4670
    # result['mean_influence'] = 25.9874
    # result['density'] = 0.0068

    return result

def get_evaluate_max(index_name,index_type,field):
    query_body = {
        'query':{
            'match_all':{}
            },
        'size':1,
        'sort':[{field: {'order': 'desc'}}]
        }
    try:
        result = es_user_profile.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        max_evaluate = result[0]['_source'][field]
    except Exception, e:
        raise e
        max_evaluate = 1
    return max_evaluate


def oslom_coms(path,name): #1222.24431992秒
    t1 = time.time()
    print os.getcwd()
    os.system('cp '+path+name+' OSLOM2/OSLOM2/')
    os.system('OSLOM2/OSLOM2/./oslom_undir -f OSLOM2/OSLOM2/'+name+' -hr 0 -w')
    print time.time()-t1
    with open('OSLOM2/OSLOM2/'+name+'_oslo_files/tp') as f:
        #coms = collections.defaultdict(list)
        coms = {}
        i = 0
        j = 0
        lines = f.readlines()
        for line in lines:
            j += 1
            if j%2 == 0:
                coms[i] = line.split()
                i += 1
        #print 'coms',coms
    return coms  

def slpa_coms(path,name):
    t1 = time.time()
    os.chdir('/home/jiangln/own_weibo/code/GANXiS_v3.0.2')
    os.system('java -jar GANXiSw.jar  -i ../'+path+name)#+' -Sym 1'
    print name,time.time()-t1
    with open('output/SLPAw_'+name.split('.')[0]+'_run1_r0.4_v3_T100.icpm') as f:
    # os.system('java -jar GANXiSw.jar -i 107_m_6.txt -Sym 1')
    # print time.time()-t1
    # with open('output/SLPAw_107_m_6_run1_r0.4_v3_T100.icpm') as f:
        #coms = collections.defaultdict(list)
        coms = {}
        i = 0
        lines = f.readlines()
        for line in lines:
            coms[i] = line.split()
            i += 1
        #print 'coms:::',coms
    return coms


def ExtendQ(G,coms_list):
    #获取每个节点属于的标签数
    o = {}
    r = {}
    s = 0
    for i in coms_list:
        for j in i:
            try:
                o[j] += 1     
            except:
                o[j] = 1
    final_g = G.subgraph(o.keys())
    for i in final_g.adjacency():
        #i: ('a', {'c': {'weight': 2}, 'b': {'weight': 1}, 'd': {'weight': 1}})
        r[i[0]] = sum([j['weight'] for j in i[1].values()])
        s += r[i[0]]

    EQ = 0.0
    for com in coms_list:
        for i in com:
            for j in com:
                if i == j:
                    continue
                try:
                    EQ += (final_g.adj[i][j]['weight']-(r[i]*r[j])/s)/float(o[i]*o[j])
                except:
                    continue
    EQ = EQ/s
    
    return EQ


#组织社区生成
def create_weibo_community(xnr_user_no,today_time):
    

    #给定的nodes可能会因为网络结构或排序被删掉
    s = time.time()
    #得到划分的社区
    G,allG,coms_list = find_from_uid_list(xnr_user_no)
    print 'group evaluate...'

    all_influence = get_evaluate_max(influence_index,influence_type,'bci_week_ave')
    all_sensitive = get_evaluate_max(sensitive_index,sensitive_type,'sensitive_week_ave')

    print 'allG nodes:',allG.number_of_nodes()        
    print 'G nodes:',G.number_of_nodes()

    file_path = './weibo_data/' + xnr_user_no + '_' + ts2datetime(today_time) + '_' +'save_com.json'
    print 'file_path:',file_path
    f = open(file_path,'w')
    for k,v in enumerate(coms_list):
        #计算评价指标
        f.write(json.dumps(group_evaluate(xnr_user_no,v,all_influence,all_sensitive,G))+'\n')
    print 'total time:',time.time()-s
    print 'eq:',ExtendQ(allG,coms_list)
    mark = True
    return mark



if __name__ == '__main__':
    start_time = int(time.time())
    
    if S_TYPE == 'test':
        today_time = datetime2ts(WEIBO_COMMUNITY_DATE)
        xnr_user_no_list = ['WXNR0004']
    else:
        today_time = time.time()-0*DAY
        xnr_user_no_list = get_compelete_wbxnr()

    # xnr_user_no_list = ['WXNR0004']
    for xnr_user_no in xnr_user_no_list:
        create_weibo_community(xnr_user_no,today_time)


    end_time = int(time.time())
    print 'cost_time:::',end_time - start_time

