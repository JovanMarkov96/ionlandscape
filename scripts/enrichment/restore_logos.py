import os
import frontmatter
from datetime import datetime

for filename in os.listdir("content/companies"):
    if not filename.endswith(".md"): continue
    
    filepath = os.path.join("content/companies", filename)
    post = frontmatter.load(filepath)
    slug = post.metadata.get("id")
    
    # Safely apply logo path
    if "media" not in post.metadata or not isinstance(post.metadata["media"], dict):
        post.metadata["media"] = {}
        
    # Set logo path if file exists
    if os.path.exists(f"website/static/logos/{slug}.png"):
        post.metadata["media"]["logo_path"] = f"/logos/{slug}.png"
        
    post.metadata['last_verified_at'] = datetime.now().strftime("%Y-%m-%d")
    post.metadata['verification_source_count'] = len(post.metadata.get('sources', []))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
        
print("Logos mapping restored securely.")
