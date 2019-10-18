from pydub import AudioSegment


#调整两个音频的响度一致， 返回一个AudioSegment对象
def change_voice_dbfs(music1,music2):
    music1_db=music1.dBFS
    music2_db=music2.dBFS
    db=music1_db-music2_db
    if db>0:
        music2+=abs(db)
    elif db<0:
        music1+=abs(db)
    return music1,music2


#制作一个无声音频对象并返回
def makeSilentVoice(duration):
    # 创建无声的AudioSegment
    silence = AudioSegment.silent(duration=duration)
    return silence


def addVoice(v_list):
    playlist=AudioSegment.empty()
    for sound in v_list:
        playlist+=sound
    return playlist


def getSoundDb(sound):
    return sound.dBFS


def changeDb(sound):
    base_db=-15
    db=sound.dBFS-base_db
    if db>0:
        sound-=abs(db)
    elif db<0:
        sound+=abs(db)
    return sound

def multi_changdb(soundList):
    return map(changeDb,soundList)

def save(sound,filename):
    sound.export(filename,format="mp3")


if __name__=="__main__":
    filepath=r"E:\BaiduNetdiskDownload\逼哥牛逼\专辑系列\专辑系列\108 个关键词 2012 Live\阿兰.mp3"
    sound=AudioSegment.from_mp3(filepath)

    save(changeDb(sound),'test2.mp3')





