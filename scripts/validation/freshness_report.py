#!/usr/bin/env python3
"""
freshness_report.py — scan all entities and emit a staleness queue.

For each entity type, lists entries sorted by last_verified_at (oldest / never
first), flagging anything past its staleness window. Metrics staleness is
tracked separately by scripts/enrich/metrics.py.

Windows (days):
  companies    90
  people      180
  institutions 365

Excludes:
  - Stubs (people whose id starts with 000- — lineage-only, no editable content)
  - .evidence. files (audit/evidence sidecars, not canonical entities)

Usage:
    python scripts/validation/freshness_report.py [--window-companies N]
                                                   [--window-people N]
                                                   [--window-institutions N]

Report: reports/freshness_report.md
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import frontmatter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR       = ROOT / "content" / "people"
INSTITUTIONS_DIR = ROOT / "content" / "institutions"
COMPANIES_DIR    = ROOT / "content" / "companies"
REPORT_PATH      = ROOT / "reports" / "freshness_report.md"

DEFAULT_WINDOWS = {"company": 90, "person": 180, "institution": 365}


# ── Per-entity staleness check ────────────────────────────────────────────────

def days_since(date_value) -> int | None:
    """Return days since date_value, or None if date_value is falsy/unparseable."""
    if not date_value:
        return None
    try:
        return (date.today() - date.fromisoformat(str(date_value))).days
    except (ValueError, TypeError):
        return None


def load_entities(content_dir: Path, entity_type: str, windows: dict, skip_prefix: str = None) -> list:
    results = []
    window = windows[entity_type]
    for path in sorted(content_dir.glob("*.md")):
        if ".evidence." in path.name:
            continue
        if skip_prefix and path.stem.startswith(skip_prefix):
            continue

        m = frontmatter.load(path).metadata
        eid  = m.get("id", path.stem)
        name = m.get("name", eid)
        lv   = m.get("last_verified_at")
        age  = days_since(lv)
        src_count = m.get("verification_source_count", 0) or 0

        if age is None:
            status = "never_verified"
        elif age > window:
            status = "stale"
        else:
            status = "fresh"

        results.append({
            "id": eid, "name": name, "type": entity_type,
            "last_verified_at": str(lv) if lv else None,
            "age_days": age, "window": window,
            "src_count": src_count, "status": status,
        })

    results.sort(key=lambda r: (
        {"never_verified": 0, "stale": 1, "fresh": 2}[r["status"]],
        -(r["age_days"] or 0),
    ))
    return results


# ── Report writer ─────────────────────────────────────────────────────────────

def write_report(all_results: list, windows: dict):
    today = date.today().isoformat()

    by_type = {}
    for r in all_results:
        by_type.setdefault(r["type"], []).append(r)

    lines = [
        "# Data Freshness Report",
        f"\nGenerated: {today}",
        f"\nStaleness windows — companies: {windows['company']}d  |  "
        f"people: {windows['person']}d  |  institutions: {windows['institution']}d\n",
    ]

    # Summary table
    lines.append("## Summary\n")
    lines.append("| Entity type | Total | Never verified | Stale | Fresh |")
    lines.append("|---|---|---|---|---|")
    for etype in ["company", "person", "institution"]:
        rs = by_type.get(etype, [])
        nv = sum(1 for r in rs if r["status"] == "never_verified")
        st = sum(1 for r in rs if r["status"] == "stale")
        fr = sum(1 for r in rs if r["status"] == "fresh")
        lines.append(f"| {etype.capitalize()}s | {len(rs)} | {nv} | {st} | {fr} |")
    lines.append("")

    # Per-type queues
    for etype, label, emoji in [
        ("company",     "Companies",    "🏢"),
        ("person",      "People",       "👤"),
        ("institution", "Institutions", "🏛️"),
    ]:
        rs = by_type.get(etype, [])
        if not rs:
            continue

        window = windows[etype]
        nv = [r for r in rs if r["status"] == "never_verified"]
        stale = [r for r in rs if r["status"] == "stale"]
        fresh = [r for r in rs if r["status"] == "fresh"]

        lines.append(f"\n## {emoji} {label}  (window: {window}d)\n")

        if nv:
            lines.append(f"### Never verified ({len(nv)})\n")
            for r in nv:
                lines.append(f"- `{r['id']}` — {r['name']}  _(sources: {r['src_count']})_")
            lines.append("")

        if stale:
            lines.append(f"### Stale — past {window}d window ({len(stale)})\n")
            for r in stale:
                lines.append(
                    f"- `{r['id']}` — {r['name']}  "
                    f"_(verified {r['age_days']}d ago on {r['last_verified_at']}, "
                    f"sources: {r['src_count']})_"
                )
            lines.append("")

        if fresh:
            lines.append(f"### Fresh — within {window}d ({len(fresh)})\n")
            for r in fresh:
                lines.append(
                    f"- `{r['id']}` — {r['name']}  "
                    f"_(verified {r['age_days']}d ago on {r['last_verified_at']}, "
                    f"sources: {r['src_count']})_"
                )
            lines.append("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report: {REPORT_PATH}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--window-companies",    type=int, default=DEFAULT_WINDOWS["company"],
                        metavar="N", help="Staleness window for companies (days, default 90)")
    parser.add_argument("--window-people",       type=int, default=DEFAULT_WINDOWS["person"],
                        metavar="N", help="Staleness window for people (days, default 180)")
    parser.add_argument("--window-institutions", type=int, default=DEFAULT_WINDOWS["institution"],
                        metavar="N", help="Staleness window for institutions (days, default 365)")
    args = parser.parse_args()

    windows = {
        "company":     args.window_companies,
        "person":      args.window_people,
        "institution": args.window_institutions,
    }

    all_results = []

    dirs = [
        (COMPANIES_DIR,    "company",     None),
        (PEOPLE_DIR,       "person",      "000-"),
        (INSTITUTIONS_DIR, "institution", None),
    ]

    for content_dir, etype, skip_prefix in dirs:
        rs = load_entities(content_dir, etype, windows, skip_prefix=skip_prefix)
        all_results.extend(rs)
        nv = sum(1 for r in rs if r["status"] == "never_verified")
        st = sum(1 for r in rs if r["status"] == "stale")
        fr = sum(1 for r in rs if r["status"] == "fresh")
        print(f"{etype.capitalize()}s ({len(rs)}): {nv} never verified, {st} stale, {fr} fresh")

    write_report(all_results, windows)


if __name__ == "__main__":
    main()
