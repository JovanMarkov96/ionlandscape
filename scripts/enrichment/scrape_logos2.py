import os
import frontmatter
import urllib.request
from urllib.parse import urlparse
import time

os.makedirs("website/static/logos", exist_ok=True)

for filename in os.listdir("content/companies"):
    if not filename.endswith(".md"): continue
    path = os.path.join("content/companies", filename)
    post = frontmatter.load(path)
    
    website = post.metadata.get("links", {}).get("website", "")
    slug = post.metadata.get("id")
    
    if website and slug:
        domain = urlparse(website).netloc
        if domain.startswith("www."):
            domain = domain[4:]
            
        # Use Google Favicon API as a fallback which allows larger sizes up to 128/256
        logo_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
        logo_path = f"website/static/logos/{slug}.png"
        
        try:
            req = urllib.request.Request(logo_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(logo_path, "wb") as out:
                    out.write(response.read())
            
            if "media" not in post.metadata or not isinstance(post.metadata["media"], dict):
                post.metadata["media"] = {}
                
            post.metadata["media"]["logo_path"] = f"/logos/{slug}.png"
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))
                
            print(f"Success for {slug} ({domain})")
        except Exception as e:
            print(f"Failed for {slug} ({domain}): {e}")
    time.sleep(0.5)

