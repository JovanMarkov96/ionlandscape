from pathlib import Path
import frontmatter

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / 'content' / 'institutions'
LOGO_DIR = ROOT / 'website' / 'static' / 'img' / 'institutions'


def update_evidence(evidence_path: Path, note: str) -> None:
    if evidence_path.exists():
        text = evidence_path.read_text(encoding='utf-8')
    else:
        text = '---\n---\n\n# Evidence Map\n\n'

    if '## Sources' not in text:
        text = text.rstrip() + '\n\n## Sources\n'

    if note not in text:
        text = text.rstrip() + f"\n- {note}\n"

    evidence_path.write_text(text, encoding='utf-8')


def main():
    updated = 0
    for md_path in sorted(CONTENT_DIR.glob('i*.md')):
        if md_path.name.endswith('.evidence.md'):
            continue
        post = frontmatter.load(md_path)
        media = post.get('media') or {}
        if media.get('logo_path'):
            continue
        inst_id = post.get('id') or md_path.stem
        # find matching file in LOGO_DIR
        matches = list(LOGO_DIR.glob(f"{inst_id}.*"))
        if not matches:
            continue
        # pick first match
        rel = f"/img/institutions/{matches[0].name}"
        media['logo_path'] = rel
        post['media'] = media
        content = frontmatter.dumps(post)
        md_path.write_text(content, encoding='utf-8')
        evidence_path = md_path.with_suffix('.evidence.md')
        update_evidence(evidence_path, f'Logo populated from assets: {matches[0].name}')
        updated += 1
        print('updated', md_path.name, '->', rel)
    print('total updated', updated)


if __name__ == '__main__':
    main()
