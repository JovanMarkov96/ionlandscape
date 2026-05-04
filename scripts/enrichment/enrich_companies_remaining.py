import os
import frontmatter
from datetime import datetime

def update_company(filepath, data_updates, evidence_content):
    if not os.path.exists(filepath):
        return
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

companies_data = {
  "c009-quantlr": {
      "data": {
          "founded_year": 2018,
          "status": {"operating_status": "private"},
          "platforms": ["photonic"],
          "applications": ["networking"],
          "approach": {
              "elevator_pitch": "Quantum-secure communication infrastructure.",
              "differentiators": ["QKD infrastructure"]
          },
          "sources": [{"url": "https://quantlr.com/about"}]
      },
      "evidence": "# Evidence Map: QuantLR\n## Sources\n1. [QuantLR](https://quantlr.com/about)"
  },
  "c010-quantum-transistors": {
      "data": {
          "founded_year": 2021,
          "status": {"operating_status": "stealth"},
          "platforms": ["silicon_spin", "topological"],
          "applications": ["computing"],
          "approach": {
              "elevator_pitch": "Developer of semiconductor-based quantum processor technology.",
              "differentiators": []
          },
          "sources": [{"url": "https://quantumtransistors.com"}]
      },
      "evidence": "# Evidence Map: Quantum Transistors\n## Sources\n1. [Company Site](https://quantumtransistors.com)"
  },
  "c011-quancilla": {
      "data": {
          "founded_year": 2023,
          "status": {"operating_status": "stealth"},
          "modality": "software",
          "platforms": ["trapped_ion", "superconducting"],
          "applications": ["software_control", "computing"],
          "approach": {
              "elevator_pitch": "Early-stage quantum software startup.",
              "differentiators": []
          },
          "sources": [{"url": "https://quancilla.com"}]
      },
      "evidence": "# Evidence Map: Quancilla\n## Sources\n1. [Quancilla](https://quancilla.com)"
  },
  "c012-enquantum": {
      "data": {
          "founded_year": 2022,
          "status": {"operating_status": "private"},
          "platforms": ["photonic"],
          "applications": ["networking"],
          "approach": {
              "elevator_pitch": "Quantum communication infrastructure.",
              "differentiators": []
          },
          "sources": [{"url": "https://enquantum.com"}]
      },
      "evidence": "# Evidence Map: enQuantum\n## Sources\n1. [enQuantum](https://enquantum.com)"
  },
  "c015-quamcore": {
      "data": {
          "founded_year": 2024,
          "status": {"operating_status": "stealth"},
          "platforms": ["superconducting"],
          "applications": ["computing"],
          "approach": {
              "elevator_pitch": "Deep-tech quantum computing startup developing a superconducting processor.",
              "differentiators": ["Novel superconducting architectures"]
          },
          "people": {
              "spun_out_of": ["Weizmann Institute of Science", "Technion"]
          },
          "sources": [{"url": "https://quamcore.com"}]
      },
      "evidence": "# Evidence Map: QuamCore\n## Sources\n1. [QuamCore](https://quamcore.com)"
  }
}

for c_slug, c_info in companies_data.items():
    filepath = f"content/companies/{c_slug}.md"
    update_company(filepath, c_info["data"], c_info["evidence"])
    print(f"Processed {c_slug}")
