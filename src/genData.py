import json
from fuzzywuzzy import fuzz
import etri
import pickle
from collections import OrderedDict

#load data
def load_data():
    with open('../resource/sejongset.json','r') as f:
        sejongset = json.load(f)
    with open('../resource/kolu_from_annotations.json','r') as f:
        kolu_anno = json.load(f)

    return sejongset, kolu_anno

sejongset, kolu_anno = load_data()

#similarity
def get_sim_score(word_1,word_2):
    sim_score = fuzz.ratio(word_1, word_2)*0.01
    return sim_score

def check_first_two_overlab(word_1,word_2):
    result = False
    w1_list = word_1.split(' ')
    if len(w1_list) == 1:
        if len(word_1) >1 and len(word_2) >1:
            if word_1[:2] == word_2[:2]:
                result = True
        #elif len(word_1) ==1 and len(word_2) == 1:
        else:
            if word_1[0] == word_2[0]:
                result = True
#        else:
#            pass 
    else:
        if len(w1_list[0]) >1 and len(word_2) >1:
            if w1_list[0][:2] == word_2[:2]:
                result = True
        elif len(w1_list[0]) == 1 and len(word_2) == 1:
            if w1_list[0][0] == word_2[0]:
                result = True
        else:
            pass

        if len(w1_list[1]) >1 and len(word_2) >1:
            if w1_list[1][:2] == word_2[:2]:
                result = True
        elif len(w1_list[1]) == 1 and len(word_2) == 1:
            if w1_list[1][0] == word_2[0]:
                result = True
        else:
            pass



    return result

def check_sim(word_1,word_2):
    sim_score = get_sim_score(word_1,word_2)
#    sim_score = fuzz.partial_ratio(word_1, word_2)*0.01
    two_overlab = check_first_two_overlab(word_1,word_2)

    if sim_score >= 0.2:
        if two_overlab == True:
            result = True
        else:
            result = False
    else:
        result = False

    return result,sim_score

def get_lemma(word,pos):
    lemma = word
    if pos == 'VV+ETM':
        if word[-1] == '하' or word[-1] == '되':
            lemma = word
        else:
            word1 = word+' 것이다'
            pos1 = pos.split('+')[0]
            lemma = etri.lemmatizer(word1,'VV')
            ll = lemma.split(' ')
            if len(ll) > 1:
                lemma = etri.lemmatizer(word1,'VA')

            ll = lemma.split(' ')
            if len(ll) > 1:
                lemma = word

#            lemma = word
#                print(lemma)
                
#            else:
#                lemma = word
    elif pos == 'NNG+JKO+VV+ETM':
        if word[-1] == '하' or word[-1] == '되':
            lemma = word
        else:
            word1 = word+' 것이다'
            pos1 = pos.split('+')[0]
            lemma = word
#            if pos1 == 'VV':
#                lemma = etri.lemmatizer(word1,pos1)
#                print(lemma)
#            else:
#                lemma = word

    else:
        pos1 = pos.split('+')[0]
        if pos1 == 'VV':
            lemma = etri.lemmatizer(word,pos1)

#    elif pos1 != 'VV' and pos2 == 'VV':
#        word = word+'다'
#        lemma = etri.lemmatizer(word,pos2)
        else:
            lemma = word
#    print(lemma)
    return lemma

def get_entry(lu,p):
    w1 = get_lemma(lu,p)
#    print(w1)
    kolu = w1
    pos = p
    final_pos = pos
    pos_list = pos.split('+')
    max_sim = -1.0
    best_entry = False
    check = False

#    print(kolu)

    tokens = w1.split(' ')
    for sejong in sejongset:
        w2 = sejong['word']
        entry = sejong['word']
        w2_lemma = sejong['lemma']
        w2_pos = sejong['pos']
        if len(tokens) == 1:
