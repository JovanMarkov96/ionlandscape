#!/usr/bin/env python3
"""DuckDuckGo-based, token-efficient SERP -> page extractor.

This is a free, open-source alternative to SerpAPI for running web searches
without an API key. It queries DuckDuckGo (via the `duckduckgo_search` package),
fetches top result pages, extracts the main text with `trafilatura`, and returns
short candidate sentences mentioning advisor/supervisor keywords.

Usage:
  python scripts/utils/ddg_extract.py "Name PhD advisor" --num 5
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import List

import requests
import trafilatura
ADVISOR_KEYWORDS = re.compile(r"\b(advisor|supervisor|supervised by|doctoral advisor|thesis|PhD supervisor|Ph\.D\. supervisor|doctoral supervisor)\b", re.I)


def search_ddg(query: str, num: int = 5) -> List[dict]:
    """Lightweight DuckDuckGo HTML search (no external package).

    Uses the DuckDuckGo HTML results endpoint to avoid JS and APIs.
    Returns a list of {title, snippet, url}.
    """
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; quantum-landscape-bot/1.0)"}
    try:
        r = requests.post(url, data=params, headers=headers, timeout=15)
        r.raise_for_status()
        html = r.text
    except Exception:
        return []
    # Find result blocks: look for <a rel="nofollow" class="result__a" href="..."> or generic <a href="/l/?kh=-1&uddg=...">
    results = []
    # simple regex to find <a ... href="...">text</a>
    for match in re.finditer(r'<a[^>]+href="(?P<h>https?://[^"]+)"[^>]*>(?P<t>.*?)</a>', html, re.I | re.S):
        if len(results) >= num:
            break
        href = match.group("h")
        title = re.sub(r'<.*?>', '', match.group("t")).strip()
        # snippet: try to find nearby <a> sibling isn't reliable; leave empty
        results.append({"title": title, "snippet": "", "url": href})
    return results


def fetch_page(url: str, timeout: int = 10) -> str | None:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; quantum-landscape-bot/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def extract_candidate_sentences(text: str) -> List[str]:
    if not text:
        return []
    main = trafilatura.extract(text) or text
    sentences = re.split(r'(?<=[.!?])\s+', main)
    candidates = []
    for s in sentences:
        if ADVISOR_KEYWORDS.search(s):
            cleaned = " ".join(s.split())
            candidates.append(cleaned)
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def run(query: str, num: int = 5):
    results = search_ddg(query, num=num)
    output = []
    for r in results:
        url = r.get("url")
        snippet = r.get("snippet")
        title = r.get("title")
        page_html = fetch_page(url) if url else None
        candidates = extract_candidate_sentences(page_html)
        if not candidates and snippet and ADVISOR_KEYWORDS.search(snippet):
            candidates = [snippet]
        output.append({"title": title, "url": url, "candidates": candidates[:5]})
    print(json.dumps({"query": query, "results": output}, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query", help="Search query (e.g. 'Name PhD advisor')")
    p.add_argument("--num", type=int, default=5, help="Top N DDG results to fetch")
    args = p.parse_args()
    run(args.query, num=args.num)


if __name__ == "__main__":
    main()
