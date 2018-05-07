# -*- coding: utf-8 -*-
from google_trans import translate as google_trans
from baidu_trans import translate as baidu_trans
from youdao_trans import translate as youdao_trans
from langconv import *
import time
import os
from aip import AipSpeech
import sys
sys.path.append('../../')
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.path.abspath(os.getcwd()), 'xnr'))

from xnr.global_config import BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY

'''
q为待翻译的语句组成的列表
trans()函数可选参数target_language, 代表翻译成哪种语言。
目前支持：
    target_language='zh-cn'(默认参数)
    target_language='en'(英语)
'''
def trans(q, target_language='zh-cn'):
    if isinstance(q, list):
        res = google_trans(q, target_language)
        if res:
            return res
        else:
            res = baidu_trans(q, target_language)
            if res:
                return res
            else:
                res = youdao_trans(q, target_language)
                if res:
                    return res
    return False

#繁体转简体
def traditional2simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

#简体转繁体
def simplified2traditional(sentence):  
    sentence = Converter('zh-hant').convert(sentence)  
    return sentence  

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#语音转文本
def voice2text(voice_path):
    #转换MP3文件为WAV格式文件
    mp3_file = voice_path
    wav_file = voice_path.split('.mp3')[0] + '.wav'
    cmd = ' lame --decode ' + mp3_file + ' ' + wav_file
    os.popen(cmd)
    #调用百度语音API，进行识别
    client = AipSpeech(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
    res = client.asr(speech=get_file_content(wav_file), format='wav', rate=8000, options={'lan': 'zh',})
    #转换完成之后，立即删除中间文件.wav。还没写这一点。。。
    try:
        if not res['err_no']:   #成功
            return res['result'][0]
        else:
            return res['err_msg']
    except Exception,e:
        print e
    return False

if __name__ == '__main__':
    # '''
    q = ['안녕하세요.', 'Hello world','test',"Jason Gao shared Joel Wang's post."]
    # q = ["絕食、減肥、刷存在感，到處都有不作秀就會死的人。不過作秀到最後也是把自己作死。 https://t.co/yVcGdVZ9h7"]
    # #q = ["ཁྱེད་གཉིས་ཞལ་འཕྲད་དགོས་。 7ཀརྨ་པ་ཨོ་རྒྱན་འཕྲིན་ལས་རྡོ་རྗེ་མཆོག་དང་་7ཀརྨ་པ་མཐའ་ཡས་རྡོ་རྗེ་མཆོག་གཉིས་ངེས་པར་དུ་ཞལ་མཇལ་འཛོམས་གནང ་ནས་ཞི་བའི་མཛའ་འབྲེལ་བསྐྲུན་དགོས་。ཁྱེད་རྣམ་གཉིས་མི་ལོ་མང་པོ་རིང་ལ་ཕན་ཚུན་ཞལ་འཕྲད་པའི་གསུང་གླེང་གང་ཡང ་མི་འདུགདེ་ནི་སྲིད་ཀྱི་གནོད་ཤུགས་དང་་。སྒེར་གྱི་བྱ་བ་ཞིག་གིས་ཡིན་ནམ་。གཞན་དུ་ན་ཅི་ཞིག་。ཁོ་བོས་འདི ་ནས་འབོད་སྐུལ་དང་་。དྲན་གསོ་ཞིག་བྱ་འདོད་པ་ཞ ིག་ལ་。ད་ལན་ངེད་བོད་རྒྱུད་ནང་བསྟན་གྱི་བླ་ཆེན་གཉིས་འབྲེལ་མེད་སོ་སོར་འཁོད་པའི་གནས་སྟངས་དེས་。འོག་གི་མཆོད་ སྡེ་ཁག་དང་་。དད་ལྡན་པ་རྣམས་ལ་གས་ཆག་ཅིག་མཐོང་སོང་་。ད་ནི་གས་ཆག་དེ་མེད་པར་བཟོ་མཁན་དེ་。སྤྲུལ་ སྐུ་ཁོང་གཉིས་ལ་འགན་འཁྲི་དེ་བབས་ཡོད་。སོང་ཙང་་。ཁྱེད་རྣམ་གཉིས་ངེས་པར་མཇལ་འཕྲད་གནང་ནས་ཕ་མ་གཅིག་གི་སྤུན ་ཟླ་ནང་བཞིན་ཕན་ཚུན་ལ་བརྩེ་བའི་འདུ་ཤེས་བསྟེན་དགོས་。ད ་ལྟར་བྱུང་ན་བོད་བྱིངས་དང་་。ལྷག་པར་བཀའ་རྒྱུད་ཀྱི་བསྟན་པའི་འཕྲིན་ལས་དེ་ཁྱབ་བརྡལ་མུ་མེད་དུ་འགྲོ་ངེས་。དེས་ ན་བཀའ་རྒྱུད་ཀྱི་བླ་ཆེན་དང་་。མཁན་པོ་。དད་ལྡན་པ་གཙོས་བོད་པ་ནང་བསྟན་ཆོས་ལུགས་རིས་མེད་སེམས་ལ་འཁྱིལ་ཚུན ་དེ་ལྟར་རེ་སྐུལ་དང་་。གདོང་གཏུགས་ཀྱི་བྱ་འགུལ་ངེས་པར་སྤེལ་དགོས་。སྤྱི་ལོ་。ཟླ217 10 13ཚེསཉིན་སྟོང་ཐུན་པས་ཚོར་བ ་དྲག་པོ་རླབས་ཀྱི་སྣག་ཚ་བྱས་ནས་ཤར་མར་ས ྲིངས་སོ་。་。"]
    # # q = ["RT @nyhopin: 失算的諜戰：郭文貴、劉彥平與川普、FBI （《點點今天事》）https://t.co/TQ97rNa1LH https://t.co/xARoQGmYRB"]
    # # m = ["RT @nyhopin: 失算的谍战：郭文贵、刘彦平与川普、FBI （《点点今天事》）https://t.co/TQ97rNa1LH https://t.co/xARoQGmYRB"]
    # # q = ["Jason Gao shared Joel Wang's post"]
    
    # start = time.time()
    # print trans(q)[0]
    print trans(q)[0].encode('utf-8')
    # end = time.time()
    # print end-start
    # '''

    # li = [u'', u'新聞、時事、中國內幕、香港台灣新聞、世界新聞、財經、名家點評、生活、教育、時尚、幽默、奇聞異事、娛樂、健康養生', u'正體：http://b5.secretchina.com/ 簡體：http://www.secretchina.com/']
    # # traditional_sentence = u'新聞、時事、中國內幕、香港台灣新聞、世界新聞、財經、名家點評、生活、教育、時尚、幽默、奇聞異事、娛樂、健康養生 正體：http://b5.secretchina.com/ 簡體：http://www.secretchina.com/'
    # ti = []
    # for l in li:    
    #     simplified_sentence = traditional2simplified(l)
    #     ti.append(l)
    #     print(simplified_sentence)
    # for t in ti:
    #     traditional_sentence = simplified2traditional(t)
    #     print(traditional_sentence)

    # voice_path = '/home/ubuntu8/Lvlei/xnr1/xnr/static/WX/voice/2018-01-03/a.mp3'
    # print os.path.isfile(voice_path)
    # print voice2text(voice_path)
