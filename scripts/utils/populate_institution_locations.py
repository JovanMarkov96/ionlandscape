#!/usr/bin/env python3
"""
Populate missing `location.city` and `location.country` for institutions.

Approach:
1. For each institution missing `location.country`, search Wikipedia for the institution name.
2. Request page coordinates via the MediaWiki API; if coordinates found, reverse-geocode
   with Nominatim (OpenStreetMap) to obtain `city` and `country`.
3. If coordinates missing, request the page extract (intro) and try to parse "in City, Country" patterns.
4. Write updates into the institution Markdown frontmatter (`content/institutions/*.md`).

Notes:
- Uses courteous delays to avoid hammering external services.
- Nominatim requires a descriptive User-Agent; set `HEADERS` accordingly.

Run: py scripts/utils/populate_institution_locations.py
"""
import json
import re
import time
from pathlib import Path
import requests
import frontmatter

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'website' / 'static' / 'data' / 'institutions.json'
CONTENT_DIR = ROOT / 'content' / 'institutions'
WIKI_API = 'https://en.wikipedia.org/w/api.php'
NOMINATIM = 'https://nominatim.openstreetmap.org/reverse'
HEADERS = {
    'User-Agent': 'QuantumLandscape/0.1 (https://github.com/JovanMarkov96)'
}


def wiki_search(title):
    params = {'action': 'query', 'list': 'search', 'srsearch': title, 'format': 'json', 'srlimit': 1}
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    hits = r.json().get('query', {}).get('search', [])
    return hits[0].get('title') if hits else None


def wiki_coords(title):
    params = {'action': 'query', 'prop': 'coordinates', 'titles': title, 'colimit': 1, 'format': 'json'}
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    pages = r.json().get('query', {}).get('pages', {})
    if not pages:
        return None
    page = next(iter(pages.values()))
    coords = page.get('coordinates')
    if coords and isinstance(coords, list):
        c = coords[0]
        return float(c.get('lat')), float(c.get('lon'))
    return None


def wiki_intro(title):
    params = {'action': 'query', 'prop': 'extracts', 'exintro': True, 'explaintext': True, 'titles': title, 'format': 'json'}
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    pages = r.json().get('query', {}).get('pages', {})
    if not pages:
        return ''
    page = next(iter(pages.values()))
    return page.get('extract', '')


def reverse_geocode(lat, lon):
    params = {'format': 'jsonv2', 'lat': lat, 'lon': lon, 'zoom': 10, 'addressdetails': 1}
    r = requests.get(NOMINATIM, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def write_location(md_path: Path, location_update: dict):
    post = frontmatter.load(md_path)
    meta = post.metadata or {}
    loc = meta.get('location', {}) or {}
    loc.update(location_update)
    meta['location'] = loc
    post.metadata = meta
    content = frontmatter.dumps(post)
    md_path.write_text(content, encoding='utf-8')


def parse_intro_for_location(intro: str):
    # Look for patterns like "in City, Country" or "located in City, Country"
    m = re.search(r'\bin\s+([A-Z][A-Za-z\-\s\.\'"\(\)]+?),\s*([A-Z][A-Za-z\-\s\.]+)', intro)
    if m:
        city = m.group(1).strip()
        country = m.group(2).strip()
        return city, country
    # Try "located in Country" simple match
    m2 = re.search(r'located in ([A-Z][A-Za-z\-\s\.]+)', intro)
    if m2:
        country = m2.group(1).strip()
        return None, country
    return None, None


def main():
    if not DATA_PATH.exists():
        print('institutions.json not found at', DATA_PATH)
        return
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    updated = 0
    for inst in data:
        loc = inst.get('location') or {}
        if loc.get('country'):
            continue
        name = inst.get('name') or inst.get('sort_name') or inst.get('id')
        md_fn = inst.get('md_filename')
        if not md_fn:
            continue
        md_path = CONTENT_DIR / md_fn
        if not md_path.exists():
            print('Missing md file for', md_fn)
            continue

        print('Processing:', name)
        try:
            title = wiki_search(name)
            if title:
                # Try coords first
                coords = wiki_coords(title)
                if coords:
                    lat, lon = coords
                    print('  coords:', lat, lon)
                    geo = reverse_geocode(lat, lon)
                    addr = geo.get('address', {})
                    country = addr.get('country')
                    city = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('county')
                    location_update = {}
                    if city:
                        location_update['city'] = city
                    if country:
                        location_update['country'] = country
                    # add lat/lon
                    location_update['lat'] = lat
                    location_update['lon'] = lon
                    if location_update:
                        write_location(md_path, location_update)
                        updated += 1
                        print('  wrote location from coords:', location_update)
                        time.sleep(1.0)
                        continue

                # Fallback: parse intro
                intro = wiki_intro(title)
                city, country = parse_intro_for_location(intro)
                if city or country:
                    location_update = {}
                    if city:
                        location_update['city'] = city
                    if country:
                        location_update['country'] = country
                    write_location(md_path, location_update)
                    updated += 1
                    print('  wrote location from intro:', location_update)
                    time.sleep(0.9)
                    continue

            print('  no location found for', name)
            time.sleep(0.6)
        except Exception as e:
            print('  error for', name, e)
            time.sleep(0.8)

    print('Locations updated for', updated, 'institutions')


if __name__ == '__main__':
    import json
    main()
