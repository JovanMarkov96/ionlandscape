#!/usr/bin/env python3
"""Retry fetching the logos that failed, with retries + fallback sources."""
import os, io, time, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO_DIR = os.path.join(ROOT, "website", "static", "img", "institutions")

TARGETS = {
    "i016-mit-lincoln-laboratory_mark.png": "ll.mit.edu",
    "i032-stockholm-university_mark.png": "su.se",
    "i035-tsinghua-university_mark.png": "tsinghua.edu.cn",
    "i040-university-of-buenos-aires_mark.png": "uba.ar",
    "i057-open-quantum-design_mark.png": "openquantumdesign.org",
    "i031-stellenbosch-university_mark.png": "sun.ac.za",
    "i047-university-of-kassel_mark.png": "uni-kassel.de",
    "i042-university-of-california-berkeley_mark.png": "berkeley.edu",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (logo-fetch)"}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def to_png_256(data):
    img = Image.open(io.BytesIO(data))
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
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    w, h = img.size
    scale = min(256 / w, 256 / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas.paste(img, ((256 - nw) // 2, (256 - nh) // 2), img)
    return canvas


def sources(domain):
    return [
        f"https://icon.horse/icon/{domain}",
        f"https://www.google.com/s2/favicons?domain={domain}&sz=256",
        f"https://favicon.yandex.net/favicon/v2/https://{domain}?size=120",
    ]


def main():
    ok, fail = [], []
    for fname, domain in TARGETS.items():
        got = False
        for url in sources(domain):
            for attempt in range(3):
                try:
                    data = fetch(url)
                    if len(data) < 200:
                        raise ValueError(f"too small ({len(data)}b)")
                    png = to_png_256(data)
                    png.save(os.path.join(LOGO_DIR, fname), "PNG")
                    print(f"OK   {domain:24} -> {fname} via {url.split('/')[2]} ({len(data)}b)")
                    got = True
                    break
                except Exception as e:
                    last = str(e)
                    time.sleep(1.2)
            if got:
                break
        if got:
            ok.append(fname)
        else:
            fail.append((fname, domain, last))
            print(f"FAIL {domain:24} -> {fname}: {last}")
        time.sleep(0.3)
    print(f"\nDone. {len(ok)} ok, {len(fail)} failed.")
    if fail:
        print("Still failed:", [d for _, d, _ in fail])


if __name__ == "__main__":
    main()