#            w2 = sejong['lemma']
            if 'NN' in pos_list[0]: #1개 단어이면서 명사인 경우- exact matching
                if w1[-1] == '들':
                    if w1 == '우리들':
                        pass
                    elif len(w1) < 3:
                        pass
                    else:
                        w1 = w1[:-1]
                    print(w1)
                if w1 == w2 and w2_pos == 'n':
                    best_entry = entry
                    check = True
                    max_sim = 1
                    kolu = w1
#                    print(best_entry)
            elif 'VV' in pos or 'VA' in pos: #1개 단어이면서 명사아닌경우
                w1_e = w1+'다'
#                print(w1_e)
                if w1_e == w2 and w2_pos != 'n':
                    best_entry = entry
                    check = True
                    max_sim = 1
                    if w2_pos == 'v':
                        final_pos = 'VV'
                    else:
                        final_pos = 'VA'
                    kolu = w2_lemma
                else:
                    if '하' in entry:
                        sim,score = check_sim(w1,w2_lemma)
                    else:
                        sim,score = check_sim(w1,w2)
                    if sim == True:
                        if score >= max_sim:
                            max_sim = score
                            best_entry = entry
                            check = True
                            if 'VV' in pos:
                                if '하' in entry:
                                    kolu = w2_lemma
                                else:
                                    kolu = w1
                            else:
                                kolu = w2_lemma
                            if w2_pos == 'v':
                                final_pos = 'VV'
                            elif w2_pos == 'adj':
                                final_pos = 'VA'
                            elif w2_pos == 'n':
                                final_pos = pos_list[0]
                            else:
                                pass

            else:
                if '하' in entry:
                    sim,score = check_sim(w1,w2_lemma)
                else:
                    sim,score = check_sim(w1,w2)
                if sim == True:
                    if score >= max_sim:
                        max_sim = score
                        best_entry = entry
                        check = True
                        kolu = w1
                        if w2_pos == 'v':
                            final_pos = 'VV'
                        elif w2_pos == 'adj':
                            final_pos = 'VA'
                        elif w2_pos == 'n':
                            final_pos = pos_list[0]
                        else:
                            pass


        else: #2개 이상 어휘
#            print(w1)
            if '하' in entry:
                sim,score = check_sim(w1,w2_lemma)
            else:
                sim,score = check_sim(w1,w2)
            if sim == True:
                if score >= max_sim:
                    max_sim = score
                    best_entry = entry
                    check = True
                    if w2_pos == 'v':
                        kolu = w1
                        final_pos = 'VV'
                    elif w2_pos == 'adj':
                        final_pos = 'VA'
                        kolu = w2_lemma
                    elif w2_pos == 'n':
                        final_pos = pos_list[0]
                        kolu = best_entry
                    else:
                        pass
                

    if best_entry:
        pass
    else:
        best_entry = kolu


#    print(kolu,best_entry, final_pos,check, max_sim)
    return kolu,best_entry,final_pos

#lu,p = '가','VV'
#e = get_entry(lu,p)
#print(e)

#gen ENTRY
def gen_entry():
    print(len(kolu_anno))
    result = []
    n = 0
    lu_id = 1
    for kolu in kolu_anno:
        lu = {}
        word = kolu['lemma']
        pos = kolu['pos']
        best_entry = False
        lemma,entry,pos = get_entry(word,pos)
        print(lu_id,entry,lemma,pos)

        new = True
        for i in result:
            try:
                if entry == i['lu'] and kolu['fid'] == i['fid'] and kolu['pos'] == i['pos']:
                    ko_annotation_id = i['ko_annotation_id']
                    ko_annotation_id = ko_annotation_id + kolu['ko_annotation_id']
                    ko_annotation_id = list(set(ko_annotation_id))
                    lemma = i['lemma_var']
                    lemma.append(kolu['lemma'])
                    lemma = list(set(lemma))
                    enlu = i['en_lu']
                    enlu = enlu + kolu['en_lu']
                    enlu = list(set(enlu))
                    i['ko_annotation_id'] = ko_annotation_id
                    i['lemma_var'] = lemma
                    i['en_lu'] = enlu
                    new = False
