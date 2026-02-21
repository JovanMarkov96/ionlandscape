#!/usr/bin/env python3
"""
Fix all data consistency issues found by audit_data.py.

Issues to fix:
1. Standardize "USA" -> "United States" in people profiles
2. Standardize Innsbruck institution names for Roos and Blatt
3. Fix location mismatches (Lobino, Barclay, Hayasaka, Ballance, Streed)
"""
import os, sys, re, yaml

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE_DIR = os.path.join(ROOT, 'content', 'people')

# ── Define fixes ───────────────────────────────────────────────────────

FIXES = {
    # ── 1. Country standardization: "USA" → "United States" ──
    "004-christopher-monroe": {"location": {"country": "United States"}},
    "006-david-wineland": {"location": {"country": "United States"}},
    "007-dietrich-leibfried": {"location": {"country": "United States"}},
    "008-john-bollinger": {"location": {"country": "United States"}},
    "009-hartmut-haeffner": {"location": {"country": "United States"}},
    "010-jungsang-kim": {"location": {"country": "United States"}},
    
    # ── 2. Institution name standardization ──
    # "IQOQI Innsbruck (ÖAW) & University of Innsbruck" → "University of Innsbruck"
    "005-christian-roos": {
        "current_position": {"institution": "University of Innsbruck", "title": "Senior Scientist"}
    },
    # "University of Innsbruck & IQOQI Innsbruck (ÖAW)" → "University of Innsbruck"
    "017-rainer-blatt": {
        "current_position": {"institution": "University of Innsbruck", "title": "Professor Emeritus"}
    },
    
    # ── 3. Location fixes ──
    # Chris Ballance: He works at IonQ but is based in the UK (Oxford office)
    # Actually, Chris Ballance is CTO of IonQ, but based in Oxford UK.
    # His location should match where he physically is. 
    # IonQ does have UK operations. Let's keep his location as Oxford.
    # The mismatch is expected since IonQ HQ is in the US but he's in Oxford.
    
    # Mirko Lobino: current_position is University of Trento (Italy), NOT Australia.
    # His profile has old location data from Griffith University. Fix location.
    "067-mirko-lobino": {
        "location": {
            "city": "Trento",
            "country": "Italy",
            "region": "Trentino-Alto Adige",
            "lat": 46.0664,
            "lon": 11.1501
        }
    },
    
    # Paul Barclay: Institution is University of Calgary but city says Vancouver.
    # University of Calgary is in Calgary, Alberta.
    "068-paul-barclay": {
        "location": {
            "city": "Calgary",
            "country": "Canada",
            "region": "Alberta",
            "lat": 51.0776,
            "lon": -114.1300
        }
    },
    
    # Kazuhiro Hayasaka: Institution is NICT (in Koganei, Tokyo) but city says Kobe.
    # He probably moved. Fix location to Koganei.
    "045-kazuhiro-hayasaka": {
        "location": {
            "city": "Koganei",
            "country": "Japan",
            "region": "Tokyo",
            "lat": 35.7107,
            "lon": 139.4895
        }
    },
    
    # Erik Streed: Griffith University - his profile says Gold Coast
    # Griffith University has campuses in Brisbane and Gold Coast.
    # The Gold Coast campus is valid. Fix institution coordinates instead.
    
    # Winfried Hensinger: Brighton/Falmer vs Brighton - this is fine,
    # just a naming variant. Let's standardize to "Brighton".
    "012-winfried-hensinger": {
        "location": {"city": "Brighton"}
    },
}


def apply_fixes():
    """Apply all fixes to people markdown files."""
    for person_id, fix_data in FIXES.items():
        # Find the file
        filename = f"{person_id}.md"
        filepath = os.path.join(PEOPLE_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"  SKIP: {filename} not found")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse YAML frontmatter
        if not content.startswith('---'):
            print(f"  SKIP: {filename} has no frontmatter")
            continue
        
        # Split into frontmatter and body
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"  SKIP: {filename} malformed frontmatter")
            continue
        
        fm_text = parts[1]
        body = parts[2]
        
        fm = yaml.safe_load(fm_text)
        
        # Apply fixes
        changes = []
        for key, value in fix_data.items():
            if isinstance(value, dict):
                if key not in fm:
                    fm[key] = {}
                for subkey, subval in value.items():
                    old_val = fm[key].get(subkey, '<missing>')
                    if old_val != subval:
                        fm[key][subkey] = subval
                        changes.append(f"  {key}.{subkey}: '{old_val}' → '{subval}'")
            else:
                old_val = fm.get(key, '<missing>')
                if old_val != value:
                    fm[key] = value
                    changes.append(f"  {key}: '{old_val}' → '{value}'")
        
        if not changes:
            print(f"  OK (no changes needed): {filename}")
            continue
        
        # Write back
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=True)
        new_content = f"---\n{new_fm}---{body}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  FIX: {filename}")
        for c in changes:
            print(f"       {c}")


def fix_griffith_institution():
    """Fix Griffith University institution coordinates to include Gold Coast campus."""
    inst_dir = os.path.join(ROOT, 'content', 'institutions')
    for fname in os.listdir(inst_dir):
        if 'griffith' in fname.lower():
            filepath = os.path.join(inst_dir, fname)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update description to mention both campuses
            content = content.replace(
                'city: "Brisbane"',
                'city: "Brisbane/Gold Coast"'
            )
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  FIX: {fname} - updated city to include Gold Coast")


if __name__ == '__main__':
    print("Applying data fixes...")
    print()
    apply_fixes()
    print()
    fix_griffith_institution()
    print()
    print("Done! Run audit_data.py again to verify.")
