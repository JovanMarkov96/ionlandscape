#!/usr/bin/env python3
"""
validate_profiles.py — JSON-Schema validation for all three entity types.

Routes each profile to the right schema based on the directory it lives in:
  content/people/        → schemas/person.schema.json
  content/companies/     → schemas/company.schema.json
  content/institutions/  → schemas/institution.schema.json

Used by .github/workflows/validate_profiles.yml in CI.

Usage:
    python scripts/validation/validate_profiles.py            # all entity types
    python scripts/validation/validate_profiles.py --people   # subset
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"
CONTENT_DIR = ROOT / "content"

ENTITY_DIRS = {
    "people":       ("person",      CONTENT_DIR / "people",       SCHEMA_DIR / "person.schema.json"),
    "companies":    ("company",     CONTENT_DIR / "companies",    SCHEMA_DIR / "company.schema.json"),
    "institutions": ("institution", CONTENT_DIR / "institutions", SCHEMA_DIR / "institution.schema.json"),
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def parse_frontmatter(fpath):
    text = fpath.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return {"__yaml_error__": str(e)}


def validate_dir(label, entity_type, content_dir, schema_path):
    if not content_dir.exists():
        print(f"  (no {label} directory)")
        return 0, 0
    if not schema_path.exists():
        print(f"  FAILschema missing: {schema_path}")
        return 0, 1

    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)
    validator = jsonschema.Draft7Validator(schema)

    files = sorted(content_dir.glob("*.md"))
    failed = 0
    for fpath in files:
        meta = parse_frontmatter(fpath)
        if meta is None:
            print(f"  FAIL{fpath.name}: no frontmatter")
            failed += 1
            continue
        if isinstance(meta, dict) and "__yaml_error__" in meta:
            print(f"  FAIL{fpath.name}: YAML error: {meta['__yaml_error__']}")
            failed += 1
            continue

        errors = list(validator.iter_errors(meta))
        if errors:
            print(f"  FAIL{fpath.name}:")
            for err in errors:
                path = ".".join(str(p) for p in err.absolute_path) or "(root)"
                print(f"     [{path}] {err.message}")
            failed += 1

    print(f"  {label}: {len(files)} files, {failed} failed")
    return len(files), failed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--people",       action="store_true")
    ap.add_argument("--companies",    action="store_true")
    ap.add_argument("--institutions", action="store_true")
    args = ap.parse_args()

    if not HAS_JSONSCHEMA:
        print("ERROR: jsonschema not installed (pip install jsonschema)")
        sys.exit(2)

    selected = [k for k in ("people", "companies", "institutions") if getattr(args, k)]
    if not selected:
        selected = ["people", "companies", "institutions"]

    print("Validating profiles against v2/v1 schemas")
    total = 0
    total_failed = 0
    for label in selected:
        entity_type, content_dir, schema_path = ENTITY_DIRS[label]
        print(f"\n-- {label} ({entity_type}) --")
        n, f = validate_dir(label, entity_type, content_dir, schema_path)
        total += n
        total_failed += f

    print()
    print("-" * 50)
    print(f"Total: {total} files, {total_failed} failed")
    if total_failed:
        sys.exit(1)
    print("OK: all valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