#                    print(i)
                    break
                else:
                    pass
            except KeyboardInterrupt:
                raise
        if new:
            lemmas = []
            lemmas.append(lemma)
            lu['lemma_var'] = lemmas
            lu['frameName'] = kolu['frameName']
            lu['lu_id'] = lu_id
            lu_id = lu_id +1
            lu['fid'] = kolu['fid']
            lu['ko_annotation_id'] = kolu['ko_annotation_id']
            lu['pos'] = pos
            lu['en_lu'] = kolu['en_lu']
            lu['lu'] = entry
            result.append(lu)

#            print(lu)


    with open('./KFN_lus_v1.json','w') as f:
        json.dump(result,f,indent=4,ensure_ascii=False)



    print(len(result)/len(kolu_anno))

#gen_entry() 

def get_fid(frame):
    with open('../resource/FN17_frame_id.json','r') as f:
        d = json.load(f)

    for i in d:
        if frame == i['frame']:
            fid = i['id']

    return fid

def load_manual():
    with open('../resource/added_kolus.csv','r') as f:
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
            if j == 'O':# or j == 'A':
                correct.append(c)
            c = c+1
        for r in correct:
            ko = second_line[r]
            lu = {}
            lu['frame'] = frame
            lu['en_lu'] = enlu
            dum = ko.split('.')
            if dum[-1] != 'v':
                pass
#                print(frame,enlu,ko)
#                if ko != '':
#                    if dum[0][-1] != '다' and len(dum) == 2:
#                        ko = dum[0][:-1]+'.'+dum[0][-1]+'.'+dum[1]
#                    else:
#                        if dum[-1] == '':
#                            ko = dum[0]+'.v'
#                    lu['lu'] = ko
#                    lus.append(lu)
            else:
                if ko != '':
                    lu['lu'] = dum[0]+'다'+'.v'
                    lus.append(lu)

        n = n+4

    return lus

def rev_kolu():

    with open('./KFN_lus_v1.json','r') as f:
        kfn2 = json.load(f)

    for i in kfn2:
#        print(i)
        lu_old = i['lu']
        lu_old_list = lu_old.split(' ')
        pos = i['pos']
        pos_list = pos.split('+')
        i['mapSejong'] = False
        i['lexeme'] = False
        i['publish'] = False

        insejong = False
        if len(pos_list) == 1 and len(lu_old_list) == 1:
            if 'NN' in pos or pos == 'VV' or pos == 'VA':
                if pos == 'VV' or pos == 'VA':
                    for sejong in sejongset:
                        if sejong['pos'] == 'v' or sejong['pos'] == 'adj':
                            if lu_old == sejong['word']:
                                insejong = True
                                lexeme = sejong['lemma']
                                if len(sejong['lemma']) == 1:
                                    lexeme = sejong['word'][:-1]
                                else:
                                    lexeme = sejong['lemma']
                                break
                    if insejong:
                        #do something
                        if pos == 'VV':
                            new_pos = 'v'
                        else:
                            new_pos = 'a'
                        lu = lu_old+'.'+new_pos
                        i['lu'] = lu
                        i['lexeme'] = lexeme
                        i['publish'] = True
                else:
                    #do something
                    new_pos = 'n'
                    lu = lu_old+'.'+new_pos
                    i['lu'] = lu
                    i['lexeme'] = lu_old
                    i['publish'] = True
    print(kfn2[0])

    with open('./KFN_lus_v2.json','w') as f:
        json.dump(kfn2,f,indent=4,ensure_ascii=False)

#rev_kolu()


def rev_kolu2():
    #중복된걸 합치기 위함!
    with open('./KFN_lus_v2.json.','r') as f:
        d = json.load(f)
    result = []
    n = 0
    for i in d:
        if n == 0:
            result.append(i)
            n = n+1
        else:
            new = True
            for j in result:
