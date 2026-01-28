#!/usr/bin/env python3
"""
create_profile_template.py

Create a new profile template with minimal verified frontmatter.
Prompts for required information and validates before creating.

Usage:
    python scripts/create_profile_template.py
"""

import os
import sys
from datetime import datetime
import frontmatter
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")


def slugify(name: str) -> str:
    """Convert name to slug format."""
    return re.sub(r'[^\w\s-]', '', name.lower().strip()).replace(' ', '-')


def get_next_id() -> str:
    """Get next available ID number."""
    import glob
    
    existing_ids = []
    for md_file in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        basename = os.path.basename(md_file)
        match = re.match(r'(\d+)-', basename)
        if match:
            existing_ids.append(int(match.group(1)))
    
    if existing_ids:
        return str(max(existing_ids) + 1).zfill(3)
    return "001"


def prompt_required(field_name: str, description: str) -> str:
    """Prompt for a required field."""
    while True:
        value = input(f"{field_name} ({description}): ").strip()
        if value:
            return value
        print(f"  ❌ {field_name} is required. Please enter a value.")


def prompt_optional(field_name: str, description: str, default: str = None) -> str:
    """Prompt for an optional field."""
    prompt_text = f"{field_name} ({description})"
    if default:
        prompt_text += f" [{default}]"
    prompt_text += ": "
    
    value = input(prompt_text).strip()
    return value if value else default


def prompt_yes_no(question: str, default: bool = None) -> bool:
    """Prompt for yes/no answer."""
    suffix = " [Y/n]: " if default is True else " [y/N]: " if default is False else " [y/n]: "
    
    while True:
        answer = input(question + suffix).strip().lower()
        
        if not answer and default is not None:
            return default
        
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print("  Please answer 'y' or 'n'")


