import urllib.request
from urllib.parse import urlencode
import json
#from src import etri2conll

def getETRI(text):
    url = "http://143.248.135.20:31235/etri_parser"
    contents = {}
    contents['text'] = text
    contents = json.dumps(contents).encode('utf-8')
    u = urllib.request.Request(url, contents)
    response = urllib.request.urlopen(u)
    result = response.read().decode('utf-8')
    result = json.loads(result)
    return result

def lemmatizer(word, pos):
    etri = getETRI(word)
    lemmas = etri[0]['WSD']
    lemma = word
    for i in lemmas:
        p = i['type']
        if pos == 'v' or pos == 'VV':
            if p == 'VV':
                lemma = i['text']
                break
        elif pos == 'n' or pos == 'NN' or pos == 'NNG' or pos == 'NNP' or pos =='NNB' or pos =='NR' or pos == 'NP':
            if 'NN' in p:
                lemma = i['text']
                break
        elif pos == 'adj' or pos == 'VA':
            if p == 'VA':
                lemma = i['text']
                break
        else:
            pass
    return lemma
def getPOS(word):
    etri = getETRI(word)
    pos = etri[0]['WSD'][0]['type']
    if pos.startswith('N'):
        pos = 'n'
    elif pos == 'VV':
        pos = 'v'
    elif pos == 'VA':
        pos = 'adj'
    else:
        pos == 'n'
    return pos

#def getETRI_CoNLL2006(text):
#    nlp = getETRI(text)
#    result = etri2conll.etri2conll2006(nlp)
#    return result

