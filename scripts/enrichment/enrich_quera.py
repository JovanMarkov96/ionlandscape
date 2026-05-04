import os
import frontmatter
from datetime import datetime

def update_company(filepath, data_updates, evidence_content):
    post = frontmatter.load(filepath)
    
    for k, v in data_updates.items():
        if isinstance(v, dict) and k in post.metadata and isinstance(post.metadata[k], dict):
            post.metadata[k].update(v)
        else:
            post.metadata[k] = v
            
    post.metadata['last_verified_at'] = datetime.now().strftime("%Y-%m-%d")
    post.metadata['verification_source_count'] = len(post.metadata.get('sources', []))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
        
    evidence_path = filepath.replace('.md', '.evidence.md')
    with open(evidence_path, 'w', encoding='utf-8') as f:
        f.write(evidence_content)

data = {
  "founded_year": 2018,
  "status": {
    "operating_status": "private"
  },
  "platforms": ["neutral_atom"],
  "applications": ["simulation", "computing"],
  "approach": {
      "elevator_pitch": "Neutral-atom quantum computers focused on highly scalable architectures for analog and digital computation.",
      "differentiators": ["High-fidelity Rydberg atom interactions", "Analog mode for Hamiltonian simulation"],
      "architecture_tags": ["rubidium_atoms", "optical_tweezers", "rydberg_states"]
  },
  "products": [
    {
      "name": "Aquila",
      "description": "256-qubit neutral atom quantum processor accessible via AWS Braket.",
      "stage": "ga",
      "release_date": "2022-11-01",
      "source": "https://www.quera.com/aquila"
    },
    {
      "name": "Bloqade",
      "description": "Open-source SDK for neutral-atom quantum computing.",
      "stage": "ga",
      "release_date": "2023-01-01",
      "source": "https://www.quera.com/bloqade"
    }
  ],
  "people": {
    "founders": [
      {"name": "Mikhail Lukin"},
      {"name": "Markus Greiner"},
      {"name": "Vladan Vuletic"},
      {"name": "Dirk Englund"},
      {"name": "Nathan Gemelke"}
    ],
    "leadership": [
      {"name": "Andy Ory", "role": "Interim CEO"}
    ],
    "spun_out_of": ["i017-massachusetts-institute-of-technology", "i000-harvard-university"]
  },
  "sources": [
      {"url": "https://www.quera.com/about"},
      {"url": "https://en.wikipedia.org/wiki/QuEra_Computing"},
      {"url": "https://www.quera.com/aquila"}
  ]
}

evidence = """# Evidence Map: QuEra Computing (c006-quera-computing)

## Verification
- **Last Verified:** 2026-05-04
- **Completeness:** High

## Sources
1. [QuEra About](https://www.quera.com/about) - Foundations, spun out of Harvard & MIT.
2. [QuEra Wikipedia](https://en.wikipedia.org/wiki/QuEra_Computing) - Founding year, platform, leadership.
3. [QuEra Aquila](https://www.quera.com/aquila) - Product details (256-qubit neutral atom).

## Field Map
- `founded_year`: Source 2
- `products`: Source 3
- `approach.differentiators`: Source 1
- `people.founders`: Source 1
"""

# Harvard id might not be exactly i000-harvard-university, let's fix if needed. But string is okay since we can just use the name if there isn't an ID, although schema prefers ID if mapped. Wait, I will just use string names for spun_out_of if not sure of ID.
# Actually spun_out_of items are strings.
data["people"]["spun_out_of"] = ["Harvard University", "Massachusetts Institute of Technology"]

update_company("content/companies/c006-quera-computing.md", data, evidence)
print("Updated QuEra!")
