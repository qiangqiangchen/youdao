# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter



def cixingTransition(sent):
    if "." not in sent:
        return sent
    cixing=sent.split(".")[0]
    if cixing=='n':
        return sent.replace(cixing,"作为名词有")+"，的意思"
    elif cixing=="pron":
        return sent.replace(cixing, "作为代词有")+"，的意思"
    elif cixing=="adj":
        return sent.replace(cixing, "作为形容有")+"，的意思"
    elif cixing=="num":
        return sent.replace(cixing, "作为数词有")+"，的意思"
    elif cixing=="v":
        return sent.replace(cixing, "作为动词有")+"，的意思"
    elif cixing=="adv":
        return sent.replace(cixing, "作为副词有")+"，的意思"
    elif cixing=="art":
        return sent.replace(cixing, "作为冠词有")+"，的意思"
    elif cixing=="prep":
        return sent.replace(cixing, "作为介词有")+"，的意思"
    elif cixing=="conj":
        return sent.replace(cixing, "作为连词有")+"，的意思"
    elif cixing=="int":
        return sent.replace(cixing, "作为感叹词有")+"，的意思"
    elif cixing=="vt":
        return sent.replace(cixing, "作为及物动词有")+"，的意思"
    elif cixing=="vi":
        return sent.replace(cixing, "作为不及物动词有")+"，的意思"






def getHtml(url):
    session=requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))
    rep=session.get(url)
    if rep.status_code==200:
        return rep
    return None

def getfayin(url,filename):
    res=getHtml(url)
    with open(filename,'wb') as f:
        f.write(res.content)

def pageOpear(word):
    result={}
    voice_base_url = 'http://dict.youdao.com/dictvoice?audio='
    base_url='http://dict.youdao.com/w/'
    response=getHtml(base_url+word)
    if not response:
        pass
    soup = BeautifulSoup(response.text, features="html.parser")

    #音标和发音
    phonetic=soup.find_all(name="span", attrs={"class":"pronounce"})
    phonetic_USA=phonetic[-1].span.get_text()
    voice_path=phonetic[-1].a['data-rel']

    result["phonetic_USA"] = phonetic_USA
    result['voice_path']=voice_base_url+voice_path

    #释义
    trans_container=soup.find(name="div",attrs={"class":"trans-container"}).ul.find_all('li')
    trans_str=[]
    for trans in trans_container:
        trans_str.append(trans.get_text())
    result["trans_str"]=list(map(cixingTransition,trans_str))

    #短语
    try:
        wordGroup=soup.find(name="div",attrs={"id":"wordGroup"}).find_all('p')
        wordGroup_str=""
        for wordG in wordGroup:
            # print(wordG.span.a.get_text())
            wordGroup_str+=(wordG.get_text("\t",strip=True)+"\n")

        result["wordGroup_str"]=wordGroup_str
    except:
        result["wordGroup_str"]=""


    #双语例句
    try:
        bilingual=soup.find(name="div",attrs={"id":"bilingual"}).ul.find_all('li')
        examples=[]
        for sent in bilingual:
            example_dict={}
            sent_info=sent.find_all('p')
            example=sent_info[0].get_text().strip()
            fanyi=sent_info[1].get_text().strip()
            sent_voice=sent_info[0].a["data-rel"]
            example_dict['example']=example
            example_dict['fanyi']=fanyi
            example_dict['sent_voice']=voice_base_url+sent_voice
            examples.append(example_dict)

        result['examples']=examples
    except:
        result['examples']=""

    return result








if __name__=='__main__':
    r=pageOpear('sing')
    with open('test.txt', 'w',encoding='utf-8') as f:
        for i in r.values():
            f.write(str(i))





