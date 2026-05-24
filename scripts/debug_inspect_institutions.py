import json, os
p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'website', 'static', 'data', 'institutions.json')
print('path=', p)
with open(p, encoding='utf-8') as f:
    data = json.load(f)
print('total=', len(data))
empty = 0
import re
for i, item in enumerate(data[:80]):
    name = item.get('name')
    iid = item.get('id') or ''
    sort = item.get('sort_name')
    if name and name.strip():
        derived = name.strip()
    elif sort and str(sort).strip():
        derived = str(sort).strip()
    else:
        # remove leading iNNN- prefix and any trailing .md like suffixes
        s = re.sub(r'^(i\d+-)?', '', iid)
        s = re.sub(r'md$', '', s)
        derived = s.replace('-', ' ').strip().title()
    if not (name and name.strip()) and not (sort and str(sort).strip()):
        empty += 1
    print(i, 'id=', iid, 'name=', repr(name), 'derived=', derived)
print('empty names count=', empty)
