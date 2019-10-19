# -*- coding:utf-8 -*-
import os

from pydub import AudioSegment
from model import soundCompound
from model import engine, voiceOperate
from model.engine import pageOpear
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


def part1(temp,starttime=0):
    print(starttime)
    audio_list=[]
    lrc_txt=[]
    lrc_time_current=starttime
    #第一部分
    word=temp["word"]
    #获取读音加入列表
    word_sound=soundCompound.getVoiceByYoudao(temp["voice_path"])

    lrc_txt.append(lrcFormat(lrc_time_current,word+"  "+temp["phonetic_USA"]))
    lrc_time_current += len(word_sound)
    audio_list.append(word_sound)
    #获取分解读音并加入列表
    word_fenjie=soundCompound.fenjie(word)
    audio_list.append(word_fenjie)

    lrc_txt.append(lrcFormat(lrc_time_current, word+"  "+temp["phonetic_USA"]))
    lrc_time_current += len(word_fenjie)
    #再加1遍读音
    audio_list.append(word_sound)

    lrc_txt.append(lrcFormat(lrc_time_current,word+"  "+temp["phonetic_USA"]))
    lrc_time_current += len(word_sound)
    #获取翻译语音并加入列表
    for i in temp["trans_str"]:
        trans=soundCompound.getVoiceByBaidu(i)
        audio_list.append(trans)
        lrc_txt.append(lrcFormat(lrc_time_current, i))
        lrc_time_current += len(trans)

    # 再加2遍读音
    audio_list.append(word_sound*2)

    lrc_txt.append(lrcFormat(lrc_time_current, word + temp["phonetic_USA"]))
    lrc_time_current += len(word_sound * 2)


    #第二部分
    #获取常用短语并加入列表
    for j in temp["wordGroup_str"]:
        wordGroup=soundCompound.getVoiceByBaidu(j)
        audio_list.append(wordGroup*2)
        lrc_txt.append(lrcFormat(lrc_time_current, j))
        lrc_time_current += len(wordGroup * 2)

    #加个1秒间隔
    audio_list.append(voiceOperate.makeSilentVoice(1000))
    lrc_time_current +=1000
    #第三部分
    #获取例句以及翻译，例句读两遍，加入列表

    for k in temp["examples"]:
        sent=soundCompound.getVoiceByYoudao(k["sent_voice"])
        audio_list.append(sent*2)
        lrc_txt.append(lrcFormat(lrc_time_current, k["example"]))
        lrc_time_current += len(sent * 2)
        fanyi=soundCompound.getVoiceByBaidu(k['fanyi'])
        audio_list.append(fanyi)
        lrc_txt.append(lrcFormat(lrc_time_current,k['fanyi']))
        lrc_time_current += len(fanyi)


    # voiceOperate.save(voiceOperate.addVoice(audio_list),"temp.mp3")
    return voiceOperate.addVoice(audio_list),lrc_time_current,lrc_txt


def comp(word_list):
    start_time=0
    lrc_list=[]
    audio_list=[]
    for i in word_list:
        print("正在爬取{}".format(i))
        r=pageOpear(i)
        audio,lrc_time,lrc_txt=part1(r,start_time)
        start_time+=len(audio)
        audio_list.append(audio)
        lrc_list+=lrc_txt

    voiceOperate.save(voiceOperate.addVoice(audio_list),"test1.mp3")
    print(start_time)
    with open("test1.txt","w",encoding="utf-8") as f:
        f.write("\n".join(lrc_list))





if __name__=='__main__':
    words=["abandon","absent","absolute","absorb","abuse"]
    comp(words)
    print("合成完成")
