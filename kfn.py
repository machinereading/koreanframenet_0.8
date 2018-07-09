import json
import pprint
from nltk.corpus import framenet as fn
import os
import re

def load_kfn():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    #print(type(dir_path))
    with open(dir_path+'/resource/KFN_lus.json','r') as f:
        kolus = json.load(f)
    with open(dir_path+'/resource/KFN_annotations.json','r') as f:
        annos = json.load(f)
    with open(dir_path+'/resource/KFN_annotations_from_sejong.json','r') as f:
        s_annos = json.load(f)
    return kolus,annos,s_annos

kolus,annos,s_annos = load_kfn()

def lus():
    return kolus

def get_lu_id(lexicalUnit,frame):
    # get lu id from lu(entry) and frame
    lu_id = False
    for i in kolus:
        if lexicalUnit == i['lu'] and frame == i['frameName']:
            lu_id = i['lu_id']
            break
    return lu_id

def lus_by_lemma(lemma):
    lu_id = False
    lu_list = []
    for i in kolus:
        pos = i['lu'].split('.')[1]
        lexeme = i['lexeme'] + '.' + pos
        if lemma == lexeme: #only matching with lexeme
            lu = i['lu']
            lu_list.append(lu)
#    if len(lu_list) == 0:
#        for i in kolus:
#            if lemma in i['lu']:
#                d = {}
#                d['lu_id'] = i['lu_id']
#                d['lu'] = i['lu']
#                lu_list.append(d)
    return lu_list

def lus_by_lu(lemma):
    result = []
    for i in kolus:
        lexu = i['lu'].split('.')[0] + '.' + i['lu'].split('.')[1]
        if lemma == lexu:
            result.append(i)
    return result


def lus_by_surfaceform(surfaceform):
    lu_id = False
    lu_list = []
    for i in kolus:
        if surfaceform in i['surface_forms']:
            lu = i['lu']
            lu_list.append(lu)
    return lu_list

def lu(lu_id):
    # get lu information using lu_id
    lexicalUnit = False
    for i in kolus:
        if lu_id == i['lu_id']:
            lexicalUnit = i
            break
    return lexicalUnit

def annotations_by_lu(lu_id):
    result = []
    lexicalUnit = lu(lu_id)
    ko_annotation = lexicalUnit['ko_annotation_id']
    sejong_annotation = lexicalUnit['sejong_annotation_id']
    result = ko_annotation + sejong_annotation
    return result

def annotation(lu_id):
    aids = annotations_by_lu(lu_id)
    result = []
    for i in aids:
        if type(i) == str:
            for s_anno in s_annos:
                for k in s_anno['annotations']:
                    if i == k['ko_annotation_id']:
                        for d in k['denotations']:
                            if d['span']['begin'] != -1:
                                result.append(k)
        elif type(i) == int:
            for anno in annos:
                for k in anno['frameAnnotation']['ko_annotations']:
                    if i == k['ko_annotation_id']:
                        k['text'] = anno['text']['ko_text']
                        result.append(k)
        else:
            pass
    return result

def surface_to_lu_id(surface, frame):
#    spc = ['\,','.','!','?']
#    if len(surface) >1:
#        if surface[-1] in spc:
#            surface = re.sub('[,.?!]','',surface)
    result = []
    for i in kolus:
        if frame == i['frameName']:
            if surface in i['surface_forms']:
                result.append(i['lu_id'])
    result = list(set(result))
    ds = []
    for i in result:
        lu_info = lu(i)
        p = lu_info['lu'].split('.')[1]
        n = len(lu_info['ko_annotation_id'])
        d = (i, p, n)
        ds.append(d)
    if len(ds) > 0:
        luid = ds[0]
        for i in ds:
            if i[1] == 'v':
                luid = i
        for i in ds:
            if luid[1] == 'v':
                if i[1] == 'v':
                    if i[2] > luid[2]:
                        luid = i
                    else:
                        pass
                else:
                    pass
            else:
                if i[2] > luid[2]:
                    luid = i
    else:
        luid = False
    return luid[0]
