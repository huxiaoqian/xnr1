用户话题分类函数test_topic.py中的topic_classfiy函数


用户话题偏好分类调用方法：
from test_topic import topic_classfiy
函数输入、输出说明：
输入数据示例：
uidlist:mid列表（[mid1,mid2,mid3,...]）
uid_weibo:分词之后的词频字典（{mid1:{'key1':f1,'key2':f2...}...}）

输出数据示例：字典
用户关注较多的话题（1个）：
{uid1:['art']...}