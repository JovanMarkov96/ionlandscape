#!/usr/bin/env python3
"""Extract unique institutions from people profiles and map members/alumni."""
import json, os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE_JSON = os.path.join(ROOT, 'website', 'static', 'data', 'people.json')

with open(PEOPLE_JSON, 'r', encoding='utf-8') as f:
    people = json.load(f)

# Extract current institutions and build member/alumni maps
institutions = {}  # name -> {current_members: [], alumni: []}

for p in people:
    md = p.get('md_filename', '')
    cp = p.get('current_position', {})
    if isinstance(cp, dict) and cp.get('institution'):
        inst = cp['institution'].strip()
        if inst not in institutions:
            institutions[inst] = {'current_members': [], 'alumni': []}
        institutions[inst]['current_members'].append(md)
    
    # Check education for alumni status
    for edu in (p.get('education') or []):
        if isinstance(edu, dict) and edu.get('institution'):
            einst = edu['institution'].strip()
            if einst not in institutions:
                institutions[einst] = {'current_members': [], 'alumni': []}
            # Only add as alumni if not currently there
            cp_inst = cp.get('institution', '').strip() if isinstance(cp, dict) else ''
            if einst != cp_inst and md not in institutions[einst]['alumni']:
                institutions[einst]['alumni'].append(md)
    
    # Check postdocs for alumni
    for pd in (p.get('postdocs') or []):
        if isinstance(pd, dict) and pd.get('institution'):
            pinst = pd['institution'].strip()
            if pinst not in institutions:
                institutions[pinst] = {'current_members': [], 'alumni': []}
            cp_inst = cp.get('institution', '').strip() if isinstance(cp, dict) else ''
            if pinst != cp_inst and md not in institutions[pinst]['alumni']:
                institutions[pinst]['alumni'].append(md)

# Print current_position institutions (these are most important)
print("=" * 60)
print("CURRENT POSITION INSTITUTIONS (need files):")
print("=" * 60)
cp_insts = set()
for p in people:
    cp = p.get('current_position', {})
    if isinstance(cp, dict) and cp.get('institution'):
        cp_insts.add(cp['institution'].strip())

for i, inst in enumerate(sorted(cp_insts), 1):
    members = institutions[inst]['current_members']
    alumni = institutions[inst]['alumni']
    print(f"{i:2d}. {inst}")
    print(f"    Current members ({len(members)}): {members}")
    if alumni:
        print(f"    Alumni ({len(alumni)}): {alumni}")
    print()
