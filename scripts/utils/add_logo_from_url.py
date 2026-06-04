import sys
from pathlib import Path
import requests
import frontmatter

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / 'content' / 'institutions'
LOGO_DIR = ROOT / 'website' / 'static' / 'img' / 'institutions'
LOGO_DIR.mkdir(parents=True, exist_ok=True)


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


def main(inst_id: str, logo_url: str):
    md_path = CONTENT_DIR / f"{inst_id}.md"
    if not md_path.exists():
        print('md not found', md_path)
        return
    post = frontmatter.load(md_path)
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; QuantumLandscapeBot/1.0)'}
    resp = requests.get(logo_url, timeout=30, headers=headers)
    if resp.status_code >= 400:
        print('failed to download', resp.status_code)
        return
    ext = logo_url.split('.')[-1].split('?')[0]
    if ext.lower() not in ('png', 'jpg', 'jpeg', 'svg', 'webp'):
        ext = 'png'
    filename = f"{inst_id}.{ext}"
    dest = LOGO_DIR / filename
    dest.write_bytes(resp.content)

    media = post.get('media') or {}
    media['logo_path'] = f"/img/institutions/{filename}"
    post['media'] = media
    content = frontmatter.dumps(post)
    md_path.write_text(content, encoding='utf-8')

    evidence_path = md_path.with_suffix('.evidence.md')
    update_evidence(evidence_path, logo_url)
    print('updated', inst_id, '->', media['logo_path'])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: add_logo_from_url.py <inst_id> <logo_url>')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
