# -*- coding:utf-8 -*-
import math

import multiprocessing

import os

import time
from bs4 import BeautifulSoup
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

def demo3():
    base_url="https://www.shanbay.com/wordlist/3127/26842/?page={}"
    base_url_list=[base_url.format(i) for i in range(1,50)]
    word_list=[]
    for i in base_url_list:
        res=getHtml(i)
        soup = BeautifulSoup(res.text, features="html.parser")
        words=soup.find_all(name="td", attrs={"class":"span2"})
        # print(len(words))
        for word in words:
            word_list.append(word.strong.get_text())
    print(len(word_list))
    with open("words.txt","w") as f:
        f.write(",".join(word_list))


def print_word(list):
    for i in list:
        print("{}进程输出:{}".format(os.getpid(),i))
        time.sleep(1)


def demo4():
    words = ["abandon", "absent", "absolute", "absorb", "abuse","academic","accept","accident","accompany",
             "accomplish","account","accumulate","accurate"]
    pool = multiprocessing.Pool(3)
    for i in range(math.ceil(len(words)//5)+1):
        # print(words[i*5:i*5+5])
        pool.apply_async(print_word, (words[i*5:i*5+5],))
    pool.close()
    pool.join()



if __name__ == "__main__":
    demo4()
