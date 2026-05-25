#!/usr/bin/env python3
"""
openalex_candidates.py — Wave 1 deterministic candidate generator.

Queries OpenAlex for papers matching platform-specific keywords, aggregates
the most prolific authors, and deduplicates against existing repo people.
Outputs private/discovery/<platform>_candidates.csv.

Strategy: /works keyword search (title + abstract) → author tally →
batch-fetch author records for top candidates → filter by works_count threshold.
This is more platform-specific than topic-ID queries, which are too coarse.

Usage:
    python scripts/discover/openalex_candidates.py --platform nv
    python scripts/discover/openalex_candidates.py --platform neutral_atom
    python scripts/discover/openalex_candidates.py --platform superconducting
    python scripts/discover/openalex_candidates.py --platform all
    python scripts/discover/openalex_candidates.py --platform nv --max-works 400 --min-papers 3
"""

import argparse
import csv
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import frontmatter
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "content" / "people"
DISCOVERY_DIR = ROOT / "private" / "discovery"
UTILS_DIR = ROOT / "scripts" / "utils"

OPENALEX_BASE = "https://api.openalex.org"
CONTACT_EMAIL = "ozerilab@weizmann.ac.il"
RATE_SLEEP = 0.15

PLATFORM_QUERIES = {
    "nv": {
        "label": "NV / Colour Centre",
        "keywords": [
            "nitrogen-vacancy center qubit",
            "NV center quantum computing",
            "diamond spin qubit",
            "color center spin qubit",
        ],
        "min_works_count": 20,
    },
    "neutral_atom": {
        "label": "Neutral Atoms / Rydberg",
        "keywords": [
            "Rydberg qubit quantum gate",
            "Rydberg atom array quantum",
            "neutral atom tweezer qubit",
            "optical tweezer quantum computing",
        ],
        "min_works_count": 20,
    },
    "superconducting": {
        "label": "Superconducting",
        "keywords": [
            "superconducting qubit quantum",
            "transmon qubit circuit QED",
            "superconducting quantum processor",
            "Josephson junction qubit gate",
        ],
        "min_works_count": 20,
    },
}


# ── Repo people index (for deduplication) ─────────────────────────────────────

def build_repo_index() -> tuple[set[str], set[str]]:
    """
    Returns (known_orcids, known_openalex_ids) — both lowercase-stripped.
    Used to exclude people already in the repo from candidate lists.
    """
    known_orcids: set[str] = set()
    known_openalex_ids: set[str] = set()
    for p in PEOPLE_DIR.glob("*.md"):
        if ".evidence." in p.name:
            continue
        m = frontmatter.load(p).metadata
        links = m.get("links") or {}
        orcid = links.get("orcid")
        if orcid:
            bare = orcid.strip().rstrip("/").split("/")[-1].lower()
            known_orcids.add(bare)
        openalex = links.get("openalex")
        if openalex:
            aid = openalex.strip().rstrip("/").split("/")[-1].upper()
            known_openalex_ids.add(aid)
    return known_orcids, known_openalex_ids


# ── OpenAlex helpers ──────────────────────────────────────────────────────────

def get_headers() -> dict:
    return {"User-Agent": f"ionlandscape-discovery/1.0 (mailto:{CONTACT_EMAIL})"}