def main():
    print("=" * 80)
    print("Ion Landscape - Create New Profile")
    print("=" * 80)
    print()
    print("This tool creates a minimal profile template with verified information.")
    print("Only fill in fields for which you have authoritative sources.")
    print("Leave fields empty (press Enter) if you cannot verify the information.")
    print()
    
    # Get basic information
    name = prompt_required("Full Name", "e.g., Jonathan P. Home")
    
    # Generate ID
    next_num = get_next_id()
    slug = slugify(name)
    suggested_id = f"{next_num}-{slug}"
    person_id = prompt_optional("Person ID", "unique identifier", suggested_id)
    
    # Sort name (usually Last, First Middle)
    name_parts = name.split()
    if len(name_parts) >= 2:
        suggested_sort = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
    else:
        suggested_sort = name
    sort_name = prompt_optional("Sort Name", "for alphabetical sorting", suggested_sort)
    
    print("\n--- Current Position ---")
    institution = prompt_required("Institution", "e.g., ETH Zürich")
    title = prompt_optional("Title", "e.g., Professor, Assistant Professor", "Professor")
    
    print("\n--- Location ---")
    city = prompt_required("City", "e.g., Zürich")
    country = prompt_required("Country", "e.g., Switzerland")
    region = prompt_optional("Region/State", "e.g., Zürich, California", "")
    
    print("\n⚠️  Coordinates (lat/lon) should be verified from a reliable source")
    print("   You can leave these empty and fill them in later.")
    lat_str = prompt_optional("Latitude", "decimal degrees", "")
    lon_str = prompt_optional("Longitude", "decimal degrees", "")
    
    lat = float(lat_str) if lat_str else None
    lon = float(lon_str) if lon_str else None
    
    print("\n--- Classification ---")
    print("Group type: 1) experimental  2) theory")
    group_type_choice = prompt_optional("Choice", "1 or 2", "1")
    group_type = "experimental" if group_type_choice == "1" else "theory"
    label = "Experimental group" if group_type == "experimental" else "Theory group"
    
    print("\n--- Links ---")
    print("Only add links that you have verified.")
    homepage = prompt_optional("Homepage URL", "personal or group website", "")
    group_page = prompt_optional("Group Page URL", "university group page", "")
    google_scholar = prompt_optional("Google Scholar URL", "full profile URL", "")
    orcid = prompt_optional("ORCID URL", "e.g., https://orcid.org/0000-...", "")
    
    print("\n--- Education (PhD) ---")
    print("Only fill if you can verify this information from reliable sources.")
    has_phd_info = prompt_yes_no("Do you have verified PhD information?", False)
    
    education = []
    if has_phd_info:
        phd_institution = prompt_optional("PhD Institution", "e.g., University of Oxford", "")
        phd_year_str = prompt_optional("PhD Year", "e.g., 2006", "")
        phd_advisor = prompt_optional("PhD Advisor", "full name", "")
        
        phd_year = int(phd_year_str) if phd_year_str else None
        
        print("\nConfidence level:")
        print("  1) confirmed - verified from official sources")
        print("  2) academictree_only - only found on AcademicTree")
        print("  3) not_found - attempted verification but not found")
        confidence_choice = prompt_optional("Confidence", "1, 2, or 3", "")
        confidence_map = {
            "1": "confirmed",
            "2": "academictree_only",
            "3": "not_found"
        }
        confidence = confidence_map.get(confidence_choice)
        
        education.append({
            "degree": "PhD (Physics)",
            "institution": phd_institution if phd_institution else None,
            "year": phd_year,
            "advisor": phd_advisor if phd_advisor else None,
            "confidence": confidence,
            "note": None
        })
    
    print("\n--- Research Platforms ---")
    print("Common platforms: Trapped ions, Neutral atoms, Superconducting qubits, etc.")
    platforms_input = prompt_optional("Platforms", "comma-separated", "Trapped ions")
    platforms = [p.strip() for p in platforms_input.split(',') if p.strip()]
    
    # Build metadata
    metadata = {
        "id": person_id,
        "name": name,
        "sort_name": sort_name,
        "current_position": {
            "institution": institution,
            "title": title
        },
        "location": {
            "city": city,
            "country": country,
            "region": region if region else None,
            "lat": lat,
            "lon": lon
        },
        "group_type": group_type,
        "labels": [label],
        "platforms": platforms,
        "education": education if education else [],
        "postdocs": [],
        "affiliations": [],
        "keywords": [],
        "ion_species": [],
        "links": {},
        "thesis": {
            "title": None,
            "year": None,
            "link": None,
            "note": None
        },
        "created_at": datetime.now().strftime('%Y-%m-%d'),
        "updated_at": datetime.now().strftime('%Y-%m-%d')
    }
    
    # Add links
    if homepage:
        metadata["links"]["homepage"] = homepage
    if group_page:
        metadata["links"]["group_page"] = group_page
    if google_scholar:
        metadata["links"]["google_scholar"] = google_scholar
    if orcid:
        metadata["links"]["orcid"] = orcid
    
    # Default content
    content = f"{name} is a researcher at {institution}.\n\n## Publications\nSee full publication list on Google Scholar."
    
    # Preview
    print("\n" + "=" * 80)
    print("PREVIEW")
    print("=" * 80)
    print(f"\nFilename: {person_id}.md")
    print("\nFrontmatter:")
    print("---")
    import yaml
    print(yaml.dump(metadata, default_flow_style=False, sort_keys=False))
    print("---")
    print(f"\n{content}\n")
    
    # Confirm
    if not prompt_yes_no("\nCreate this profile?", True):
        print("Cancelled.")
        return 1
    
    # Create file
    filename = f"{person_id}.md"
    filepath = os.path.join(CONTENT_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"\n❌ Error: File already exists: {filepath}")
        return 1
    
    post = frontmatter.Post(content, **metadata)
    
    with open(filepath, 'wb') as f:
        frontmatter.dump(post, f)
    
    print(f"\n✅ Created: {filepath}")
    print(f"\nNext steps:")
    print(f"  1. Review and verify the information")
    print(f"  2. Add sources as comments or in commit message")
    print(f"  3. Run: python scripts/verify_profile_data.py {person_id}")
    print(f"  4. Commit: git add {filepath}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
