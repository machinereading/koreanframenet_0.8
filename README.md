# Korean FrameNet

## About

Korean FrameNet is a lexical database that has rich annotations to represent the meaning of text using semantic frames

## prerequisite
* `python 3`
* `nltk` (optional)

## How to use
refer `example.py`

### How to get all LUs
```
import json
import kfn
lus = kfn.lus()
print(len(lus))
```
`14699` LUs are in Korean FrameNet

### How to get lexical unit (LU) IDs
```
import json
import kfn
from nltk.corpus import framenet as fn

#get lus
lus = kfn.lus_by_lemma('나누다')
lus = kfn.lus_by_lemma('나누') #if you want use a morpheme
print(lus)
```
`[{'lu': '나누다.v.Separating', 'lu_id': 5045}, {'lu': '나누다.v.Giving', 'lu_id': 6937}]`  

In this case, the word '나누다' has two meanings (frames), `Separating` and `Giving`

### How to get LU object by LU IDs
```
#get lu by lu_id
lu_id == lus[0]['lu_id'] #if you want to get information about the LU '`나누다.v.Separating`'
lu = kfn.lu(lu_id)

frame_id = lu['fid']
f = fn.frame(frame_id)
print('frame:', f.name) #Frame Name
print('definition:', f.definition) #Frame Definition
```
`frame: Separating`  
`definition: These words refer to separating a Whole into Parts, or separating one part from another.`  

### How to get Annotations by LU IDs
```
annotations = kfn.annotation(lus[1]['lu_id'])
print('text:', annotations[1]['text'])
print('denotations:', annotations[1]['denotations'])
```
`'text': '1949의 휴전협정 결과로 예루살렘은 나누어졌다 : 서 예루살렘은 ...`  

In the `denotations`, the text '1949의 휴전협정 결과' is annotated as a frame element `cause`, and the text '예루살렘' is a frame element `whole`.

## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)

## Maintainer
Younggyun Hahm `hahmyg@kaist.ac.kr`

## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST

## Ciation
the paper _'Semi-automatic Korean FrameNet Annotation over KAIST Treebank'_ is accepted at LREC2018
