#!/usr/bin/env python3
"""Quick AcademicTree advisor lookup (token-efficient).

Approach:
- Use a SERP provider (SerpAPI) to search for `"{name}" site:academictree.org/physics`
- Fetch the person page HTML (requests)
- Extract advisor/mentor entries via simple CSS selectors and keyword search
- Return compact JSON with advisor names and source URLs (1-3 sentence quotes)

Usage:
  export SERPAPI_API_KEY=...
  python scripts/utils/academictree_lookup.py "Rainer Blatt"

Note: academictree.org may rate-limit or block bots; use SerpAPI to avoid heavy crawling.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import List

import requests
from bs4 import BeautifulSoup
import trafilatura

try:
    from serpapi import GoogleSearch
except Exception:
    GoogleSearch = None


def serp_find_academictree(name: str, api_key: str, num: int = 5) -> List[str]:
    if GoogleSearch is None:
        raise RuntimeError("serpapi package not installed or import failed")
    q = f'{name} site:academictree.org/physics'
    params = {"q": q, "api_key": api_key}
    search = GoogleSearch(params)
    data = search.get_dict()
    urls = []
    for item in data.get("organic_results", [])[:num]:
        link = item.get("link") or item.get("displayed_link")
        if link and "academictree.org" in link:
            urls.append(link)
    return urls


KEYWORDS = re.compile(r"advisor|supervisor|doctoral advisor|supervised by|mentored by", re.I)


def fetch_html(url: str, timeout: int = 10) -> str | None:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ionlandscape-bot/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def parse_academictree_person(html: str) -> dict:
    out = {"advisors": [], "other_roles": []}
    if not html:
        return out
    # Try trafilatura first for clean text
    main_text = trafilatura.extract(html) or ""
    # Small-pass: find lines with advisor keywords
    candidates = []
    for line in re.split(r"\n+", main_text):
        if KEYWORDS.search(line):
            s = " ".join(line.split())
            candidates.append(s)
    # HTML parse for links that may be parent nodes in the graph
    soup = BeautifulSoup(html, "lxml")
    # AcademicTree person pages often have a list or table of relations; search for anchors under 'Mentors' or similar
    for header in soup.find_all(["h2", "h3", "h4", "strong"]):
        txt = header.get_text(strip=True)
        if KEYWORDS.search(txt):
            # collect sibling links
            parent = header.parent
            if parent:
                links = parent.find_all("a")
                for a in links:
                    name = a.get_text(strip=True)
                    href = a.get("href")
                    if name:
                        out["advisors"].append({"name": name, "url": href})
    # fallback: regex-extracted candidate lines
    if not out["advisors"] and candidates:
        out["advisors_text"] = candidates[:5]
    return out


def lookup(name: str, num: int = 5) -> dict:
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        print("ERROR: set SERPAPI_API_KEY environment variable", file=sys.stderr)
        sys.exit(2)
    results = {"query": name, "candidates": []}
    urls = serp_find_academictree(name, api_key=api_key, num=num)
    for u in urls:
        html = fetch_html(u)
        parsed = parse_academictree_person(html)
        results["candidates"].append({"url": u, "parsed": parsed})
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("name", help="Person name to lookup on AcademicTree")
    p.add_argument("--num", type=int, default=5, help="Top N candidate pages to inspect")
    args = p.parse_args()
    out = lookup(args.name, num=args.num)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
