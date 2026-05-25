#!/usr/bin/env python3
"""Phase 4 — enrich stub people with a current institution from Wikipedia's
infobox (sourced). Batches up to 50 page titles per API request to stay well
within rate limits. Prefers an institution already in our dataset (so the person
cross-links and inherits coordinates); otherwise records the most-recent
institution Wikipedia lists. Unmatched stubs are reported, not modified.
"""
import os, glob, re, json, time, unicodedata, urllib.parse, urllib.request, sys
import frontmatter

def sprint(*args):
    msg = " ".join(str(a) for a in args)
    sys.stdout.write(msg.encode("ascii", "replace").decode("ascii") + "\n")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PEOPLE = os.path.join(ROOT, "content", "people")
INST_JSON = os.path.join(ROOT, "website", "static", "data", "institutions.json")
UA = "ionlandscape-research/1.0 (https://q-factor.com; academic ecosystem map)"

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ASCII', 'ignore').decode('ASCII')
    return re.sub(r'\s+', ' ', re.sub(r'[().,\-–—/]', ' ', s.lower())).strip()

insts = json.load(open(INST_JSON, encoding="utf-8"))
inst_keys = {}
for i in insts:
    for k in [i.get("name")] + (i.get("aliases") or []) + (i.get("abbreviations") or []):
        if k:
            inst_keys[norm(k)] = i["name"]

def match_our_inst(wp_inst):
    n = norm(wp_inst)
    if n in inst_keys:
        return inst_keys[n]
    for k, name in inst_keys.items():
        if len(k) > 6 and (k in n or n in k):
            return name
    return None

def extract_institutions(wikitext):
    m = re.search(r'\|\s*(?:institutions|workplaces)\s*=\s*(.+)', wikitext or '', re.I)
    if not m:
        return []
    raw = m.group(1)
    links = re.findall(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]', raw)
    return [l.strip() for l in links if l.strip()]

def fetch_batch(titles):
    """Return {title: wikitext} for a batch of <=50 titles (full lead content)."""
    params = {
        "action": "query", "prop": "revisions", "rvprop": "content",
        "rvslots": "main", "format": "json", "redirects": "1",
        "titles": "|".join(titles),
    }
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        d = json.loads(r.read().decode("utf-8"))
    # Map redirects/normalizations back
    title_map = {}
    for n in d.get("query", {}).get("normalized", []):
        title_map[n["from"]] = n["to"]
    for n in d.get("query", {}).get("redirects", []):
        title_map[n["from"]] = n["to"]
    resolved = {}
    for pg in d.get("query", {}).get("pages", {}).values():
        if "missing" in pg or not pg.get("revisions"):
            continue
        rev = pg["revisions"][0]
        txt = rev.get("slots", {}).get("main", {}).get("*") or rev.get("*", "")
        resolved[pg["title"]] = txt
    def lookup(t):
        cur = t
        for _ in range(3):
            if cur in resolved:
                return resolved[cur]
            cur = title_map.get(cur, cur)
        return resolved.get(cur)
    return {t: lookup(t) for t in titles}

def main():
    stubs = []
    for fp in sorted(glob.glob(os.path.join(PEOPLE, "*.md"))):
        if fp.endswith(".evidence.md"):
            continue
        post = frontmatter.load(fp)
        meta = post.metadata
        if not meta.get("stub"):
            continue
        if (meta.get("current_position") or {}).get("institution"):
            continue
        stubs.append((fp, post))

    names = [p.metadata.get("name", "") for _, p in stubs]
    wiki = {}
    for i in range(0, len(names), 6):
        batch = [n for n in names[i:i+6] if n]
        try:
            wiki.update(fetch_batch(batch))
            sprint(f"  fetched batch {i//6+1} ({len(batch)} titles)")
        except Exception as e:
            sprint("  batch error:", e)
        time.sleep(2.0)

    enriched = matched_ours = no_wiki = 0
    report = []
    for fp, post in stubs:
        meta = post.metadata
        name = meta.get("name", "")
        txt = wiki.get(name)
        wp = extract_institutions(txt) if txt else []
        if not wp:
            no_wiki += 1
            report.append(f"- {name}")
            continue
        chosen = None
        for cand in reversed(wp):
            m = match_our_inst(cand)
            if m:
                chosen = m; matched_ours += 1; break
        if not chosen:
            chosen = wp[-1]
        cp = meta.get("current_position") or {}
        meta["current_position"] = {"institution": chosen, "title": cp.get("title", "")}
        srcs = meta.get("sources", []) or []
        wiki_url = "https://en.wikipedia.org/wiki/" + name.replace(" ", "_")
        if not any(s.get("url") == wiki_url for s in srcs):
            srcs.append({"note": "Affiliation from Wikipedia infobox", "url": wiki_url})
        meta["sources"] = srcs
        with open(fp, "wb") as f:
            frontmatter.dump(post, f)
        enriched += 1
        sprint(f"  {name} -> {chosen}")

    sprint(f"\nEnriched: {enriched} ({matched_ours} matched our dataset)")
    sprint(f"No Wikipedia institutions field: {no_wiki}")
    if report:
        rpt = os.path.join(ROOT, "reports", "people_needing_institution.md")
        os.makedirs(os.path.dirname(rpt), exist_ok=True)
        with open(rpt, "w", encoding="utf-8") as f:
            f.write("# Stub people still needing an institution (manual/source pass)\n\n" + "\n".join(report) + "\n")
        sprint("Report:", rpt)

if __name__ == "__main__":
    main()
