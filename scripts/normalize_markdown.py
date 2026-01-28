import os
import glob
import frontmatter
import yaml

# Path to content
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")

def normalize_empty(value):
    """Recursively convert empty strings to None."""
    if value == "":
        return None
    if isinstance(value, dict):
        return {k: normalize_empty(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_empty(v) for v in value]
    return value

def enforce_types(meta):
    """Enforce specific data types for schema consistency."""
    
    def to_int(val):
        if val is None: return None
        try: return int(val)
        except: return None
        
    def to_float(val):
        if val is None: return None
        try: return float(val)
        except: return None

    # Education years
    if meta.get('education'):
        for edu in meta['education']:
            if isinstance(edu, dict) and 'year' in edu:
                edu['year'] = to_int(edu['year'])
    
    # Thesis year
    if meta.get('thesis'):
         if isinstance(meta['thesis'], dict) and 'year' in meta['thesis']:
             meta['thesis']['year'] = to_int(meta['thesis']['year'])

    # Location lat/lon
    if meta.get('location'):
        loc = meta['location']
        if isinstance(loc, dict):
            if 'lat' in loc: loc['lat'] = to_float(loc['lat'])
            if 'lon' in loc: loc['lon'] = to_float(loc['lon'])
            
    # Arrays
    for arr_field in ['platforms', 'keywords', 'affiliations', 'postdocs', 'labels', 'ion_species']:
        if arr_field in meta:
            if meta[arr_field] is None:
                meta[arr_field] = []
            elif not isinstance(meta[arr_field], list):
                meta[arr_field] = [meta[arr_field]]

    return meta

def main():
    print(f"Normalizing markdown files in {CONTENT_DIR}...")
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    
    count = 0
    for file_path in files:
        changed = False
        post = frontmatter.load(file_path)
        
        # 1. Normalize empty strings
        # We need to detect if changes happen to avoid spurious writes?
        # A deep compare is hard, so we just process and maybe write always, or check equality.
        
        old_meta = str(post.metadata)
        
        post.metadata = normalize_empty(post.metadata)
        post.metadata = enforce_types(post.metadata)
        
        if str(post.metadata) != old_meta:
            # Save
            # We use frontmatter.dump but need to be careful with formatting?
            # frontmatter.dump uses YAML. defaults are usually fine.
            
            with open(file_path, 'wb') as f:
                frontmatter.dump(post, f)
            print(f"Updated {os.path.basename(file_path)}")
            count += 1
            
    print(f"Normalized {count} markdown files.")

if __name__ == "__main__":
    main()
