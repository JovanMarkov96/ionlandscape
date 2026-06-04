#!/usr/bin/env python3
"""
openalex.py — Wave 0 deterministic harvest from OpenAlex.

For every person with an ORCID, fetches the full OpenAlex author object and
writes:
  - links.openalex            (stable OpenAlex author id)
  - metrics{h_index, citation_count, publication_count, source, retrieved_at}
  - current_position.institution  (from last_known_institutions[0].display_name,
                                   reconciled to the canonical repo name)
  - current_position.confidence   openalex_inferred
  - current_position.source       <openalex author url>
  - location{city, country, lat, lon, precision: city, geocode_source: openalex}
                                   (from institution geo; never downgrades precision)
  - keywords[]                    (candidate topics — not applications; Wave 3 judgment)

Rules:
  - Never overwrites current_position.confidence == "confirmed".
  - Never downgrades location.precision to a lower tier.
  - Stubs (000- prefix) are skipped.

Caches:
  scripts/utils/openalex_author_cache.json  (keyed by bare ORCID)
  scripts/utils/openalex_inst_cache.json    (keyed by OpenAlex institution id)

Reports:
  reports/openalex_report.md
  reports/openalex_institution_map.md

Usage:
    python scripts/enrich/openalex.py [--person ID] [--dry-run] [--force]
                                      [--only metrics|position|geo|topics]
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
UTILS_DIR = ROOT / "scripts" / "utils"
REPORTS_DIR = ROOT / "reports"

AUTHOR_CACHE_PATH = UTILS_DIR / "openalex_author_cache.json"
INST_CACHE_PATH = UTILS_DIR / "openalex_inst_cache.json"
REPORT_PATH = REPORTS_DIR / "openalex_report.md"
INST_MAP_PATH = REPORTS_DIR / "openalex_institution_map.md"

OPENALEX_BASE = "https://api.openalex.org"
CONTACT_EMAIL = "ozerilab@weizmann.ac.il"
FRESHNESS_DAYS = 90
RATE_SLEEP = 0.15

PRECISION_RANK = {"building": 4, "campus": 3, "city": 2, "inherited": 1, "none": 0, None: -1}


# ── Cache helpers ─────────────────────────────────────────────────────────────

def load_cache(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_cache(path: Path, cache: dict):
    UTILS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ── Freshness ─────────────────────────────────────────────────────────────────

def is_fresh(retrieved_at, force: bool) -> bool:
    if force or not retrieved_at:
        return False
    try:
        return (date.today() - date.fromisoformat(str(retrieved_at))).days < FRESHNESS_DAYS
    except (ValueError, TypeError):
        return False


def higher_precision(new: str, existing) -> bool:
    return PRECISION_RANK.get(new, -1) > PRECISION_RANK.get(existing, -1)


# ── ORCID extraction ──────────────────────────────────────────────────────────

def bare_orcid(orcid_url: str) -> str | None:
    if not orcid_url:
        return None
    return orcid_url.strip().rstrip("/").split("/")[-1] or None


# ── OpenAlex API ──────────────────────────────────────────────────────────────

def fetch_author(orcid: str) -> dict | None:
    """Fetch full OpenAlex author object by ORCID. Returns None on 404 or error."""
    url = f"{OPENALEX_BASE}/authors/https://orcid.org/{orcid}"
    headers = {"User-Agent": f"quantum-landscape-openalex/1.0 (mailto:{CONTACT_EMAIL})"}
    try:
        r = requests.get(url, headers=headers, params={"mailto": CONTACT_EMAIL}, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"    [warn] OpenAlex author error for {orcid}: {e}")
        return None


def fetch_institution_geo(openalex_inst_id: str, inst_cache: dict) -> dict | None:
    """
    Fetch OpenAlex institution geo, using per-id cache.
    openalex_inst_id is the full URL, e.g. 'https://openalex.org/I27837315'.
    Returns dict with: display_name, ror, city, country, lat, lon.
    """
    cache_key = openalex_inst_id.rstrip("/").split("/")[-1]
    if cache_key in inst_cache:
        return inst_cache[cache_key]

    url = f"{OPENALEX_BASE}/institutions/{openalex_inst_id}"
    headers = {"User-Agent": f"quantum-landscape-openalex/1.0 (mailto:{CONTACT_EMAIL})"}
    try:
        time.sleep(RATE_SLEEP)
        r = requests.get(url, headers=headers, params={"mailto": CONTACT_EMAIL}, timeout=15)
        if r.status_code == 404:
            inst_cache[cache_key] = None
            return None
        r.raise_for_status()
        d = r.json()
        geo = d.get("geo") or {}
        entry = {
            "display_name": d.get("display_name"),
            "ror": d.get("ror"),
            "city": geo.get("city"),
            "country": geo.get("country"),
            "lat": geo.get("latitude"),
            "lon": geo.get("longitude"),
        }
        inst_cache[cache_key] = entry
        return entry
    except Exception as e:
        print(f"    [warn] OpenAlex institution error for {openalex_inst_id}: {e}")
        return None


# ── Institution name reconciliation ──────────────────────────────────────────

def build_repo_inst_lookup() -> dict:
    """
    Returns {lowercased_name_or_alias: {id, canonical_name, ror}}.
    Used to reconcile OpenAlex display_name → repo canonical institution name.
    Matches by exact lowercased name/alias/abbreviation; falls back to ROR.
    """
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
    """
    Returns (name_to_write, matched_repo_id_or_None).
    Strategy: exact name/alias match → ROR match → unmatched (write display_name verbatim).
    """
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


# ── Per-person processing ─────────────────────────────────────────────────────

def process_person(path: Path, author_cache: dict, inst_cache: dict,
                   repo_lookup: dict, force: bool, dry_run: bool,
                   only: str | None) -> dict:
    post = frontmatter.load(path)
    meta = post.metadata
    pid = meta.get("id", path.stem)
    name = meta.get("name", pid)

    if str(pid).startswith("000-"):
        return {"id": pid, "name": name, "status": "stub"}

    orcid_url = (meta.get("links") or {}).get("orcid")
    orcid = bare_orcid(orcid_url)
    if not orcid:
        return {"id": pid, "name": name, "status": "no_orcid"}

    today = date.today().isoformat()

    # ── Fetch author (cache + freshness gate) ─────────────────────────────────
    cached = author_cache.get(orcid)
    if cached and is_fresh(cached.get("retrieved_at"), force):
        author_data = cached["author"]
        retrieved_at = cached["retrieved_at"]
    else:
        time.sleep(RATE_SLEEP)
        author_data = fetch_author(orcid)
        if author_data is None:
            return {"id": pid, "name": name, "status": "openalex_miss", "orcid": orcid}
        retrieved_at = today
        author_cache[orcid] = {"author": author_data, "retrieved_at": today}

    result: dict = {
        "id": pid, "name": name, "status": "processed", "orcid": orcid,
        "changes": [], "inst_display_name": None, "matched_inst_id": None,
    }
    changed = False

    # ── 1. Metrics ────────────────────────────────────────────────────────────
    if only in (None, "metrics"):
        stats = author_data.get("summary_stats") or {}
        new_metrics = {
            "h_index": stats.get("h_index"),
            "citation_count": author_data.get("cited_by_count"),
            "publication_count": author_data.get("works_count"),
            "source": "openalex",
            "retrieved_at": retrieved_at,
        }
        existing = meta.get("metrics") or {}
        if (existing.get("source") != "openalex"
                or not is_fresh(existing.get("retrieved_at"), force)):
            if not dry_run:
                meta["metrics"] = new_metrics
            result["changes"].append("metrics")
            result["new_metrics"] = new_metrics
            changed = True

    # ── 2. links.openalex ────────────────────────────────────────────────────
    if only in (None, "metrics"):
        author_url = author_data.get("id")
        if author_url:
            links = dict(meta.get("links") or {})
            if links.get("openalex") != author_url:
                links["openalex"] = author_url
                if not dry_run:
                    meta["links"] = links
                result["changes"].append("links.openalex")
                changed = True

    # ── 3. Institution: fetch geo, reconcile, write position + location ───────
    if only in (None, "position", "geo"):
        insts = author_data.get("last_known_institutions") or []
        if insts:
            inst_ref = insts[0]
            openalex_inst_id = inst_ref.get("id", "")
            display_name = inst_ref.get("display_name", "")
            result["inst_display_name"] = display_name

            inst_geo = None
            openalex_ror = None
            if openalex_inst_id:
                inst_geo = fetch_institution_geo(openalex_inst_id, inst_cache)
                if inst_geo:
                    openalex_ror = inst_geo.get("ror")

            canonical_name, matched_id = reconcile_institution(
                display_name, openalex_ror, repo_lookup
            )
            result["matched_inst_id"] = matched_id
            result["canonical_inst_name"] = canonical_name

            # Write location from institution geo — never downgrade precision
            # NOTE: We deliberately do NOT write current_position.institution from
            # OpenAlex. OpenAlex last_known_institutions are derived from paper
            # affiliations and are frequently wrong (e.g. instrument co. affiliations
            # appearing as primary institution). Affiliation must come from human
            # curation or the manual_institution column in shortlist CSVs.
            if only in (None, "geo") and inst_geo:
                geo_city = inst_geo.get("city")
                geo_lat = inst_geo.get("lat")
                geo_lon = inst_geo.get("lon")
                geo_country = inst_geo.get("country")
                if geo_city and geo_lat is not None:
                    existing_loc = dict(meta.get("location") or {})
                    if higher_precision("city", existing_loc.get("precision")):
                        new_loc = dict(existing_loc)
                        new_loc.update({
                            "city": geo_city,
                            "country": geo_country or existing_loc.get("country", ""),
                            "lat": round(float(geo_lat), 6),
                            "lon": round(float(geo_lon), 6) if geo_lon is not None else None,
                            "precision": "city",
                            "geocode_source": "openalex",
                        })
                        if not dry_run:
                            meta["location"] = new_loc
                        result["changes"].append("location")
                        changed = True

    # ── 4. Keywords (candidate topics) ───────────────────────────────────────
    if only in (None, "topics"):
        topics = author_data.get("topics") or []
        new_topics = [t["display_name"] for t in topics[:10] if t.get("display_name")]
        if new_topics:
            existing_kw = list(meta.get("keywords") or [])
            additions = [t for t in new_topics if t not in existing_kw]
            if additions:
                merged = existing_kw + additions
                if not dry_run:
                    meta["keywords"] = merged
                result["changes"].append("keywords")
                changed = True

    # ── Write ─────────────────────────────────────────────────────────────────
    if changed and not dry_run:
        meta["updated_at"] = today
        post.metadata = meta
        path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")

    result["status"] = "updated" if result["changes"] else "no_changes"
    return result


# ── Reports ───────────────────────────────────────────────────────────────────

def write_reports(results: list):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    by_status: dict[str, list] = {}
    for r in results:
        by_status.setdefault(r["status"], []).append(r)

    updated    = by_status.get("updated", [])
    no_changes = by_status.get("no_changes", [])
    no_orcid   = by_status.get("no_orcid", [])
    missed     = by_status.get("openalex_miss", [])
    stubs      = by_status.get("stub", [])

    # openalex_report.md
    lines = [
        "# OpenAlex Harvest Report (Wave 0)",
        f"\nGenerated: {date.today().isoformat()}",
        f"\n**Updated:** {len(updated)}  |  "
        f"**No changes:** {len(no_changes)}  |  "
        f"**No ORCID:** {len(no_orcid)}  |  "
        f"**OpenAlex miss:** {len(missed)}  |  "
        f"**Stubs skipped:** {len(stubs)}\n",
    ]

    if updated:
        lines += [
            "\n## Updated\n",
            "| Person | Fields changed | Institution | Repo match |",
            "|---|---|---|---|",
        ]
        for r in updated:
            ch = ", ".join(r.get("changes", []))
            inst = r.get("canonical_inst_name", "—")
            mid = r.get("matched_inst_id") or "UNMATCHED"
            lines.append(f"| {r['name']} (`{r['id']}`) | {ch} | {inst} | {mid} |")

    if missed:
        lines.append("\n## OpenAlex misses (ORCID present, no record found)\n")
        for r in missed:
            lines.append(f"- {r['name']} (`{r['id']}`) — ORCID `{r['orcid']}`")

    if no_orcid:
        lines.append(f"\n## No ORCID ({len(no_orcid)} — out of scope for Wave 0)\n")
        for r in no_orcid:
            lines.append(f"- {r['name']} (`{r['id']}`)")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report: {REPORT_PATH}")

    # openalex_institution_map.md
    inst_map: dict[str, str] = {}
    for r in results:
        dn = r.get("inst_display_name")
        if dn:
            inst_map[dn] = r.get("matched_inst_id") or "UNMATCHED"

    map_lines = [
        "# OpenAlex → Repo Institution Map",
        f"\nGenerated: {date.today().isoformat()}",
        "\nProduced by `scripts/enrich/openalex.py`. Feeds Wave 1/2 institution creation.",
        "\n| OpenAlex display_name | Matched repo id |",
        "|---|---|",
    ]
    for dn in sorted(inst_map):
        map_lines.append(f"| {dn} | {inst_map[dn]} |")

    unmatched = sorted(dn for dn, mid in inst_map.items() if mid == "UNMATCHED")
    if unmatched:
        map_lines.append(f"\n## Unmatched ({len(unmatched)}) — Wave 2 institution-creation candidates\n")
        for dn in unmatched:
            map_lines.append(f"- {dn}")

    INST_MAP_PATH.write_text("\n".join(map_lines) + "\n", encoding="utf-8")
    print(f"Institution map: {INST_MAP_PATH}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--force", action="store_true", help="Ignore freshness; re-fetch.")
    parser.add_argument("--person", metavar="ID", help="Process only this person id.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch + report; write nothing.")
    parser.add_argument(
        "--only", choices=["metrics", "position", "geo", "topics"],
        help="Restrict which field groups to write.",
    )
    args = parser.parse_args()

    author_cache = load_cache(AUTHOR_CACHE_PATH)
    inst_cache = load_cache(INST_CACHE_PATH)
    repo_lookup = build_repo_inst_lookup()

    paths = sorted(p for p in PEOPLE_DIR.glob("*.md") if ".evidence." not in p.name)
    if args.person:
        target_id = args.person
        paths = [p for p in paths
                 if p.stem == target_id
                 or frontmatter.load(p).metadata.get("id") == target_id]
        if not paths:
            print(f"No person found: {args.person}")
            return

    print(f"Processing {len(paths)} people  "
          f"({len(repo_lookup)} institution lookup entries)")
    if args.dry_run:
        print("  [DRY RUN — no files will be written]")

    results = []
    icons = {"updated": "+", "no_changes": "-", "no_orcid": ".",
             "openalex_miss": "!", "stub": "s", "processed": "?"}

    for i, path in enumerate(paths, 1):
        r = process_person(
            path, author_cache, inst_cache, repo_lookup,
            force=args.force, dry_run=args.dry_run, only=args.only,
        )
        results.append(r)
        icon = icons.get(r["status"], "?")
        detail = ", ".join(r.get("changes", [])) if r.get("changes") else r["status"]
        print(f"  [{i:3d}/{len(paths)}] {icon} {r['name']}  ({detail})")
        if i % 20 == 0:
            save_cache(AUTHOR_CACHE_PATH, author_cache)
            save_cache(INST_CACHE_PATH, inst_cache)

    save_cache(AUTHOR_CACHE_PATH, author_cache)
    save_cache(INST_CACHE_PATH, inst_cache)
    write_reports(results)

    def count(s):
        return sum(1 for r in results if r["status"] == s)

    print(f"\nDone.  Updated: {count('updated')}  "
          f"No changes: {count('no_changes')}  "
          f"No ORCID: {count('no_orcid')}  "
          f"Misses: {count('openalex_miss')}  "
          f"Stubs: {count('stub')}")


if __name__ == "__main__":
    main()
