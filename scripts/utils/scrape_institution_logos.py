import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import frontmatter
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / 'content' / 'institutions'
LOGO_DIR = ROOT / 'website' / 'static' / 'img' / 'institutions'
LOGO_DIR.mkdir(parents=True, exist_ok=True)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': UA})

KEYWORDS = ['logo', 'brand', 'site-logo', 'header-logo', 'navbar', 'branding', 'identity']


def score_candidate(src: str, attrs: str) -> int:
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


def find_logo_url(html: str, base_url: str) -> str | None:
    soup = BeautifulSoup(html, 'html.parser')
    candidates: list[tuple[int, str]] = []
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
        attrs_lower = attrs.lower()
        if not any(k in attrs_lower for k in KEYWORDS) and 'logo' not in src.lower():
            continue
        score = score_candidate(src, attrs)
        candidates.append((score, src))

    if not candidates:
        return None

    candidates.sort(reverse=True, key=lambda x: x[0])
    best_src = candidates[0][1]
    return urljoin(base_url, best_src)


def find_meta_or_icon(html: str, base_url: str) -> str | None:
    soup = BeautifulSoup(html, 'html.parser')
    # Common social image metadata
    metas = [
        ('property', 'og:logo'),
        ('property', 'og:image'),
        ('name', 'twitter:image'),
        ('name', 'twitter:image:src'),
        ('name', 'image')
    ]
    for attr, val in metas:
        tag = soup.find('meta', attrs={attr: val})
        if tag and tag.get('content'):
            return urljoin(base_url, tag.get('content'))

    # Check link rel icons
    for rel in ('icon', 'shortcut icon', 'apple-touch-icon', 'apple-touch-icon-precomposed'):
        tag = soup.find('link', rel=lambda r: r and rel in r)
        if tag and tag.get('href'):
            return urljoin(base_url, tag.get('href'))

    return None


def find_wikipedia_logo(wiki_url: str) -> str | None:
    try:
        resp = SESSION.get(wiki_url, timeout=15)
    except requests.RequestException:
        return None
    if resp.status_code >= 400:
        return None

    soup = BeautifulSoup(resp.text, 'html.parser')
    infobox = soup.find('table', class_=lambda c: c and 'infobox' in c)
    if not infobox:
        return None

    img = infobox.find('img')
    if not img:
        return None

    src = img.get('src')
    if not src:
        return None
    if src.startswith('//'):
        return f"https:{src}"
    return src


def search_wikipedia_for_institution(name: str) -> str | None:
    if not name:
        return None
    api = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': name,
        'format': 'json',
        'srlimit': 3,
    }
    try:
        resp = SESSION.get(api, params=params, timeout=15)
    except requests.RequestException:
        return None
    if resp.status_code >= 400:
        return None
    data = resp.json()
    results = data.get('query', {}).get('search', [])
    if not results:
        return None
    title = results[0].get('title')
    if not title:
        return None
    return f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"


def slug_to_name(slug: str) -> str:
    # slug like 'i002-aarhus-university' -> 'Aarhus University'
    parts = slug.split('-', 1)
    if len(parts) == 2:
        name_part = parts[1]
    else:
        name_part = slug
    name = name_part.replace('-', ' ')
    # simple title case, keep common uppercase tokens
    name = ' '.join([w.upper() if w.isupper() else w.capitalize() for w in name.split()])
    return name


def find_inline_logo_svg(html: str) -> str | None:
    soup = BeautifulSoup(html, 'html.parser')
    for svg in soup.find_all('svg'):
        attrs = ' '.join([
            svg.get('aria-label') or '',
            ' '.join(svg.get('class') or []),
            svg.get('id') or ''
        ]).lower()
        if any(k in attrs for k in KEYWORDS):
            return str(svg)
    return None


def infer_extension(url: str, content_type: str) -> str:
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


def update_evidence(evidence_path: Path, logo_url: str) -> None:
    if evidence_path.exists():
        text = evidence_path.read_text(encoding='utf-8')
    else:
        text = '---\n---\n\n# Evidence Map\n\n'

    if '## Sources' not in text:
        text = text.rstrip() + '\n\n## Sources\n'

    if logo_url not in text:
        text = text.rstrip() + f"\n- Logo: {logo_url}\n"

    evidence_path.write_text(text, encoding='utf-8')


