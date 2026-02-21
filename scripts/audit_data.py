#!/usr/bin/env python3
"""
Comprehensive audit of people and institution data consistency.

Checks:
1. Person location matches their institution's location (city/country)
2. Person's current_position.institution matches an institution file name
3. Institution member/alumni directories are consistent with people data
4. Coordinates are reasonable (not null, not 0,0)
5. All required fields present
"""
import json, os, sys, math

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE_JSON = os.path.join(ROOT, 'website', 'static', 'data', 'people.json')
INST_JSON = os.path.join(ROOT, 'website', 'static', 'data', 'institutions.json')

with open(PEOPLE_JSON, 'r', encoding='utf-8') as f:
    people = json.load(f)

with open(INST_JSON, 'r', encoding='utf-8') as f:
    institutions = json.load(f)

# Build institution lookup
inst_by_name = {}
inst_aliases = {}
for inst in institutions:
    inst_by_name[inst['name']] = inst
    for alias in (inst.get('aliases') or []):
        inst_aliases[alias] = inst['name']

issues = []
warnings = []

print("=" * 70)
print("DATA CONSISTENCY AUDIT")
print("=" * 70)

# ── 1. Check each person ─────────────────────────────────────────────
print("\n── PERSON CHECKS ──")
for p in people:
    pid = p.get('id', '???')
    name = p.get('name', '???')
    loc = p.get('location', {})
    cp = p.get('current_position', {})
    
    # Check required fields
    if not loc.get('city'):
        issues.append(f"[{pid}] {name}: MISSING city")
    if not loc.get('country'):
        issues.append(f"[{pid}] {name}: MISSING country")
    if loc.get('lat') is None or loc.get('lon') is None:
        issues.append(f"[{pid}] {name}: MISSING coordinates")
    elif loc['lat'] == 0 and loc['lon'] == 0:
        issues.append(f"[{pid}] {name}: Coordinates are (0,0) - likely wrong")
    
    if not cp.get('institution'):
        issues.append(f"[{pid}] {name}: MISSING current_position.institution")
        continue
    
    inst_name = cp['institution']
    
    # Check if institution exists
    matched_inst = inst_by_name.get(inst_name)
    if not matched_inst:
        # Try aliases
        canonical = inst_aliases.get(inst_name)
        if canonical:
            matched_inst = inst_by_name.get(canonical)
            warnings.append(f"[{pid}] {name}: Institution '{inst_name}' matched via alias to '{canonical}'")
        else:
            issues.append(f"[{pid}] {name}: Institution '{inst_name}' NOT FOUND in institution files")
            continue
    
    # Check person location vs institution location
    p_city = (loc.get('city') or '').strip().lower()
    p_country = (loc.get('country') or '').strip().lower()
    i_city = (matched_inst.get('location', {}).get('city') or '').strip().lower()
    i_country = (matched_inst.get('location', {}).get('country') or '').strip().lower()
    
    if p_country and i_country and p_country != i_country:
        issues.append(f"[{pid}] {name}: Country mismatch - person='{loc.get('country')}', institution '{inst_name}'='{matched_inst['location'].get('country')}'")
    
    if p_city and i_city and p_city != i_city:
        # Check if they're close by coordinates instead
        p_lat = loc.get('lat', 0) or 0
        p_lon = loc.get('lon', 0) or 0
        i_lat = matched_inst.get('location', {}).get('lat', 0) or 0
        i_lon = matched_inst.get('location', {}).get('lon', 0) or 0
        
        if p_lat and i_lat:
            dist_deg = math.sqrt((p_lat - i_lat)**2 + (p_lon - i_lon)**2)
            if dist_deg > 0.5:  # More than ~50km apart
                issues.append(
                    f"[{pid}] {name}: LOCATION MISMATCH - person city='{loc.get('city')}' ({p_lat},{p_lon}), "
                    f"institution '{inst_name}' city='{matched_inst['location'].get('city')}' ({i_lat},{i_lon}) "
                    f"[~{dist_deg*111:.0f}km apart]"
                )
            else:
                warnings.append(
                    f"[{pid}] {name}: City name differs ('{loc.get('city')}' vs '{matched_inst['location'].get('city')}') "
                    f"but coordinates are close (~{dist_deg*111:.0f}km)"
                )

# ── 2. Check each institution ────────────────────────────────────────
print("\n── INSTITUTION CHECKS ──")
for inst in institutions:
    iid = inst.get('id', '???')
    iname = inst.get('name', '???')
    iloc = inst.get('location', {})
    
    if not iloc.get('city'):
        issues.append(f"[INST {iid}] {iname}: MISSING city")
    if not iloc.get('country'):
        issues.append(f"[INST {iid}] {iname}: MISSING country")
    if iloc.get('lat') is None or iloc.get('lon') is None:
        issues.append(f"[INST {iid}] {iname}: MISSING coordinates")
    elif iloc['lat'] == 0 and iloc['lon'] == 0:
        issues.append(f"[INST {iid}] {iname}: Coordinates are (0,0)")
    
    if not inst.get('short_description'):
        warnings.append(f"[INST {iid}] {iname}: MISSING short_description")
    
    # Check directory consistency
    directory = inst.get('directory', {})
    members = directory.get('current_members', [])
    alumni = directory.get('alumni', [])
    member_count = directory.get('member_count', 0)
    alumni_count = directory.get('alumni_count', 0)
    
    if len(members) != member_count:
        issues.append(f"[INST {iid}] {iname}: member_count={member_count} but actual members={len(members)}")
    if len(alumni) != alumni_count:
        issues.append(f"[INST {iid}] {iname}: alumni_count={alumni_count} but actual alumni={len(alumni)}")

# ── 3. Cross-reference: verify institution directories match people ──
print("\n── CROSS-REFERENCE CHECKS ──")

# Build expected member lists from people data
expected_members = {}  # inst_name -> set of md_filenames
for p in people:
    cp = p.get('current_position', {})
    if cp.get('institution'):
        inst = cp['institution']
        if inst not in expected_members:
            expected_members[inst] = set()
        expected_members[inst].add(p.get('md_filename', ''))

for inst in institutions:
    iname = inst['name']
    directory = inst.get('directory', {})
    actual_members = set(directory.get('current_members', []))
    expected = expected_members.get(iname, set())
    
    missing_from_dir = expected - actual_members
    extra_in_dir = actual_members - expected
    
    if missing_from_dir:
        issues.append(f"[INST] {iname}: People in this institution but NOT in directory: {missing_from_dir}")
    if extra_in_dir:
        warnings.append(f"[INST] {iname}: In directory but NOT listed as current: {extra_in_dir}")

# ── 4. Summary ───────────────────────────────────────────────────────
print(f"\n{'='*70}")
print(f"ISSUES ({len(issues)}):")
print(f"{'='*70}")
for i, issue in enumerate(issues, 1):
    print(f"  {i:2d}. {issue}")

print(f"\n{'='*70}")
print(f"WARNINGS ({len(warnings)}):")
print(f"{'='*70}")
for i, warning in enumerate(warnings, 1):
    print(f"  {i:2d}. {warning}")

print(f"\n{'='*70}")
print(f"TOTALS: {len(people)} people, {len(institutions)} institutions")
print(f"ISSUES: {len(issues)} | WARNINGS: {len(warnings)}")
print(f"{'='*70}")
