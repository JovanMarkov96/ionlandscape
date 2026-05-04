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
  "c003-alpine-quantum-technologies-aqt": {
      "data": {
          "founded_year": 2017,
          "status": {"operating_status": "private"},
          "platforms": ["trapped_ion"],
          "applications": ["computing", "simulation"],
          "approach": {
              "elevator_pitch": "Commercializing ion-trap quantum computers capable of operating in standard data center environments.",
              "differentiators": ["Room-temperature 19-inch rack-mounted systems", "Calcium ions"],
              "architecture_tags": ["calcium_ions", "rack_mounted"]
          },
          "products": [
            {"name": "PINE", "description": "24-qubit trapped-ion quantum computer", "stage": "ga", "release_date": "2023-01-01", "source": "https://www.aqt.eu/pine"}
          ],
          "people": {
            "founders": [{"name": "Rainer Blatt"}, {"name": "Thomas Monz"}, {"name": "Peter Zoller"}],
            "leadership": [{"name": "Thomas Monz", "role": "CEO"}],
            "spun_out_of": ["University of Innsbruck", "IQOQI"]
          },
          "sources": [{"url": "https://www.aqt.eu/about"}]
      },
      "evidence": "# Evidence Map: AQT\n## Sources\n1. [AQT About](https://www.aqt.eu/about)"
  },
  "c004-oxford-ionics": {
      "data": {
          "founded_year": 2019,
          "status": {"operating_status": "private"},
          "platforms": ["trapped_ion"],
          "applications": ["computing"],
          "approach": {
              "elevator_pitch": "Trapped-ion quantum computing using electronic qubit control directly integrated into the quantum processor chip.",
              "differentiators": ["No lasers for qubit control", "Electronic microwave control"],
              "architecture_tags": ["microwave_control", "surface_traps"]
          },
          "people": {
            "founders": [{"name": "Chris Ballance"}, {"name": "Tom Harty"}],
            "leadership": [{"name": "Chris Ballance", "role": "CEO"}],
            "spun_out_of": ["University of Oxford"]
          },
          "sources": [{"url": "https://www.oxionics.com/about"}]
      },
      "evidence": "# Evidence Map: Oxford Ionics\n## Sources\n1. [Oxford Ionics](https://www.oxionics.com/about)"
  },
  "c005-q-ctrl": {
      "data": {
          "founded_year": 2017,
          "status": {"operating_status": "private"},
          "platforms": ["trapped_ion", "superconducting", "neutral_atom"],
          "applications": ["software_control", "sensing_metrology"],
          "approach": {
              "elevator_pitch": "Quantum control software to accelerate the development of useful quantum technology.",
              "differentiators": ["Hardware-agnostic error suppression", "AI-driven quantum control"]
          },
          "products": [
             {"name": "Black Opal", "description": "Educational platform", "stage": "ga"},
             {"name": "Fire Opal", "description": "Error suppression software", "stage": "ga"}
          ],
          "people": {
            "founders": [{"name": "Michael Biercuk"}],
            "leadership": [{"name": "Michael Biercuk", "role": "CEO"}],
            "spun_out_of": ["University of Sydney"]
          },
          "sources": [{"url": "https://qctrl.com/about"}]
      },
      "evidence": "# Evidence Map: Q-CTRL\n## Sources\n1. [Q-CTRL About](https://qctrl.com/about)"
  },
  "c007-quantum-machines": {
      "data": {
          "founded_year": 2018,
          "status": {"operating_status": "private"},
          "platforms": ["trapped_ion", "superconducting", "quantum_dot"],
          "applications": ["software_control", "computing"],
          "approach": {
              "elevator_pitch": "Quantum Orchestration Platform providing hardware and software for operating quantum computers.",
              "differentiators": ["Pulse-level control", "Real-time classical processing", "Hardware-agnostic OPX"],
              "architecture_tags": ["pulse_processor", "fpga"]
          },
          "products": [
             {"name": "OPX+", "description": "Quantum control hardware", "stage": "ga"},
             {"name": "QUA", "description": "Pulse-level programming language", "stage": "ga"}
          ],
          "people": {
            "founders": [{"name": "Itamar Sivan"}, {"name": "Yonatan Cohen"}, {"name": "Nissim Ofek"}],
            "leadership": [{"name": "Itamar Sivan", "role": "CEO"}],
            "spun_out_of": ["Weizmann Institute of Science"]
          },
          "sources": [{"url": "https://www.quantum-machines.co/about"}]
      },
      "evidence": "# Evidence Map: QM\n## Sources\n1. [QM About](https://www.quantum-machines.co/about)"
  },
  "c008-classiq-technologies": {
      "data": {
          "founded_year": 2020,
          "status": {"operating_status": "private"},
          "platforms": ["trapped_ion", "superconducting", "neutral_atom"],
          "applications": ["software_control", "computing"],
          "approach": {
              "elevator_pitch": "Platform for designing quantum software circuits.",
              "differentiators": ["Functional-level circuit design", "Constraint-based synthesis"]
          },
          "people": {
            "founders": [{"name": "Nir Minerbi"}, {"name": "Amir Naveh"}, {"name": "Yehuda Naveh"}],
            "leadership": [{"name": "Nir Minerbi", "role": "CEO"}],
            "spun_out_of": []
          },
          "sources": [{"url": "https://www.classiq.io/about"}]
      },
      "evidence": "# Evidence Map: Classiq\n## Sources\n1. [Classiq About](https://www.classiq.io/about)"
  },
  "c001-quantum-art": {
      "data": {
          "founded_year": 2022,
          "status": {"operating_status": "stealth"},
          "platforms": ["trapped_ion"],
          "applications": ["computing"],
          "approach": {
              "elevator_pitch": "Scaling trapped ion quantum computers.",
              "differentiators": []
          },
          "people": {
            "founders": [{"name": "Roee Ozeri"}, {"name": "Tal David"}],
            "leadership": [{"name": "Tal David", "role": "CEO"}],
            "spun_out_of": ["Weizmann Institute of Science"]
          },
          "sources": [{"url": "https://quantum-art.tech/about"}]
      },
      "evidence": "# Evidence Map: Quantum Art\n## Sources\n1. [QA About](https://quantum-art.tech/about)"
  },
  "c013-qedma": {
      "data": {
          "founded_year": 2020,
          "status": {"operating_status": "private"},
          "platforms": ["trapped_ion", "superconducting"],
          "applications": ["software_control"],
          "approach": {
              "elevator_pitch": "Quantum error mitigation software.",
              "differentiators": ["Algorithmic error mitigation"]
          },
          "people": {
            "founders": [{"name": "Asaf Ozeri"}],
            "leadership": [{"name": "Asaf Ozeri", "role": "CEO"}],
             "spun_out_of": []
          },
          "sources": [{"url": "https://qedma.com"}]
      },
      "evidence": "# Evidence Map: Qedma\n## Sources\n1. [Qedma Website](https://qedma.com)"
  },
  "c014-quantum-source-labs": {
      "data": {
          "founded_year": 2021,
          "status": {"operating_status": "private"},
          "platforms": ["photonic"],
          "applications": ["computing"],
          "approach": {
              "elevator_pitch": "Scaling photonic quantum computers using cavity QED.",
              "differentiators": ["High-efficiency single photon sources"]
          },
          "people": {
            "founders": [{"name": "Oded Melamed"}],
            "leadership": [{"name": "Oded Melamed", "role": "CEO"}],
             "spun_out_of": ["Weizmann Institute of Science"]
          },
          "sources": [{"url": "https://qs-labs.com"}]
      },
      "evidence": "# Evidence Map: Quantum Source\n## Sources\n1. [QS Labs](https://qs-labs.com)"
  }
}

for c_slug, c_info in companies_data.items():
    filepath = f"content/companies/{c_slug}.md"
    update_company(filepath, c_info["data"], c_info["evidence"])
    print(f"Processed {c_slug}")
