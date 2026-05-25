#!/usr/bin/env python3
"""
geocode.py — populate location.precision (and optionally lat/lon) for all entities.

What it does, in order:
  1. Institutions with lat/lon but no precision → set precision: city (default).
  2. Companies with lat/lon but no precision → set precision: city.
  3. People with lat/lon but no precision → set precision: city.
  4. People with no lat/lon whose current_position.institution resolves to a
     known institution with coordinates → copy those coords, set precision: inherited.
  5. Entities with city+country but no lat/lon → geocode via Nominatim,
     set precision: city, record geocode_source + geocoded_at.

What it does NOT do (future campus-level pass):
  - Find real street addresses for labs/offices.
  - Upgrade existing "city" precision entries to "campus" or "building".
  Those require web research per institution and are tracked in
  private/todo/04-geocoding.md.

Cache:  scripts/utils/geocode_cache.json  (keyed by "city||country")
Report: reports/geocode_report.md

Never overwrites a higher precision tier with a lower one.

Usage:
    python scripts/enrich/geocode.py [--dry-run] [--force]
"""

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

import frontmatter
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "content" / "people"
INSTITUTIONS_DIR = ROOT / "content" / "institutions"
COMPANIES_DIR = ROOT / "content" / "companies"
CACHE_PATH = ROOT / "scripts" / "utils" / "geocode_cache.json"
REPORT_PATH = ROOT / "reports" / "geocode_report.md"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "ionlandscape-geocoder/1.0 (mailto:ozerilab@weizmann.ac.il)"
RATE_SLEEP = 1.1  # Nominatim requires 1 req/s; add small buffer

PRECISION_RANK = {"building": 4, "campus": 3, "city": 2, "inherited": 1, "none": 0, None: -1}


# ── Cache ─────────────────────────────────────────────────────────────────────

def load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict):
    CACHE_PATH.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ── Precision helpers ─────────────────────────────────────────────────────────

def higher_precision(new: str, existing) -> bool:
    """Return True if new precision is strictly higher than existing."""
    return PRECISION_RANK.get(new, -1) > PRECISION_RANK.get(existing, -1)


# ── Nominatim ────────────────────────────────────────────────────────────────

def geocode_city(city: str, country: str, cache: dict) -> tuple | None:
    """Return (lat, lon) for city+country via Nominatim. None on miss."""
    key = f"{city.strip().lower()}||{country.strip().lower()}"
    if key in cache:
        entry = cache[key]
        if entry:
            return entry["lat"], entry["lon"]
        return None  # cached miss

    time.sleep(RATE_SLEEP)
    try:
        r = requests.get(
            NOMINATIM_URL,
            params={"q": f"{city}, {country}", "format": "json", "limit": 1},
            headers={"User-Agent": USER_AGENT},
            timeout=15,
        )
        r.raise_for_status()
        results = r.json()
        if results:
            lat = float(results[0]["lat"])
            lon = float(results[0]["lon"])
            cache[key] = {"lat": lat, "lon": lon}
            return lat, lon
        cache[key] = None  # cache the miss
        return None
    except Exception as e:
        print(f"  [warn] Nominatim error for '{city}, {country}': {e}")
        return None


# ── Institution resolver (for people inheritance) ────────────────────────────

def build_institution_lookup() -> dict:
    """
    Returns a dict mapping lowercase institution name/alias/abbreviation
    to {"lat": ..., "lon": ..., "id": ...}.
    """
    lookup = {}
    for p in INSTITUTIONS_DIR.glob("*.md"):
        if ".evidence." in p.name:
            continue
        m = frontmatter.load(p).metadata
        loc = m.get("location") or {}
        lat, lon = loc.get("lat"), loc.get("lon")
        if not lat:
            continue
        iid = m.get("id", p.stem)
        keys = [m.get("name", "")] + (m.get("aliases") or []) + (m.get("abbreviations") or [])
        for k in keys:
            if k:
                lookup[k.strip().lower()] = {"lat": lat, "lon": lon, "id": iid}
    return lookup


# ── Per-entity processor ──────────────────────────────────────────────────────

