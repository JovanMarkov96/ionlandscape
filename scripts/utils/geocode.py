#!/usr/bin/env python3
"""Phase 3 — geocode institutions and companies to campus/building precision via
Nominatim (OpenStreetMap). Cached, rate-limited (1 req/sec), sanity-checked so a
wrong-country match can never overwrite a good point.

Writes back to MD frontmatter:
  location.lat / location.lon  (upgraded)
  location.precision = "campus"
  location.geocode_source = "nominatim"
  location.geocoded_at = ISO date

Usage: python scripts/utils/geocode.py
"""
import os, glob, json, time, math, urllib.parse, urllib.request
from datetime import date
import frontmatter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INST = os.path.join(ROOT, "content", "institutions")
COMP = os.path.join(ROOT, "content", "companies")
CACHE_PATH = os.path.join(os.path.dirname(__file__), "geocode_cache.json")
UA = "quantum-landscape-geocoder/1.0 (quantum ecosystem research map)"

cache = {}
if os.path.exists(CACHE_PATH):
    try:
        cache = json.load(open(CACHE_PATH, encoding="utf-8"))
    except Exception:
        cache = {}

def save_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def haversine(a, b):
    if None in a or None in b:
        return 1e9
    R = 6371.0
    dlat = math.radians(b[0] - a[0]); dlon = math.radians(b[1] - a[1])
    x = math.sin(dlat/2)**2 + math.cos(math.radians(a[0]))*math.cos(math.radians(b[0]))*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(x))

def nominatim(query):
    if query in cache:
        return cache[query]
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": query, "format": "json", "limit": 1, "addressdetails": 0
    })
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read().decode("utf-8"))
        result = {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])} if data else None
    except Exception as e:
        result = None
        print("  geocode error:", e)
    cache[query] = result
    save_cache()
    time.sleep(1.1)  # respect Nominatim 1 req/sec
    return result

def process(dirpath, prefix):
    upgraded = skipped = failed = 0
    for fp in sorted(glob.glob(os.path.join(dirpath, "*.md"))):
        if fp.endswith(".evidence.md"):
            continue
        post = frontmatter.load(fp)
        meta = post.metadata
        if meta.get("entity_type") == "company" and prefix == "inst":
            continue
        loc = meta.get("location", {}) or {}
        name = meta.get("name", "")
        city = loc.get("city", "")
        country = loc.get("country", "")
        if not name:
            continue
        # Already campus/building precision? skip.
        if loc.get("precision") in ("campus", "building"):
            skipped += 1
            continue
        cur = (loc.get("lat"), loc.get("lon"))
        query = ", ".join([p for p in [name, city, country] if p])
        res = nominatim(query)
        if not res:
            failed += 1
            print(f"  FAIL  {name}")
            continue
        new = (res["lat"], res["lon"])
        # Sanity: if we already had coords, the campus point must be within 60km.
        if cur[0] is not None and haversine(cur, new) > 60:
            failed += 1
            print(f"  REJECT (too far {haversine(cur,new):.0f}km) {name}")
            continue
        loc["lat"] = round(new[0], 6)
        loc["lon"] = round(new[1], 6)
        loc["precision"] = "campus"
        loc["geocode_source"] = "nominatim"
        loc["geocoded_at"] = date.today().isoformat()
        meta["location"] = loc
        with open(fp, "wb") as f:
            frontmatter.dump(post, f)
        upgraded += 1
        print(f"  OK    {name} -> {loc['lat']}, {loc['lon']}")
    print(f"[{prefix}] upgraded={upgraded} skipped={skipped} failed={failed}")

print("=== Institutions ===")
process(INST, "inst")
print("=== Companies ===")
process(COMP, "comp")
print("Done")
