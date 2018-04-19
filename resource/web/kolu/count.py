import json

l = {}
pos = {}
total_target = 0
for i in range(1, 7131) : 
	f = open(str(i) + '.json')
	cur_count = 0 
	data = json.loads(f.read())
	for pattern in data['patterns'] : 
		cur_count +=len(pattern['examples'])
	total_target += cur_count
	if data['frameName'] not in l : 
		l[data['frameName']] = cur_count
	else :
		l[data['frameName']] += cur_count

print total_target
for elem in l.keys() : 
	print unicode(elem) + '\t' +  unicode(l[elem])

print len(l.keys())
"""
	if data['ko_pos'] in pos.keys() : 
		pos[data['ko_pos']] += 1
	else :
		pos[data['ko_pos']] = 1

for elem in pos.keys() : 
	print unicode(elem) + '\t' +  unicode(pos[elem])
"""
f.close()