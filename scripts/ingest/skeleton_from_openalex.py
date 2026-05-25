#!/usr/bin/env python3
"""
skeleton_from_openalex.py — Wave 2 skeleton creator.

Reads a shortlist CSV (one row per person: name, orcid, group_type, platforms,
applications), fetches full data from OpenAlex for each person and their
institution, creates thin-but-valid person + institution .md files, and runs
validation. All institution/position data tagged openalex_inferred.

Input CSV columns (required):
  name, orcid, group_type, platforms, applications

Input CSV columns (optional):
  note  — free-form human note (not written to files)

Usage:
    python scripts/ingest/skeleton_from_openalex.py
        --shortlist private/discovery/neutral_atom_shortlist.csv
        [--dry-run]
        [--start-person-id 080]
        [--start-inst-id 070]

GAME_PLAN: Wave 2. Every new person file is immediately queued for Wave 3
enrichment. Do not add judgment fields (advisor, key_papers, thesis) here.
"""

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
from datetime import date
from pathlib import Path

import frontmatter
import requests
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "content" / "people"
INSTITUTIONS_DIR = ROOT / "content" / "institutions"
SCHEMAS_DIR = ROOT / "schemas"
UTILS_DIR = ROOT / "scripts" / "utils"

OPENALEX_BASE = "https://api.openalex.org"
CONTACT_EMAIL = "ozerilab@weizmann.ac.il"
RATE_SLEEP = 0.15
TODAY = date.today().isoformat()

PRECISION_RANK = {"building": 4, "campus": 3, "city": 2, "inherited": 1, "none": 0, None: -1}

INST_CACHE_PATH = UTILS_DIR / "openalex_inst_cache.json"


# ── Cache ─────────────────────────────────────────────────────────────────────

