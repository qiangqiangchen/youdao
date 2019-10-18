# -*- coding:utf-8 -*-
import os

from pydub import AudioSegment

from model import engine, voiceOperate

"""
音频内容：[读单词+读字母分解+读单词+读意思+读单词*2]+[读短语*2]+[读例句*2]
歌词部分: 第一部分，（单词时间+1s+字母分解+1s+单词时间+意思时间*2+1s）
          第二部分，循环取（短语+1s）*2+意思+1s
          第三部分，读例句+1+意思+2

https://blog.csdn.net/weixin_44065501/article/details/86147964

https://blog.csdn.net/Debatrix/article/details/59058762

https://ptorch.com/news/112.html
"""

def fenjie(word):
    word_list=[]
    for i in word:
        word_list.append(AudioSegment.from_mp3('./basevoice/{}.mp3'.format(i)))
    _,fenjie=voiceOperate.addVoice(word_list)
    fenjie.export("fenjie.mp3","mp3")
    return fenjie


if __name__=='__main__':
    fenjie("about")
    # dir="./basevoice"
    # base_str="abcdefghijklmnopqrstuvwxyz"
    # for i in base_str:
    #     result = engine.pageOpear(i)
    #     filename = os.path.join(dir, "{}.mp3".format(i))
    #     engine.getfayin(result["voice_path"], filename)
