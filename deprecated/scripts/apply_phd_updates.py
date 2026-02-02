import frontmatter
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")

UPDATES = {
    "016-jonathan-home": {
        "institution": "University of Oxford",
        "year": 2006,
        "advisor": "Andrew Steane",
        "note": None # Remove note
    },
    "007-dietrich-leibfried": {
        "institution": "Ludwig-Maximilians-University Munich",
        "year": 1995,
        "advisor": "Theodor W. Hänsch",
        "note": "Thesis research conducted at Max Planck Institute for Quantum Optics (MPQ)."
    },
    "008-john-bollinger": {
        "institution": "Harvard University",
        "year": 1981,
        "advisor": "Arthur Pipkin",
        "note": None
    },
    "009-hartmut-haeffner": {
        "institution": "University of Mainz",
        "year": 2000,
        "advisor": "Günter Werth",
        "note": "Advisor inferred from publications (e.g. PRL 85, 5304) and shared affiliation at Mainz; needs independent confirmation."
    },
    "010-jungsang-kim": {
        "institution": "Stanford University",
        "year": 1999,
        "advisor": "Yoshihisa Yamamoto",
        "note": None
    },
    "011-kihwan-kim": {
        "institution": "Seoul National University",
        "year": 2004,
        "advisor": "Wonho Jhe",
        "note": None
    },
    "012-winfried-hensinger": {
        "institution": "University of Queensland",
        "year": 2002,
        "advisor": "Halina Rubinsztein-Dunlop; Norman Heckenberg; Gerard Milburn",
        "note": None
    },
    "013-ferdinand-schmidt-kaler": {
        "institution": "Ludwig-Maximilians-University Munich",
        "year": 1992,
        "advisor": "Theodor W. Hänsch",
        "note": None
    },
    "014-thomas-monz": {
        "institution": "University of Innsbruck",
        "year": 2011,
        "advisor": "Rainer Blatt",
        "note": None
    }
}

def apply_updates():
    print("Applying PhD updates...")
    count = 0
    for filename_base, data in UPDATES.items():
        filename = f"{filename_base}.md"
        filepath = os.path.join(CONTENT_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found.")
            continue
            
        post = frontmatter.load(filepath)
        
        # Find PhD block
        updated = False
        if 'education' in post.metadata and isinstance(post.metadata['education'], list):
            for edu in post.metadata['education']:
                if 'degree' in edu and 'PhD' in edu['degree']:
                    # Update fields
                    edu['institution'] = data['institution']
                    edu['year'] = data['year']
                    edu['advisor'] = data['advisor']
                    
                    if data['note'] is None:
                        if 'note' in edu:
                            del edu['note']
                    else:
                        edu['note'] = data['note']
                    
                    updated = True
                    # Break after updating the first PhD block found
                    break
        
        if updated:
            with open(filepath, 'wb') as f:
                frontmatter.dump(post, f)
            print(f"Updated {filename}")
            count += 1
        else:
            print(f"Skipped {filename} (PhD block not found)")

    print(f"Applied updates to {count} files.")

if __name__ == "__main__":
    apply_updates()
