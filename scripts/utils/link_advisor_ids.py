#!/usr/bin/env python3
"""Resolve advisor cross-links in people profiles.

This scans content/people/*.md, matches education[].advisor values against
existing person names/sort names, and fills advisor_id where an unambiguous
match exists. When a profile gains at least one advisor_id, lineage_check is
marked advisor_verified and last_checked is refreshed.

Usage:
  python scripts/utils/link_advisor_ids.py --write
  python scripts/utils/link_advisor_ids.py --report
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import unicodedata
from datetime import date

import frontmatter


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")


def normalize_name(value: str) -> str:
    if not value:
        return ""
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = re.sub(r"[\.,'’`\(\)\[\]\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def collect_people():
    people = []
    for file_path in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        post = frontmatter.load(file_path)
        meta = post.metadata
        person_id = meta.get("id")
        name = meta.get("name") or ""
        sort_name = meta.get("sort_name") or ""
        if not person_id:
            continue
        aliases = {normalize_name(name), normalize_name(sort_name)}
        people.append({
            "file_path": file_path,
            "id": person_id,
            "name": name,
            "sort_name": sort_name,
            "aliases": {alias for alias in aliases if alias},
        })
    return people


def build_lookup(people):
    lookup = {}
    ambiguous = set()
    for person in people:
        for alias in person["aliases"]:
            if alias in lookup and lookup[alias] != person["id"]:
                ambiguous.add(alias)
            else:
                lookup[alias] = person["id"]
    for alias in ambiguous:
        lookup.pop(alias, None)
    return lookup


def resolve_advisor(advisor: str, lookup: dict[str, str]) -> str | None:
    if not advisor:
        return None
    if ";" in advisor:
        return None
    advisor_norm = normalize_name(advisor)
    if not advisor_norm:
        return None
    if advisor_norm in lookup:
        return lookup[advisor_norm]
    # Heuristic: handle abbreviated middle initials by comparing token sets.
    advisor_tokens = advisor_norm.split()
    for alias, person_id in lookup.items():
        alias_tokens = alias.split()
        if len(alias_tokens) >= 2 and len(advisor_tokens) >= 2 and alias_tokens[0] == advisor_tokens[0] and alias_tokens[-1] == advisor_tokens[-1]:
            return person_id
    return None


def update_profile(file_path: str, lookup: dict[str, str]) -> list[str]:
    post = frontmatter.load(file_path)
    meta = post.metadata
    changed = []
    education = meta.get("education") or []
    matched_any = False

    for entry in education:
        if not isinstance(entry, dict):
            continue
        advisor = entry.get("advisor")
        if not advisor or entry.get("advisor_id"):
            continue
        advisor_id = resolve_advisor(advisor, lookup)
        if advisor_id:
            entry["advisor_id"] = advisor_id
            changed.append(f"advisor_id={advisor_id}")
            matched_any = True

    lineage_check = meta.get("lineage_check")
    if matched_any:
        if not isinstance(lineage_check, dict):
            lineage_check = {}
        if lineage_check.get("advisor_verified") is not True:
            lineage_check["advisor_verified"] = True
            changed.append("advisor_verified=true")
        lineage_check["last_checked"] = date.today().isoformat()
        changed.append("last_checked=today")
        meta["lineage_check"] = lineage_check

    if changed:
        post.metadata = meta
        with open(file_path, "wb") as handle:
            frontmatter.dump(post, handle)

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Link advisor_id values for people profiles.")
    parser.add_argument("--write", action="store_true", help="Write changes back to files")
    parser.add_argument("--report", action="store_true", help="Print a report of resolvable advisors")
    args = parser.parse_args()

    people = collect_people()
    lookup = build_lookup(people)

    total_matched = 0
    for person in people:
        post = frontmatter.load(person["file_path"])
        education = post.metadata.get("education") or []
        resolved = []
        for entry in education:
            if not isinstance(entry, dict):
                continue
            advisor = entry.get("advisor")
            if advisor and not entry.get("advisor_id"):
                advisor_id = resolve_advisor(advisor, lookup)
                if advisor_id:
                    resolved.append((advisor, advisor_id))
        if resolved and args.report:
            print(f"{person['id']} {person['name']}")
            for advisor, advisor_id in resolved:
                print(f"  {advisor} -> {advisor_id}")
        if args.write:
            changes = update_profile(person["file_path"], lookup)
            if changes:
                total_matched += 1
                print(f"updated {person['id']}: {', '.join(changes)}")

    if args.write:
        print(f"updated {total_matched} profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())