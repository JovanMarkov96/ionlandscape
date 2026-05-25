#!/usr/bin/env python3
"""
Fill missing institution `short_description` fields from Wikipedia.

For each institution in `website/static/data/institutions.json` that lacks a
`short_description`, this script will search Wikipedia for the institution's
name, fetch the introductory extract, and write it into the institution's
Markdown frontmatter (`content/institutions/<md_filename>`).

Run: py scripts/utils/fill_institution_descriptions_from_wikipedia.py
"""
import json
import os
import time
from pathlib import Path
import requests
import frontmatter

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'website' / 'static' / 'data' / 'institutions.json'
CONTENT_DIR = ROOT / 'content' / 'institutions'

WIKI_API = 'https://en.wikipedia.org/w/api.php'
# Use a descriptive User-Agent to avoid 403 responses from Wikimedia
HEADERS = {'User-Agent': 'IonLandscape/0.1 (https://github.com/JovanMarkov96)'}


def wiki_search(title):
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': title,
        'format': 'json',
        'srlimit': 1,
    }
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    hits = data.get('query', {}).get('search', [])
    if not hits:
        return None
    return hits[0].get('title')


def wiki_extract(title):
    params = {
        'action': 'query',
        'prop': 'extracts|pageprops|info',
        'inprop': 'url',
        'exintro': True,
        'explaintext': True,
        'titles': title,
        'format': 'json'
    }
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    pages = data.get('query', {}).get('pages', {})
    if not pages:
        return None
    page = next(iter(pages.values()))
    extract = page.get('extract', '').strip()
    fullurl = page.get('fullurl') or ''
    return extract, fullurl


def safe_write_frontmatter(md_path: Path, meta_updates: dict):
    post = frontmatter.load(md_path)
    meta = post.metadata or {}
    meta.update(meta_updates)
    post.metadata = meta
    # Use dumps to avoid bytes/str write issues
    content = frontmatter.dumps(post)
    md_path.write_text(content, encoding='utf-8')


def main():
    if not DATA_PATH.exists():
        print('institutions.json not found at', DATA_PATH)
        return
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    updated = 0
    for inst in data:
        short = inst.get('short_description') or ''
        md_fn = inst.get('md_filename')
        if not md_fn:
            continue
        md_path = CONTENT_DIR / md_fn
        if not md_path.exists():
            print('Missing md file for', md_fn)
            continue
        if short and short.strip():
            # already has description
            continue

        name = inst.get('name') or inst.get('sort_name') or inst.get('id')
        if not name:
            continue

        try:
            print('Searching Wikipedia for:', name)
            title = wiki_search(name)
            if not title:
                print('  No wiki hit for', name)
                continue
            print('  Found wiki page:', title)
            extract, url = wiki_extract(title)
            if not extract:
                print('  No extract for', title)
                continue

            # Use first paragraph as short_description (split on double newline)
            para = extract.split('\n\n')[0].strip()
            if len(para) > 1000:
                para = para[:1000].rsplit(' ', 1)[0] + '...'

            # Update frontmatter short_description and add source
            meta_upd = {'short_description': para}
            # Append source evidence
            post = frontmatter.load(md_path)
            sources = post.metadata.get('sources', []) if post.metadata else []
            src_entry = {'note': f'Imported short_description from Wikipedia ({title})', 'url': url}
            # Avoid duplicate
            if src_entry not in sources:
                sources.append(src_entry)
            meta_upd['sources'] = sources

            print('  Writing short_description to', md_fn)
            safe_write_frontmatter(md_path, meta_upd)
            updated += 1
            # Be polite to the API
            time.sleep(1.1)

        except Exception as e:
            print('Error for', name, e)

    print('Updated descriptions for', updated, 'institutions')


if __name__ == '__main__':
    main()