def process_entity(path: Path, entity_type: str, inst_lookup: dict,
                   cache: dict, force: bool, dry_run: bool) -> dict:
    post = frontmatter.load(path)
    meta = post.metadata
    eid = meta.get("id", path.stem)
    name = meta.get("name", eid)

    loc = dict(meta.get("location") or {})
    existing_precision = loc.get("precision")

    changes = {}
    action = "no_change"

    if loc.get("lat"):
        # Has coordinates — just stamp precision: city if missing or lower
        if higher_precision("city", existing_precision):
            changes["precision"] = "city"
            action = "precision_stamped"

    elif entity_type == "person":
        # No coordinates — try inheritance from current institution
        inst_name = (meta.get("current_position") or {}).get("institution", "")
        match = inst_lookup.get(inst_name.strip().lower()) if inst_name else None
        if match:
            changes = {"lat": match["lat"], "lon": match["lon"], "precision": "inherited"}
            action = "inherited"
        elif loc.get("city") and str(loc.get("city", "")).lower() not in ("unknown", ""):
            # Has city/country but no lat — try Nominatim
            coords = geocode_city(loc["city"], loc.get("country", ""), cache)
            if coords:
                today = date.today().isoformat()
                changes = {
                    "lat": coords[0], "lon": coords[1],
                    "precision": "city",
                    "geocode_source": "nominatim",
                    "geocoded_at": today,
                }
                action = "geocoded"
            else:
                action = "geocode_miss"
        else:
            action = "no_location_data"

    elif loc.get("city") and str(loc.get("city", "")).lower() not in ("unknown", ""):
        # Institution or company with city but no lat
        coords = geocode_city(loc["city"], loc.get("country", ""), cache)
        if coords:
            today = date.today().isoformat()
            changes = {
                "lat": coords[0], "lon": coords[1],
                "precision": "city",
                "geocode_source": "nominatim",
                "geocoded_at": today,
            }
            action = "geocoded"
        else:
            action = "geocode_miss"

    if changes and not dry_run:
        loc.update(changes)
        meta["location"] = loc
        path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")

    return {"id": eid, "name": name, "type": entity_type, "action": action, "changes": changes}


# ── Report ────────────────────────────────────────────────────────────────────

def write_report(results: list):
    by_action = {}
    for r in results:
        by_action.setdefault(r["action"], []).append(r)

    lines = [
        "# Geocoding / Precision Report",
        f"\nGenerated: {date.today().isoformat()}\n",
        f"**Precision stamped:** {len(by_action.get('precision_stamped', []))}  |  "
        f"**Inherited:** {len(by_action.get('inherited', []))}  |  "
        f"**Geocoded:** {len(by_action.get('geocoded', []))}  |  "
        f"**No change:** {len(by_action.get('no_change', []))}  |  "
        f"**No location data:** {len(by_action.get('no_location_data', []))}  |  "
        f"**Geocode miss:** {len(by_action.get('geocode_miss', []))}\n",
    ]

    if by_action.get("geocoded"):
        lines.append("\n## Geocoded (new coordinates from Nominatim)\n")
        for r in by_action["geocoded"]:
            c = r["changes"]
            lines.append(f"- {r['name']} (`{r['id']}`) → {c['lat']:.4f}, {c['lon']:.4f}")

    if by_action.get("inherited"):
        lines.append("\n## Inherited from institution\n")
        for r in by_action["inherited"]:
            c = r["changes"]
            lines.append(f"- {r['name']} (`{r['id']}`) → {c['lat']:.4f}, {c['lon']:.4f}")

    if by_action.get("geocode_miss"):
        lines.append("\n## Geocode misses (city known but Nominatim returned nothing)\n")
        for r in by_action["geocode_miss"]:
            lines.append(f"- {r['name']} (`{r['id']}`)")

    if by_action.get("no_location_data"):
        lines.append(f"\n## No location data ({len(by_action['no_location_data'])} — stays off the map)\n")
        for r in by_action["no_location_data"]:
            lines.append(f"- {r['name']} (`{r['id']}`)")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report: {REPORT_PATH}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Don't write files.")
    parser.add_argument("--force", action="store_true", help="Re-geocode even cached entries.")
    args = parser.parse_args()

    cache = load_cache()
    inst_lookup = build_institution_lookup()

    results = []
    dirs = [
        (INSTITUTIONS_DIR, "institution"),
        (COMPANIES_DIR, "company"),
        (PEOPLE_DIR, "person"),
    ]

    for content_dir, etype in dirs:
        paths = sorted(p for p in content_dir.glob("*.md") if ".evidence." not in p.name)
        print(f"\nProcessing {len(paths)} {etype}s...")
        for i, path in enumerate(paths, 1):
            r = process_entity(path, etype, inst_lookup, cache, args.force, args.dry_run)
            results.append(r)
            icon = {"precision_stamped": "p", "inherited": "i", "geocoded": "+",
                    "no_change": "-", "no_location_data": ".", "geocode_miss": "!"}
            print(f"  [{i:3d}/{len(paths)}] {icon.get(r['action'],'?')} {r['name']}  ({r['action']})")
            if i % 20 == 0:
                save_cache(cache)

    save_cache(cache)
    write_report(results)

    for action, label in [("precision_stamped", "Stamped"), ("inherited", "Inherited"),
                           ("geocoded", "Geocoded"), ("no_location_data", "Off-map"),
                           ("geocode_miss", "Misses")]:
        print(f"  {label}: {sum(1 for r in results if r['action'] == action)}")


if __name__ == "__main__":
    main()
