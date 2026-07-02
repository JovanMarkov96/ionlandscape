# -*- coding: utf-8 -*-
"""Re-check failing URLs with retries/backoff + http fallback; for persistent 404s
query the Wayback availability API. Writes reports/linkcheck_confirmed.json."""
import json, sys, time
import requests
import urllib3
urllib3.disable_warnings()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}

rep = json.load(open('reports/linkcheck.json', encoding='utf-8'))
fails = sorted({e['url'] for e in rep['entries'] if e['status'] in ('broken', 'ssl', 'timeout')})
print(f"re-checking {len(fails)} URLs")

def try_get(url, timeout=25):
    try:
        r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True, verify=False)
        return r.status_code, r.url
    except requests.exceptions.SSLError:
        return 'ssl', None
    except requests.exceptions.ConnectionError as e:
        return 'conn', None
    except requests.exceptions.Timeout:
        return 'timeout', None
    except Exception as e:
        return 'err', None

confirmed = {}
for u in fails:
    statuses = []
    final = None
    for attempt in range(3):
        code, fin = try_get(u)
        statuses.append(code)
        if isinstance(code, int) and code < 400:
            final = fin
            break
        time.sleep(1.5)
    if isinstance(statuses[-1], int) and statuses[-1] < 400:
        confirmed[u] = {"verdict": "ok_on_retry", "final": final}
        continue
    # http fallback for ssl/conn
    if statuses[-1] in ('ssl', 'conn', 'timeout') and u.startswith('https://'):
        code, fin = try_get('http://' + u[8:])
        if isinstance(code, int) and code < 400:
            confirmed[u] = {"verdict": "http_ok", "final": fin}
            continue
    # wayback availability
    wb = None
    try:
        r = requests.get('https://archive.org/wayback/available', params={'url': u}, timeout=20)
        snap = r.json().get('archived_snapshots', {}).get('closest', {})
        if snap.get('available'):
            wb = snap.get('url')
    except Exception:
        pass
    confirmed[u] = {"verdict": "dead", "last": str(statuses[-1]), "wayback": wb}
    print(f"  DEAD ({statuses[-1]}): {u[:100]}" + (f"  [wayback ok]" if wb else ""))

json.dump(confirmed, open('reports/linkcheck_confirmed.json', 'w', encoding='utf-8'), indent=1)
ok = sum(1 for v in confirmed.values() if v['verdict'] != 'dead')
print(f"\n{ok} recovered on retry, {len(confirmed)-ok} confirmed dead")
