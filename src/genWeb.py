import json
import glob
import pprint
#from xml.etree.ElementTree import Element, dump, parse, ElementTree
import lxml.etree

def load_data():
    with open('../resource/KFN_lus.json','r') as f:
        kolus = json.load(f)
    with open('../resource/KFN_annotations.json','r') as f:
        annos = json.load(f)
    with open('../resource/KFN_annotations_from_sejong.json','r') as f:
        sejong_annos = json.load(f)

    return kolus,annos,sejong_annos

kolus,annos,sejong_annos = load_data()

def get_sejong_annos(sid):
    for i in sejong_annos:
        for j in i['annotations']:
            if sid == j['ko_annotation_id']:
                result = j
    return result


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
        sids = lu['sejong_annotation_id']
        if len(sids) > 0:
            for sid in sids:
                s_anno = get_sejong_annos(sid)
                pat = {}
                pat['valenceText'] = 'annotation id: '+str(sid)
                exam = s_anno
                exam['frameName'] = lu['frameName']
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

def get_lu_id(lu):
    with open('../resource/KFN_lus.json','r') as f:
        d = json.load(f)
    for i in d:
        if lu == i['lu']:
            lu_id = i['lu_id']
            break
    return lu_id

def gen_frame_index():
#    files = glob.glob('../resource/web/frame/*.xml')

    with open('../resource/KFN_frame_lu_pair.json','r') as f:
        d = json.load(f)
    cDate = '24/04/2018 09:00:00 KST Web'
    cBy = 'hahm'
    status = 'Created'
    for i in d:
        filename = '../resource/web/frame/'+i['frame']+'.xml'
        tree = lxml.etree.parse(filename)
        note = tree.getroot()
        xsl = note.getprevious()
#        note = parse(filename)
#        print(xsl)
        for j in i['ko_lu']:
            lu_id = get_lu_id(j)
            lu_id = 'ko.'+str(lu_id)
            lu = j

            lexUnit = lxml.etree.Element('lexUnit')
            lexUnit.attrib['name'] = lu
            lexUnit.attrib['ID'] = lu_id
            lexUnit.attrib['cDate'] = cDate
            lexUnit.attrib['cBy'] = cBy
            lexUnit.attrib['status'] = status
            note.append(lexUnit)



        tree.write(filename, xml_declaration=True,encoding='utf-8',method='xml', pretty_print=True)

        print(i['frame'])


def gen_lu_xml():
    with open('../resource/KFN_lus.json','r') as f:
        lus = json.load(f)
    with open('../resource/sejongset.json','r') as f:
        sejongs = json.load(f)

    for i in lus:
        name = i['lu']
        frame = i['frameName']
        lu_id = i['lu_id']

        filename = '../resource/web/lu/luko.'+str(lu_id)+'.xml'
        i = "http://www.w3.org/2001/XMLSchema-instance"
        root = lxml.etree.Element("lexUnit", nsmap={'xsi':i})
        root.attrib['name'] = name
        root.attrib['ID'] = str(lu_id)
        root.attrib['frame'] = frame
        root.attrib[lxml.etree.QName(i,'schemaLocation')] = "../schema/lexUnit.xsd"
        root.attrib['xmlns'] = "http://framenet.icsi.berkeley.edu"

        root.addprevious(lxml.etree.PI('xml-stylesheet','type="text/xsl" href="lexUnit.xsl"'))

        doc = lxml.etree.ElementTree(root)
        print(name,lu_id)
            
        doc.write(filename,pretty_print=True,xml_declaration=True,encoding='utf-8', method='xml')



    

gen_lu_files()
print(1)
gen_lu_index()
print(2)
gen_frame_index()
print(3)
gen_lu_xml()
print(4)
