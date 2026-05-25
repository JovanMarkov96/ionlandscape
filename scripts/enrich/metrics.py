#!/usr/bin/env python3
"""
metrics.py — populate the metrics{} block for every person who has an ORCID.

Primary source: OpenAlex (free, no key, author looked up by ORCID).
Returns: h_index, citation_count (cited_by_count), publication_count (works_count).

Cache:  scripts/utils/metrics_cache.json  (keyed by bare ORCID id)
Report: reports/metrics_report.md

Only re-fetches entries whose metrics.source != "openalex" OR whose
metrics.retrieved_at is older than FRESHNESS_DAYS (default 90). Use --force
to bypass the freshness gate.

Usage:
    python scripts/enrich/metrics.py [--force] [--person <id>] [--dry-run]
"""

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

import frontmatter
import requests

# Windows terminals often use a narrow code page; upgrade stdout to utf-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "content" / "people"
CACHE_PATH = ROOT / "scripts" / "utils" / "metrics_cache.json"
REPORT_PATH = ROOT / "reports" / "metrics_report.md"

OPENALEX_BASE = "https://api.openalex.org"
CONTACT_EMAIL = "ozerilab@weizmann.ac.il"
FRESHNESS_DAYS = 90
RATE_SLEEP = 0.15  # polite gap between requests


# ── Cache helpers ─────────────────────────────────────────────────────────────

def load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict):
    CACHE_PATH.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ── Freshness ─────────────────────────────────────────────────────────────────

def is_fresh(retrieved_at, force: bool) -> bool:
    if force or not retrieved_at:
        return False
    try:
        return (date.today() - date.fromisoformat(str(retrieved_at))).days < FRESHNESS_DAYS
    except (ValueError, TypeError):
        return False


# ── ORCID extraction ──────────────────────────────────────────────────────────

def bare_orcid(orcid_url: str) -> str | None:
    if not orcid_url:
        return None
    return orcid_url.strip().rstrip("/").split("/")[-1] or None


# ── OpenAlex fetch ────────────────────────────────────────────────────────────

def fetch_openalex(orcid: str) -> dict | None:
    """Query OpenAlex for author summary by ORCID. Returns None on 404 or error."""
    url = f"{OPENALEX_BASE}/authors/https://orcid.org/{orcid}"
    headers = {"User-Agent": f"ionlandscape-metrics/1.0 (mailto:{CONTACT_EMAIL})"}
    try:
        r = requests.get(url, headers=headers, params={"mailto": CONTACT_EMAIL}, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        d = r.json()
        stats = d.get("summary_stats") or {}
        return {
            "h_index": stats.get("h_index"),
            "citation_count": d.get("cited_by_count"),
            "publication_count": d.get("works_count"),
            "openalex_id": d.get("id"),
        }
    except Exception as e:
        print(f"    [warn] OpenAlex error for ORCID {orcid}: {e}")
        return None


# ── Per-person processing ─────────────────────────────────────────────────────

def process_person(path: Path, cache: dict, force: bool, dry_run: bool) -> dict:
    post = frontmatter.load(path)
    meta = post.metadata
    pid = meta.get("id", path.stem)
    name = meta.get("name", pid)

    orcid_url = (meta.get("links") or {}).get("orcid")
    orcid = bare_orcid(orcid_url)
    if not orcid:
        return {"id": pid, "name": name, "status": "no_orcid"}

    existing = meta.get("metrics") or {}

    # Skip if already sourced from openalex and still fresh
    if existing.get("source") == "openalex" and is_fresh(existing.get("retrieved_at"), force):
        return {"id": pid, "name": name, "status": "fresh", "orcid": orcid}

    today = date.today().isoformat()

    # Use cache when fresh enough
    cached = cache.get(orcid)
    if cached and is_fresh(cached.get("retrieved_at"), force):
        data = cached
    else:
        time.sleep(RATE_SLEEP)
        fetched = fetch_openalex(orcid)
        if fetched is None:
            return {"id": pid, "name": name, "status": "openalex_miss", "orcid": orcid}
        data = {**fetched, "retrieved_at": today}
        cache[orcid] = data

    new_metrics = {
        "h_index": data.get("h_index"),
        "citation_count": data.get("citation_count"),
        "publication_count": data.get("publication_count"),
        "source": "openalex",
        "retrieved_at": data.get("retrieved_at", today),
    }

    if not dry_run:
        meta["metrics"] = new_metrics
        path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")

    return {
        "id": pid, "name": name, "status": "updated",
        "orcid": orcid, "old": dict(existing), "new": new_metrics,
    }


# ── Report ────────────────────────────────────────────────────────────────────

def write_report(results: list):
    by_status = {}
    for r in results:
        by_status.setdefault(r["status"], []).append(r)

    updated   = by_status.get("updated", [])
    fresh     = by_status.get("fresh", [])
    no_orcid  = by_status.get("no_orcid", [])
    missed    = by_status.get("openalex_miss", [])

    lines = [
        "# Metrics Enrichment Report",
        f"\nGenerated: {date.today().isoformat()}",
        f"\n**Updated:** {len(updated)}  |  "
        f"**Skipped (fresh):** {len(fresh)}  |  "
        f"**No ORCID:** {len(no_orcid)}  |  "
        f"**OpenAlex miss:** {len(missed)}\n",
    ]

    if updated:
        lines += [
            "\n## Updated\n",
            "| Person | h-index | Citations | Publications |",
            "|---|---|---|---|",
        ]
        for r in updated:
            n = r["new"]
            lines.append(
                f"| {r['name']} (`{r['id']}`) "
                f"| {n['h_index']} | {n['citation_count']} | {n['publication_count']} |"
            )

    if missed:
        lines.append("\n## OpenAlex misses (have ORCID, no OpenAlex record)\n")
        for r in missed:
            lines.append(f"- {r['name']} (`{r['id']}`) — `{r['orcid']}`")

    if no_orcid:
        lines.append(f"\n## No ORCID ({len(no_orcid)} people — metrics not auto-filled)\n")
        for r in no_orcid:
            lines.append(f"- {r['name']} (`{r['id']}`)")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="Ignore freshness; re-fetch everything.")
    parser.add_argument("--person", metavar="ID", help="Process only this one person id.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch + report but don't write files.")
    args = parser.parse_args()

    cache = load_cache()

    paths = sorted(p for p in PEOPLE_DIR.glob("*.md") if ".evidence." not in p.name)
    if args.person:
        paths = [p for p in paths if p.stem == args.person]
        if not paths:
            print(f"No person found: {args.person}")
            return

    icons = {"updated": "+", "fresh": "-", "no_orcid": ".", "openalex_miss": "!"}
    results = []
    print(f"Processing {len(paths)} people...")

    for i, path in enumerate(paths, 1):
        r = process_person(path, cache, force=args.force, dry_run=args.dry_run)
        results.append(r)
        icon = icons.get(r["status"], "?")
        print(f"  [{i:3d}/{len(paths)}] {icon} {r['name']}  ({r['status']})")
        if i % 20 == 0:
            save_cache(cache)

    save_cache(cache)
    write_report(results)

    counts = {s: sum(1 for r in results if r["status"] == s) for s in icons}
    print(f"\nDone. Updated: {counts['updated']}  Fresh: {counts['fresh']}  "
          f"No ORCID: {counts['no_orcid']}  Misses: {counts['openalex_miss']}")


if __name__ == "__main__":
    main()
