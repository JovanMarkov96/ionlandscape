#!/usr/bin/env python3
"""Fetch institution logos that are invisible on a white background.

Strategy: download each institution's icon from icon.horse (favicon aggregator),
convert/normalize to a 256x256 PNG. Favicons carry their own brand colors so they
are guaranteed visible. Files saved over the existing *_mark.png.
"""
import os
import io
import sys
import time
import urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO_DIR = os.path.join(ROOT, "website", "static", "img", "institutions")

# institution mark filename (without dir) -> domain
TARGETS = {
    "i004-duke-university_mark.png": "duke.edu",
    "i007-georgia-institute-of-technology_mark.png": "gatech.edu",
    "i016-mit-lincoln-laboratory_mark.png": "ll.mit.edu",
    "i018-national-institute-of-information-and-communications-technology-nict_mark.png": "nict.go.jp",
    "i019-national-institute-of-standards-and-technology-nist-boulder_mark.png": "nist.gov",
    "i024-palacky-university-olomouc_mark.png": "upol.cz",
    "i028-sandia-national-laboratories_mark.png": "sandia.gov",
    "i032-stockholm-university_mark.png": "su.se",
    "i035-tsinghua-university_mark.png": "tsinghua.edu.cn",
    "i040-university-of-buenos-aires_mark.png": "uba.ar",
    "i043-university-of-california-los-angeles_mark.png": "ucla.edu",
    "i044-university-of-granada_mark.png": "ugr.es",
    "i048-university-of-oregon_mark.png": "uoregon.edu",
    "i057-open-quantum-design_mark.png": "openquantumdesign.org",
    "i031-stellenbosch-university_mark.png": "sun.ac.za",
    "i037-university-of-amsterdam_mark.png": "uva.nl",
    "i046-university-of-innsbruck_mark.png": "uibk.ac.at",
    "i005-eth-zurich_mark.png": "ethz.ch",
    "i047-university-of-kassel_mark.png": "uni-kassel.de",
    "i015-kyoto-university_mark.png": "kyoto-u.ac.jp",
    "i045-university-of-groningen_mark.png": "rug.nl",
    "i042-university-of-california-berkeley_mark.png": "berkeley.edu",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (logo-fetch)"}


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def to_png_256(data):
    """Load any image (png/ico/jpg), pick largest frame, normalize to 256x256 RGBA on transparent."""
    img = Image.open(io.BytesIO(data))
    # For ICO, choose the largest available size
    if getattr(img, "n_frames", 1) > 1 or img.format == "ICO":
        best = None
        try:
            for i in range(getattr(img, "n_frames", 1)):
                img.seek(i)
                if best is None or (img.size[0] * img.size[1]) > (best.size[0] * best.size[1]):
                    best = img.convert("RGBA")
        except Exception:
            best = img.convert("RGBA")
        img = best
    else:
        img = img.convert("RGBA")

    # Scale up/down to fit 256 while keeping aspect, center on transparent 256 canvas
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    w, h = img.size
    scale = min(256 / w, 256 / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas.paste(img, ((256 - nw) // 2, (256 - nh) // 2), img)
    return canvas


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    ok, fail = [], []
    for fname, domain in TARGETS.items():
        if only and only not in fname:
            continue
        url = f"https://icon.horse/icon/{domain}"
        try:
            data = fetch(url)
            if len(data) < 200:
                raise ValueError(f"too small ({len(data)}b)")
            png = to_png_256(data)
            out = os.path.join(LOGO_DIR, fname)
            png.save(out, "PNG")
            ok.append((fname, domain, len(data)))
            print(f"OK   {domain:28} -> {fname} ({len(data)}b)")
        except Exception as e:
            fail.append((fname, domain, str(e)))
            print(f"FAIL {domain:28} -> {fname}: {e}")
        time.sleep(0.4)
    print(f"\nDone. {len(ok)} ok, {len(fail)} failed.")
    if fail:
        print("Failed domains:", [d for _, d, _ in fail])


if __name__ == "__main__":
    main()
