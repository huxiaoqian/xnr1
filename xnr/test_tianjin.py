# -*-coding:utf-8-*-
import json

from gexf import Gexf 

#uid = '2458565150'
def make_gexf(data):
    
    data = {"\u5409\u6da6\u8001\u5e74\u62a4\u7406\u9662": {"6275229294": "1", "6243523934": "1", "1877405305": "1", "1662421853": "1", "5991730933": "1", "6304836401": "1", "5814101383": "1", "\u4e50\u4e30\u8c46": "1", "\u6ec1\u5dde\u7535\u89c6\u6d77\u6587Heaven": "1", "3987847925": "1", "6098385442": "1", "1395351964": "1", "\u674e\u660c\u9686": "1", "5990899374": "1", "abcdefghijklmnpqrstvwxz\u552f\u7f3ayou": "1", "5745815627": "1", "\u516c\u6c11\u90b1\u5927\u6625": "1", "6318017985": "1", "5607760954": "1", "6270112614": "1", "\u56fd\u5b89\u963f\u7518": "1", "1664286135": "1", "5141377652": "1", "Hello\u95ee\u95ee": "2", "2757429615": "1", "\u88ab\u96e8\u6dcb\u6e7f\u7684\u6cb30017": "1", "6320356688": "1", "6018228099": "1", "6269797331": "1", "6272680967": "1", "6317341846": "1", "6322872796": "1", "1572341030": "1", "O\u5582O": "1", "6296904276": "1", "1450052847": "2", "\u82e5\u9c7c\u8fde\u7ebf": "2", "\u4e60\u8001\u5927\u7c89\u4e1d\u56e2": "1", "2823061207": "1", "3810928079": "2", "6250948222": "2", "edc\u738b\u6893\u6770": "1", "6272704962": "1", "1156630854": "1", "5402561705": "1", "5993430785": "1", "5957444703": "1", "6266167807": "1", "5992576619": "1", "\u4e2d\u56fd\u5218\u6770": "1", "5648019521": "7", "5724064182": "1", "5992650552": "3", "3016007484": "3", "6269796422": "1", "5976158583": "1", "5157327393": "1", "6041211181": "1", "6317405050": "1", "\u5feb\u4e50\u4eab\u53d7\u54e5": "1", "5447223426": "2", "6300381760": "1", "6272705212": "1", "3471083010": "1", "6261097607": "1", "5993415069": "1", "6325775390": "1", "\u6e58\u6f6d\u52c7\u54e5": "1", "3247863115": "1", "6271836519": "1", "6272698664": "1", "5074288254": "1", "3888986344": "1", "5656644495": "1", "5991731017": "1", "2176738144": "1", "\u5409\u6da6\u8001\u5e74\u62a4\u7406\u9662": "80", "\u732b\u80e1\u5b50003": "1", "6074312884": "1", "5882391111": "1", "1734279067": "2", "2962476841": "1", "5425602260": "1", "6310232656": "1", "5628161559": "1", "6272650627": "1", "6185995537": "2", "\u641c\u4e91\u770b\u96fe": "1", "2869600560": "1", "1735076091": "1", "1200567991": "1", "6268174030": "1", "\u6b27\u5185\u5c14": "1", "5892361259": "1", "5829771464": "1", "3841033240": "1", "\u7fe0\u82b1\u4e0d\u5728\u5bb6": "1", "5712636713": "1", "6321234042": "1", "5325071667": "1", "6272647920": "1", "5306773463": "1", "5360256624": "1", "6271961341": "1", "5658393186": "1", "6141995512": "1", "5972854058": "1", "3743662405": "1", "6328834480": "1", "1616360392": "1", "6318261070": "1", "5779227099": "1", "6272649295": "2", "5821128842": "1", "\u6f6e\u6c55\u4e4b\u58f0": "1", "2707227033": "1", "6272697292": "1", "6300969403": "1"}, "5878945047": {"1004971465": "3", "6263843085": "1", "3864099125": "1", "\u9633\u5149\u6da6\u6cc9": "1", "3396338004": "1", "6242248144": "5", "3186156695": "1", "1253353954": "1", "5414109077": "1", "6220490305": "1", "3099285325": "1", "6094786738": "1", "2003070025": "1", "1726282561": "2", "6000406541": "1", "\u8fc7\u5c71\u9f99\u95ed\u5634": "2", "6280422323": "2", "6277972476": "4", "6018522808": "1", "3769902564": "3", "2404927335": "1", "1641467814": "5", "3287139227": "2", "1874352720": "3", "6027160426": "1", "5697376801": "1", "6082049257": "3", "1801394715": "1", "5375191085": "1", "5378555683": "3", "2279627837": "1", "5841988388": "1", "5869689197": "2", "6262378498": "7", "6253832619": "1", "5357960585": "1", "5949001583": "1", "6240963220": "3", "5767209657": "1", "3059641932": "1", "6068690460": "1", "2837613893": "1", "5176650943": "2", "1041691681": "2", "6244015880": "1", "5102203725": "1", "6314828166": "1", "3223367355": "8", "\u9760\u8c31\u4e0d\u5f97": "1", "5816357083": "1", "3016007484": "4", "6283655778": "1", "1069976075": "1", "1342595314": "1", "6288081462": "1", "2997413405": "1", "5915750682": "1", "5878945047": "4", "3926320534": "1", "2972240965": "1", "2864775453": "1"}, "\u4e2d\u56fd\u5218\u6770": {"6073647904": "6"}, "\u65b9\u5728\u5317\u65b9": {"6142710234": "1", "2316814285": "1", "5940355413": "1", "5812762782": "1", "2295436394": "6", "6254661549": "1", "3815253542": "1", "2844259041": "2"}}

    gexf = Gexf("Gephi.org","A Web network")
    graph=gexf.addGraph("undirected","static","A Web network")
    graph.addNodeAttribute('size',type='integer')
    i = 0
    node_id_dict = {}
    for key,value in data.iteritems():
        if len(value.keys()):
            tmp = graph.addNode(str(i),key)
            tmp.addAttribute('size',str(len(value.keys())))
            if key not in node_id_dict.keys(): 
                node_id_dict[key] = str(i)
                i += 1
            #print 'key::',key

        for key_2,value_2 in value.iteritems():
            tmp = graph.addNode(str(i),key_2)
            tmp.addAttribute('size',str(value_2))
            if key_2 not in node_id_dict.keys():
                node_id_dict[key_2] = str(i)
                i += 1
           
            #print 'graph::',graph
    m = 0 
    for key,value in data.iteritems():
        print 'm::',m
        m+=1
        for key_2,value_2 in value.iteritems():   
            print 'm::::::',m
            graph.addEdge(node_id_dict[key],node_id_dict[key_2],str(value_2))
            m+=1

    print len(node_id_dict.keys())
    output_file=open("./data_network.gexf","w")
    gexf.write(output_file)


