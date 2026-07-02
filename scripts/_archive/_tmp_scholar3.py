# -*- coding: utf-8 -*-
"""Scholar discovery v2: DDG html search -> candidate user ids -> verify by fetching
the Scholar profile (name match + affiliation/email overlap). Harvests the profile's
verified homepage as a group-page candidate. Restartable via reports/scholar_cache2.json."""
import glob, html, json, os, random, re, sys, time, unicodedata
import requests
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}
CACHE = 'reports/scholar_cache3.json'
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

GENERIC = {'university', 'institute', 'national', 'center', 'centre', 'technology', 'institut',
           'laboratory', 'college', 'department', 'research', 'sciences', 'science', 'group',
           'physics', 'quantum'}

def inst_tokens(fm):
    toks = set()
    cp = fm.get('current_position') or {}
    names = [cp.get('institution')] + [a.get('name') for a in (fm.get('affiliations') or []) if isinstance(a, dict)]
    for nm in names:
        if nm:
            for w in norm(nm).split():
                if len(w) > 4 and w not in GENERIC:
                    toks.add(w)
    return toks

targets = []
for f in sorted(glob.glob('content/people/*.md')):
    if f.endswith('.evidence.md'):
        continue
    fm = yaml.safe_load(open(f, encoding='utf-8').read().split('---')[1])
    if fm.get('stub') or str(fm.get('id', '')).startswith('000-'):
        continue
    gs = (fm.get('links') or {}).get('google_scholar')
    if gs and 'q3Yb14' not in gs:   # include Pan whose stored id is dead
        continue
    targets.append((f, fm))
# process the site's core platform first
targets.sort(key=lambda t: 0 if 'trapped_ion' in (t[1].get('platforms') or []) else 1)
print(f"{len(targets)} targets; {len(cache)} cached")

session = requests.Session()
RE_DDG = re.compile(r'result__a[^>]+href="([^"]+)"')
RE_PRF_NAME = re.compile(r'<div id="gsc_prf_in">(.*?)</div>', re.S)
RE_PRF_AFF = re.compile(r'class="gsc_prf_il"[^>]*>(.*?)</div>', re.S)
RE_PRF_HOME = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>\s*Homepage\s*</a>', re.I)
TAGS = re.compile(r'<[^>]+>')

def fetch_profile(user):
    url = f"https://scholar.google.com/citations?user={user}&hl=en"
    try:
        r = session.get(url, headers=UA, timeout=25)
    except Exception:
        return None
    if r.status_code != 200 or 'gsc_prf_in' not in r.text:
        return None
    name = TAGS.sub('', RE_PRF_NAME.search(r.text).group(1)).strip()
    affs = [html.unescape(TAGS.sub('', m)) for m in RE_PRF_AFF.findall(r.text)]
    home = RE_PRF_HOME.search(r.text)
    return {"name": html.unescape(name), "affs": affs, "home": html.unescape(home.group(1)) if home else None, "url": url}

ddg_fail = 0
processed = 0
for f, fm in targets:
    pid = fm['id']
    if pid in cache:
        continue
    if ddg_fail >= 8:
        print("too many DDG failures — stopping")
        break
    name = fm['name']
    try:
        r = session.get("https://search.brave.com/search",
                        params={"q": f'site:scholar.google.com "{name}"'},
                        headers=UA, timeout=25)
    except Exception as e:
        ddg_fail += 1
        time.sleep(20)
        continue
    if r.status_code in (403, 429):
        ddg_fail += 1
        print(f"  Brave throttle at {name} (fail {ddg_fail})")
        time.sleep(90)
        continue
    ddg_fail = 0
    ids = list(dict.fromkeys(re.findall(r'scholar\.google\.[a-z.]+/citations\?[^"&]*user=([\w-]+)', r.text)))
    if not ids:
        cache[pid] = {"verdict": "no_results", "file": f}
        json.dump(cache, open(CACHE, 'w', encoding='utf-8'), indent=1)
        processed += 1
        time.sleep(12 + random.random() * 6)
        continue
    verdict = {"verdict": "none", "file": f, "checked": ids[:3]}
    toks = inst_tokens(fm)
    for user in ids[:3]:
        time.sleep(1.5 + random.random())
        prof = fetch_profile(user)
        if not prof:
            continue
        if not name_match(name, prof['name']):
            continue
        hay = norm(' '.join(prof['affs']))
        if any(t in hay for t in toks):
            verdict = {"verdict": "found", "user": user, "scholar_name": prof['name'],
                       "aff": prof['affs'][:2], "home": prof['home'], "file": f}
            print(f"  OK   {name:28s} -> {user}  ({(prof['affs'] or [''])[0][:48]})" + ("  [home]" if prof['home'] else ""))
            break
        else:
            # name matches but affiliation doesn't — record best weak candidate
            if verdict["verdict"] == "none":
                verdict = {"verdict": "weak", "user": user, "scholar_name": prof['name'],
                           "aff": prof['affs'][:2], "home": prof['home'], "file": f}
    if verdict['verdict'] == 'weak':
        print(f"  weak {name:28s} -> {verdict['user']}  ({(verdict['aff'] or [''])[0][:48]})")
    cache[pid] = verdict
    json.dump(cache, open(CACHE, 'w', encoding='utf-8'), indent=1)
    processed += 1
    time.sleep(12 + random.random() * 6)

found = [v for v in cache.values() if v['verdict'] == 'found']
weak = [v for v in cache.values() if v['verdict'] == 'weak']
print(f"\nprocessed {processed} this run; total cache {len(cache)}: found {len(found)}, weak {len(weak)}")
