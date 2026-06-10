# -*- coding: utf-8 -*-
"""Pass A: for people with ORCID but missing google_scholar or group_page, pull
researcher-urls from the public ORCID API; collect scholar ids + homepage/group
candidates. Pass B: for people still unresolved, try Wikidata wbsearchentities.
Verified scholar ids are written; group candidates merged into reports/group_candidates.json."""
import glob, html, json, re, sys, time, unicodedata
import requests
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
session = requests.Session()

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z ]', ' ', s.lower()).strip()

def name_match(a, b):
    pa, pb = norm(a).split(), norm(b).split()
    return bool(pa and pb) and pa[-1] == pb[-1] and pa[0][0] == pb[0][0]

RE_PRF_NAME = re.compile(r'<div id="gsc_prf_in">(.*?)</div>', re.S)
RE_PRF_HOME = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>\s*Homepage\s*</a>', re.I)
TAGS = re.compile(r'<[^>]+>')

def fetch_profile(user):
    try:
        r = session.get(f"https://scholar.google.com/citations?user={user}&hl=en", headers=UA, timeout=25)
    except Exception:
        return None
    if r.status_code != 200 or 'gsc_prf_in' not in r.text:
        return None
    nm = html.unescape(TAGS.sub('', RE_PRF_NAME.search(r.text).group(1)).strip())
    hm = RE_PRF_HOME.search(r.text)
    return {"name": nm, "home": html.unescape(hm.group(1)) if hm else None}

files = {}
for f in sorted(glob.glob('content/people/*.md')):
    if f.endswith('.evidence.md'):
        continue
    fm = yaml.safe_load(open(f, encoding='utf-8').read().split('---')[1])
    if fm.get('stub') or str(fm.get('id', '')).startswith('000-'):
        continue
    files[fm['id']] = (f, fm)

group_cand = json.load(open('reports/group_candidates.json', encoding='utf-8'))
stats = {"orcid_checked": 0, "scholar_from_orcid": 0, "group_from_orcid": 0,
         "wd_search_hits": 0, "scholar_from_wd2": 0, "orcid_from_wd2": 0}

GROUPISH = re.compile(r'(group|lab|labs|team|research)', re.I)
SCHOLAR_RE = re.compile(r'scholar\.google\.[a-z.]+/citations\?.*user=([\w-]+)')

# ---------- Pass A: ORCID researcher-urls ----------
applied_scholar = []
for pid, (f, fm) in files.items():
    links = fm.get('links') or {}
    orcid = links.get('orcid')
    need_gs = not links.get('google_scholar')
    need_gp = not links.get('group_page') and pid not in group_cand
    if not orcid or not (need_gs or need_gp):
        continue
    oid = orcid.rstrip('/').rsplit('/', 1)[-1]
    try:
        r = session.get(f"https://pub.orcid.org/v3.0/{oid}/researcher-urls",
                        headers={**UA, "Accept": "application/json"}, timeout=25)
        urls = [(u.get('url-name') or '', (u.get('url') or {}).get('value') or '')
                for u in r.json().get('researcher-url', [])]
    except Exception:
        continue
    stats["orcid_checked"] += 1
    for label, u in urls:
        m = SCHOLAR_RE.search(u)
        if m and need_gs:
            user = m.group(1)
            prof = fetch_profile(user)
            time.sleep(1.0)
            if prof and name_match(fm['name'], prof['name']):
                gs_url = f"https://scholar.google.com/citations?user={user}"
                raw = open(f, encoding='utf-8').read()
                mm = re.search(r'^links:\n', raw, re.M)
                raw = raw[:mm.end()] + f"  google_scholar: {gs_url}\n" + raw[mm.end():]
                open(f, 'w', encoding='utf-8').write(raw)
                stats["scholar_from_orcid"] += 1
                applied_scholar.append(pid)
                need_gs = False
                if prof.get('home') and need_gp:
                    group_cand[pid] = prof['home']
                    stats["group_from_orcid"] += 1
                    need_gp = False
        elif need_gp and u.startswith('http') and 'scholar.google' not in u and 'orcid' not in u:
            if GROUPISH.search(label) or GROUPISH.search(u):
                group_cand[pid] = u
                stats["group_from_orcid"] += 1
                need_gp = False
    time.sleep(0.3)

# ---------- Pass B: Wikidata wbsearchentities for still-missing scholar ----------
wd = json.load(open('reports/wikidata_people.json', encoding='utf-8'))
for pid, (f, fm) in files.items():
    fm = yaml.safe_load(open(f, encoding='utf-8').read().split('---')[1])
    links = fm.get('links') or {}
    if links.get('google_scholar') or pid in wd:
        continue
    name = fm['name']
    try:
        r = session.get("https://www.wikidata.org/w/api.php",
                        params={"action": "wbsearchentities", "search": name, "language": "en",
                                "type": "item", "limit": 5, "format": "json"},
                        headers=UA, timeout=20)
        hits = r.json().get('search', [])
    except Exception:
        continue
    qid = None
    for h in hits:
        desc = (h.get('description') or '').lower()
        if any(w in desc for w in ('physicist', 'scientist', 'researcher', 'professor', 'chemist', 'engineer')):
            if name_match(name, h.get('label', '')):
                qid = h['id']
                break
    if not qid:
        continue
    stats["wd_search_hits"] += 1
    try:
        r = session.get(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json", headers=UA, timeout=25)
        ent = r.json()['entities'][qid]
        claims = ent.get('claims', {})
    except Exception:
        continue
    def claim(prop):
        c = claims.get(prop)
        return c[0]['mainsnak']['datavalue']['value'] if c and c[0]['mainsnak'].get('datavalue') else None
    scholar = claim('P1960')
    orc = claim('P496')
    raw = open(f, encoding='utf-8').read()
    add = []
    if scholar:
        prof = fetch_profile(scholar)
        time.sleep(1.0)
        if prof and name_match(name, prof['name']):
            add.append(f"  google_scholar: https://scholar.google.com/citations?user={scholar}\n")
            stats["scholar_from_wd2"] += 1
            if prof.get('home') and not links.get('group_page') and pid not in group_cand:
                group_cand[pid] = prof['home']
    if orc and not links.get('orcid'):
        add.append(f"  orcid: https://orcid.org/{orc}\n")
        stats["orcid_from_wd2"] += 1
    if add:
        mm = re.search(r'^links:\n', raw, re.M)
        if mm:
            raw = raw[:mm.end()] + ''.join(add) + raw[mm.end():]
            open(f, 'w', encoding='utf-8').write(raw)
    time.sleep(0.4)

json.dump(group_cand, open('reports/group_candidates.json', 'w', encoding='utf-8'), indent=1)
print(stats)
print(f"group candidates now: {len(group_cand)}")
