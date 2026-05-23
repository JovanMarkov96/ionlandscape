import os
import glob
import frontmatter
import re
import unicodedata
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_DIR = os.path.join(ROOT, "content")
PEOPLE_DIR = os.path.join(CONTENT_DIR, "people")
COMPANIES_DIR = os.path.join(CONTENT_DIR, "companies")
INSTITUTIONS_DIR = os.path.join(CONTENT_DIR, "institutions")

def slugify(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name = name.strip().lower().replace(" ", "-")
    return re.sub(r'[^a-z0-9\-]', '', name)

# Collect valid IDs and names to avoid duplicates
valid_ids = set()
valid_names = set()

def load_ids(directory):
    for md_path in glob.glob(os.path.join(directory, "*.md")):
        if md_path.endswith(".evidence.md"): continue
        try:
            post = frontmatter.load(md_path)
            meta = post.metadata
            item_id = meta.get("id")
            if not item_id:
                item_id = slugify(meta.get("name", os.path.basename(md_path).replace(".md", "")))
            valid_ids.add(item_id)
            if "name" in meta:
                valid_names.add(slugify(meta["name"]))
        except Exception:
            pass

load_ids(PEOPLE_DIR)
load_ids(COMPANIES_DIR)
load_ids(INSTITUTIONS_DIR)

# Find dangling people references
dangling_people = set()

# From people (advisors, postdoc_advisors)
for md_path in glob.glob(os.path.join(PEOPLE_DIR, "*.md")):
    if md_path.endswith(".evidence.md"): continue
    try:
        meta = frontmatter.load(md_path).metadata
        for edu in meta.get("education", []):
            adv = edu.get("advisor")
            if adv:
                adv_id = slugify(adv)
                if adv_id not in valid_ids and adv_id not in valid_names:
                    dangling_people.add(adv)
        for pd in meta.get("postdocs", []):
            adv = pd.get("advisor")
            if adv:
                adv_id = slugify(adv)
                if adv_id not in valid_ids and adv_id not in valid_names:
                    dangling_people.add(adv)
    except:
        pass

# From companies (founders, leadership)
for md_path in glob.glob(os.path.join(COMPANIES_DIR, "*.md")):
    if md_path.endswith(".evidence.md"): continue
    try:
        meta = frontmatter.load(md_path).metadata
        for founder in meta.get("people", {}).get("founders", []):
            f_name = founder.get("name")
            if f_name:
                f_id = founder.get("person_id") or slugify(f_name)
                if f_id not in valid_ids and slugify(f_name) not in valid_names:
                    dangling_people.add(f_name)
        for leader in meta.get("people", {}).get("leadership", []):
            l_name = leader.get("name")
            if l_name:
                l_id = leader.get("person_id") or slugify(l_name)
                if l_id not in valid_ids and slugify(l_name) not in valid_names:
                    dangling_people.add(l_name)
    except:
        pass

# From institutions (leadership)
for md_path in glob.glob(os.path.join(INSTITUTIONS_DIR, "*.md")):
    if md_path.endswith(".evidence.md"): continue
    try:
        meta = frontmatter.load(md_path).metadata
        for leader in meta.get("leadership", []):
            l_name = leader.get("name")
            if l_name:
                l_id = leader.get("person_id") or slugify(l_name)
                if l_id not in valid_ids and slugify(l_name) not in valid_names:
                    dangling_people.add(l_name)
    except:
        pass

# Create stubs
stub_count = 0
for name in dangling_people:
    slug = slugify(name)
    # Assign a fake ID like 999-slug to indicate it's a stub, or 000-slug
    pid = f"000-{slug}"
    
    if pid in valid_ids:
        continue
        
    post = frontmatter.Post("")
    post.metadata = {
        "schema_version": 2,
        "id": pid,
        "entity_type": "person",
        "name": name,
        "location": {
            "city": "Unknown",
            "country": "Unknown"
        },
        "group_type": "mixed",
        "platforms": [],
        "applications": ["computing"], # Required for mixed
        "active": "unknown",
        "stub": True,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    out_path = os.path.join(PEOPLE_DIR, f"{pid}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
    
    valid_ids.add(pid)
    valid_names.add(slug)
    stub_count += 1

print(f"Generated {stub_count} person stubs.")