#                print(j)
                if i['lu'] == j['lu']:
#                    print('1')
                    if i['pos'] == j['pos']:
#                        print('2')
                        if i['frameName'] == j['frameName']:
#                            print('3')
                            ko_annotation_id = j['ko_annotation_id']
                            ko_annotation_id = ko_annotation_id + i['ko_annotation_id']
                            j['ko_annotation_id'] = list(set(ko_annotation_id))
    
                            en_lu = j['en_lu']
                            en_lu = en_lu + list(set(i['en_lu']))
                            j['en_lu'] = en_lu

                            lemma_var = j['lemma_var']
                            lemma_var = lemma_var + i['lemma_var']
                            j['lemma_var'] = list(set(lemma_var))
                            new = False
                            print('merged',i['lu_id'])
                            break
                else:
                    pass
            if new:
                result.append(i)
            n = n+1
    with open('./KFN_lus_v3.json','w') as f:
        json.dump(result,f,indent=4,ensure_ascii=False)



def get_from_manual():

    with open('./KFN_lus_v3.json','r') as f:
        kfn2 = json.load(f)
    lus = load_manual()
    n = 0
    for i in lus:
        lu_json = {}
        s = False
        frame = i['frame']
        en_lu = []
        en_lu.append(i['en_lu'])
        lu_old = i['lu'].split('.')
        if lu_old[-1] == 'v':
#            print(lu_old[0])
            if lu_old[0][-1] != '다':
                lu = lu_old[0]+'다.v'
            else:
                lu = lu_old[0]+'.v'
            lexeme = lu_old[0]
        else:
            lu = lu_old[0]+'.v'
#            print(lu_old)
            if len(lu_old) >1 and lu_old[-1] != '' and lu_old[-1] != ' ':
                s = lu_old[0]+'.v.'+lu_old[1]+'.'+lu_old[2]
            else:
                s = False

#        print(lu,s)

        new = True

        for j in kfn2:
#            print(lu)
#            print(j)
            pos_i = lu.split('.')[-1]
            pos_j = j['lu'].split('.')[-1]
            if lu == j['lu'] and frame == j['frameName'] and pos_i and pos_j:
                new = False
                if s:
                    j['mapSejong'] = s
#                    print(j)
        
        if new:
            if s:
                lu_json['lu'] = lu
                lemma_var = []
                lu_json['lemma_var'] = lemma_var
                lu_json['lexeme'] = lu_old[0]
                lu_json['frameName'] = frame
                lu_json['lu_id'] = 0
                lu_json['fid'] = get_fid(frame)
                lu_json['ko_annotation_id'] = []
                lu_json['pos'] = 'VV'
                lu_json['en_lu'] = en_lu
                lu_json['publish'] = True
                lu_json['mapSejong'] = s

#                print(n, lu,frame, len(lus))
                n = n+1


            else:
                lu_json['lu'] = lu
                lemma_var = []
                lemma_var.append(lu_old[0])
                lu_json['lemma_var'] = lemma_var
                lu_json['lexeme'] = lu_old[0]
                lu_json['frameName'] = frame
                lu_json['lu_id'] = 0
                lu_json['fid'] = get_fid(frame)
                lu_json['ko_annotation_id'] = []
                lu_json['pos'] = 'VV'
                lu_json['en_lu'] = en_lu
                lu_json['publish'] = True
                lu_json['mapSejong'] = False
#                print(n, lu,frame, len(lus))
                n = n+1
#            print(lu_json)

            kfn2.append(lu_json)


    with open('../resource/KFN_lus.json','w') as f:
        json.dump(kfn2,f,indent=4,ensure_ascii=False)

    print('done')

#get_from_manual()

