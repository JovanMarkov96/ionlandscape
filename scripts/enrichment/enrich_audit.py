#!/usr/bin/env python3
"""
enrich_audit.py — Stage 3 triage and enrichment-priority scoring.

Scans all people, companies, and institutions. For each entry computes:
  - connectivity score  (how often the entity is referenced by others)
  - field completeness  (% of recommended fields that are non-empty)
  - enrichment tier     (A = high-leverage, B = normal, C = stub/thin)

Outputs:
  reports/enrichment_audit.md   — human-readable priority table
  reports/enrichment_audit.json — machine-readable priority data

Usage:
    python scripts/enrichment/enrich_audit.py
    python scripts/enrichment/enrich_audit.py --json-only
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "content"
REPORTS_DIR = ROOT / "reports"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)

# ---------------------------------------------------------------------------
# Recommended fields per entity type (non-trivial, enrichment-worthy)
# ---------------------------------------------------------------------------

PERSON_RECOMMENDED = [
    "applications", "ion_species", "current_position", "education",
    "key_papers", "lineage_check", "links.google_scholar", "links.orcid",
    "links.homepage", "links.group_page", "thesis.title", "thesis.link",
    "postdocs", "affiliations", "last_verified_at", "verification_source_count",
]

COMPANY_RECOMMENDED = [
    "founded_year", "short_summary", "approach", "focus_areas", "products",
    "people.founders", "people.leadership", "funding", "milestones",
    "offices", "partnerships", "links.website", "links.linkedin",
    "last_verified_at", "verification_source_count", "applications",
]

INSTITUTION_RECOMMENDED = [
    "short_description", "platforms_represented", "applications_represented",
    "group_count", "leadership", "national_programs", "networks",
    "links.department", "links.quantum_center", "news",
    "last_verified_at", "verification_source_count",
]


def parse_frontmatter(fpath):
    text = fpath.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def get_nested(d, dotpath):
    """Retrieve a value from a nested dict using a dot-separated path."""
    parts = dotpath.split(".")
    cur = d
    for p in parts:
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur


def is_populated(value):
    """Check if a value counts as 'populated' (non-null, non-empty)."""
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    if isinstance(value, list) and len(value) == 0:
        return False
    if isinstance(value, dict) and all(v is None or v == "" or v == [] for v in value.values()):
        return False
    return True


def field_completeness(meta, recommended_fields):
    """Return (populated_count, total_count, missing_field_names)."""
    populated = 0
    missing = []
    for field in recommended_fields:
        val = get_nested(meta, field)
        if is_populated(val):
            populated += 1
        else:
            missing.append(field)
    return populated, len(recommended_fields), missing


# ---------------------------------------------------------------------------
# Connectivity scoring
# ---------------------------------------------------------------------------

def load_all_entries():
    """Load all entries grouped by type."""
    entries = {"people": [], "companies": [], "institutions": []}
    for etype, subdir in [("people", "people"), ("companies", "companies"), ("institutions", "institutions")]:
        d = CONTENT_DIR / subdir
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name.endswith(".evidence.md"):
                continue
            meta = parse_frontmatter(f)
            if meta:
                meta["_file"] = f.name
                meta["_has_evidence"] = (f.parent / f.name.replace(".md", ".evidence.md")).exists()
                entries[etype].append(meta)
    return entries


def compute_person_connectivity(entries):
    """Count how often each person's name or id appears across all entries."""
    scores = defaultdict(int)
    all_people = entries["people"]

    # Build name→id map
    name_to_id = {}
    for p in all_people:
        pid = p.get("id", "")
        name = p.get("name", "")
        name_to_id[name.lower()] = pid
        # Also index last name
        parts = name.split()
        if parts:
            name_to_id[parts[-1].lower()] = pid

    # Scan all people for advisor / postdoc references
    for p in all_people:
        pid = p.get("id", "")
        for edu in p.get("education", []) or []:
            advisor = edu.get("advisor") or ""
            advisor_id = edu.get("advisor_id") or ""
            if advisor_id:
                scores[advisor_id] += 2  # direct id reference
            elif advisor:
                target = name_to_id.get(advisor.lower())
                if target and target != pid:
                    scores[target] += 1

        for pd in p.get("postdocs", []) or []:
            advisor = pd.get("advisor") or ""
            advisor_id = pd.get("advisor_id") or ""
            if advisor_id:
                scores[advisor_id] += 2
            elif advisor:
                target = name_to_id.get(advisor.lower())
                if target and target != pid:
                    scores[target] += 1

    # Scan institutions for member/alumni references
    for inst in entries["institutions"]:
        directory = inst.get("directory") or {}
        for member_file in (directory.get("current_members") or []):
            member_id = member_file.replace(".md", "")
            scores[member_id] += 1
        for alumni_file in (directory.get("alumni") or []):
            alumni_id = alumni_file.replace(".md", "")
            scores[alumni_id] += 1

    # Scan companies for founder references
    for co in entries["companies"]:
        people_block = co.get("people") or {}
        for founder in people_block.get("founders") or []:
            fpid = founder.get("person_id")
            if fpid:
                scores[fpid] += 2

    return scores


