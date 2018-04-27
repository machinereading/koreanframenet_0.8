import json
import kfn
import pprint
from nltk.corpus import framenet as fn


#get all lus
lus = kfn.lus()
print(len(lus))

#get lus
lus = kfn.lus_by_lemma('나누다')
print(lus)

#get lu by lu_id
lu = kfn.lu(lus[0]['lu_id'])
pprint.pprint(lu)

frame_id = lu['fid']
f = fn.frame(frame_id)
print(f.name)
print(f.definition)

#get annotations by lu_id
annotations = kfn.annotation(lus[0]['lu_id'])
print(annotations)
