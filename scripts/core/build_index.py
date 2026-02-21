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

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_DIR = os.path.join(ROOT, "content", "people")
COMPANIES_DIR = os.path.join(ROOT, "content", "companies")
INSTITUTIONS_DIR = os.path.join(ROOT, "content", "institutions")
OUT_DIR = os.path.join(ROOT, "website", "static", "data")
os.makedirs(OUT_DIR, exist_ok=True)

def slugify(name):
    return name.strip().lower().replace(" ", "-").replace(",", "").replace(".", "")

people = []
companies = []
institutions = []
features = []
company_features = []
institution_features = []
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
        "group_type": meta.get("group_type", "experimental"),
        "labels": meta.get("labels", []),
        "ion_species": meta.get("ion_species", []),
        "links": meta.get("links", {}),
        "thesis": meta.get("thesis", {}),
        "short_bio": short_bio,
        "md_filename": os.path.basename(md_path),
        "created_at": meta.get("created_at", ""),
        "updated_at": meta.get("updated_at", ""),
    }
    people.append(person_obj)

    # GeoJSON feature (only if lat/lon provided)
    # Extract institution names from affiliations
    affiliations_list = []
    for aff in meta.get("affiliations", []):
        inst = aff.get("name")
        if inst:
            affiliations_list.append(inst)

    properties = {
        "id": pid,
        "name": name,
        "current_position": person_obj.get("current_position", ""),
        "platforms": person_obj["platforms"],
        "affiliations": affiliations_list,
        "city": location.get("city", ""),
        "country": location.get("country", ""),
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

# Process Companies
for md_path in glob.glob(os.path.join(COMPANIES_DIR, "*.md")):
    try:
        post = frontmatter.load(md_path)
        meta = post.metadata
        cid = meta.get("id") or slugify(meta.get("name", os.path.basename(md_path)))
        name = meta.get("name", "")
        location = meta.get("location", {})
        lat = location.get("lat")
        lon = location.get("lon")
        
        # Parse content
        content = post.content.strip()
        short_summary = meta.get("short_summary", "")
        if not short_summary and content:
             short_summary = content.split("\n\n")[0].strip()

        company_obj = {
            "id": cid,
            "name": name,
            "sort_name": meta.get("sort_name", name),
            "entity_type": "company",
            "platforms": meta.get("platforms", []),
            "location": location,
            "short_summary": short_summary,
            "approach": meta.get("approach", {}),
            "focus_areas": meta.get("focus_areas", []),
            "products": meta.get("products", []),
            "people": meta.get("people", {}),
            "status": meta.get("status", {}),
            "funding": meta.get("funding", {}),
            "milestones": meta.get("milestones", []),
            "links": meta.get("links", {}),
            "media": meta.get("media", {}),
            "sources": meta.get("sources", []),
            "md_filename": os.path.basename(md_path),
            "updated_at": meta.get("updated_at", "")
        }
        companies.append(company_obj)

        # GeoJSON Feature
        properties = {
            "id": cid,
            "name": name,
            "entity_type": "company",
            "platforms": company_obj["platforms"],
            "city": location.get("city", ""),
            "country": location.get("country", ""),
            "short_summary": short_summary,
            "logo_path": meta.get("media", {}).get("logo_path", ""),
            "md_filename": company_obj["md_filename"]
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
        company_features.append(feature)

    except Exception as e:
        print(f"Error processing company {md_path}: {e}")

# Process Institutions
for md_path in glob.glob(os.path.join(INSTITUTIONS_DIR, "*.md")):
    try:
        post = frontmatter.load(md_path)
        meta = post.metadata
        iid = meta.get("id") or slugify(meta.get("name", os.path.basename(md_path)))
        name = meta.get("name", "")
        location = meta.get("location", {})
        lat = location.get("lat")
        lon = location.get("lon")

        # Auto-generate directories
        current_members = []
        alumni = []
        
        # Build set of matching names for the institution (its name + aliases)
        match_names = {name.lower().strip()}
        for alias in meta.get("aliases", []):
            match_names.add(alias.lower().strip())
        
        for person in people:
            pid = person["md_filename"]
            is_current = False
            
            # Check current position
            cp = person.get("current_position", {})
            if isinstance(cp, dict):
                p_inst = cp.get("institution", "").lower().strip()
                if p_inst in match_names:
                    is_current = True
            
            if is_current:
                current_members.append(pid)
            else:
                # Check education & postdocs for alumni
                is_alumni = False
                for edu in person.get("education", []):
                    edu_inst = edu.get("institution", "")
                    if edu_inst and edu_inst.lower().strip() in match_names:
                        is_alumni = True
                        break
                if not is_alumni:
                    for pd in person.get("postdocs", []):
                        pd_inst = pd.get("institution", "")
                        if pd_inst and pd_inst.lower().strip() in match_names:
                            is_alumni = True
                            break
                if is_alumni:
                    alumni.append(pid)

        inst_obj = {
            "id": iid,
            "name": name,
            "sort_name": meta.get("sort_name", name),
            "entity_type": "institution",
            "aliases": meta.get("aliases", []),
            "abbreviations": meta.get("abbreviations", []),
            "location": location,
            "institution_type": meta.get("institution_type", "unknown"),
            "short_description": meta.get("short_description", ""),
            "focus_areas": meta.get("focus_areas", []),
            "links": meta.get("links", {}),
            "media": meta.get("media", {}),
            "directory": {
                "current_members": current_members,
                "alumni": alumni,
                "member_count": len(current_members),
                "alumni_count": len(alumni)
            },
            "sources": meta.get("sources", []),
            "md_filename": os.path.basename(md_path),
            "updated_at": meta.get("updated_at", "")
        }
        institutions.append(inst_obj)

        # GeoJSON Feature
        properties = {
            "id": iid,
            "name": name,
            "entity_type": "institution",
            "city": location.get("city", ""),
            "country": location.get("country", ""),
            "short_description": inst_obj["short_description"],
            "logo_path": meta.get("media", {}).get("logo_path", ""),
            "md_filename": inst_obj["md_filename"]
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
        institution_features.append(feature)

    except Exception as e:
        print(f"Error processing institution {md_path}: {e}")

# Write people.json (existing)
people_json_path = os.path.join(OUT_DIR, "people.json")
with open(people_json_path, "w", encoding="utf-8") as f:
    json.dump(people, f, ensure_ascii=False, indent=2)

# Write companies.json (new)
companies_json_path = os.path.join(OUT_DIR, "companies.json")
with open(companies_json_path, "w", encoding="utf-8") as f:
    json.dump(companies, f, ensure_ascii=False, indent=2)

# Write institutions.json (new)
institutions_json_path = os.path.join(OUT_DIR, "institutions.json")
with open(institutions_json_path, "w", encoding="utf-8") as f:
    json.dump(institutions, f, ensure_ascii=False, indent=2)

# Write people.geojson (existing)
geojson_obj = {
    "type": "FeatureCollection",
    "features": features
}
geojson_path = os.path.join(OUT_DIR, "people.geojson")
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_obj, f, ensure_ascii=False, indent=2)

# Write companies.geojson (new)
comp_geojson_obj = {
    "type": "FeatureCollection",
    "features": company_features
}
comp_geojson_path = os.path.join(OUT_DIR, "companies.geojson")
with open(comp_geojson_path, "w", encoding="utf-8") as f:
    json.dump(comp_geojson_obj, f, ensure_ascii=False, indent=2)

# Write institutions.geojson (new)
inst_geojson_obj = {
    "type": "FeatureCollection",
    "features": institution_features
}
inst_geojson_path = os.path.join(OUT_DIR, "institutions.geojson")
with open(inst_geojson_path, "w", encoding="utf-8") as f:
    json.dump(inst_geojson_obj, f, ensure_ascii=False, indent=2)

# Write edges.csv
edges_path = os.path.join(OUT_DIR, "edges.csv")
with open(edges_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target", "type"])
    for src, tgt, etype in edges:
        writer.writerow([src, tgt, etype])

print("Wrote:", people_json_path)
print("Wrote:", companies_json_path)
print("Wrote:", institutions_json_path)
print("Wrote:", geojson_path)
print("Wrote:", comp_geojson_path)
print("Wrote:", inst_geojson_path)
print("Wrote:", edges_path)
