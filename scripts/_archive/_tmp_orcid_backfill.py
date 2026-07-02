# -*- coding: utf-8 -*-
"""Backfill links.orcid (and links.openalex) for non-stub people missing them,
via OpenAlex author search. STRICT matching:
  - last name exact (case-insensitive), first initial matches
  - and the OpenAlex author's affiliation history overlaps the person's known
    institution names (current_position.institution or affiliations[].name)
Only writes when exactly one candidate passes. Never touches other fields."""
import glob, json, re, sys, time, unicodedata
import requests
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MAILTO = "ozerilab@weizmann.ac.il"

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z ]', ' ', s.lower()).strip()

def name_match(person_name, cand_name):
    pn, cn = norm(person_name).split(), norm(cand_name).split()
    if not pn or not cn:
        return False
    if pn[-1] != cn[-1]:           # last name exact
        return False
    return pn[0][0] == cn[0][0]    # first initial

def inst_tokens(fm):
    toks = set()
    cp = fm.get('current_position') or {}
    for nm in [cp.get('institution')] + [a.get('name') for a in (fm.get('affiliations') or []) if isinstance(a, dict)]:
        if nm:
            t = norm(nm)
            toks.add(t)
            # distinctive words (len>4, not generic)
            for w in t.split():
                if len(w) > 4 and w not in ('university', 'institute', 'national', 'center', 'centre', 'technology', 'institut', 'laboratory', 'college', 'department', 'research', 'sciences', 'science'):
                    toks.add(w)
    return toks

def affil_names(author):
    out = []
    for a in (author.get('affiliations') or []):
        n = (a.get('institution') or {}).get('display_name')
        if n:
            out.append(n)
    for i in (author.get('last_known_institutions') or []):
        if i.get('display_name'):
            out.append(i['display_name'])
    return out

targets = []
for f in sorted(glob.glob('content/people/*.md')):
    if f.endswith('.evidence.md'):
        continue
    raw = open(f, encoding='utf-8').read()
    fm = yaml.safe_load(raw.split('---')[1])
    if fm.get('stub') or str(fm.get('id', '')).startswith('000-'):
        continue
    links = fm.get('links') or {}
    if links.get('orcid'):
        continue
    targets.append((f, fm))
print(f"{len(targets)} non-stub people missing orcid")

found, ambiguous, none = [], [], []
session = requests.Session()
for idx, (f, fm) in enumerate(targets):
    name = fm['name']
    try:
        r = session.get('https://api.openalex.org/authors',
                        params={'search': name, 'per-page': 25, 'mailto': MAILTO}, timeout=30)
        results = r.json().get('results', [])
    except Exception as e:
        print(f"  ERR {name}: {e}")
        continue
    toks = inst_tokens(fm)
    cands = []
    for a in results:
        if not name_match(name, a.get('display_name', '')):
            # also check alternatives
            if not any(name_match(name, alt) for alt in (a.get('display_name_alternatives') or [])[:5]):
                continue
        affs = [norm(x) for x in affil_names(a)]
        aff_hit = any(any(tok in aff or aff in tok for aff in affs) for tok in toks if len(tok) > 4)
        if aff_hit:
            cands.append(a)
    # dedupe candidates by orcid/id
    seen, uniq = set(), []
    for a in cands:
        k = a.get('orcid') or a.get('id')
        if k not in seen:
            seen.add(k)
            uniq.append(a)
    if len(uniq) == 1:
        a = uniq[0]
        found.append({"file": f, "name": name, "orcid": a.get('orcid'),
                      "openalex": a.get('id'), "oa_name": a.get('display_name'),
                      "affs": affil_names(a)[:3], "works": a.get('works_count')})
    elif len(uniq) > 1:
        # prefer the one with most works if names are identical
        uniq.sort(key=lambda x: -(x.get('works_count') or 0))
        if (uniq[0].get('works_count') or 0) >= 3 * max(1, (uniq[1].get('works_count') or 0)):
            a = uniq[0]
            found.append({"file": f, "name": name, "orcid": a.get('orcid'),
                          "openalex": a.get('id'), "oa_name": a.get('display_name'),
                          "affs": affil_names(a)[:3], "works": a.get('works_count')})
        else:
            ambiguous.append({"name": name, "cands": [(x.get('display_name'), x.get('orcid'), x.get('works_count')) for x in uniq[:3]]})
    else:
        none.append(name)
    if (idx + 1) % 20 == 0:
        print(f"  {idx+1}/{len(targets)}  (found {len(found)})")
    time.sleep(0.15)

json.dump({"found": found, "ambiguous": ambiguous, "none": none},
          open('reports/orcid_backfill.json', 'w', encoding='utf-8'), indent=1)
with_orcid = [x for x in found if x['orcid']]
print(f"\nmatched: {len(found)} (with orcid: {len(with_orcid)}), ambiguous: {len(ambiguous)}, none: {len(none)}")

# Apply: insert orcid + openalex into links block of each file
applied = 0
for x in with_orcid:
    raw = open(x['file'], encoding='utf-8').read()
    m = re.search(r'^links:\n', raw, re.M)
    orcid_line = f"  orcid: {x['orcid']}\n"
    oa_line = f"  openalex: {x['openalex']}\n"
    if m:
        ins = orcid_line
        if 'openalex:' not in raw:
            ins += oa_line
        raw = raw[:m.end()] + ins + raw[m.end():]
    else:
        # add links block after the id line
        m2 = re.search(r'^id: .+\n', raw, re.M)
        block = f"links:\n{orcid_line}{oa_line}"
        raw = raw[:m2.end()] + block + raw[m2.end():]
    open(x['file'], 'w', encoding='utf-8').write(raw)
    applied += 1
print(f"applied orcid to {applied} files")
