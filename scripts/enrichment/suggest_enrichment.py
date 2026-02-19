#!/usr/bin/env python3
"""
suggest_enrichment.py

Scans all Ion Landscape profiles for missing fields, prepares LLM enrichment
prompts, and outputs structured suggestions.

This script is designed for CI integration (GitHub Actions) and local use.

Usage:
    python scripts/suggest_enrichment.py --dry-run
    python scripts/suggest_enrichment.py --call-llm
"""

import os
import re
import sys
import json
import glob
import yaml
import argparse
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_DIR = os.path.join(ROOT_DIR, "content", "people")
DEFAULT_OUTPUT = os.path.join(ROOT_DIR, "reports", "suggestions.json")
PROMPT_TEMPLATE_PATH = os.path.join(ROOT_DIR, "scripts", "prompt_templates", "enrich_profile_prompt.txt")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def load_prompt_template():
    if not os.path.exists(PROMPT_TEMPLATE_PATH):
        raise FileNotFoundError(f"Missing prompt template: {PROMPT_TEMPLATE_PATH}")
    with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def parse_frontmatter(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}

def extract_missing_fields(meta):
    missing = []
    
    # Check Links
    links = meta.get("links", {}) or {}
    for key in ["orcid", "google_scholar", "homepage", "group_page"]:
        if not links.get(key):
            missing.append(f"links.{key}")

    # Check Education (PhD)
    has_advisor = False
    has_phd_year = False
    for edu in meta.get("education", []) or []:
        deg = str(edu.get("degree", ""))
        if "PhD" in deg:
            if edu.get("advisor"): has_advisor = True
            if edu.get("year"): has_phd_year = True
    
    if not has_advisor: missing.append("education.phd_advisor")
    if not has_phd_year: missing.append("education.phd_year")

    # Check Thesis Metadata
    thesis = meta.get("thesis", {}) or {}
    if not thesis.get("title"): missing.append("thesis.title")
    if not thesis.get("link"): missing.append("thesis.link")

    return missing

def _format_known_info(meta):
    lines = []
    if meta.get("group_type"): lines.append(f"- Group Type: {meta['group_type']}")
    if meta.get("ion_species"): lines.append(f"- Ion Species: {', '.join(meta['ion_species'])}")
    if meta.get("platforms"): lines.append(f"- Platforms: {', '.join(meta['platforms'])}")
    if meta.get("keywords"): lines.append(f"- Keywords: {', '.join(meta['keywords'])}")
    
    # existing education
    for edu in meta.get("education", []) or []:
        lines.append(f"- Education: {edu.get('degree')} at {edu.get('institution')} ({edu.get('year')})")
        
    return "\n".join(lines) if lines else "(None)"

def call_llm_stub(prompt):
    # This is a stub for the actual LLM call.
    # In production, replace this with requests to OpenAI/Anthropic/Ollama API.
    return {
        "suggestions": {
            "demo_field": {
                "value": None,
                "confidence": "not_found",
                "source": "LLM stub",
                "note": "Real API call not enabled yet"
            }
        }
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print prompts only")
    parser.add_argument("--call-llm", action="store_true", help="Simulate LLM call")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    template = load_prompt_template()
    all_suggestions = []

    for fpath in sorted(files):
        meta = parse_frontmatter(fpath)
        pid = meta.get("id", os.path.basename(fpath).replace(".md", ""))
        name = meta.get("name", "Unknown")
        positions = meta.get("current_position", {})
        institution = positions.get("institution", "Unknown")
        loc = meta.get("location", {})
        country = loc.get("country",CodeContent: "Unknown")

        missing = extract_missing_fields(meta)
        if not missing:
            continue

        prompt = template.format(
            name=name,
            institution=institution,
            country=country,
            profile_id=pid,
            known_info=_format_known_info(meta),
            missing_fields="\n".join([f"- {m}" for m in missing])
        )

        if args.dry_run:
            print(f"--- Prompt for {pid} ---")
            print(prompt)
            print("\n")
            continue

        if args.call_llm:
            # Here we would call the real LLM API
            # result = call_openai(prompt)
            result = call_llm_stub(prompt)
            
            # Format output structure
            entry = {
                "profile_id": pid,
                "review_status": "pending",
                "generated_at": datetime.now().isoformat(),
                "suggestions": result.get("suggestions", {})
            }
            all_suggestions.append(entry)

    if not args.dry_run and all_suggestions:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"items": all_suggestions}, f, indent=2)
        print(f"✅ Wrote {len(all_suggestions)} suggestions to {args.output}")

if __name__ == "__main__":
    main()
