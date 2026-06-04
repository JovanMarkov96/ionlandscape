#!/usr/bin/env python3
"""Lightweight, token-efficient SERP -> page extractor for advisor lookup.

Usage: set environment variable `SERPAPI_API_KEY`, then:
  python scripts/utils/serp_extract.py "Jonathan Home PhD advisor" --num 5

This script:
- queries SerpAPI for top results (compact JSON only)
- fetches each target page (requests)
- extracts main text with trafilatura
- returns short candidate sentences that mention advisor/supervisor/thesis
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import List

import requests
import trafilatura

try:
    from serpapi import GoogleSearch
except Exception:
    GoogleSearch = None


def search_serpapi(query: str, api_key: str, num: int = 5) -> List[dict]:
    if GoogleSearch is None:
        raise RuntimeError("serpapi package not installed or import failed")
    params = {"q": query, "api_key": api_key}
    search = GoogleSearch(params)
    data = search.get_dict()
    results = []
    for item in data.get("organic_results", [])[:num]:
        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "url": item.get("link") or item.get("displayed_link"),
        })
    return results


def fetch_page(url: str, timeout: int = 10) -> str | None:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; quantum-landscape-bot/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


ADVISOR_KEYWORDS = re.compile(r"\b(advisor|supervisor|supervised by|doctoral advisor|thesis|PhD supervisor|Ph\.D\. supervisor|doctoral supervisor)\b", re.I)


def extract_candidate_sentences(text: str) -> List[str]:
    if not text:
        return []
    # Use trafilatura to extract main content if HTML passed in
    main = trafilatura.extract(text) or text
    # split into sentences (simple split; designed for short extracts)
    sentences = re.split(r'(?<=[.!?])\s+', main)
    candidates = []
    for s in sentences:
        if ADVISOR_KEYWORDS.search(s):
            cleaned = " ".join(s.split())
            if len(cleaned) <= 1000:
                candidates.append(cleaned)
    # dedupe while preserving order
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def run(query: str, num: int = 5):
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        print("ERROR: set SERPAPI_API_KEY environment variable", file=sys.stderr)
        sys.exit(2)

    results = search_serpapi(query, api_key=api_key, num=num)
    output = []
    for r in results:
        url = r.get("url")
        snippet = r.get("snippet")
        title = r.get("title")
        page_html = fetch_page(url) if url else None
        candidates = extract_candidate_sentences(page_html)
        # If none found in full page, fall back to snippet
        if not candidates and snippet and ADVISOR_KEYWORDS.search(snippet):
            candidates = [snippet]
        output.append({"title": title, "url": url, "candidates": candidates[:5]})

    print(json.dumps({"query": query, "results": output}, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query", help="Search query (e.g. 'Name PhD advisor')")
    p.add_argument("--num", type=int, default=5, help="Top N SERP results to fetch")
    args = p.parse_args()
    run(args.query, num=args.num)


if __name__ == "__main__":
    main()
