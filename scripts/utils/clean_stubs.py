#!/usr/bin/env python3
"""Phase 1 — stub people hygiene:
  1. Fix mojibake names (e.g. "Jos? Ignacio Latorre" -> "José Ignacio Latorre").
  2. Strip "Dr./Prof." honorific prefixes.
  3. Split compound stubs ("A; B") into one stub file per person.
  4. Remove stubs that duplicate a real (non-stub) profile by first+last name.
Idempotent. Prints a summary.
"""
import os, glob, re, unicodedata
import frontmatter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PEOPLE = os.path.join(ROOT, "content", "people")

def slugify(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name = name.strip().lower().replace(" ", "-")
    return re.sub(r'[^a-z0-9\-]', '', name)

def first_last_key(name):
    n = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII').lower()
    n = re.sub(r'\b(dr|prof|phd|jr|sr)\b\.?', '', n)
    n = re.sub(r'[^a-z ]', ' ', n)
    toks = [t for t in n.split() if len(t) > 1]
    if len(toks) >= 2:
        return toks[0] + ' ' + toks[-1]
    return ' '.join(toks)

# Known good spellings for mojibake fixes
MOJIBAKE = {
    "Jos? Ignacio Latorre": "José Ignacio Latorre",
}

def load_all():
    out = []
    for fp in glob.glob(os.path.join(PEOPLE, "*.md")):
        if fp.endswith(".evidence.md"):
            continue
        post = frontmatter.load(fp)
        out.append((fp, post))
    return out

def main():
    files = load_all()
    real_keys = set()
    for fp, post in files:
        if not post.metadata.get("stub"):
            nm = post.metadata.get("name", "")
            if nm:
                real_keys.add(first_last_key(nm))

    fixed_enc = stripped = split = removed = 0

    for fp, post in files:
        meta = post.metadata
        name = meta.get("name", "")
        is_stub = bool(meta.get("stub"))

        # 1. mojibake
        if name in MOJIBAKE:
            meta["name"] = MOJIBAKE[name]
            name = meta["name"]
            with open(fp, "wb") as f:
                frontmatter.dump(post, f)
            fixed_enc += 1

        if not is_stub:
            continue

        # 3. compound split
        if ";" in name:
            parts = [p.strip() for p in name.split(";") if p.strip()]
            for part in parts:
                # skip if this person already covered by a real profile
                if first_last_key(part) in real_keys:
                    continue
                new_slug = "000-" + slugify(part)
                new_fp = os.path.join(PEOPLE, new_slug + ".md")
                if os.path.exists(new_fp):
                    continue
                np = frontmatter.Post("", **{
                    "id": new_slug, "name": part, "entity_type": "person",
                    "stub": True, "platforms": [], "applications": ["computing"],
                    "group_type": "mixed", "active": "unknown",
                    "location": {"city": "Unknown", "country": "Unknown"},
                    "schema_version": 2,
                    "created_at": meta.get("created_at", ""), "updated_at": meta.get("updated_at", ""),
                })
                with open(new_fp, "wb") as f:
                    frontmatter.dump(np, f)
            os.remove(fp)
            split += 1
            continue

        # 2. strip honorific
        new_name = re.sub(r'^(Dr|Prof|PhD)\.?\s+', '', name).strip()
        if new_name != name:
            meta["name"] = new_name
            name = new_name
            with open(fp, "wb") as f:
                frontmatter.dump(post, f)
            stripped += 1

        # 4. dedup vs real profile
        if first_last_key(name) in real_keys:
            os.remove(fp)
            removed += 1

    print(f"Mojibake fixed: {fixed_enc}")
    print(f"Honorifics stripped: {stripped}")
    print(f"Compound stubs split: {split}")
    print(f"Duplicate stubs removed: {removed}")

if __name__ == "__main__":
    main()
