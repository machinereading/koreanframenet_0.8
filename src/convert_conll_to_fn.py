
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
#                 fe_list = fe_bio.split('-')[1:]
#                 fe = '_'.join(fe_list)
                d = {}
                d['id'] = fe_id
#                 d['obj'] = fe.title()
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


# In[39]:


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


# In[22]:


def get_anno_item(anno, target_span, frame):
    b = target_span['begin']
    e = target_span['end']
    result = False
    for i in anno['frameAnnotation']['ko_annotations']:
        ko_annotation_id = i['ko_annotation_id']
        ori_frame = i['frameName']
        rev_frame = rev_annoframe(ko_annotation_id)
        if rev_frame:
            pass
        else:
            rev_frame = ori_frame
        if frame == rev_frame:
            ori_b = -1
            ori_e = -1
            for d in i['denotations']:
                if d['obj'] == 'target':
                    ori_b = int(d['span']['begin'])
                    ori_e = int(d['span']['end'])
            if ori_b >= 0:
                if b <= ori_b and ori_e <= e:
                    result = i
                    break
                
    if result == False:
        for i in anno['frameAnnotation']['ko_annotations']:
            ko_annotation_id = i['ko_annotation_id']
            rev_frame = rev_annoframe(ko_annotation_id)
            if frame == rev_frame:
                result = i
                break
                
    if result:
        return result
    else:
        print('ERROR_get_anno_item')


# In[41]:


def get_origin_item(sent_id):
    text_item = False
    frame_item = False
    with open(v01+'KFN_annotations.json','r') as f:
        annos = json.load(f)
    for i in annos:
        text_i = i['text']
        frame_i = i['frameAnnotation']
        if sent_id == text_i['sent_id']:
            text_item = text_i
            frame_item = frame_i
            break
    if text_item and frame_item:
        return text_item, frame_item
    else:
        print('ERROR_get_origin_item')


# In[13]:


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


# In[19]:


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
        
        
# text = '나는 밥을 먹었다'
# span = get_token_span([1,2], text)
# print(span)


# In[16]:


def gen_denotations(tokens, text, frame_index):
    # 1) find target
    target_ids = []
    for token in tokens:
        if token[12] != '_':
            target_ids.append(int(token[0]))
            target = token[12]
    span = get_token_span(target_ids, text)
    deno = {}
    deno['id'] = 1
    deno['obj'] = frame_index
    deno['span'] = span
    deno['token_span'] = target_ids
    deno['role'] = 'TARGET'
    b = span['begin']
    e = span['end']
    deno['text'] = text[b:e]
    denos = []
    denos.append(deno)
    # 2) find arguments
    fe_id = 2
    for i in range(len(tokens)):
        if tokens[i][14] != 'O':
            fe_bio = tokens[i][14]
#             print(i, fe_bio)
            fe_list = fe_bio.split('_')[1:]
            fe = '_'.join(fe_list)
            if fe_bio.startswith('B'):
                d = {}
                d['id'] = fe_id
                d['obj'] = fe.title()                
                n = 1
                arg_span = []
                arg_span.append(int(tokens[i][0]))
                nextfe = False
                while i+n < len(tokens):
                    nextfe = tokens[i+n][14]
                    if nextfe == 'I_'+fe:
                        arg_span.append(int(tokens[i+n][0]))
                        n += 1
                    else:
                        break                    
                fe_id += 1
                d['token_span'] = arg_span
                span = get_token_span(arg_span, text)
                d['span'] = span
                b = span['begin']
                e = span['end']
                d['text'] = text[b:e]
                d['role'] = 'ARGUMENT'
                denos.append(d)
            elif fe_bio.startswith('S'):
                fe_bio = tokens[i][14]
                fe_list = fe_bio.split('_')[1:]
                fe = '_'.join(fe_list)
                d = {}
                d['id'] = fe_id
                d['obj'] = fe.title()
                token_span = [ int(tokens[i][0]) ]
                d['token_span'] = token_span
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
    if denos:
        return denos
    else:
        print('ERROR_gen_denotations')
            
            
#     for i in tokens:
        


# In[43]:


def gen_annotation():
    sentlist = []
    for i in sent_idx:
        sentlist.append(i)
    
    ko_annotation_id = 0
    annotation_file = []
    for sent_id in sentlist:
#         sent_id = 3033
        annotation_file_item = {}
        
        text = sent_idx[sent_id]
        text_item, frame_item = get_origin_item(sent_id)
        text_item['ko_text'] = text
        annotation_file_item['text'] = text_item

        annotations = anno_idx[sent_id]
        anno = get_anno(sent_id)
        print('sid:', sent_id)
        print('text:',text)   
        anno_items = []
        for a in annotations:
#             print(a)
            if a:
                frame = get_frame(a)
                target, target_id = get_target(a)
                lu = get_lu(a)
                lu = lu+'.'+frame
    #             print('frame', frame)
                denos = gen_denotations(a, text, frame)
                for i in denos:
                    if i['role'] == 'TARGET':
                        target_span = i['span']
                anno_item = get_anno_item(anno, target_span, frame)
                try:
                    origin_lus = anno_item['origin_lus']
                except KeyboardInterrupt:
                    raise
                except:
                    origin_lus = []
                for i in origin_lus:
                    i = i.lower()
                origin_lus = list(set(origin_lus))
                anno_item['origin_lus'] = origin_lus
                anno_item['denotations'] = denos
                anno_item['frameName'] = frame
                relations = get_relations(denos)
                anno_item['relations'] = relations
                anno_item['ko_annotation_id'] = ko_annotation_id
                anno_item['lu'] = lu
    #             anno_item['target'] = target
                anno_items.append(anno_item)
                ko_annotation_id += 1
    
        frame_item['ko_annotations'] = anno_items
        annotation_file_item['frameAnnotation'] = frame_item
        print(len(anno_items),'annotations are saved.\n')
        annotation_file.append(annotation_file_item)
        
        
# #         break  
#     with open('../resource/v0.8/KFN_annotations.json','w') as f:
#         json.dump(annotation_file, f, ensure_ascii=False, indent=4)
        
#     print(len(annotation_file), 'sentences')
#     print(ko_annotation_id, 'annotations')
        
# gen_annotation()


# In[17]:


# with open(fndir+'KFN_annotations.json','r') as f:
#     annos = json.load(f)
# for i in annos:
#     k = i['frameAnnotation']['ko_annotations']
#     frames = []
#     for j in k:
#         f = j['frameName']
#         if f in frames:
#             print(i['text']['sent_id'])
#         frames.append(f)