def main() -> None:
    success: list[tuple[str, str]] = []
    failed: list[tuple[str, str]] = []

    for md_path in sorted(CONTENT_DIR.glob('i*.md')):
        if md_path.name.endswith('.evidence.md'):
            continue
        post = frontmatter.load(md_path)
        inst_id = post.get('id') or md_path.stem
        media = post.get('media') or {}
        if media.get('logo_path'):
            continue

        links = post.get('links') or {}
        website = links.get('website') or ''
        if not website.startswith('http'):
            website = ''

        print(f'Processing {inst_id} (file={md_path.name})')
        try:
            resp = None
            logo_url = None
            if website:
                try:
                    resp = SESSION.get(website, timeout=15)
                    if resp.status_code < 400:
                        logo_url = find_logo_url(resp.text, website)
                        if not logo_url:
                            # try meta tags and favicons as fallback
                            logo_url = find_meta_or_icon(resp.text, website)
                except Exception:
                    # ignore website fetch errors (SSL, timeouts) and try fallbacks
                    resp = None
            inline_svg = None
            if not logo_url and resp is not None:
                inline_svg = find_inline_logo_svg(resp.text)
            if not logo_url and not inline_svg:
                wiki_url = links.get('wikipedia') or ''
                if wiki_url:
                    logo_url = find_wikipedia_logo(wiki_url)
                else:
                    # try searching Wikipedia by name when no wiki link present
                    name = post.get('name') or ''
                    if not name:
                        name = slug_to_name(inst_id)
                    wiki_url = search_wikipedia_for_institution(name)
                    if wiki_url:
                        logo_url = find_wikipedia_logo(wiki_url)
            if not logo_url and not inline_svg:
                # final attempt: try meta/icon on an empty website by probing root
                if website:
                    meta_logo = find_meta_or_icon(resp.text if resp is not None else '', website)
                    if meta_logo:
                        logo_url = meta_logo
            if not logo_url and not inline_svg:
                failed.append((inst_id, 'no_logo_found'))
                continue

            print(f'  found logo_url={logo_url} inline_svg={bool(inline_svg)}')
            if inline_svg:
                if isinstance(inline_svg, bytes):
                    inline_svg = inline_svg.decode('utf-8', errors='ignore')
                filename = f"{inst_id}.svg"
                dest = LOGO_DIR / filename
                dest.write_text(inline_svg, encoding='utf-8')
            else:
                if logo_url.startswith('data:image/'):
                    header, data = logo_url.split(',', 1)
                    ext = header.split('/')[1].split(';')[0]
                    filename = f"{inst_id}.{ext}"
                    dest = LOGO_DIR / filename
                    dest.write_bytes(__import__('base64').b64decode(data))
                else:
                    logo_resp = SESSION.get(logo_url, timeout=15)
                    if logo_resp.status_code >= 400:
                        failed.append((inst_id, f'logo_http_{logo_resp.status_code}'))
                        continue

                    ext = infer_extension(logo_url, logo_resp.headers.get('content-type', ''))
                    filename = f"{inst_id}.{ext}"
                    dest = LOGO_DIR / filename
                    dest.write_bytes(logo_resp.content)

            media['logo_path'] = f"/img/institutions/{filename}"
            post['media'] = media
            # Use dumps + write_text to avoid binary/text write issues
            content = frontmatter.dumps(post)
            md_path.write_text(content, encoding='utf-8')

            evidence_path = md_path.with_suffix('.evidence.md')
            if logo_url:
                update_evidence(evidence_path, logo_url)

            success.append((inst_id, logo_url or 'inline_svg'))
            time.sleep(0.4)
        except Exception as exc:
            import traceback
            tb = traceback.format_exc()
            print(f'EXCEPTION for {inst_id}:')
            print(tb)
            failed.append((inst_id, f'error:{exc}'))

    print('success', len(success))
    print('failed', len(failed))
    if failed:
        print('failed_ids', failed[:10])


if __name__ == '__main__':
    main()
