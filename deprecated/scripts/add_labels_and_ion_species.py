import argparse
import os
import re
from datetime import date
import yaml

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

def load_frontmatter(md_text: str):
    m = FRONTMATTER_RE.match(md_text)
    if not m:
        raise ValueError("File missing YAML frontmatter with --- blocks.")
    fm_text, body = m.group(1), m.group(2)
    fm = yaml.safe_load(fm_text) or {}
    return fm, body

def dump_frontmatter(fm: dict, body: str) -> str:
    # Keep YAML readable and stable.
    fm_text = yaml.safe_dump(
        fm, sort_keys=False, allow_unicode=True, width=120, default_flow_style=False
    ).strip()
    return f"---\n{fm_text}\n---\n\n{body.lstrip()}"

def normalize_label_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return [str(v) for v in x]
    return [str(x)]

def normalize_species_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return [str(v) for v in x]
    return [str(x)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles_dir", required=True, help="Directory containing person *.md files")
    ap.add_argument("--ion_map", required=True, help="YAML mapping: id -> [ion species]")
    ap.add_argument("--dry_run", action="store_true", help="Print changes but do not write files")
    ap.add_argument("--overwrite_ion_species", action="store_true",
                   help="Overwrite existing ion_species even if non-empty")
    args = ap.parse_args()

    with open(args.ion_map, "r", encoding="utf-8") as f:
        ion_map = yaml.safe_load(f) or {}

    changed = 0
    total = 0

    for root, _, files in os.walk(args.profiles_dir):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            total += 1

            with open(path, "r", encoding="utf-8") as f:
                txt = f.read()

            try:
                fm, body = load_frontmatter(txt)
            except ValueError:
                # Skip files without frontmatter
                continue

            orig = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)

            # 1) group_type
            if not fm.get("group_type"):
                fm["group_type"] = "experimental"

            # 2) labels
            labels = normalize_label_list(fm.get("labels"))
            if "Experimental group" not in labels:
                labels.append("Experimental group")
            # de-dup, preserve order
            seen = set()
            labels = [l for l in labels if not (l in seen or seen.add(l))]
            fm["labels"] = labels

            # 3) ion_species
            pid = fm.get("id")
            mapped = ion_map.get(pid)
            if mapped is not None:
                existing = normalize_species_list(fm.get("ion_species"))
                if args.overwrite_ion_species or not existing:
                    fm["ion_species"] = mapped
                else:
                    # merge without duplicates
                    merged = existing + [v for v in mapped if v not in existing]
                    fm["ion_species"] = merged
            else:
                # Ensure the key exists so UI can rely on it if missing
                if "ion_species" not in fm:
                    fm["ion_species"] = []

            # 4) updated_at stamp
            # Only update if something actually changed to avoid noise? 
            # The script logic compares `orig` vs `new` at the end on value semantic.
            # But changing `updated_at` makes `new` always different if we update it unconditionally.
            # User script says: "if 'updated_at' in fm: fm['updated_at'] = ..."
            # I will follow the user script logic exactly.
            if "updated_at" in fm:
                fm["updated_at"] = str(date.today())

            new = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)

            # Compare semantics to avoid updating file if nothing material changed (except updated_at potentially)
            # But updated_at triggers change.
            # Let's write.
            
            if new != orig:
                changed += 1
                if args.dry_run:
                    print(f"[DRY] Would update: {path}")
                else:
                    out = dump_frontmatter(fm, body)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(out)
                    print(f"Updated: {path}")

    print(f"\nDone. Scanned {total} .md files, updated {changed}.")

if __name__ == "__main__":
    main()
