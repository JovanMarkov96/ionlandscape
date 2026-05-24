import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import frontmatter
import requests
from bs4 import BeautifulSoup

ROOT = Path('d:/OneDrive - weizmann.ac.il/GitHub/ionlandscape')
CONTENT_DIR = ROOT / 'content' / 'institutions'
LOGO_DIR = ROOT / 'website' / 'static' / 'img' / 'institutions'
LOGO_DIR.mkdir(parents=True, exist_ok=True)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': UA})

KEYWORDS = ['logo', 'brand', 'site-logo', 'header-logo', 'navbar', 'branding']


def score_candidate(src, attrs):
    attrs_lower = attrs.lower()
    score = 0
    if 'logo' in attrs_lower:
        score += 5
    if 'brand' in attrs_lower:
        score += 3
    if 'navbar' in attrs_lower or 'header' in attrs_lower:
        score += 1
    if 'logo' in src.lower():
        score += 4
    if src.lower().endswith('.svg'):
        score += 3
    if src.lower().endswith('.png'):
        score += 2
    if src.lower().endswith('.webp'):
        score += 1
    return score


def find_logo_url(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    candidates = []
    for img in soup.find_all('img'):
        src = img.get('src') or ''
        if not src:
            continue
        attrs = ' '.join([
            img.get('alt') or '',
            ' '.join(img.get('class') or []),
            img.get('id') or '',
            src
        ])
        if not any(k in attrs.lower() for k in KEYWORDS):
            continue
        score = score_candidate(src, attrs)
        candidates.append((score, src))

    if not candidates:
        return None

    candidates.sort(reverse=True, key=lambda x: x[0])
    best_src = candidates[0][1]
    return urljoin(base_url, best_src)


def infer_extension(url, content_type):
    url_path = urlparse(url).path
    ext = Path(url_path).suffix.lower().lstrip('.')
    if ext in {'svg', 'png', 'jpg', 'jpeg', 'webp'}:
        return 'jpg' if ext == 'jpeg' else ext
    if content_type:
        ct = content_type.lower()
        if 'svg' in ct:
            return 'svg'
        if 'png' in ct:
            return 'png'
        if 'jpeg' in ct or 'jpg' in ct:
            return 'jpg'
        if 'webp' in ct:
            return 'webp'
    return 'png'


def update_evidence(evidence_path, logo_url):
    if evidence_path.exists():
        text = evidence_path.read_text(encoding='utf-8')
    else:
        text = '---\n---\n\n# Evidence Map\n\n'

    if '## Sources' not in text:
        text = text.rstrip() + '\n\n## Sources\n'

    if logo_url not in text:
        text = text.rstrip() + f"\n- Logo: {logo_url}\n"

    evidence_path.write_text(text, encoding='utf-8')


success = []
failed = []

for md_path in sorted(CONTENT_DIR.glob('i*.md')):
    post = frontmatter.load(md_path)
    media = post.get('media') or {}
    if media.get('logo_path'):
        continue

    links = post.get('links') or {}
    website = links.get('website') or ''
    if not website.startswith('http'):
        failed.append((post.get('id'), 'no_website'))
        continue

    try:
        resp = SESSION.get(website, timeout=15)
        if resp.status_code >= 400:
            failed.append((post.get('id'), f'http_{resp.status_code}'))
            continue
        logo_url = find_logo_url(resp.text, website)
        if not logo_url:
            failed.append((post.get('id'), 'no_logo_found'))
            continue

        logo_resp = SESSION.get(logo_url, timeout=15)
        if logo_resp.status_code >= 400:
            failed.append((post.get('id'), f'logo_http_{logo_resp.status_code}'))
            continue

        ext = infer_extension(logo_url, logo_resp.headers.get('content-type', ''))
        filename = f"{post.get('id')}.{ext}"
        dest = LOGO_DIR / filename
        dest.write_bytes(logo_resp.content)

        media['logo_path'] = f"/img/institutions/{filename}"
        post['media'] = media
        frontmatter.dump(post, md_path.open('w', encoding='utf-8'))

        evidence_path = md_path.with_suffix('.evidence.md')
        update_evidence(evidence_path, logo_url)

        success.append((post.get('id'), logo_url))
        time.sleep(0.4)
    except Exception as exc:
        failed.append((post.get('id'), f'error:{exc}'))

print('success', len(success))
print('failed', len(failed))
if failed:
    print('failed_ids', failed[:10])
