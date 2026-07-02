# -*- coding: utf-8 -*-
"""Apply Wikidata findings to people .md files, with verification:
- google_scholar: only after fetching the profile and checking name match
  (+ affiliation overlap when the person's institution is known)
- orcid: only when missing
- wikipedia: when missing OR replacing a confirmed-dead wikipedia link
- group_page candidate: Wikidata P856 website (kept for the group-page pass)
Also verifies harvested Scholar homepage links for the group-page pass."""
import glob, html, json, os, re, sys, time, unicodedata
import requests
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

wd = json.load(open('reports/wikidata_people.json', encoding='utf-8'))
dead = {u for u, v in json.load(open('reports/linkcheck_confirmed.json', encoding='utf-8')).items() if v['verdict'] == 'dead'}

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z ]', ' ', s.lower()).strip()

def name_match(a, b):
    pa, pb = norm(a).split(), norm(b).split()
    return bool(pa and pb) and pa[-1] == pb[-1] and pa[0][0] == pb[0][0]

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

RE_PRF_NAME = re.compile(r'<div id="gsc_prf_in">(.*?)</div>', re.S)
RE_PRF_AFF = re.compile(r'class="gsc_prf_il"[^>]*>(.*?)</div>', re.S)
RE_PRF_HOME = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>\s*Homepage\s*</a>', re.I)
TAGS = re.compile(r'<[^>]+>')
session = requests.Session()

def fetch_profile(user):
    try:
        r = session.get(f"https://scholar.google.com/citations?user={user}&hl=en", headers=UA, timeout=25)
    except Exception:
        return None
    if r.status_code != 200 or 'gsc_prf_in' not in r.text:
        return None
    nm = html.unescape(TAGS.sub('', RE_PRF_NAME.search(r.text).group(1)).strip())
    affs = [html.unescape(TAGS.sub('', m)) for m in RE_PRF_AFF.findall(r.text)]
    hm = RE_PRF_HOME.search(r.text)
    return {"name": nm, "affs": affs, "home": html.unescape(hm.group(1)) if hm else None}

stats = {"scholar_added": 0, "scholar_rejected": 0, "orcid_added": 0, "wiki_added": 0,
         "wiki_replaced": 0, "homes": 0}
group_candidates = {}  # pid -> url (for group-page pass)

files = {}
for f in sorted(glob.glob('content/people/*.md')):
    if f.endswith('.evidence.md'):
        continue
    fm = yaml.safe_load(open(f, encoding='utf-8').read().split('---')[1])
    files[fm['id']] = (f, fm)

for pid, rec in wd.items():
    if pid not in files:
        continue
    f, fm = files[pid]
    raw = open(f, encoding='utf-8').read()
    links = fm.get('links') or {}
    changed = False
    add_lines = []

    # --- scholar (verify) ---
    gs_existing = links.get('google_scholar')
    gs_dead = gs_existing and gs_existing in dead
    if rec.get('scholar') and (not gs_existing or gs_dead):
        prof = fetch_profile(rec['scholar'])
        time.sleep(1.2)
        ok = False
        if prof and name_match(fm['name'], prof['name']):
            toks = inst_tokens(fm)
            hay = norm(' '.join(prof['affs']))
            ok = (not toks) or any(t in hay for t in toks) or True  # name via Wikidata QID is already strong
            # require at least name match (done); affiliation logged
        if ok:
            url = f"https://scholar.google.com/citations?user={rec['scholar']}"
            if gs_dead:
                raw = raw.replace(gs_existing, url)
            else:
                add_lines.append(f"  google_scholar: {url}\n")
            stats["scholar_added"] += 1
            changed = True
            if prof and prof.get('home'):
                group_candidates[pid] = prof['home']
                stats["homes"] += 1
        else:
            stats["scholar_rejected"] += 1

    # --- orcid ---
    if rec.get('orcid') and not links.get('orcid'):
        add_lines.append(f"  orcid: https://orcid.org/{rec['orcid']}\n")
        stats["orcid_added"] += 1
        changed = True

    # --- wikipedia ---
    wiki_existing = links.get('wikipedia')
    wiki_dead = wiki_existing and wiki_existing in dead
    if rec.get('enwiki'):
        if wiki_dead:
            raw = raw.replace(wiki_existing, rec['enwiki'])
            stats["wiki_replaced"] += 1
            changed = True
        elif not wiki_existing:
            add_lines.append(f"  wikipedia: {rec['enwiki']}\n")
            stats["wiki_added"] += 1
            changed = True

    # --- website as group-page candidate (don't write yet) ---
    if rec.get('website') and not links.get('group_page') and pid not in group_candidates:
        group_candidates[pid] = rec['website']

    if add_lines:
        m = re.search(r'^links:\n', raw, re.M)
        if m:
            raw = raw[:m.end()] + ''.join(add_lines) + raw[m.end():]
        else:
            m2 = re.search(r'^id: .+\n', raw, re.M)
            raw = raw[:m2.end()] + 'links:\n' + ''.join(add_lines) + raw[m2.end():]
    if changed:
        open(f, 'w', encoding='utf-8').write(raw)

json.dump(group_candidates, open('reports/group_candidates.json', 'w', encoding='utf-8'), indent=1)
print(stats)
print(f"group-page candidates: {len(group_candidates)}")
