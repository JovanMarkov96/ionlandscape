#!/usr/bin/env python3
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE_JSON = os.path.join(ROOT, 'website', 'static', 'data', 'people.json')

with open(PEOPLE_JSON, 'r', encoding='utf-8') as f:
    people = json.load(f)

companies = set()

for p in people:
    cp = p.get('current_position', {})
    inst = cp.get('institution', '')
    
    # We heuristically know these words often mean it's a company
    if any(x in inst.lower() for x in ['inc', 'ltd', 'gmbh', 'ionq', 'quantinuum', 'quantum art', 'eleqtron', 'oxford ionics', 'infleqtion', 'coldquanta', 'alpine quantum']):
        companies.add(inst)
        
    for aff in p.get('affiliations', []):
        if aff.get('type') == 'company':
            companies.add(aff.get('name'))

print("Found Companies:")
for c in sorted(list(companies)):
    print(" -", c)
