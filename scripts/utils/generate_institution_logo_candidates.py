import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / 'content' / 'institutions'
OUT_FILE = Path(__file__).resolve().parents[0] / 'institution_logo_candidates.json'

from scrape_institution_logos import (
    SESSION,
    find_logo_url,
    find_meta_or_icon,
    find_wikipedia_logo,
    search_wikipedia_for_institution,
)


def probe_website(url: str):
    try:
        # allow insecure SSL to probe more sites
        resp = SESSION.get(url, timeout=15, verify=False)
    except Exception as e:
        return {'error': str(e)}
    if resp.status_code >= 400:
        return {'status_code': resp.status_code}
    html = resp.text
    logo = find_logo_url(html, url)
    meta = find_meta_or_icon(html, url)
    inline_svg = None
    return {'logo': logo, 'meta': meta}


def main():
    results = {}
    for md_path in sorted(CONTENT_DIR.glob('i*.md')):
        if md_path.name.endswith('.evidence.md'):
            continue
        try:
            import frontmatter
            post = frontmatter.load(md_path)
        except Exception:
            continue
        inst_id = post.get('id') or md_path.stem
        name = post.get('name') or ''
        links = post.get('links') or {}
        website = links.get('website') or ''
        wiki = links.get('wikipedia') or ''
        entry = {'name': name, 'website': website, 'wiki_link': wiki}

        if website:
            entry['probe'] = probe_website(website)
        else:
            entry['probe'] = {'error': 'no_website'}

        # try searching wikipedia
        if not wiki:
            wiki_search = search_wikipedia_for_institution(name)
            entry['wiki_search'] = wiki_search
            if wiki_search:
                entry['wiki_logo'] = find_wikipedia_logo(wiki_search)
            else:
                entry['wiki_logo'] = None
        else:
            entry['wiki_search'] = wiki
            entry['wiki_logo'] = find_wikipedia_logo(wiki) or None

        results[inst_id] = entry

    OUT_FILE.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print('wrote', OUT_FILE)


if __name__ == '__main__':
    main()
