import json

with open('./resource/KFN_lus.json','r') as f:
    d = json.load(f)

n,v,a,fr = [],[],[],[]
for i in d:
    lu = i['lu']
    pos = lu.split('.')[-1]
    f = i['fid']

    if pos == 'n':
        n.append(lu)
    elif pos == 'v':
        v.append(lu)
    elif pos == 'a':
        a.append(lu)
    else:
        pass
    fr.append(f)

#print(len(n),len(v),len(a), len(d))
#print(len(list(set(n))), len(list(set(v))), len(list(set(a))))
#print(len(list(set(fr))))

n = 0
for i in d:
    if i['mapSejong'] != False:
        n = n+1
print(n)



