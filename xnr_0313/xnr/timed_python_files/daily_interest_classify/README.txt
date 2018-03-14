日常分类主函数调用

from daily_classifier import triple_classifier_new

输入数据：
text_list 微博文本list,[weibo1,weibo2,...]

输出数据：
result 类别标签（英文）list,[label1,label2,...]

特别说明：该函数是一个批量分类函数，可以一次输入多个文本进行分类，每条微博文本分类的时间约为0.03秒

标签中英文对照关系：
1.	旅游'travel'
2.	美食'food'
3.	汽车'cars'
4.	游戏'games'
5.	星座'constellation'
6.	音乐'music'
7.	影视'movie': 电影、电视剧、综艺 'movie', 'soup', 'shows'
8.	健身'fitness': 运动健身、瘦身 'exercise', 'fit'
9.	养生'health'：健康、养生 'health', 'well-being'
10.	体育'sports'
11.	萌宠'pets'
12.	动漫'cartoon'
13.	时尚'fashion': 艺术、美妆、时尚 'arts', 'makeup', 'fashion'
14.	鸡汤'soul': 宗教、情感 'religion', 'emotion'
