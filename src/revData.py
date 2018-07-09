import json

#갔다오다.v --> 가다.v (180709)
def day180709():
    with open('../resource/KFN_lus.json.bak','r') as f:
        d = json.load(f)

    new_lu = []
    for i in d:
        if i['lu_id'] == 2542:
            lu = i
            pass
        else:
            new_lu.append(i)
    for i in new_lu:
        if i['lu_id'] == 1054:
            ko_annotation_id = i['ko_annotation_id'] + lu['ko_annotation_id']
            i['ko_annotation_id'] = list(set(ko_annotation_id))
            fe_list = i['fe_list'] + lu['fe_list']
            i['fe_list'] = list(set(fe_list))
            en_lu = i['en_lu'] + lu['en_lu']
            i['en_lu'] = list(set(en_lu))
            surface_forms = i['surface_forms'] + lu['surface_forms']
            i['surface_forms'] = list(set(surface_forms))
    with open('../resource/KFN_lus.json','w') as f:
        json.dump(new_lu, f, ensure_ascii=False, indent=4)

    files = ['../data/training.tsv', '../data/dev.tsv', '../data/test.tsv']
    for fname in files:
        with open(fname,'r') as f:
            d = f.readlines()
        with open(fname,'w') as f:
            for i in d:
                i =  i.replace('갔다오다.v', '가다.v')
                f.write(i)

#day180709()




