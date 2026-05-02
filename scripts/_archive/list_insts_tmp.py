import json

f = open('website/static/data/people.json', encoding='utf-8')
p = json.load(f)
f.close()

insts = set(x.get('current_position', {}).get('institution') for x in p if 'current_position' in x)
print('\n'.join(sorted([str(i) for i in insts])))
