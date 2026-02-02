import os
import re
import glob

PEOPLE_DIR = os.path.join(os.path.dirname(__file__), '../content/people')

def renumber_profiles():
    # Get all markdown files
    files = glob.glob(os.path.join(PEOPLE_DIR, "*.md"))
    
    # Parse files into (id, filename, full_path)
    parsed_files = []
    for fpath in files:
        fname = os.path.basename(fpath)
        match = re.match(r'(\d{3})-(.*)', fname)
        if match:
            current_id = int(match.group(1))
            slug = match.group(2) # includes .md
            parsed_files.append({
                'id': current_id,
                'slug': slug,
                'path': fpath,
                'filename': fname
            })
    
    # Sort by current ID
    sorted_files = sorted(parsed_files, key=lambda x: x['id'])
    
    print(f"Found {len(sorted_files)} profiles. Starting renumbering...")
    
    changes = []
    
    # Renumber
    for index, file_info in enumerate(sorted_files, start=1):
        old_id = file_info['id']
        new_id = index
        
        # Format new ID
        new_id_str = f"{new_id:03d}"
        old_id_str = f"{old_id:03d}"
        
        # New filename
        new_filename = f"{new_id_str}-{file_info['slug']}"
        new_path = os.path.join(PEOPLE_DIR, new_filename)
        
        # Even if ID is same, check if content needs update (unlikely if same ID, but good for consistency)
        # But primarily only act if ID changes
        if new_id != old_id:
            print(f"Renaming {file_info['filename']} -> {new_filename}")
            
            # 1. Update Content
            with open(file_info['path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Regex update the id: field
            # Pattern: id: 001-slug
            # We want to replace just the 001 part in the ID line, or the whole ID line
            
            # Robust replacement for "id: XXX-slug"
            # We construct the old ID string expected in the file
            old_id_val = f"{old_id_str}-{file_info['slug'][:-3]}" # remove .md
            new_id_val = f"{new_id_str}-{file_info['slug'][:-3]}"
            
            # Using regex to ensure we only target the 'id:' key
            # Looking for "id: old_id_val"
            pattern = re.compile(rf"^id:\s*{re.escape(old_id_val)}", re.MULTILINE)
            
            if pattern.search(content):
                new_content = pattern.sub(f"id: {new_id_val}", content)
                
                with open(file_info['path'], 'w', encoding='utf-8') as f:
                    f.write(new_content)
            else:
                print(f"WARNING: Could not find 'id: {old_id_val}' in {file_info['filename']}")
            
            # 2. Rename File
            # We need to close the file handle before renaming (done by with block)
            try:
                os.rename(file_info['path'], new_path)
                changes.append(f"{old_id_str} -> {new_id_str} ({file_info['slug'][:-3]})")
            except OSError as e:
                print(f"Error renaming {file_info['filename']}: {e}")

    print(f"\nRenumbering complete. {len(changes)} files updated.")
    # Verify mapping
    print("Change Log:")
    for change in changes:
        print(change)

if __name__ == "__main__":
    renumber_profiles()
