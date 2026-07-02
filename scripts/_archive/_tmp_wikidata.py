# -*- coding: utf-8 -*-
"""Batch-resolve people via Wikidata SPARQL: Google Scholar id (P1960), ORCID (P496),
official website (P856), English Wikipedia sitelink. Saves reports/wikidata_people.json."""
import glob, json, sys, time, unicodedata, re
import requests
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "quantum-landscape-enrichment/1.0 (ozerilab@weizmann.ac.il)"}
SPARQL = "https://query.wikidata.org/sparql"

people = []
for f in sorted(glob.glob('content/people/*.md')):
    if f.endswith('.evidence.md'):
        continue
    fm = yaml.safe_load(open(f, encoding='utf-8').read().split('---')[1])
    if fm.get('stub') or str(fm.get('id', '')).startswith('000-'):
        continue
    people.append((f, fm))
print(f"{len(people)} non-stub people")

def esc(s):
    return s.replace('\\', '').replace('"', '')

out = {}
CHUNK = 40
names = [(fm['id'], fm['name'], f) for f, fm in people]
for i in range(0, len(names), CHUNK):
    chunk = names[i:i+CHUNK]
    values = ' '.join(f'"{esc(n)}"@en' for _, n, _ in chunk)
    q = f"""
SELECT ?name ?item ?scholar ?orcid ?website ?enwiki ?occLabel WHERE {{
  VALUES ?name {{ {values} }}
  ?item rdfs:label|skos:altLabel ?name .
  ?item wdt:P31 wd:Q5 .
  OPTIONAL {{ ?item wdt:P1960 ?scholar . }}
  OPTIONAL {{ ?item wdt:P496 ?orcid . }}
  OPTIONAL {{ ?item wdt:P856 ?website . }}
  OPTIONAL {{ ?enwiki schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> . }}
  OPTIONAL {{ ?item wdt:P106 ?occ . ?occ rdfs:label ?occLabel . FILTER(LANG(?occLabel)='en') }}
}}"""
    try:
        r = requests.get(SPARQL, params={'query': q, 'format': 'json'}, headers=UA, timeout=120)
        rows = r.json()['results']['bindings']
    except Exception as e:
        print(f"  chunk {i}: ERR {e}")
        time.sleep(5)
        continue
    for row in rows:
        nm = row['name']['value']
        rec = out.setdefault(nm, {'items': {}})
        qid = row['item']['value'].rsplit('/', 1)[-1]
        it = rec['items'].setdefault(qid, {'occs': set()})
        for k in ('scholar', 'orcid', 'website', 'enwiki'):
            if k in row:
                it[k] = row[k]['value']
        if 'occLabel' in row:
            it['occs'].add(row['occLabel']['value'])
    print(f"  chunk {i//CHUNK+1}/{(len(names)+CHUNK-1)//CHUNK}: {len(rows)} rows")
    time.sleep(1.5)

# disambiguate: prefer items whose occupations look like physicist/scientist
SCI = {'physicist', 'scientist', 'researcher', 'university teacher', 'chemist', 'engineer',
       'quantum physicist', 'professor', 'academic', 'computer scientist'}
resolved = {}
for pid, nm, f in names:
    rec = out.get(nm)
    if not rec:
        continue
    items = []
    for qid, it in rec['items'].items():
        sci = bool(it['occs'] & SCI)
        items.append((qid, it, sci))
    sci_items = [x for x in items if x[2]]
    pick = None
    if len(sci_items) == 1:
        pick = sci_items[0]
    elif len(items) == 1:
        pick = items[0]
    if pick:
        qid, it, sci = pick
        resolved[pid] = {'qid': qid, 'sci': sci, 'file': f,
                         'scholar': it.get('scholar'), 'orcid': it.get('orcid'),
                         'website': it.get('website'), 'enwiki': it.get('enwiki')}

js = {k: v for k, v in resolved.items()}
json.dump(js, open('reports/wikidata_people.json', 'w', encoding='utf-8'), indent=1)
n_sch = sum(1 for v in resolved.values() if v['scholar'])
n_orc = sum(1 for v in resolved.values() if v['orcid'])
n_web = sum(1 for v in resolved.values() if v['website'])
n_wiki = sum(1 for v in resolved.values() if v['enwiki'])
print(f"\nresolved {len(resolved)} people: scholar={n_sch}, orcid={n_orc}, website={n_web}, enwiki={n_wiki}")
