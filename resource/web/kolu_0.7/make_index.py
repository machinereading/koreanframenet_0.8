import json

indices = []

for i in range(1,8221) :
	f = open(str(i) + '.json')
	data = json.loads(f.read())

	f.close()
	indices.append({'lu':data['ko_lu'], 'pos':data['ko_pos'], 'id':i})

indices = sorted(indices, key=lambda x: x['lu'])
print indices[0]['lu']
f = open('index.json', 'w')
f.write(json.dumps(indices))

f.close()
