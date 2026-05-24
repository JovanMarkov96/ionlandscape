from pathlib import Path
import frontmatter

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / 'content' / 'institutions'
LOGO_DIR = ROOT / 'website' / 'static' / 'img' / 'institutions'

def main():
    updated = 0
    for md_path in sorted(CONTENT_DIR.glob('i*.md')):
        if md_path.name.endswith('.evidence.md'):
            continue
        post = frontmatter.load(md_path)
        media = post.get('media') or {}
        inst_id = post.get('id') or md_path.stem
        mark = LOGO_DIR / f"{inst_id}_mark.png"
        if mark.exists():
            rel = f"/img/institutions/{mark.name}"
            if media.get('logo_path') != rel:
                media['logo_path'] = rel
                post['media'] = media
                md_path.write_text(frontmatter.dumps(post), encoding='utf-8')
                updated += 1
                print('set mark for', inst_id)
    print('total set', updated)

if __name__ == '__main__':
    main()
