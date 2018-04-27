import json

def corpus():
    with open('./resource/KFN_annotations.json','r') as f:
        corpus = json.load(f)
    text = []
    for i in corpus:
        text.append(i['text']['origin_lang'])

    e,j = 0,0
    n = 0
    for i in text:
        if i == 'en':
            e = e+1
        else:
            j = j+1
        n = n+1
    print(e,j)
    print(n)

#corpus()
def load_manual():
    with open('./resource/added_kolus.csv','r') as f:
        d = f.readlines()
    n = 0
    lus = []
    for i in range(3656):
        first = n
        second = n+1
        third = n+2
        first_line = d[first].split('\t')
        second_line = d[second].split('\t')
        third_line = d[third].split('\t')
        frame = first_line[0]
        enlu = second_line[0]
        c = 0
        correct = []
        for j in third_line:
            if j == 'O' or j == 'A':
                correct.append(c)
            c = c+1
        for r in correct:
            ko = second_line[r]
            lu = {}
            lu['frame'] = frame
            lu['en_lu'] = enlu
            dum = ko.split('.')
            if dum[-1] != 'v':
                if ko != '':
                    if dum[0][-1] != '다' and len(dum) == 2:
                        ko = dum[0][:-1]+'.'+dum[0][-1]+'.'+dum[1]
                    else:
                        if dum[-1] == '':
                            ko = dum[0]+'.v.'+frame
                    lu['lu'] = ko
                    lus.append(lu['lu'])
            else:
                if ko != '':
                    lu['lu'] = dum[0]+'다'+'.v.'+frame
                    lus.append(lu['lu'])

        n = n+4
#    result = []
    print(len(list(set(lus))))

load_manual()

def statistics():
    with open('./resource/KFN_lus.json','r') as f:
        lus = json.load(f)
    from_c = []
    from_s = []
    from_e = []
    all_lu = []

    for i in lus:
        pos = i['lu'].split('.')[1]
        if len(i['ko_annotation_id']) > 0:
            from_c.append(pos)
        elif type(i['mapSejong']) == str:
            from_s.append(pos)
        else:
            from_e.append(pos)

        all_lu.append(pos)

    print('코퍼스에서 온것 전체:',len(all_lu))
    n,v,a,error = 0,0,0,0
    for i in all_lu:
        if i == "n":
            n = n+1
        elif i == "v":
            v = v+1
        elif i == "a":
            a = a+1
        else:
            error = error+1
    print(n,v,a,error)

    n,v,a,error = 0,0,0,0
    for i in from_c:
        if i == "n":
            n = n+1
        elif i == "v":
            v = v+1
        elif i == "a":
            a = a+1
        else:
            error = error+1
    print(n,v,a,error, len(from_c))

    n,v,a,error = 0,0,0,0
    for i in from_s:
        if i == "n":
            n = n+1
        elif i == "v":
            v = v+1
        elif i == "a":
            a = a+1
        else:
            error = error+1
    print(n,v,a,error, len(from_s))

def frame_stat():
    with open('./resource/KFN_frame_lu_pair.json','r') as f:
        d = json.load(f)
    n = 0
    for i in d:
        if len(i['ko_lu']) >0:
            n = n+1
    print(n)

def anno_stat():
    with open('./resource/KFN_annotations.json','r') as f:
        annos = json.load(f)
    with open('./resource/KFN_annotations_from_sejong.json','r') as f:
        sejongs = json.load(f)

    n = 0
    for i in annos:
        a = i['frameAnnotation']['ko_annotations']
        n = n+ len(a)
    print(n)

    with open('./resource/KFN_lus.json','r') as f:
        lus = json.load(f)
    r = []
    for i in lus:
        r = list(set(r+i['sejong_annotation_id']))

    n = 0
    for i in sejongs:
        for j in i['annotations']:
#            print(i['sejongset'])
#            print(j)
            if j['ko_annotation_id'] in r:
                n = n+len(a)
    print(n)


def lu_frame_stat():
    with open('./resource/KFN_lus.json','r') as f:
        d = json.load(f)
    n = 0
    for i in d:
        a = i['ko_annotation_id']
        s = i['sejong_annotation_id']
        if len(a) > 0 or len(s) > 0:
            n = n+1
    print(n)
#statistics()
#frame_stat()
#anno_stat()
#lu_frame_stat()
