import json
from nltk.corpus import framenet as fn

def load_kfn():
    with open('./resource/KFN_lus.json','r') as f:
        lus = json.load(f)
    return lus

lus = load_kfn()

def get_lu_id(lu,frame):
    # get lu id from lu(entry) and frame
    lu_id = False
    for i in lus:
        if lu == i['lu'] and frame == i['frameName']:
            lu_id = i['lu_id']
            break
    return lu_id

def get_lu_by_id(lu_id):
    # get lu information by lu_id
    lu = False
    for i in lus:
        if lu_id == i['lu_id']:
            lu = i
            break
    return lu

def lus_by_lemma(lemma):
    lu_id = False
    lu_list = []
    for i in lus:
        if lemma == i['lexeme']: #only matching with lexeme
            lu_id = i['lu_id']
            lu = get_lu_by_id(lu_id)
            lu_list.append(lu)
    return lu_list



