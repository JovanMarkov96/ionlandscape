import json
import os
import re
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path(r"c:\Users\jovanm\.gemini\antigravity\scratch\ionlandscape")
JSON_PATH = BASE_DIR / "website/build/data/people.json"
CONTENT_DIR = BASE_DIR / "content/people"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_markdown_file(old_path, new_path, new_id):
    """
    Renames the markdown file and updates the 'id:' in the frontmatter.
    """
    if not old_path.exists():
        print(f"Warning: Markdown file not found at {old_path}")
        return False
    
    # Read content
    with open(old_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update ID in frontmatter
    # Regex look for "id: <something>" in the YAML frontmatter
    # Assuming standard frontmatter format
    pattern = r"^(id:\s*)(.+)$"
    def replace_id(match):
        return f"{match.group(1)}{new_id}"
    
    new_content = re.sub(pattern, replace_id, content, count=1, flags=re.MULTILINE)
    
    # Write to existing path first (to be safe before move, or just write to new path)
    # Actually, let's write to the OLD path first to ensure we have the content, then move.
    # But safer to write to NEW path, then delete old.
    
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    if old_path != new_path:
        os.remove(old_path)
        
    return True

def normalize_empty(value):
    """Recursively convert empty strings to None in dicts/lists."""
    if value == "":
        return None
    if isinstance(value, dict):
        return {k: normalize_empty(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_empty(v) for v in value]
    return value

def enforce_types(person):
    """Enforce specific data types for schema consistency."""
    
    # helper
    def to_int(val):
        if val is None: return None
        try: return int(val)
        except: return None
        
    def to_float(val):
        if val is None: return None
        try: return float(val)
        except: return None

    # Education years
    if person.get('education'):
        for edu in person['education']:
            if 'year' in edu:
                edu['year'] = to_int(edu['year'])
    
    # Thesis year
    if person.get('thesis'):
         if 'year' in person['thesis']:
             person['thesis']['year'] = to_int(person['thesis']['year'])

    # Location lat/lon
    if person.get('location'):
        loc = person['location']
        if 'lat' in loc: loc['lat'] = to_float(loc['lat'])
        if 'lon' in loc: loc['lon'] = to_float(loc['lon'])
        
    # Arrays
    for arr_field in ['platforms', 'keywords', 'affiliations', 'postdocs']:
        if arr_field in person:
            if person[arr_field] is None:
                person[arr_field] = []
            elif not isinstance(person[arr_field], list):
                # Should not happen based on current data but good for safety
                person[arr_field] = [person[arr_field]]

    return person

def main():
    print("Starting cleanup...")
    data = load_json(JSON_PATH)
    
    # 1. Fix Duplicates
    # We need to detect duplicate PREFIXES, not just identical IDs.
    # Map of prefix (int) -> list of (index, original_id)
    prefix_map = {}
    
    max_prefix = 0
    
    for i, p in enumerate(data):
        pid = p['id']
        match = re.match(r"^(\d+)-", pid)
        if match:
            prefix = int(match.group(1))
            if prefix > max_prefix:
                max_prefix = prefix
            prefix_map.setdefault(prefix, []).append((i, pid))
        else:
            # Handle IDs without prefix if any? Assume all have prefix based on file.
            pass
            
    print(f"Max existing prefix: {max_prefix}")
    
    changes_summary = []
    duplicates_fixed = 0
    
    # Sort prefixes to be deterministic
    for prefix in sorted(prefix_map.keys()):
        entries = prefix_map[prefix]
        if len(entries) > 1:
            # Collision found!
            print(f"Found duplicate prefix {prefix:03d} for IDs: {[e[1] for e in entries]}")
            
            # Keep the first one (by original index)
            # Rename the rest
            # entries are already in index order because we appended them in loop
            
            for idx, old_id in entries[1:]:
                person = data[idx]
                
                # Generate new ID
                max_prefix += 1
                new_prefix = f"{max_prefix:03d}"
                # Extract the name part
                parts = old_id.split('-', 1)
                if len(parts) > 1:
                    name_part = parts[1]
                else:
                    name_part = old_id # Fallback
                    
                new_id = f"{new_prefix}-{name_part}"
                
                print(f"  Renaming index {idx}: {old_id} -> {new_id}")
                
                # perform update
                person['id'] = new_id
                
                # Rename markdown file
                old_md_name = person.get('md_filename', f"{old_id}.md")
                new_md_name = f"{new_id}.md"
                
                old_md_path = CONTENT_DIR / old_md_name
                new_md_path = CONTENT_DIR / new_md_name
                
                success = update_markdown_file(old_md_path, new_md_path, new_id)
                if success:
                    person['md_filename'] = new_md_name
                    changes_summary.append(f"Fixed duplicate: {old_id} -> {new_id}")
                    duplicates_fixed += 1
                else:
                     print(f"FAILED to update markdown for {old_id}")

    # 2. Normalize Data
    empty_fields_fixed = 0
    
    for person in data:
        # We need to count how many fields we change from "" to None
        # Let's do a comparison roughly or just count during normalization?
        # Simpler to just normalize and count total changes? 
        # User wants "How many empty fields were normalized".
        
        # We can implement a walking counter but let's just do it in place.
        # Custom walker for counting
        def count_empty_strings(obj):
            c = 0
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if v == "": c += 1
                    else: c += count_empty_strings(v)
            elif isinstance(obj, list):
                for v in obj:
                    if v == "": c += 1
                    else: c += count_empty_strings(v)
            return c
            
        empty_fields_fixed += count_empty_strings(person)
        
        # Apply normalization
        # We replace the person dict content with the normalized version
        # But we need to keep the reference in 'data' list, so we modify contents?
        # Or just re-assign. Data is a list, so:
        # person = normalize_empty(person) -> this just rebinds local var 'person'
        # We need data[i] = normalize_empty(data[i])
        pass # loop below handles it
        
    # Re-loop to apply changes (to avoid index confusion)
    for i in range(len(data)):
        data[i] = normalize_empty(data[i])
        data[i] = enforce_types(data[i])

    # 3. Save
    save_json(data, JSON_PATH)
    
    print("\n--- SUMMARY ---")
    print(f"Duplicate IDs fixed: {duplicates_fixed}")
    print(f"Empty fields normalized: {empty_fields_fixed}")
    for change in changes_summary:
        print(change)
        
if __name__ == "__main__":
    main()
