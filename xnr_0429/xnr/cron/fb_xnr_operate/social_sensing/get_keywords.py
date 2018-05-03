# -*-coding:utf-8-*-

from  textrank4zh import TextRank4Keyword,TextRank4Sentence

def extract_keyword(text):
    word = TextRank4Keyword()
    word.analyze(text,window = 2,lower = True)
    w_list = word.get_keywords(num = 20,word_min_len = 1)  
    print w_list

    for w in w_list:
        print w.word,w.weight 
    print sorted(w_list, key=lambda x:x["weight"], reverse=True)[:5]

    phrase = word.get_keyphrases(keywords_num = 5,min_occur_num=2)  

if __name__ == "__main__":
    text = "【江西一老人遇车祸拒绝赔偿，现场安慰司机“我不讹你们的钱”】3月3日，一篇《#不讹人#为刘振仕老人点赞》的微博引发网友关注。据博主介绍，刘振仕今年77岁，是吉安市泰和县人。2日上午，刘振仕乘坐的三轮车拐道时，和相向的一辆小车相撞。当即，三轮车侧翻，他从车上摔下来，所幸仅手掌被擦伤了一点。正当小车司机肖杨杰手足无策时，老人安慰他们别慌：“我不讹司机，我家四个儿子都有车，知道开车的难处，我不讹你们的冤枉钱。”救护车来后，老人还是不肯去，“去一下医院至少一千多，你们现在赚钱也不容易，我到时候回家敷点草药就没事了，你们放心。就算等会真的有什么事，我也不会找你们麻烦。”老人还拒绝了肖杨杰的赔偿，说给了钱也会花掉。肖杨杰说，自己当时非常感动，无以言"
    extract_keyword(text)
