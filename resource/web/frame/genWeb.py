import json
import glob
import pprint
from xml.etree.ElementTree import Element, dump, parse, ElementTree

def get_lu_id(lu):
    with open('/disk_4/framenet/resource/KFN_lus.json','r') as f:
        d = json.load(f)
    for i in d:
        if lu == i['lu']:
            lu_id = i['lu_id']
    return lu_id

def gen_frame_index():
#    files = glob.glob('../resource/web/frame/*.xml')

    with open('/disk_4/framenet/resource/KFN_frame_lu_pair.json','r') as f:

        d = json.load(f)
    cDate = '24/04/2018 09:00:00 KST Web'
    cBy = 'hahm'
    status = 'Created'
    for i in d:
        filename = i['frame']+'.xml'
        tree = parse(filename)
        note = tree.getroot()
        for j in i['ko_lu']:
            lu_id = get_lu_id(j)
            lu_id = 'ko.'+str(lu_id)
            lu = j

            lexUnit = Element('lexUnit')
            lexUnit.attrib['name'] = lu
            lexUnit.attrib['ID'] = lu_id
            lexUnit.attrib['cDate'] = cDate
            lexUnit.attrib['cBy'] = cBy
            lexUnit.attrib['status'] = status
            note.append(lexUnit)



        ElementTree(tree).write(filename)


        print(i['frame'])
        break


    

#gen_lu_files()
#gen_lu_index()

gen_frame_index()
