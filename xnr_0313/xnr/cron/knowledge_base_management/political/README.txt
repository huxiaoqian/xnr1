使用说明：
from political_main import political_classfiy

political_classfiy函数输入输出说明：
输入：
    uid_list:uid列表 [uid1,uid2,uid3,...]
    uid_weibo:分词之后的词频字典  {uid1:{'key1':f1,'key2':f2...}...}

输出：
    domain：政治倾向标签字典   {uid1:label,uid2:label2...}
