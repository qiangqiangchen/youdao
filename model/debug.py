# -*- coding:utf-8 -*-
from pydub import AudioSegment

from model.engine import getHtml



def demo1():
    # 加载mp3音频
    input_music_1 = AudioSegment.from_mp3(r"E:\youdao\youdao\basevoice\b.mp3")
    input_music_2 = AudioSegment.from_mp3(r"E:\youdao\youdao\basevoice\a.mp3")
    # 获取音频的响度（音量）
    input_music_1_db = input_music_1.dBFS
    input_music_2_db = input_music_2.dBFS


    # 获取音频的时长，单位为毫秒
    input_music_1_time = len(input_music_1)


    print(input_music_1_db)
    print(input_music_2_db)
    print(input_music_1_time)
    # print(input_music_1.duration_seconds)
    #    1-2
    db=input_music_1_db-input_music_2_db
    if db>0:
        input_music_2+=abs(db)
    elif db<0:
        input_music_1+=abs(db)

    print(input_music_1.dBFS)
    print(input_music_2.dBFS)

    # output=input_music_1+input_music_2
    # output.export("test1.mp3",format="mp3")



def demo2():
    input_music_1 = AudioSegment.from_mp3(r"E:\youdao\youdao\basevoice\a.mp3")
    #创建空的AudioSegment
    empty=AudioSegment.empty()

    #创建无声的AudioSegment
    ten_second_silence=AudioSegment.silent(duration=10000)

    #截取音频前10秒
    start=input_music_1[:10000]
    new=start+ten_second_silence+input_music_1[10000:]
    print(input_music_1.duration_seconds)
    print(new.duration_seconds)
    # new.export("new.mp3",format="mp3")



if __name__ == "__main__":
    demo1()
