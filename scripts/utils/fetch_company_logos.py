"""Fetch favicon/logo images for companies missing a logo and normalize them to
128x128 transparent-padded PNGs in website/static/logos/<id>.png."""
import io
import os
import sys
import requests
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "website", "static", "logos")
os.makedirs(OUT, exist_ok=True)

COMPANIES = {
    "c019-pasqal": "pasqal.com",
    "c020-iqm": "meetiqm.com",
    "c021-google-quantum-ai": "quantumai.google",
    "c022-ibm-quantum": "ibm.com",
    "c023-oxford-quantum-circuits": "oqc.tech",
    "c024-rigetti-computing": "rigetti.com",
    "c025-quantum-brilliance": "quantumbrilliance.com",
    "c026-nvision-imaging": "nvision-quantum.com",
    "c027-element-six": "e6.com",
    "c028-atom-computing": "atom-computing.com",
    "c029-infleqtion": "infleqtion.com",
    "c030-psiquantum": "psiquantum.com",
    "c031-xanadu": "xanadu.ai",
    "c032-orca-computing": "orcacomputing.com",
    "c033-quix-quantum": "quixquantum.com",
    "c034-quandela": "quandela.com",
}

UA = {"User-Agent": "Mozilla/5.0 (logo-fetch; ozerilab@weizmann.ac.il)"}


def fetch(url):
    try:
        r = requests.get(url, headers=UA, timeout=15)
        if r.status_code == 200 and len(r.content) > 400:
            return r.content
    except Exception:
        pass
    return None


def load_image(data):
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        return im.convert("RGBA")
    except Exception:
        return None


def normalize(im, size=128):
    # square-pad on transparent, then resize
    w, h = im.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
    return canvas.resize((size, size), Image.LANCZOS)


results = {"ok": [], "fail": []}
for cid, domain in COMPANIES.items():
    sources = [
        f"https://www.google.com/s2/favicons?domain={domain}&sz=256",
        f"https://www.google.com/s2/favicons?domain={domain}&sz=128",
        f"https://icons.duckduckgo.com/ip3/{domain}.ico",
        f"https://icon.horse/icon/{domain}",
    ]
    im = None
    used = None
    for url in sources:
        data = fetch(url)
        if not data:
            continue
        cand = load_image(data)
        if cand is None:
            continue
        # reject tiny low-res icons (<32px) unless it's the last resort
        if max(cand.size) < 32 and url != sources[-1]:
            im = im or cand
            used = used or url
            continue
        im, used = cand, url
        break
    if im is None:
        results["fail"].append((cid, domain))
        print(f"  FAIL {cid} ({domain})")
        continue
    out = os.path.join(OUT, f"{cid}.png")
    normalize(im).save(out, optimize=True)
    results["ok"].append((cid, im.size, used.split("/")[2]))
    print(f"  ok   {cid:30s} src={used.split('/')[2]:24s} orig={im.size}")

print(f"\nDone. {len(results['ok'])} ok, {len(results['fail'])} failed.")
if results["fail"]:
    print("Failed:", ", ".join(c for c, _ in results["fail"]))
