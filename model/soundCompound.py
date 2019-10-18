# -*- coding:utf-8 -*-

from aip import AipSpeech



def getVoiceFromBaidu(word):
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
        with open('auido.mp3', 'wb') as f:
            f.write(result)

if __name__=="__main__":
    getVoiceFromBaidu("作为介词有. 关于；目的是；针对；忙于；因为；在……到处，的意思")
