# -*- coding:utf-8 -*-

from aip import AipSpeech

from model.engine import getHtml


def getVoiceByBaidu(word,filename):
    """ 你的 APPID AK SK """
    APP_ID = '9998866'
    API_KEY = 'C4VUcZCpy4hpSyP4zEAC7GMF'
    SECRET_KEY = '0800e45aca7c8bfafabadea8deb93762'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(word, 'zh', 1, {
        'vol': 5,'per':1,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(filename, 'wb') as f:
            f.write(result)


def getVoiceByYoudao(url,filename):
        res = getHtml(url)
        with open(filename, 'wb') as f:
            f.write(res.content)

if __name__=="__main__":
    # getVoiceByBaidu("Curiosity. Why do you have curiosity about me?,好奇心。你们为什么对我有好奇心？","audio.mp3")
    getVoiceByYoudao("http://dict.youdao.com/dictvoice?audio=Curiosity.+Why+do+you+have+curiosity+about+me%3F&le=eng","fanyi.mp3")
