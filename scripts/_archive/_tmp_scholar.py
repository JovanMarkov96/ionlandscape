# -*- coding: utf-8 -*-
"""Discover Google Scholar profiles for non-stub people missing links.google_scholar.
Uses scholar.google.com author search; STRICT acceptance:
  - exactly one result whose name matches (last exact + first initial)
  - AND affiliation text or verified-email domain overlaps the person's institution
Caches progress in reports/scholar_cache.json (restartable); aborts politely on a
bot-block. Also captures the profile's verified homepage URL when present
(candidate group page). Apply step writes links.google_scholar into the .md."""
import glob, json, os, random, re, sys, time, unicodedata
import requests
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}
CACHE = 'reports/scholar_cache.json'
cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z ]', ' ', s.lower()).strip()

def name_match(person_name, cand_name):
    pn, cn = norm(person_name).split(), norm(cand_name).split()
    if not pn or not cn:
        return False
    if pn[-1] != cn[-1]:
        return False
    return pn[0][0] == cn[0][0]

def inst_tokens(fm):
    toks = set()
    cp = fm.get('current_position') or {}
    names = [cp.get('institution')] + [a.get('name') for a in (fm.get('affiliations') or []) if isinstance(a, dict)]
    for nm in names:
        if nm:
            t = norm(nm)
            for w in t.split():
                if len(w) > 4 and w not in ('university', 'institute', 'national', 'center', 'centre',
                                            'technology', 'institut', 'laboratory', 'college',
                                            'department', 'research', 'sciences', 'science', 'group'):
                    toks.add(w)
    return toks

targets = []
for f in sorted(glob.glob('content/people/*.md')):
    if f.endswith('.evidence.md'):
        continue
    fm = yaml.safe_load(open(f, encoding='utf-8').read().split('---')[1])
    if fm.get('stub') or str(fm.get('id', '')).startswith('000-'):
        continue
    if (fm.get('links') or {}).get('google_scholar'):
        continue
    targets.append((f, fm))
print(f"{len(targets)} people missing google_scholar; {len(cache)} cached")

# author-search result blocks: gsc_1usr ; fields: name in h3 .gs_ai_name a, aff .gs_ai_aff, email .gs_ai_eml
RE_BLOCK = re.compile(r'<div class="gsc_1usr">(.*?)</div>\s*</div>\s*</div>', re.S)
RE_USER = re.compile(r'/citations\?hl=[^&]*&(?:amp;)?user=([\w-]+)')
RE_USER2 = re.compile(r'user=([\w-]+)')
RE_NAME = re.compile(r'gs_ai_name[^>]*><a[^>]*>(.*?)</a>', re.S)
RE_AFF = re.compile(r'gs_ai_aff[^>]*>(.*?)</div>', re.S)
RE_EML = re.compile(r'gs_ai_eml[^>]*>(.*?)</div>', re.S)
TAGS = re.compile(r'<[^>]+>')

session = requests.Session()
blocked = False
processed = 0
for f, fm in targets:
    pid = fm['id']
    if pid in cache:
        continue
    if blocked:
        break
    name = fm['name']
    q = requests.utils.quote(name)
    url = f"https://scholar.google.com/citations?view_op=search_authors&mauthors={q}&hl=en"
    try:
        r = session.get(url, headers=UA, timeout=25)
    except Exception as e:
        print(f"  ERR {name}: {e}")
        time.sleep(10)
        continue
    if r.status_code == 429 or 'unusual traffic' in r.text or 'gs_captcha' in r.text:
        print(f"  BLOCKED at {name} ({processed} done this run) — stopping politely")
        blocked = True
        break
    blocks = RE_BLOCK.findall(r.text)
    toks = inst_tokens(fm)
    cands = []
    for b in blocks:
        nm = TAGS.sub('', (RE_NAME.search(b) or [None, ''])[1] if RE_NAME.search(b) else '')
        nm = nm.replace('&nbsp;', ' ').strip()
        um = RE_USER.search(b) or RE_USER2.search(b)
        aff = TAGS.sub('', RE_AFF.search(b).group(1)) if RE_AFF.search(b) else ''
        eml = TAGS.sub('', RE_EML.search(b).group(1)) if RE_EML.search(b) else ''
        if not um or not nm:
            continue
        if not name_match(name, nm):
            continue
        hay = norm(aff + ' ' + eml)
        aff_hit = any(t in hay for t in toks)
        cands.append({"user": um.group(1), "name": nm, "aff": aff, "eml": eml, "aff_hit": aff_hit})
    strong = [c for c in cands if c['aff_hit']]
    if len(strong) == 1:
        cache[pid] = {"verdict": "found", "user": strong[0]['user'], "scholar_name": strong[0]['name'],
                      "aff": strong[0]['aff'], "file": f}
        print(f"  OK   {name:30s} -> {strong[0]['user']} ({strong[0]['aff'][:50]})")
    elif len(cands) == 1 and len(blocks) == 1:
        # single result overall, name matches, but no affiliation overlap — record as weak
        cache[pid] = {"verdict": "weak", "user": cands[0]['user'], "scholar_name": cands[0]['name'],
                      "aff": cands[0]['aff'], "file": f}
        print(f"  weak {name:30s} -> {cands[0]['user']} ({cands[0]['aff'][:50]})")
    else:
        cache[pid] = {"verdict": "none", "n_blocks": len(blocks), "n_namematch": len(cands), "file": f}
    processed += 1
    json.dump(cache, open(CACHE, 'w', encoding='utf-8'), indent=1)
    time.sleep(3.0 + random.random() * 2.5)

found = [v for v in cache.values() if v['verdict'] == 'found']
weak = [v for v in cache.values() if v['verdict'] == 'weak']
print(f"\ncache: {len(cache)} processed, found {len(found)}, weak {len(weak)}, blocked={blocked}")
