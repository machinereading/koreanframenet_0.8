import json
import pprint
def get_sejong(sid):
    with open('../resource/sejongset.json','r') as f:
        sejong = json.load(f)
    for i in sejong:
        if sid == i['sejongset']:
            result = i 
    return result

def gen_annotations_from_sejong():
    with open('../resource/sejongset.json','r') as f:
        sejong = json.load(f)

    sid = 1
    result = []
    for i in sejong:
        pos = i['pos']
        print(sid, i['sejongset'])
        if pos == 'n':
            sd = {}
            sd['sejongset'] = i['sejongset']
            annos = []
            for exam in i['examples']:
                if exam:
                    print(exam)
                    sent = exam.replace('~',i['word'])
                    s = sent.find(i['word'])
                    e = s+len(i['word'])

                    d = {}
                    d['text'] = sent
                    d['relations'] = []
                    d['ko_annotation_id'] = 'sejong.'+str(sid)
                    d['target'] = sent[s:e]
                    denos = []
                    deno = {}
                    span = {}
                    span['begin'] = s
                    span['end'] = e
#                    span['id'] = "1"
#                    span['obj'] = "target"
                    deno['span'] = span
                    deno['obj'] = "target"
                    deno['id'] = "1"
                    denos.append(deno)
                    d['denotations'] = denos
                    annos.append(d)
                    sid = sid+1
                    print(d)
            sd['annotations'] = annos
            result.append(sd)

        elif pos == 'v' or pos == 'a':
            sd = {}
            sd['sejongset'] = i['sejongset']
            annos = []
            if len(i['word']) > 2:
                w = i['word'][:2]
            elif len(i['word']) == 2:
                w = i['word'][:1]
            else:
                pass
#            print(w)

            for exam in i['examples']:
                if exam:
                    sent = exam
                    print(sent)
                    s = sent.find(w)

                    e = s
                    et = sent[s]

                    rec = True
                    while rec == True:
                        et = sent[e]
                        if et == ' ' or et == '.' or e == len(sent)-1:
                            rec=False
                        e = e+1
                    e = e-1
                    d = {}
                    d['text'] = sent
                    d['relations'] = []
                    d['ko_annotation_id'] = 'sejong.'+str(sid)
                    d['target'] = sent[s:e]
                    denos = []
                    deno = {}
                    span = {}
                    span['begin'] = s 
                    span['end'] = e 
#                    span['id'] = "1"
#                    span['obj'] = "target"
                    deno['span'] = span
                    deno['id'] = "1"
                    deno['obj'] = "target"
                    denos.append(deno)
                    d['denotations'] = denos
                    annos.append(d)
                    sid = sid+1
                    print(d)
            sd['annotations'] = annos
            result.append(sd)

        else:
            pass
        print(sid)
    with open('../resource/KFN_annotations_from_sejong.json','w') as f:
        json.dump(result,f,indent=4,ensure_ascii=False)



gen_annotations_from_sejong()


def get_annotations_from_sejong():
    with open('../resource/KFN_lus.json','r') as f:
        lus = json.load(f)

    for i in lus:
        sid = i['mapSejong']
        if s != False:
            s = get_sejong(sid)



