#!/usr/bin/env python3
"""
build_index.py

Parses Markdown person files in content/people/*.md and generates:
- website/static/data/people.json
- website/static/data/people.geojson
- website/static/data/edges.csv

Run: python scripts/build_index.py
"""
import os
import glob
import json
import csv
import frontmatter
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content", "people")
OUT_DIR = os.path.join(ROOT, "website", "static", "data")
os.makedirs(OUT_DIR, exist_ok=True)

def slugify(name):
    return name.strip().lower().replace(" ", "-").replace(",", "").replace(".", "")

people = []
features = []
edges = []  # tuples: (source_id, target_id, type)

for md_path in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
    post = frontmatter.load(md_path)
    meta = post.metadata
    pid = meta.get("id") or slugify(meta.get("name", os.path.basename(md_path)))
    name = meta.get("name", "")
    location = meta.get("location", {})
    lat = location.get("lat")
    lon = location.get("lon")
    if lat is None or lon is None:
        # If location missing, leave lat/lon as None and mark for later manual geocoding
        lat, lon = None, None

    # Short bio: first paragraph from content
    content = post.content.strip()
    short_bio = ""
    if content:
        short_bio = content.split("\n\n")[0].strip()

    person_obj = {
        "id": pid,
        "name": name,
        "sort_name": meta.get("sort_name", ""),
        "current_position": meta.get("current_position", {}),
        "platforms": meta.get("platforms", []),
        "affiliations": meta.get("affiliations", []),
        "location": {
            "city": location.get("city", ""),
            "region": location.get("region", ""),
            "country": location.get("country", ""),
            "lat": lat,
            "lon": lon,
        },
        "education": meta.get("education", []),
        "postdocs": meta.get("postdocs", []),
        "keywords": meta.get("keywords", []),
        "links": meta.get("links", {}),
        "thesis": meta.get("thesis", {}),
        "short_bio": short_bio,
        "md_filename": os.path.basename(md_path),
        "created_at": meta.get("created_at", ""),
        "updated_at": meta.get("updated_at", ""),
    }
    people.append(person_obj)

    # GeoJSON feature (only if lat/lon provided)
    properties = {
        "id": pid,
        "name": name,
        "platforms": person_obj["platforms"],
        "short_bio": short_bio,
        "md_filename": person_obj["md_filename"]
    }
    feature = {
        "type": "Feature",
        "properties": properties,
        "geometry": None
    }
    if lat is not None and lon is not None:
        feature["geometry"] = {
            "type": "Point",
            "coordinates": [lon, lat]
        }
    features.append(feature)

    # Edges: education advisors
    for edu in meta.get("education", []):
        adv = edu.get("advisor")
        if adv:
            target_id = slugify(adv)
            edges.append((target_id, pid, "advisor"))

    # Postdoc advisors
    for pd in meta.get("postdocs", []):
        adv = pd.get("advisor")
        if adv:
            target_id = slugify(adv)
            edges.append((target_id, pid, "postdoc_advisor"))

    # Affiliations: person -> institution/company
    for aff in meta.get("affiliations", []):
        inst = aff.get("name")
        if inst:
            edges.append((pid, slugify(inst), "affiliated_with"))

# Write people.json
people_json_path = os.path.join(OUT_DIR, "people.json")
with open(people_json_path, "w", encoding="utf-8") as f:
    json.dump(people, f, ensure_ascii=False, indent=2)

# Write people.geojson
geojson_obj = {
    "type": "FeatureCollection",
    "features": features
}
geojson_path = os.path.join(OUT_DIR, "people.geojson")
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_obj, f, ensure_ascii=False, indent=2)

# Write edges.csv
edges_path = os.path.join(OUT_DIR, "edges.csv")
with open(edges_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target", "type"])
    for src, tgt, etype in edges:
        writer.writerow([src, tgt, etype])

print("Wrote:", people_json_path)
print("Wrote:", geojson_path)
print("Wrote:", edges_path)
