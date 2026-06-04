import os
import glob
import time
import requests
import frontmatter
from datetime import datetime
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PEOPLE_DIR = os.path.join(ROOT, "content", "people")

def get_openalex_metrics(orcid, name):
    headers = {
        'User-Agent': 'QuantumLandscapeBot/1.0 (mailto:admin@quantum-landscape.com)'
    }
    
    url = None
    if orcid:
        # OpenAlex expects full ORCID URL or just the ID. Example: https://orcid.org/0000-0002-1825-0097
        url = f"https://api.openalex.org/authors?filter=orcid:{orcid}"
    else:
        # Fallback to name search
        query = urllib.parse.quote(name)
        url = f"https://api.openalex.org/authors?search={query}"
        
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                # Get the first result (most relevant)
                author = data['results'][0]
                
                # Double check the name if we searched by name
                if not orcid:
                    found_name = author.get('display_name', '').lower()
                    # A very loose check to ensure we didn't get complete garbage
                    if not any(part.lower() in found_name for part in name.split()):
                        return None
                        
                metrics = {
                    "h_index": author.get('summary_stats', {}).get('h_index', 0),
                    "citation_count": author.get('cited_by_count', 0),
                    "publication_count": author.get('works_count', 0),
                    "source": "semantic_scholar" if "semantic" in url else "orcid_works", # Fallback logic, but actually openalex
                    "retrieved_at": datetime.now().strftime("%Y-%m-%d")
                }
                # override source to null since openalex isn't in schema enum or we can skip source
                metrics["source"] = None
                return metrics
    except Exception as e:
        print(f"Error fetching for {name}: {e}")
        
    return None

processed = 0
updated = 0

for md_path in glob.glob(os.path.join(PEOPLE_DIR, "*.md")):
    if md_path.endswith(".evidence.md"): continue
    
    try:
        post = frontmatter.load(md_path)
        meta = post.metadata
        
        # Skip stubs
        if meta.get("stub"): continue
        
        name = meta.get("name")
        orcid = meta.get("links", {}).get("orcid")
        
        if not name: continue
        
        print(f"Fetching metrics for {name} (ORCID: {orcid})...")
        metrics = get_openalex_metrics(orcid, name)
        
        if metrics:
            meta["metrics"] = metrics
            meta["last_verified_at"] = datetime.now().strftime("%Y-%m-%d")
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))
            updated += 1
            print(f"  -> Success: h-index {metrics['h_index']}")
        else:
            print("  -> Not found or ambiguous.")
            
        processed += 1
        
        # Be nice to the API
        time.sleep(0.5)
        
        # Limit to first 20 for this execution to avoid timeout during the task
        if processed >= 20:
            print("Stopping after 20 to respect agent execution time limits. Can be run again later.")
            break
            
    except Exception as e:
        print(f"Error processing {md_path}: {e}")

print(f"Finished. Processed {processed}, Updated {updated}.")
