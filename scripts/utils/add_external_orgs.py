#!/usr/bin/env python3
"""Add real ecosystem orgs referenced by edges but missing from the dataset,
alias the two that belong to existing institutions, and clean prose
spun_out_from values that are not real org references."""
import os, frontmatter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INST = os.path.join(ROOT, "content", "institutions")
COMP = os.path.join(ROOT, "content", "companies")

NEW_INSTITUTIONS = {
    "i060-harvard-university.md": {
        "name": "Harvard University", "entity_type": "institution",
        "institution_type": "university",
        "location": {"city": "Cambridge", "country": "USA", "lat": 42.3770, "lon": -71.1167},
        "focus_areas": ["Quantum Simulation", "AMO Physics"],
        "platforms_represented": ["neutral_atom"],
        "short_description": "Harvard University is a private research university in Cambridge, Massachusetts; its physics department is a leading centre for neutral-atom quantum simulation and AMO research.",
        "links": {"website": "https://www.harvard.edu/"},
    },
    "i061-hebrew-university-of-jerusalem.md": {
        "name": "Hebrew University of Jerusalem", "entity_type": "institution",
        "institution_type": "university",
        "location": {"city": "Jerusalem", "country": "Israel", "lat": 31.7767, "lon": 35.1974},
        "focus_areas": ["Quantum Communication", "AMO Physics"],
        "platforms_represented": ["trapped_ion"],
        "short_description": "The Hebrew University of Jerusalem is Israel's leading research university and a hub for quantum information and AMO physics research.",
        "links": {"website": "https://en.huji.ac.il/"},
    },
    "i062-lawrence-berkeley-national-laboratory.md": {
        "name": "Lawrence Berkeley National Laboratory", "entity_type": "institution",
        "institution_type": "national_lab",
        "location": {"city": "Berkeley", "country": "USA", "lat": 37.8759, "lon": -122.2503},
        "focus_areas": ["Quantum Computing", "Quantum Sensing"],
        "platforms_represented": ["trapped_ion"],
        "short_description": "Lawrence Berkeley National Laboratory (Berkeley Lab) is a U.S. Department of Energy national laboratory conducting research across quantum computing, sensing and materials.",
        "links": {"website": "https://www.lbl.gov/"},
    },
    "i063-shanghai-qi-zhi-institute.md": {
        "name": "Shanghai Qi Zhi Institute", "entity_type": "institution",
        "institution_type": "research_centre",
        "location": {"city": "Shanghai", "country": "China", "lat": 31.2304, "lon": 121.4737},
        "focus_areas": ["Quantum Computing", "Quantum Simulation"],
        "platforms_represented": ["trapped_ion"],
        "short_description": "The Shanghai Qi Zhi Institute is a research institute focused on artificial intelligence and quantum information science.",
        "links": {"website": "https://sqz.ac.cn/"},
    },
}

NEW_COMPANIES = {
    "c016-universal-quantum.md": {
        "name": "Universal Quantum", "entity_type": "company",
        "platforms": ["trapped_ion"], "categories": ["Hardware"],
        "location": {"city": "Brighton", "country": "United Kingdom", "lat": 50.8225, "lon": -0.1372},
        "short_summary": "Universal Quantum is a UK company building scalable trapped-ion quantum computers using modular architecture and electric-field-link qubit connections.",
        "links": {"website": "https://universalquantum.com/"},
    },
    "c017-eleqtron.md": {
        "name": "eleQtron", "entity_type": "company",
        "platforms": ["trapped_ion"], "categories": ["Hardware"],
        "location": {"city": "Siegen", "country": "Germany", "lat": 50.8748, "lon": 8.0243},
        "short_summary": "eleQtron is a German quantum computing company developing trapped-ion hardware based on its MAGIC (magnetic gradient induced coupling) technology.",
        "links": {"website": "https://eleqtron.com/"},
    },
}

ALIASES = {
    "i004-duke-university.md": ["Duke Quantum Center"],
    "i014-johannes-gutenberg-university-mainz.md": ["Helmholtz Institute Mainz"],
}

# Companies whose spun_out_from is descriptive prose, not a real org -> clear it
CLEAN_SPINOUT = [
    "c008-classiq-technologies.md", "c013-qedma.md",
    "c014-quantum-source-labs.md", "c015-quamcore.md",
]

def write_new(dirpath, table):
    for fname, meta in table.items():
        fp = os.path.join(dirpath, fname)
        if os.path.exists(fp):
            print("exists:", fname); continue
        meta = dict(meta)
        meta["id"] = fname[:-3]
        meta["schema_version"] = 1
        post = frontmatter.Post("", **meta)
        with open(fp, "wb") as f:
            frontmatter.dump(post, f)
        print("created:", fname)

write_new(INST, NEW_INSTITUTIONS)
write_new(COMP, NEW_COMPANIES)

for fname, al in ALIASES.items():
    fp = os.path.join(INST, fname)
    post = frontmatter.load(fp)
    cur = post.metadata.get("aliases", []) or []
    changed = False
    for a in al:
        if a not in cur:
            cur.append(a); changed = True
    if changed:
        post.metadata["aliases"] = cur
        with open(fp, "wb") as f:
            frontmatter.dump(post, f)
        print("aliased:", fname, al)

for fname in CLEAN_SPINOUT:
    fp = os.path.join(COMP, fname)
    post = frontmatter.load(fp)
    people_block = post.metadata.get("people", {}) or {}
    if people_block.get("spun_out_of"):
        people_block["spun_out_of"] = []
        post.metadata["people"] = people_block
        with open(fp, "wb") as f:
            frontmatter.dump(post, f)
        print("cleaned spinout prose:", fname)

print("Done")
