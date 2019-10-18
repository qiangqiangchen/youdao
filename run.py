# -*- coding:utf-8 -*-
import os

from model import engine

"""
音频内容：读单词+读意思+读字母分解+读单词*2+读例句*2
https://blog.csdn.net/weixin_44065501/article/details/86147964

https://blog.csdn.net/Debatrix/article/details/59058762

https://ptorch.com/news/112.html
"""




if __name__=='__main__':
    dir="./basevoice"
    base_str="abcdefghijklmnopqrstuvwxyz"
    for i in base_str:
        result = engine.pageOpear(i)
        filename = os.path.join(dir, "{}.mp3".format(i))
        engine.getfayin(result["voice_path"], filename)