def rev_kolu_for_luname():
    with open('../resource/KFN_lus.json','r') as f:
        d = json.load(f)
    for i in d:
        lu_olds = i['lu'].split('.')
        lu_old = lu_olds[0]+'.'+lu_olds[1]
        frame = i['frameName']
        lu_new = lu_old+'.'+frame
        i['lu'] = lu_new
    with open('../resource/KFN_lus.json','w') as f:
        json.dump(d,f,indent=4,ensure_ascii=False)

def rev_with_sejong():
    with open('../resource/KFN_lus.json','r') as f:
        d = json.load(f)
    with open('../resource/sejongset.json','r') as f:
        s = json.load(f)

    for i in d:
        sejongset = i['mapSejong']
        if sejongset != False:
            for j in s:
                if j['sejongset'] == sejongset:
                    lemma = j['lemma']
                    l = lemma
                    if len(lemma) == 1:
                        l = j['word'][:-1]
                    break
#            print(l)
            i['lexeme'] = l

    for i in d:
        sejongset = i['mapSejong']
        if sejongset != False:
            pass
        else:
            ss = []
            for j in s:
                lu = i['lu'].split('.')[0]
                pos = i['lu'].split('.')[1]
                if lu == j['word'] and pos == j['pos']:
                    ss.append(j['sejongset'])
#            print(ss)
            if len(ss) == 1:
                i['mapSejong'] = ss[0]

    with open('../resource/KFN_lus.json','w') as f:
        json.dump(d,f,indent=4,ensure_ascii=False)

def gen_public():
    with open('../resource/KFN_lus.json','r') as f:
        nopub = json.load(f)

#    with open('../resource/KFN_lus_all.pickle','wb') as f:
#        pickle.dump(nopub,f)

#    with open('../resource/KFN_lus_all.pickle','rb') as f:
#        nopub = pickle.load(f)

    lus = []
    lid = 1
    n = 1
    for i in nopub:
        if i['publish'] == True:
            i['lu_id'] = lid
            lus.append(i)
            lid = lid +1
    with open('../resource/KFN_lus.json','w') as f:
        json.dump(lus,f,indent=4,ensure_ascii=False)


def gen_kfn_by_frame():
    with open('../resource/KFN_lus.json','r') as f:
        lus = json.load(f)

    with open('../resource/FN17_frame_id.json') as f:
        fids = json.load(f)

    for i in fids:
        kolu = []
        for j in lus:
            if j['frameName'] == i['frame']:
                kolu.append(j['lu'])
            else:
                pass
        i['ko_lu'] = kolu

    with open('../resource/KFN_frame_lu_pair.json','w') as f:
        json.dump(fids,f,indent=4,ensure_ascii=False)

def get_sejong_anno(sid):
    with open('../resource/KFN_annotations_from_sejong.json','r') as f:
        sejong = json.load(f)
    result = []
    for i in sejong:
        if sid == i['sejongset']:
            for j in  i['annotations']:
                result.append(j['ko_annotation_id'])
            break
    return result

def gen_annotations_from_sejong():
    with open('../resource/KFN_lus.json','r') as f:
        lus = json.load(f)
    for i in lus:
        sid = i['mapSejong']
        sejong_anno = []
        if sid != False:
            try:
                l = i['sejong_annotation_id']
            except:
                i['sejong_annotation_id'] = []
            if len(i['sejong_annotation_id']) == 0:
                s = get_sejong_anno(sid)
#                print(i)
                sejong_anno = s
                print(i['lu_id'],s)
                i['sejong_annotation_id'] = sejong_anno
#        break
    with open('../resource/KFN_lus.json','w') as f:
        json.dump(lus,f,indent=4,ensure_ascii=False)


def gen_again_manual():
    manual = load_manual()
    with open('../resource/KFN_lus.json','r') as f:
        lus = json.load(f)

    print(len(manual))

    add = []
    for m in manual:
#        print(m)
        l = m['lu']+'.'+m['frame']
        lu = {}
        lu['lu'] = l
        lu['publish'] = True
        lemma = m['lu'].split('.')[0][:-1]
        lu['lexeme'] = lemma
        lu['pos'] = 'VV'
        lemma_var = []
        lemma_var.append(lemma)
        lu['lemma_var'] = lemma_var
        lu['frameName'] = m['frame']
        lu['mapSejong'] = False
        lu['fid'] = get_fid(m['frame'])
        lu['ko_annotation_id'] = []
        en_lus = []
        en_lus.append(m['en_lu'])
        lu['lu_id'] = 1
        lu['en_lu'] = en_lus
        new = True
        for i in lus:
            if l == i['lu']:
                new = False
            else:
                pass
        if new:
            add.append(lu)
#            print(lu)
    lus = lus + add
    with open('../resource/KFN_lus.json','w') as f:
        json.dump(lus,f,indent=4,ensure_ascii=False)

def final_rev():
    with open('../resource/KFN_lus.json','r') as f:
        d = json.load(f)

    for i in d:
        try:
            l = i['sejong_annotation_id']
        except:
            i['sejong_annotation_id'] = []
            print(i['lu_id'])
    with open('../resource/KFN_lus.json','w') as f:
        json.dump(d,f,indent=4,ensure_ascii=False)

def final_final_rev():
    with open('../resource/KFN_lus.json','r') as f:
        d = json.load(f)
    n = 0
    lus = d
    for i in d:
        lex = i['lu'].split('.')[0]
        pos = i['lu'].split('.')[1]
        frame = i['lu'].split('.')[2]
        new = True
        if lex[-2:] == '다다':
            print(i['lu'])
            i['lu'] = lex[:-1]+'.'+pos+'.'+frame
#            for j in lus:
#                if lu == j['lu']:
#                    new = False
#                else:
#                    pass
#            if new == True:
#                print('wow')
#                n = n+1
#    print(n)
    with open('../resource/KFN_lus.json','w') as f:
        json.dump(d,f,indent=4,ensure_ascii=False)


def final_check_duple():
    with open('../resource/KFN_lus.json','r') as f:
        d = json.load(f)
    result = []
    n = 0
    for i in d:
        if n == 0:
            result.append(i)
            n = n+1
        else:
            new = True
            for j in result:
                if i['lu'] == j['lu']:
                    ko_annotation_id = j['ko_annotation_id']
                    ko_annotation_id = ko_annotation_id + i['ko_annotation_id']
                    j['ko_annotation_id'] = list(set(ko_annotation_id))
                    en_lu = j['en_lu']
                    en_lu = en_lu + list(set(i['en_lu']))
                    j['en_lu'] = en_lu
                    lemma_var = j['lemma_var']
                    lemma_var = lemma_var + i['lemma_var']
                    j['lemma_var'] = list(set(lemma_var))

                    sid = j['sejong_annotation_id']
                    sid = sid + i['sejong_annotation_id']
                    j['sejong_annotation_id'] = list(set(sid))
                    

                    new = False
#                    print('merged',i['lu_id'])
#                    print(j)
                    break
                else:
                    pass
            if new:
                result.append(i)
#    print(len(result))


    with open('../resource/KFN_lus.json','w') as f:
        json.dump(result,f,indent=4,ensure_ascii=False)


#final_check_duple()
#gen_public()
#gen_kfn_by_frame()




#gen_again_manual()
#print(1)
#rev_with_sejong()
#print(2)
#gen_public()
#print(3)
#gen_kfn_by_frame()
#print(4)
#gen_annotations_from_sejong()
#print(5)
#final_rev()
#final_final_rev()




#gen_entry()
#rev_kolu()
#rev_kolu2()
#get_from_manual()
#rev_kolu_for_luname()
#rev_with_sejong()
#gen_public()
#gen_kfn_by_frame()
#gen_annotations_from_sejong()

def test():
    with open('../resource/KFN_lus.json','r') as f:
        d = json.load(f)
    print(len(d))

test()