def load_inst_cache() -> dict:
    if INST_CACHE_PATH.exists():
        return json.loads(INST_CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_inst_cache(cache: dict):
    INST_CACHE_PATH.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# ── OpenAlex helpers ──────────────────────────────────────────────────────────

HDR = {"User-Agent": f"ionlandscape-skeleton/1.0 (mailto:{CONTACT_EMAIL})"}
P_BASE = {"mailto": CONTACT_EMAIL}


def fetch_author_by_orcid(orcid: str) -> dict | None:
    url = f"{OPENALEX_BASE}/authors/https://orcid.org/{orcid}"
    time.sleep(RATE_SLEEP)
    try:
        r = requests.get(url, headers=HDR, params=P_BASE, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  [warn] OpenAlex author error for {orcid}: {e}")
        return None


def fetch_orcid_institution(orcid: str) -> str | None:
    """Fetch current/most-recent employer from ORCID public API.

    ORCID is researcher-controlled and more reliable than OpenAlex for current
    affiliation. Returns the organisation name string, or None if unavailable.
    """
    url = f"https://pub.orcid.org/v3.0/{orcid}/employments"
    time.sleep(RATE_SLEEP)
    try:
        r = requests.get(url, headers={"Accept": "application/json"}, timeout=15)
        if r.status_code != 200:
            return None
        data = r.json()
        summaries = (
            data.get("affiliation-group", [])
        )
        # Collect all employments, prefer those with no end-date (current)
        entries = []
        for group in summaries:
            for summary in group.get("summaries", []):
                emp = summary.get("employment-summary", {})
                end = emp.get("end-date")
                org = ((emp.get("organization") or {}).get("name") or "").strip()
                if org:
                    entries.append((end is None, org))  # (is_current, name)
        if not entries:
            return None
        # Sort: current entries first (True > False), then take first
        entries.sort(key=lambda x: x[0], reverse=True)
        return entries[0][1]
    except Exception as e:
        print(f"  [warn] ORCID employments error for {orcid}: {e}")
        return None


def search_institution_by_name(name: str) -> dict | None:
    """Search OpenAlex institutions by display name, return first match geo dict."""
    params = {**P_BASE, "search": name, "per-page": 1,
              "select": "id,display_name,ror,homepage_url,type,geo"}
    time.sleep(RATE_SLEEP)
    try:
        r = requests.get(f"{OPENALEX_BASE}/institutions", headers=HDR,
                         params=params, timeout=15)
        r.raise_for_status()
        results = r.json().get("results", [])
        if not results:
            return None
        d = results[0]
        geo = d.get("geo") or {}
        return {
            "display_name": d.get("display_name"),
            "ror": d.get("ror"),
            "homepage_url": d.get("homepage_url"),
            "type": d.get("type"),
            "city": geo.get("city"),
            "country": geo.get("country"),
            "lat": geo.get("latitude"),
            "lon": geo.get("longitude"),
            "openalex_id": d.get("id"),
        }
    except Exception as e:
        print(f"  [warn] Institution search error for '{name}': {e}")
        return None


def fetch_institution_geo(openalex_inst_id: str, cache: dict) -> dict | None:
    key = openalex_inst_id.rstrip("/").split("/")[-1]
    if key in cache:
        return cache[key]
    time.sleep(RATE_SLEEP)
    url = f"{OPENALEX_BASE}/institutions/{openalex_inst_id}"
    try:
        r = requests.get(url, headers=HDR, params=P_BASE, timeout=15)
        if r.status_code == 404:
            cache[key] = None
            return None
        r.raise_for_status()
        d = r.json()
        geo = d.get("geo") or {}
        entry = {
            "display_name": d.get("display_name"),
            "ror": d.get("ror"),
            "homepage_url": d.get("homepage_url"),
            "type": d.get("type"),
            "city": geo.get("city"),
            "country": geo.get("country"),
            "lat": geo.get("latitude"),
            "lon": geo.get("longitude"),
            "openalex_id": d.get("id"),
        }
        cache[key] = entry
        return entry
    except Exception as e:
        print(f"  [warn] OpenAlex institution error for {openalex_inst_id}: {e}")
        return None


# ── Repo institution lookup ───────────────────────────────────────────────────

def build_repo_inst_lookup() -> dict:
    """Returns {lower_name_or_alias: {id, canonical_name, ror}}"""
    lookup = {}
    for p in INSTITUTIONS_DIR.glob("*.md"):
        if ".evidence." in p.name:
            continue
        m = frontmatter.load(p).metadata
        iid = m.get("id", p.stem)
        canonical = m.get("name", "")
        ror = (m.get("links") or {}).get("ror") or ""
        keys = [canonical] + (m.get("aliases") or []) + (m.get("abbreviations") or [])
        entry = {"id": iid, "canonical_name": canonical, "ror": ror}
        for k in keys:
            if k:
                lookup[k.strip().lower()] = entry
    return lookup


def reconcile_institution(display_name: str, openalex_ror: str | None,
                           repo_lookup: dict) -> tuple[str, str | None]:
    key = display_name.strip().lower()
    if key in repo_lookup:
        e = repo_lookup[key]
        return e["canonical_name"], e["id"]
    if openalex_ror:
        ror_id = openalex_ror.rstrip("/").split("/")[-1]
        for e in repo_lookup.values():
            repo_ror_id = (e.get("ror") or "").rstrip("/").split("/")[-1]
            if repo_ror_id and repo_ror_id == ror_id:
                return e["canonical_name"], e["id"]
    return display_name, None


# ── ID allocation ─────────────────────────────────────────────────────────────

def next_person_id() -> int:
    ids = []
    for p in PEOPLE_DIR.glob("*.md"):
        if ".evidence." in p.name:
            continue
        m = re.match(r"^(\d{3})", p.stem)
        if m:
            n = int(m.group(1))
            if n != 0:
                ids.append(n)
    return max(ids) + 1 if ids else 1


def next_inst_id() -> int:
    ids = []
    for p in INSTITUTIONS_DIR.glob("*.md"):
        if ".evidence." in p.name:
            continue
        m = re.match(r"^i(\d+)", p.stem)
        if m:
            ids.append(int(m.group(1)))
    return max(ids) + 1 if ids else 1


def slugify(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = nfkd.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug


# ── Institution skeleton writer ───────────────────────────────────────────────

def create_institution_skeleton(geo: dict, inst_id: int,
                                 platforms: list[str], dry_run: bool) -> tuple[str, str]:
    """
    Creates an institution .md skeleton from OpenAlex institution geo data.
    Returns (canonical_name, repo_id).
    """
    name = geo.get("display_name", "")
    ror = geo.get("ror") or ""
    homepage = geo.get("homepage_url") or ""
    oa_type = geo.get("type") or ""
    oa_id = geo.get("openalex_id") or ""
    city = geo.get("city") or ""
    country = geo.get("country") or ""
    lat = geo.get("lat")
    lon = geo.get("lon")

    inst_type_map = {
        "education": "university",
        "government": "national_lab",
        "company": "company",
        "nonprofit": "national_lab",
        "facility": "national_lab",
        "archive": "national_lab",
        "funder": "other",
        "healthcare": "other",
        "other": "other",
    }
    institution_type = inst_type_map.get((oa_type or "").lower(), "university")

    slug = slugify(name)
    file_id = f"i{inst_id:03d}-{slug}"
    canonical_name = name

    loc: dict = {"city": city, "country": country}
    if lat is not None:
        loc["lat"] = round(float(lat), 6)
        loc["lon"] = round(float(lon), 6) if lon is not None else None
        loc["precision"] = "city"
        loc["geocode_source"] = "openalex"

    links: dict = {}
    if ror:
        links["ror"] = ror
    if oa_id:
        links["openalex"] = oa_id
    if homepage:
        links["website"] = homepage

    meta = {
        "id": file_id,
        "name": canonical_name,
        "entity_type": "institution",
        "schema_version": 1,
        "institution_type": institution_type,
        "location": loc,
        "platforms_represented": platforms,
        "links": links,
        "created_at": TODAY,
        "updated_at": TODAY,
        "last_verified_at": TODAY,
        "verification_source_count": 1,
    }

    path = INSTITUTIONS_DIR / f"{file_id}.md"
    if not dry_run:
        post = frontmatter.Post("", **meta)
        path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")
        print(f"  [inst] Created {file_id}  ({canonical_name})")

    return canonical_name, file_id


# ── Person skeleton writer ────────────────────────────────────────────────────

def create_person_skeleton(row: dict, author_data: dict | None,
                            inst_geo: dict | None, canonical_inst: str,
                            person_id: int, dry_run: bool,
                            inst_source: str = "openalex_inferred") -> str:
    """
    Creates a person .md skeleton. Returns the new person file id.
    inst_source: confidence tag for current_position ('openalex_inferred' or 'orcid_inferred').
    """
    name = row["name"].strip()
    orcid = row["orcid"].strip()
    group_type = row["group_type"].strip()
    platforms = [p.strip() for p in row["platforms"].split(",") if p.strip()]
    applications_raw = row.get("applications", "").strip()
    applications = [a.strip() for a in applications_raw.split(",") if a.strip()] if applications_raw else []

    slug = slugify(name)
    file_id = f"{person_id:03d}-{slug}"

    # Metrics + links from OpenAlex
    stats = (author_data or {}).get("summary_stats") or {}
    metrics = {
        "h_index": stats.get("h_index"),
        "citation_count": (author_data or {}).get("cited_by_count"),
        "publication_count": (author_data or {}).get("works_count"),
        "source": "openalex",
        "retrieved_at": TODAY,
    } if author_data else None

    links: dict = {}
    if orcid:
        links["orcid"] = f"https://orcid.org/{orcid}"
    if author_data and author_data.get("id"):
        links["openalex"] = author_data["id"]

    # Location from institution geo
    loc: dict = {}
    if inst_geo:
        city = inst_geo.get("city") or ""
        country = inst_geo.get("country") or ""
        lat = inst_geo.get("lat")
        lon = inst_geo.get("lon")
        loc = {"city": city, "country": country}
        if lat is not None:
            loc.update({
                "lat": round(float(lat), 6),
                "lon": round(float(lon), 6) if lon is not None else None,
                "precision": "city",
                "geocode_source": "openalex",
            })
    else:
        loc = {"city": "", "country": ""}

    # current_position
    current_position = {
        "institution": canonical_inst,
        "title": "",
        "confidence": inst_source,
        "source": (author_data or {}).get("id") or "",
    }

    # Keywords from OpenAlex topics
    topics = (author_data or {}).get("topics") or []
    keywords = [t["display_name"] for t in topics[:10] if t.get("display_name")]

    # Sort name: last, first (rough heuristic — Wave 3 corrects)
    parts = name.split()
    sort_name = f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) > 1 else name

    meta = {
        "id": file_id,
        "name": name,
        "sort_name": sort_name,
        "entity_type": "person",
        "schema_version": 2,
        "created_at": TODAY,
        "updated_at": TODAY,
        "group_type": group_type,
        "platforms": platforms,
        "active": "active",
        "current_position": current_position,
        "location": loc,
        "links": links,
        "last_verified_at": TODAY,
        "verification_source_count": 1,
    }

    if metrics:
        meta["metrics"] = metrics
    if keywords:
        meta["keywords"] = keywords

    # applications required for experimental/mixed
    if group_type in ("experimental", "mixed") and applications:
        meta["applications"] = applications
    elif group_type in ("experimental", "mixed") and not applications:
        meta["applications"] = ["computing"]  # safe default; Wave 3 corrects
    # theory: no applications field needed

    path = PEOPLE_DIR / f"{file_id}.md"
    if not dry_run:
        post = frontmatter.Post("", **meta)
        path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")
        print(f"  [person] Created {file_id}  ({name})")

    return file_id


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--shortlist", required=True, help="Path to shortlist CSV.")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files.")
    args = parser.parse_args()

    shortlist_path = Path(args.shortlist)
    if not shortlist_path.exists():
        print(f"Error: {shortlist_path} not found")
        sys.exit(1)

    rows = list(csv.DictReader(shortlist_path.open(encoding="utf-8")))
    print(f"Shortlist: {len(rows)} people  |  dry_run={args.dry_run}")

    repo_lookup = build_repo_inst_lookup()
    inst_cache = load_inst_cache()

    person_id = next_person_id()
    inst_id = next_inst_id()

    print(f"Starting person IDs at {person_id:03d}, institution IDs at i{inst_id:03d}")
    if args.dry_run:
        print("  [DRY RUN]\n")

    results = []
    new_insts: dict[str, str] = {}  # openalex_inst_id → repo_id

    for i, row in enumerate(rows, 1):
        name = row["name"].strip()
        orcid = row["orcid"].strip()
        platforms_raw = row.get("platforms", "").strip()
        platforms = [p.strip() for p in platforms_raw.split(",") if p.strip()]

        print(f"\n[{i:2d}/{len(rows)}] {name}  (ORCID: {orcid})")

        # ── Fetch author from OpenAlex ────────────────────────────────────────
        author_data = fetch_author_by_orcid(orcid) if orcid else None
        if author_data is None:
            print(f"  [warn] OpenAlex miss for {orcid}")

        # ── Fetch institution geo ─────────────────────────────────────────────
        inst_geo = None
        canonical_inst = ""
        matched_inst_id = None
        display_name = ""

        manual_inst = (row.get("manual_institution") or "").strip()
        inst_source = "openalex_inferred"  # default; overridden below

        if manual_inst:
            # 1st priority: human-verified institution name from shortlist CSV
            inst_geo = search_institution_by_name(manual_inst)
            display_name = (inst_geo or {}).get("display_name") or manual_inst
            inst_source = "openalex_inferred"  # geo from OA; name from human
        elif orcid:
            # 2nd priority: ORCID employments (researcher-controlled, reliable)
            orcid_inst = fetch_orcid_institution(orcid)
            if orcid_inst:
                print(f"  → ORCID institution: {orcid_inst}")
                inst_geo = search_institution_by_name(orcid_inst)
                display_name = (inst_geo or {}).get("display_name") or orcid_inst
                inst_source = "orcid_inferred"
            else:
                print(f"  [warn] No ORCID employer for {name}; leaving institution empty")
        else:
            print(f"  [warn] No ORCID and no manual_institution for {name}")

        if display_name:
            oa_ror = (inst_geo or {}).get("ror")
            oa_inst_id = (inst_geo or {}).get("openalex_id") or ""

            canonical_inst, matched_inst_id = reconcile_institution(
                display_name, oa_ror, repo_lookup
            )

            if matched_inst_id is None:
                if inst_geo:
                    dedup_key = oa_inst_id or f"name:{display_name}"
                    if dedup_key in new_insts:
                        matched_inst_id = new_insts[dedup_key]
                        canonical_inst = next(
                            v["canonical_name"] for v in repo_lookup.values()
                            if v["id"] == matched_inst_id
                        )
                    else:
                        print(f"  → New institution: {display_name}")
                        canonical_inst, new_inst_id = create_institution_skeleton(
                            inst_geo, inst_id, platforms, args.dry_run
                        )
                        new_insts[dedup_key] = new_inst_id
                        repo_lookup[canonical_inst.lower()] = {
                            "id": new_inst_id,
                            "canonical_name": canonical_inst,
                            "ror": inst_geo.get("ror") or "",
                        }
                        matched_inst_id = new_inst_id
                        inst_id += 1
                else:
                    print(f"  [warn] No institution geo for {name}")
                    canonical_inst = display_name
            else:
                print(f"  → Institution matched: {canonical_inst} ({matched_inst_id})")

        # ── Create person skeleton ────────────────────────────────────────────
        file_id = create_person_skeleton(
            row, author_data, inst_geo, canonical_inst, person_id, args.dry_run,
            inst_source=inst_source,
        )
        person_id += 1

        results.append({
            "id": file_id, "name": name, "orcid": orcid,
            "institution": canonical_inst, "matched_inst_id": matched_inst_id,
        })

    save_inst_cache(inst_cache)

    print(f"\n{'='*60}")
    print(f"Done. {'[DRY RUN] ' if args.dry_run else ''}"
          f"{len(results)} people, {len(new_insts)} new institutions")
    print(f"\nNext steps:")
    if not args.dry_run:
        print("  1. python scripts/validation/validate_profiles.py --people --institutions")
        print("  2. python scripts/core/build_index.py")
        print("  3. Review reports/unresolved_edges.md")
    else:
        print("  Re-run without --dry-run to create files")


if __name__ == "__main__":
    main()
