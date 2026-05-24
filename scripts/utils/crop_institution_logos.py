from pathlib import Path
from PIL import Image
import frontmatter

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / 'content' / 'institutions'
LOGO_DIR = ROOT / 'website' / 'static' / 'img' / 'institutions'

EXTS_RASTER = ('.png', '.jpg', '.jpeg', '.webp')


def crop_center_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    return img.crop((left, top, left + s, top + s))


def main():
    updated = 0
    for md_path in sorted(CONTENT_DIR.glob('i*.md')):
        if md_path.name.endswith('.evidence.md'):
            continue
        post = frontmatter.load(md_path)
        inst_id = post.get('id') or md_path.stem
        media = post.get('media') or {}
        src_path = None

        # prefer existing media.logo_path
        logo_path = media.get('logo_path')
        if logo_path:
            candidate = (ROOT / 'website' / logo_path.lstrip('/'))
            if candidate.exists() and candidate.suffix.lower() in EXTS_RASTER:
                src_path = candidate

        # fallback: look for raw files matching inst_id
        if not src_path:
            for ext in EXTS_RASTER:
                candidate = LOGO_DIR / f"{inst_id}{ext}"
                if candidate.exists():
                    src_path = candidate
                    break

        if not src_path:
            continue

        # create mark filename
        mark_name = f"{inst_id}_mark.png"
        dest = LOGO_DIR / mark_name

        try:
            with Image.open(src_path) as im:
                im = im.convert('RGBA')
                sq = crop_center_square(im)
                sq = sq.resize((256, 256), Image.LANCZOS)
                sq.save(dest, format='PNG')

            media['logo_path'] = f"/img/institutions/{mark_name}"
            post['media'] = media
            md_path.write_text(frontmatter.dumps(post), encoding='utf-8')

            # update evidence
            evidence_path = md_path.with_suffix('.evidence.md')
            if evidence_path.exists():
                text = evidence_path.read_text(encoding='utf-8')
            else:
                text = '---\n---\n\n# Evidence Map\n\n'
            if '## Sources' not in text:
                text = text.rstrip() + '\n\n## Sources\n'
            note = f"Cropped square mark created: {mark_name}"
            if note not in text:
                text = text.rstrip() + f"\n- {note}\n"
                evidence_path.write_text(text, encoding='utf-8')

            updated += 1
            print('created', dest.name, 'for', inst_id)
        except Exception as e:
            print('failed', inst_id, e)

    print('total cropped', updated)


if __name__ == '__main__':
    main()
