#!/usr/bin/env python3
"""Analyze institution logos: detect which are invisible/near-invisible on a WHITE background."""
import os, glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO_DIR = os.path.join(ROOT, "website", "static", "img", "institutions")

def analyze(path):
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as e:
        return ("ERROR", str(e))
    img.thumbnail((128, 128))
    # Composite onto white
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    comp = Image.alpha_composite(white, img).convert("RGB")
    px = list(comp.getdata())
    n = len(px)
    # Count "ink" pixels — those clearly darker/more saturated than white
    ink = 0
    for r, g, b in px:
        # distance from white
        if (255 - r) + (255 - g) + (255 - b) > 90:  # at least ~30/channel darker
            ink += 1
    ink_ratio = ink / n
    return (round(ink_ratio * 100, 1), n)

results = []
for f in sorted(glob.glob(os.path.join(LOGO_DIR, "*_mark.png"))):
    name = os.path.basename(f)
    ink_pct, _ = analyze(f)
    results.append((name, ink_pct))

# Sort by ink percentage (lowest = most invisible)
results.sort(key=lambda x: x[1] if isinstance(x[1], (int, float)) else 999)
print("Logos sorted by visible-ink %% on white (low = invisible/needs replacement):")
for name, pct in results:
    flag = "  <-- INVISIBLE ON WHITE" if isinstance(pct, (int, float)) and pct < 3 else ""
    print(f"  {pct:>6}%  {name}{flag}")