def fetch_works_page(keyword: str, cursor: str = "*", per_page: int = 200) -> dict:
    """Fetch one page of works matching keyword (title+abstract search)."""
    params = {
        "filter": f"title_and_abstract.search:{keyword},type:article",
        "sort": "cited_by_count:desc",
        "per-page": per_page,
        "cursor": cursor,
        "mailto": CONTACT_EMAIL,
        "select": "id,authorships,cited_by_count,publication_year",
    }
    time.sleep(RATE_SLEEP)
    r = requests.get(f"{OPENALEX_BASE}/works", headers=get_headers(),
                     params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def collect_author_tally(keywords: list[str], max_works: int) -> dict[str, dict]:
    """
    Run keyword queries, collect authorships, return:
    {openalex_author_id: {name, orcid, institution, country, paper_count, queries}}
    """
    tally: dict[str, dict] = {}

    for kw in keywords:
        collected = 0
        cursor = "*"
        print(f"  Querying: '{kw}'")
        while collected < max_works:
            try:
                page = fetch_works_page(kw, cursor, per_page=min(200, max_works - collected))
            except Exception as e:
                print(f"    [warn] fetch error: {e}")
                break

            results = page.get("results", [])
            if not results:
                break

            for work in results:
                for authorship in (work.get("authorships") or []):
                    author = authorship.get("author") or {}
                    aid = (author.get("id") or "").rstrip("/").split("/")[-1].upper()
                    if not aid:
                        continue
                    if aid not in tally:
                        inst_list = authorship.get("institutions") or []
                        inst = inst_list[0] if inst_list else {}
                        tally[aid] = {
                            "openalex_id": f"https://openalex.org/{aid}",
                            "name": author.get("display_name", ""),
                            "orcid": (author.get("orcid") or "").split("/")[-1],
                            "institution": inst.get("display_name", ""),
                            "country": inst.get("country_code", ""),
                            "paper_count": 0,
                            "queries": set(),
                            "works_count": None,
                            "cited_by_count": None,
                            "h_index": None,
                        }
                    tally[aid]["paper_count"] += 1
                    tally[aid]["queries"].add(kw[:40])

            collected += len(results)
            cursor = page.get("meta", {}).get("next_cursor")
            if not cursor:
                break

        print(f"    → {collected} works, {len(tally)} unique authors so far")

    return tally


def batch_fetch_author_details(author_ids: list[str],
                                batch_size: int = 50) -> dict[str, dict]:
    """
    Batch-fetch author records from OpenAlex for a list of OpenAlex author IDs.
    Returns {bare_id: {works_count, cited_by_count, h_index, last_known_institutions}}.
    """
    details: dict[str, dict] = {}
    for i in range(0, len(author_ids), batch_size):
        batch = author_ids[i: i + batch_size]
        pipe_ids = "|".join(f"https://openalex.org/{aid}" for aid in batch)
        params = {
            "filter": f"ids.openalex:{pipe_ids}",
            "per-page": batch_size,
            "mailto": CONTACT_EMAIL,
            "select": "id,works_count,cited_by_count,summary_stats,last_known_institutions",
        }
        time.sleep(RATE_SLEEP)
        try:
            r = requests.get(f"{OPENALEX_BASE}/authors", headers=get_headers(),
                             params=params, timeout=20)
            r.raise_for_status()
            for a in r.json().get("results", []):
                aid = a.get("id", "").rstrip("/").split("/")[-1].upper()
                stats = a.get("summary_stats") or {}
                insts = a.get("last_known_institutions") or []
                details[aid] = {
                    "works_count": a.get("works_count"),
                    "cited_by_count": a.get("cited_by_count"),
                    "h_index": stats.get("h_index"),
                    "institution": insts[0].get("display_name", "") if insts else "",
                    "country": insts[0].get("country_code", "") if insts else "",
                }
        except Exception as e:
            print(f"  [warn] batch fetch error: {e}")
    return details


# ── CSV output ────────────────────────────────────────────────────────────────

def write_csv(candidates: list[dict], platform: str):
    DISCOVERY_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DISCOVERY_DIR / f"{platform}_candidates.csv"
    fieldnames = [
        "name", "openalex_id", "orcid", "institution", "country",
        "works_count", "cited_by_count", "h_index",
        "platform_paper_count", "source_queries", "in_repo",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in candidates:
            writer.writerow({
                "name": c["name"],
                "openalex_id": c["openalex_id"],
                "orcid": c["orcid"],
                "institution": c["institution"],
                "country": c["country"],
                "works_count": c["works_count"] or "",
                "cited_by_count": c["cited_by_count"] or "",
                "h_index": c["h_index"] or "",
                "platform_paper_count": c["paper_count"],
                "source_queries": "; ".join(sorted(c["queries"])),
                "in_repo": c.get("in_repo", False),
            })
    print(f"CSV → {out_path}  ({len(candidates)} candidates)")
    return out_path


# ── Per-platform run ──────────────────────────────────────────────────────────

def run_platform(platform: str, max_works: int, min_papers: int):
    cfg = PLATFORM_QUERIES[platform]
    print(f"\n{'='*60}")
    print(f"Platform: {cfg['label']}")
    print(f"{'='*60}")

    known_orcids, known_openalex_ids = build_repo_index()
    print(f"Repo: {len(known_orcids)} known ORCIDs, {len(known_openalex_ids)} known OpenAlex IDs")

    tally = collect_author_tally(cfg["keywords"], max_works)

    # Filter: keep only authors appearing in >= min_papers platform papers
    candidates_ids = [aid for aid, d in tally.items() if d["paper_count"] >= min_papers]
    print(f"\nAuthors with ≥{min_papers} platform papers: {len(candidates_ids)}")

    if not candidates_ids:
        print("  No candidates — try lowering --min-papers")
        return

    # Batch-fetch author details for the filtered set
    print(f"Fetching author details for {len(candidates_ids)} candidates...")
    details = batch_fetch_author_details(candidates_ids)

    min_works = cfg["min_works_count"]
    candidates = []
    for aid in candidates_ids:
        d = tally[aid]
        det = details.get(aid, {})
        wc = det.get("works_count") or d.get("works_count")
        if wc is not None and wc < min_works:
            continue  # filter out students / postdocs by productivity proxy

        # Use fetched institution if better than the tally's first-seen institution
        inst = det.get("institution") or d["institution"]
        country = det.get("country") or d["country"]

        orcid_bare = d["orcid"].lower() if d["orcid"] else ""
        in_repo = (orcid_bare in known_orcids) or (aid in known_openalex_ids)

        candidates.append({
            **d,
            "institution": inst,
            "country": country,
            "works_count": det.get("works_count"),
            "cited_by_count": det.get("cited_by_count"),
            "h_index": det.get("h_index"),
            "in_repo": in_repo,
        })

    # Sort: not-in-repo first, then by cited_by_count desc
    candidates.sort(key=lambda c: (c["in_repo"], -(c["cited_by_count"] or 0)))

    not_in_repo = [c for c in candidates if not c["in_repo"]]
    in_repo = [c for c in candidates if c["in_repo"]]
    print(f"Candidates after filters: {len(candidates)} total "
          f"({len(not_in_repo)} new, {len(in_repo)} already in repo)")

    write_csv(candidates, platform)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--platform", choices=list(PLATFORM_QUERIES) + ["all"],
        default="all", help="Which platform to generate candidates for.",
    )
    parser.add_argument(
        "--max-works", type=int, default=600,
        help="Max works to fetch per keyword query (default 600).",
    )
    parser.add_argument(
        "--min-papers", type=int, default=2,
        help="Min platform-specific papers to be included (default 2).",
    )
    args = parser.parse_args()

    platforms = list(PLATFORM_QUERIES) if args.platform == "all" else [args.platform]
    for plat in platforms:
        run_platform(plat, args.max_works, args.min_papers)

    print("\nDone. Review CSVs in private/discovery/ before passing to Wave 2.")


if __name__ == "__main__":
    main()
