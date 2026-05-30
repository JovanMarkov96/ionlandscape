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
import re
import unicodedata
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_DIR = os.path.join(ROOT, "content", "people")
COMPANIES_DIR = os.path.join(ROOT, "content", "companies")
INSTITUTIONS_DIR = os.path.join(ROOT, "content", "institutions")
OUT_DIR = os.path.join(ROOT, "website", "static", "data")
os.makedirs(OUT_DIR, exist_ok=True)

def slugify(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name = name.strip().lower().replace(" ", "-")
    return re.sub(r'[^a-z0-9\-]', '', name)

_LOWER_WORDS = {'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'yet', 'so',
                'in', 'on', 'at', 'to', 'of', 'with', 'by', 'from', 'as', 'into',
                'via', 'per', 'vs'}

def smart_title(s):
    words = s.split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in _LOWER_WORDS:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return ' '.join(result)

people = []
companies = []
institutions = []
features = []
company_features = []
institution_features = []
edges = []  # tuples: (source_id, target_id, type)

for md_path in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
    if md_path.endswith(".evidence.md"):
        continue
    post = frontmatter.load(md_path)
    meta = post.metadata
    # Derive a sane filename base (basename without extension)
    base = os.path.splitext(os.path.basename(md_path))[0]
    pid = meta.get("id") or slugify(meta.get("name") or base)
    # Prefer explicit frontmatter name; otherwise derive from filename base
    name = meta.get("name") or smart_title(re.sub(r'^(i\d+-)?', '', base).replace('-', ' ').strip())
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
        "nobel_prize": meta.get("nobel_prize"),
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

    # Edges: education advisors (store RAW names; resolved to node IDs at the end).
    # Advisor strings may list several people ("A; B") — split into one edge each.
    for edu in meta.get("education", []):
        adv = edu.get("advisor")
        if adv:
            for a in re.split(r'\s*;\s*', adv):
                if a.strip():
                    edges.append((a.strip(), pid, "advisor"))

    # Postdoc advisors
    for pd in meta.get("postdocs", []):
        adv = pd.get("advisor")
        if adv:
            for a in re.split(r'\s*;\s*', adv):
                if a.strip():
                    edges.append((a.strip(), pid, "postdoc_advisor"))

    # Affiliations: person -> institution/company
    for aff in meta.get("affiliations", []):
        inst = aff.get("name")
        if inst:
            edges.append((pid, inst, "affiliated_with"))

# Process Companies
for md_path in glob.glob(os.path.join(COMPANIES_DIR, "*.md")):
    if md_path.endswith(".evidence.md"):
        continue
    try:
        post = frontmatter.load(md_path)
        meta = post.metadata
        base = os.path.splitext(os.path.basename(md_path))[0]
        cid = meta.get("id") or slugify(meta.get("name") or base)
        name = meta.get("name") or smart_title(re.sub(r'^(c\d+-)?', '', base).replace('-', ' ').strip())
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
            "categories": meta.get("categories", []),
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

        # Auto-generate directories
        current_members = []
        
        # Build set of matching names for the company (its name + aliases)
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
            
            # Check affiliations
            for aff in person.get("affiliations", []):
                aff_name = aff.get("name", "").lower().strip()
                if aff_name in match_names:
                    is_current = True
            
            if is_current:
                current_members.append(pid)

        company_obj["directory"] = {
            "current_members": current_members,
            "member_count": len(current_members)
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

        # Edges from company founders, leadership, and spinouts
        people_block = meta.get("people", {})
        for founder in people_block.get("founders", []):
            f_name = founder.get("name")
            if f_name:
                edges.append((founder.get("person_id") or f_name, cid, "founder"))
        for leader in people_block.get("leadership", []):
            l_name = leader.get("name")
            if l_name:
                edges.append((leader.get("person_id") or l_name, cid, "leadership"))
        for spin in people_block.get("spun_out_of", []):
            if isinstance(spin, str):
                edges.append((cid, spin, "spun_out_from"))
            elif isinstance(spin, dict) and spin.get("name"):
                edges.append((cid, spin.get("institution_id") or spin.get("name"), "spun_out_from"))

        company_features.append(feature)

    except Exception as e:
        print(f"Error processing company {md_path}: {e}")

# Process Institutions
for md_path in glob.glob(os.path.join(INSTITUTIONS_DIR, "*.md")):
    if md_path.endswith(".evidence.md"):
        continue
    try:
        post = frontmatter.load(md_path)
        meta = post.metadata
        base = os.path.splitext(os.path.basename(md_path))[0]
        iid = meta.get("id") or slugify(meta.get("name") or base)
        name = meta.get("name") or smart_title(re.sub(r'^(i\d+-)?', '', base).replace('-', ' ').strip())
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

        company_spinouts = []
        for company in companies:
            c_spinouts = company.get("people", {}).get("spun_out_of", [])
            for spin in c_spinouts:
                if isinstance(spin, str):
                    if spin.lower().strip() in match_names:
                        company_spinouts.append(company["id"])
                elif isinstance(spin, dict):
                    if spin.get("institution_id") == iid or spin.get("name", "").lower().strip() in match_names:
                        company_spinouts.append(company["id"])

        # Edges from leadership
        for leader in meta.get("leadership", []):
            l_name = leader.get("name")
            if l_name:
                edges.append((leader.get("person_id") or l_name, iid, "leadership"))

        # Skip entries that are actually companies (e.g. IonQ)
        if meta.get("entity_type") == "company":
            continue

        # Diversify sources: include the institution's own website alongside Wikipedia
        inst_sources = list(meta.get("sources", []))
        website = (meta.get("links", {}) or {}).get("website")
        if website:
            existing_urls = {s.get("url", "").rstrip("/") for s in inst_sources}
            if website.rstrip("/") not in existing_urls:
                inst_sources.append({"note": "Official website", "url": website})

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
            "platforms_represented": meta.get("platforms_represented", []),
            "applications_represented": meta.get("applications_represented", []),
            "links": meta.get("links", {}),
            "media": meta.get("media", {}),
            "directory": {
                "current_members": current_members,
                "alumni": alumni,
                "company_spinouts": company_spinouts,
                "member_count": len(current_members),
                "alumni_count": len(alumni)
            },
            "sources": inst_sources,
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

# --- Location inheritance: people without coordinates inherit their current
# institution's point (precision = "inherited"). Fixes profiles with Unknown location. ---
def _norm_loc(s):
    return re.sub(r'\s+', ' ', re.sub(r'[().,\-–—/]', ' ', (s or '').lower())).strip()

_inst_loc_map = {}
def _add_inst_key(inst, *keys):
    for k in keys:
        nk = _norm_loc(k)
        if nk and nk not in _inst_loc_map:
            _inst_loc_map[nk] = inst

for _i in institutions:
    loc = _i.get("location") or {}
    if loc.get("lat") is not None and loc.get("lon") is not None:
        _add_inst_key(_i, _i.get("name"))
        for a in _i.get("aliases", []):
            _add_inst_key(_i, a)
        for a in _i.get("abbreviations", []):
            _add_inst_key(_i, a)

def _resolve_inst_loc(name):
    if not name:
        return None
    nk = _norm_loc(name)
    if nk in _inst_loc_map:
        return _inst_loc_map[nk]
    acronyms = [a.lower() for a in re.findall(r'\b[A-Z]{2,}\b', name or '')]
    for _i in institutions:
        loc = _i.get("location") or {}
        if loc.get("lat") is None or loc.get("lon") is None:
            continue
        ni = _norm_loc(_i.get("name"))
        if not ni:
            continue
        if (len(ni) > 6 and ni in nk) or (len(nk) > 6 and nk in ni):
            return _i
        if any(len(a) >= 3 and a in ni.split(' ') for a in acronyms):
            return _i
    return None

_feature_by_pid = {f["properties"]["id"]: f for f in features}
_inherited_count = 0
for person in people:
    loc = person.get("location") or {}
    if loc.get("lat") is None or loc.get("lon") is None:
        inst_name = (person.get("current_position") or {}).get("institution")
        inst = _resolve_inst_loc(inst_name)
        if inst:
            iloc = inst["location"]
            loc["lat"] = iloc.get("lat")
            loc["lon"] = iloc.get("lon")
            if not loc.get("city") or str(loc.get("city")).lower() == "unknown":
                loc["city"] = iloc.get("city", "")
            if not loc.get("country") or str(loc.get("country")).lower() == "unknown":
                loc["country"] = iloc.get("country", "")
            loc["precision"] = "inherited"
            person["location"] = loc
            feat = _feature_by_pid.get(person["id"])
            if feat is not None:
                feat["properties"]["city"] = loc.get("city", "")
                feat["properties"]["country"] = loc.get("country", "")
                feat["geometry"] = {"type": "Point", "coordinates": [iloc.get("lon"), iloc.get("lat")]}
            _inherited_count += 1

print(f"Location inheritance: {_inherited_count} people inherited institution coordinates")

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

# Validate and resolve edges
valid_ids = {p["id"] for p in people} | {c["id"] for c in companies} | {i["id"] for i in institutions}

def _norm(s):
    # Strip diacritics so "Vuletić" matches "Vuletic"; drop honorifics
    s = unicodedata.normalize('NFKD', s or '').encode('ASCII', 'ignore').decode('ASCII')
    s = re.sub(r'\b(dr|prof|professor|phd)\b\.?', ' ', s.lower())
    return re.sub(r'\s+', ' ', re.sub(r'[().,\-–—/]', ' ', s)).strip()

def _first_last(s):
    """First+last token of a normalized person name, ignoring middle initials."""
    toks = [t for t in _norm(s).split(' ') if len(t) > 1]
    if len(toks) >= 2:
        return toks[0] + ' ' + toks[-1]
    return ''

# Build a name/alias/abbreviation -> node id resolution map (first writer wins).
_resolve_map = {}
def _add_keys(node_id, *keys):
    for k in keys:
        nk = _norm(k)
        if nk and nk not in _resolve_map:
            _resolve_map[nk] = node_id

# Secondary people index keyed by first+last name (ignores middle initials),
# used only as a fallback so it never shadows exact matches.
_person_first_last = {}
for p in people:
    _add_keys(p["id"], p["id"], p.get("name"), p.get("sort_name"))
    for a in p.get("aliases", []):
        _add_keys(p["id"], a)
    fl = _first_last(p.get("name"))
    if fl and fl not in _person_first_last:
        _person_first_last[fl] = p["id"]
for c in companies:
    _add_keys(c["id"], c["id"], c.get("name"))
    for a in c.get("aliases", []):
        _add_keys(c["id"], a)
for i in institutions:
    _add_keys(i["id"], i["id"], i.get("name"))
    for a in i.get("aliases", []):
        _add_keys(i["id"], a)
    for a in i.get("abbreviations", []):
        _add_keys(i["id"], a)

def _resolve(raw):
    """Resolve a raw name/id to a node id; None if no confident match."""
    if raw in valid_ids:
        return raw
    nk = _norm(raw)
    if not nk:
        return None
    if nk in _resolve_map:
        return _resolve_map[nk]
    # People fallback: match on first+last name (handles "Christopher Monroe"
    # -> "Christopher R. Monroe", and honorific-prefixed founder names).
    fl = _first_last(raw)
    if fl and fl in _person_first_last:
        return _person_first_last[fl]
    # Org fallback: acronym / substring matching against institutions AND companies
    # (handles "National Institute of Standards and Technology (NIST), Boulder" -> "NIST Boulder"
    #  and "IonQ, Inc. (USA)" -> "IonQ")
    acronyms = [a.lower() for a in re.findall(r'\b[A-Z]{2,}\b', raw or '')]
    for entity in list(institutions) + list(companies):
        ni = _norm(entity.get("name"))
        if not ni:
            continue
        if len(ni) >= 4 and ni in nk:
            return entity["id"]
        if len(nk) > 6 and nk in ni:
            return entity["id"]
        toks = ni.split(' ')
        if any(len(a) >= 3 and a in toks for a in acronyms):
            return entity["id"]
    return None

valid_edges = []
_seen_edges = set()
unresolved_edges = []
for src, tgt, etype in edges:
    rs, rt = _resolve(src), _resolve(tgt)
    if rs and rt and rs != rt:
        key = (rs, rt, etype)
        if key not in _seen_edges:
            _seen_edges.add(key)
            valid_edges.append({"source": rs, "target": rt, "type": etype})
    else:
        unresolved_edges.append((src, tgt, etype, rs is not None, rt is not None))

print(f"Edges: {len(valid_edges)} resolved, {len(unresolved_edges)} unresolved")

# Write an unresolved-edges report for human follow-up
if unresolved_edges:
    report_dir = os.path.join(ROOT, "reports")
    os.makedirs(report_dir, exist_ok=True)
    with open(os.path.join(report_dir, "unresolved_edges.md"), "w", encoding="utf-8") as rf:
        rf.write("# Unresolved graph edges\n\n")
        rf.write("Endpoints that could not be matched to a known node.\n\n")
        rf.write("| source | target | type | src ok | tgt ok |\n|---|---|---|---|---|\n")
        for src, tgt, etype, so, to in sorted(unresolved_edges):
            rf.write(f"| {src} | {tgt} | {etype} | {so} | {to} |\n")

# Write edges.json
edges_json_path = os.path.join(OUT_DIR, "edges.json")
with open(edges_json_path, "w", encoding="utf-8") as f:
    json.dump(valid_edges, f, ensure_ascii=False, indent=2)

# Write edges.csv (legacy)
edges_path = os.path.join(OUT_DIR, "edges.csv")
with open(edges_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target", "type"])
    for e in valid_edges:
        writer.writerow([e["source"], e["target"], e["type"]])

print("Wrote:", people_json_path)
print("Wrote:", companies_json_path)
print("Wrote:", institutions_json_path)
print("Wrote:", geojson_path)
print("Wrote:", comp_geojson_path)
print("Wrote:", inst_geojson_path)
print("Wrote:", edges_json_path)
print("Wrote:", edges_path)