def compute_institution_connectivity(entries):
    """Score institutions by directory size + cross-references."""
    scores = defaultdict(int)
    for inst in entries["institutions"]:
        iid = inst.get("id", "")
        directory = inst.get("directory") or {}
        scores[iid] += len(directory.get("current_members") or [])
        scores[iid] += len(directory.get("alumni") or [])
        scores[iid] += len(directory.get("company_spinouts") or [])

    # People affiliations pointing to institutions
    for p in entries["people"]:
        for aff in p.get("affiliations") or []:
            eid = aff.get("entity_id") or ""
            if eid.startswith("i"):
                scores[eid] += 1

    return scores


def compute_company_connectivity(entries):
    """Score companies by cross-references."""
    scores = defaultdict(int)
    for p in entries["people"]:
        for aff in p.get("affiliations") or []:
            eid = aff.get("entity_id") or ""
            if eid.startswith("c"):
                scores[eid] += 1

    for co in entries["companies"]:
        cid = co.get("id", "")
        people_block = co.get("people") or {}
        scores[cid] += len(people_block.get("founders") or [])
        scores[cid] += len(people_block.get("leadership") or [])
        funding = co.get("funding") or {}
        if funding.get("rounds"):
            scores[cid] += len(funding["rounds"])

    return scores


def assign_tier(connectivity, completeness_pct, has_evidence):
    """Assign enrichment priority tier."""
    if has_evidence and completeness_pct >= 70:
        return "A-done"  # already enriched
    if connectivity >= 3 or completeness_pct < 30:
        return "A"       # high priority
    if connectivity >= 1 or completeness_pct < 60:
        return "B"       # normal priority
    return "C"           # low priority / already decent


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(entries, person_conn, inst_conn, co_conn):
    lines = []
    lines.append("# Enrichment Audit Report")
    lines.append(f"\nGenerated: {date.today().isoformat()}\n")

    json_data = {"generated": date.today().isoformat(), "people": [], "companies": [], "institutions": []}

    # --- People ---
    lines.append("## People (79 entries)")
    lines.append("")
    lines.append("| Tier | ID | Name | Connectivity | Completeness | Evidence | Missing |")
    lines.append("|------|-----|------|:---:|:---:|:---:|---------|")

    people_rows = []
    for p in entries["people"]:
        pid = p.get("id", "?")
        name = p.get("name", "?")
        conn = person_conn.get(pid, 0)
        pop, total, missing = field_completeness(p, PERSON_RECOMMENDED)
        pct = round(100 * pop / total) if total else 0
        has_ev = p.get("_has_evidence", False)
        tier = assign_tier(conn, pct, has_ev)
        people_rows.append((tier, pid, name, conn, pct, has_ev, missing))
        json_data["people"].append({
            "id": pid, "name": name, "connectivity": conn,
            "completeness_pct": pct, "has_evidence": has_ev,
            "tier": tier, "missing": missing,
        })

    # Sort: A first, then A-done, B, C; within tier by connectivity desc
    tier_order = {"A": 0, "A-done": 1, "B": 2, "C": 3}
    people_rows.sort(key=lambda r: (tier_order.get(r[0], 9), -r[3], -r[4]))
    for tier, pid, name, conn, pct, has_ev, missing in people_rows:
        ev_mark = "✅" if has_ev else "❌"
        miss_str = ", ".join(missing[:4])
        if len(missing) > 4:
            miss_str += f" (+{len(missing)-4})"
        lines.append(f"| {tier} | `{pid}` | {name} | {conn} | {pct}% | {ev_mark} | {miss_str} |")

    # --- Companies ---
    lines.append("")
    lines.append("## Companies (15 entries)")
    lines.append("")
    lines.append("| Tier | ID | Name | Connectivity | Completeness | Missing |")
    lines.append("|------|-----|------|:---:|:---:|---------|")

    co_rows = []
    for c in entries["companies"]:
        cid = c.get("id", "?")
        name = c.get("name", "?")
        conn = co_conn.get(cid, 0)
        pop, total, missing = field_completeness(c, COMPANY_RECOMMENDED)
        pct = round(100 * pop / total) if total else 0
        tier = "A" if conn >= 2 or pct < 40 else "B"
        co_rows.append((tier, cid, name, conn, pct, missing))
        json_data["companies"].append({
            "id": cid, "name": name, "connectivity": conn,
            "completeness_pct": pct, "tier": tier, "missing": missing,
        })

    co_rows.sort(key=lambda r: (0 if r[0] == "A" else 1, -r[3], -r[4]))
    for tier, cid, name, conn, pct, missing in co_rows:
        miss_str = ", ".join(missing[:4])
        if len(missing) > 4:
            miss_str += f" (+{len(missing)-4})"
        lines.append(f"| {tier} | `{cid}` | {name} | {conn} | {pct}% | {miss_str} |")

    # --- Institutions ---
    lines.append("")
    lines.append("## Institutions (59 entries)")
    lines.append("")
    lines.append("| Tier | ID | Name | Connectivity | Completeness | Missing |")
    lines.append("|------|-----|------|:---:|:---:|---------|")

    inst_rows = []
    for i in entries["institutions"]:
        iid = i.get("id", "?")
        name = i.get("name", "?")
        conn = inst_conn.get(iid, 0)
        pop, total, missing = field_completeness(i, INSTITUTION_RECOMMENDED)
        pct = round(100 * pop / total) if total else 0
        tier = "A" if conn >= 4 or pct < 30 else "B"
        inst_rows.append((tier, iid, name, conn, pct, missing))
        json_data["institutions"].append({
            "id": iid, "name": name, "connectivity": conn,
            "completeness_pct": pct, "tier": tier, "missing": missing,
        })

    inst_rows.sort(key=lambda r: (0 if r[0] == "A" else 1, -r[3], -r[4]))
    for tier, iid, name, conn, pct, missing in inst_rows:
        miss_str = ", ".join(missing[:4])
        if len(missing) > 4:
            miss_str += f" (+{len(missing)-4})"
        lines.append(f"| {tier} | `{iid}` | {name} | {conn} | {pct}% | {miss_str} |")

    # --- Summary ---
    a_people = sum(1 for r in people_rows if r[0] == "A")
    done_people = sum(1 for r in people_rows if r[0] == "A-done")
    a_co = sum(1 for r in co_rows if r[0] == "A")
    a_inst = sum(1 for r in inst_rows if r[0] == "A")

    lines.insert(2, f"**Summary**: {a_people} tier-A people ({done_people} already enriched), "
                    f"{a_co} tier-A companies, {a_inst} tier-A institutions.\n")

    return "\n".join(lines), json_data


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--json-only", action="store_true", help="Only emit JSON, skip markdown")
    args = ap.parse_args()

    entries = load_all_entries()
    print(f"Loaded: {len(entries['people'])} people, {len(entries['companies'])} companies, "
          f"{len(entries['institutions'])} institutions")

    person_conn = compute_person_connectivity(entries)
    inst_conn = compute_institution_connectivity(entries)
    co_conn = compute_company_connectivity(entries)

    report_md, report_json = generate_report(entries, person_conn, inst_conn, co_conn)

    REPORTS_DIR.mkdir(exist_ok=True)

    json_path = REPORTS_DIR / "enrichment_audit.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)
    print(f"[OK] JSON: {json_path}")

    if not args.json_only:
        md_path = REPORTS_DIR / "enrichment_audit.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"[OK] Markdown: {md_path}")


if __name__ == "__main__":
    main()
