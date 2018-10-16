
# coding: utf-8

# In[1]:


import json
from pprint import pprint


# In[29]:


v01 = '../resource/v0.1/'
v07 = '../resource/'
v08 = '../resource/v0.8/'


# In[3]:


def load_data():
    with open(v01+'KFN_lus.json','r') as f:
        kfn = json.load(f)
    return kfn
kfn = load_data()


# In[4]:


def load_csv():
    with open('../data/v0.8/training.tsv','r') as f:
        trn = f.readlines()
    with open('../data/v0.8/test.tsv','r') as f:
        tst = f.readlines()
    with open('../data/v0.8/dev.tsv','r') as f:
        dev = f.readlines()
    trn.append('\n')
    tst.append('\n')
    tst.append('\n')
    cdata = trn+tst+dev
    sent = []
    d = {}
    result = []
    n_of_sents = 0
    sent_idx = {}
    # 1) gen sent_id and its text:
    for line in cdata:
        line = line.rstrip('\n')
        if line.startswith('#'):
            if line[1] == 's':
                sent_id = int(line.split(':')[1])
            if line[1] == 't':
                text = line.split('text:')[1]
                text_list = text.split(' ')
                text = ' '.join(text_list)
        else:
            if sent_id and text:
                sent_idx[sent_id] = text
            sent_id = False
            text = False
    anno_idx = {}
    for line in cdata:
        line = line.rstrip('\n')
        if line.startswith('#'):
            if line[1] == 's':
                sent_id = int(line.split(':')[1])
        else:
            if line != '':
                token = line.split('\t')
                sent.append(token)
            else:
                exist = False
                for a in anno_idx:
                    if sent_id == a:
                        exist = True
                if exist:
                    annotations = anno_idx[sent_id]
                    annotations.append(sent)
                    anno_idx[sent_id] = annotations
#                     break
                else:
                    annotations = []
                    annotations.append(sent)
                    anno_idx[sent_id] = annotations
                sent = []
    return sent_idx, anno_idx                   

sent_idx, anno_idx = load_csv()


# In[5]:


# print(sent_idx[1])
# print(anno_idx[1])


# In[30]:


with open(v01+'KFN_annotations.json','r') as f:
    kfn_annos = json.load(f)
with open(v07+'KFN_annotations.json','r') as f:
    kfn_annos_07 = json.load(f)


# In[8]:


def get_anno(sent_id):
#     print('input:',sent_id)
    result = False
    for i in kfn_annos:
        origin_id = i['text']['sent_id']
        if sent_id == origin_id:
            result = i
            break
    if result:
        return result
    else:
        print('ERROR')


# In[9]:


def get_frame(tokens):
    frame = False
    for token in tokens:
        if token[13] != '_':
            frame = token[13]
    if frame:
        return frame


# In[10]:


def get_lu(tokens):
    lu = False
    for token in tokens:
        if token[12] != '_':
            lu = token[12]
    if lu:
        return lu
    else:
        print('ERROR: get_lu')


# In[43]:


def get_target(tokens):
    target = False
    target_ids = []
    target_word = []
    for token in tokens:
        if token[12] != '_':
            target_word.append(token[1])
            target_ids.append(int(token[0]))
    if len(target_word) > 0:
        target = ' '.join(target_word)
        
    
    if target:
        return target, target_ids
    else:
        print('ERROR_get_target')


# In[12]:


def rev_annoframe(ko_annotation_id):
    frame = False
    for i in kfn:
        if ko_annotation_id in i['ko_annotation_id']:
            frame = i['frameName']
            break
    return frame


# In[42]:


def get_origin_lus(lu, frame):
    result = []
    origin_lus = []
    item = lu+'.'+frame
    for i in kfn:
        if item == i['lu']:
            origin_lus = i['en_lu']
            break
    for i in origin_lus:
        lu = i.lower()
        result.append(lu)
    result = list(set(result))
    return result


# In[14]:


def get_token_span(token_ids, text):
    text = text.split(' ')
    d = {}
    cid = -1
    for i in range(len(text)):
        if i == 0:
            d[i] = (0, len(text[i]))
            cid = len(text[i]) +1
        else:
            d[i] = (cid, cid+len(text[i]))
            cid =  cid+len(text[i]) +1
    start = True
    for i in token_ids:
        if start == True:
            begin = d[i][0]
            start = False
        end = d[i][1]
    span = {}
    span['begin'] = begin
    span['end'] = end
    return span


# In[15]:


