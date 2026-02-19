#!/usr/bin/env python3
"""
validate_profiles.py

A script to validate Ion Landscape researcher profiles against the JSON Schema.
It parses YAML frontmatter from Markdown files and checks it against
schemas/profile.schema.json.

This script is used in GitHub Actions (validate_profiles.yml) to prevent
invalid data from merging.

Usage:
  python scripts/validate_profiles.py
"""

import os
import sys
import glob
import re
import json
import yaml
import argparse

# Try to import jsonschema; fall back to manual checks if missing
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_PATH = os.path.join(ROOT_DIR, "schemas", "profile.schema.json")
CONTENT_DIR = os.path.join(ROOT_DIR, "content", "people")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def load_schema():
    if not os.path.exists(SCHEMA_PATH):
        print(f"❌ Schema not found at {SCHEMA_PATH}")
        sys.exit(1)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_frontmatter(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        print(f"❌ YAML error in {os.path.basename(fpath)}: {e}")
        return None

def validate_profile(meta, schema, filename):
    errors = []
    
    if HAS_JSONSCHEMA:
        validator = jsonschema.Draft7Validator(schema)
        for error in validator.iter_errors(meta):
            path = ".".join(str(p) for p in error.path) or "root"
            errors.append(f"[{path}] {error.message}")
    else:
        # Fallback manual validation (simplified)
        required = schema.get("required", [])
        for field in required:
            if field not in meta:
                errors.append(f"Missing required field: {field}")
        
        # Check ORCID format if present
        orcid = (meta.get("links") or {}).get("orcid")
        if orcid and not re.match(r"^https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", orcid):
             errors.append(f"Invalid ORCID format: {orcid}")

    return errors

def main():
    print(f"🔍 Validating profiles in {CONTENT_DIR}...")
    
    if not HAS_JSONSCHEMA:
        print("⚠️  'jsonschema' library not found. Using limited manual validation.")
        print("   (Install with `pip install jsonschema` for full validation)")

    schema = load_schema()
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    
    failed_count = 0
    total_count = 0
    
    for fpath in sorted(files):
        total_count += 1
        fname = os.path.basename(fpath)
        meta = parse_frontmatter(fpath)
        
        if meta is None:
            print(f"❌ {fname}: Failed to parse frontmatter")
            failed_count += 1
            continue

        errors = validate_profile(meta, schema, fname)
        
        if errors:
            print(f"❌ {fname}:")
            for err in errors:
                print(f"  - {err}")
            failed_count += 1
        else:
            # print(f"✅ {fname}")
            pass

    print("-" * 40)
    print(f"Processed {total_count} profiles.")
    
    if failed_count > 0:
        print(f"❌ Validation FAILED: {failed_count} profiles have errors.")
        sys.exit(1)
    else:
        print("✅ Validation PASSED: All profiles are valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
