import json
import os
import re
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUGGESTIONS_FILE = os.path.join(BASE_DIR, "scripts", "enrichment", "suggestions.json")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")

def load_suggestions():
    if not os.path.exists(SUGGESTIONS_FILE):
        print(f"No suggestions file found at {SUGGESTIONS_FILE}")
        return []
    with open(SUGGESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def update_profile(file_path, suggestion):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        print(f"Skipping {file_path}: Invalid frontmatter")
        return

    frontmatter_raw = match.group(1)
    body = match.group(2)
    
    try:
        data = yaml.safe_load(frontmatter_raw)
    except yaml.YAMLError as e:
        print(f"Skipping {file_path}: YAML error {e}")
        return

    # Apply suggestions
    fields = suggestion.get("suggested_fields", {})
    updated = False
    
    for key, value in fields.items():
        if value is None:
            continue
            
        # Handle nested keys like links.orcid
        parts = key.split(".")
        target = data
        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]
        
        last_key = parts[-1]
        
        # Only update if value is different or missing
        if target.get(last_key) != value:
            print(f"  - Updating {key}: {value}")
            target[last_key] = value
            updated = True

    if updated:
        # Write back
        new_frontmatter = yaml.dump(data, sort_keys=True, allow_unicode=True)
        new_content = f"---\n{new_frontmatter}---\n{body}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes for {file_path}")

def main():
    suggestions = load_suggestions()
    print(f"Loaded {len(suggestions)} suggestions")
    
    for item in suggestions:
        pid = item["profile_id"]
        # Find file
        # Try exact ID match first, then search
        filename = f"{pid}.md"
        file_path = os.path.join(CONTENT_DIR, filename)
        
        if not os.path.exists(file_path):
            # Try to find by ID in file content if filename doesn't match? 
            # For now assume filename matches ID as per repo convention
            print(f"File not found for {pid}")
            continue
            
        print(f"Processing {pid}...")
        update_profile(file_path, item)

if __name__ == "__main__":
    main()
