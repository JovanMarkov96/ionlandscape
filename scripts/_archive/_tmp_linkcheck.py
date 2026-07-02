# -*- coding: utf-8 -*-
"""Check all profile URLs (links + sources) across people/companies/institutions.
Classifies: ok / broken (404,410,DNS,conn) / blocked (403,429,5xx) / timeout / ssl.
Writes reports/linkcheck.json with per-URL detail incl. redirect targets."""
import glob, json, re, sys, yaml, concurrent.futures as cf
import requests
import urllib3
urllib3.disable_warnings()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

entries = []  # (file, field, url)
for pattern in ['content/people/*.md', 'content/companies/*.md', 'content/institutions/*.md']:
    for f in sorted(glob.glob(pattern)):
        if f.endswith('.evidence.md'):
            continue
        try:
            fm = yaml.safe_load(open(f, encoding='utf-8').read().split('---')[1])
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        for k, v in (fm.get('links') or {}).items():
            if isinstance(v, str) and v.startswith('http'):
                entries.append((f, 'links.' + k, v))
        for i, src in enumerate(fm.get('sources') or []):
            u = src.get('url') if isinstance(src, dict) else None
            if u and u.startswith('http'):
                entries.append((f, f'sources.{i}', u))

# de-dup by URL for checking
urls = sorted({u for _, _, u in entries})
print(f"{len(entries)} link references, {len(urls)} unique URLs")

def check(url):
    try:
        r = requests.get(url, headers=UA, timeout=15, allow_redirects=True, stream=True, verify=False)
        final = r.url
        code = r.status_code
        r.close()
        if code in (404, 410):
            return {"url": url, "status": "broken", "code": code, "final": final}
        if code in (401, 403, 429) or 500 <= code < 600:
            return {"url": url, "status": "blocked", "code": code, "final": final}
        if code >= 400:
            return {"url": url, "status": "broken", "code": code, "final": final}
        return {"url": url, "status": "ok", "code": code, "final": final}
    except requests.exceptions.SSLError as e:
        return {"url": url, "status": "ssl", "err": str(e)[:120]}
    except requests.exceptions.ConnectionError as e:
        s = str(e)
        kind = "dns" if ("getaddrinfo" in s or "NameResolution" in s) else "conn"
        return {"url": url, "status": "broken", "err": kind}
    except requests.exceptions.Timeout:
        return {"url": url, "status": "timeout"}
    except Exception as e:
        return {"url": url, "status": "error", "err": str(e)[:120]}

results = {}
with cf.ThreadPoolExecutor(max_workers=24) as ex:
    for i, res in enumerate(ex.map(check, urls)):
        results[res["url"]] = res
        if (i + 1) % 200 == 0:
            print(f"  {i+1}/{len(urls)}")

by_status = {}
for r in results.values():
    by_status.setdefault(r["status"], []).append(r)
print({k: len(v) for k, v in sorted(by_status.items())})

report = {"entries": [{"file": f, "field": fld, "url": u, **results[u]} for f, fld, u in entries]}
json.dump(report, open('reports/linkcheck.json', 'w', encoding='utf-8'), indent=1)
print("wrote reports/linkcheck.json")
# print broken summary grouped by file-type
for st in ('broken', 'ssl', 'timeout', 'error'):
    rows = [e for e in report["entries"] if e["status"] == st]
    print(f"\n== {st}: {len(rows)} refs ==")
    for e in rows[:60]:
        print(f"  {e['file'].split('/')[-1] if '/' in e['file'] else e['file']} | {e['field']} | {e['url'][:90]} | {e.get('code', e.get('err',''))}")
