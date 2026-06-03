# -*- coding: utf-8 -*-
"""Find VERIFIED links for trapped-ion researchers via the ORCID public API.
Match candidates by affiliation, then take the ORCID iD plus any homepage /
Google Scholar URLs the researcher self-listed on their own ORCID record.
Only adds links that are missing; never overwrites an existing one. Logs all
decisions for review."""
import io, re, sys, time, unicodedata, glob
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
from pathlib import Path
import frontmatter, requests

ROOT = Path(r"d:/OneDrive - weizmann.ac.il/GitHub/ionlandscape")
PD = ROOT / "content" / "people"
S = requests.Session()
S.headers.update({"User-Agent": "ionlandscape-link-bot/1.0 (research map)",
                  "Accept": "application/json"})

STOP = {"university","institute","institut","technology","science","sciences","of","for",
        "the","and","national","center","centre","research","physics","quantum","de","la",
        "college","laboratory","lab","department","school","faculty","gmbh","inc","ltd",
        "joint","advanced","applied","engineering","standards","gutenberg","johannes"}

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", " ", s)

def distinctive(s):
    return {t for t in norm(s).split() if len(t) > 4 and t not in STOP}

def person_inst_tokens(m):
    toks = set()
    cp = m.get("current_position") or {}
    if isinstance(cp, dict) and cp.get("institution"): toks |= distinctive(cp["institution"])
    for e in (m.get("education") or []):
        if isinstance(e,dict) and e.get("institution"): toks |= distinctive(e["institution"])
    for e in (m.get("postdocs") or []):
        if isinstance(e,dict) and e.get("institution"): toks |= distinctive(e["institution"])
    for a in (m.get("affiliations") or []):
        if isinstance(a,dict) and a.get("name"): toks |= distinctive(a["name"])
    return toks

def split_name(name):
    n = re.sub(r"\b(Dr|Prof|Professor|Sir)\.?\b", "", name).strip()
    parts = [p for p in n.split() if p]
    if len(parts) < 2: return None, None
    given = parts[0]
    family = parts[-1]
    return given, family

def orcid_search(given, family):
    try:
        q = f'given-names:{given} AND family-name:{family}'
        r = S.get("https://pub.orcid.org/v3.0/expanded-search/",
                  params={"q": q, "rows": 15}, timeout=25)
        if r.status_code >= 400: return []
        return r.json().get("expanded-result") or []
    except Exception as e:
        print("  search err", e); return []

def researcher_urls(orcid):
    try:
        r = S.get(f"https://pub.orcid.org/v3.0/{orcid}/researcher-urls", timeout=25)
        if r.status_code >= 400: return []
        out = []
        for u in r.json().get("researcher-url") or []:
            name = (u.get("url-name") or "").lower()
            url = ((u.get("url") or {}).get("value") or "")
            if url: out.append((name, url))
        return out
    except Exception:
        return []

def classify(name, url):
    low = (name + " " + url).lower()
    if "scholar.google" in url: return "google_scholar"
    if "orcid.org" in url: return None
    if "google" in low and "scholar" in low: return "google_scholar"
    if any(k in low for k in ("group","lab","team")): return "group_page"
    if any(k in low for k in ("home","personal","website","page","profile")): return "homepage"
    return "homepage"

log = []
added_orcid = added_other = 0
files = [f for f in sorted(glob.glob(str(PD/"*.md"))) if not f.endswith(".evidence.md")]
for f in files:
    post = frontmatter.load(f); m = post.metadata
    if "trapped_ion" not in (m.get("platforms") or []): continue
    name = m.get("name",""); given, family = split_name(name)
    if not family: continue
    links = m.get("links") or {}
    if links.get("orcid"):  # already has a (validated) ORCID — skip lookup
        continue
    itoks = person_inst_tokens(m)
    cands = orcid_search(given, family)
    match = None
    for c in cands:
        cinst = " ".join(c.get("institution-name") or [])
        ctoks = distinctive(cinst)
        gn = norm(c.get("given-names") or ""); fn = norm(c.get("family-names") or "")
        name_ok = family.lower() in fn or fn in norm(family) or given.lower()[:4] in gn
        if name_ok and itoks & ctoks:
            match = c; break
    if not match:
        log.append(f"SKIP {m.get('id')} ({name}) — no affiliation-matched ORCID among {len(cands)} candidates")
        time.sleep(0.2); continue
    orcid = match.get("orcid-id")
    links["orcid"] = f"https://orcid.org/{orcid}"
    added_orcid += 1
    extras = []
    for uname, url in researcher_urls(orcid):
        kind = classify(uname, url)
        if kind and not links.get(kind):
            links[kind] = url; extras.append(kind); added_other += 1
    post["links"] = links
    # evidence
    ev = Path(f.replace(".md",".evidence.md"))
    note = f"Verified ORCID {orcid} matched by affiliation ({' '.join(match.get('institution-name') or [])}); links added: orcid" + ("," + ",".join(extras) if extras else "") + " [2026-06-03 link sweep]."
    et = ev.read_text(encoding="utf-8") if ev.exists() else "---\n---\n\n# Evidence Map\n\n## Sources\n"
    if "## Sources" not in et: et = et.rstrip()+"\n\n## Sources\n"
    ev.write_text(et.rstrip()+"\n- "+note+"\n", encoding="utf-8")
    io.open(f,"w",encoding="utf-8").write(frontmatter.dumps(post)+"\n")
    log.append(f"OK   {m.get('id')} ({name}) -> {orcid} | extras: {extras} | inst: {' '.join(match.get('institution-name') or [])[:60]}")
    time.sleep(0.25)

io.open(ROOT/"orcid_log.txt","w",encoding="utf-8").write(
    f"added ORCID: {added_orcid}, added homepage/scholar: {added_other}\n"+"\n".join(log))
print(f"added ORCID: {added_orcid}, added other: {added_other}")
