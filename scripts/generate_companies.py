#!/usr/bin/env python3
"""
Generate markdown profiles for known companies if they don't exist.
"""
import os
import json
import re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPANIES_DIR = os.path.join(ROOT, 'content', 'companies')

COMPANIES_DATA = {
    "c002-ionq": {
        "name": "IonQ",
        "sort_name": "IonQ",
        "aliases": ["IonQ, Inc.", "IonQ, Inc. (USA)"],
        "location": {
            "city": "College Park",
            "region": "Maryland",
            "country": "United States",
            "lat": 38.980,
            "lon": -76.920
        },
        "platforms": ["Trapped ions"],
        "short_summary": "Develops general-purpose trapped ion quantum computers and software.",
        "links": {"website": "https://ionq.com"}
    },
    "c003-alpine-quantum-technologies-aqt": {
        "name": "Alpine Quantum Technologies",
        "sort_name": "Alpine Quantum Technologies",
        "aliases": ["Alpine Quantum Technologies (AQT)", "AQT"],
        "location": {
            "city": "Innsbruck",
            "region": "Tyrol",
            "country": "Austria",
            "lat": 47.269,
            "lon": 11.393
        },
        "platforms": ["Trapped ions"],
        "short_summary": "A commercial provider of trapped-ion quantum computers.",
        "links": {"website": "https://www.aqt.eu"}
    },
    "c004-oxford-ionics": {
        "name": "Oxford Ionics",
        "sort_name": "Oxford Ionics",
        "aliases": ["Oxford Ionics"],
        "location": {
            "city": "Kidlington",
            "region": "Oxfordshire",
            "country": "United Kingdom",
            "lat": 51.826,
            "lon": -1.291
        },
        "platforms": ["Trapped ions"],
        "short_summary": "High-performance quantum computers based on trapped ions and electronic qubit control.",
        "links": {"website": "https://www.oxionics.com"}
    },
    "c005-q-ctrl": {
        "name": "Q-CTRL",
        "sort_name": "Q-CTRL",
        "aliases": ["Q-CTRL"],
        "location": {
            "city": "Sydney",
            "region": "New South Wales",
            "country": "Australia",
            "lat": -33.886,
            "lon": 151.200
        },
        "platforms": ["Software"],
        "short_summary": "Provides quantum control software to stabilize quantum hardware and accelerate quantum computing.",
        "links": {"website": "https://qctrl.com"}
    },
    "c006-quera-computing": {
        "name": "QuEra Computing",
        "sort_name": "QuEra Computing",
        "aliases": ["QuEra Computing Inc."],
        "location": {
            "city": "Boston",
            "region": "Massachusetts",
            "country": "United States",
            "lat": 42.360,
            "lon": -71.058
        },
        "platforms": ["Neutral atoms"],
        "short_summary": "Builder of advanced quantum computers based on neutral atoms.",
        "links": {"website": "https://www.quera.com"}
    }
}

def generate_companies():
    os.makedirs(COMPANIES_DIR, exist_ok=True)
    
    for c_id, data in COMPANIES_DATA.items():
        filepath = os.path.join(COMPANIES_DIR, f"{c_id}.md")
        if os.path.exists(filepath):
            print(f"Skipping {c_id}, already exists.")
            continue
            
        frontmatter = {
            "id": c_id,
            "name": data["name"],
            "sort_name": data["sort_name"],
            "entity_type": "company",
            "location": data["location"],
            "platforms": data["platforms"],
            "short_summary": data["short_summary"],
            "aliases": data["aliases"],
        }
        
        # Add basic skeleton fields
        frontmatter["people"] = {
            "founders": [],
            "leadership": [],
            "spun_out_of": []
        }
        frontmatter["status"] = {
            "operating_status": "active"
        }
        frontmatter["links"] = data["links"]
        frontmatter["media"] = {"logo_path": ""}
        frontmatter["sources"] = []
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(frontmatter, f, sort_keys=False, allow_unicode=True)
            f.write("---\n\n")
            
        print(f"Created {filepath}")

if __name__ == "__main__":
    generate_companies()
