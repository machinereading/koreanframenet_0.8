import json
import glob
import pprint

def load_data():
    with open('../resource/KFN_lus.json','r') as f:
        kolus = json.load(f)
    with open('../resource/KFN_annotations.json','r') as f:
        annos = json.load(f)

    return kolus,annos

kolus,annos = load_data()

def gen_lu_files():
    n = 0
    for lu in kolus:
        filename = str(lu['lu_id'])+'.json'
        d = {}
        d['ko_pos'] = lu['pos']
        d['ko_lu'] = lu['lu']
        d['frameID'] = lu['fid']
        d['frameName'] = lu['frameName']
        d['en_lus'] = lu['en_lu']
        d['lu_id'] = lu['lu_id']
        patterns = []
        aids = lu['ko_annotation_id']
        annotation = []
        for aid in aids:
            for anno in annos:
                text = anno['text']['ko_text']
                kos = anno['frameAnnotation']['ko_annotations']
                for ko in kos:
                    if aid == ko['ko_annotation_id']:
                        pat = {}
                        pat['valenceText'] = 'annotation id: '+str(aid)
                        exam = ko
                        exam['text'] = text
                        examples = []
                        examples.append(exam)
                        pat['examples'] = examples
                        patterns.append(pat)

        d['patterns'] = patterns
        with open('../resource/web/kolu/'+filename,'w') as f:
            json.dump(d,f,indent=4,ensure_ascii=False)
            print(filename,'is written')

def gen_lu_index():
    files = glob.glob('../resource/web/kolu/*.json')
    lu_files = []
    for i in files:
        if 'index.json' in i:
            pass
        else:
            lu_files.append(i)

    indices = []
    for i in lu_files:
        filename =  str(i)+'.json'
        with open(i, 'r') as f:
            data = json.load(f)
        kolu = data['ko_lu']

        if data['ko_lu'].startswith('('):
            kolu = kolu.split(')')[-1]
        else:
            pass
        if kolu.startswith(' '):
            kolu = kolu[1:]
        indices.append({'lu':kolu, 'pos':data['ko_pos'], 'id':data['lu_id']})

    indices = sorted(indices,key=lambda x: x['lu'])
    with open('../resource/web/kolu/index.json', 'w') as f:
        json.dump(indices,f,indent=4,ensure_ascii=False)
        print('index.json is written')
    print(len(indices), 'is indexed')

gen_lu_files()
gen_lu_index()