def get_args(tokens, text):
    denos = []
    fe_id = 2
    for i in range(len(tokens)):
        if tokens[i][14] != 'O':

            fe_bio = tokens[i][14]
            fe = fe_bio.split('-')[1]
            
            if fe_bio.startswith('B'):
                d = {}
                d['id'] = fe_id
                d['obj'] = fe              
                n = 1
                arg_span = []
                arg_span.append(int(tokens[i][0]))
                nextfe = False
                while i+n < len(tokens):
                    nextfe = tokens[i+n][14]
                    if nextfe == 'I-'+fe:
                        arg_span.append(int(tokens[i+n][0]))
                        n += 1
                    else:
                        break                    
                fe_id += 1
                d['tokens'] = arg_span
                span = get_token_span(arg_span, text)
                d['span'] = span
                b = span['begin']
                e = span['end']
                d['text'] = text[b:e]
                d['role'] = 'ARGUMENT'

                denos.append(d)
            elif fe_bio.startswith('S'):
                fe_bio = tokens[i][14]
                fe = fe_bio.split('-')[1]
#                 fe_list = fe_bio.split('-')[1:]
#                 fe = '_'.join(fe_list)
                d = {}
                d['id'] = fe_id
                d['obj'] = fe
                token_span = [ int(tokens[i][0]) ]
                d['tokens'] = token_span
                span = get_token_span(token_span, text)
                d['span'] = span
                b = span['begin']
                e = span['end']
                d['text'] = text[b:e]
                d['role'] = 'ARGUMENT'
                fe_id += 1
                denos.append(d)
            else:
                pass
    return denos


# In[16]:


def get_relations(denos):
    relations = []
    for i in denos:
        if i['role'] == 'ARGUMENT':
            did = i['id']
            relation = {}
            relation['subj'] = 1
            relation['obj'] = did
            relation['pred'] = 'arg'
            relations.append(relation)
    return relations


# In[41]:


def get_annotation_id(sent_id, frame, target_ids):
    annotation_id = False
    for i in kfn_annos_07:
        if sent_id == i['text']['sent_id']:
            for a in i['frameAnnotation']['ko_annotations']:
                
                target_frame = a['frameName']
                
                if frame == target_frame:
                
                    for d in a['denotations']:
                        if d['role'] == 'TARGET':
                            if target_ids[0] <= d['token_span'][0] +5 and target_ids[-1] + 5  >= d['token_span'][-1]:
                                annotation_id = a['annotation_id']
                                break
                if not annotation_id:
                    annotat_id = a['annotation_id']
            break
    if annotation_id:
        return annotation_id
    else:
        print('ERROR: get_annotation_id')


# In[47]:


def gen_data():
    result = []
    ko_annotation_id = 0
    for sent_id in anno_idx:
        conlls = anno_idx[sent_id]
        tokens = []
        for conll in conlls:
            for token in conll:
                word = token[1]
                tokens.append(token[1])
            break
        text = ' '.join(tokens)
         
        anno = get_anno(sent_id)
        anno['text']['ko_text'] = text
        anno['text']['ko_tokens'] = tokens       
        
        ko_annotations = []
        for conll in conlls:
            if len(conll) > 0:
                denos = []
                target, target_id = get_target(conll)
                lu = get_lu (conll)
                frame = get_frame(conll)
                origin_lus = get_origin_lus(lu, frame)


    #             print(target, target_id, lu, frame, origin_lus)

                # for target
                deno = {}
                deno['role'] = 'TARGET'
                deno['id'] = 1
                deno['obj'] = frame
                span =  get_token_span(target_id, text)
                deno['span'] = span
                deno['tokens'] = target_id
                deno['text'] = text[span['begin']:span['end']]
                denos.append(deno)

                # for arguments
                args = get_args(conll, text)
                denos = denos + args

                relations = get_relations(denos)

                ko_annotation = {}
                ko_annotation['origin_lus'] = origin_lus
                ko_annotation['ko_annotation_id'] = ko_annotation_id            
                annotation_id = get_annotation_id(sent_id, frame, target_id)

                ko_annotation['annotation_id'] = annotation_id

                ko_annotation['denotations'] = denos
                ko_annotation['sent_id'] = sent_id
                ko_annotation['relations'] = relations
                ko_annotation['lu'] = lu

                ko_annotations.append(ko_annotation)
                print(ko_annotation_id)
                ko_annotation_id += 1
        anno['frameAnnotation']['ko_annotations'] = ko_annotations
        
        
        result.append(anno)
        
    with open(v08+'KFN_annotations.json','w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
            
        
gen_data() 

