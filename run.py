# -*- coding:utf-8 -*-
import os

from pydub import AudioSegment
from model import soundCompound
from model import engine, voiceOperate
from model.soundCompound import fenjie

"""
音频内容：[读单词+读字母分解+读单词+读意思+读单词*2]+[读短语*2]+[读例句*2]
歌词部分: 第一部分，（单词时间+1s+字母分解+1s+单词时间+意思时间*2+1s）
          第二部分，循环取（短语+1s）*2+意思+1s
          第三部分，读例句+1+意思+2

https://blog.csdn.net/weixin_44065501/article/details/86147964

https://blog.csdn.net/Debatrix/article/details/59058762

https://ptorch.com/news/112.html
"""


#获取单词字母读音，返回一个AudioSegment对象
# def fenjie(word):
#     word_list=[]
#     for i in word:
#         word_list.append(AudioSegment.from_mp3('./basevoice/{}.mp3'.format(i)))
#     durationTime,fenjie=voiceOperate.addVoice(word_list)
#     (fenjie+voiceOperate.makeSilentVoice(5000)+fenjie).export("fenjie.mp3","mp3")
#     return durationTime,fenjie

def lrcFormat(starttime,txt):
    m=starttime//60000
    if m<10:
        m="0{}".format(m)
    s=round(starttime/1000%60,2)
    if s<10:
        s="0{}".format(s)
    return "[{}:{}]{}".format(m,s,txt)


def part1(temp):
    audio_list=[]
    lrc_txt=[]
    lrc_time_current=0
    #第一部分
    word=temp["word"]
    #获取读音加入列表
    word_sound=soundCompound.getVoiceByYoudao(temp["voice_path"])
    lrc_time_current += len(word_sound)
    lrc_txt.append(lrcFormat(lrc_time_current,word+"  "+temp["phonetic_USA"]))
    audio_list.append(word_sound)
    #获取分解读音并加入列表
    word_fenjie=soundCompound.fenjie(word)
    audio_list.append(word_fenjie)
    lrc_time_current +=len(word_fenjie)
    lrc_txt.append(lrcFormat(lrc_time_current, word+"  "+temp["phonetic_USA"]))
    #再加1遍读音
    audio_list.append(word_sound)
    lrc_time_current += len(word_sound)
    lrc_txt.append(lrcFormat(lrc_time_current,word+"  "+temp["phonetic_USA"]))
    #获取翻译语音并加入列表
    for i in temp["trans_str"]:
        trans=soundCompound.getVoiceByBaidu(i)
        audio_list.append(trans)
        lrc_time_current += len(trans)
        lrc_txt.append(lrcFormat(lrc_time_current, i))

    # 再加2遍读音
    audio_list.append(word_sound*2)
    lrc_time_current += len(word_sound*2)
    lrc_txt.append(lrcFormat(lrc_time_current, word + temp["phonetic_USA"]))


    #第二部分
    #获取常用短语并加入列表
    for j in temp["wordGroup_str"]:
        wordGroup=soundCompound.getVoiceByBaidu(j)
        audio_list.append(wordGroup*2)
        lrc_time_current += len(wordGroup*2)
        lrc_txt.append(lrcFormat(lrc_time_current, j))

    #加个1秒间隔
    audio_list.append(voiceOperate.makeSilentVoice(1000))
    lrc_time_current +=1000
    #第三部分
    #获取例句以及翻译，例句读两遍，加入列表

    for k in temp["examples"]:
        sent=soundCompound.getVoiceByYoudao(k["sent_voice"])
        audio_list.append(sent*2)
        lrc_time_current += len(sent * 2)
        lrc_txt.append(lrcFormat(lrc_time_current, k["example"]))
        fanyi=soundCompound.getVoiceByBaidu(k['fanyi'])
        audio_list.append(fanyi)
        lrc_time_current += len(fanyi * 2)
        lrc_txt.append(lrcFormat(lrc_time_current,k['fanyi']))


    voiceOperate.save(voiceOperate.addVoice(audio_list),"temp.mp3")
    for line in lrc_txt:
        print(line)







if __name__=='__main__':
    temp={'word': 'about', 'phonetic_USA': '[əˈbaʊt]', 'voice_path': 'http://dict.youdao.com/dictvoice?audio=about&type=2', 'trans_str': ['作为副词有. 大约；将近；到处；（特定位置）四下；闲着；周围；掉头，的意思', '作为介词有. 关于；目的是；针对；忙于；因为；在……到处；在……四处；在……附近；在……（具有某种品质）；围绕；为……感到，的意思', '作为形容有. 在场的，可得到的；就要……的；四处走动的；有证据的，在起作用的，的意思', '作为名词有. (About) （法、印、美）阿布（人名），的意思'], 'wordGroup_str': ['how about,你认为…怎样', 'what about,怎么样；（对于）…怎么样', 'all about,到处，各处；关于…的一切', 'about us,关于我们；公司简介', 'do about,处理；应付；就某事采取行动或措施', 'go about,v. 着手做；四处走动；传开；从事', 'about to do,刚要；即将', 'about of,打算；即将', 'out and about,能够外出走动', 'up and about,（病人病情好转）起床走动', 'on or about,大约于…'], 'examples': [{'example': 'Then he enquired everything about her.', 'fanyi': '然后他打听有关她的一切。', 'sent_voice': 'http://dict.youdao.com/dictvoice?audio=Then+he+enquired+everything+about+her.&le=eng'}, {'example': 'Do you have anything to say about this?', 'fanyi': '有关这件事你有没有什么要说的？', 'sent_voice': 'http://dict.youdao.com/dictvoice?audio=Do+you+have+anything+to+say+about+this%3F&le=eng'}, {'example': 'Curiosity. Why do you have curiosity about me?', 'fanyi': '好奇心。你们为什么对我有好奇心？', 'sent_voice': 'http://dict.youdao.com/dictvoice?audio=Curiosity.+Why+do+you+have+curiosity+about+me%3F&le=eng'}]}
    part1(temp)

