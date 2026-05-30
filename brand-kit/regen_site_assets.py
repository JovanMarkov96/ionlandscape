"""Regenerate website/static/img/brand assets from the EXACT selected-logo variants.

The clean SVG mark in the kit is a thick-stroke vector *approximation*; the
`exact-*` PNG variants are the real selected logo. This script produces the
crisp, tightly-cropped site assets (mark, horizontal wordmarks, and a composed
stacked wordmark) used by the navbar and welcome splash.
"""
import os
from PIL import Image

KIT = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(KIT, "png")
OUT = os.path.normpath(os.path.join(KIT, "..", "website", "static", "img", "brand"))
os.makedirs(OUT, exist_ok=True)


def trim(im, pad_frac=0.0):
    im = im.convert("RGBA")
    bbox = im.split()[-1].getbbox()
    im = im.crop(bbox)
    if pad_frac:
        pad = max(2, int(im.size[1] * pad_frac))
        canvas = Image.new("RGBA", (im.size[0] + 2 * pad, im.size[1] + 2 * pad), (0, 0, 0, 0))
        canvas.paste(im, (pad, pad), im)
        im = canvas
    return im


def col_alpha(im):
    a = im.split()[-1]
    w, h = im.size
    px = a.load()
    sums = [0] * w
    for x in range(w):
        s = 0
        for y in range(h):
            s += px[x, y]
        sums[x] = s
    return sums


def extract_text(wordmark_path):
    """Crop just the 'Quantum Landscape' text from a horizontal wordmark
    (drops the leading mark by finding the first wide transparent gap)."""
    im = Image.open(wordmark_path).convert("RGBA")
    bbox = im.split()[-1].getbbox()
    im = im.crop(bbox)
    w, h = im.size
    sums = col_alpha(im)
    thresh = max(sums) * 0.012
    content = [s > thresh for s in sums]
    # first content run = mark; find the gap after it, text starts after the gap
    i = 0
    while i < w and not content[i]:
        i += 1
    while i < w and content[i]:
        i += 1  # end of mark
    gap_min = int(w * 0.03)
    gap_start = i
    while i < w and not content[i]:
        i += 1
    # require a real gap; if the run was too short keep scanning
    while i < w and (i - gap_start) < gap_min:
        while i < w and content[i]:
            i += 1
        gap_start = i
        while i < w and not content[i]:
            i += 1
    text_start = i
    text = im.crop((text_start, 0, w, h))
    return trim(text)


def compose_stacked(mark_path, wordmark_path, out_path):
    mark = trim(Image.open(mark_path))
    text = extract_text(wordmark_path)
    # scale text so its width is ~1.9x the mark width (typical stacked look)
    target_text_w = int(mark.size[0] * 1.9)
    scale = target_text_w / text.size[0]
    text = text.resize((target_text_w, max(1, int(text.size[1] * scale))), Image.LANCZOS)
    gap = int(mark.size[1] * 0.16)
    pad = int(max(mark.size[0], text.size[0]) * 0.04)
    W = max(mark.size[0], text.size[0]) + 2 * pad
    H = mark.size[1] + gap + text.size[1] + 2 * pad
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.paste(mark, ((W - mark.size[0]) // 2, pad), mark)
    canvas.paste(text, ((W - text.size[0]) // 2, pad + mark.size[1] + gap), text)
    canvas.save(out_path, optimize=True)
    print("stacked ->", os.path.basename(out_path), canvas.size)


# 1. Mark (exact)
trim(Image.open(os.path.join(PNG, "exact-selected-mark-transparent-512.png"))).save(
    os.path.join(OUT, "mark.png"), optimize=True)
print("mark.png done")

# 2. Horizontal wordmarks (exact, tight crop + small pad)
for variant in ("dark", "light"):
    src = os.path.join(PNG, f"exact-wordmark-horizontal-on-{variant}-transparent-2560.png")
    trim(Image.open(src), pad_frac=0.04).save(
        os.path.join(OUT, f"wordmark-horizontal-on-{variant}.png"), optimize=True)
    print(f"wordmark-horizontal-on-{variant}.png done")

# 3. Stacked wordmarks (composed from exact mark + exact wordmark text)
for variant in ("dark", "light"):
    compose_stacked(
        os.path.join(PNG, "exact-selected-mark-transparent-1024.png"),
        os.path.join(PNG, f"exact-wordmark-horizontal-on-{variant}-transparent-2560.png"),
        os.path.join(OUT, f"wordmark-stacked-on-{variant}.png"),
    )

print("\nAll exact site assets regenerated in", OUT)