verified_num2ch_dict = {-1: u'普通用户', 0:u'名人', 1: u'政府', 2: u'企业',\
        3:u'媒体', 4:u'校园', 5: u'网站', 6:u'应用', 7:u'团体(机构)',\
        8:u'待审企业', 200:u'初级达人', 220:u'中高级达人', 400:u'已故v用户'}

def write_to_json(file_name,data):
    with open(file_name,'wb') as json_file:
        #json_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8', 'ignore'))
        json_file.write(json.dumps(data)+'\n')

## 写成json文件
data_all = {}
city_move_data = []
hashtag_data = []
with open('portrait_info_tianjin_0813.txt','rb') as f:
    for data in f:
        data = json.loads(data)
        for uid,uid_info in data.iteritems():
            # 迁徙图
            city_data_inner = []
            city_move_dict = uid_info['city_move_dict']
            for key_start,city_dict in city_move_dict.iteritems():
                for key_end,value in city_dict.iteritems():
                    city_data_inner.append([{'name':key_start},{'name':key_end,'value':value}])
                city_move_data.append([key_start,city_data_inner])

            data_all['city_move_data'] = city_move_data
            print 'city_move_data::',city_move_data

            # hashtag
            hashtag_dict = uid_info['hashtag_dict_group']
            hashtag_user = []
            hashtag_links = []
            count_hashtag = 0
            name_list = []
            print 'hashtag_dict::',hashtag_dict
            for user, user_hashtag in hashtag_dict.iteritems():
                if user_hashtag:
                    if user not in name_list:
                        hashtag_user.append({'name':user,'draggable':True,'category':0,'number':count_hashtag,'value':len(user_hashtag.keys()),'showNum':2})
                        name_list.append(user)
                        count_hashtag += 1
                        print 'user::',user
                    for hashtag_label, hashtag_count in user_hashtag.iteritems():
                        if hashtag_label not in name_list:
                            hashtag_user.append({'name':hashtag_label,'draggable':True,'category':1,'number':count_hashtag,'value':hashtag_count,'showNum':2})
                            hashtag_links.append({'source':user,'target':hashtag_label})
                            name_list.append(hashtag_label)
                            count_hashtag += 1
                            print 'hashtag_label::',hashtag_label
            
            hashtag_data.append(hashtag_user)
            hashtag_data.append(hashtag_links)
            data_all['hashtag_data'] = hashtag_data

            # 人格
            big5_data = [[u'外倾性',u'情绪稳定性',u'开放性',u'宜人性',u'尽责性'],[43,21,65,32,64]]
            black_data = [[{'text':u'家庭','max':100},\
                            {'text':u'抑郁','max':100},\
                            {'text':u'冲动','max':100},\
                            {'text':u'事业','max':100}],\
                            [56,46,86,32]]
            data_all['renge'] = [big5_data,black_data]

            # 画像
            
            weibo_user_dict = uid_info['weibo_user_dict']
            weibo_user_dict['verified_type'] = verified_num2ch_dict[weibo_user_dict['verified_type']]

            user_portrait_dict = uid_info['user_portrait_dict']
            user_portrait_dict['activeness'] = int(user_portrait_dict['activeness'])
            user_portrait_dict['influence'] = int(user_portrait_dict['influence'])
            user_portrait_dict['topic_string'] = user_portrait_dict['topic_string'].split('&')[0]

            weibo_user_dict.update(user_portrait_dict)

            data_all['user_info'] = weibo_user_dict


            write_to_json('data_portrait.json',data_all)
        

    